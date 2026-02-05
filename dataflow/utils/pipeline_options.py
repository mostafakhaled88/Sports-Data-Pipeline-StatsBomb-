# dataflow/utils/pipeline_options.py

from apache_beam.options.pipeline_options import PipelineOptions


def get_pipeline_options(
    runner: str,
    project: str,
    region: str,
    temp_location: str,
    staging_location: str,
):
    return PipelineOptions(
        temp_location="gs://statsbomb-temp/events_temp",
        runner=runner,
        project="football-analytics-project",
        region=region,
        temp_location=temp_location,
        staging_location=staging_location,
        save_main_session=True,
        setup_file="./setup.py"
    )
