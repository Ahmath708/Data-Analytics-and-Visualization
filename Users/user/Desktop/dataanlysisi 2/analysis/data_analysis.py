import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

DATA_PATH = 'C:/Users/user/Desktop/dataanlysisi 2/data/dataset.xlsx'
OUTPUT_PATH = 'C:/Users/user/Desktop/dataanlysisi 2/analysis/'

def load_data():
    customers = pd.read_excel(DATA_PATH, sheet_name='Customers')
    products = pd.read_excel(DATA_PATH, sheet_name='Products')
    orders = pd.read_excel(DATA_PATH, sheet_name='Orders')
    return customers, products, orders

def customer_analysis(customers, orders):
    print("\n=== CUSTOMER ANALYSIS ===")
    
    merged = orders.merge(customers, on='CustomerID')
    
    customer_stats = merged.groupby('CustomerID').agg({
        'OrderID': 'count',
        'TotalAmount': ['sum', 'mean'],
        'Quantity': 'sum'
    }).round(2)
    customer_stats.columns = ['OrderCount', 'TotalSpent', 'AvgOrderValue', 'TotalQuantity']
    customer_stats = customer_stats.reset_index()
    
    top_customers = customer_stats.nlargest(10, 'TotalSpent')[['CustomerID', 'TotalSpent', 'OrderCount']].merge(
        customers[['CustomerID', 'CustomerName']], on='CustomerID'
    )[['CustomerID', 'CustomerName', 'TotalSpent', 'OrderCount']]
    print("\nTop 10 Customers by Revenue:")
    print(top_customers.to_string(index=False))
    
    city_analysis = merged.groupby('City').agg({
        'CustomerID': 'nunique',
        'TotalAmount': 'sum'
    }).round(2)
    city_analysis.columns = ['CustomerCount', 'Revenue']
    city_analysis = city_analysis.sort_values('Revenue', ascending=False).head(10)
    print("\nTop 10 Cities by Revenue:")
    print(city_analysis.to_string())
    
    age_groups = pd.cut(merged['Age'], bins=[0, 25, 35, 45, 55, 65, 100], 
                       labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
    age_analysis = merged.groupby(age_groups).agg({
        'OrderID': 'count',
        'TotalAmount': 'sum'
    }).round(2)
    age_analysis.columns = ['OrderCount', 'Revenue']
    print("\nRevenue by Age Group:")
    print(age_analysis.to_string())
    
    return customer_stats

def product_analysis(products, orders):
    print("\n=== PRODUCT ANALYSIS ===")
    
    merged = orders.merge(products, on='ProductID')
    
    category_perf = merged.groupby('Category').agg({
        'OrderID': 'count',
        'TotalAmount': 'sum',
        'Quantity': 'sum'
    }).round(2)
    category_perf.columns = ['OrderCount', 'Revenue', 'UnitsSold']
    category_perf = category_perf.sort_values('Revenue', ascending=False)
    print("\nCategory Performance:")
    print(category_perf.to_string())
    
    top_products = merged.groupby(['ProductID', 'ProductName']).agg({
        'OrderID': 'count',
        'TotalAmount': 'sum'
    }).round(2)
    top_products.columns = ['OrderCount', 'Revenue']
    top_products = top_products.sort_values('Revenue', ascending=False).head(15)
    print("\nTop 15 Products by Revenue:")
    print(top_products.to_string())
    
    product_price_analysis = products.groupby('Category')['UnitPrice'].agg(['mean', 'min', 'max', 'std']).round(2)
    print("\nPrice Statistics by Category:")
    print(product_price_analysis.to_string())
    
    return category_perf

def sales_trend_analysis(orders):
    print("\n=== SALES TREND ANALYSIS ===")
    
    orders['OrderDate'] = pd.to_datetime(orders['OrderDate'])
    orders['YearMonth'] = orders['OrderDate'].dt.to_period('M')
    orders['Year'] = orders['OrderDate'].dt.year
    orders['Month'] = orders['OrderDate'].dt.month
    orders['Quarter'] = orders['OrderDate'].dt.quarter
    orders['DayOfWeek'] = orders['OrderDate'].dt.day_name()
    
    monthly_sales = orders.groupby('YearMonth').agg({
        'OrderID': 'count',
        'TotalAmount': 'sum',
        'Quantity': 'sum'
    }).round(2)
    monthly_sales.columns = ['Orders', 'Revenue', 'UnitsSold']
    print("\nMonthly Sales Trend:")
    print(monthly_sales.to_string())
    
    quarterly_sales = orders.groupby(['Year', 'Quarter']).agg({
        'OrderID': 'count',
        'TotalAmount': 'sum'
    }).round(2)
    quarterly_sales.columns = ['Orders', 'Revenue']
    print("\nQuarterly Sales:")
    print(quarterly_sales.to_string())
    
    daily_pattern = orders.groupby('DayOfWeek').agg({
        'OrderID': 'count',
        'TotalAmount': 'sum'
    }).round(2)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_pattern = daily_pattern.reindex(day_order)
    print("\nDaily Sales Pattern:")
    print(daily_pattern.to_string())
    
    return monthly_sales

def statistical_analysis(orders, customers):
    print("\n=== STATISTICAL ANALYSIS ===")
    
    revenue_stats = orders['TotalAmount'].describe()
    print("\nRevenue Statistics:")
    print(revenue_stats.round(2))
    
    order_status_dist = orders['OrderStatus'].value_counts()
    print("\nOrder Status Distribution:")
    print(order_status_dist)
    
    cancel_rate = (orders['OrderStatus'] == 'Cancelled').sum() / len(orders) * 100
    print(f"\nCancellation Rate: {cancel_rate:.2f}%")
    
    completed_orders = orders[orders['OrderStatus'] == 'Completed']
    avg_order_value = completed_orders['TotalAmount'].mean()
    print(f"Average Order Value (Completed): ${avg_order_value:.2f}")
    
    customer_age_stats = customers['Age'].describe()
    print("\nCustomer Age Statistics:")
    print(customer_age_stats.round(2))
    
    return revenue_stats

def generate_report():
    print("=" * 60)
    print("DATA ANALYTICS REPORT")
    print("=" * 60)
    
    customers, products, orders = load_data()
    
    customer_stats = customer_analysis(customers, orders)
    category_perf = product_analysis(products, orders)
    monthly_sales = sales_trend_analysis(orders)
    revenue_stats = statistical_analysis(orders, customers)
    
    customer_stats.to_excel(OUTPUT_PATH + 'customer_stats.xlsx', index=False)
    category_perf.to_excel(OUTPUT_PATH + 'category_performance.xlsx')
    monthly_sales.to_excel(OUTPUT_PATH + 'monthly_sales.xlsx')
    
    print("\n" + "=" * 60)
    print("Reports saved to:", OUTPUT_PATH)
    print("=" * 60)

if __name__ == "__main__":
    generate_report()