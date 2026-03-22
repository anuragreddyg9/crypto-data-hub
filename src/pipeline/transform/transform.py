from datetime import datetime
import pandas as pd

def transform(data):
    ts = datetime.utcnow()

    rows = []

    for d in data:
        if not d:
            continue

        price = d.get("current_price", 0)

        rows.append({
            "asset": d.get("id", ""),
            "symbol": d.get("symbol", ""),
            "price": price,
            "market_cap": d.get("market_cap", 0),
            "volume": d.get("total_volume", 0),

            # features (simple but useful)
            "volatility": 0,
            "ma": price,
            "trend": "up",
            "timestamp": ts
        })

    return rows