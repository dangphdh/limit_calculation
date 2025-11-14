# Databricks Notebook Setup Guide
# Hướng Dẫn Cài Đặt Notebook Databricks

This guide explains how to set up and run the limit calculation notebook on Databricks.

Hướng dẫn này giải thích cách cài đặt và chạy notebook tính hạn mức trên Databricks.

## Files / Tệp tin

- `databricks_limit_calculation.py` - Main Databricks notebook / Notebook Databricks chính
- `limit_calculator.py` - Limit calculation module / Module tính toán hạn mức

## Prerequisites / Yêu cầu

1. **Databricks Workspace**: Access to a Databricks workspace (Community, Standard, or Premium)
2. **Cluster**: A running Databricks cluster with:
   - Runtime: DBR 11.3 LTS or higher (recommended)
   - Python: 3.8+
   - Libraries: Standard Python libraries (included in DBR)

## Setup Instructions / Hướng Dẫn Cài Đặt

### Step 1: Upload Files to Databricks / Bước 1: Tải File Lên Databricks

#### Option A: Using Databricks UI / Tùy chọn A: Sử dụng giao diện Databricks

1. Log in to your Databricks workspace
2. Click on **Workspace** in the left sidebar
3. Navigate to your desired folder (e.g., `/Users/your-email@domain.com/`)
4. Click **Create** → **Upload file**
5. Upload `databricks_limit_calculation.py`
6. Repeat to upload `limit_calculator.py`

#### Option B: Using Databricks CLI / Tùy chọn B: Sử dụng Databricks CLI

```bash
# Install Databricks CLI
pip install databricks-cli

# Configure authentication
databricks configure --token

# Upload files
databricks workspace import databricks_limit_calculation.py /Users/your-email@domain.com/databricks_limit_calculation.py
databricks workspace import limit_calculator.py /Users/your-email@domain.com/limit_calculator.py
```

#### Option C: Using Databricks Repos (Git Integration) / Tùy chọn C: Sử dụng Databricks Repos (Tích hợp Git)

1. In Databricks, click **Repos** in the left sidebar
2. Click **Add Repo**
3. Enter the Git repository URL: `https://github.com/dangphdh/limit_calculation`
4. Click **Create Repo**
5. The notebook and module will be automatically synced

### Step 2: Install the Limit Calculator Module / Bước 2: Cài Đặt Module Limit Calculator

The `limit_calculator.py` module needs to be accessible to the notebook. You have several options:

Module `limit_calculator.py` cần có thể truy cập từ notebook. Bạn có một số tùy chọn:

#### Option A: Same Directory (Simplest) / Tùy chọn A: Cùng Thư Mục (Đơn giản nhất)

If you upload both files to the same directory, Python will automatically find the module.

Nếu bạn tải cả hai file lên cùng thư mục, Python sẽ tự động tìm thấy module.

#### Option B: Add to Python Path / Tùy chọn B: Thêm vào Python Path

Add this cell at the beginning of the notebook:

```python
import sys
sys.path.append('/dbfs/path/to/your/module/')
```

#### Option C: Install as Library / Tùy chọn C: Cài Đặt Như Thư Viện

1. Package the module:
```bash
# Create setup.py
cat > setup.py << EOF
from setuptools import setup

setup(
    name='limit_calculator',
    version='1.0',
    py_modules=['limit_calculator'],
)
EOF

# Build wheel
python setup.py bdist_wheel
```

2. In Databricks:
   - Go to **Compute** → Select your cluster
   - Click **Libraries** → **Install new**
   - Select **Upload** → Upload the wheel file
   - Install the library

### Step 3: Create and Attach to a Cluster / Bước 3: Tạo và Gắn Với Cluster

