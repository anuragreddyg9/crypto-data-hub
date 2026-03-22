import time
import pandas as pd

from extract.coingecko import fetch_data
from transform.transform import transform
from features.features import add_features
from load.load import save

BUFFER = []


def run():
    print("pipeline started")

while True:
    raw = fetch_data()
    print("RAW:", raw[:1])

    rows = transform(raw)
    print("ROWS:", rows[:1])

    BUFFER.extend(rows)

    df = pd.DataFrame(BUFFER)

    print("DF SHAPE:", df.shape)
    if not df.empty:
        df = add_features(df)
        save(df)

    time.sleep(20)

if __name__ == "__main__":
    run()