# Ingestion Layer

This folder contains the **raw data ingestion layer** of the Sports Data Pipeline. Its responsibility is to **fetch raw StatsBomb data from public endpoints and land it into Google Cloud Storage (GCS)** using a clean, partitioned directory structure.

This layer represents the **Bronze (raw) zone** of the data architecture.

---

## Responsibilities

* Fetch raw JSON data from StatsBomb Open Data endpoints
* Persist raw responses **unchanged** to GCS
* Apply a consistent, partitioned folder structure
* Add ingestion-time metadata

> ❗ No transformation, validation, or schema enforcement happens here

---

## Folder Structure

```
ingestion/
├── config.py
├── fetch_competitions.py
├── fetch_matches.py
├── fetch_events.py
├── gcs_client.py
```

---

## config.py

### Purpose

Central configuration file for ingestion jobs.

### Contains

* GCP project and bucket configuration
* Base StatsBomb endpoints
* Request timeout configuration

### Key Variables

* `PROJECT_ID`
* `BUCKET_NAME`
* `BASE_URL`
* `COMPETITIONS_ENDPOINT`
* `MATCHES_ENDPOINT`
* `EVENTS_ENDPOINT`

---

## gcs_client.py

### `upload_json(bucket_name, destination_path, data)`

#### Purpose

Lightweight wrapper around the Google Cloud Storage client to upload raw JSON bytes.

#### Key Features

* Uploads data **without modification**
* Explicit `application/json` content type
* Simple, reusable interface

---

## fetch_competitions.py

### Purpose

Fetches the global **competitions metadata** file from StatsBomb and stores it in GCS.

### Data Flow

1. Call StatsBomb competitions endpoint
2. Generate ingestion date (UTC)
3. Upload raw JSON to GCS

### GCS Layout

```
competitions/
└── ingestion_date=YYYY-MM-DD/
    └── competitions.json
```

---

## fetch_matches.py

### Purpose

Fetches **match metadata** for all available competitions and seasons.

### Data Flow

1. Fetch competitions list
2. Loop through `(competition_id, season_id)` pairs
3. Fetch matches JSON per competition-season
4. Upload raw responses to GCS

### GCS Layout

```
matches/
└── competition_id=XX/
    └── season_id=YY/
        └── ingestion_date=YYYY-MM-DD/
            └── matches.json
```

### Error Handling

* Non-200 responses are skipped
* Ingestion continues without failing the full job

---

## fetch_events.py

### Purpose

Fetches **event-level match data** (passes, shots, duels, etc.) for selected matches.

### Input

* CSV file containing:

  * `competition_id`
  * `season_id`
  * `match_id`

### Data Flow

1. Read match metadata from CSV
2. Fetch events JSON per match
3. Upload raw events to GCS

### GCS Layout

```
events/
└── competition_id=XX/
    └── season_id=YY/
        └── match_id=ZZZ/
            └── ingestion_date=YYYY-MM-DD/
                └── events.json
```

### Error Handling

* Skips matches with missing or unavailable event files
* Continues ingestion for remaining matches

---

## Design Principles

* **Raw-first ingestion**: data is stored exactly as received
* **Partitioned storage**: optimized for downstream processing
* **Idempotent by design**: re-runs create new ingestion partitions
* **Failure tolerant**: individual failures do not stop the pipeline

---

## How This Fits in the Architecture

```
StatsBomb API
     ↓
Ingestion (this layer)
     ↓
GCS Raw Zone (Bronze)
     ↓
Dataflow (Parsing & Validation)
     ↓
BigQuery (Analytics)
```

---

## How to Run

### Fetch Competitions

```bash
python ingestion/fetch_competitions.py
```

### Fetch Matches

```bash
python ingestion/fetch_matches.py
```

### Fetch Events

```bash
python ingestion/fetch_events.py \
  --matches_csv data/matches.csv
```

---

## Future Improvements

* Retry & backoff for HTTP requests
* Parallel downloads for large match sets
* Checkpointing for partial failures
* Structured logging

---

Part of the **Sports Data Pipeline** project.
