from cluster_config import LOCAL_NODE, LOCAL_ENDPOINT
from surreal_client import run_sql

TABLES = [
    "chi_tiet_hoa_don_theo_ma_kh",
    "doanh_thu_moi_ngay_theo_ma_cn",
    "kho_sp_theo_ma_cn",
    "sl_khach_hang_moi_ngay_theo_ma_cn",
    "doanh_thu_sp_quy_cn",
    "doanh_thu_thang_nv_cn",
]

def remove_old_tables():
    for table in TABLES:
        try:
            run_sql(LOCAL_NODE, LOCAL_ENDPOINT, f"REMOVE TABLE {table};", f"REMOVE OLD TABLE {table}")
        except Exception as exc:
            print(f"Skip removing {table}: {exc}")

def create_schema():
    schema_sql = """
DEFINE TABLE chi_tiet_hoa_don_theo_ma_kh SCHEMAFULL;
DEFINE FIELD ma_khach_hang ON TABLE chi_tiet_hoa_don_theo_ma_kh TYPE int;
DEFINE FIELD ma_hoa_don ON TABLE chi_tiet_hoa_don_theo_ma_kh TYPE int;
DEFINE FIELD ma_san_pham ON TABLE chi_tiet_hoa_don_theo_ma_kh TYPE string;
DEFINE FIELD so_luong ON TABLE chi_tiet_hoa_don_theo_ma_kh TYPE int;
DEFINE FIELD thanh_tien ON TABLE chi_tiet_hoa_don_theo_ma_kh TYPE int;
DEFINE FIELD tong_tien ON TABLE chi_tiet_hoa_don_theo_ma_kh TYPE int;
DEFINE FIELD ngay_tao ON TABLE chi_tiet_hoa_don_theo_ma_kh TYPE string;
DEFINE FIELD phuong_thuc_thanh_toan ON TABLE chi_tiet_hoa_don_theo_ma_kh TYPE string;
DEFINE FIELD ma_nhan_vien ON TABLE chi_tiet_hoa_don_theo_ma_kh TYPE int;
DEFINE FIELD ma_chi_nhanh ON TABLE chi_tiet_hoa_don_theo_ma_kh TYPE int;
DEFINE FIELD ghi_chu ON TABLE chi_tiet_hoa_don_theo_ma_kh TYPE string;
DEFINE INDEX idx_cthd_pk ON TABLE chi_tiet_hoa_don_theo_ma_kh FIELDS ma_khach_hang, ngay_tao, ma_hoa_don UNIQUE;
DEFINE INDEX idx_cthd_customer ON TABLE chi_tiet_hoa_don_theo_ma_kh FIELDS ma_khach_hang;
DEFINE INDEX idx_cthd_payment ON TABLE chi_tiet_hoa_don_theo_ma_kh FIELDS phuong_thuc_thanh_toan;

DEFINE TABLE doanh_thu_moi_ngay_theo_ma_cn SCHEMAFULL;
DEFINE FIELD ma_chi_nhanh ON TABLE doanh_thu_moi_ngay_theo_ma_cn TYPE int;
DEFINE FIELD ngay ON TABLE doanh_thu_moi_ngay_theo_ma_cn TYPE string;
DEFINE FIELD tong_tien ON TABLE doanh_thu_moi_ngay_theo_ma_cn TYPE int;
DEFINE FIELD ghi_chu ON TABLE doanh_thu_moi_ngay_theo_ma_cn TYPE string;
DEFINE INDEX idx_dt_ngay_pk ON TABLE doanh_thu_moi_ngay_theo_ma_cn FIELDS ma_chi_nhanh, ngay UNIQUE;
DEFINE INDEX idx_dt_ngay ON TABLE doanh_thu_moi_ngay_theo_ma_cn FIELDS ngay;

DEFINE TABLE kho_sp_theo_ma_cn SCHEMAFULL;
DEFINE FIELD ma_chi_nhanh ON TABLE kho_sp_theo_ma_cn TYPE int;
DEFINE FIELD ma_san_pham ON TABLE kho_sp_theo_ma_cn TYPE string;
DEFINE FIELD ten_san_pham ON TABLE kho_sp_theo_ma_cn TYPE string;
DEFINE FIELD tinh_trang ON TABLE kho_sp_theo_ma_cn TYPE string;
DEFINE FIELD tong_so_luong_danh_gia ON TABLE kho_sp_theo_ma_cn TYPE int;
DEFINE FIELD tong_so_luong_da_ban ON TABLE kho_sp_theo_ma_cn TYPE int;
DEFINE FIELD tong_so_luong_ton_kho ON TABLE kho_sp_theo_ma_cn TYPE int;
DEFINE INDEX idx_kho_pk ON TABLE kho_sp_theo_ma_cn FIELDS ma_chi_nhanh, ma_san_pham, tong_so_luong_ton_kho UNIQUE;
DEFINE INDEX idx_kho_product ON TABLE kho_sp_theo_ma_cn FIELDS ma_san_pham;
DEFINE INDEX idx_kho_stock ON TABLE kho_sp_theo_ma_cn FIELDS tong_so_luong_ton_kho;

DEFINE TABLE sl_khach_hang_moi_ngay_theo_ma_cn SCHEMAFULL;
DEFINE FIELD ma_chi_nhanh ON TABLE sl_khach_hang_moi_ngay_theo_ma_cn TYPE int;
DEFINE FIELD ngay ON TABLE sl_khach_hang_moi_ngay_theo_ma_cn TYPE string;
DEFINE FIELD so_luong_khach_hang ON TABLE sl_khach_hang_moi_ngay_theo_ma_cn TYPE int;
DEFINE INDEX idx_cus_day_pk ON TABLE sl_khach_hang_moi_ngay_theo_ma_cn FIELDS ma_chi_nhanh, ngay UNIQUE;
DEFINE INDEX idx_cus_amount ON TABLE sl_khach_hang_moi_ngay_theo_ma_cn FIELDS so_luong_khach_hang;

DEFINE TABLE doanh_thu_sp_quy_cn SCHEMAFULL;
DEFINE FIELD ma_chi_nhanh ON TABLE doanh_thu_sp_quy_cn TYPE int;
DEFINE FIELD ma_san_pham ON TABLE doanh_thu_sp_quy_cn TYPE string;
DEFINE FIELD nam ON TABLE doanh_thu_sp_quy_cn TYPE int;
DEFINE FIELD quy ON TABLE doanh_thu_sp_quy_cn TYPE int;
DEFINE FIELD tong_doanh_thu ON TABLE doanh_thu_sp_quy_cn TYPE int;
DEFINE INDEX idx_dt_sp_quy_pk ON TABLE doanh_thu_sp_quy_cn FIELDS ma_chi_nhanh, ma_san_pham, nam, quy UNIQUE;
DEFINE INDEX idx_dt_sp_product ON TABLE doanh_thu_sp_quy_cn FIELDS ma_san_pham;
DEFINE INDEX idx_dt_sp_revenue ON TABLE doanh_thu_sp_quy_cn FIELDS tong_doanh_thu;

DEFINE TABLE doanh_thu_thang_nv_cn SCHEMAFULL;
DEFINE FIELD ma_chi_nhanh ON TABLE doanh_thu_thang_nv_cn TYPE int;
DEFINE FIELD ma_nhan_vien ON TABLE doanh_thu_thang_nv_cn TYPE int;
DEFINE FIELD nam ON TABLE doanh_thu_thang_nv_cn TYPE int;
DEFINE FIELD thang ON TABLE doanh_thu_thang_nv_cn TYPE int;
DEFINE FIELD tong_doanh_thu ON TABLE doanh_thu_thang_nv_cn TYPE int;
DEFINE INDEX idx_dt_nv_month_pk ON TABLE doanh_thu_thang_nv_cn FIELDS ma_chi_nhanh, ma_nhan_vien, nam, thang UNIQUE;
DEFINE INDEX idx_dt_nv_revenue ON TABLE doanh_thu_thang_nv_cn FIELDS tong_doanh_thu;
"""
    run_sql(LOCAL_NODE, LOCAL_ENDPOINT, schema_sql, f"CREATE SCHEMA ON {LOCAL_NODE}")

def main():
    print(f"Creating schema on local node: {LOCAL_NODE}")
    remove_old_tables()
    create_schema()
    print("Schema created successfully.")

if __name__ == "__main__":
    main()
