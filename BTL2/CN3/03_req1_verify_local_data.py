from cluster_config import LOCAL_NODE, LOCAL_ENDPOINT, BRANCH_BY_NODE
from surreal_client import run_sql, extract_rows, print_table, get_count

TABLES = [
    "chi_tiet_hoa_don_theo_ma_kh",
    "doanh_thu_moi_ngay_theo_ma_cn",
    "kho_sp_theo_ma_cn",
    "sl_khach_hang_moi_ngay_theo_ma_cn",
    "doanh_thu_sp_quy_cn",
    "doanh_thu_thang_nv_cn",
]

def show_db_info():
    run_sql(LOCAL_NODE, LOCAL_ENDPOINT, "INFO FOR DB;", f"REQ1 - INFO FOR DB ON {LOCAL_NODE}", print_raw=True)

def show_counts():
    rows = []
    for table in TABLES:
        rows.append({
            "node": LOCAL_NODE,
            "table": table,
            "record_count": get_count(LOCAL_NODE, LOCAL_ENDPOINT, table),
        })
    print_table(rows, f"REQ1 - RECORD COUNT ON {LOCAL_NODE}", limit=20)

def show_small_samples():
    branch = BRANCH_BY_NODE[LOCAL_NODE]
    sample_queries = {
        "doanh_thu_moi_ngay_theo_ma_cn": f"SELECT * FROM doanh_thu_moi_ngay_theo_ma_cn WHERE ma_chi_nhanh = {branch} LIMIT 3;",
        "chi_tiet_hoa_don_theo_ma_kh": f"SELECT * FROM chi_tiet_hoa_don_theo_ma_kh WHERE ma_chi_nhanh = {branch} LIMIT 3;",
        "kho_sp_theo_ma_cn": f"SELECT * FROM kho_sp_theo_ma_cn WHERE ma_chi_nhanh = {branch} LIMIT 3;",
    }
    for table_name, sql in sample_queries.items():
        result = run_sql(LOCAL_NODE, LOCAL_ENDPOINT, sql, f"REQ1 - SAMPLE {table_name}")
        rows = extract_rows(result)
        print_table(rows, f"SAMPLE {table_name}", limit=3)

def main():
    show_db_info()
    show_counts()
    show_small_samples()

if __name__ == "__main__":
    main()
