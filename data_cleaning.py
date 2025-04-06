
"""
Walmart Retail Sales Data Cleaning Module

This module handles the data cleaning operations for the Walmart Retail Sales dataset.
It includes functions to clean product names, format dates, and export the cleaned data to CSV.
"""

import pandas as pd
import csv

def load_data(file_path):
    return pd.read_excel(file_path)

def clean_product_names(df):
    df["Product Name"] = df["Product Name"].str.encode('ascii', errors='ignore').str.decode('ascii')
    return df

def format_dates(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

def export_to_csv(df, output_file):
    """
    Export cleaned data to CSV with pipe delimiter
    
    Args:
        df (pandas.DataFrame): DataFrame to export
        output_file (str): Output file path
    """
    df.to_csv(output_file, sep="|", quoting=csv.QUOTE_ALL, 
              doublequote=False, escapechar="\\", index=False)

def main():
    """
    Main function to execute the data cleaning process
    """
    # Load the dataset
    sales = load_data("WalmartRetailSales.xlsx")
    
    # Clean product names
    sales = clean_product_names(sales)
    
    # Format dates
    sales = format_dates(sales)
    
    # Export cleaned data
    export_to_csv(sales, "WalmartRetailSales_Cleaned.csv")
    
    print("Data cleaning completed successfully!")

if __name__ == "__main__":
    main()
