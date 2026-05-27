from cluster_config import NODES
from surreal_client import run_sql, extract_rows, print_table

def main():
    union_rows = []
    for node_name, url in NODES.items():
        sql = """
SELECT * FROM doanh_thu_thang_nv_cn
WHERE tong_doanh_thu >= 25000000
LIMIT 5;
"""
        result = run_sql(node_name, url, sql, f"REQ2 Q3 - HIGH EMPLOYEE REVENUE ON {node_name}")
        rows = extract_rows(result)
        for row in rows:
            row["_source_node"] = node_name
            union_rows.append(row)
    print_table(union_rows, "REQ2 Q3 - UNION HIGH EMPLOYEE REVENUE", limit=15)

if __name__ == "__main__":
    main()
