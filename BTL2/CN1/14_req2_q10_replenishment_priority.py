from cluster_config import NODES
from surreal_client import run_sql, extract_rows, print_table

"""
REQ2 Q10 - HARD QUERY 2
Product Replenishment Priority

Business question:
Which products should be restocked first when we combine low inventory with
quarterly product revenue across all branches?

Distributed logic:
- Query inventory table from each node.
- Query product-quarter revenue from each node.
- Join the two result sets in Python by branch + product.
- Calculate a replenishment priority score.
"""

YEAR = 2025
QUARTER = 2


def fetch_inventory(node_name, url):
    sql = """
SELECT * FROM kho_sp_theo_ma_cn;
"""
    result = run_sql(node_name, url, sql, f"REQ2 Q10 - FETCH INVENTORY ON {node_name}")
    return extract_rows(result)


def fetch_product_revenue(node_name, url):
    sql = f"""
SELECT * FROM doanh_thu_sp_quy_cn
WHERE nam = {YEAR} AND quy = {QUARTER};
"""
    result = run_sql(node_name, url, sql, f"REQ2 Q10 - FETCH PRODUCT REVENUE ON {node_name}")
    return extract_rows(result)


def main():
    priority_rows = []

    for node_name, url in NODES.items():
        inventory_rows = fetch_inventory(node_name, url)
        revenue_rows = fetch_product_revenue(node_name, url)

        revenue_by_product = {}
        for row in revenue_rows:
            key = (row.get("ma_chi_nhanh"), row.get("ma_san_pham"))
            revenue_by_product[key] = revenue_by_product.get(key, 0) + row.get("tong_doanh_thu", 0)

        inventory_by_product = {}
        for row in inventory_rows:
            key = (row.get("ma_chi_nhanh"), row.get("ma_san_pham"))
            item = inventory_by_product.setdefault(key, {
                "node": node_name,
                "branch": row.get("ma_chi_nhanh"),
                "product": row.get("ma_san_pham"),
                "product_name": row.get("ten_san_pham"),
                "total_stock": 0,
                "total_sold": 0,
                "inventory_rows": 0,
            })
            item["total_stock"] += row.get("tong_so_luong_ton_kho", 0)
            item["total_sold"] += row.get("tong_so_luong_da_ban", 0)
            item["inventory_rows"] += 1

        for key, item in inventory_by_product.items():
            quarter_revenue = revenue_by_product.get(key, 0)
            total_stock = item["total_stock"]
            total_sold = item["total_sold"]

            # Higher revenue and sales increase priority. Higher stock decreases priority.
            priority_score = round((quarter_revenue / 1_000_000) + (total_sold / 10) - (total_stock / 5), 2)

            if priority_score >= 45:
                action = "URGENT RESTOCK"
            elif priority_score >= 25:
                action = "MONITOR + RESTOCK"
            else:
                action = "NORMAL"

            priority_rows.append({
                "node": item["node"],
                "branch": item["branch"],
                "product": item["product"],
                "product_name": item["product_name"],
                "total_stock": total_stock,
                "total_sold": total_sold,
                "q2_revenue": quarter_revenue,
                "priority_score": priority_score,
                "suggested_action": action,
            })

    priority_rows.sort(key=lambda row: row["priority_score"], reverse=True)

    print_table(
        priority_rows,
        "REQ2 Q10 - DISTRIBUTED PRODUCT REPLENISHMENT PRIORITY",
        limit=12,
    )


if __name__ == "__main__":
    main()
