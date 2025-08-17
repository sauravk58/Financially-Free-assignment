"""
Utility functions for data processing and analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def clean_registration_data(df):
    """
    Clean and standardize vehicle registration data
    
    Args:
        df (pd.DataFrame): Raw registration data
    
    Returns:
        pd.DataFrame: Cleaned data
    """
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df = df.dropna(subset=['Registrations'])
    
    # Standardize date format
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    
    # Standardize vehicle categories
    category_mapping = {
        'Two Wheeler': '2W',
        'Three Wheeler': '3W',
        'Four Wheeler': '4W',
        'Motor Cycle': '2W',
        'Scooter': '2W',
        'Auto Rickshaw': '3W',
        'Car': '4W',
        'SUV': '4W'
    }
    
    if 'Category' in df.columns:
        df['Category'] = df['Category'].map(category_mapping).fillna(df['Category'])
    
    return df

def calculate_market_metrics(df):
    """
    Calculate various market metrics for investment analysis
    
    Args:
        df (pd.DataFrame): Vehicle registration data
    
    Returns:
        dict: Market metrics
    """
    metrics = {}
    
    # Market size
    metrics['total_registrations'] = df['Registrations'].sum()
    
    # Market share by category
    category_share = df.groupby('Category')['Registrations'].sum()
    metrics['category_market_share'] = (category_share / category_share.sum() * 100).to_dict()
    
    # Top manufacturers
    manufacturer_totals = df.groupby('Manufacturer')['Registrations'].sum()
    metrics['top_manufacturers'] = manufacturer_totals.nlargest(10).to_dict()
    
    # Growth rates
    if 'Date' in df.columns:
        df_monthly = df.groupby([df['Date'].dt.to_period('M'), 'Category'])['Registrations'].sum().reset_index()
        df_monthly['Date'] = df_monthly['Date'].dt.to_timestamp()
        
        # Calculate YoY growth
        df_monthly['Year'] = df_monthly['Date'].dt.year
        df_monthly['Month'] = df_monthly['Date'].dt.month
        
        yoy_growth = df_monthly.groupby(['Category', 'Month'])['Registrations'].pct_change(periods=1) * 100
        metrics['avg_yoy_growth'] = yoy_growth.groupby('Category').mean().to_dict()
    
    return metrics

def identify_trends(df):
    """
    Identify key trends in the data for investor insights
    
    Args:
        df (pd.DataFrame): Vehicle registration data
    
    Returns:
        list: List of trend insights
    """
    trends = []
    
    # Seasonal trends
    if 'Date' in df.columns:
        monthly_avg = df.groupby(df['Date'].dt.month)['Registrations'].mean()
        peak_month = monthly_avg.idxmax()
        low_month = monthly_avg.idxmin()
        
        trends.append(f"Peak registration month: {peak_month}")
        trends.append(f"Lowest registration month: {low_month}")
    
    # Category trends
    category_totals = df.groupby('Category')['Registrations'].sum()
    dominant_category = category_totals.idxmax()
    trends.append(f"Dominant vehicle category: {dominant_category}")
    
    # Manufacturer concentration
    manufacturer_totals = df.groupby('Manufacturer')['Registrations'].sum()
    top_5_share = manufacturer_totals.nlargest(5).sum() / manufacturer_totals.sum() * 100
    trends.append(f"Top 5 manufacturers control {top_5_share:.1f}% of market")
    
    return trends

def export_insights_report(df, filename="vehicle_insights_report.txt"):
    """
    Export key insights to a text report
    
    Args:
        df (pd.DataFrame): Vehicle registration data
        filename (str): Output filename
    """
    metrics = calculate_market_metrics(df)
    trends = identify_trends(df)
    
    with open(filename, 'w') as f:
        f.write("VEHICLE REGISTRATION ANALYTICS REPORT\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("KEY METRICS:\n")
        f.write(f"Total Registrations: {metrics['total_registrations']:,}\n")
        f.write("\nMarket Share by Category:\n")
        for category, share in metrics['category_market_share'].items():
            f.write(f"  {category}: {share:.1f}%\n")
        
        f.write("\nTop Manufacturers:\n")
        for manufacturer, registrations in list(metrics['top_manufacturers'].items())[:5]:
            f.write(f"  {manufacturer}: {registrations:,}\n")
        
        f.write("\nKEY TRENDS:\n")
        for trend in trends:
            f.write(f"• {trend}\n")
        
        f.write(f"\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"Report exported to {filename}")
