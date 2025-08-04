import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

def prepare_ml_data(df, sentiment):
    df = df.copy()
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)

    df = df.dropna(subset=['rsi', 'macd', 'volume', 'target'])
    df['sentiment'] = sentiment  # Add as constant feature for each row

    X = df[['rsi', 'macd', 'volume', 'sentiment']]
    y = df['target']
    return train_test_split(X, y, test_size=0.2, shuffle=False)

def train_and_evaluate(X_train, X_test, y_train, y_test):
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    acc = accuracy_score(y_test, predictions)
    cm = confusion_matrix(y_test, predictions)
    return acc, cm
