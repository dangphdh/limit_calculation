# Databricks notebook source
# MAGIC %md
# MAGIC # Available Credit Limit Calculation on Databricks
# MAGIC # Tính Toán Hạn Mức Khả Dụng trên Databricks
# MAGIC 
# MAGIC This notebook demonstrates how to calculate available credit limits on Databricks using input tables.
# MAGIC 
# MAGIC Notebook này minh họa cách tính hạn mức khả dụng trên Databricks sử dụng các bảng đầu vào.
# MAGIC 
# MAGIC ## Features / Tính năng:
# MAGIC - Read limit and collateral data from Spark tables / Đọc dữ liệu hạn mức và TSĐB từ bảng Spark
# MAGIC - Calculate available limits for hierarchical structures / Tính hạn mức khả dụng cho cấu trúc phân cấp
# MAGIC - Support different CCR by product type / Hỗ trợ CCR khác nhau theo loại sản phẩm
# MAGIC - Shared collateral allocation / Phân bổ TSĐB liên thông
# MAGIC - Export results to Delta tables / Xuất kết quả ra bảng Delta

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Setup and Import / Cài Đặt và Import

# COMMAND ----------

# Import necessary libraries
from decimal import Decimal
from typing import List, Dict, Tuple
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, lit, when, sum as spark_sum, struct
from pyspark.sql.types import StructType, StructField, StringType, DecimalType
import pandas as pd

# Import limit calculator module
# Note: Upload limit_calculator.py to DBFS or install as a library
from limit_calculator import (
    LimitCalculator,
    LimitInfo,
    CollateralInfo,
    LimitResult
)

