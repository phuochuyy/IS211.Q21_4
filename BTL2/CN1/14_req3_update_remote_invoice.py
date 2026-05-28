from cluster_config import LOCAL_NODE, NODES, NEXT_NODE, BRANCH_BY_NODE
from surreal_client import run_sql, extract_rows, print_table, verify_record_all_nodes

def main():
    target_node = NEXT_NODE[LOCAL_NODE]
    target_branch = BRANCH_BY_NODE[target_node]
    target_url = NODES[target_node]
    record_id = f"cn{target_branch}_cthd_005"

    read_sql = f"SELECT * FROM chi_tiet_hoa_don_theo_ma_kh:{record_id};"

    before_result = run_sql(target_node, target_url, read_sql, f"REQ3 UPDATE - READ BEFORE UPDATE ON {target_node}")
    print_table(extract_rows(before_result), "BEFORE UPDATE", limit=3)

    update_sql = f"""
UPDATE chi_tiet_hoa_don_theo_ma_kh:{record_id} SET
    so_luong = 15,
    thanh_tien = 1500000,
    tong_tien = 1550000,
    phuong_thuc_thanh_toan = 'Chuyển Khoản',
    ghi_chu = 'Updated by {LOCAL_NODE}, routed to {target_node}';
"""
    run_sql(target_node, target_url, update_sql, f"REQ3 UPDATE - {LOCAL_NODE} UPDATES RECORD ON {target_node}", print_raw=True)

    after_result = run_sql(target_node, target_url, read_sql, f"REQ3 UPDATE - READ AFTER UPDATE ON {target_node}")
    print_table(extract_rows(after_result), "AFTER UPDATE", limit=3)

    verify_record_all_nodes(NODES, "chi_tiet_hoa_don_theo_ma_kh", record_id)

if __name__ == "__main__":
    main()
