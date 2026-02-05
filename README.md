# ⚽ Sports Data Pipeline (StatsBomb)

An **end-to-end data engineering project** that ingests open football (soccer) data from **StatsBomb**, stores it in **Google Cloud Storage**, processes it using **Apache Beam / Dataflow**, and loads analytics-ready tables into **BigQuery**.

This project is designed to reflect **real-world, production-style data pipelines** with clear separation of concerns, fault tolerance, and scalability.

---

## 🚀 Project Goals

* Build a **cloud-native data pipeline** using GCP tools
* Apply **Bronze → Silver** data architecture principles
* Practice real-world ingestion, parsing, and error handling
* Create a **portfolio-grade project** suitable for data engineering roles

---

## 🧱 Architecture Overview

```
StatsBomb Open Data (GitHub)
            ↓
      Ingestion Layer
  (Python + Requests)
            ↓
 Google Cloud Storage (Raw / Bronze)
            ↓
 Apache Beam / Dataflow
 (Parsing, Validation, Enrichment)
            ↓
      BigQuery Tables
   (Analytics-Ready / Silver)
```

---

## 📁 Repository Structure

```
sports-data-pipeline/
├── ingestion/          # Raw data ingestion (Bronze layer)
├── dataflow/           # Apache Beam pipelines (Processing layer)
│   ├── pipelines/      # End-to-end Beam pipelines
│   ├── transforms/     # Parsing & transformation logic (DoFn)
│   ├── schemas/        # BigQuery table schemas
│   ├── utils/          # Shared utilities
│   └── __init__.py
├── data/               # Local helper data (CSVs, configs)
├── setup.py            # Beam dependency packaging
└── README.md           # Project documentation
```

---

## 🟤 Ingestion Layer (Bronze)

**Location:** `ingestion/`

Responsibilities:

* Fetch raw JSON data from StatsBomb Open Data endpoints
* Store data *unchanged* in Google Cloud Storage
* Apply partitioned directory structure
* Add ingestion-time metadata

Data fetched:

* Competitions
* Matches
* Match events

👉 See `ingestion/README.md` for details.

---

## ⚙️ Processing Layer (Apache Beam / Dataflow)

**Location:** `dataflow/`

Responsibilities:

* Read raw JSON files from GCS
* Parse and normalize nested JSON
* Enforce schemas
* Capture parsing & insertion errors
* Load clean data into BigQuery

Pipelines included:

* `competitions_pipeline.py`
* `matches_pipeline.py`
* `events_pipeline.py`

Advanced features:

* Multi-output `ParDo`
* Dead-letter tables
* BigQuery insert failure capture
* Beam Metrics for observability

👉 See `dataflow/README.md` and subfolder READMEs for details.

---

## 🧪 Data Quality & Reliability

This project follows **production-grade reliability patterns**:

* Raw data is never mutated
* Errors are routed to **dead-letter tables**, not dropped
* Pipelines are append-only and idempotent
* Explicit schemas prevent silent failures

---

## 📊 BigQuery Output Tables

Dataset: `statsbomb_raw`

Tables:

* `competitions`
* `matches`
* `events`
* `lineups`
* `events_deadletter`
* `bq_insert_errors`

Tables are designed for:

* Analytics
* Dashboarding
* Downstream feature engineering

---

## ▶️ How to Run

### 1️⃣ Ingest Raw Data

```bash
python ingestion/fetch_competitions.py
python ingestion/fetch_matches.py
python ingestion/fetch_events.py --matches_csv data/matches.csv
```

---

### 2️⃣ Run Pipelines Locally (DirectRunner)

```bash
python dataflow/pipelines/competitions_pipeline.py
python dataflow/pipelines/matches_pipeline.py
```

---

### 3️⃣ Run on Google Dataflow (Example)

```bash
python dataflow/pipelines/events_pipeline.py \
  --runner DataflowRunner \
  --project football-analytics-project \
  --region us-central1 \
  --temp_location gs://statsbomb-raw/temp \
  --staging_location gs://statsbomb-raw/staging \
  --input_path gs://statsbomb-raw/events/**/*.json \
  --output_table football-analytics-project:statsbomb_raw.events \
  --lineup_table football-analytics-project:statsbomb_raw.lineups \
  --deadletter_table football-analytics-project:statsbomb_raw.events_deadletter \
  --bq_errors_table football-analytics-project:statsbomb_raw.bq_insert_errors
```

---

## 🛠️ Tech Stack

* **Python 3**
* **Apache Beam**
* **Google Cloud Dataflow**
* **Google Cloud Storage**
* **BigQuery**
* **StatsBomb Open Data**

---

## 🎯 Skills Demonstrated

* Cloud data engineering (GCP)
* Batch data ingestion & processing
* Schema-first design
* Fault-tolerant pipelines
* Production-ready folder structure
* Sports analytics data modeling

---

## 🔮 Future Improvements

* Partitioned & clustered BigQuery tables
* Automated scheduling (Cloud Composer / Airflow)
* CI/CD for pipelines
* Unit & integration tests
* Gold-layer analytics marts

---

## 👤 Author

**Mostafa Khaled Farag**
Data Analyst / Aspiring Data Engineer
📍 Cairo, Egypt
📧 [mosta.mk@gmail.com](mailto:mosta.mk@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/mostafa-khaled-442b841b4/)
💻 [GitHub](https://github.com/mostafakhaled88)

---

⭐ If you found this project useful or inspiring, feel free to star the repo!