print("✓ Imports successful / Import thành công!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Define Input Table Schemas / Định Nghĩa Schema Bảng Đầu Vào
# MAGIC 
# MAGIC We will create sample input tables with the following schemas:
# MAGIC 
# MAGIC Chúng ta sẽ tạo các bảng đầu vào mẫu với schema sau:
# MAGIC 
# MAGIC ### Table 1: `collateral_info` - Thông tin TSĐB
# MAGIC - `customer_id`: Customer ID / Mã khách hàng
# MAGIC - `total_collateral`: Total collateral value / Tổng giá trị TSĐB
# MAGIC - `unsecured_ratio`: Unsecured credit ratio / Tỷ lệ tín chấp
# MAGIC - `max_unsecured`: Maximum unsecured limit / Hạn mức tín chấp tối đa
# MAGIC 
# MAGIC ### Table 2: `limit_master` - Hạn mức tổng
# MAGIC - `customer_id`: Customer ID / Mã khách hàng
# MAGIC - `limit_id`: Limit ID / Mã hạn mức
# MAGIC - `limit_name`: Limit name / Tên hạn mức
# MAGIC - `approved_limit`: Approved limit amount / Hạn mức được cấp
# MAGIC 
# MAGIC ### Table 3: `limit_detail` - Chi tiết hạn mức con
# MAGIC - `customer_id`: Customer ID / Mã khách hàng
# MAGIC - `limit_id`: Limit ID / Mã hạn mức
# MAGIC - `limit_name`: Limit name / Tên hạn mức
# MAGIC - `parent_limit_id`: Parent limit ID / Mã hạn mức cha
# MAGIC - `approved_limit`: Approved limit amount / Hạn mức được cấp
# MAGIC - `outstanding_amount`: Current outstanding / Dư nợ hiện tại
# MAGIC - `ccr`: Credit Conversion Rate / Tỷ lệ quy đổi rủi ro
# MAGIC - `product_type`: Product type (LOAN, GUARANTEE, LC) / Loại sản phẩm

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Create Sample Input Tables / Tạo Bảng Đầu Vào Mẫu

# COMMAND ----------

# Create sample collateral_info table
collateral_data = [
    ("CUST_001", Decimal("80000000000"), Decimal("0.20"), Decimal("30000000000")),
    ("CUST_002", Decimal("100000000000"), Decimal("0.25"), Decimal("40000000000"))
]

collateral_schema = StructType([
    StructField("customer_id", StringType(), False),
    StructField("total_collateral", DecimalType(20, 2), False),
    StructField("unsecured_ratio", DecimalType(5, 4), False),
    StructField("max_unsecured", DecimalType(20, 2), False)
])

df_collateral = spark.createDataFrame(collateral_data, schema=collateral_schema)

# Register as temp view for SQL queries
df_collateral.createOrReplaceTempView("collateral_info")

print("✓ Created collateral_info table / Đã tạo bảng collateral_info")
display(df_collateral)

# COMMAND ----------

# Create sample limit_master table
master_limit_data = [
    ("CUST_001", "MASTER_001", "Hạn mức tổng - KH 001", Decimal("100000000000")),
    ("CUST_002", "MASTER_002", "Hạn mức tổng - KH 002", Decimal("150000000000"))
]

master_limit_schema = StructType([
    StructField("customer_id", StringType(), False),
    StructField("limit_id", StringType(), False),
    StructField("limit_name", StringType(), False),
    StructField("approved_limit", DecimalType(20, 2), False)
])

df_master_limit = spark.createDataFrame(master_limit_data, schema=master_limit_schema)
df_master_limit.createOrReplaceTempView("limit_master")

print("✓ Created limit_master table / Đã tạo bảng limit_master")
display(df_master_limit)

# COMMAND ----------

# Create sample limit_detail table
limit_detail_data = [
    # Customer 001
    ("CUST_001", "LOAN_001", "Vay vốn lưu động", "MASTER_001", Decimal("60000000000"), Decimal("40000000000"), Decimal("1.0"), "LOAN"),
    ("CUST_001", "GUARANTEE_001", "Bảo lãnh", "MASTER_001", Decimal("30000000000"), Decimal("20000000000"), Decimal("0.5"), "GUARANTEE"),
    ("CUST_001", "LC_001", "L/C trả ngay", "MASTER_001", Decimal("20000000000"), Decimal("10000000000"), Decimal("0.2"), "LC"),
    
    # Customer 002
    ("CUST_002", "LOAN_002", "Vay dài hạn", "MASTER_002", Decimal("80000000000"), Decimal("50000000000"), Decimal("1.0"), "LOAN"),
    ("CUST_002", "GUARANTEE_002", "Bảo lãnh thầu", "MASTER_002", Decimal("40000000000"), Decimal("25000000000"), Decimal("0.6"), "GUARANTEE"),
    ("CUST_002", "LC_002", "L/C chậm trả", "MASTER_002", Decimal("30000000000"), Decimal("15000000000"), Decimal("0.5"), "LC")
]

limit_detail_schema = StructType([
    StructField("customer_id", StringType(), False),
    StructField("limit_id", StringType(), False),
    StructField("limit_name", StringType(), False),
    StructField("parent_limit_id", StringType(), False),
    StructField("approved_limit", DecimalType(20, 2), False),
    StructField("outstanding_amount", DecimalType(20, 2), False),
    StructField("ccr", DecimalType(5, 4), False),
    StructField("product_type", StringType(), False)
])

df_limit_detail = spark.createDataFrame(limit_detail_data, schema=limit_detail_schema)
df_limit_detail.createOrReplaceTempView("limit_detail")

print("✓ Created limit_detail table / Đã tạo bảng limit_detail")
display(df_limit_detail)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Explore Input Data / Khám Phá Dữ Liệu Đầu Vào

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Summary of limits by customer and product type
# MAGIC -- Tổng hợp hạn mức theo khách hàng và loại sản phẩm
# MAGIC 
# MAGIC SELECT 
# MAGIC   customer_id,
# MAGIC   product_type,
# MAGIC   COUNT(*) as limit_count,
# MAGIC   SUM(approved_limit) as total_approved_limit,
# MAGIC   SUM(outstanding_amount) as total_outstanding,
# MAGIC   ROUND(SUM(outstanding_amount * ccr), 2) as total_weighted_outstanding,
# MAGIC   ROUND(SUM(outstanding_amount) / SUM(approved_limit) * 100, 2) as utilization_pct
# MAGIC FROM limit_detail
# MAGIC GROUP BY customer_id, product_type
# MAGIC ORDER BY customer_id, product_type

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Calculate Available Limits / Tính Toán Hạn Mức Khả Dụng
# MAGIC 
# MAGIC We'll create a function to calculate limits for each customer.
# MAGIC 
# MAGIC Chúng ta sẽ tạo hàm để tính hạn mức cho từng khách hàng.

# COMMAND ----------

def calculate_customer_limits(customer_id: str) -> Tuple[Dict, List[Dict]]:
    """
    Calculate available limits for a customer
    Tính hạn mức khả dụng cho một khách hàng
    
    Args:
        customer_id: Customer ID / Mã khách hàng
        
    Returns:
        Tuple of (master_result_dict, child_results_list)
    """
    # Get collateral info for customer
    coll_row = df_collateral.filter(col("customer_id") == customer_id).first()
    if not coll_row:
        raise ValueError(f"Customer {customer_id} not found in collateral_info")
    
    collateral_info = CollateralInfo(
        total_collateral=Decimal(str(coll_row.total_collateral)),
        unsecured_ratio=Decimal(str(coll_row.unsecured_ratio)),
        max_unsecured=Decimal(str(coll_row.max_unsecured))
    )
    
    # Get master limit
    master_row = df_master_limit.filter(col("customer_id") == customer_id).first()
    if not master_row:
        raise ValueError(f"Master limit not found for customer {customer_id}")
    
    master_limit = LimitInfo(
        limit_id=master_row.limit_id,
        limit_name=master_row.limit_name,
        approved_limit=Decimal(str(master_row.approved_limit)),
        outstanding_amount=Decimal('0'),
        ccr=Decimal('1.0')
    )
    
    # Get child limits
    child_rows = df_limit_detail.filter(col("customer_id") == customer_id).collect()
    child_limits = []
    
    for row in child_rows:
        child_limit = LimitInfo(
            limit_id=row.limit_id,
            limit_name=row.limit_name,
            approved_limit=Decimal(str(row.approved_limit)),
            outstanding_amount=Decimal(str(row.outstanding_amount)),
            ccr=Decimal(str(row.ccr)),
            parent_limit_id=row.parent_limit_id
        )
        child_limits.append(child_limit)
    
    # Calculate
    calculator = LimitCalculator(collateral_info)
    master_result, child_results = calculator.calculate_hierarchical_limits(
        master_limit=master_limit,
        child_limits=child_limits,
        allocation_method='ccr'
    )
    
    # Convert to dictionaries
    def result_to_dict(result: LimitResult, customer_id: str) -> Dict:
        return {
            'customer_id': customer_id,
            'limit_id': result.limit_id,
            'limit_name': result.limit_name,
            'approved_limit': float(result.approved_limit),
            'outstanding_nominal': float(result.outstanding_nominal),
            'outstanding_weighted': float(result.outstanding_weighted),
            'ccr': float(result.ccr),
            'collateral_allocated': float(result.collateral_allocated),
            'collateral_available': float(result.collateral_available),
            'unsecured_limit': float(result.unsecured_limit),
            'available_limit_weighted': float(result.available_limit_weighted),
            'available_limit_nominal': float(result.available_limit_nominal) if result.available_limit_nominal is not None else None,
            'utilization_ratio': float(result.utilization_ratio)
        }
    
    master_dict = result_to_dict(master_result, customer_id)
    child_dicts = [result_to_dict(r, customer_id) for r in child_results]
    
    return master_dict, child_dicts

print("✓ Function defined / Đã định nghĩa hàm calculate_customer_limits")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Calculate Limits for All Customers / Tính Hạn Mức Cho Tất Cả Khách Hàng

# COMMAND ----------

# Get list of customers
customers = [row.customer_id for row in df_collateral.select("customer_id").distinct().collect()]

# Calculate for all customers
all_master_results = []
all_child_results = []

for customer_id in customers:
    print(f"Calculating for customer: {customer_id}")
    master_result, child_results = calculate_customer_limits(customer_id)
    all_master_results.append(master_result)
    all_child_results.extend(child_results)

print(f"\n✓ Calculated limits for {len(customers)} customers / Đã tính hạn mức cho {len(customers)} khách hàng")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Create Result DataFrames / Tạo DataFrame Kết Quả

# COMMAND ----------

# Convert to Pandas DataFrames first for easier handling
pdf_master_results = pd.DataFrame(all_master_results)
pdf_child_results = pd.DataFrame(all_child_results)

# Convert to Spark DataFrames
df_master_results = spark.createDataFrame(pdf_master_results)
df_child_results = spark.createDataFrame(pdf_child_results)

# Register as temp views
df_master_results.createOrReplaceTempView("limit_results_master")
df_child_results.createOrReplaceTempView("limit_results_child")

print("✓ Created result tables / Đã tạo bảng kết quả")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Display Master Limit Results / Hiển Thị Kết Quả Hạn Mức Tổng

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC   customer_id,
# MAGIC   limit_id,
# MAGIC   limit_name,
# MAGIC   ROUND(approved_limit / 1000000000, 2) as approved_limit_bil,
# MAGIC   ROUND(outstanding_nominal / 1000000000, 2) as outstanding_nominal_bil,
# MAGIC   ROUND(outstanding_weighted / 1000000000, 2) as outstanding_weighted_bil,
# MAGIC   ROUND(available_limit_weighted / 1000000000, 2) as available_weighted_bil,
# MAGIC   ROUND(utilization_ratio, 2) as utilization_pct
# MAGIC FROM limit_results_master
# MAGIC ORDER BY customer_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Display Child Limit Results / Hiển Thị Kết Quả Hạn Mức Con

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC   customer_id,
# MAGIC   limit_id,
# MAGIC   limit_name,
# MAGIC   ROUND(ccr * 100, 2) as ccr_pct,
# MAGIC   ROUND(approved_limit / 1000000000, 2) as approved_bil,
# MAGIC   ROUND(outstanding_nominal / 1000000000, 2) as outstanding_bil,
# MAGIC   ROUND(collateral_allocated / 1000000000, 2) as collateral_allocated_bil,
# MAGIC   ROUND(collateral_available / 1000000000, 2) as collateral_available_bil,
# MAGIC   ROUND(unsecured_limit / 1000000000, 2) as unsecured_bil,
# MAGIC   ROUND(available_limit_nominal / 1000000000, 2) as available_nominal_bil,
# MAGIC   ROUND(utilization_ratio, 2) as utilization_pct
# MAGIC FROM limit_results_child
# MAGIC ORDER BY customer_id, limit_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10. Detailed Analysis for Customer CUST_001 / Phân Tích Chi Tiết Cho Khách Hàng CUST_001

# COMMAND ----------

# Filter results for CUST_001
df_cust001_results = df_child_results.filter(col("customer_id") == "CUST_001")

print("="*80)
print("CUSTOMER CUST_001 - DETAILED LIMIT ANALYSIS")
print("KHÁCH HÀNG CUST_001 - PHÂN TÍCH CHI TIẾT HẠN MỨC")
print("="*80)

# Convert to Pandas for better display
pdf_cust001 = df_cust001_results.toPandas()

for idx, row in pdf_cust001.iterrows():
    print(f"\n{'-'*80}")
    print(f"Limit / Hạn mức: {row['limit_name']} (ID: {row['limit_id']})")
    print(f"{'-'*80}")
    print(f"Approved limit / Hạn mức được cấp:     {row['approved_limit']/1e9:>12,.2f} billion VND")
    print(f"CCR:                                    {row['ccr']*100:>12,.2f}%")
    print(f"Outstanding (nominal) / Dư nợ danh nghĩa: {row['outstanding_nominal']/1e9:>12,.2f} billion VND")
    print(f"Outstanding (weighted) / Dư nợ quy đổi:   {row['outstanding_weighted']/1e9:>12,.2f} billion VND")
    print(f"Utilization / Tỷ lệ sử dụng:           {row['utilization_ratio']:>12,.2f}%")
    print(f"\nCollateral allocated / TSĐB phân bổ:   {row['collateral_allocated']/1e9:>12,.2f} billion VND")
    print(f"Collateral available / TSĐB khả dụng:  {row['collateral_available']/1e9:>12,.2f} billion VND")
    print(f"Unsecured limit / Hạn mức tín chấp:    {row['unsecured_limit']/1e9:>12,.2f} billion VND")
    print(f"\nAvailable limit (nominal) / HM khả dụng: {row['available_limit_nominal']/1e9:>12,.2f} billion VND")
    print(f"Available limit (weighted) / HM quy đổi: {row['available_limit_weighted']/1e9:>12,.2f} billion VND")

print(f"\n{'='*80}\n")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11. Collateral Allocation Analysis / Phân Tích Phân Bổ TSĐB

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Collateral allocation breakdown by customer
# MAGIC -- Phân tích phân bổ TSĐB theo khách hàng
# MAGIC 
# MAGIC WITH collateral_summary AS (
# MAGIC   SELECT 
# MAGIC     r.customer_id,
# MAGIC     c.total_collateral,
# MAGIC     SUM(r.outstanding_nominal) as total_outstanding,
# MAGIC     SUM(r.outstanding_weighted) as total_weighted_outstanding,
# MAGIC     SUM(r.collateral_allocated) as total_collateral_allocated,
# MAGIC     SUM(r.collateral_available) as total_collateral_available
# MAGIC   FROM limit_results_child r
# MAGIC   JOIN collateral_info c ON r.customer_id = c.customer_id
# MAGIC   GROUP BY r.customer_id, c.total_collateral
# MAGIC )
# MAGIC SELECT 
# MAGIC   customer_id,
# MAGIC   ROUND(total_collateral / 1000000000, 2) as total_collateral_bil,
# MAGIC   ROUND(total_outstanding / 1000000000, 2) as total_outstanding_bil,
# MAGIC   ROUND(total_weighted_outstanding / 1000000000, 2) as total_weighted_bil,
# MAGIC   ROUND(total_collateral_allocated / 1000000000, 2) as allocated_bil,
# MAGIC   ROUND(total_collateral_available / 1000000000, 2) as available_bil,
# MAGIC   ROUND(total_weighted_outstanding / total_collateral * 100, 2) as collateral_usage_pct
# MAGIC FROM collateral_summary
# MAGIC ORDER BY customer_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12. Visualization - Limit Utilization / Trực Quan Hóa - Tỷ Lệ Sử Dụng Hạn Mức

# COMMAND ----------

import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")

# Get data for visualization
pdf_viz = df_child_results.toPandas()

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1: Utilization by Customer and Limit Type
ax1 = axes[0, 0]
pivot_util = pdf_viz.pivot_table(
    values='utilization_ratio', 
    index='customer_id', 
    columns='limit_name', 
    aggfunc='mean'
)
pivot_util.plot(kind='bar', ax=ax1, colormap='viridis')
ax1.set_title('Limit Utilization by Customer / Tỷ lệ sử dụng hạn mức theo khách hàng', fontsize=12, fontweight='bold')
ax1.set_xlabel('Customer / Khách hàng')
ax1.set_ylabel('Utilization % / Tỷ lệ sử dụng %')
ax1.legend(title='Limit Type / Loại hạn mức', bbox_to_anchor=(1.05, 1), loc='upper left')
ax1.grid(True, alpha=0.3)

# Plot 2: Available vs Approved Limit
ax2 = axes[0, 1]
x = range(len(pdf_viz))
width = 0.35
ax2.bar([i - width/2 for i in x], pdf_viz['approved_limit']/1e9, width, label='Approved / Được cấp', alpha=0.8)
ax2.bar([i + width/2 for i in x], pdf_viz['available_limit_nominal']/1e9, width, label='Available / Khả dụng', alpha=0.8)
ax2.set_title('Approved vs Available Limit / Hạn mức được cấp vs khả dụng', fontsize=12, fontweight='bold')
ax2.set_xlabel('Limit Index / Chỉ số hạn mức')
ax2.set_ylabel('Amount (Billion VND) / Số tiền (Tỷ VNĐ)')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: Collateral Allocation
ax3 = axes[1, 0]
collateral_data = pdf_viz.groupby('customer_id').agg({
    'collateral_allocated': 'sum',
    'collateral_available': 'sum'
}).reset_index()
x_pos = range(len(collateral_data))
ax3.bar(x_pos, collateral_data['collateral_allocated']/1e9, alpha=0.8, label='Allocated / Đã phân bổ')
ax3.bar(x_pos, collateral_data['collateral_available']/1e9, alpha=0.8, label='Available / Khả dụng')
ax3.set_xticks(x_pos)
ax3.set_xticklabels(collateral_data['customer_id'])
ax3.set_title('Collateral Allocation / Phân bổ TSĐB', fontsize=12, fontweight='bold')
ax3.set_xlabel('Customer / Khách hàng')
ax3.set_ylabel('Amount (Billion VND) / Số tiền (Tỷ VNĐ)')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot 4: CCR Distribution
ax4 = axes[1, 1]
ccr_counts = pdf_viz.groupby('ccr').size()
colors = plt.cm.Set3(range(len(ccr_counts)))
wedges, texts, autotexts = ax4.pie(
    ccr_counts.values, 
    labels=[f'CCR {float(x)*100:.0f}%' for x in ccr_counts.index],
    autopct='%1.1f%%',
    colors=colors,
    startangle=90
)
ax4.set_title('Distribution by CCR / Phân bố theo CCR', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()

display(fig)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 13. Save Results to Delta Tables / Lưu Kết Quả Vào Bảng Delta

# COMMAND ----------

# Define output paths (adjust based on your environment)
# Định nghĩa đường dẫn output (điều chỉnh theo môi trường của bạn)

# Option 1: Save to DBFS
# output_path_master = "/dbfs/data/limit_calculation/results_master"
# output_path_child = "/dbfs/data/limit_calculation/results_child"

# Option 2: Save as Delta tables in database
database_name = "limit_calculation"
spark.sql(f"CREATE DATABASE IF NOT EXISTS {database_name}")

# Save master results
df_master_results.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable(f"{database_name}.limit_results_master")

# Save child results
df_child_results.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable(f"{database_name}.limit_results_child")

print(f"✓ Results saved to database: {database_name}")
print(f"  - Table: {database_name}.limit_results_master")
print(f"  - Table: {database_name}.limit_results_child")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 14. Create Summary Report / Tạo Báo Cáo Tổng Hợp

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Summary report for management
# MAGIC -- Báo cáo tổng hợp cho ban lãnh đạo
# MAGIC 
# MAGIC SELECT 
# MAGIC   'Total Customers / Tổng số KH' as metric,
# MAGIC   COUNT(DISTINCT customer_id) as value,
# MAGIC   '' as unit
# MAGIC FROM limit_results_child
# MAGIC 
# MAGIC UNION ALL
# MAGIC 
# MAGIC SELECT 
# MAGIC   'Total Limits / Tổng số hạn mức',
# MAGIC   COUNT(*),
# MAGIC   'limits'
# MAGIC FROM limit_results_child
# MAGIC 
# MAGIC UNION ALL
# MAGIC 
# MAGIC SELECT 
# MAGIC   'Total Approved Limit / Tổng hạn mức được cấp',
# MAGIC   ROUND(SUM(approved_limit) / 1000000000, 2),
# MAGIC   'billion VND'
# MAGIC FROM limit_results_child
# MAGIC 
# MAGIC UNION ALL
# MAGIC 
# MAGIC SELECT 
# MAGIC   'Total Outstanding / Tổng dư nợ',
# MAGIC   ROUND(SUM(outstanding_nominal) / 1000000000, 2),
# MAGIC   'billion VND'
# MAGIC FROM limit_results_child
# MAGIC 
# MAGIC UNION ALL
# MAGIC 
# MAGIC SELECT 
# MAGIC   'Total Available Limit / Tổng hạn mức khả dụng',
# MAGIC   ROUND(SUM(available_limit_nominal) / 1000000000, 2),
# MAGIC   'billion VND'
# MAGIC FROM limit_results_child
# MAGIC 
# MAGIC UNION ALL
# MAGIC 
# MAGIC SELECT 
# MAGIC   'Average Utilization / Tỷ lệ sử dụng trung bình',
# MAGIC   ROUND(AVG(utilization_ratio), 2),
# MAGIC   '%'
# MAGIC FROM limit_results_child

# COMMAND ----------

# MAGIC %md
# MAGIC ## 15. Example: What-If Analysis / Ví Dụ: Phân Tích Giả Định
# MAGIC 
# MAGIC Simulate what happens if CUST_001 borrows an additional 15 billion VND
# MAGIC 
# MAGIC Mô phỏng điều gì xảy ra nếu CUST_001 vay thêm 15 tỷ VNĐ

# COMMAND ----------

# Create modified scenario for CUST_001
print("="*80)
print("WHAT-IF ANALYSIS: Customer CUST_001 borrows additional 15 billion VND")
print("PHÂN TÍCH GIẢ ĐỊNH: Khách hàng CUST_001 vay thêm 15 tỷ VNĐ")
print("="*80)

# Get current data for CUST_001
cust001_limits = df_limit_detail.filter(col("customer_id") == "CUST_001").collect()

# Modify the loan outstanding
modified_data = []
for row in cust001_limits:
    if row.limit_id == "LOAN_001":
        # Increase loan outstanding by 15 billion
        new_outstanding = Decimal(str(row.outstanding_amount)) + Decimal("15000000000")
        modified_data.append((
            row.customer_id, row.limit_id, row.limit_name, row.parent_limit_id,
            Decimal(str(row.approved_limit)), new_outstanding, 
            Decimal(str(row.ccr)), row.product_type
        ))
    else:
        modified_data.append((
            row.customer_id, row.limit_id, row.limit_name, row.parent_limit_id,
            Decimal(str(row.approved_limit)), Decimal(str(row.outstanding_amount)), 
            Decimal(str(row.ccr)), row.product_type
        ))

# Create temporary modified dataframe
df_modified = spark.createDataFrame(modified_data, schema=limit_detail_schema)

# Recalculate for the modified scenario
# (This would require modifying the calculate_customer_limits function to accept a custom df)

print("\n✓ Scenario created / Đã tạo kịch bản")
print("Note: In production, you would recalculate limits with the modified data")
print("Lưu ý: Trong thực tế, bạn sẽ tính lại hạn mức với dữ liệu đã sửa đổi")

display(df_modified)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 16. Conclusion and Next Steps / Kết Luận và Bước Tiếp Theo
# MAGIC 
# MAGIC ### Summary / Tóm tắt:
# MAGIC 
# MAGIC This notebook demonstrated how to:
# MAGIC 1. ✅ Create input tables with limit and collateral data
# MAGIC 2. ✅ Calculate available limits for hierarchical structures
# MAGIC 3. ✅ Handle different CCR by product type
# MAGIC 4. ✅ Allocate shared collateral across limits
# MAGIC 5. ✅ Export results to Delta tables
# MAGIC 6. ✅ Create visualizations and summary reports
# MAGIC 
# MAGIC Notebook này đã minh họa cách:
# MAGIC 1. ✅ Tạo bảng đầu vào với dữ liệu hạn mức và TSĐB
# MAGIC 2. ✅ Tính hạn mức khả dụng cho cấu trúc phân cấp
# MAGIC 3. ✅ Xử lý CCR khác nhau theo loại sản phẩm
# MAGIC 4. ✅ Phân bổ TSĐB liên thông giữa các hạn mức
# MAGIC 5. ✅ Xuất kết quả ra bảng Delta
# MAGIC 6. ✅ Tạo trực quan hóa và báo cáo tổng hợp
# MAGIC 
# MAGIC ### Next Steps / Bước tiếp theo:
# MAGIC 
# MAGIC - **Automation / Tự động hóa**: Schedule this notebook to run periodically
# MAGIC - **Alerting / Cảnh báo**: Set up alerts when utilization exceeds thresholds
# MAGIC - **Integration / Tích hợp**: Connect to source systems for real-time data
# MAGIC - **Enhanced Analytics / Phân tích nâng cao**: Add trend analysis and forecasting
# MAGIC - **Performance / Hiệu năng**: Optimize for large-scale data processing

# COMMAND ----------

print("\n" + "="*80)
print("NOTEBOOK EXECUTION COMPLETE / HOÀN THÀNH THỰC THI NOTEBOOK")
print("="*80)
print("\nAll calculations completed successfully!")
print("Tất cả tính toán đã hoàn thành thành công!")
print("\nResults are available in:")
print("Kết quả có sẵn tại:")
print(f"  - {database_name}.limit_results_master")
print(f"  - {database_name}.limit_results_child")
print("="*80 + "\n")