1. In Databricks, go to **Compute**
2. Click **Create Cluster**
3. Configure:
   - **Cluster name**: `limit-calculation-cluster`
   - **Cluster mode**: Single Node (for testing) or Standard (for production)
   - **Databricks runtime version**: 11.3 LTS or higher
   - **Node type**: Choose based on your data size (e.g., `Standard_DS3_v2` on Azure)
4. Click **Create Cluster**
5. Wait for the cluster to start (usually 3-5 minutes)

### Step 4: Open and Run the Notebook / Bước 4: Mở và Chạy Notebook

1. Navigate to the uploaded `databricks_limit_calculation.py` file
2. Click on it to open
3. Attach to your cluster:
   - Click **Disconnected** at the top
   - Select your cluster from the dropdown
4. Run the notebook:
   - Click **Run All** to execute all cells
   - Or run cells individually using **Shift+Enter**

## Notebook Structure / Cấu Trúc Notebook

The notebook is organized into the following sections:

Notebook được tổ chức thành các phần sau:

1. **Setup and Import** - Import libraries and modules
2. **Define Input Table Schemas** - Define data structure
3. **Create Sample Input Tables** - Create example data
4. **Explore Input Data** - SQL queries to explore data
5. **Calculate Available Limits** - Main calculation function
6. **Calculate for All Customers** - Process all customers
7. **Create Result DataFrames** - Convert results to DataFrames
8. **Display Results** - Show master and child limit results
9. **Detailed Analysis** - Deep dive into specific customer
10. **Collateral Allocation Analysis** - Analyze collateral distribution
11. **Visualization** - Charts and graphs
12. **Save Results to Delta Tables** - Persist results
13. **Summary Report** - Executive summary
14. **What-If Analysis** - Scenario simulation
15. **Conclusion** - Summary and next steps

## Input Tables / Bảng Đầu Vào

The notebook expects the following input tables:

Notebook yêu cầu các bảng đầu vào sau:

### 1. `collateral_info` - Collateral Information

| Column | Type | Description |
|--------|------|-------------|
| customer_id | String | Customer ID / Mã khách hàng |
| total_collateral | Decimal(20,2) | Total collateral value / Tổng TSĐB |
| unsecured_ratio | Decimal(5,4) | Unsecured ratio (0-1) / Tỷ lệ tín chấp |
| max_unsecured | Decimal(20,2) | Max unsecured limit / Hạn mức tín chấp tối đa |

### 2. `limit_master` - Master Limits

| Column | Type | Description |
|--------|------|-------------|
| customer_id | String | Customer ID / Mã khách hàng |
| limit_id | String | Limit ID / Mã hạn mức |
| limit_name | String | Limit name / Tên hạn mức |
| approved_limit | Decimal(20,2) | Approved limit / Hạn mức được cấp |

### 3. `limit_detail` - Child Limits

| Column | Type | Description |
|--------|------|-------------|
| customer_id | String | Customer ID / Mã khách hàng |
| limit_id | String | Limit ID / Mã hạn mức |
| limit_name | String | Limit name / Tên hạn mức |
| parent_limit_id | String | Parent limit ID / Mã hạn mức cha |
| approved_limit | Decimal(20,2) | Approved limit / Hạn mức được cấp |
| outstanding_amount | Decimal(20,2) | Outstanding / Dư nợ |
| ccr | Decimal(5,4) | CCR (0-1) / Tỷ lệ quy đổi |
| product_type | String | Product type / Loại sản phẩm |

## Using Your Own Data / Sử Dụng Dữ Liệu Riêng

To use your own data instead of sample data:

Để sử dụng dữ liệu riêng thay vì dữ liệu mẫu:

1. **Prepare your source tables** in Delta format or other supported formats
2. **Modify the notebook**:
   - Comment out sections 3 (Create Sample Input Tables)
   - Replace with references to your actual tables:

