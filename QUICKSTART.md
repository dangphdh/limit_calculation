# Quick Start Guide - Databricks Limit Calculation
# Hướng Dẫn Nhanh - Tính Hạn Mức Databricks

## What's New / Có Gì Mới

This repository now includes a **Databricks notebook** that allows you to calculate available credit limits using **input tables** (Spark/Delta tables).

Repository này hiện bao gồm **notebook Databricks** cho phép tính hạn mức khả dụng sử dụng **bảng đầu vào** (bảng Spark/Delta).

## Quick Start / Bắt Đầu Nhanh

### 1. Upload to Databricks / Tải Lên Databricks

**Files to upload / Tệp cần tải lên:**
- `databricks_limit_calculation.py` - The notebook / Notebook chính
- `limit_calculator.py` - Calculation module / Module tính toán

**How to upload / Cách tải lên:**

```bash
# Option 1: Use Databricks UI
# 1. Go to Workspace → Upload files
# 2. Select both files

# Option 2: Use Git (recommended)
# 1. In Databricks, go to Repos → Add Repo
# 2. Enter: https://github.com/dangphdh/limit_calculation
```

### 2. Run the Notebook / Chạy Notebook

1. Open `databricks_limit_calculation.py`
2. Attach to a cluster (DBR 11.3+)
3. Click "Run All"

That's it! The notebook will:
- Create sample input tables
- Calculate limits for all customers
- Display results with visualizations
- Save to Delta tables

Xong! Notebook sẽ:
- Tạo bảng đầu vào mẫu
- Tính hạn mức cho tất cả khách hàng
- Hiển thị kết quả với biểu đồ
- Lưu vào bảng Delta

## Input Tables / Bảng Đầu Vào

The notebook expects 3 input tables / Notebook cần 3 bảng đầu vào:

### 1. `collateral_info` - Collateral Information

```sql
CREATE TABLE collateral_info (
    customer_id STRING,
    total_collateral DECIMAL(20,2),  -- Total TSĐB
    unsecured_ratio DECIMAL(5,4),     -- Tỷ lệ tín chấp
    max_unsecured DECIMAL(20,2)       -- Max tín chấp
)
```

### 2. `limit_master` - Master Limits

```sql
CREATE TABLE limit_master (
    customer_id STRING,
    limit_id STRING,
    limit_name STRING,
    approved_limit DECIMAL(20,2)
)
```

### 3. `limit_detail` - Child Limits

```sql
CREATE TABLE limit_detail (
    customer_id STRING,
    limit_id STRING,
    limit_name STRING,
    parent_limit_id STRING,
    approved_limit DECIMAL(20,2),
    outstanding_amount DECIMAL(20,2),
    ccr DECIMAL(5,4),                 -- 0-1 (e.g., 1.0 for 100%)
    product_type STRING               -- LOAN, GUARANTEE, LC
)
```

## Output Tables / Bảng Đầu Ra

Results are saved to / Kết quả được lưu vào:

1. `limit_calculation.limit_results_master` - Master limit results
2. `limit_calculation.limit_results_child` - Child limit results

Query them with / Truy vấn với:

```sql
SELECT * FROM limit_calculation.limit_results_master;
SELECT * FROM limit_calculation.limit_results_child;
```

## Using Your Own Data / Sử Dụng Dữ Liệu Riêng

Replace this section in the notebook:

```python
# Comment out section 3 (Create Sample Input Tables)
# Add instead:

df_collateral = spark.table("your_database.collateral_info")
df_master_limit = spark.table("your_database.limit_master")
df_limit_detail = spark.table("your_database.limit_detail")

# Create temp views
df_collateral.createOrReplaceTempView("collateral_info")
df_master_limit.createOrReplaceTempView("limit_master")
df_limit_detail.createOrReplaceTempView("limit_detail")
```

## Example Output / Ví Dụ Kết Quả

```
Customer CUST_001 - Detailed Limit Analysis
================================================================
Limit: Vay vốn lưu động (ID: LOAN_001)
----------------------------------------------------------------
Approved limit:                      60.00 billion VND
CCR:                                100.00%
Outstanding (nominal):               40.00 billion VND
Outstanding (weighted):              40.00 billion VND
Utilization:                         66.67%

Collateral allocated:                61.54 billion VND
Collateral available:                21.54 billion VND
Unsecured limit:                     12.00 billion VND

Available limit (nominal):           20.00 billion VND
Available limit (weighted):          20.00 billion VND
```

## Key Features / Tính Năng Chính

✅ **Hierarchical limits** / Hạn mức phân cấp
- Master and child limits
- Automatic aggregation

✅ **Different CCR by product** / CCR khác nhau theo sản phẩm
- Loan: 100%
- Guarantee: 50-100%
- L/C: 20-50%

✅ **Shared collateral** / TSĐB liên thông
- Pari-passu allocation
- Priority allocation

✅ **Visualizations** / Trực quan hóa
- Utilization charts
- Collateral allocation
- Limit comparison

✅ **Delta table export** / Xuất Delta table
- Persistent storage
- Query with SQL
- Integration ready

## Need Help? / Cần Trợ Giúp?

📖 **Detailed guide**: See `DATABRICKS_SETUP.md`
📖 **Full documentation**: See `Tai_lieu_Tinh_Han_muc_Kha_dung.md`
📖 **Code reference**: See `README_CODE.md`

## Troubleshooting / Khắc Phục Lỗi

### Module not found / Không tìm thấy module

**Error**: `ModuleNotFoundError: No module named 'limit_calculator'`

**Solution**: Place both files in same directory or add to path:
```python
import sys
sys.path.append('/path/to/module')
```

### Permission denied / Không có quyền

**Error**: Cannot create database or table

**Solution**: Write to DBFS instead:
```python
df.write.mode("overwrite").parquet("/dbfs/tmp/results")
```

## What's Different from Jupyter Notebook? / Khác Gì Với Jupyter Notebook?

| Feature | Jupyter Notebook | Databricks Notebook |
|---------|------------------|---------------------|
| Data source | In-memory data | Spark/Delta tables |
| Scale | Single machine | Distributed cluster |
| Storage | Local files | Delta Lake |
| SQL queries | No | Yes (with `%sql`) |
| Scheduling | Manual | Built-in scheduler |
| Sharing | Export file | Share workspace |

## Next Steps / Bước Tiếp Theo

1. ✅ Run the sample notebook
2. ✅ Explore the results
3. 📝 Prepare your input tables
4. 🔄 Replace sample data with real data
5. 📊 Schedule for regular execution
6. 🚀 Integrate with your workflow

## Support / Hỗ Trợ

For questions or issues / Đối với câu hỏi hoặc vấn đề:

1. Check `DATABRICKS_SETUP.md` for detailed instructions
2. Review example outputs in the notebook
3. Run unit tests: `python -m unittest test_limit_calculator.py`
4. Check the main documentation

---

**Version**: 1.0
**Last Updated**: 2025-11-14
**Compatibility**: Databricks Runtime 11.3 LTS or higher
