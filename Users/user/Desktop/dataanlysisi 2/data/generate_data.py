import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Sports', 'Books', 'Beauty', 'Toys']
products = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smart Watch', 'Camera', 'Printer'],
    'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Sneakers', 'Hat', 'Scarf'],
    'Home & Kitchen': ['Blender', 'Toaster', 'Microwave', 'Cookware Set', 'Bedding', 'Lamp', 'Chair'],
    'Sports': ['Basketball', 'Tennis Racket', 'Yoga Mat', 'Dumbbells', 'Bicycle', 'Soccer Ball', 'Golf Club'],
    'Books': ['Novel', 'Textbook', 'Cookbook', 'Biography', 'Comics', 'Magazine', 'Journal'],
    'Beauty': ['Shampoo', 'Moisturizer', 'Perfume', 'Lipstick', 'Nail Polish', 'Face Mask', 'Sunscreen'],
    'Toys': ['Action Figure', 'Board Game', 'Puzzle', 'Doll', 'RC Car', 'Building Blocks', 'Art Set']
}

customer_names = ['John Smith', 'Emma Johnson', 'Michael Williams', 'Jane Brown', 'David Jones', 'Sarah Miller', 
                'James Davis', 'Mary Garcia', 'Robert Rodriguez', 'Linda Martinez', 'William Hernandez', 
                'Patricia Lopez', 'Richard Gonzalez', 'Elizabeth Wilson', 'Thomas Anderson', 'Jessica Taylor',
                'Daniel Thomas', 'Susan Jackson', 'Charles White', 'Karen Harris', 'Christopher Martin',
                'Nancy Thompson', 'Matthew Moore', 'Betty Young', 'Anthony Walker', 'Helen Hall', 'Mark Allen',
                'Dorothy Sanchez', 'Steven Clark', 'Carol Rodriguez', 'Paul Lewis', 'Ruth Lee', 'Andrew Walker',
                'Michelle Hall', 'Joshua Young', 'Sara Anderson']

cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego',
         'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte', 'Indianapolis',
         'Seattle', 'Denver', 'Boston', 'Nashville', 'Portland', 'Las Vegas', 'Detroit', 'Memphis']

num_customers = 200
num_products = len([p for cat in products.values() for p in cat])
num_orders = 1000

customer_ids = list(range(1001, 1001 + num_customers))
product_ids = list(range(2001, 2001 + num_products))
dates = [(datetime(2024, 1, 1) + timedelta(days=random.randint(0, 730))).strftime('%Y-%m-%d') for _ in range(num_orders)]

customers_df = pd.DataFrame({
    'CustomerID': customer_ids,
    'CustomerName': random.sample(customer_names * 6, num_customers),
    'Email': [f'user{i}@email.com' for i in range(1001, 1001 + num_customers)],
    'City': random.choices(cities, k=num_customers),
    'State': random.choices(['NY', 'CA', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI'], k=num_customers),
    'Age': [random.randint(18, 75) for _ in range(num_customers)],
    'RegistrationDate': [(datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1460))).strftime('%Y-%m-%d') for _ in range(num_customers)]
})

product_list = []
pid = 2001
for cat, prods in products.items():
    for p in prods:
        product_list.append({'ProductID': pid, 'ProductName': p, 'Category': cat, 'UnitPrice': round(random.uniform(5, 500), 2)})
        pid += 1

products_df = pd.DataFrame(product_list)

orders_df = pd.DataFrame({
    'OrderID': range(5001, 5001 + num_orders),
    'CustomerID': random.choices(customer_ids, k=num_orders),
    'ProductID': random.choices(product_ids, k=num_orders),
    'OrderDate': dates,
    'Quantity': [random.randint(1, 10) for _ in range(num_orders)],
    'Discount': [round(random.uniform(0, 0.3), 2) for _ in range(num_orders)]
})

orders_df = orders_df.merge(products_df[['ProductID', 'UnitPrice']], on='ProductID')
orders_df['TotalAmount'] = orders_df['Quantity'] * orders_df['UnitPrice'] * (1 - orders_df['Discount'])
orders_df['ShippingCost'] = orders_df['TotalAmount'].apply(lambda x: round(random.uniform(0, 15) if x > 50 else 5, 2))
orders_df['OrderStatus'] = random.choices(['Completed', 'Pending', 'Cancelled', 'Shipped'], k=num_orders, weights=[70, 10, 5, 15])

with pd.ExcelWriter('C:/Users/user/Desktop/dataanlysisi 2/data/dataset.xlsx') as writer:
    customers_df.to_excel(writer, sheet_name='Customers', index=False)
    products_df.to_excel(writer, sheet_name='Products', index=False)
    orders_df.to_excel(writer, sheet_name='Orders', index=False)

print("Dataset created: customers.xlsx, products.xlsx, orders.xlsx")
print(f"Customers: {len(customers_df)}, Products: {len(products_df)}, Orders: {len(orders_df)}")