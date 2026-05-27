# Plant Paradise - Distributed NoSQL Demo with SurrealDB

Dự án này minh chứng mô hình **NoSQL phân tán 3 máy** sử dụng **SurrealDB + Python middleware + Surrealist UI** cho bài tập cơ sở dữ liệu phân tán.


---

## 1. Mục tiêu bài demo

Dự án đáp ứng 3 nhóm yêu cầu chính:

| Requirement | Nội dung minh chứng |
|---|---|
| Req [8] | Cài đặt SurrealDB, tạo schema NoSQL, seed dữ liệu mẫu |
| Req [9] | Truy vấn phân tán trên 3 máy bằng Python middleware |
| Req [10] | CRUD phân tán: máy này tạo/sửa/xóa dữ liệu trên máy khác |
---

## 2. Mô hình hệ thống

Hệ thống gồm 3 máy/chi nhánh:

| Node | IP | Chi nhánh | Dữ liệu lưu trữ |
|---|---|---:|---|
| CN1 | `26.41.51.255` | 1 | Dữ liệu có `ma_chi_nhanh = 1` |
| CN2 | `26.201.116.10` | 2 | Dữ liệu có `ma_chi_nhanh = 2` |
| CN3 | `26.105.5.3` | 3 | Dữ liệu có `ma_chi_nhanh = 3` |

Mỗi node chạy một **SurrealDB instance độc lập** bằng Docker. Dữ liệu được phân mảnh theo chi nhánh, không dùng chung storage và không tự động nhân bản.

---

## 3. Vai trò của từng thành phần

| Thành phần | Vai trò |
|---|---|
| SurrealDB | Lưu trữ dữ liệu NoSQL trên từng node |
| Docker | Chạy SurrealDB server trên từng máy |
| Python middleware | Kết nối đến CN1, CN2, CN3; chạy query từng node; union kết quả |
| Surrealist UI | Quan sát schema/data trực quan trên từng node |

Lưu ý: **Surrealist không phải distributed query engine**. Surrealist chỉ query được node đang connect. Phần query toàn hệ thống được thực hiện bằng Python.

---

## 4. Công nghệ sử dụng

- SurrealDB
- Docker Desktop
- Python 3
- Python libraries:
  - `requests`
  - `tabulate`
- Surrealist Desktop/Web UI
- PowerShell trên Windows

---

## 5. Cấu trúc source code

```text
.
├── cluster_config.py
├── surreal_client.py
├── requirements.txt
├── 00_create_ui_user.ps1
├── 00_test_local_and_cross_connection.ps1
├── 01_create_schema_local.py
├── 02_seed_local_small.py
├── 03_req1_verify_local_data.py
├── 04_req2_connection_matrix.py
├── 05_req2_q1_union_daily_revenue.py
├── 06_req2_q2_inventory_range.py
├── 07_req2_q3_high_employee_revenue.py
├── 08_req2_q4_aggregate_summary.py
├── 09_req2_q5_payment_method_audit.py
├── 10_req2_q6_product_quarter_revenue.py
├── 11_req2_q7_customer_traffic.py
├── 12_req2_q8_customer_invoice_lookup.py
├── 13_req3_create_remote_record.py
├── 14_req3_update_remote_invoice.py
├── 15_req3_delete_remote_record.py
├── surrealist_ui_queries.sql
└── README.md
```

---

## 6. Cấu hình từng máy

Trong file `cluster_config.py`, mỗi máy cần có `LOCAL_NODE` đúng với node đang chạy.

### CN1

```python
LOCAL_NODE = "CN1"
```

### CN2

```python
LOCAL_NODE = "CN2"
```

### CN3

```python
LOCAL_NODE = "CN3"
```

Các endpoint chính:

```python
NODES = {
    "CN1": "http://26.41.51.255:8000/sql",
    "CN2": "http://26.201.116.10:8000/sql",
    "CN3": "http://26.105.5.3:8000/sql",
}
```

---

## 7. Cài đặt SurrealDB bằng Docker

Chạy trên từng máy.

### CN1

```powershell
docker pull surrealdb/surrealdb:latest

docker volume create surreal_cn1_data

docker run -d --name surreal-cn1 --user root --restart unless-stopped -p 8000:8000 -v surreal_cn1_data:/data -w /data surrealdb/surrealdb:latest start --bind 0.0.0.0:8000 --user root --pass root surrealkv://database
```

