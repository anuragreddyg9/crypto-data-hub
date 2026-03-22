from datetime import datetime

def transform(data):
    ts = datetime.utcnow()

    return [
        {
            "asset": d.get("id"),
            "symbol": d.get("symbol"),
            "price": d.get("current_price"),
            "market_cap": d.get("market_cap"),
            "volume": d.get("total_volume"),
            "timestamp": ts
        }
        for d in data
    ]