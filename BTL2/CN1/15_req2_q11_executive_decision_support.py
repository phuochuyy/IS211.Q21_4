from cluster_config import NODES
from surreal_client import run_sql, extract_rows, print_table

"""
REQ2 Q11 - SUPER HARD QUERY
Executive Decision Support Report

Business question:
From all distributed nodes, generate a management-level action list:
- Which branch is strongest?
- Which branch needs attention?
- Which product should be restocked first?
- Which branch has high customer pressure?
- Which branch has high cash-payment exposure?

Distributed logic:
- Query 6 tables from every node.
- Combine operational, revenue, inventory, customer, product, and employee data.
- Calculate branch score and business recommendations in Python.
"""


def fetch(node_name, url, table_name):
    sql = f"SELECT * FROM {table_name};"
    result = run_sql(node_name, url, sql, f"REQ2 Q11 - FETCH {table_name} ON {node_name}")
    return extract_rows(result)


def safe_divide(a, b):
    return round(a / b, 2) if b else 0


def build_branch_profile(node_name, url):
    daily_revenue = fetch(node_name, url, "doanh_thu_moi_ngay_theo_ma_cn")
    customers = fetch(node_name, url, "sl_khach_hang_moi_ngay_theo_ma_cn")
    invoices = fetch(node_name, url, "chi_tiet_hoa_don_theo_ma_kh")
    inventory = fetch(node_name, url, "kho_sp_theo_ma_cn")
    product_revenue = fetch(node_name, url, "doanh_thu_sp_quy_cn")
    employee_revenue = fetch(node_name, url, "doanh_thu_thang_nv_cn")

    branch = None
    for source in [daily_revenue, customers, invoices, inventory, product_revenue, employee_revenue]:
        if source:
            branch = source[0].get("ma_chi_nhanh")
            break

    total_revenue = sum(row.get("tong_tien", 0) for row in daily_revenue)
    total_customers = sum(row.get("so_luong_khach_hang", 0) for row in customers)
    invoice_count = len(invoices)
    cash_count = sum(1 for row in invoices if row.get("phuong_thuc_thanh_toan") == "Tiền Mặt")
    cash_value = sum(row.get("tong_tien", 0) for row in invoices if row.get("phuong_thuc_thanh_toan") == "Tiền Mặt")
    low_stock_items = [row for row in inventory if row.get("tong_so_luong_ton_kho", 0) <= 35]

    peak_day = None
    if daily_revenue:
        peak_day = max(daily_revenue, key=lambda row: row.get("tong_tien", 0))

    top_employee = None
    if employee_revenue:
        top_employee = max(employee_revenue, key=lambda row: row.get("tong_doanh_thu", 0))

    top_product = None
    if product_revenue:
        top_product = max(product_revenue, key=lambda row: row.get("tong_doanh_thu", 0))

    first_3_days = sorted(daily_revenue, key=lambda row: row.get("ngay", ""))[:3]
    last_3_days = sorted(daily_revenue, key=lambda row: row.get("ngay", ""))[-3:]
    first_3_revenue = sum(row.get("tong_tien", 0) for row in first_3_days)
    last_3_revenue = sum(row.get("tong_tien", 0) for row in last_3_days)
    trend_change = safe_divide((last_3_revenue - first_3_revenue) * 100, first_3_revenue)

    branch_score = round(
        (total_revenue / 1_000_000)
        + (total_customers / 10)
        + (safe_divide(total_revenue, total_customers) / 10_000)
        - (len(low_stock_items) * 8)
        - (safe_divide(cash_count * 100, invoice_count) * 0.5),
        2,
    )

    return {
        "node": node_name,
        "branch": branch,
        "total_revenue": total_revenue,
        "total_customers": total_customers,
        "avg_rev_per_customer": safe_divide(total_revenue, total_customers),
        "invoice_count": invoice_count,
        "cash_ratio_%": safe_divide(cash_count * 100, invoice_count),
        "cash_value": cash_value,
        "low_stock_count": len(low_stock_items),
        "peak_day": peak_day.get("ngay") if peak_day else "N/A",
        "peak_day_revenue": peak_day.get("tong_tien", 0) if peak_day else 0,
        "top_employee": top_employee.get("ma_nhan_vien") if top_employee else "N/A",
        "top_employee_revenue": top_employee.get("tong_doanh_thu", 0) if top_employee else 0,
        "top_product": top_product.get("ma_san_pham") if top_product else "N/A",
        "top_product_revenue": top_product.get("tong_doanh_thu", 0) if top_product else 0,
        "trend_change_%": trend_change,
        "branch_score": branch_score,
        "low_stock_items": low_stock_items,
    }


