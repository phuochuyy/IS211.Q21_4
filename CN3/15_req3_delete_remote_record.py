from cluster_config import LOCAL_NODE, NODES, NEXT_NODE
from surreal_client import run_sql, verify_record_all_nodes

def main():
    target_node = NEXT_NODE[LOCAL_NODE]
    target_url = NODES[target_node]
    record_id = f"req3_create_from_{LOCAL_NODE.lower()}_to_{target_node.lower()}"

    delete_sql = f"DELETE doanh_thu_moi_ngay_theo_ma_cn:{record_id};"
    run_sql(target_node, target_url, delete_sql, f"REQ3 DELETE - {LOCAL_NODE} DELETES RECORD ON {target_node}", print_raw=True)
    verify_record_all_nodes(NODES, "doanh_thu_moi_ngay_theo_ma_cn", record_id)

if __name__ == "__main__":
    main()
