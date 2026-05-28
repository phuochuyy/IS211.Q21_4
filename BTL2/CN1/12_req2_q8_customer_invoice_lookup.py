from cluster_config import NODES, BRANCH_BY_NODE
from surreal_client import run_sql, extract_rows, print_table

def main():
    union_rows = []

    for node_name, url in NODES.items():
        branch = BRANCH_BY_NODE[node_name]
        customer_id = branch * 1000 + 502

        sql = f"""
SELECT * FROM chi_tiet_hoa_don_theo_ma_kh
WHERE ma_khach_hang = {customer_id}
LIMIT 5;
"""
        result = run_sql(node_name, url, sql, f"REQ2 Q8 - CUSTOMER INVOICE LOOKUP ON {node_name}")
        rows = extract_rows(result)

        for row in rows:
            row["_source_node"] = node_name
            union_rows.append(row)

    print_table(
        union_rows,
        "REQ2 Q8 - UNION CUSTOMER INVOICE LOOKUP",
        limit=15
    )

if __name__ == "__main__":
    main()
