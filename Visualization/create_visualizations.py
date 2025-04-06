#!/usr/bin/env python3
"""
Walmart Retail Sales Visualization Generator

This script creates visualizations for the Walmart Retail Sales Analysis project.
It generates various charts and graphs to visualize sales trends, profitability,
and other key metrics from the Walmart retail sales data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Create visualizations directory if it doesn't exist
os.makedirs('visualizations', exist_ok=True)

# Set visualization style
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Sample data creation (in a real scenario, this would be loaded from the database)
# Creating yearly sales data
years = list(range(2001, 2016))
order_line_items = [322, 299, 277, 289, 310, 271, 247, 276, 288, 306, 245, 1580, 1325, 1144, 1220]
yearly_sales_df = pd.DataFrame({'Year': years, 'Order_Line_Items': order_line_items})

# Creating sales growth data for selected states
states = ['California', 'New York', 'Texas', 'Florida', 'Illinois']
years_growth = [2012, 2013, 2014, 2015]
sales_data = {
    'California': [250000, 275000, 310000, 290000],
    'New York': [180000, 195000, 210000, 230000],
    'Texas': [220000, 240000, 235000, 260000],
    'Florida': [160000, 175000, 190000, 205000],
    'Illinois': [140000, 130000, 150000, 165000]
}

# Creating profit by region and subcategory data
regions = ['East', 'West', 'Central', 'South']
subcategories = [
    'Office Machines', 'Telephones and Communication', 
    'Binders and Binder Accessories', 'Copiers and Fax',
    'Chairs & Chairmats', 'Computer Peripherals'
]

# Generate random profit data for each region and subcategory
np.random.seed(42)  # For reproducibility
profit_data = []
for region in regions:
    for subcategory in subcategories:
        profit = np.random.randint(5000, 90000)
        order_count = np.random.randint(20, 200)
        profit_data.append({
            'Region': region,
            'Sub_Category': subcategory,
            'Total_Profit': profit,
            'Order_Count': order_count
        })
profit_df = pd.DataFrame(profit_data)

# Visualization 1: Yearly Sales Trend
def create_yearly_sales_chart():
    plt.figure(figsize=(14, 8))
    ax = sns.barplot(x='Year', y='Order_Line_Items', data=yearly_sales_df, palette='viridis')
    
    # Add value labels on top of bars
    for i, v in enumerate(yearly_sales_df['Order_Line_Items']):
        ax.text(i, v + 30, str(v), ha='center', fontweight='bold')
    
    plt.title('Yearly Sales Trend (2001-2015)', fontsize=18)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Order Line Items', fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('visualizations/yearly_sales_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created yearly sales trend visualization")

# Visualization 2: Sales Growth for Selected States
def create_sales_growth_chart():
    plt.figure(figsize=(14, 8))
    
    for state in states:
        plt.plot(years_growth, sales_data[state], marker='o', linewidth=2, label=state)
    
    plt.title('Yearly Sales Trend for Selected States (2012-2015)', fontsize=18)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Total Sales ($)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='State', fontsize=12)
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('visualizations/state_sales_growth.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created state sales growth visualization")

# Visualization 3: Top Profitable Subcategories by Region
def create_top_subcategories_chart():
    # Get top 3 subcategories by profit for each region
    top_subcats = profit_df.groupby('Region').apply(
        lambda x: x.nlargest(3, 'Total_Profit')
    ).reset_index(drop=True)
    
    plt.figure(figsize=(16, 10))
    g = sns.barplot(x='Sub_Category', y='Total_Profit', hue='Region', data=top_subcats, palette='Set2')
    
    plt.title('Top 3 Most Profitable Sub-Categories by Region', fontsize=18)
    plt.xlabel('Product Sub-Category', fontsize=14)
    plt.ylabel('Total Profit ($)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Region', fontsize=12)
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('visualizations/top_subcategories_by_region.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created top subcategories by region visualization")

# Visualization 4: Profit vs Order Count Scatter Plot
def create_profit_vs_orders_chart():
    plt.figure(figsize=(14, 8))
    
    sns.scatterplot(
        x='Order_Count', 
        y='Total_Profit', 
        hue='Region', 
        size='Total_Profit',
        sizes=(100, 1000),
        alpha=0.7,
        data=profit_df,
        palette='deep'
    )
    
    plt.title('Profit vs Order Count by Region', fontsize=18)
    plt.xlabel('Number of Orders', fontsize=14)
    plt.ylabel('Total Profit ($)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Region', fontsize=12)
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('visualizations/profit_vs_orders.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created profit vs orders visualization")

# Visualization 5: Regional Profit Distribution
def create_regional_profit_distribution():
    # Calculate total profit by region
    region_profit = profit_df.groupby('Region')['Total_Profit'].sum().reset_index()
    
    plt.figure(figsize=(12, 8))
    
    # Create pie chart
    plt.pie(
        region_profit['Total_Profit'], 
        labels=region_profit['Region'],
        autopct='%1.1f%%',
        startangle=90,
        shadow=True,
        explode=[0.05] * len(region_profit),
        colors=sns.color_palette('pastel'),
        wedgeprops={'edgecolor': 'black', 'linewidth': 1}
    )
    
    plt.title('Profit Distribution by Region', fontsize=18)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('visualizations/regional_profit_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created regional profit distribution visualization")

if __name__ == "__main__":
    print("Generating visualizations for Walmart Retail Sales Analysis...")
    
    # Create all visualizations
    create_yearly_sales_chart()
    create_sales_growth_chart()
    create_top_subcategories_chart()
    create_profit_vs_orders_chart()
    create_regional_profit_distribution()
    
    print("All visualizations created successfully!")
