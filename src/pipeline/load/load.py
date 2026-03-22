import os
import pandas as pd

COLUMNS = [
    "asset",
    "symbol",
    "price",
    "market_cap",
    "volume",
    "timestamp",
    "price_to_volume",
    "ma",
    "volatility",
    "trend"
]


def save(df, path="data/crypto_stream.csv"):
    os.makedirs("data", exist_ok=True)

    if df.empty:
        return

    for col in COLUMNS:
        if col not in df.columns:
            df[col] = None

    df = df[COLUMNS]

    df.to_csv(
        path,
        mode="a",
        header=not os.path.exists(path),
        index=False
    )