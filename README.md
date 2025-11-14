# Limit Calculation - Hệ thống Tính Hạn Mức Khả Dụng

## Mô tả

Dự án tài liệu hướng dẫn chi tiết về cách tính toán hạn mức khả dụng (Available Limit) cho hệ thống tín dụng ngân hàng, bao gồm:

- Hạn mức phân cấp (tổng, con, cháu)
- Tỷ lệ CCR (Credit Conversion Rate) khác nhau cho từng sản phẩm
- TSĐB (Tài sản đảm bảo) liên thông giữa các hạn mức
- Công thức tính toán và ví dụ minh họa

## Nội dung

### Tài liệu chính

- **Tai_lieu_Tinh_Han_muc_Kha_dung.md**: Tài liệu đầy đủ về yêu cầu và cách tính hạn mức khả dụng

### Các khái niệm chính

1. **Hạn mức phân cấp**
   - Hạn mức tổng (Master Limit)
   - Hạn mức con (Child Limit)
   - Hạn mức cháu (Sub-child Limit)

2. **CCR - Credit Conversion Rate**
   - Vay: 100%
   - Bảo lãnh: 50-100%
   - L/C: 20-50%

3. **TSĐB liên thông**
   - Phân bổ động theo dư nợ thực tế
   - Hạn mức con chia sẻ TSĐB

## Cấu trúc

```
limit_calculation/
├── Tai_lieu_Tinh_Han_muc_Kha_dung.md  # Tài liệu chi tiết
├── limit_calculator.py                 # Module Python tính toán
├── example.py                          # Ví dụ minh họa
├── limit_examples.ipynb                # Jupyter notebook
├── databricks_limit_calculation.py    # Databricks notebook (MỚI)
├── DATABRICKS_SETUP.md                # Hướng dẫn Databricks (MỚI)
├── test_limit_calculator.py           # Unit tests
├── README.md                           # File này
└── .gitignore                          # Git ignore
```

## Tính năng chính

- ✅ Công thức tính hạn mức cho cấu trúc phân cấp
- ✅ Xử lý CCR khác nhau cho từng loại sản phẩm
- ✅ TSĐB liên thông giữa các hạn mức con
- ✅ Ví dụ tính toán cụ thể
- ✅ Code mẫu Python và SQL
- ✅ Stored Procedure
- ✅ **Databricks notebook với bảng đầu vào (MỚI)**

## Phiên bản

- **Version**: 2.0
- **Ngày cập nhật**: 06/11/2025
- **Cập nhật**: Bổ sung cấu trúc phân cấp hạn mức, CCR và TSĐB liên thông

## Tác giả

GitHub Copilot

## Giấy phép

Tài liệu nội bộ - Sử dụng cho mục đích học tập và tham khảo
