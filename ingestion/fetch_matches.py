# ingestion/fetch_matches.py

import json
import requests
from datetime import datetime

from config import (
    BUCKET_NAME,
    COMPETITIONS_ENDPOINT,
    MATCHES_ENDPOINT
)
from gcs_client import upload_json


def fetch_competitions():
    response = requests.get(COMPETITIONS_ENDPOINT, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_matches():
    competitions = fetch_competitions()
    ingestion_date = datetime.utcnow().strftime("%Y-%m-%d")

    for comp in competitions:
        competition_id = comp["competition_id"]
        season_id = comp["season_id"]

        url = f"{MATCHES_ENDPOINT}/{competition_id}/{season_id}.json"

        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            print(f"Skipping {competition_id}-{season_id}")
            continue

        gcs_path = (
            f"matches/"
            f"competition_id={competition_id}/"
            f"season_id={season_id}/"
            f"ingestion_date={ingestion_date}/"
            f"matches.json"
        )

        upload_json(
            bucket_name=BUCKET_NAME,
            destination_path=gcs_path,
            data=response.content
        )


if __name__ == "__main__":
    fetch_matches()
