from cluster_config import NODES
from surreal_client import run_sql, extract_rows, print_table

PAYMENT_METHOD = "Tiền Mặt"

def main():
    union_rows = []
    for node_name, url in NODES.items():
        sql = f"""
SELECT * FROM chi_tiet_hoa_don_theo_ma_kh
WHERE phuong_thuc_thanh_toan = '{PAYMENT_METHOD}'
LIMIT 5;
"""
        result = run_sql(node_name, url, sql, f"REQ2 Q5 - PAYMENT AUDIT ON {node_name}")
        rows = extract_rows(result)
        for row in rows:
            row["_source_node"] = node_name
            union_rows.append(row)

    print_table(
        union_rows,
        f"REQ2 Q5 - UNION PAYMENT METHOD AUDIT: {PAYMENT_METHOD}",
        limit=15
    )

if __name__ == "__main__":
    main()
