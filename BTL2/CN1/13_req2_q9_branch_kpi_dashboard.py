from cluster_config import NODES
from surreal_client import run_sql, extract_rows, print_table

"""
REQ2 Q9 - HARD QUERY 1
Branch KPI Dashboard

Business question:
Which branch is performing well when we combine revenue, customer traffic,
invoice activity, cash-payment exposure, inventory risk, and employee revenue?

Distributed logic:
- Query 5 tables from each node.
- Aggregate each node locally in Python.
- Union the branch-level KPI rows into one system-wide dashboard.
"""

LOW_STOCK_LIMIT = 35


def fetch_rows(node_name, url, table_name):
    sql = f"SELECT * FROM {table_name};"
    result = run_sql(node_name, url, sql, f"REQ2 Q9 - FETCH {table_name} ON {node_name}")
    return extract_rows(result)


def safe_divide(a, b):
    return round(a / b, 2) if b else 0


def main():
    dashboard_rows = []

    for node_name, url in NODES.items():
        daily_revenue_rows = fetch_rows(node_name, url, "doanh_thu_moi_ngay_theo_ma_cn")
        customer_rows = fetch_rows(node_name, url, "sl_khach_hang_moi_ngay_theo_ma_cn")
        invoice_rows = fetch_rows(node_name, url, "chi_tiet_hoa_don_theo_ma_kh")
        inventory_rows = fetch_rows(node_name, url, "kho_sp_theo_ma_cn")
        employee_rows = fetch_rows(node_name, url, "doanh_thu_thang_nv_cn")

        total_revenue = sum(row.get("tong_tien", 0) for row in daily_revenue_rows)
        total_customers = sum(row.get("so_luong_khach_hang", 0) for row in customer_rows)
        invoice_count = len(invoice_rows)
        cash_invoice_count = sum(1 for row in invoice_rows if row.get("phuong_thuc_thanh_toan") == "Tiền Mặt")
        cash_ratio = safe_divide(cash_invoice_count * 100, invoice_count)
        low_stock_count = sum(1 for row in inventory_rows if row.get("tong_so_luong_ton_kho", 0) <= LOW_STOCK_LIMIT)
        top_employee_revenue = max([row.get("tong_doanh_thu", 0) for row in employee_rows] or [0])

        avg_revenue_per_customer = safe_divide(total_revenue, total_customers)
        avg_revenue_per_invoice = safe_divide(total_revenue, invoice_count)

        risk_level = "LOW"
        if low_stock_count >= 3 or cash_ratio >= 35:
            risk_level = "MEDIUM"
        if low_stock_count >= 5 or cash_ratio >= 50:
            risk_level = "HIGH"

        dashboard_rows.append({
            "node": node_name,
            "branch": daily_revenue_rows[0].get("ma_chi_nhanh") if daily_revenue_rows else "N/A",
            "total_revenue": total_revenue,
            "total_customers": total_customers,
            "avg_rev_per_customer": avg_revenue_per_customer,
            "invoice_count": invoice_count,
            "avg_rev_per_invoice": avg_revenue_per_invoice,
            "cash_ratio_%": cash_ratio,
            "low_stock_sku_count": low_stock_count,
            "top_employee_revenue": top_employee_revenue,
            "risk_level": risk_level,
        })

    dashboard_rows.sort(key=lambda row: row["total_revenue"], reverse=True)

    print_table(
        dashboard_rows,
        "REQ2 Q9 - DISTRIBUTED BRANCH KPI DASHBOARD",
        limit=10,
    )


if __name__ == "__main__":
    main()
