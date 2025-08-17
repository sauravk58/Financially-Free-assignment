# Vehicle Registration Analytics Dashboard

🎥 **Walkthrough Video**  
[![Watch the demo](<img width="1364" height="609" alt="image" src="https://github.com/user-attachments/assets/49c04f50-847a-41bf-924a-a38cc301c042" />)
](https://youtu.be/TKqCtzP02uA)

An interactive Streamlit dashboard for analyzing vehicle registration data with an investor's perspective, built for backend developer internship assignment.

## 🎯 Project Overview

This dashboard provides comprehensive analysis of vehicle registration trends using data similar to the Vahan Dashboard format. It focuses on:

- **YoY (Year-over-Year) and QoQ (Quarter-over-Quarter) growth analysis**
- **Vehicle category performance (2W/3W/4W)**
- **Manufacturer-wise registration trends**
- **Investment insights and market analysis**

## 🚀 Features

### Core Analytics
- **Interactive Filters**: Date range, vehicle categories, and manufacturer selection
- **Growth Metrics**: Automated YoY and QoQ growth calculations
- **Trend Visualization**: Time series charts with category breakdowns
- **Market Share Analysis**: Pie charts and bar graphs for market distribution

### Investor-Focused Insights
- **Key Performance Indicators**: Total registrations, growth rates, market leaders
- **Manufacturer Performance**: Growth comparison and trend analysis
- **Market Concentration**: Analysis of top manufacturers' market control
- **Seasonal Patterns**: Peak and low registration periods identification

### Technical Features
- **Responsive Design**: Clean, professional UI optimized for investor presentations
- **Real-time Filtering**: Dynamic data updates based on user selections
- **Export Capabilities**: Downloadable insights and reports
- **Modular Architecture**: Separate modules for data collection, processing, and visualization

## 📊 Dashboard Sections

1. **Overview Tab**: General trends and market share visualization
2. **Growth Analysis Tab**: YoY and QoQ growth metrics with detailed breakdowns
3. **Manufacturer Analysis Tab**: Company-specific performance and comparisons
4. **Insights Tab**: Key findings and investment recommendations

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
\`\`\`bash
git clone <repository-url>
cd vehicle-registration-dashboard
\`\`\`

2. **Install dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Run the dashboard**
\`\`\`bash
streamlit run app.py
\`\`\`

4. **Access the dashboard**
Open your browser and navigate to `http://localhost:8501`

### Alternative Setup with Virtual Environment
\`\`\`bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
\`\`\`

## 📁 Project Structure

\`\`\`
vehicle-registration-dashboard/
├── app.py                 # Main Streamlit application
├── data_collector.py      # Data collection from Vahan Dashboard
├── utils.py              # Utility functions for data processing
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
└── data/                # Data storage directory (if using local files)
\`\`\`

## 📈 Data Assumptions

### Data Source
- **Primary**: Vahan Dashboard public API (when available)
- **Fallback**: Sample data generated to match Vahan data structure
- **Format**: Monthly vehicle registration data by category and manufacturer

### Data Structure
```python
{
    'Date': datetime,           # Registration date
    'Category': str,           # Vehicle category (2W/3W/4W)
    'Manufacturer': str,       # Vehicle manufacturer
    'Registrations': int,      # Number of registrations
    'State': str,             # State code (optional)
    'Year': int,              # Year extracted from date
    'Quarter': str            # Quarter (Q1/Q2/Q3/Q4)
}
