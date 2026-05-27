import requests
from requests.auth import HTTPBasicAuth
from tabulate import tabulate

from cluster_config import USER, PASSWORD, NAMESPACE, DATABASE

HEADERS = {
    "surreal-ns": NAMESPACE,
    "surreal-db": DATABASE,
    "Accept": "application/json",
}

def run_sql(node_name, url, sql, title=None, print_raw=False):
    if title:
        print(f"\n========== {title} ==========")

    response = requests.post(
        url,
        auth=HTTPBasicAuth(USER, PASSWORD),
        headers=HEADERS,
        data=sql.encode("utf-8"),
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()

    for item in result:
        if isinstance(item, dict) and item.get("status") == "ERR":
            raise RuntimeError(f"SurrealDB error on {node_name}: {item.get('result')}")

    if print_raw:
        print(result)

    return result

def extract_rows(result, statement_index=0):
    if not result or statement_index >= len(result):
        return []

    item = result[statement_index]
    rows = item.get("result", [])

    if rows is None:
        return []

    if isinstance(rows, list):
        return rows

    return [rows]

def print_table(rows, title="RESULT", limit=10):
    print(f"\n========== {title} ==========")

    if not rows:
        print("No data found")
        return

    display_rows = rows[:limit]
    print(tabulate(display_rows, headers="keys", tablefmt="fancy_grid"))

    if len(rows) > limit:
        print(f"... showing {limit}/{len(rows)} rows only")

def q(value):
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace("'", "\\'")
        return f"'{escaped}'"
    if value is None:
        return "NONE"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)

def upsert_statement(table, record_id, fields):
    assignments = []
    for key, value in fields.items():
        assignments.append(f"{key} = {q(value)}")
    return f"UPSERT {table}:{record_id} SET " + ", ".join(assignments) + ";"

def create_statement(table, record_id, fields):
    assignments = []
    for key, value in fields.items():
        assignments.append(f"{key} = {q(value)}")
    return f"CREATE {table}:{record_id} SET " + ", ".join(assignments) + ";"

def get_count(node_name, url, table_name):
    sql = f"SELECT count() AS total FROM {table_name} GROUP ALL;"
    result = run_sql(node_name, url, sql)
    rows = extract_rows(result)
    if rows:
        return rows[0].get("total", 0)
    return 0

def verify_record_all_nodes(nodes, table_name, record_id):
    rows = []
    for node_name, url in nodes.items():
        sql = f"SELECT * FROM {table_name}:{record_id};"
        result = run_sql(node_name, url, sql)
        found_rows = extract_rows(result)
        rows.append({
            "node": node_name,
            "record": f"{table_name}:{record_id}",
            "found": "YES" if found_rows else "NO",
        })
    print_table(rows, "VERIFY RECORD ON ALL NODES", limit=10)
