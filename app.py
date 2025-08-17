import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Vehicle Registration Analytics Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    """Generate sample vehicle registration data similar to Vahan Dashboard"""
    np.random.seed(42)
    
    # Date range for the last 3 years
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2024, 3, 31)
    
    # Generate monthly data
    date_range = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # Vehicle categories
    categories = ['2W', '3W', '4W']
    
    # Major manufacturers by category
    manufacturers = {
        '2W': ['Hero MotoCorp', 'Honda', 'TVS', 'Bajaj', 'Yamaha', 'Royal Enfield'],
        '3W': ['Bajaj', 'Mahindra', 'Piaggio', 'TVS', 'Force Motors'],
        '4W': ['Maruti Suzuki', 'Hyundai', 'Tata Motors', 'Mahindra', 'Kia', 'Honda Cars']
    }
    
    data = []
    
    for date in date_range:
        for category in categories:
            for manufacturer in manufacturers[category]:
                # Base registrations with seasonal trends
                base_registrations = {
                    '2W': np.random.normal(15000, 3000),
                    '3W': np.random.normal(2000, 500),
                    '4W': np.random.normal(8000, 2000)
                }
                
                # Add growth trends and seasonality
                year_factor = 1 + (date.year - 2021) * 0.1  # 10% annual growth base
                seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * date.month / 12)  # Seasonal variation
                
                registrations = max(0, int(base_registrations[category] * year_factor * seasonal_factor))
                
                data.append({
                    'Date': date,
                    'Year': date.year,
                    'Quarter': f"Q{(date.month-1)//3 + 1}",
                    'Month': date.strftime('%B'),
                    'Category': category,
                    'Manufacturer': manufacturer,
                    'Registrations': registrations
                })
    
    return pd.DataFrame(data)

def calculate_growth_metrics(df, groupby_cols, value_col='Registrations'):
    """Calculate YoY and QoQ growth metrics"""
    df_grouped = df.groupby(groupby_cols + ['Year', 'Quarter'])[value_col].sum().reset_index()
    
    # Calculate YoY growth
    df_grouped['YoY_Growth'] = df_grouped.groupby(groupby_cols + ['Quarter'])[value_col].pct_change(periods=1) * 100
    
    # Calculate QoQ growth
    df_grouped['QoQ_Growth'] = df_grouped.groupby(groupby_cols)[value_col].pct_change(periods=1) * 100
    
    return df_grouped

def create_trend_chart(df, title, y_col='Registrations'):
    """Create trend line chart"""
    fig = px.line(df, x='Date', y=y_col, color='Category' if 'Category' in df.columns else None,
                  title=title, markers=True)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Registrations",
        hovermode='x unified',
        template='plotly_white'
    )
    return fig

