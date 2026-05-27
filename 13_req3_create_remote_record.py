from cluster_config import LOCAL_NODE, NODES, NEXT_NODE, BRANCH_BY_NODE
from surreal_client import run_sql, create_statement, verify_record_all_nodes

def main():
    target_node = NEXT_NODE[LOCAL_NODE]
    target_branch = BRANCH_BY_NODE[target_node]
    target_url = NODES[target_node]
    record_id = f"req3_create_from_{LOCAL_NODE.lower()}_to_{target_node.lower()}"

    fields = {
        "ma_chi_nhanh": target_branch,
        "ngay": "2025-02-01",
        "tong_tien": target_branch * 10_000_000 + 999_999,
        "ghi_chu": f"Created by {LOCAL_NODE}, routed to {target_node}",
    }

    sql = create_statement("doanh_thu_moi_ngay_theo_ma_cn", record_id, fields)
    run_sql(target_node, target_url, sql, f"REQ3 CREATE - {LOCAL_NODE} CREATES RECORD ON {target_node}", print_raw=True)
    verify_record_all_nodes(NODES, "doanh_thu_moi_ngay_theo_ma_cn", record_id)

if __name__ == "__main__":
    main()
