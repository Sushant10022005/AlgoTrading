def backtest(df):
    df = df.copy()
    df['next_close'] = df['close'].shift(-1)
    df['return'] = (df['next_close'] - df['close']) / df['close']
    df['strategy_return'] = df['return'] * df['signal']

    total_return = df['strategy_return'].sum()
    total_signals = df['signal'].sum()
    win_ratio = (df['strategy_return'] > 0).sum() / total_signals if total_signals > 0 else 0

    return total_return, win_ratio, df
