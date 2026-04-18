import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import warnings
warnings.filterwarnings('ignore')

DATA_PATH = 'C:/Users/user/Desktop/dataanlysisi 2/data/dataset.xlsx'
OUTPUT_PATH = 'C:/Users/user/Desktop/dataanlysisi 2/dashboard/dashboard.html'

def load_and_prepare():
    customers = pd.read_excel(DATA_PATH, sheet_name='Customers')
    products = pd.read_excel(DATA_PATH, sheet_name='Products')
    orders = pd.read_excel(DATA_PATH, sheet_name='Orders')
    
    orders['OrderDate'] = pd.to_datetime(orders['OrderDate'])
    df = orders.merge(customers, on='CustomerID').merge(products, on='ProductID')
    df['YearMonth'] = df['OrderDate'].dt.to_period('M').astype(str)
    df['Year'] = df['OrderDate'].dt.year
    df['Quarter'] = df['OrderDate'].dt.quarter
    return df

def create_dashboard_html(df):
    completed = df[df['OrderStatus'] == 'Completed']
    
    total_revenue = completed['TotalAmount'].sum()
    total_orders = len(completed)
    avg_order = completed['TotalAmount'].mean()
    total_customers = df['CustomerID'].nunique()
    cancel_rate = (df['OrderStatus'] == 'Cancelled').sum() / len(df) * 100
    
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            'Monthly Revenue Trend', 'Revenue by Category',
            'Top 10 Customers', 'Top 10 Cities',
            'Orders by Status', 'Revenue by Age Group'
        ),
        specs=[[{'type': 'bar'}, {'type': 'pie'}],
               [{'type': 'bar'}, {'type': 'bar'}],
               [{'type': 'pie'}, {'type': 'bar'}]],
        horizontal_spacing=0.12,
        vertical_spacing=0.10
    )
    
    monthly = completed.groupby('YearMonth')['TotalAmount'].sum().reset_index()
    fig.add_trace(go.Bar(x=monthly['YearMonth'], y=monthly['TotalAmount'], 
                      name='Revenue', marker_color='#3498db'),
                row=1, col=1)
    
    category = completed.groupby('Category')['TotalAmount'].sum().reset_index()
    fig.add_trace(go.Pie(labels=category['Category'], values=category['TotalAmount'],
                       name='Category', hole=0.4),
                row=1, col=2)
    
    top_customers = completed.groupby('CustomerName')['TotalAmount'].sum().nlargest(10).reset_index()
    fig.add_trace(go.Bar(x=top_customers['TotalAmount'], y=top_customers['CustomerName'],
                       orientation='h', name='Customers', marker_color='#27ae60'),
                row=2, col=1)
    
    top_cities = completed.groupby('City')['TotalAmount'].sum().nlargest(10).reset_index()
    fig.add_trace(go.Bar(x=top_cities['City'], y=top_cities['TotalAmount'],
                       name='Cities', marker_color='#9b59b6'),
                row=2, col=2)
    
    status = df['OrderStatus'].value_counts().reset_index()
    fig.add_trace(go.Pie(labels=status['OrderStatus'], values=status['OrderStatus'],
                       name='Status', hole=0.4),
                row=3, col=1)
    
    age_groups = pd.cut(completed['Age'], bins=[0, 25, 35, 45, 55, 65, 100], 
                      labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
    age = completed.groupby(age_groups)['TotalAmount'].sum().reset_index()
    fig.add_trace(go.Bar(x=age['Age'], y=age['TotalAmount'],
                       name='Age', marker_color='#e74c3c'),
                row=3, col=2)
    
    fig.update_layout(
        title=dict(
            text=f"""<b>Data Analytics Dashboard</b><br>
            <sub>Total Revenue: ${total_revenue:,.2f} | Orders: {total_orders} | Avg Order: ${avg_order:,.2f} | Customers: {total_customers} | Cancellation Rate: {cancel_rate:.1f}%</sub>""",
            x=0.5
        ),
        height=1200,
        showlegend=False,
        template='plotly_white'
    )
    
    fig.update_annotations(font_size=12)
    
    return fig

def generate_html_dashboard():
    df = load_and_prepare()
    fig = create_dashboard_html(df)
    fig.write_html(OUTPUT_PATH)
    print(f"Interactive dashboard saved to: {OUTPUT_PATH}")

if __name__ == '__main__':
    generate_html_dashboard()