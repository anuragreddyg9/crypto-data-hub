def add_features(df):
    df = df.sort_values("timestamp")

    df["price_to_volume"] = df["price"] / (df["volume"] + 1)

    df["ma"] = df.groupby("asset")["price"].transform(lambda x: x.rolling(5).mean())

    df["volatility"] = df.groupby("asset")["price"].transform(lambda x: x.rolling(5).std())

    df["trend"] = df.groupby("asset")["price"].transform(lambda x: x.diff())

    return df