### CN2

```powershell
docker pull surrealdb/surrealdb:latest

docker volume create surreal_cn2_data

docker run -d --name surreal-cn2 --user root --restart unless-stopped -p 8000:8000 -v surreal_cn2_data:/data -w /data surrealdb/surrealdb:latest start --bind 0.0.0.0:8000 --user root --pass root surrealkv://database
```

### CN3

```powershell
docker pull surrealdb/surrealdb:latest

docker volume create surreal_cn3_data

docker run -d --name surreal-cn3 --user root --restart unless-stopped -p 8000:8000 -v surreal_cn3_data:/data -w /data surrealdb/surrealdb:latest start --bind 0.0.0.0:8000 --user root --pass root surrealkv://database
```

Mở firewall port 8000 trên từng máy:

```powershell
New-NetFirewallRule -DisplayName "SurrealDB Port 8000" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

Kiểm tra container:

```powershell
docker ps
```

---

## 8. Cài thư viện Python

Vào folder source code:

```powershell
cd C:\surreal-ddbs-demo
pip install -r requirements.txt
```

Nếu `pip` không chạy:

```powershell
py -m pip install -r requirements.txt
```

---

## 9. Tạo user cho Surrealist UI

Chạy trên từng máy:

```powershell
.\00_create_ui_user.ps1
```

Nếu PowerShell chặn script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\00_create_ui_user.ps1
```

Thông tin đăng nhập Surrealist:

```text
Authentication: Database
Username: ui_admin
Password: ui_admin_123
Namespace: ddbs
Database: plant_paradise
```

---

## 10. Cấu hình Surrealist UI

Tạo 3 connection:

### CN1

```text
Connection name: CN1 - Plant Paradise
Protocol: HTTP
Address: 26.41.51.255:8000
Authentication: Database
Username: ui_admin
Password: ui_admin_123
Namespace: ddbs
Database: plant_paradise
```

### CN2

```text
Connection name: CN2 - Plant Paradise
Protocol: HTTP
Address: 26.201.116.10:8000
Authentication: Database
Username: ui_admin
Password: ui_admin_123
Namespace: ddbs
Database: plant_paradise
```

### CN3

```text
Connection name: CN3 - Plant Paradise
Protocol: HTTP
Address: 26.105.5.3:8000
Authentication: Database
Username: ui_admin
Password: ui_admin_123
Namespace: ddbs
Database: plant_paradise
```

Test trong Surrealist:

```sql
RETURN 'Connected from Surrealist UI';
INFO FOR DB;
```

---

## 11. Requirement [8] - Tạo schema và seed dữ liệu local

Chạy trên **cả 3 máy CN1, CN2, CN3**.

```powershell
cd C:\surreal-ddbs-demo
python 01_create_schema_local.py
python 02_seed_local_small.py
python 03_req1_verify_local_data.py
```

Nếu dùng `py` thay cho `python`:

```powershell
py 01_create_schema_local.py
py 02_seed_local_small.py
py 03_req1_verify_local_data.py
```

Kết quả đúng:

| Máy | Dữ liệu đúng |
|---|---|
| CN1 | `ma_chi_nhanh = 1`, record id bắt đầu bằng `cn1_` |
| CN2 | `ma_chi_nhanh = 2`, record id bắt đầu bằng `cn2_` |
| CN3 | `ma_chi_nhanh = 3`, record id bắt đầu bằng `cn3_` |

Lưu ý: `01_create_schema_local.py` sẽ xóa bảng cũ và tạo lại schema mới. Nếu không muốn mất dữ liệu cũ thì không chạy file này.

---

## 12. Requirement [9] - Kiểm tra kết nối phân tán

Chạy trên **cả 3 máy**:

```powershell
python 04_req2_connection_matrix.py
```

Kết quả mong đợi:

```text
CN1 -> CN1 OK
CN1 -> CN2 OK
CN1 -> CN3 OK
```

```text
CN2 -> CN1 OK
CN2 -> CN2 OK
CN2 -> CN3 OK
```

```text
CN3 -> CN1 OK
CN3 -> CN2 OK
CN3 -> CN3 OK
```

---

## 13. Requirement [9] - 8 query phân tán

Chạy trên **CN1** là đủ để demo, vì Python trên CN1 sẽ kết nối đến CN1, CN2, CN3 và union kết quả.

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

