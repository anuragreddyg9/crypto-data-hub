import time
import pandas as pd

from extract.coingecko import fetch_data
from transform.transform import transform
from load.load import save

BUFFER = []
MAX_BUFFER = 200

def run():
    print("🚀 pipeline started")

    while True:
        raw = fetch_data()
        rows = transform(raw)

        BUFFER.extend(rows)

        if len(BUFFER) > MAX_BUFFER:
            BUFFER[:] = BUFFER[-MAX_BUFFER:]

        df = pd.DataFrame(BUFFER)

        if not df.empty:
            save(df)

        time.sleep(15)


if __name__ == "__main__":
    run()