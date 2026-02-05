# ingestion/fetch_competitions.py

import requests
from datetime import datetime

from config import (
    BUCKET_NAME,
    COMPETITIONS_ENDPOINT
)
from gcs_client import upload_json


def fetch_competitions():
    response = requests.get(COMPETITIONS_ENDPOINT, timeout=30)
    response.raise_for_status()

    ingestion_date = datetime.utcnow().strftime("%Y-%m-%d")

    gcs_path = (
        f"competitions/"
        f"ingestion_date={ingestion_date}/"
        f"competitions.json"
    )

    upload_json(
        bucket_name=BUCKET_NAME,
        destination_path=gcs_path,
        data=response.content
    )


if __name__ == "__main__":
    fetch_competitions()
