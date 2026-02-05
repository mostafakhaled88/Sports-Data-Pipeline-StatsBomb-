# dataflow/pipelines/competitions_pipeline.py

import apache_beam as beam
from apache_beam.io import fileio
from apache_beam.io.gcp.bigquery import WriteToBigQuery

from dataflow.schemas.competitions_schema import COMPETITIONS_SCHEMA
from dataflow.transforms.parse_competitions import ParseCompetitionsFn
from dataflow.utils.pipeline_options import get_pipeline_options


INPUT_PATH = "gs://statsbomb-raw/competitions/*/competitions.json"
BQ_TABLE = "football-analytics-project:statsbomb_raw.competitions"


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
            | "Match files" >> fileio.MatchFiles(INPUT_PATH)
            | "Read files" >> fileio.ReadMatches()
            | "Read file content" >> beam.Map(lambda f: f.read_utf8())
            | "Parse competitions JSON" >> beam.ParDo(ParseCompetitionsFn())
            | "Write to BigQuery" >> WriteToBigQuery(
                table=BQ_TABLE,
                schema=COMPETITIONS_SCHEMA,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )


if __name__ == "__main__":
    run()
