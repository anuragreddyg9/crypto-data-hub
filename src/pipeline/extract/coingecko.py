import requests

API_URL = "https://api.coingecko.com/api/v3/coins/markets"

PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1
}

def fetch_data():
    try:
        r = requests.get(API_URL, params=PARAMS, timeout=10)

        if r.status_code == 429:
            return []

        r.raise_for_status()
        return r.json()

    except:
        return []