import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import warnings
warnings.filterwarnings('ignore')

DATA_PATH = 'C:/Users/user/Desktop/dataanlysisi 2/data/dataset.xlsx'

def load_data():
    customers = pd.read_excel(DATA_PATH, sheet_name='Customers')
    products = pd.read_excel(DATA_PATH, sheet_name='Products')
    orders = pd.read_excel(DATA_PATH, sheet_name='Orders')
    return customers, products, orders

def prepare_data(customers, products, orders):
    orders['OrderDate'] = pd.to_datetime(orders['OrderDate'])
    merged = orders.merge(customers, on='CustomerID').merge(products, on='ProductID')
    merged['YearMonth'] = merged['OrderDate'].dt.to_period('M').astype(str)
    merged['Year'] = merged['OrderDate'].dt.year
    merged['Quarter'] = merged['OrderDate'].dt.quarter
    merged['MonthName'] = merged['OrderDate'].dt.month_name()
    return merged

def create_dashboard():
    customers, products, orders = load_data()
    df = prepare_data(customers, products, orders)
    
    app = dash.Dash(__name__)
    
    total_revenue = df[df['OrderStatus'] == 'Completed']['TotalAmount'].sum()
    total_orders = len(df[df['OrderStatus'] == 'Completed'])
    avg_order = df[df['OrderStatus'] == 'Completed']['TotalAmount'].mean()
    total_customers = df['CustomerID'].nunique()
    
    app.layout = html.Div([
        html.H1("Data Analytics Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),
        
        html.Div([
            html.Div([html.H4("Total Revenue"), html.H2(f"${total_revenue:,.2f}")], 
                     className="card", style={'background': '#27ae60', 'color': 'white'}),
            html.Div([html.H4("Total Orders"), html.H2(f"{total_orders:,}")], 
                     className="card", style={'background': '#3498db', 'color': 'white'}),
            html.Div([html.H4("Avg Order Value"), html.H2(f"${avg_order:,.2f}")], 
                     className="card", style={'background': '#e74c3c', 'color': 'white'}),
            html.Div([html.H4("Total Customers"), html.H2(f"{total_customers:,}")], 
                     className="card", style={'background': '#9b59b6', 'color': 'white'}),
        ], className="stats-row"),
        
        html.Div([
            html.Div([
                html.H3("Monthly Revenue Trend"),
                dcc.Graph(id='monthly-chart')
            ], className="chart-box"),
            html.Div([
                html.H3("Revenue by Category"),
                dcc.Graph(id='category-chart')
            ], className="chart-box"),
        ], className="charts-row"),
        
        html.Div([
            html.Div([
                html.H3("Top 10 Customers"),
                dcc.Graph(id='customer-chart')
            ], className="chart-box"),
            html.Div([
                html.H3("Revenue by City"),
                dcc.Graph(id='city-chart')
            ], className="chart-box"),
        ], className="charts-row"),
        
        html.Div([
            html.Div([
                html.H3("Orders by Status"),
                dcc.Graph(id='status-chart')
            ], className="chart-box"),
            html.Div([
                html.H3("Revenue by Age Group"),
                dcc.Graph(id='age-chart')
            ], className="chart-box"),
        ], className="charts-row"),
        
        html.Div([
            html.Div([
                html.H3("Quarterly Performance"),
                dcc.Graph(id='quarterly-chart')
            ], className="chart-box"),
            html.Div([
                html.H3("Top Products"),
                dcc.Graph(id='product-chart')
            ], className="chart-box"),
        ], className="charts-row"),
    ])
    
    @app.callback(
        Output('monthly-chart', 'figure'),
        Input('monthly-chart', 'id')
    )
    def update_monthly_chart(_):
        monthly = df[df['OrderStatus'] == 'Completed'].groupby('YearMonth')['TotalAmount'].sum().reset_index()
        fig = px.bar(monthly, x='YearMonth', y='TotalAmount', 
                    title='Monthly Revenue',
                    color_discrete_sequence=['#3498db'])
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        return fig
    
    @app.callback(
        Output('category-chart', 'figure'),
        Input('category-chart', 'id')
    )
    def update_category_chart(_):
        category = df[df['OrderStatus'] == 'Completed'].groupby('Category')['TotalAmount'].sum().reset_index()
        fig = px.pie(category, values='TotalAmount', names='Category',
                   title='Revenue by Category')
        return fig
    
    @app.callback(
        Output('customer-chart', 'figure'),
        Input('customer-chart', 'id')
    )
    def update_customer_chart(_):
        top_customers = df[df['OrderStatus'] == 'Completed'].groupby('CustomerName')['TotalAmount'].sum().nlargest(10).reset_index()
        fig = px.bar(top_customers, x='CustomerName', y='TotalAmount',
                    title='Top 10 Customers by Revenue',
                    color_discrete_sequence=['#27ae60'])
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', xaxis_tickangle=-45)
        return fig
    
    @app.callback(
        Output('city-chart', 'figure'),
        Input('city-chart', 'id')
    )
    def update_city_chart(_):
        city = df[df['OrderStatus'] == 'Completed'].groupby('City')['TotalAmount'].sum().nlargest(10).reset_index()
        fig = px.bar(city, x='City', y='TotalAmount',
                    title='Top 10 Cities by Revenue',
                    color_discrete_sequence=['#9b59b6'])
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', xaxis_tickangle=-45)
        return fig
    
    @app.callback(
        Output('status-chart', 'figure'),
        Input('status-chart', 'id')
    )
    def update_status_chart(_):
        status = df['OrderStatus'].value_counts().reset_index()
        fig = px.pie(status, values='OrderStatus', names='OrderStatus',
                   title='Order Status Distribution')
        return fig
    
    @app.callback(
        Output('age-chart', 'figure'),
        Input('age-chart', 'id')
    )
    def update_age_chart(_):
        age_groups = pd.cut(df['Age'], bins=[0, 25, 35, 45, 55, 65, 100], 
                          labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
        age = df[df['OrderStatus'] == 'Completed'].groupby(age_groups)['TotalAmount'].sum().reset_index()
        fig = px.bar(age, x='Age', y='TotalAmount',
                    title='Revenue by Age Group',
                    color_discrete_sequence=['#e74c3c'])
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        return fig
    
    @app.callback(
        Output('quarterly-chart', 'figure'),
        Input('quarterly-chart', 'id')
    )
    def update_quarterly_chart(_):
        quarterly = df[df['OrderStatus'] == 'Completed'].groupby(['Year', 'Quarter'])['TotalAmount'].sum().reset_index()
        quarterly['YearQuarter'] = quarterly['Year'].astype(str) + '-Q' + quarterly['Quarter'].astype(str)
        fig = px.bar(quarterly, x='YearQuarter', y='TotalAmount',
                    title='Quarterly Revenue',
                    color_discrete_sequence=['#3498db'])
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        return fig
    
    @app.callback(
        Output('product-chart', 'figure'),
        Input('product-chart', 'id')
    )
    def update_product_chart(_):
        products_top = df[df['OrderStatus'] == 'Completed'].groupby('ProductName')['TotalAmount'].sum().nlargest(10).reset_index()
        fig = px.bar(products_top, x='ProductName', y='TotalAmount',
                    title='Top 10 Products by Revenue',
                    color_discrete_sequence=['#f39c12'])
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', xaxis_tickangle=-45)
        return fig
    
    return app

if __name__ == '__main__':
    app = create_dashboard()
    app.run_server(debug=True, port=8050)

print("Dashboard can be run with: python dashboard.py")
print("Access at: http://localhost:8050")