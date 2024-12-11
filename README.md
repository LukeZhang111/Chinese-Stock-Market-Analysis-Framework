# Chinese Stock Market Analysis Framework

## Overview
A comprehensive Python-based analysis tool for studying Chinese stock markets (SSE and SZSE). This project provides in-depth analysis of stock performance, technical indicators, and market patterns using a Jupyter notebook interface.

## Prerequisites
- Python 3.8 or higher
- Jupyter Notebook/Lab
- Required Python packages:
```
pandas
numpy
matplotlib
seaborn
yfinance
scipy
statsmodels
```

## Installation

1. Install required packages:
```bash
pip install pandas numpy matplotlib seaborn yfinance scipy statsmodels
```

## Running the Analysis

1. Start Jupyter Notebook:
```bash
jupyter notebook
```

2. Open `Final.ipynb`

3. The notebook is structured in sections:
   - Setup and Configuration
   - Data Collection
   - Data Preprocessing
   - Technical Analysis
   - Risk Analysis
   - Exchange Analysis

4. Run cells sequentially (Shift + Enter) to:
   - Initialize the database
   - Fetch stock data
   - Process and analyze the data
   - Generate visualizations

## Using the Analysis Tools

### Stock Universe Configuration
Modify the `stock_universe` dictionary to analyze different stocks:
```python
stock_universe = {
    'SSE': {  # Shanghai Stock Exchange
        '600519.SS': 'Kweichow Moutai',
        # Add more SSE stocks...
    },
    'SZSE': {  # Shenzhen Stock Exchange
        '000858.SZ': 'Wuliangye Yibin',
        # Add more SZSE stocks...
    }
}
```

### Analysis Features

1. Technical Analysis:
```python
ta = TechnicalAnalysis(processed_data)
analysis_data = ta.add_technical_indicators()
```
- Calculates RSI, MACD, Bollinger Bands

2. Market Visualization:
```python
visualizer = MarketVisualizer(analysis_data)
visualizer.plot_price_with_indicators('600519.SS')  # Replace with desired stock symbol
visualizer.plot_market_comparison()
```
- Creates price charts with technical indicators
- Generates market comparisons

3. Volume Analysis:
```python
volume_analyzer = VolumeAnalysis(analysis_data)
volume_stats = volume_analyzer.analyze_all_stocks()
```
- Analyzes trading volumes and patterns

4. Risk Assessment:
```python
risk_analyzer = RiskAnalysis(analysis_data)
risk_metrics = risk_analyzer.analyze_all_stocks()
```
- Calculates volatility, VaR, and Sharpe ratios

5. Exchange Analysis:
```python
sector_analyzer = SectorAnalysis(analysis_data, stock_info)
sector_metrics, exchange_characteristics = sector_analyzer.analyze_sectors()
```
- Compares SSE and SZSE performance

6. All data from Yahoo Finance(https://finance.yahoo.com/)
   You can search for data for companies by typing something like '600519.SS', '601318.SS', '600036.SS', '601398.SS', '600276.SS', '000858.SZ', '000333.SZ', '000651.SZ', '000002.SZ', '002594.SZ'

### Customizing Analysis Parameters
Adjust analysis parameters in the `Config` class:
```python
class Config:
    START_DATE = datetime.now() - timedelta(days=365*2)  # Adjust time period
    MOVING_AVERAGES = [20, 50, 200]  # Modify MA periods
    VOLATILITY_WINDOW = 30  # Change volatility calculation window
    RISK_FREE_RATE = 0.03  # Update risk-free rate
```

## Output Examples
The analysis generates:
- Price charts with technical indicators
- Correlation heatmaps
- Volume analysis charts
- Risk metrics visualizations
- Exchange comparison plots
