# ingestion/gcs_client.py

from google.cloud import storage


def upload_json(bucket_name: str, destination_path: str, data: bytes):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_path)

    blob.upload_from_string(
        data,
        content_type="application/json"
    )

    print(f"Uploaded to gs://{bucket_name}/{destination_path}")
