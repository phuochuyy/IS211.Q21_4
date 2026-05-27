from cluster_config import NODES
from surreal_client import run_sql, extract_rows, print_table

MIN_CUSTOMERS = 135

def main():
    union_rows = []
    for node_name, url in NODES.items():
        sql = f"""
SELECT * FROM sl_khach_hang_moi_ngay_theo_ma_cn
WHERE so_luong_khach_hang >= {MIN_CUSTOMERS}
LIMIT 5;
"""
        result = run_sql(node_name, url, sql, f"REQ2 Q7 - HIGH CUSTOMER TRAFFIC ON {node_name}")
        rows = extract_rows(result)
        for row in rows:
            row["_source_node"] = node_name
            union_rows.append(row)

    print_table(
        union_rows,
        f"REQ2 Q7 - UNION HIGH CUSTOMER TRAFFIC >= {MIN_CUSTOMERS}",
        limit=15
    )

if __name__ == "__main__":
    main()
