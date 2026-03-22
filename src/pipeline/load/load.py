import psycopg2

DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "crypto_db",
    "user": "crypto_user",
    "password": "crypto_pass",
    "port": 5432
}

def save(df):
    if df is None or df.empty:
        return

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    rows = [
        (
            r["asset"],
            r["symbol"],
            r["price"],
            r["market_cap"],
            r["volume"],
            r["volatility"],
            r["ma"],
            r["trend"],
            r["timestamp"]
        )
        for _, r in df.iterrows()
    ]

    cur.executemany("""
        INSERT INTO crypto_prices (
            asset, symbol, price, market_cap, volume,
            volatility, moving_avg, trend, timestamp
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, rows)

    conn.commit()
    cur.close()
    conn.close()