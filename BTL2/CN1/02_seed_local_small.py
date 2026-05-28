from cluster_config import LOCAL_NODE, LOCAL_ENDPOINT, BRANCH_BY_NODE
from surreal_client import run_sql, upsert_statement, get_count, print_table

PRODUCTS = [
    ("CCNPLT0001", "Cây Monstera Mini"),
    ("CCNPLT0002", "Cây Lưỡi Hổ"),
    ("CCNPLT0003", "Cây Trầu Bà"),
    ("CCNPLT0004", "Cây Kim Tiền"),
    ("CCNPLT0005", "Cây Sen Đá"),
]

PAYMENTS = ["Tiền Mặt", "Chuyển Khoản", "Thẻ", "Ví Điện Tử"]

TABLES = [
    "chi_tiet_hoa_don_theo_ma_kh",
    "doanh_thu_moi_ngay_theo_ma_cn",
    "kho_sp_theo_ma_cn",
    "sl_khach_hang_moi_ngay_theo_ma_cn",
    "doanh_thu_sp_quy_cn",
    "doanh_thu_thang_nv_cn",
]

def seed_invoice_details(branch):
    statements = []
    for i in range(1, 16):
        customer_id = branch * 1000 + 500 + (i % 5)
        invoice_id = branch * 100000 + i
        product_code, _ = PRODUCTS[i % len(PRODUCTS)]
        quantity = (i % 4) + 1
        unit_price = 80000 + i * 15000
        line_total = quantity * unit_price
        invoice_total = line_total + 50000
        employee_id = branch * 100 + ((i % 2) + 1)
        day = (i % 10) + 1
        record_id = f"cn{branch}_cthd_{i:03d}"
        fields = {
            "ma_khach_hang": customer_id,
            "ma_hoa_don": invoice_id,
            "ma_san_pham": product_code,
            "so_luong": quantity,
            "thanh_tien": line_total,
            "tong_tien": invoice_total,
            "ngay_tao": f"2025-01-{day:02d}T10:00:00Z",
            "phuong_thuc_thanh_toan": PAYMENTS[i % len(PAYMENTS)],
            "ma_nhan_vien": employee_id,
            "ma_chi_nhanh": branch,
            "ghi_chu": f"Seed data CN{branch}",
        }
        statements.append(upsert_statement("chi_tiet_hoa_don_theo_ma_kh", record_id, fields))
    return statements

def seed_daily_revenue(branch):
    statements = []
    for day in range(1, 11):
        record_id = f"cn{branch}_rev_2025_01_{day:02d}"
        fields = {
            "ma_chi_nhanh": branch,
            "ngay": f"2025-01-{day:02d}",
            "tong_tien": 10_000_000 * branch + day * 250_000,
            "ghi_chu": f"Daily revenue CN{branch}",
        }
        statements.append(upsert_statement("doanh_thu_moi_ngay_theo_ma_cn", record_id, fields))
    return statements

def seed_inventory(branch):
    statements = []
    for i in range(1, 11):
        product_code, product_name = PRODUCTS[(i - 1) % len(PRODUCTS)]
        stock = 20 + branch * 5 + i * 3
        status = "Còn hàng" if stock >= 30 else "Sắp hết hàng"
        record_id = f"cn{branch}_kho_{i:03d}"
        fields = {
            "ma_chi_nhanh": branch,
            "ma_san_pham": product_code,
            "ten_san_pham": product_name,
            "tinh_trang": status,
            "tong_so_luong_danh_gia": 10 + i,
            "tong_so_luong_da_ban": 80 + branch * 10 + i,
            "tong_so_luong_ton_kho": stock,
        }
        statements.append(upsert_statement("kho_sp_theo_ma_cn", record_id, fields))
    return statements

def seed_daily_customers(branch):
    statements = []
    for day in range(1, 11):
        record_id = f"cn{branch}_cus_2025_01_{day:02d}"
        fields = {
            "ma_chi_nhanh": branch,
            "ngay": f"2025-01-{day:02d}",
            "so_luong_khach_hang": 100 + branch * 20 + day * 3,
        }
        statements.append(upsert_statement("sl_khach_hang_moi_ngay_theo_ma_cn", record_id, fields))
    return statements

def seed_product_quarter_revenue(branch):
    statements = []
    for product_index in range(1, 3):
        product_code, _ = PRODUCTS[product_index - 1]
        for quarter in range(1, 5):
            record_id = f"cn{branch}_spq_{product_index}_{quarter}"
            fields = {
                "ma_chi_nhanh": branch,
                "ma_san_pham": product_code,
                "nam": 2025,
                "quy": quarter,
                "tong_doanh_thu": 30_000_000 + branch * 3_000_000 + product_index * 1_000_000 + quarter * 500_000,
            }
            statements.append(upsert_statement("doanh_thu_sp_quy_cn", record_id, fields))
    return statements

def seed_employee_month_revenue(branch):
    statements = []
    for employee_no in range(1, 3):
        employee_id = branch * 100 + employee_no
        for month in range(1, 7):
            record_id = f"cn{branch}_nv_{employee_id}_{month:02d}"
            fields = {
                "ma_chi_nhanh": branch,
                "ma_nhan_vien": employee_id,
                "nam": 2025,
                "thang": month,
                "tong_doanh_thu": 20_000_000 + branch * 2_000_000 + employee_no * 1_000_000 + month * 700_000,
            }
            statements.append(upsert_statement("doanh_thu_thang_nv_cn", record_id, fields))
    return statements

def main():
    branch = BRANCH_BY_NODE[LOCAL_NODE]
    statements = []
    statements.extend(seed_invoice_details(branch))
    statements.extend(seed_daily_revenue(branch))
    statements.extend(seed_inventory(branch))
    statements.extend(seed_daily_customers(branch))
    statements.extend(seed_product_quarter_revenue(branch))
    statements.extend(seed_employee_month_revenue(branch))

    print(f"Seeding data for {LOCAL_NODE}, branch {branch}")
    print(f"Total statements: {len(statements)}")

    run_sql(LOCAL_NODE, LOCAL_ENDPOINT, "\n".join(statements), f"SEED LOCAL DATA ON {LOCAL_NODE}")

    count_rows = []
    for table in TABLES:
        count_rows.append({
            "node": LOCAL_NODE,
            "table": table,
            "record_count": get_count(LOCAL_NODE, LOCAL_ENDPOINT, table),
        })
    print_table(count_rows, "LOCAL DATA COUNT SUMMARY", limit=20)

if __name__ == "__main__":
    main()
