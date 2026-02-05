# dataflow/transforms/parse_competitions.py

import json
from datetime import datetime
import apache_beam as beam


class ParseCompetitionsFn(beam.DoFn):
    def process(self, element):
        """
        element: full JSON file content as a string
        """

        ingestion_date = datetime.utcnow().date().isoformat()

        records = json.loads(element)  # THIS is now a list

        for record in records:
            yield {
                "competition_id": record.get("competition_id"),
                "season_id": record.get("season_id"),
                "competition_name": record.get("competition_name"),
                "country_name": record.get("country_name"),
                "season_name": record.get("season_name"),
                "competition_gender": record.get("competition_gender"),
                "competition_youth": record.get("competition_youth"),
                "competition_international": record.get("competition_international"),
                "ingestion_date": ingestion_date,
            }
