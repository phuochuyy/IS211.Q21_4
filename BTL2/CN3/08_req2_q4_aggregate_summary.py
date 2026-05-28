from cluster_config import NODES
from surreal_client import run_sql, extract_rows, print_table

def main():
    summary_rows = []
    for node_name, url in NODES.items():
        revenue_sql = """
SELECT math::sum(tong_tien) AS total_daily_revenue
FROM doanh_thu_moi_ngay_theo_ma_cn
GROUP ALL;
"""
        invoice_sql = """
SELECT count() AS invoice_detail_count
FROM chi_tiet_hoa_don_theo_ma_kh
GROUP ALL;
"""
        revenue_result = run_sql(node_name, url, revenue_sql, f"REQ2 Q4 - TOTAL REVENUE ON {node_name}")
        invoice_result = run_sql(node_name, url, invoice_sql, f"REQ2 Q4 - INVOICE COUNT ON {node_name}")

        revenue_rows = extract_rows(revenue_result)
        invoice_rows = extract_rows(invoice_result)
        total_revenue = revenue_rows[0].get("total_daily_revenue", 0) if revenue_rows else 0
        invoice_count = invoice_rows[0].get("invoice_detail_count", 0) if invoice_rows else 0

        summary_rows.append({
            "node": node_name,
            "total_daily_revenue": total_revenue,
            "invoice_detail_count": invoice_count,
        })
    print_table(summary_rows, "REQ2 Q4 - DISTRIBUTED AGGREGATE SUMMARY", limit=10)

if __name__ == "__main__":
    main()