```python
# Instead of creating sample data, read from your tables
df_collateral = spark.table("your_database.collateral_info")
df_master_limit = spark.table("your_database.limit_master")
df_limit_detail = spark.table("your_database.limit_detail")

# Create temp views
df_collateral.createOrReplaceTempView("collateral_info")
df_master_limit.createOrReplaceTempView("limit_master")
df_limit_detail.createOrReplaceTempView("limit_detail")
```

3. **Ensure your tables match the expected schema** (see Input Tables section above)

## Output Tables / Bảng Đầu Ra

The notebook creates two output tables:

Notebook tạo hai bảng đầu ra:

1. **`limit_calculation.limit_results_master`** - Master limit results
2. **`limit_calculation.limit_results_child`** - Child limit results

You can query these tables using SQL:

```sql
SELECT * FROM limit_calculation.limit_results_master;
SELECT * FROM limit_calculation.limit_results_child;
```

## Scheduling / Lên Lịch

To run the notebook automatically on a schedule:

Để chạy notebook tự động theo lịch:

1. Open the notebook in Databricks
2. Click **Schedule** at the top right
3. Click **Add Schedule**
4. Configure:
   - **Name**: Daily limit calculation
   - **Schedule type**: Scheduled
   - **Time**: Choose your desired time (e.g., 02:00 AM daily)
   - **Cluster**: Select your cluster
5. Click **Create**

## Troubleshooting / Khắc Phục Sự Cố

### Issue: Module not found error / Lỗi: Không tìm thấy module

**Error**: `ModuleNotFoundError: No module named 'limit_calculator'`

**Solution** / Giải pháp:
- Ensure `limit_calculator.py` is in the same directory as the notebook
- Or add the module path to `sys.path`
- Or install as a library (see Setup Instructions)

### Issue: Permission denied / Lỗi: Không có quyền

**Error**: Permission errors when writing to database

**Solution** / Giải pháp:
- Ensure your user has CREATE DATABASE and CREATE TABLE permissions
- Or modify the output path to write to DBFS instead:

```python
df_master_results.write.mode("overwrite").parquet("/dbfs/tmp/limit_results_master")
```

### Issue: Decimal precision errors / Lỗi: Độ chính xác Decimal

**Error**: Decimal precision or rounding errors

**Solution** / Giải pháp:
- Python's Decimal type is used for precise financial calculations
- Ensure you convert to Decimal when reading from Spark DataFrames:
```python
Decimal(str(spark_value))
```

### Issue: Memory errors with large datasets / Lỗi: Hết bộ nhớ với dữ liệu lớn

**Solution** / Giải pháp:
- Process customers in batches
- Use a larger cluster with more memory
- Optimize the calculation logic to use Spark operations instead of Python loops

## Performance Optimization / Tối Ưu Hiệu Năng

For large-scale production use:

Đối với sử dụng sản xuất quy mô lớn:

1. **Use Spark operations** instead of collecting all data to driver
2. **Partition your data** by customer_id for parallel processing
3. **Cache intermediate results** that are reused
4. **Use broadcast joins** for small lookup tables
5. **Enable adaptive query execution** (enabled by default in DBR 7.3+)

Example optimization:

```python
# Enable AQE
spark.conf.set("spark.sql.adaptive.enabled", "true")

# Cache frequently accessed tables
df_collateral.cache()
df_master_limit.cache()
```

## Support / Hỗ Trợ

For issues or questions:

Đối với vấn đề hoặc câu hỏi:

- Check the main repository README: `README_CODE.md`
- Review the detailed documentation: `Tai_lieu_Tinh_Han_muc_Kha_dung.md`
- Run the tests: `python -m unittest test_limit_calculator.py`

## Version Information / Thông Tin Phiên Bản

- **Version**: 1.0
- **Compatible with**: Databricks Runtime 11.3 LTS or higher
- **Python**: 3.8+
- **Dependencies**: Standard library only (no external dependencies)

## License / Giấy Phép

Internal documentation - For learning and reference purposes

Tài liệu nội bộ - Sử dụng cho mục đích học tập và tham khảo