def main():
    profiles = []
    for node_name, url in NODES.items():
        profiles.append(build_branch_profile(node_name, url))

    score_rows = []
    for profile in profiles:
        score_rows.append({
            "node": profile["node"],
            "branch": profile["branch"],
            "branch_score": profile["branch_score"],
            "total_revenue": profile["total_revenue"],
            "total_customers": profile["total_customers"],
            "avg_rev_per_customer": profile["avg_rev_per_customer"],
            "cash_ratio_%": profile["cash_ratio_%"],
            "low_stock_count": profile["low_stock_count"],
            "trend_change_%": profile["trend_change_%"],
        })

    score_rows.sort(key=lambda row: row["branch_score"], reverse=True)
    print_table(score_rows, "REQ2 Q11 - EXECUTIVE BRANCH SCOREBOARD", limit=10)

    strongest = max(profiles, key=lambda row: row["branch_score"])
    weakest = min(profiles, key=lambda row: row["branch_score"])
    highest_cash = max(profiles, key=lambda row: row["cash_ratio_%"])
    highest_customer_pressure = max(profiles, key=lambda row: row["total_customers"])

    all_low_stock = []
    for profile in profiles:
        for item in profile["low_stock_items"]:
            all_low_stock.append({
                "node": profile["node"],
                "branch": profile["branch"],
                "product": item.get("ma_san_pham"),
                "product_name": item.get("ten_san_pham"),
                "stock": item.get("tong_so_luong_ton_kho", 0),
            })
    all_low_stock.sort(key=lambda row: row["stock"])
    most_urgent_stock = all_low_stock[0] if all_low_stock else None

    recommendations = [
        {
            "priority": 1,
            "action": "Protect best branch performance",
            "target": f"{strongest['node']} / branch {strongest['branch']}",
            "reason": f"Highest branch_score={strongest['branch_score']} and revenue={strongest['total_revenue']}",
        },
        {
            "priority": 2,
            "action": "Investigate weaker branch",
            "target": f"{weakest['node']} / branch {weakest['branch']}",
            "reason": f"Lowest branch_score={weakest['branch_score']}; check stock, traffic, and payment mix",
        },
        {
            "priority": 3,
            "action": "Prepare staff/capacity plan",
            "target": f"{highest_customer_pressure['node']} / branch {highest_customer_pressure['branch']}",
            "reason": f"Highest customer traffic={highest_customer_pressure['total_customers']}",
        },
        {
            "priority": 4,
            "action": "Audit cash payment exposure",
            "target": f"{highest_cash['node']} / branch {highest_cash['branch']}",
            "reason": f"Highest cash_ratio={highest_cash['cash_ratio_%']}% and cash_value={highest_cash['cash_value']}",
        },
    ]

    if most_urgent_stock:
        recommendations.append({
            "priority": 5,
            "action": "Urgent restock",
            "target": f"{most_urgent_stock['node']} / {most_urgent_stock['product']}",
            "reason": f"Lowest stock={most_urgent_stock['stock']} for {most_urgent_stock['product_name']}",
        })

    print_table(recommendations, "REQ2 Q11 - EXECUTIVE ACTION RECOMMENDATIONS", limit=10)


if __name__ == "__main__":
    main()
