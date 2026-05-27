from cluster_config import NODES
from surreal_client import run_sql, extract_rows, print_table

QUERY_DATE = "2025-01-05"

def main():
    union_rows = []
    for node_name, url in NODES.items():
        sql = f"""
SELECT * FROM doanh_thu_moi_ngay_theo_ma_cn
WHERE ngay = '{QUERY_DATE}'
LIMIT 5;
"""
        result = run_sql(node_name, url, sql, f"REQ2 Q1 - DAILY REVENUE ON {node_name}")
        rows = extract_rows(result)
        for row in rows:
            row["_source_node"] = node_name
            union_rows.append(row)
    print_table(union_rows, f"REQ2 Q1 - UNION DAILY REVENUE FOR {QUERY_DATE}", limit=10)

if __name__ == "__main__":
    main()
