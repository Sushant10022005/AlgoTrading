from datafetch import DataFetcher
from logger import SheetsLogger
from indicators import compute_indicators
from strategy import apply_strategy
from backtest_strategy import backtest
from ml_model import prepare_ml_data, train_and_evaluate


def main():
    fetcher = DataFetcher()
    data = fetcher.fetch_stock_data()

    summary_data = []
    ml_results = []

    for symbol, stock in data.items():
        df = stock['price_data'].copy()
        sentiment = stock['sentiment']

        df.columns = df.columns.str.lower()
        df = compute_indicators(df)
        df = apply_strategy(df)
        total_return, win_ratio, df = backtest(df)

        # ✅ Append only once
        summary_data.append([
            symbol,
            round(total_return * 100, 2),
            round(win_ratio * 100, 2),
            round(sentiment, 3)
        ])

        print(f"{symbol}: Return = {total_return:.2%}, Win Ratio = {win_ratio:.2%}")

        # ML
        try:
            X_train, X_test, y_train, y_test = prepare_ml_data(df, sentiment)
            acc, cm = train_and_evaluate(X_train, X_test, y_train, y_test)
            ml_results.append([
                symbol,
                round(acc * 100, 2),
                int(cm[0][0]), int(cm[0][1]),
                int(cm[1][0]), int(cm[1][1])
            ])
        except Exception as e:
            ml_results.append([symbol, 'Error', '-', '-', '-', '-'])
            print(f"ML Error for {symbol}: {str(e)}")

    sheet_logger = SheetsLogger()
    sheet_logger.log_stock_data(data)
    sheet_logger.log_summary(summary_data)
    sheet_logger.log_ml_results(ml_results)


if __name__ == '__main__':
    main()