Ý nghĩa từng query:

| File | Ý nghĩa thực tế |
|---|---|
| `05_req2_q1_union_daily_revenue.py` | Xem doanh thu theo ngày trên toàn hệ thống |
| `06_req2_q2_inventory_range.py` | Tìm sản phẩm có tồn kho trong khoảng cần theo dõi |
| `07_req2_q3_high_employee_revenue.py` | Tìm nhân viên có doanh thu cao |
| `08_req2_q4_aggregate_summary.py` | Tổng hợp doanh thu và số hóa đơn theo từng node |
| `09_req2_q5_payment_method_audit.py` | Kiểm tra giao dịch theo phương thức thanh toán |
| `10_req2_q6_product_quarter_revenue.py` | Xem doanh thu sản phẩm theo quý |
| `11_req2_q7_customer_traffic.py` | Tìm ngày có lượng khách cao |
| `12_req2_q8_customer_invoice_lookup.py` | Tra cứu lịch sử hóa đơn theo khách hàng |

---

## 14. Requirement [10] - CRUD phân tán

Routing CRUD hiện tại:

| Máy chạy script | Node bị thao tác |
|---|---|
| CN1 | CN2 |
| CN2 | CN3 |
| CN3 | CN1 |

---

### 14.1. CN1 thao tác dữ liệu trên CN2

Chạy trên **CN1**:

```powershell
python 13_req3_create_remote_record.py
python 14_req3_update_remote_invoice.py
python 15_req3_delete_remote_record.py
```

Kết quả mong đợi:

```text
CREATE: record được tạo trên CN2
UPDATE: record cn2_cthd_005 được update trên CN2
DELETE: record demo CN1 -> CN2 bị xóa khỏi CN2
```

Check bằng Surrealist CN2:

```sql
SELECT * FROM doanh_thu_moi_ngay_theo_ma_cn:req3_create_from_cn1_to_cn2;
SELECT * FROM chi_tiet_hoa_don_theo_ma_kh:cn2_cthd_005;
```

---

### 14.2. CN2 thao tác dữ liệu trên CN3

Chạy trên **CN2**:

```powershell
python 13_req3_create_remote_record.py
python 14_req3_update_remote_invoice.py
python 15_req3_delete_remote_record.py
```

Kết quả mong đợi:

```text
CREATE: record được tạo trên CN3
UPDATE: record cn3_cthd_005 được update trên CN3
DELETE: record demo CN2 -> CN3 bị xóa khỏi CN3
```

Check bằng Surrealist CN3:

```sql
SELECT * FROM doanh_thu_moi_ngay_theo_ma_cn:req3_create_from_cn2_to_cn3;
SELECT * FROM chi_tiet_hoa_don_theo_ma_kh:cn3_cthd_005;
```

---

### 14.3. CN3 thao tác dữ liệu trên CN1

Chạy trên **CN3**:

```powershell
python 13_req3_create_remote_record.py
python 14_req3_update_remote_invoice.py
python 15_req3_delete_remote_record.py
```

Kết quả mong đợi:

```text
CREATE: record được tạo trên CN1
UPDATE: record cn1_cthd_005 được update trên CN1
DELETE: record demo CN3 -> CN1 bị xóa khỏi CN1
```

Check bằng Surrealist CN1:

```sql
SELECT * FROM doanh_thu_moi_ngay_theo_ma_cn:req3_create_from_cn3_to_cn1;
SELECT * FROM chi_tiet_hoa_don_theo_ma_kh:cn1_cthd_005;
```

---

## 15. Lệnh Surrealist để kiểm tra dữ liệu phân mảnh

### Check CN1

```sql
SELECT * FROM doanh_thu_moi_ngay_theo_ma_cn
WHERE ma_chi_nhanh = 1
LIMIT 5;
```

### Check CN2

```sql
SELECT * FROM doanh_thu_moi_ngay_theo_ma_cn
WHERE ma_chi_nhanh = 2
LIMIT 5;
```

### Check CN3

```sql
SELECT * FROM doanh_thu_moi_ngay_theo_ma_cn
WHERE ma_chi_nhanh = 3
LIMIT 5;
```

Để chứng minh không nhân bản, vào CN1 thử query dữ liệu của CN2:

```sql
SELECT * FROM doanh_thu_moi_ngay_theo_ma_cn
WHERE ma_chi_nhanh = 2
LIMIT 5;
```

