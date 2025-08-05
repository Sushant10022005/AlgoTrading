# Algo-Trading System 

## Features

- Fetches historical data for 3 NIFTY 50 stocks (RELIANCE, HDFCBANK, INFY)
- Uses Alpha Vantage API with fallback to yfinance
- Calculates RSI, MACD, 20-DMA, 50-DMA
- Strategy: Buy signal triggered when RSI < 30 and 20-DMA crosses above 50-DMA
- Backtests the strategy over 6 months
- Logs trade prices, volume, and sentiment to Google Sheets
- Logs return %, win ratio %, and ML accuracy/confusion matrix to Sheets
- Applies Logistic Regression to predict next-day stock movement

## Tech Stack

- Python (pandas, scikit-learn, yfinance)
- Google Sheets API (gspread + oauth2client)
- Alpha Vantage + NewsAPI for stock + sentiment data
- TextBlob for sentiment scoring

## Google Sheets Output

- **Trade_Log**: Stock prices, volume, sentiment
- **Summary**: Return %, Win Ratio %, Sentiment
- **ML_Results**: Accuracy and Confusion Matrix

## How to Run

1. Create a `.env` file:

2. Place your `credentials.json` (Google Sheets API) in the project root

3. Install dependencies:
    `pip install -r requirements.txt`

4. Run the script:
    `python src/main.py`

## ✅ Output Example

RELIANCE.NS: Return = 2.27%, Win Ratio = 100.00%
INFY.NS: Return = 0.00%, Win Ratio = 0.00%

Google Sheets will be updated in real-time with all trade logs, strategy summary, and ML results.
`https://docs.google.com/spreadsheets/d/1aKdGBSVpMdpNHnLUcrjRJos8bhUI7OYwCy2vRmDsJr0/edit?usp=sharing`

