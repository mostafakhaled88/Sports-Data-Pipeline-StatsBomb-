# ingestion/fetch_events.py

import csv
import requests
from datetime import datetime
import argparse

from config import BUCKET_NAME, EVENTS_ENDPOINT
from gcs_client import upload_json


def load_matches(csv_file):
    matches = []
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            matches.append({
                "competition_id": int(row["competition_id"]),
                "season_id": int(row["season_id"]),
                "match_id": int(row["match_id"])
            })
    return matches


def fetch_events(matches):
    ingestion_date = datetime.utcnow().strftime("%Y-%m-%d")

    for event_meta in matches:
        competition_id = event_meta["competition_id"]
        season_id = event_meta["season_id"]
        match_id = event_meta["match_id"]

        events_url = f"{EVENTS_ENDPOINT}/{match_id}.json"
        events_response = requests.get(events_url, timeout=30)

        if events_response.status_code != 200:
            print(f"Skipping events for match {match_id}")
            continue

        gcs_path = (
            f"events/"
            f"competition_id={competition_id}/"
            f"season_id={season_id}/"
            f"match_id={match_id}/"
            f"ingestion_date={ingestion_date}/"
            f"events.json"
        )

        upload_json(
            bucket_name=BUCKET_NAME,
            destination_path=gcs_path,
            data=events_response.content,
        )

        print(
            f"Uploaded events | "
            f"competition={competition_id} "
            f"season={season_id} "
            f"match={match_id}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--matches_csv",
        required=True,
        help="Path to CSV file containing competition_id, season_id, match_id"
    )
    args = parser.parse_args()

    matches = load_matches(args.matches_csv)
    fetch_events(matches)
