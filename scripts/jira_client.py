import os
import re
import sys
import json
import base64
import urllib.request
import urllib.error


def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ[k.strip()] = v.strip()


def get_headers():
    load_env()
    email = os.environ.get("JIRA_EMAIL")
    token = os.environ.get("JIRA_API_TOKEN")
    if not email or not token:
        print("Error: Faltan JIRA_EMAIL o JIRA_API_TOKEN en el archivo .env")
        sys.exit(1)
    auth = base64.b64encode(f"{email}:{token}".encode("utf-8")).decode("utf-8")
    return {
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


def extract_text(node):
    if not isinstance(node, dict):
        return ""
    text = node.get("text", "")
    for child in node.get("content", []):
        text += extract_text(child)
    if node.get("type") in ("paragraph", "listItem", "heading"):
        text += "\n"
    return text


def parse_inline(text):
    """Convierte **negritas** y `código` a nodos inline de ADF."""
    nodes = []
    tokens = re.split(r'(\*\*.*?\*\*|`.*?`)', text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith('**') and tok.endswith('**') and len(tok) > 4:
            nodes.append({"type": "text", "text": tok[2:-2], "marks": [{"type": "strong"}]})
        elif tok.startswith('`') and tok.endswith('`') and len(tok) > 2:
            nodes.append({"type": "text", "text": tok[1:-1], "marks": [{"type": "code"}]})
        else:
            nodes.append({"type": "text", "text": tok})
    return nodes or [{"type": "text", "text": " "}]


def normalize_markdown(md_text):
    """Reconstruye saltos de línea si la terminal o Copilot aplastó la tabla en una sola línea."""
    text = md_text.replace('\\n', '\n')
    # Si detecta separadores de tabla |---|---| pegados sin saltos de línea, los separa
    text = re.sub(r'\|\s*\|', '|\n|', text)
    # Separa el título si quedó pegado justo antes del primer | de la tabla
    text = re.sub(r'([^\n|])\s*(\|[^|\n]+\|)', r'\1\n\2', text, count=1)
    return text


def markdown_to_adf(md_text):
    """Convierte Markdown (tablas, títulos, listas y párrafos) a Atlassian Document Format."""
    lines = normalize_markdown(md_text).splitlines()
    content = []
    i = 0


    while i < len(lines):
        line = lines[i].strip()


        if not line:
            i += 1
            continue


        # 1. Tablas Markdown
        if line.startswith('|') and line.endswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
                table_lines.append(lines[i].strip())
                i += 1


            rows = []
            for idx, tline in enumerate(table_lines):
                cells = [c.strip() for c in tline.strip('|').split('|')]
                # Ignorar línea separadora |---|---|
                if all(re.match(r'^:?-+:?$', c.replace(' ', '')) for c in cells if c):
                    continue
                is_header = (idx == 0)
                cell_type = "tableHeader" if is_header else "tableCell"
                row_cells = []
                for cell in cells:
                    row_cells.append({
                        "type": cell_type,
                        "attrs": {},
                        "content": [{"type": "paragraph", "content": parse_inline(cell)}]
                    })
                rows.append({"type": "tableRow", "content": row_cells})


            if rows:
                content.append({
                    "type": "table",
                    "attrs": {"isNumberColumnEnabled": False, "layout": "default"},
                    "content": rows
                })
            continue


        # 2. Encabezados (#, ##, ###)
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            content.append({
                "type": "heading",
                "attrs": {"level": level},
                "content": parse_inline(text)
            })
            i += 1
            continue


        # 3. Listas con viñetas (- o *)
        if re.match(r'^[-*]\s+', line):
            list_items = []
            while i < len(lines) and re.match(r'^[-*]\s+', lines[i].strip()):
                item_text = re.sub(r'^[-*]\s+', '', lines[i].strip())
                list_items.append({
                    "type": "listItem",
                    "content": [{"type": "paragraph", "content": parse_inline(item_text)}]
                })
                i += 1
            content.append({"type": "bulletList", "content": list_items})
            continue


        # 4. Párrafo estándar
        content.append({"type": "paragraph", "content": parse_inline(line)})
        i += 1


    return {
        "type": "doc",
        "version": 1,
        "content": content or [{"type": "paragraph", "content": [{"type": "text", "text": md_text}]}]
    }


def get_issue(issue_key):
    load_env()
    base_url = os.environ.get("JIRA_URL", "").rstrip("/")
    url = f"{base_url}/rest/api/3/issue/{issue_key}"
    req = urllib.request.Request(url, headers=get_headers())
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            fields = data.get("fields", {})
            summary = fields.get("summary", "Sin título")
            desc = extract_text(fields.get("description", {})).strip()
            status = fields.get("status", {}).get("name", "Desconocido")
            print(f"=== TICKET: {issue_key} ===")
            print(f"Estado: {status}")
            print(f"Título: {summary}\n")
            print(f"Descripción y Criterios de Aceptación:\n{desc}")
    except urllib.error.HTTPError as e:
        print(f"Error al consultar Jira ({e.code}): {e.read().decode()}")


def get_sprint_issues(sprint_query):
    load_env()
    base_url = os.environ.get("JIRA_URL", "").rstrip("/")
    if sprint_query.lower() == "active":
        jql = "sprint in openSprints() ORDER BY key ASC"
    else:
        jql = f'sprint = "{sprint_query}" ORDER BY key ASC'


    url = f"{base_url}/rest/api/3/search/jql"
    payload = {
        "jql": jql,
        "fields": ["summary", "description", "status", "issuetype"]
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=get_headers(),
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            issues = data.get("issues", [])
            if not issues:
                print(f"No se encontraron historias para el sprint: {sprint_query}")
                return
            print(f"=== HISTORIAS DEL SPRINT ({sprint_query}) - Total: {len(issues)} ===\n")
            for issue in issues:
                key = issue.get("key")
                fields = issue.get("fields", {})
                itype = fields.get("issuetype", {}).get("name", "Issue")
                status = fields.get("status", {}).get("name", "")
                summary = fields.get("summary", "Sin título")
                desc = extract_text(fields.get("description", {})).strip()
                print(f"[{key}] ({itype} - {status}) {summary}")
                print(f"Descripción:\n{desc}\n" + "-" * 50)
    except urllib.error.HTTPError as e:
        print(f"Error al consultar el Sprint ({e.code}): {e.read().decode()}")


def add_comment(issue_key, comment_text):
    load_env()
    base_url = os.environ.get("JIRA_URL", "").rstrip("/")
    url = f"{base_url}/rest/api/3/issue/{issue_key}/comment"
    payload = {
        "body": markdown_to_adf(comment_text)
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=get_headers(),
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status in (200, 201):
                print(f"✅ Comentario con formato nativo publicado exitosamente en {issue_key}.")
    except urllib.error.HTTPError as e:
        print(f"Error al publicar comentario ({e.code}): {e.read().decode()}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso:")
        print("  Leer ticket:         python scripts/jira_client.py get QAAIW-1")
        print("  Leer sprint:         python scripts/jira_client.py sprint active")
        print("  Comentar texto:      python scripts/jira_client.py comment QAAIW-1 'Texto'")
        print("  Comentar desde md:   python scripts/jira_client.py comment-file QAAIW-1 salida.md")
        sys.exit(1)


    action = sys.argv[1].lower()
    target = sys.argv[2]


    if action == "get":
        get_issue(target.upper())
    elif action == "sprint":
        get_sprint_issues(target)
    elif action == "comment" and len(sys.argv) >= 4:
        add_comment(target.upper(), sys.argv[3])
    elif action == "comment-file" and len(sys.argv) >= 4:
        with open(sys.argv[3], 'r', encoding='utf-8') as f:
            add_comment(target.upper(), f.read())