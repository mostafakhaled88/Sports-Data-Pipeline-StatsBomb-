# dataflow/pipelines/matches_pipeline.py

import apache_beam as beam
from apache_beam.io import fileio
from apache_beam.io.gcp.bigquery import WriteToBigQuery

from dataflow.schemas.matches_schema import MATCHES_SCHEMA
from dataflow.transforms.parse_matches import ParseMatchesFn
from dataflow.utils.pipeline_options import get_pipeline_options


INPUT_PATH = "gs://statsbomb-raw/matches/**/matches.json"
BQ_TABLE = "football-analytics-project:statsbomb_raw.matches"


def run():
    options = get_pipeline_options(
        runner="DirectRunner",
        project="football-analytics-project",
        region="us-central1",
        temp_location="gs://statsbomb-raw/temp",
        staging_location="gs://statsbomb-raw/staging",
    )

    with beam.Pipeline(options=options) as p:
        (
            p
            | "Match match files" >> fileio.MatchFiles(INPUT_PATH)
            | "Read match files" >> fileio.ReadMatches()
            | "Read content" >> beam.Map(lambda f: f.read_utf8())
            | "Parse matches" >> beam.ParDo(ParseMatchesFn())
            | "Write to BigQuery" >> WriteToBigQuery(
                table=BQ_TABLE,
                schema=MATCHES_SCHEMA,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )


if __name__ == "__main__":
    run()

