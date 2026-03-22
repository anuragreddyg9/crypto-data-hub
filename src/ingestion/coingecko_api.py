# uses CoinGecko public API (no key required)
import requests
import pandas as pd
from datetime import datetime
import time
import os

API_URL = "https://api.coingecko.com/api/v3/coins/markets"

PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1
}

DATA_FILE = "data/crypto_data.csv"

os.makedirs("data", exist_ok=True)


def fetch_snapshot():
    response = requests.get(API_URL, params=PARAMS)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data)[[
        "id",
        "symbol",
        "current_price",
        "market_cap",
        "total_volume"
    ]]

    df["timestamp"] = datetime.utcnow().isoformat()
    df["source"] = "coingecko"

    return df


def run_streamer():
    print("🚀 Starting market ingestion service...")

    while True:
        try:
            df = fetch_snapshot()

            print(df.head(3))

            df.to_csv(
                DATA_FILE,
                mode="a",
                header=not os.path.exists(DATA_FILE),
                index=False
            )

            print("✅ batch saved")

            time.sleep(8 + (datetime.utcnow().second % 4))

        except Exception as e:
            print("⚠️ error:", e)
            time.sleep(5)


if __name__ == "__main__":
    run_streamer()