def create_growth_chart(df, growth_type='YoY_Growth'):
    """Create growth percentage chart"""
    fig = px.bar(df, x='Quarter', y=growth_type, color='Category',
                 title=f"{growth_type.replace('_', ' ')} by Quarter",
                 barmode='group')
    fig.update_layout(
        xaxis_title="Quarter",
        yaxis_title="Growth %",
        template='plotly_white'
    )
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🚗 Vehicle Registration Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("**Investor-Focused Analysis of Vehicle Registration Trends**")
    
    # Load data
    with st.spinner("Loading vehicle registration data..."):
        df = load_sample_data()
    
    # Sidebar filters
    st.sidebar.header("📊 Dashboard Filters")
    
    # Date range selection
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Vehicle category filter
    categories = st.sidebar.multiselect(
        "Select Vehicle Categories",
        options=df['Category'].unique(),
        default=df['Category'].unique()
    )
    
    # Manufacturer filter
    manufacturers = st.sidebar.multiselect(
        "Select Manufacturers",
        options=sorted(df['Manufacturer'].unique()),
        default=sorted(df['Manufacturer'].unique())[:10]  # Default to top 10
    )
    
    # Filter data
    if len(date_range) == 2:
        filtered_df = df[
            (df['Date'].dt.date >= date_range[0]) &
            (df['Date'].dt.date <= date_range[1]) &
            (df['Category'].isin(categories)) &
            (df['Manufacturer'].isin(manufacturers))
        ]
    else:
        filtered_df = df[
            (df['Category'].isin(categories)) &
            (df['Manufacturer'].isin(manufacturers))
        ]
    
    if filtered_df.empty:
        st.error("No data available for the selected filters. Please adjust your selection.")
        return
    
    # Key Metrics Section
    st.header("📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate key metrics
    total_registrations = filtered_df['Registrations'].sum()
    avg_monthly_registrations = filtered_df.groupby(['Year', 'Month'])['Registrations'].sum().mean()
    
    # Latest quarter data for growth calculation
    latest_quarter_data = filtered_df[filtered_df['Year'] == filtered_df['Year'].max()]
    prev_quarter_data = filtered_df[filtered_df['Year'] == (filtered_df['Year'].max() - 1)]
    
    if not prev_quarter_data.empty:
        latest_total = latest_quarter_data['Registrations'].sum()
        prev_total = prev_quarter_data['Registrations'].sum()
        yoy_growth = ((latest_total - prev_total) / prev_total) * 100 if prev_total > 0 else 0
    else:
        yoy_growth = 0
    
    with col1:
        st.metric(
            label="Total Registrations",
            value=f"{total_registrations:,}",
            delta=f"{yoy_growth:.1f}% YoY"
        )
    
    with col2:
        st.metric(
            label="Avg Monthly Registrations",
            value=f"{avg_monthly_registrations:,.0f}"
        )
    
    with col3:
        top_category = filtered_df.groupby('Category')['Registrations'].sum().idxmax()
        st.metric(
            label="Leading Category",
            value=top_category
        )
    
    with col4:
        top_manufacturer = filtered_df.groupby('Manufacturer')['Registrations'].sum().idxmax()
        st.metric(
            label="Top Manufacturer",
            value=top_manufacturer
        )
    
    # Main Dashboard Content
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Growth Analysis", "🏭 Manufacturer Analysis", "💡 Insights"])
    
    with tab1:
        st.subheader("Registration Trends Overview")
        
        # Overall trend by category
        monthly_data = filtered_df.groupby(['Date', 'Category'])['Registrations'].sum().reset_index()
        fig_trend = create_trend_chart(monthly_data, "Monthly Vehicle Registrations by Category")
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Market share pie chart
        col1, col2 = st.columns(2)
        
        with col1:
            category_totals = filtered_df.groupby('Category')['Registrations'].sum()
            fig_pie = px.pie(values=category_totals.values, names=category_totals.index,
                           title="Market Share by Vehicle Category")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Top 10 manufacturers
            top_manufacturers = filtered_df.groupby('Manufacturer')['Registrations'].sum().nlargest(10)
            fig_bar = px.bar(x=top_manufacturers.values, y=top_manufacturers.index,
                           orientation='h', title="Top 10 Manufacturers by Registrations")
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab2:
        st.subheader("Growth Analysis (YoY & QoQ)")
        
        # Calculate growth metrics
        growth_data = calculate_growth_metrics(filtered_df, ['Category'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # YoY Growth
            yoy_data = growth_data.dropna(subset=['YoY_Growth'])
            if not yoy_data.empty:
                fig_yoy = create_growth_chart(yoy_data, 'YoY_Growth')
                st.plotly_chart(fig_yoy, use_container_width=True)
        
        with col2:
            # QoQ Growth
            qoq_data = growth_data.dropna(subset=['QoQ_Growth'])
            if not qoq_data.empty:
                fig_qoq = create_growth_chart(qoq_data, 'QoQ_Growth')
                st.plotly_chart(fig_qoq, use_container_width=True)
        
        # Growth table
        st.subheader("Detailed Growth Metrics")
        if not growth_data.empty:
            display_data = growth_data[['Year', 'Quarter', 'Category', 'Registrations', 'YoY_Growth', 'QoQ_Growth']].round(2)
            st.dataframe(display_data, use_container_width=True)
    
    with tab3:
        st.subheader("Manufacturer Performance Analysis")
        
        # Manufacturer growth analysis
        manufacturer_growth = calculate_growth_metrics(filtered_df, ['Manufacturer'])
        
        # Top growing manufacturers
        if not manufacturer_growth.empty:
            latest_growth = manufacturer_growth[manufacturer_growth['Year'] == manufacturer_growth['Year'].max()]
            top_growing = latest_growth.nlargest(10, 'YoY_Growth')[['Manufacturer', 'Registrations', 'YoY_Growth']]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Top Growing Manufacturers (YoY)**")
                st.dataframe(top_growing.round(2), use_container_width=True)
            
            with col2:
                # Manufacturer trend for selected manufacturers
                selected_manufacturers = st.multiselect(
                    "Select manufacturers to compare trends:",
                    options=sorted(filtered_df['Manufacturer'].unique()),
                    default=sorted(filtered_df['Manufacturer'].unique())[:5]
                )
                
                if selected_manufacturers:
                    manufacturer_trend_data = filtered_df[filtered_df['Manufacturer'].isin(selected_manufacturers)]
                    monthly_manufacturer_data = manufacturer_trend_data.groupby(['Date', 'Manufacturer'])['Registrations'].sum().reset_index()
                    
                    fig_manufacturer_trend = px.line(monthly_manufacturer_data, x='Date', y='Registrations', 
                                                   color='Manufacturer', title="Manufacturer Trend Comparison")
                    st.plotly_chart(fig_manufacturer_trend, use_container_width=True)
    
    with tab4:
        st.subheader("💡 Investment Insights & Key Findings")
        
        # Calculate insights
        total_by_category = filtered_df.groupby('Category')['Registrations'].sum()
        growth_by_category = calculate_growth_metrics(filtered_df, ['Category'])
        
        # Key insights
        st.markdown("""
        <div class="insight-box">
        <h4>🎯 Key Investment Insights:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        insights = []
        
        # Market dominance insight
        dominant_category = total_by_category.idxmax()
        dominant_share = (total_by_category[dominant_category] / total_by_category.sum()) * 100
        insights.append(f"**Market Leadership**: {dominant_category} vehicles dominate with {dominant_share:.1f}% market share")
        
        # Growth insight
        if not growth_by_category.empty:
            latest_growth = growth_by_category[growth_by_category['Year'] == growth_by_category['Year'].max()]
            if not latest_growth.empty:
                fastest_growing = latest_growth.loc[latest_growth['YoY_Growth'].idxmax()]
                insights.append(f"**Growth Leader**: {fastest_growing['Category']} showing strongest YoY growth at {fastest_growing['YoY_Growth']:.1f}%")
        
        # Manufacturer concentration
        top_5_manufacturers = filtered_df.groupby('Manufacturer')['Registrations'].sum().nlargest(5)
        concentration_ratio = (top_5_manufacturers.sum() / filtered_df['Registrations'].sum()) * 100
        insights.append(f"**Market Concentration**: Top 5 manufacturers control {concentration_ratio:.1f}% of the market")
        
        # Seasonal patterns
        monthly_avg = filtered_df.groupby('Month')['Registrations'].mean()
        peak_month = monthly_avg.idxmax()
        insights.append(f"**Seasonality**: Peak registration period is {peak_month}")
        
        for insight in insights:
            st.markdown(f"• {insight}")
        
        # Investment recommendations
        st.markdown("""
        <div class="insight-box">
        <h4>📊 Investment Recommendations:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        recommendations = [
            "**Electric Vehicle Transition**: Monitor EV adoption rates across categories for future investment opportunities",
            "**Supply Chain Resilience**: Focus on manufacturers with consistent growth patterns and market stability",
            "**Regional Expansion**: Analyze geographic distribution for untapped market potential",
            "**Technology Integration**: Invest in companies leading in connected vehicle technologies",
            "**Financing Solutions**: Vehicle financing companies show correlation with registration growth"
        ]
        
        for rec in recommendations:
            st.markdown(f"• {rec}")
        
        # Data summary
        st.subheader("📋 Data Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Data Points", len(filtered_df))
        with col2:
            st.metric("Date Range", f"{filtered_df['Date'].min().strftime('%Y-%m')} to {filtered_df['Date'].max().strftime('%Y-%m')}")
        with col3:
            st.metric("Manufacturers Covered", filtered_df['Manufacturer'].nunique())

if __name__ == "__main__":
    main()
