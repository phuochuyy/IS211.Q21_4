from cluster_config import NODES
from surreal_client import run_sql, extract_rows, print_table

PRODUCT_CODE = "CCNPLT0001"

def main():
    union_rows = []
    for node_name, url in NODES.items():
        sql = f"""
SELECT * FROM doanh_thu_sp_quy_cn
WHERE ma_san_pham = '{PRODUCT_CODE}'
LIMIT 5;
"""
        result = run_sql(node_name, url, sql, f"REQ2 Q6 - PRODUCT QUARTER REVENUE ON {node_name}")
        rows = extract_rows(result)
        for row in rows:
            row["_source_node"] = node_name
            union_rows.append(row)

    print_table(
        union_rows,
        f"REQ2 Q6 - UNION PRODUCT QUARTER REVENUE: {PRODUCT_CODE}",
        limit=15
    )

if __name__ == "__main__":
    main()
