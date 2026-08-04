import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


# -------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------
CSV_FILE_NAME = "Ecommerce_Sales_Cleaned_data.csv"  # Replace with your actual CSV file name
DB_FILE_NAME = "project3.db"
TABLE_NAME = "sales"

# Check if the CSV file exists before starting
if not os.path.exists(CSV_FILE_NAME):
    print(
        f"❌ Error: Could not find '{CSV_FILE_NAME}'. Please make sure your CSV file is in the same folder!"
    )
    exit()

print(f"📖 Reading '{CSV_FILE_NAME}'...")
df = pd.read_csv(CSV_FILE_NAME)

# -------------------------------------------------------------------
# STEP 1: DATA CLEANING (Fixes the "SUM returns 0" issue)
# -------------------------------------------------------------------
# Strip whitespace from column names to avoid hidden space bugs
df.columns = df.columns.str.strip()

# Clean 'TotalPrice' column so SQLite can treat it as numbers
if "TotalPrice" in df.columns:
    # If the column contains text/strings (e.g. "$1,200"), clean it up
    df["TotalPrice"] = (
        df["TotalPrice"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    # Convert to numeric float (coercing bad entries to NaN/NULL)
    df["TotalPrice"] = pd.to_numeric(df["TotalPrice"], errors="coerce").fillna(
        0
    )
else:
    print(
        f"❌ Error: Column 'TotalPrice' not found in CSV. Available columns are: {list(df.columns)}"
    )
    exit()

# -------------------------------------------------------------------
# STEP 2: CREATE / UPDATE SQLITE DATABASE
# -------------------------------------------------------------------
conn = sqlite3.connect(DB_FILE_NAME)

# Save cleaned dataframe to SQLite table
df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
print(
    f"✅ Data successfully written to table '{TABLE_NAME}' inside '{DB_FILE_NAME}'!"
)


# -------------------------------------------------------------------
# STEP 3: RUN THE ERROR-FREE SQL QUERY
# -------------------------------------------------------------------
def run_query(query):
    return pd.read_sql_query(query, conn)


query_2 = """
SELECT 
    Product, 
    SUM(TotalPrice) AS revenue
FROM sales
GROUP BY Product
ORDER BY revenue DESC 
LIMIT 6;
"""

print("\n--- TOP 6 PRODUCTS BY REVENUE ---")
results = run_query(query_2)
print(results)

query_3 = """
SELECT 
    ReferralSource,
    Sum(TotalPrice) AS revenue
FROM sales
GROUP BY ReferralSource
ORDER BY revenue DESC;
"""
print("\n--- REVENUE BY REFERRAL SOURCE ---")
results = run_query(query_3)
print(results)  

query_4 = """
SELECT  
    PaymentMethod,
    SUM(Quantity) AS total_quantity
FROM sales
GROUP BY PaymentMethod
ORDER BY total_quantity DESC;
"""
print("\n--- TOTAL QUANTITY BY PAYMENT METHOD ---") 
results = run_query(query_4)
print(results)

query_5 = """
SELECT
    OrderStatus,
    SUM(Quantity) AS total_quantity
FROM sales
GROUP BY OrderStatus
ORDER BY total_quantity DESC;
"""
print("\n--- TOTAL QUANTITY BY ORDER STATUS ---")
results = run_query(query_5)
print(results)

query_6 = """
SELECT
    CouponCode,
    SUM(Quantity) AS total_quantity
FROM sales
GROUP BY CouponCode
ORDER BY total_quantity DESC;
"""
print("\n--- TOTAL QUANTITY BY COUPON CODE ---")
results = run_query(query_6)
print(results)

Cancellation_rate_query = """
SELECT 
    (SUM(CASE WHEN OrderStatus = 'Cancelled' THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) * 100 AS cancellation_rate
FROM sales
"""
print("\n--- CANCELLATION RATE ---")
results = run_query(Cancellation_rate_query)
print(results)

Coupon_usage_query = """
SELECT
    CouponCode,
    COUNT(*) AS usage_count
FROM sales
WHERE CouponCode IS NOT NULL AND CouponCode != ''
GROUP BY CouponCode
ORDER BY usage_count DESC;
"""
print("\n--- COUPON USAGE COUNT ---")
results = run_query(Coupon_usage_query)
print(results)

QuantityvsItemsincart_query = """
SELECT 
    SUM(Quantity) AS total_quantity,
    SUM(ItemsInCart) AS total_orders,
    (SUM(Quantity) * 1.0 / SUM(ItemsInCart)) AS avg_items_per_order
FROM sales
"""
print("\n--- QUANTITY VS ITEMS IN CART ---")
results = run_query(QuantityvsItemsincart_query)
print(results)

plt.figure(figsize=(10, 6))
plt.bar(results.columns, results.iloc[0], color='lightgreen')
plt.title('Quantity vs Items in Cart')
plt.xlabel('Metrics')
plt.ylabel('Values')
plt.tight_layout()
plt.savefig('quantity_vs_items_in_cart.png')
plt.show()


total_revenue_query = """
SELECT 
    SUM(TotalPrice) AS total_revenue
FROM sales
"""
print("\n--- TOTAL REVENUE ---")
results = run_query(total_revenue_query)
print(results)

total_orders_query = """
SELECT
    COUNT(*) AS total_orders
FROM sales
"""
print("\n--- TOTAL ORDERS ---")
results = run_query(total_orders_query)
print(results)

total_quantities_sold_query = """
SELECT
    SUM(Quantity) AS total_quantities_sold
FROM sales
WHERE OrderStatus != 'Cancelled' AND OrderStatus != 'Returned'
"""
print("\n--- TOTAL QUANTITIES SOLD (Excluding Cancelled and Returned) ---")
results = run_query(total_quantities_sold_query)
print(results)

graph_of_revenue_by_product_query = """
SELECT
    Product,
    SUM(TotalPrice) AS revenue
FROM sales
GROUP BY Product
ORDER BY revenue DESC
lIMIT 6;
"""
print("\n--- GRAPH OF REVENUE BY PRODUCT ---")
results = run_query(graph_of_revenue_by_product_query)
print(results)

plt.figure(figsize=(10, 6))
plt.bar(results['Product'], results['revenue'], color='skyblue')
plt.title('Top 6 Products by Revenue')
plt.xlabel('Product')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('top_6_products_by_revenue.png')
plt.show()

plt.pie(results['revenue'], labels=results['Product'], autopct='%1.1f%%', startangle=140)
plt.title('Revenue Distribution by Product')
plt.tight_layout()
plt.savefig('revenue_distribution_by_product.png')
plt.show()



