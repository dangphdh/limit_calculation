# Limit Calculation

Hệ thống tính toán hạn mức khả dụng cho tín dụng ngân hàng.

## Cài đặt

```bash
# Clone repository
git clone <repository-url>
cd limit_calculation

# Không cần cài đặt thêm package (chỉ dùng Python standard library)
# Python 3.7+ required
```

## Cấu trúc dự án

```
limit_calculation/
├── limit_calculator.py                  # Module chính - Tính toán hạn mức
├── example.py                           # Các ví dụ minh họa
├── test_limit_calculator.py            # Unit tests
├── limit_examples.ipynb                 # Jupyter notebook examples
├── databricks_limit_calculation.py     # Databricks notebook (NEW)
├── DATABRICKS_SETUP.md                 # Hướng dẫn cài đặt Databricks (NEW)
├── Tai_lieu_Tinh_Han_muc_Kha_dung.md  # Tài liệu chi tiết
├── README.md                            # File này
└── .gitignore
```

## Sử dụng

### 1. Chạy ví dụ

```bash
python example.py
```

Sẽ chạy 3 ví dụ:
- Ví dụ đơn giản: Hạn mức vay không phân cấp
- Ví dụ 1: Hạn mức phân cấp với CCR và TSĐB liên thông
- Ví dụ 1A: Tác động khi vay thêm

### 1B. Chạy Databricks Notebook (MỚI)

```bash
# Xem hướng dẫn chi tiết trong file DATABRICKS_SETUP.md
```

Notebook Databricks (`databricks_limit_calculation.py`) cho phép:
- Đọc dữ liệu từ các bảng Spark/Delta
- Tính toán hạn mức cho nhiều khách hàng
- Xuất kết quả ra bảng Delta
- Trực quan hóa kết quả với biểu đồ
- Phân tích what-if scenarios

**Xem chi tiết**: `DATABRICKS_SETUP.md`

### 2. Chạy unit tests

```bash
python -m unittest test_limit_calculator.py -v
```

Hoặc:

```bash
python test_limit_calculator.py
```

### 3. Sử dụng trong code

```python
from decimal import Decimal
from limit_calculator import (
    LimitCalculator,
    LimitInfo,
    CollateralInfo
)

# Thiết lập thông tin TSĐB
collateral_info = CollateralInfo(
    total_collateral=Decimal('100000000000'),  # 100 tỷ
    unsecured_ratio=Decimal('0.20'),  # 20%
    max_unsecured=Decimal('30000000000')  # 30 tỷ
)

# Khởi tạo calculator
calculator = LimitCalculator(collateral_info)

# Tạo thông tin hạn mức
limit = LimitInfo(
    limit_id='LOAN_001',
    limit_name='Vay vốn lưu động',
    approved_limit=Decimal('80000000000'),  # 80 tỷ
    outstanding_amount=Decimal('30000000000'),  # 30 tỷ
    ccr=Decimal('1.0')  # 100%
)

# Tính toán
result = calculator.calculate_single_limit(limit)

# Xem kết quả
print(f"Hạn mức khả dụng: {result.available_limit_nominal:,.0f} VNĐ")
```

## Tính năng chính

### 1. Tính hạn mức đơn
- Hỗ trợ TSĐB và tín chấp
- Tính toán CCR (Credit Conversion Rate)
- Hạn mức khả dụng danh nghĩa và quy đổi

### 2. Tính hạn mức phân cấp
- Hạn mức tổng/con/cháu
- TSĐB liên thông giữa các hạn mức
- 2 phương pháp phân bổ TSĐB:
  - Theo tỷ lệ CCR (Pari-passu)
  - Theo thứ tự ưu tiên

### 3. CCR theo sản phẩm
- Vay: 100%
- Bảo lãnh: 50-100%
- L/C: 20-50%

## Ví dụ output

```
==============================================================
Hạn mức: Vay vốn lưu động (ID: LOAN_001)
==============================================================
Hạn mức được cấp:           60,000,000,000 VNĐ
CCR:                         100.00%

Dư nợ danh nghĩa:           40,000,000,000 VNĐ
Dư nợ quy đổi:              40,000,000,000 VNĐ
Tỷ lệ sử dụng:              66.67%

TSĐB được phân bổ:          61,538,461,538 VNĐ
TSĐB khả dụng:              21,538,461,538 VNĐ
Hạn mức tín chấp:           12,000,000,000 VNĐ

Hạn mức khả dụng (quy đổi): 8,000,000,000 VNĐ
Hạn mức khả dụng (danh nghĩa): 8,000,000,000 VNĐ
==============================================================
```

## Classes chính

### LimitInfo
Thông tin hạn mức đầu vào:
- `limit_id`: Mã hạn mức
- `limit_name`: Tên hạn mức
- `approved_limit`: Hạn mức được cấp
- `outstanding_amount`: Dư nợ hiện tại
- `ccr`: Credit Conversion Rate
- `parent_limit_id`: Mã hạn mức cha (optional)

### CollateralInfo
Thông tin TSĐB:
- `total_collateral`: Tổng TSĐB
- `unsecured_ratio`: Tỷ lệ tín chấp
- `max_unsecured`: Hạn mức tín chấp tối đa

### LimitCalculator
Class tính toán chính:
- `calculate_single_limit()`: Tính hạn mức đơn
- `calculate_hierarchical_limits()`: Tính hạn mức phân cấp
- `allocate_collateral_by_ccr()`: Phân bổ TSĐB theo CCR
- `allocate_collateral_by_priority()`: Phân bổ TSĐB theo ưu tiên

### LimitResult
Kết quả tính toán:
- Dư nợ danh nghĩa và quy đổi
- TSĐB được phân bổ và khả dụng
- Hạn mức khả dụng
- Tỷ lệ sử dụng

## Tài liệu tham khảo

Xem file `Tai_lieu_Tinh_Han_muc_Kha_dung.md` để biết chi tiết về:
- Công thức tính toán
- Các trường hợp đặc biệt
- Ví dụ minh họa
- Code SQL và Stored Procedures

## Testing

Dự án bao gồm comprehensive unit tests:
- Test tính hạn mức tín chấp
- Test phân bổ TSĐB
- Test tính hạn mức đơn
- Test tính hạn mức phân cấp
- Test CCR cho các loại sản phẩm

Chạy tests:
```bash
python -m unittest discover -v
```

## Phiên bản

- **Version**: 1.0
- **Python**: 3.7+
- **Dependencies**: None (chỉ dùng standard library)

## Tác giả

GitHub Copilot

## License

Tài liệu nội bộ - Sử dụng cho mục đích học tập và tham khảo