Kết quả đúng: rỗng.

---

## 16. Thứ tự quay video đề xuất

### Bước 1: Chứng minh server đang chạy

Trên CN1/CN2/CN3:

```powershell
docker ps
```

### Bước 2: Chứng minh dữ liệu local từng chi nhánh

Trên CN1/CN2/CN3:

```powershell
python 03_req1_verify_local_data.py
```

### Bước 3: Chứng minh kết nối 3 máy

Trên CN1/CN2/CN3:

```powershell
python 04_req2_connection_matrix.py
```

### Bước 4: Chứng minh query phân tán

Trên CN1:

```powershell
python 05_req2_q1_union_daily_revenue.py
python 08_req2_q4_aggregate_summary.py
python 12_req2_q8_customer_invoice_lookup.py
```

Có thể quay đủ 8 query nếu cần.

### Bước 5: Chứng minh CRUD phân tán

Trên CN1:

```powershell
python 13_req3_create_remote_record.py
python 14_req3_update_remote_invoice.py
python 15_req3_delete_remote_record.py
```

Trên CN2:

```powershell
python 13_req3_create_remote_record.py
python 14_req3_update_remote_invoice.py
python 15_req3_delete_remote_record.py
```

Trên CN3:

```powershell
python 13_req3_create_remote_record.py
python 14_req3_update_remote_invoice.py
python 15_req3_delete_remote_record.py
```

---

## 17. Câu giải thích ngắn khi demo

```text
Hệ thống có 3 SurrealDB instances độc lập chạy trên 3 máy CN1, CN2 và CN3. Dữ liệu được phân mảnh theo chi nhánh: CN1 lưu chi nhánh 1, CN2 lưu chi nhánh 2, CN3 lưu chi nhánh 3.

Surrealist UI được dùng để quan sát schema và dữ liệu trên từng node. Khi connect vào CN1 thì query chỉ chạy trên CN1; khi connect CN2 hoặc CN3 thì query chỉ chạy trên node tương ứng.

Truy vấn phân tán toàn hệ thống được thực hiện bằng Python middleware. Python gửi query đến từng endpoint CN1, CN2, CN3, nhận kết quả và union ở tầng ứng dụng.

CRUD phân tán được thực hiện bằng routing logic: CN1 thao tác CN2, CN2 thao tác CN3, CN3 thao tác CN1. Sau mỗi thao tác, chương trình kiểm tra cả 3 node để chứng minh record chỉ tồn tại ở đúng node đích.
```

---

## 18. Lỗi thường gặp

### CREATE báo record đã tồn tại

Có thể lần trước đã chạy CREATE nhưng chưa DELETE. Chạy:

```powershell
python 15_req3_delete_remote_record.py
python 13_req3_create_remote_record.py
```

### Query ra rỗng quá nhiều

Kiểm tra đã seed data trên từng máy chưa:

```powershell
python 03_req1_verify_local_data.py
```

Nếu chưa có data, chạy lại:

```powershell
python 01_create_schema_local.py
python 02_seed_local_small.py
python 03_req1_verify_local_data.py
```

### Lỗi field `ghi_chu`

Schema cũ chưa có field `ghi_chu`. Chạy lại schema và seed:

```powershell
python 01_create_schema_local.py
python 02_seed_local_small.py
```

### Sai node khi chạy CRUD

Kiểm tra `LOCAL_NODE`:

```powershell
python -c "import cluster_config; print(cluster_config.LOCAL_NODE)"
```

Kết quả phải đúng với máy đang chạy.

---

## 19. Git commands tham khảo

```powershell
git init
git add .
git commit -m "Add SurrealDB distributed NoSQL demo"
git branch -M main
git remote add origin <your-repository-url>
git push -u origin main
```

Nếu repo đã tồn tại:

```powershell
git add .
git commit -m "Update SurrealDB distributed NoSQL source"
git push
```

---

## 20. Kết luận

Dự án minh chứng mô hình NoSQL phân tán ở mức ứng dụng:

- 3 SurrealDB instances độc lập.
- Dữ liệu phân mảnh theo chi nhánh.
- Python middleware thực hiện distributed query và union result.
- CRUD được route từ máy này sang máy khác.
- Surrealist UI hỗ trợ quan sát và kiểm chứng dữ liệu trên từng node.
