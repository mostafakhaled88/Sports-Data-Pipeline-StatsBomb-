# ingestion/config.py

PROJECT_ID = "football-analytics-project"
BUCKET_NAME = "statsbomb-raw"

BASE_URL = (
    "https://raw.githubusercontent.com/"
    "statsbomb/open-data/master/data"
)

COMPETITIONS_ENDPOINT = f"{BASE_URL}/competitions.json"
EVENTS_ENDPOINT = (
    "https://raw.githubusercontent.com/"
    "statsbomb/open-data/master/data/events"
)

MATCHES_ENDPOINT = f"{BASE_URL}/matches"

TIMEOUT = 30
