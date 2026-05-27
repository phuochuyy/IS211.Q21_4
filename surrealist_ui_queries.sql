-- Run these queries in Surrealist UI.
-- Change the branch number based on the selected connection:
-- CN1 = ma_chi_nhanh 1
-- CN2 = ma_chi_nhanh 2
-- CN3 = ma_chi_nhanh 3

RETURN 'Connected from Surrealist UI';

INFO FOR DB;

SELECT * FROM doanh_thu_moi_ngay_theo_ma_cn
WHERE ma_chi_nhanh = 1
LIMIT 5;

SELECT * FROM chi_tiet_hoa_don_theo_ma_kh
WHERE ma_chi_nhanh = 1
LIMIT 5;

SELECT * FROM kho_sp_theo_ma_cn
WHERE ma_chi_nhanh = 1
LIMIT 5;

SELECT count() AS total
FROM chi_tiet_hoa_don_theo_ma_kh
GROUP ALL;

SELECT * FROM chi_tiet_hoa_don_theo_ma_kh
WHERE phuong_thuc_thanh_toan = 'Tiền Mặt'
LIMIT 5;

SELECT * FROM kho_sp_theo_ma_cn
WHERE tong_so_luong_ton_kho >= 30
AND tong_so_luong_ton_kho <= 60
LIMIT 5;

SELECT math::sum(tong_tien) AS total_daily_revenue
FROM doanh_thu_moi_ngay_theo_ma_cn
GROUP ALL;

-- Example CRUD verification
SELECT * FROM doanh_thu_moi_ngay_theo_ma_cn:req3_create_from_cn1_to_cn2;
SELECT * FROM chi_tiet_hoa_don_theo_ma_kh:cn2_cthd_005;
