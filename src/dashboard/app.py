import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Crypto Data Hub", layout="wide")

FILE = "data/crypto_stream.csv"


def load_data():
    try:
        df = pd.read_csv(FILE)
        df.columns = [c.strip() for c in df.columns]

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce")

        df = df.dropna(subset=["timestamp", "price", "asset"])
        return df.sort_values("timestamp")

    except:
        return pd.DataFrame()


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

            col4.metric(
                "Avg Volatility",
                round(df["volatility"].mean(), 6) if "volatility" in df.columns else 0
            )

            st.subheader("Live Price Trend")

            chart = df.pivot_table(
                index="timestamp",
                columns="asset",
                values="price",
                aggfunc="mean"
            )

            st.line_chart(chart)

            st.subheader("Volume by Asset")

            if "volume" in df.columns:
                st.bar_chart(df.groupby("asset")["volume"].mean())

            st.subheader("Volatility by Asset")

            if "volatility" in df.columns:
                st.bar_chart(df.groupby("asset")["volatility"].mean())

    time.sleep(5)
    st.rerun()