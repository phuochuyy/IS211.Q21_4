# Plant Paradise SurrealDB Source - CN3

## 1. Install Python dependencies

```powershell
cd C:\surreal-ddbs-demo
pip install -r requirements.txt
```

## 2. Create UI user for Surrealist

```powershell
.\00_create_ui_user.ps1
```

Surrealist connection:

```text
Protocol: HTTP
Address: 26.105.5.3:8000
Authentication: Database
Username: ui_admin
Password: ui_admin_123
Namespace: ddbs
Database: plant_paradise
```

## 3. Run local setup for Requirement [8]

```powershell
python 01_create_schema_local.py
python 02_seed_local_small.py
python 03_req1_verify_local_data.py
```

## 4. Test distributed connection for Requirement [9]

Run this on every node:

```powershell
python 04_req2_connection_matrix.py
```

## 5. Run 8 practical distributed queries

These files are separated so CMD output is easy to read:

```powershell
python 05_req2_q1_union_daily_revenue.py
python 06_req2_q2_inventory_range.py
python 07_req2_q3_high_employee_revenue.py
python 08_req2_q4_aggregate_summary.py
python 09_req2_q5_payment_method_audit.py
python 10_req2_q6_product_quarter_revenue.py
python 11_req2_q7_customer_traffic.py
python 12_req2_q8_customer_invoice_lookup.py
```

Query purpose:

1. Q1: Daily revenue by date across CN1/CN2/CN3.
2. Q2: Inventory range query for stock monitoring.
3. Q3: High employee revenue detection.
4. Q4: Distributed aggregate summary.
5. Q5: Payment method audit, e.g. cash transactions.
6. Q6: Product quarterly revenue across branches.
7. Q7: High customer traffic days for staffing/capacity.
8. Q8: Customer invoice lookup across branches.

## 6. Run distributed CRUD for Requirement [10]

Run these on all 3 machines:

```powershell
python 13_req3_create_remote_record.py
python 14_req3_update_remote_invoice.py
python 15_req3_delete_remote_record.py
```

Routing:

```text
CN1 client -> CN2 data
CN2 client -> CN3 data
CN3 client -> CN1 data
```

## 7. Surrealist UI role

Surrealist UI is used to view one node at a time:
- schema
- tables
- branch-local data
- before/after CRUD data

Python middleware is used for real distributed queries and union results.
