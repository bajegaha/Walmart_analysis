
"""
Walmart Retail Sales Data Analysis Module

This module handles data analysis and visualization for the Walmart Retail Sales dataset.
It includes functions to analyze sales growth, profit by region and product category,
and create visualizations of the data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def setup_visualization_style():
    """
    Set up the visualization style for plots
    """
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8))

def analyze_yearly_sales(connection):
 
    query = """
    SELECT YEAR(`Order Date`) AS Year, 
           COUNT(*) AS Order_Line_Items 
    FROM sales 
    GROUP BY Year 
    ORDER BY Year;
    """
    return pd.read_sql_query(query, connection)

def create_yearly_state_sales_view(connection):
    """
    Create a SQL view for yearly state sales
    
    Args:
        connection: Database connection object
    """
    view_query = """
    CREATE OR REPLACE VIEW yearly_state_sales AS
    SELECT 
        State,
        YEAR(`Order Date`) AS Order_Year,
        SUM(Sales) AS Total_Sales
    FROM sales
    WHERE YEAR(`Order Date`) BETWEEN 2012 AND 2015
    GROUP BY State, Order_Year
    ORDER BY State, Order_Year;
    """
    connection.execute(view_query)

def calculate_sales_growth(connection):
    """
    Calculate sales growth rate by state and year
    
    Args:
        connection: Database connection object
        
    Returns:
        pandas.DataFrame: DataFrame with sales growth data
    """
    growth_query = """
    WITH yearly_data AS (
        SELECT * FROM yearly_state_sales
    )
    SELECT 
        State,
        Order_Year,
        Total_Sales,
        LAG(Total_Sales) OVER (PARTITION BY State ORDER BY Order_Year) AS Previous_Year_Sales,
        ROUND(
            (Total_Sales - LAG(Total_Sales) OVER (PARTITION BY State ORDER BY Order_Year)) / 
            LAG(Total_Sales) OVER (PARTITION BY State ORDER BY Order_Year) * 100, 
        2) AS Growth_Rate_Pct
    FROM yearly_data
    ORDER BY State, Order_Year;
    """
    return pd.read_sql_query(growth_query, connection)

def analyze_profit_by_subcategory(connection):
    """
    Analyze profit by product sub-category and region
    
    Args:
        connection: Database connection object
        
    Returns:
        pandas.DataFrame: DataFrame with profit by sub-category and region
    """
    profit_query = """
    SELECT 
        Region,
        `Product Sub-Category` AS Sub_Category,
        SUM(Profit) AS Total_Profit,
        COUNT(*) AS Order_Count
    FROM sales
    WHERE YEAR(`Order Date`) BETWEEN 2012 AND 2015
    GROUP BY Region, `Product Sub-Category`
    ORDER BY Region, Total_Profit DESC;
    """
    return pd.read_sql_query(profit_query, connection)

def find_top_products_by_region(connection):
    """
    Find top product sub-category in each region
    
    Args:
        connection: Database connection object
        
    Returns:
        pandas.DataFrame: DataFrame with top products by region
    """
    top_products_query = """
    WITH ranked_products AS (
        SELECT 
            Region,
            `Product Sub-Category` AS Sub_Category,
            SUM(Profit) AS Total_Profit,
            RANK() OVER (PARTITION BY Region ORDER BY SUM(Profit) DESC) AS rank_num
        FROM sales
        WHERE YEAR(`Order Date`) BETWEEN 2012 AND 2015
        GROUP BY Region, `Product Sub-Category`
    )
    SELECT Region, Sub_Category, Total_Profit
    FROM ranked_products
    WHERE rank_num = 1
    ORDER BY Total_Profit DESC;
    """
    return pd.read_sql_query(top_products_query, connection)

def visualize_top_subcategories(profit_df):
    """
    Visualize top sub-categories by profit for each region
    
    Args:
        profit_df (pandas.DataFrame): DataFrame with profit by sub-category and region
        
    Returns:
        matplotlib.figure.Figure: Figure with visualization
    """
    # Get top 5 sub-categories by profit for each region
    top_subcats = profit_df.groupby('Region').apply(
        lambda x: x.nlargest(5, 'Total_Profit')
    ).reset_index(drop=True)
    
    # Create plot
    plt.figure(figsize=(15, 10))
    g = sns.barplot(x='Sub_Category', y='Total_Profit', hue='Region', data=top_subcats)
    plt.title('Top 5 Most Profitable Sub-Categories by Region (2012-2015)', fontsize=16)
    plt.xlabel('Product Sub-Category', fontsize=14)
    plt.ylabel('Total Profit ($)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Region')
    plt.tight_layout()
    
    return plt.gcf()

def visualize_sales_growth(sales_growth_df):
    """
    Visualize sales growth for selected states
    
    Args:
        sales_growth_df (pandas.DataFrame): DataFrame with sales growth data
        
    Returns:
        matplotlib.figure.Figure: Figure with visualization
    """
    # Select a few interesting states for visualization
    selected_states = ['California', 'New York', 'Texas', 'Florida', 'Illinois']
    filtered_df = sales_growth_df[sales_growth_df['State'].isin(selected_states)]
    
    # Create plot
    plt.figure(figsize=(14, 8))
    for state in selected_states:
        state_data = filtered_df[filtered_df['State'] == state]
        plt.plot(state_data['Order_Year'], state_data['Total_Sales'], marker='o', linewidth=2, label=state)
    
    plt.title('Yearly Sales Trend for Selected States (2012-2015)', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Total Sales ($)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='State')
    plt.tight_layout()
    
    return plt.gcf()

def main():
    """
    Main function to execute the data analysis process
    """
    from database_operations import create_database_connection, connect_to_database
    
    # Create database connection
    # Note: Replace with your actual credentials
    engine = create_database_connection('root', 'database123', 'localhost', 'walmart')
    connection = connect_to_database(engine)
    
    # Set up visualization style
    setup_visualization_style()
    
    # Analyze yearly sales
    yearly_sales = analyze_yearly_sales(connection)
    print("Yearly Sales Analysis:")
    print(yearly_sales)
    
    # Create view for yearly state sales
    create_yearly_state_sales_view(connection)
    
    # Calculate sales growth
    sales_growth_df = calculate_sales_growth(connection)
    print("\nSales Growth Analysis:")
    print(sales_growth_df.head())
    
    # Analyze profit by sub-category and region
    profit_df = analyze_profit_by_subcategory(connection)
    print("\nProfit by Sub-Category and Region:")
    print(profit_df.head())
    
    # Find top products by region
    top_products_df = find_top_products_by_region(connection)
    print("\nTop Products by Region:")
    print(top_products_df)
    
    # Visualize top sub-categories
    visualize_top_subcategories(profit_df)
    plt.savefig('top_subcategories.png')
    
    # Visualize sales growth
    visualize_sales_growth(sales_growth_df)
    plt.savefig('sales_growth.png')
    
    # Close connection
    connection.close()
    
    print("Data analysis completed successfully!")

if __name__ == "__main__":
    main()
