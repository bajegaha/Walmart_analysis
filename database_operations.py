
"""
Walmart Retail Sales Database Operations Module

This module handles database operations for the Walmart Retail Sales dataset.
It includes functions to connect to MySQL, create tables, and execute SQL queries.
"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine, text

def create_database_connection(user, password, host, database):
    """
    Create a connection to MySQL database
    
    Args:
        user (str): MySQL username
        password (str): MySQL password
        host (str): MySQL host address
        database (str): Database name
        
    Returns:
        sqlalchemy.engine.Engine: Database engine
    """
    connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'
    engine = create_engine(connection_string)
    return engine

def connect_to_database(engine):
    """
    Create a connection object from engine
    
    Args:
        engine (sqlalchemy.engine.Engine): Database engine
        
    Returns:
        sqlalchemy.engine.Connection: Database connection
    """
    return engine.connect()

def execute_query(connection, query):
    """
    Execute SQL query
    
    Args:
        connection (sqlalchemy.engine.Connection): Database connection
        query (str): SQL query to execute
        
    Returns:
        sqlalchemy.engine.cursor.CursorResult: Query result
    """
    return connection.execute(text(query))

def read_sql_to_dataframe(query, connection):
    """
    Execute SQL query and return results as DataFrame
    
    Args:
        query (str): SQL query to execute
        connection (sqlalchemy.engine.Connection or sqlalchemy.engine.Engine): Database connection
        
    Returns:
        pandas.DataFrame: Query results as DataFrame
    """
    return pd.read_sql_query(query, connection)

def show_table_columns(engine, table_name):
    """
    Show columns in a table
    
    Args:
        engine (sqlalchemy.engine.Engine): Database engine
        table_name (str): Name of the table
        
    Returns:
        pandas.DataFrame: Table column information
    """
    query = f"SHOW COLUMNS FROM {table_name};"
    return pd.read_sql(query, con=engine)

def main():
    """
    Main function to demonstrate database operations
    """
    # Create database connection
    # Note: Replace with your actual credentials
    engine = create_database_connection('root', 'database123', 'localhost', 'walmart')
    
    # Create connection
    connection = connect_to_database(engine)
    
    # Example: Update Order Date column to DATE type
    execute_query(connection, "ALTER TABLE sales MODIFY `Order Date` DATE;")
    
    # Show table columns to verify the change
    columns_df = show_table_columns(engine, 'sales')
    print(columns_df)
    
    # Example: Read data from table
    sales_df = read_sql_to_dataframe("SELECT * FROM walmart.sales", connection)
    print(f"Total rows: {len(sales_df)}")
    
    # Close connection
    connection.close()
    
    print("Database operations completed successfully!")

if __name__ == "__main__":
    main()
