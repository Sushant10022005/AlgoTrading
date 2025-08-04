def apply_strategy(df):
    df = df.copy()
    df['signal'] = 0

    condition = (
        (df['rsi'] < 30) &
        (df['20dma'] > df['50dma']) &
        (df['20dma'].shift(1) <= df['50dma'].shift(1))
    )
    df.loc[condition, 'signal'] = 1
    return df
