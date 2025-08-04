import os
import time
import requests
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
from newsapi import NewsApiClient
from textblob import TextBlob

os.makedirs('logs', exist_ok=True)

logger = logging.getLogger('data_fetcher')
logger.setLevel(logging.INFO)

if logger.handlers:
    logger.handlers.clear()

handler = logging.FileHandler('logs/data_fetch.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

load_dotenv()

class DataFetcher:
    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_KEY')
        self.stocks = ['RELIANCE.NS', 'HDFCBANK.NS', 'INFY.NS']
        self.base_url = 'https://www.alphavantage.co/query'
        self.news_api = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

    def fetch_alpha_vantage(self, symbol):
        try:
            av_symbol = symbol.replace('.NS', '.BSE')
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': av_symbol,
                'apikey': self.alpha_vantage_key,
                'outputsize': 'full'  # Get 6+ months of data
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            if 'Time Series (Daily)' not in data:
                raise ValueError(f"No data for {av_symbol}")
            df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
            df = df.rename(columns={
                '1. open': 'open', '2. high': 'high', '3. low': 'low',
                '4. close': 'close', '5. volume': 'volume'
            })
            df.index = pd.to_datetime(df.index)
            df = df.astype(float)
            logger.info(f"Fetched Alpha Vantage data for {symbol} ({av_symbol})")
            return df.sort_index()
        except Exception as e:
            logger.error(f"Alpha Vantage error for {symbol} ({av_symbol}): {str(e)}")
            return None

    def fetch_yfinance(self, symbol):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=200) 
            df = yf.download(symbol, start=start_date, end=end_date, interval='1d', auto_adjust=False)
            if df.empty:
                raise ValueError(f"No data for {symbol}")
            logger.info(f"Fetched yfinance data for {symbol}")
            return df
        except Exception as e:
            logger.error(f"yfinance error for {symbol}: {str(e)}")
            return None
        
    def fetch_news_sentiment(self, symbol):
        try:
            company_mapping = {
                'RELIANCE.NS': 'Reliance Industries',
                'HDFCBANK.NS': 'HDFC Bank',
                'INFY.NS': 'Infosys'
            }
            company = company_mapping.get(symbol, symbol.split('.')[0])
            articles = self.news_api.get_everything(
                q=f"{company} stock", 
                from_param=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                language='en',
                sort_by='relevancy',
                page_size=10  
            )
            sentiments = []
            for article in articles['articles']:
                text = article['title'] + ' ' + (article['description'] or '')
                sentiment = TextBlob(text).sentiment.polarity
                sentiments.append(sentiment)
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
            logger.info(f"Sentiment for {symbol} ({company}): {avg_sentiment:.3f} based on {len(sentiments)} articles")
            return avg_sentiment
        except Exception as e:
            logger.error(f"News API error for {symbol}: {str(e)}")
            return 0

    def fetch_stock_data(self):
        all_data = {}
        for symbol in self.stocks:
            df = self.fetch_alpha_vantage(symbol)
            if df is None:
                logger.warning(f"Falling back to yfinance for {symbol}")
                df = self.fetch_yfinance(symbol)
            if df is not None:
                all_data[symbol] = {
                    'price_data': df,
                    'sentiment': self.fetch_news_sentiment(symbol)
                }
            else:
                logger.error(f"Failed to fetch data for {symbol} from both sources")
            time.sleep(12)
        return all_data

if __name__ == '__main__':
    fetcher = DataFetcher()
    data = fetcher.fetch_stock_data()
    for symbol, stock_data in data.items():
        if stock_data is not None:
            df = stock_data['price_data']  
            sentiment = stock_data['sentiment']
            print(f"{symbol}:\n{df.tail()}\nSentiment: {sentiment:.3f}\n")