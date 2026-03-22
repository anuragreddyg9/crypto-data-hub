import streamlit as st
import pandas as pd
import psycopg2
import time

st.set_page_config(page_title="Crypto Data Hub", layout="wide")

DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "crypto_db",
    "user": "crypto_user",
    "password": "crypto_pass",
    "port": 5432
}

def load_data():
    conn = psycopg2.connect(**DB_CONFIG)

    df = pd.read_sql("""
        SELECT *
        FROM crypto_prices
        ORDER BY timestamp DESC
        LIMIT 1000
    """, conn)

    conn.close()
    return df


st.title("Crypto Data Hub - Real Time Analytics")

placeholder = st.empty()

while True:

    df = load_data()

    with placeholder.container():

        if df.empty:
            st.warning("Waiting for streaming data...")

        else:
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Assets", df["asset"].nunique())
            col2.metric("Rows", len(df))
            col3.metric("Avg Price", round(df["price"].mean(), 2))
            col4.metric("Avg Volatility", round(df["volatility"].mean(), 6))

            st.subheader("Live Price Trend")

            chart = df.pivot_table(
                index="timestamp",
                columns="asset",
                values="price",
                aggfunc="mean"
            )

            st.line_chart(chart)

            st.subheader("Volume by Asset")
            st.bar_chart(df.groupby("asset")["volume"].mean())

            st.subheader("Volatility by Asset")
            st.bar_chart(df.groupby("asset")["volatility"].mean())

    time.sleep(5)