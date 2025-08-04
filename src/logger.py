import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import logging
import os

os.makedirs('logs', exist_ok=True)

logger = logging.getLogger('sheets_logger')
logger.setLevel(logging.DEBUG)

if logger.handlers:
    logger.handlers.clear()

handler = logging.FileHandler('logs/sheets.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

class SheetsLogger:
    def __init__(self, sheet_name='AlgoTrading'):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(sheet_name)
        self.trade_log = self.sheet.worksheet('Trade_Log')
        self.summary = self.sheet.worksheet('Summary')

    def log_stock_data(self, stock_data):
        try:
            headers = ['Date', 'Symbol', 'Close', 'Volume', 'Sentiment']
            data_rows = []
            for symbol, data in stock_data.items():
                df = data['price_data']
                sentiment = data['sentiment']
                if not df.empty:
                    if isinstance(df.columns, pd.MultiIndex):
                        df = df.xs(symbol, level='Ticker', axis=1)
                    df.columns = df.columns.str.lower()
                    latest = df.iloc[-1]  
                    data_rows.append([
                        df.index[-1].strftime('%Y-%m-%d'),
                        symbol,
                        latest['close'],
                        latest['volume'],
                        round(sentiment, 3)
                    ])
            self.trade_log.clear() 
            self.trade_log.update('A1', [headers] + data_rows)
            logger.info("Logged stock data to Google Sheets")
        except Exception as e:
            logger.error(f"Google Sheets error: {str(e)}")
    
    def log_summary(self, summary_data):
        try:
            headers = ['Symbol', 'Total Return (%)', 'Win Ratio (%)', 'Sentiment']
            self.summary.clear()
            self.summary.update('A1', [headers] + summary_data)
            logger.info("Logged strategy summary to Google Sheets")
        except Exception as e:
            logger.error(f"Error writing summary: {str(e)}")

    def log_ml_results(self, ml_results):
        try:
            headers = ['Symbol', 'Accuracy (%)', 'TN', 'FP', 'FN', 'TP']
            ml_sheet = self.sheet.worksheet('ML_Results')
            ml_sheet.clear()
            ml_sheet.update('A1', [headers] + ml_results)
            logger.info("Logged ML results to Google Sheets")
        except Exception as e:
            logger.error(f"Error writing ML results: {str(e)}")



if __name__ == '__main__':
    from datafetch import DataFetcher
    fetcher = DataFetcher()
    data = fetcher.fetch_stock_data()
    sheets_logger = SheetsLogger()  
    sheets_logger.log_stock_data(data)