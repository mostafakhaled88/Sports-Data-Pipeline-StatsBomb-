import json
from datetime import datetime
import apache_beam as beam
from dataflow.utils.safe_get import safe_get


class ParseStartingXIFn(beam.DoFn):
    def process(self, element, match_id):
        """
        element: full events JSON
        """

        ingestion_date = datetime.utcnow().date().isoformat()
        events = json.loads(element)

        for event in events:
            if safe_get(event, "type", "name") != "Starting XI":
                continue

            team = event.get("team", {})
            tactics = event.get("tactics", {})
            formation = tactics.get("formation")

            for player in tactics.get("lineup", []):
                yield {
                    "match_id": match_id,
                    "team_id": team.get("id"),
                    "team_name": team.get("name"),

                    "formation": formation,

                    "player_id": safe_get(player, "player", "id"),
                    "player_name": safe_get(player, "player", "name"),
                    "position_id": safe_get(player, "position", "id"),
                    "position_name": safe_get(player, "position", "name"),
                    "jersey_number": player.get("jersey_number"),

                    "ingestion_date": ingestion_date,
                }
