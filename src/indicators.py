def compute_indicators(df):
    df = df.copy()

    # Ensure columns are lowercase for consistency
    df.columns = df.columns.str.lower()

    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))

    df['20dma'] = df['close'].rolling(window=20).mean()
    df['50dma'] = df['close'].rolling(window=50).mean()

    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26

    return df
