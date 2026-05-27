from cluster_config import LOCAL_NODE, NODES
from surreal_client import run_sql, extract_rows, print_table

def main():
    rows = []
    for node_name, url in NODES.items():
        try:
            sql = f"RETURN '{LOCAL_NODE} connected to {node_name}';"
            result = run_sql(node_name, url, sql, f"REQ2 - CONNECTION TEST {LOCAL_NODE} -> {node_name}")
            response_rows = extract_rows(result)
            rows.append({
                "client": LOCAL_NODE,
                "target_node": node_name,
                "status": "OK",
                "message": response_rows[0] if response_rows else "",
            })
        except Exception as exc:
            rows.append({
                "client": LOCAL_NODE,
                "target_node": node_name,
                "status": "FAILED",
                "message": str(exc),
            })
    print_table(rows, f"REQ2 - CONNECTION MATRIX FROM {LOCAL_NODE}", limit=10)

if __name__ == "__main__":
    main()
