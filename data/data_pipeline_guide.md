# Data Pipeline Design — Complete Guide

> **A comprehensive reference for Data Engineers covering design, implementation, and production patterns using Python, Airflow, Pandas, PySpark, Kafka, and more.**

---

## Table of Contents

1. [Fundamentals](#1-fundamentals)
2. [Pipeline Types](#2-pipeline-types)
3. [Ingestion Layer Design](#3-ingestion-layer-design)
4. [Processing Layer Design](#4-processing-layer-design)
5. [Storage Layer Design](#5-storage-layer-design)
6. [Batch Pipeline Design](#6-batch-pipeline-design)
7. [Streaming Pipeline Design](#7-streaming-pipeline-design)
8. [CDC Pipeline Design](#8-cdc-pipeline-design)
9. [Orchestration Design](#9-orchestration-design)
10. [Data Quality in Pipelines](#10-data-quality-in-pipelines)
11. [Pipeline Observability](#11-pipeline-observability)
12. [Performance & Optimization](#12-performance--optimization)
13. [Security in Pipelines](#13-security-in-pipelines)
14. [Pipeline Design Patterns](#14-pipeline-design-patterns)
15. [Classic Pipeline Design Problems](#15-classic-pipeline-design-problems)

---

# 1. Fundamentals

## What is a Data Pipeline?

A **data pipeline** is a series of automated steps that move and transform data from one or more sources to one or more destinations. It abstracts the complexity of data movement, transformation, and delivery into a repeatable, observable process.

```
Raw Source → Ingest → Process → Store → Serve
```

**Key characteristics:**

- Automated and repeatable
- Handles failures gracefully
- Observable and monitorable
- Scalable to data volume changes

---

## Pipeline Components

### Source

The origin of your data: databases (MySQL, PostgreSQL), APIs (REST, GraphQL), files (CSV, JSON, Parquet), event streams (Kafka, Kinesis), SaaS apps (Salesforce, Stripe).

### Ingest

The mechanism that pulls or receives data from sources:

```python
# Example: Simple Python ingestion from a REST API
import requests
import json
from datetime import datetime

def ingest_api_data(endpoint: str, api_key: str, since: datetime) -> list[dict]:
    """Pull incremental data from a REST API."""
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"updated_since": since.isoformat(), "limit": 1000}
    
    all_records = []
    page = 1
    while True:
        params["page"] = page
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        records = data.get("records", [])
        if not records:
            break
        all_records.extend(records)
        page += 1
        
        if not data.get("has_more", False):
            break
    
    return all_records
```

### Process

Transformation logic: cleaning, filtering, joining, aggregating, enriching.

```python
import pandas as pd

def process_orders(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich raw order data."""
    df = raw_df.copy()
    
    # Clean
    df = df.dropna(subset=["order_id", "customer_id"])
    df["order_id"] = df["order_id"].astype(str).str.strip()
    
    # Enrich
    df["order_date"] = pd.to_datetime(df["created_at"])
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["total_with_tax"] = df["total_amount"] * 1.18
    
    # Deduplicate
    df = df.drop_duplicates(subset=["order_id"], keep="last")
    
    return df
```

### Store

Persist processed data: data warehouses (Redshift, BigQuery, Snowflake), data lakes (S3, GCS, ADLS), operational databases.

### Serve

Make data available to consumers: BI dashboards, ML features, APIs, downstream pipelines.

---

## Pipeline Design Principles

### 1. Idempotency

**Definition:** Running a pipeline multiple times with the same input produces the same output with no side effects.

**Why it matters:** Pipelines fail. When you re-run a failed job, you must not duplicate data or create inconsistencies.

```python
# BAD: Not idempotent — appends every time
def load_bad(df: pd.DataFrame, table: str, conn):
    df.to_sql(table, conn, if_exists="append")  # duplicates on re-run

# GOOD: Idempotent — delete partition then insert
def load_idempotent(df: pd.DataFrame, table: str, partition_date: str, conn):
    """Delete existing data for partition, then insert fresh."""
    with conn.begin():
        conn.execute(
            f"DELETE FROM {table} WHERE partition_date = :dt",
            {"dt": partition_date}
        )
        df["partition_date"] = partition_date
        df.to_sql(table, conn, if_exists="append", index=False)
```

```python
# PySpark idempotent write using overwrite mode with partition
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("IdempotentLoad").getOrCreate()

def idempotent_spark_write(df, output_path: str, partition_col: str, partition_value: str):
    """Overwrite only the specific partition — safe to re-run."""
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    
    df_with_partition = df.withColumn(partition_col, F.lit(partition_value))
    
    (df_with_partition
        .write
        .mode("overwrite")
        .partitionBy(partition_col)
        .parquet(output_path))
```

### 2. Replayability

**Definition:** The ability to re-process historical data from the source, producing the same results as the original run.

**Requirements for replayability:**

- Raw data is retained in immutable storage (data lake bronze layer)
- Transformations are deterministic (no `NOW()`, `RANDOM()` without seeding)
- Processing logic is versioned

```python
# Design for replayability: store raw data with ingestion metadata
import boto3
from datetime import datetime
import json

def ingest_with_replay_support(records: list[dict], source: str, s3_bucket: str):
    """Store raw data in S3 partitioned by ingestion date for future replay."""
    s3 = boto3.client("s3")
    
    ingestion_ts = datetime.utcnow()
    
    # Envelope each record with metadata
    enveloped = [
        {
            "_source": source,
            "_ingested_at": ingestion_ts.isoformat(),
            "_pipeline_version": "v1.2.3",
            "data": record
        }
        for record in records
    ]
    
    # Write to S3 partitioned path for time-travel replay
    s3_key = (
        f"raw/{source}/"
        f"year={ingestion_ts.year}/"
        f"month={ingestion_ts.month:02d}/"
        f"day={ingestion_ts.day:02d}/"
        f"hour={ingestion_ts.hour:02d}/"
        f"{ingestion_ts.timestamp()}.jsonl"
    )
    
    payload = "\n".join(json.dumps(r) for r in enveloped)
    s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=payload)
    
    return s3_key
```

### 3. Backfilling

**Definition:** Re-processing historical time periods, typically when pipeline logic changes or data was missed.

```python
# Airflow backfill example using execution_date
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def process_partition(execution_date, **kwargs):
    """Process data for a specific date partition."""
    date_str = execution_date.strftime("%Y-%m-%d")
    print(f"Processing partition for date: {date_str}")
    # ... actual processing logic using date_str

with DAG(
    "backfillable_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=True,          # enables automatic backfill
    max_active_runs=3,     # limit concurrency during backfill
) as dag:
    process = PythonOperator(
        task_id="process_partition",
        python_callable=process_partition,
        provide_context=True,
    )
```

```bash
# Trigger backfill via CLI
airflow dags backfill \
    --start-date 2024-01-01 \
    --end-date 2024-03-31 \
    backfillable_pipeline
```

### 4. Fault Tolerance

**Definition:** The pipeline continues operating (or recovers gracefully) when components fail.

```python
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def retry(max_attempts: int = 3, backoff_seconds: float = 2.0, exceptions=(Exception,)):
    """Decorator for retrying functions with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        logger.error(f"{func.__name__} failed after {max_attempts} attempts: {e}")
                        raise
                    wait = backoff_seconds ** attempt
                    logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {wait}s...")
                    time.sleep(wait)
        return wrapper
    return decorator

@retry(max_attempts=3, exceptions=(requests.HTTPError, ConnectionError))
def fetch_with_retry(url: str) -> dict:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()
```

### 5. Pipeline SLA & Monitoring

**SLA (Service Level Agreement):** A commitment on pipeline freshness, completeness, or latency.

```python
# Airflow SLA miss callback
from airflow import DAG
from datetime import datetime, timedelta
import smtplib

def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    """Called when a task misses its SLA."""
    message = f"SLA MISS: DAG {dag.dag_id} — tasks: {task_list}"
    print(f"[ALERT] {message}")
    # Integrate with PagerDuty, Slack, or email here

with DAG(
    "monitored_pipeline",
    default_args={
        "sla": timedelta(hours=2),  # each task must finish within 2 hours
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    sla_miss_callback=sla_miss_callback,
    schedule_interval="0 6 * * *",
    start_date=datetime(2024, 1, 1),
) as dag:
    pass
```

---

# 2. Pipeline Types

## Batch Pipeline

Processes data in discrete chunks at scheduled intervals. Best for:

- Non-time-critical workloads
- Complex transformations on large datasets
- Reporting and analytics

```
Schedule → Extract Chunk → Transform → Load → Done
```

**Characteristics:** High throughput, higher latency (minutes to hours), simpler error handling.

```python
# Simple batch pipeline with Pandas
import pandas as pd
from sqlalchemy import create_engine
from datetime import date, timedelta

def run_daily_batch(run_date: date):
    """Batch pipeline: extract previous day's orders, transform, and load to DW."""
    engine_src = create_engine("postgresql://user:pass@source_db/app")
    engine_dst = create_engine("postgresql://user:pass@warehouse/dw")
    
    # Extract
    query = f"""
        SELECT order_id, customer_id, total_amount, created_at, status
        FROM orders
        WHERE DATE(created_at) = '{run_date}'
    """
    df = pd.read_sql(query, engine_src)
    print(f"Extracted {len(df)} rows for {run_date}")
    
    # Transform
    df["run_date"] = run_date.isoformat()
    df["revenue_bucket"] = pd.cut(
        df["total_amount"],
        bins=[0, 50, 200, 1000, float("inf")],
        labels=["low", "medium", "high", "enterprise"]
    )
    
    # Load (idempotent)
    with engine_dst.begin() as conn:
        conn.execute(f"DELETE FROM orders_daily WHERE run_date = '{run_date}'")
    df.to_sql("orders_daily", engine_dst, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows to warehouse")
```

---

## Streaming Pipeline

Processes events continuously as they arrive. Best for:

- Real-time dashboards and alerts
- Fraud detection
- Recommendation engines
- IoT sensor data

```
Event → Message Broker → Stream Processor → Sink
```

**Characteristics:** Low latency (milliseconds to seconds), continuous processing, stateful operations.

```python
# Kafka consumer as a streaming pipeline
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "orders-topic",
    bootstrap_servers=["kafka:9092"],
    auto_offset_reset="earliest",
    group_id="orders-processor",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

def process_event(event: dict) -> dict:
    """Process a single order event in real-time."""
    return {
        "order_id": event["order_id"],
        "customer_id": event["customer_id"],
        "processed_at": datetime.utcnow().isoformat(),
        "total_with_tax": event["total_amount"] * 1.18,
    }

for message in consumer:
    event = message.value
    processed = process_event(event)
    # Write to sink (Redis, Cassandra, Kafka output topic, etc.)
    print(f"Processed event: {processed}")
```

---

## Micro-batch Pipeline

Processes small batches at very short intervals (seconds to minutes). Bridges batch and streaming.

**Example:** Spark Structured Streaming with trigger interval.

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StringType, DoubleType, LongType

spark = SparkSession.builder \
    .appName("MicroBatchPipeline") \
    .getOrCreate()

schema = StructType() \
    .add("order_id", StringType()) \
    .add("amount", DoubleType()) \
    .add("customer_id", StringType()) \
    .add("event_time", LongType())

# Read from Kafka
df_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "orders") \
    .load()

df_parsed = df_stream.select(
    F.from_json(F.col("value").cast("string"), schema).alias("data")
).select("data.*")

# Micro-batch: process every 30 seconds
query = df_parsed.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "s3://bucket/orders/") \
    .option("checkpointLocation", "s3://bucket/checkpoints/orders/") \
    .trigger(processingTime="30 seconds") \
    .start()

query.awaitTermination()
```

---

## Hybrid Pipeline (Lambda Architecture)

Combines batch and streaming layers to balance latency and accuracy.

```
                    ┌──────────────────────────────────┐
                    │          Serving Layer            │
                    └────────────┬─────────────┬────────┘
                                 │             │
              ┌──────────────────┴──┐  ┌───────┴──────────────┐
              │    Batch Layer      │  │    Speed Layer        │
              │ (accurate, slow)    │  │ (approximate, fast)   │
              │ Spark/Airflow daily │  │ Kafka/Flink real-time │
              └──────────┬──────────┘  └─────────┬────────────┘
                         │                       │
                    ┌────┴───────────────────────┴────┐
                    │         Data Sources            │
                    └─────────────────────────────────┘
```

**Use case:** Financial reporting where you need real-time approximate metrics AND accurate end-of-day numbers.

---

## ETL vs ELT

| Aspect | ETL | ELT |
|--------|-----|-----|
| Transform location | Staging/middleware | Inside the warehouse |
| Best for | Sensitive data, complex logic | Cloud DW (BigQuery, Snowflake) |
| Tools | Spark, Python, Glue | dbt, Snowflake SQL, BigQuery |
| Cost | Processing outside DW | Leverages DW compute |

```python
# ETL: Transform before loading
def etl_pipeline(source_conn, dw_conn):
    # Extract
    df = pd.read_sql("SELECT * FROM raw_events", source_conn)
    
    # Transform (outside DW)
    df = df.dropna(subset=["event_id"])
    df["event_date"] = pd.to_datetime(df["timestamp"]).dt.date
    df = df.groupby(["event_date", "event_type"]).size().reset_index(name="count")
    
    # Load (already transformed)
    df.to_sql("events_daily", dw_conn, if_exists="replace", index=False)

# ELT: Load raw, transform inside DW with dbt/SQL
def elt_pipeline(source_conn, dw_conn):
    # Extract & Load (raw, minimal transformation)
    df = pd.read_sql("SELECT * FROM raw_events", source_conn)
    df.to_sql("raw_events", dw_conn, if_exists="replace", index=False)
    
    # Transform inside DW (via dbt or SQL)
    dw_conn.execute("""
        CREATE OR REPLACE TABLE events_daily AS
        SELECT
            DATE(timestamp) AS event_date,
            event_type,
            COUNT(*) AS count
        FROM raw_events
        WHERE event_id IS NOT NULL
        GROUP BY 1, 2
    """)
```

---

## Reverse ETL

Syncs data **from** your data warehouse **back to** operational systems (CRMs, ad platforms, email tools).

```python
# Reverse ETL: Sync customer segments from DW to Salesforce
import requests

def reverse_etl_to_salesforce(dw_conn, sf_access_token: str):
    """Sync high-value customer segment from DW to Salesforce."""
    
    # Query DW for segment
    df = pd.read_sql("""
        SELECT customer_id, email, ltv_score, segment
        FROM customer_segments
        WHERE segment = 'high_value' AND updated_at >= CURRENT_DATE - 1
    """, dw_conn)
    
    sf_base = "https://your-instance.salesforce.com/services/data/v57.0"
    headers = {
        "Authorization": f"Bearer {sf_access_token}",
        "Content-Type": "application/json"
    }
    
    # Upsert records to Salesforce
    for _, row in df.iterrows():
        payload = {
            "LTV_Score__c": row["ltv_score"],
            "Segment__c": row["segment"],
        }
        sf_id = row["customer_id"]
        requests.patch(
            f"{sf_base}/sobjects/Contact/{sf_id}",
            json=payload, headers=headers
        )
    
    print(f"Synced {len(df)} records to Salesforce")
```

---

# 3. Ingestion Layer Design

## Full Load vs Incremental Load

### Full Load

Re-ingest the entire source dataset every run. Simple but expensive at scale.

```python
def full_load(source_conn, target_conn, table: str):
    """Truncate-and-reload pattern."""
    df = pd.read_sql(f"SELECT * FROM {table}", source_conn)
    with target_conn.begin() as conn:
        conn.execute(f"TRUNCATE TABLE {table}_snapshot")
    df.to_sql(f"{table}_snapshot", target_conn, if_exists="append", index=False)
    print(f"Full load complete: {len(df)} rows")
```

### Incremental Load

Only fetch new/changed records since the last run.

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

WATERMARK_FILE = Path("/tmp/pipeline_watermarks.json")

def get_watermark(source: str) -> datetime:
    """Load the last successful ingestion timestamp."""
    if WATERMARK_FILE.exists():
        watermarks = json.loads(WATERMARK_FILE.read_text())
        ts_str = watermarks.get(source)
        if ts_str:
            return datetime.fromisoformat(ts_str)
    return datetime(2020, 1, 1)  # default start

def save_watermark(source: str, ts: datetime):
    """Persist watermark after successful run."""
    watermarks = {}
    if WATERMARK_FILE.exists():
        watermarks = json.loads(WATERMARK_FILE.read_text())
    watermarks[source] = ts.isoformat()
    WATERMARK_FILE.write_text(json.dumps(watermarks))

def incremental_load(source_conn, target_conn, table: str):
    """Load only records updated since last watermark."""
    last_run = get_watermark(table)
    run_start = datetime.utcnow()
    
    query = f"""
        SELECT * FROM {table}
        WHERE updated_at > '{last_run.isoformat()}'
        ORDER BY updated_at ASC
    """
    df = pd.read_sql(query, source_conn)
    
    if df.empty:
        print(f"No new records for {table} since {last_run}")
        return
    
    # Upsert to target
    # (actual upsert logic depends on target DB)
    df.to_sql(f"{table}_incremental", target_conn, if_exists="append", index=False)
    save_watermark(table, run_start)
    print(f"Loaded {len(df)} new records")
```

---

## Change Data Capture (CDC)

CDC captures every row-level INSERT, UPDATE, DELETE from a source database with minimal overhead.

**Two main approaches:**

- **Log-based CDC:** Reads the database binary/write-ahead log (Debezium, AWS DMS). Low latency, no source queries.
- **Query-based CDC:** Polls source with `WHERE updated_at > last_run`. Higher source load, misses hard deletes.

```python
# Simulating CDC event consumption from Kafka (produced by Debezium)
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "dbserver1.inventory.orders",  # Debezium topic: server.db.table
    bootstrap_servers=["kafka:9092"],
    group_id="cdc-consumer",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

def handle_cdc_event(event: dict):
    op = event.get("op")       # 'c'=create, 'u'=update, 'd'=delete, 'r'=snapshot
    before = event.get("before")
    after = event.get("after")
    
    if op == "c":
        print(f"INSERT: {after}")
        # upsert_to_warehouse(after)
    elif op == "u":
        print(f"UPDATE: {before} → {after}")
        # upsert_to_warehouse(after)
    elif op == "d":
        print(f"DELETE: {before}")
        # soft_delete_in_warehouse(before["id"])
    elif op == "r":
        print(f"SNAPSHOT: {after}")
        # bulk_load_to_warehouse(after)

for message in consumer:
    handle_cdc_event(message.value)
```

---

## API-based Ingestion

```python
import requests
import time
from typing import Generator

def paginated_api_ingest(
    base_url: str,
    headers: dict,
    params: dict,
    page_size: int = 100
) -> Generator[list, None, None]:
    """Generator-based paginated API ingestion with rate limiting."""
    cursor = None
    
    while True:
        if cursor:
            params["cursor"] = cursor
        params["limit"] = page_size
        
        response = requests.get(base_url, headers=headers, params=params)
        
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            print(f"Rate limited. Waiting {retry_after}s...")
            time.sleep(retry_after)
            continue
        
        response.raise_for_status()
        data = response.json()
        
        records = data.get("data", [])
        if not records:
            break
        
        yield records
        
        cursor = data.get("next_cursor")
        if not cursor:
            break
        
        time.sleep(0.1)  # polite rate limiting

# Usage
all_data = []
for page in paginated_api_ingest(
    "https://api.example.com/orders",
    headers={"Authorization": "Bearer TOKEN"},
    params={"status": "completed"}
):
    all_data.extend(page)

df = pd.DataFrame(all_data)
```

---

## File-based Ingestion

```python
import boto3
import pandas as pd
from io import BytesIO
from pathlib import Path

def ingest_from_s3(bucket: str, prefix: str, file_pattern: str = "*.parquet") -> pd.DataFrame:
    """Ingest all matching files from S3 prefix into a single DataFrame."""
    s3 = boto3.client("s3")
    
    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
    
    dfs = []
    for page in pages:
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if not key.endswith(".parquet"):
                continue
            
            print(f"Reading: s3://{bucket}/{key}")
            response = s3.get_object(Bucket=bucket, Key=key)
            df = pd.read_parquet(BytesIO(response["Body"].read()))
            df["_source_file"] = key
            dfs.append(df)
    
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

# PySpark version for large-scale file ingestion
def spark_ingest_s3(spark, bucket: str, prefix: str) -> "DataFrame":
    """PySpark: read all parquet files from S3 prefix with schema inference."""
    path = f"s3://{bucket}/{prefix}/*.parquet"
    return spark.read \
        .option("mergeSchema", "true") \
        .parquet(path)
```

---

## Event-based Ingestion

```python
# Kafka producer: push events as they happen
from kafka import KafkaProducer
import json
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    acks="all",          # wait for all replicas to acknowledge
    retries=5,
    compression_type="gzip"
)

def emit_order_event(order: dict):
    """Emit an order event to Kafka."""
    event = {
        **order,
        "_event_time": datetime.utcnow().isoformat(),
        "_event_type": "order_created"
    }
    future = producer.send("orders-topic", value=event, key=str(order["order_id"]).encode())
    result = future.get(timeout=10)  # block to confirm delivery
    print(f"Emitted to partition {result.partition} offset {result.offset}")
```

---

## Push vs Pull Ingestion

| | Push | Pull |
|--|------|------|
| **How** | Source sends data to pipeline | Pipeline queries source |
| **Latency** | Lower (event-driven) | Higher (polling interval) |
| **Source load** | Minimal | Can be significant |
| **Examples** | Webhooks, Kafka, Kinesis | REST API polling, DB queries |
| **Failure risk** | Data lost if receiver down | Can replay by adjusting watermark |

```python
# Push: webhook receiver (Flask)
from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)
producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda v: json.dumps(v).encode()
)

@app.route("/webhook/orders", methods=["POST"])
def receive_order_webhook():
    """Receive pushed order events and forward to Kafka."""
    payload = request.get_json()
    
    # Validate signature (HMAC check)
    sig = request.headers.get("X-Signature")
    if not validate_signature(payload, sig):
        return jsonify({"error": "Invalid signature"}), 401
    
    producer.send("orders-topic", value=payload)
    return jsonify({"status": "accepted"}), 200
```

---

# 4. Processing Layer Design

## Stateless vs Stateful Processing

**Stateless:** Each record/event is processed independently with no memory of previous records.

```python
# Stateless transformation: enrich each record independently
def stateless_transform(record: dict) -> dict:
    """No state needed — each record is self-contained."""
    return {
        "order_id": record["order_id"],
        "total_with_tax": record["amount"] * 1.18,
        "is_large_order": record["amount"] > 1000,
        "processed_at": datetime.utcnow().isoformat()
    }
```

**Stateful:** Processing requires knowledge of previous events (running totals, session detection, deduplication).

```python
# Stateful: running sum per customer using PySpark
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def stateful_running_total(df):
    """Compute running order total per customer — requires state across rows."""
    window = Window.partitionBy("customer_id").orderBy("order_date").rowsBetween(
        Window.unboundedPreceding, Window.currentRow
    )
    return df.withColumn("running_total", F.sum("amount").over(window))
```

```python
# Stateful streaming with PySpark Structured Streaming
from pyspark.sql.streaming.state import GroupState, GroupStateTimeout
from pyspark.sql.functions import struct

def update_session_state(key, values, state: GroupState):
    """Stateful session aggregation per user."""
    if state.hasTimedOut:
        # Emit final session on timeout
        yield state.get
        state.remove()
        return
    
    current = state.getOption or {"count": 0, "total": 0.0}
    for row in values:
        current["count"] += 1
        current["total"] += row.amount
    
    state.update(current)
    state.setTimeoutDuration("10 minutes")
```

---

## Transformation Patterns

```python
import pandas as pd
import numpy as np

def apply_transformations(df: pd.DataFrame) -> pd.DataFrame:
    """Common transformation patterns."""
    
    # 1. Type casting
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    
    # 2. Normalization / Standardization
    df["amount_normalized"] = (df["amount"] - df["amount"].mean()) / df["amount"].std()
    
    # 3. Derived columns
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["days_since_epoch"] = (df["order_date"] - pd.Timestamp("1970-01-01")).dt.days
    
    # 4. Conditional logic
    df["size_category"] = np.select(
        [df["amount"] < 50, df["amount"] < 500, df["amount"] >= 500],
        ["small", "medium", "large"],
        default="unknown"
    )
    
    # 5. String cleaning
    df["customer_email"] = df["customer_email"].str.lower().str.strip()
    
    # 6. Flattening nested JSON
    if "metadata" in df.columns:
        meta_df = pd.json_normalize(df["metadata"].dropna())
        df = df.drop("metadata", axis=1).join(meta_df, how="left")
    
    return df
```

```python
# PySpark transformations
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

def spark_transformations(df):
    return (df
        # Type cast
        .withColumn("amount", F.col("amount").cast(DoubleType()))
        # Derived columns
        .withColumn("year_month", F.date_format("order_date", "yyyy-MM"))
        # Conditional
        .withColumn("size_category",
            F.when(F.col("amount") < 50, "small")
             .when(F.col("amount") < 500, "medium")
             .otherwise("large"))
        # Null handling
        .fillna({"amount": 0.0, "status": "unknown"})
        # String normalization
        .withColumn("email", F.lower(F.trim(F.col("customer_email"))))
    )
```

---

## Aggregation & Enrichment

```python
# Pandas aggregation
def aggregate_daily_metrics(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate orders to daily metrics per customer."""
    return (orders_df
        .groupby(["customer_id", "order_date"])
        .agg(
            order_count=("order_id", "count"),
            total_revenue=("amount", "sum"),
            avg_order_value=("amount", "mean"),
            distinct_products=("product_id", "nunique"),
            max_order=("amount", "max")
        )
        .reset_index()
    )

# Enrichment: join with a reference table
def enrich_with_customer_segment(orders_df: pd.DataFrame, customers_df: pd.DataFrame) -> pd.DataFrame:
    """Enrich orders with customer segment from a lookup table."""
    return orders_df.merge(
        customers_df[["customer_id", "segment", "region"]],
        on="customer_id",
        how="left"
    )
```

```python
# PySpark aggregation
from pyspark.sql import functions as F

def spark_daily_aggregation(orders_df):
    return (orders_df
        .groupBy("customer_id", F.to_date("order_timestamp").alias("order_date"))
        .agg(
            F.count("order_id").alias("order_count"),
            F.sum("amount").alias("total_revenue"),
            F.avg("amount").alias("avg_order_value"),
            F.countDistinct("product_id").alias("distinct_products")
        )
    )
```

---

## Joins in Pipelines

### Stream-Stream Join (PySpark)

```python
from pyspark.sql import functions as F

# Read two streams
orders_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "orders").load()

payments_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "payments").load()

# Parse
orders = orders_stream.select(F.from_json(F.col("value").cast("string"), orders_schema).alias("d")).select("d.*")
payments = payments_stream.select(F.from_json(F.col("value").cast("string"), payments_schema).alias("d")).select("d.*")

# Add watermarks (required for stream-stream joins)
orders_w = orders.withWatermark("order_time", "10 minutes")
payments_w = payments.withWatermark("payment_time", "20 minutes")

# Join within time window
joined = orders_w.join(
    payments_w,
    (orders_w.order_id == payments_w.order_id) &
    (payments_w.payment_time >= orders_w.order_time) &
    (payments_w.payment_time <= orders_w.order_time + F.expr("INTERVAL 1 HOUR")),
    "leftOuter"
)
```

### Stream-Table Join (Kafka + PySpark)

```python
# Static reference table joined with stream
customers_static = spark.read.parquet("s3://bucket/customers/")

orders_stream_parsed = orders_stream.select(
    F.from_json(F.col("value").cast("string"), orders_schema).alias("d")
).select("d.*")

enriched = orders_stream_parsed.join(
    F.broadcast(customers_static),  # broadcast for small lookup tables
    on="customer_id",
    how="left"
)
```

---

## Schema Validation at Processing

```python
import pandera as pa
from pandera.typing import Series

class OrderSchema(pa.DataFrameModel):
    order_id: Series[str] = pa.Field(nullable=False, unique=True)
    customer_id: Series[str] = pa.Field(nullable=False)
    amount: Series[float] = pa.Field(gt=0, lt=1_000_000)
    status: Series[str] = pa.Field(isin=["pending", "completed", "cancelled", "refunded"])
    order_date: Series[pa.DateTime] = pa.Field(nullable=False)

    class Config:
        coerce = True  # attempt type coercion before validation

@pa.check_types
def process_orders(df: pa.typing.DataFrame[OrderSchema]) -> pd.DataFrame:
    """Pandera enforces schema at function entry."""
    return df.assign(total_with_tax=df["amount"] * 1.18)

# Usage
try:
    result = process_orders(raw_df)
except pa.errors.SchemaError as e:
    print(f"Schema validation failed: {e}")
    # Route to dead letter queue
```

---

## Error Handling & Dead Letter Queues

```python
from kafka import KafkaProducer, KafkaConsumer
import json
import traceback

producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda v: json.dumps(v).encode()
)

def process_with_dlq(message: dict, processor_fn, dlq_topic: str = "orders-dlq"):
    """Process a message; route failures to Dead Letter Queue."""
    try:
        return processor_fn(message)
    except Exception as e:
        dead_letter = {
            "original_message": message,
            "error_type": type(e).__name__,
            "error_message": str(e),
            "stack_trace": traceback.format_exc(),
            "failed_at": datetime.utcnow().isoformat(),
            "retry_count": message.get("_retry_count", 0)
        }
        producer.send(dlq_topic, value=dead_letter)
        producer.flush()
        print(f"Sent to DLQ: {dead_letter['error_type']}")
        return None

# Airflow task with DLQ-style error isolation
def transform_task(**context):
    records = context["ti"].xcom_pull(task_ids="extract")
    good_records, failed_records = [], []
    
    for record in records:
        try:
            good_records.append(transform_record(record))
        except Exception as e:
            failed_records.append({"record": record, "error": str(e)})
    
    if failed_records:
        # Save failed records for inspection/replay
        pd.DataFrame(failed_records).to_csv(
            f"/tmp/failed_records_{context['ds']}.csv", index=False
        )
    
    return good_records
```

---

## Parallel Processing Design

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import multiprocessing

# CPU-bound: ProcessPoolExecutor
def process_file(file_path: str) -> pd.DataFrame:
    """Heavy CPU-bound transformation."""
    df = pd.read_parquet(file_path)
    # ... expensive computation
    return df.groupby("customer_id").agg({"amount": "sum"})

def parallel_file_processing(file_paths: list[str]) -> pd.DataFrame:
    """Process files in parallel using multiple CPU cores."""
    n_workers = multiprocessing.cpu_count() - 1
    
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = {executor.submit(process_file, fp): fp for fp in file_paths}
        results = []
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"File {futures[future]} failed: {e}")
    
    return pd.concat(results, ignore_index=True)

# IO-bound: ThreadPoolExecutor
def download_file(s3_key: str) -> bytes:
    s3 = boto3.client("s3")
    return s3.get_object(Bucket="my-bucket", Key=s3_key)["Body"].read()

def parallel_downloads(s3_keys: list[str]) -> dict:
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(download_file, k): k for k in s3_keys}
        return {futures[f]: f.result() for f in as_completed(futures)}
```

---

# 5. Storage Layer Design

## Choosing the Right Storage

| Storage Type | Use Case | Examples |
|---|---|---|
| Operational DB | OLTP, application data | PostgreSQL, MySQL, DynamoDB |
| Data Warehouse | OLAP, analytics, SQL | Redshift, BigQuery, Snowflake |
| Data Lake | Raw storage, semi-structured, ML | S3, GCS, ADLS |
| Lakehouse | Unified ACID + analytics | Delta Lake, Apache Iceberg, Hudi |

---

## Medallion Architecture (Bronze → Silver → Gold)

```
Raw/Bronze                Silver                    Gold
────────────        ──────────────────       ──────────────────
• Raw data          • Cleaned, validated     • Business-ready
• Immutable         • Deduped                • Aggregated
• Append-only       • Type-cast              • Joined/modeled
• No transformation • Schema enforced        • Ready for BI/ML
```

```python
# PySpark Medallion Architecture implementation

# ── BRONZE: Land raw data as-is ──────────────────────────────
def write_bronze(spark, raw_df, source: str, run_date: str):
    """Write raw data with ingestion metadata — never overwrite."""
    bronze_path = f"s3://datalake/bronze/{source}/date={run_date}/"
    
    enriched = raw_df \
        .withColumn("_ingested_at", F.current_timestamp()) \
        .withColumn("_source", F.lit(source)) \
        .withColumn("_run_date", F.lit(run_date))
    
    enriched.write.mode("overwrite").parquet(bronze_path)
    print(f"Bronze written: {bronze_path}")

# ── SILVER: Clean and validate ────────────────────────────────
def bronze_to_silver(spark, source: str, run_date: str):
    """Clean bronze layer into validated silver layer."""
    bronze_path = f"s3://datalake/bronze/{source}/date={run_date}/"
    silver_path = f"s3://datalake/silver/{source}/date={run_date}/"
    
    df = spark.read.parquet(bronze_path)
    
    silver = (df
        .dropDuplicates(["order_id"])
        .filter(F.col("order_id").isNotNull())
        .withColumn("amount", F.col("amount").cast("double"))
        .withColumn("order_date", F.to_date("order_date"))
        .filter(F.col("amount") > 0)
        .withColumn("_silver_processed_at", F.current_timestamp())
    )
    
    silver.write.mode("overwrite").parquet(silver_path)

# ── GOLD: Business aggregations ───────────────────────────────
def silver_to_gold(spark, run_date: str):
    """Aggregate silver into business-level gold metrics."""
    silver_path = f"s3://datalake/silver/orders/date={run_date}/"
    gold_path = f"s3://datalake/gold/daily_revenue/date={run_date}/"
    
    df = spark.read.parquet(silver_path)
    
    gold = (df
        .groupBy("region", "product_category")
        .agg(
            F.sum("amount").alias("total_revenue"),
            F.count("order_id").alias("order_count"),
            F.avg("amount").alias("avg_order_value"),
            F.countDistinct("customer_id").alias("unique_customers")
        )
        .withColumn("run_date", F.lit(run_date))
    )
    
    gold.write.mode("overwrite").parquet(gold_path)
```

---

## Partitioning Strategy

```python
# PySpark: partition by date and region
def write_partitioned(df, output_path: str):
    """Write data partitioned for efficient query pruning."""
    df.write \
        .mode("overwrite") \
        .partitionBy("year", "month", "day", "region") \
        .parquet(output_path)

# Good partition keys:
#   - Date columns (year/month/day)
#   - Low-to-medium cardinality columns (region, status)
#   - Columns frequently used in WHERE clauses

# Bad partition keys:
#   - High cardinality (customer_id, order_id → too many small files)
#   - Columns never used in filters
```

---

## File Format Selection

| Format | Best For | Pros | Cons |
|--------|----------|------|------|
| **Parquet** | Analytics, columnar queries | Columnar, compressed, splittable | Not human-readable |
| **Avro** | Streaming, schema evolution | Row-based, schema embedded, Kafka-native | Slower analytics |
| **ORC** | Hive workloads | Compressed, predicate pushdown | Less ecosystem support |
| **JSON** | Flexibility, APIs | Human-readable, flexible schema | Large size, slow queries |
| **Delta/Iceberg** | Lakehouse, ACID | ACID, time travel, schema evolution | Overhead |

```python
# Writing in different formats
df.write.parquet("s3://bucket/path/", compression="snappy")
df.write.format("avro").save("s3://bucket/path/")
df.write.orc("s3://bucket/path/")

# Delta Lake (ACID with time travel)
df.write.format("delta").mode("overwrite").save("s3://bucket/delta_table/")

# Read with time travel
spark.read.format("delta") \
    .option("versionAsOf", 5) \
    .load("s3://bucket/delta_table/")
```

---

## Compaction & Vacuuming

```python
# Delta Lake compaction (optimize small files)
from delta.tables import DeltaTable

delta_table = DeltaTable.forPath(spark, "s3://bucket/delta_table/")

# Compact small files (bin-packing)
delta_table.optimize().executeCompaction()

# Z-order for multi-dimensional pruning
delta_table.optimize().executeZOrderBy("customer_id", "order_date")

# Vacuum: remove old files beyond retention period
delta_table.vacuum(retentionHours=168)  # 7 days retention
```

---

# 6. Batch Pipeline Design

## Anatomy of a Batch Pipeline

```
┌─────────┐   ┌──────────┐   ┌───────────┐   ┌──────────┐   ┌────────┐
│ Schedule│──▶│ Extract  │──▶│ Validate  │──▶│Transform │──▶│  Load  │
└─────────┘   └──────────┘   └───────────┘   └──────────┘   └────────┘
                                    │                              │
                                    ▼                              ▼
                               ┌─────────┐                  ┌──────────┐
                               │  DLQ /  │                  │ Notify / │
                               │ Quarant.│                  │ Monitor  │
                               └─────────┘                  └──────────┘
```

---

## Batch Pipeline with Spark + Airflow

```python
# airflow/dags/batch_orders_pipeline.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "email_on_failure": True,
    "email": ["de-team@company.com"],
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=2),
}

with DAG(
    "batch_orders_pipeline",
    default_args=default_args,
    description="Daily orders batch pipeline",
    schedule_interval="0 3 * * *",  # 3 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["orders", "batch"],
) as dag:

    extract = SparkSubmitOperator(
        task_id="extract_orders",
        application="s3://code/spark/extract_orders.py",
        conf={"spark.executor.instances": "10"},
        application_args=["--date", "{{ ds }}"],
    )

    validate = PythonOperator(
        task_id="validate_schema",
        python_callable=validate_orders_schema,
        op_kwargs={"date": "{{ ds }}"},
    )

    transform = SparkSubmitOperator(
        task_id="transform_orders",
        application="s3://code/spark/transform_orders.py",
        conf={"spark.executor.memory": "8g"},
        application_args=["--date", "{{ ds }}"],
    )

    load = SparkSubmitOperator(
        task_id="load_to_warehouse",
        application="s3://code/spark/load_warehouse.py",
        application_args=["--date", "{{ ds }}"],
    )

    notify = PythonOperator(
        task_id="send_completion_notification",
        python_callable=send_slack_notification,
        op_kwargs={"message": "Orders pipeline complete for {{ ds }}"},
    )

    extract >> validate >> transform >> load >> notify
```

---

## Incremental Batch Patterns

### Append-only (New Records)

```python
def append_only_load(spark, source_path: str, target_path: str, watermark_ts: str):
    """Load only new records appended since watermark."""
    df = spark.read.parquet(source_path) \
        .filter(F.col("created_at") > watermark_ts)
    
    df.write.mode("append").partitionBy("date").parquet(target_path)
    return df.count()
```

### Upsert Pattern (Merge)

```python
from delta.tables import DeltaTable

def upsert_to_delta(spark, updates_df, target_path: str, merge_key: str):
    """Merge updates into Delta Lake table (upsert)."""
    target = DeltaTable.forPath(spark, target_path)
    
    (target.alias("target")
        .merge(
            updates_df.alias("source"),
            f"target.{merge_key} = source.{merge_key}"
        )
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )
```

---

## Backfill Design

```python
# Airflow: Dynamic backfill with configurable date range
from airflow.models import Variable

def get_backfill_dates(start: str, end: str) -> list[str]:
    """Generate list of dates for backfill range."""
    import pandas as pd
    return [str(d.date()) for d in pd.date_range(start, end, freq="D")]

with DAG("backfill_pipeline", schedule_interval=None, start_date=datetime(2024, 1, 1)) as dag:
    
    def run_for_date(run_date: str, **kwargs):
        print(f"Backfilling: {run_date}")
        # ... pipeline logic for run_date
    
    backfill_start = "{{ dag_run.conf.get('start_date', '2024-01-01') }}"
    backfill_end = "{{ dag_run.conf.get('end_date', '2024-12-31') }}"
    
    dates = get_backfill_dates("2024-01-01", "2024-06-30")
    
    prev_task = None
    for date in dates:
        task = PythonOperator(
            task_id=f"backfill_{date.replace('-', '_')}",
            python_callable=run_for_date,
            op_kwargs={"run_date": date},
        )
        if prev_task:
            prev_task >> task
        prev_task = task
```

---

## Dependency Management

```python
# Airflow: cross-DAG dependencies using ExternalTaskSensor
from airflow.sensors.external_task import ExternalTaskSensor

with DAG("downstream_pipeline", schedule_interval="0 5 * * *") as dag:
    
    wait_for_upstream = ExternalTaskSensor(
        task_id="wait_for_orders_pipeline",
        external_dag_id="batch_orders_pipeline",
        external_task_id="load_to_warehouse",
        execution_delta=timedelta(hours=2),  # upstream runs 2h earlier
        timeout=3600,        # wait max 1 hour
        mode="reschedule",   # release worker slot while waiting
    )
    
    process = PythonOperator(
        task_id="downstream_processing",
        python_callable=downstream_process,
    )
    
    wait_for_upstream >> process
```

---

# 7. Streaming Pipeline Design

## Anatomy of a Streaming Pipeline

```
Event Source → Message Broker → Stream Processor → Sink
    │               │                 │               │
Kafka Producer   Kafka Topic     Spark/Flink     S3/Redshift/
Database CDC     Kinesis         Kafka Streams   Cassandra
Webhooks         Pulsar          Faust           Elasticsearch
```

---

## Event Time vs Processing Time

```python
from pyspark.sql import functions as F

# Event time: when the event actually happened (in the data)
# Processing time: when the event was processed by the pipeline

df_with_watermark = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "orders")
    .load()
    .select(F.from_json(F.col("value").cast("string"), schema).alias("d"))
    .select("d.*")
    # Use EVENT TIME (not processing time) for accurate windowing
    .withWatermark("event_timestamp", "10 minutes")
)

# Group by event time window
windowed = (
    df_with_watermark
    .groupBy(
        F.window("event_timestamp", "1 hour"),  # event time window
        "region"
    )
    .agg(F.sum("amount").alias("hourly_revenue"))
)
```

---

## Windowing (Tumbling, Sliding, Session)

```python
from pyspark.sql import functions as F

# 1. TUMBLING WINDOW: non-overlapping, fixed size
tumbling = (
    df.withWatermark("event_time", "5 minutes")
    .groupBy(
        F.window("event_time", "1 hour"),       # 1-hour tumbling window
        "product_id"
    )
    .agg(F.count("*").alias("event_count"))
)

# 2. SLIDING WINDOW: overlapping windows
sliding = (
    df.withWatermark("event_time", "5 minutes")
    .groupBy(
        F.window("event_time", "1 hour", "15 minutes"),  # 1h window, slide every 15m
        "product_id"
    )
    .agg(F.sum("amount").alias("revenue"))
)

# 3. SESSION WINDOW: dynamic, based on activity gaps
session = (
    df.withWatermark("event_time", "10 minutes")
    .groupBy(
        F.session_window("event_time", "30 minutes"),  # session ends after 30m idle
        "user_id"
    )
    .agg(F.count("*").alias("actions_in_session"))
)
```

---

## Watermarking & Late Data Handling

```python
# Watermarks tell Spark how late data can arrive
# and when it's safe to finalize window results

df_stream = (
    raw_stream
    .withWatermark("event_time", "2 hours")  # tolerate up to 2h late data
    .groupBy(
        F.window("event_time", "1 hour"),
        "region"
    )
    .agg(F.sum("amount").alias("total"))
)

# outputMode for windowed aggregations:
# "append": only emit finalized windows (after watermark passes)
# "update": emit updated results as late data arrives
# "complete": emit all windows every trigger (memory intensive)

query = df_stream.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "s3://bucket/windowed_revenue/") \
    .option("checkpointLocation", "s3://bucket/checkpoints/") \
    .start()
```

---

## Exactly-once Semantics Design

```python
# Kafka transactions for exactly-once producer
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient

producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    acks="all",
    enable_idempotence=True,            # dedup at broker level
    transactional_id="orders-producer-1"  # enables transactions
)

producer.init_transactions()

try:
    producer.begin_transaction()
    producer.send("orders-enriched", key=b"order_1", value=b"payload")
    producer.send("audit-log", key=b"order_1", value=b"processed")
    producer.commit_transaction()
except Exception as e:
    producer.abort_transaction()
    raise

# PySpark: exactly-once with checkpointing + idempotent writes
query = df_stream.writeStream \
    .outputMode("append") \
    .format("delta") \
    .option("path", "s3://bucket/delta/orders/") \
    .option("checkpointLocation", "s3://bucket/checkpoints/orders/") \
    .start()
# Spark uses checkpoint to track processed offsets
# Delta ACID ensures no duplicates on retry
```

---

## Checkpointing & Recovery

```python
# Spark Structured Streaming checkpoint = fault tolerance
# Checkpoint stores:
#   - Kafka offsets consumed
#   - State store snapshots
#   - Metadata about completed micro-batches

query = (
    stream_df
    .writeStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("topic", "output-topic")
    .option("checkpointLocation", "s3://bucket/checkpoints/stream-job/")
    .start()
)

# On failure and restart, Spark resumes from checkpoint automatically
# No data loss, no reprocessing from the beginning
```

---

## Streaming Pipeline with Kafka + Spark

```python
# Full streaming pipeline: Kafka → Spark → Delta Lake
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("RealTimeOrdersPipeline") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

order_schema = StructType([
    StructField("order_id", StringType(), False),
    StructField("customer_id", StringType(), False),
    StructField("amount", DoubleType(), True),
    StructField("product_id", StringType(), True),
    StructField("event_time", TimestampType(), True),
    StructField("region", StringType(), True),
])

# Read from Kafka
raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "orders") \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load()

# Parse & validate
orders = (
    raw
    .select(F.from_json(F.col("value").cast("string"), order_schema).alias("d"))
    .select("d.*")
    .filter(F.col("order_id").isNotNull())
    .filter(F.col("amount") > 0)
    .withWatermark("event_time", "10 minutes")
)

# Aggregate: 1-hour window revenue by region
windowed = (
    orders
    .groupBy(F.window("event_time", "1 hour"), "region")
    .agg(
        F.sum("amount").alias("total_revenue"),
        F.count("order_id").alias("order_count")
    )
    .select(
        F.col("window.start").alias("window_start"),
        F.col("window.end").alias("window_end"),
        "region", "total_revenue", "order_count"
    )
)

# Write to Delta Lake
query = windowed.writeStream \
    .outputMode("append") \
    .format("delta") \
    .option("path", "s3://bucket/delta/hourly_revenue/") \
    .option("checkpointLocation", "s3://bucket/checkpoints/hourly_revenue/") \
    .trigger(processingTime="1 minute") \
    .start()

query.awaitTermination()
```

---

# 8. CDC Pipeline Design

## What is CDC?

Change Data Capture (CDC) tracks every data modification (INSERT, UPDATE, DELETE) at the database level and streams these changes to downstream systems in near real-time.

**Use cases:** Real-time data sync, audit trails, cache invalidation, ETL without full scans.

---

## Log-based CDC vs Query-based CDC

| | Log-based CDC | Query-based CDC |
|--|---|---|
| **Mechanism** | Reads DB binary/WAL log | Polls table with `updated_at > last_run` |
| **Latency** | Milliseconds | Minutes (polling interval) |
| **Source load** | Very low | Higher (full/incremental scans) |
| **Handles deletes** | Yes | No (hard deletes are invisible) |
| **Tools** | Debezium, AWS DMS | Airbyte, Fivetran, custom scripts |

---

## CDC with Debezium

```yaml
# Debezium connector config (registered via Kafka Connect REST API)
{
  "name": "mysql-orders-cdc",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "mysql-host",
    "database.port": "3306",
    "database.user": "debezium_user",
    "database.password": "secret",
    "database.server.id": "12345",
    "database.server.name": "mydb",
    "database.include.list": "shop",
    "table.include.list": "shop.orders",
    "database.history.kafka.bootstrap.servers": "kafka:9092",
    "database.history.kafka.topic": "schema-changes.shop",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "transforms.unwrap.drop.tombstones": "false"
  }
}
```

```python
# Consuming Debezium CDC events from Kafka
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "mydb.shop.orders",
    bootstrap_servers=["kafka:9092"],
    group_id="cdc-warehouse-sync",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
)

def sync_to_warehouse(conn, event: dict):
    """Apply CDC event to data warehouse."""
    op = event.get("op")
    after = event.get("after", {})
    before = event.get("before", {})
    
    if op in ("c", "r"):  # create / snapshot read
        conn.execute("""
            INSERT INTO orders_dw (order_id, customer_id, amount, status, updated_at)
            VALUES (%(order_id)s, %(customer_id)s, %(amount)s, %(status)s, %(updated_at)s)
            ON CONFLICT (order_id) DO NOTHING
        """, after)
    
    elif op == "u":  # update
        conn.execute("""
            INSERT INTO orders_dw (order_id, customer_id, amount, status, updated_at)
            VALUES (%(order_id)s, %(customer_id)s, %(amount)s, %(status)s, %(updated_at)s)
            ON CONFLICT (order_id) DO UPDATE SET
                customer_id = EXCLUDED.customer_id,
                amount = EXCLUDED.amount,
                status = EXCLUDED.status,
                updated_at = EXCLUDED.updated_at
        """, after)
    
    elif op == "d":  # delete
        conn.execute("""
            UPDATE orders_dw
            SET is_deleted = TRUE, deleted_at = NOW()
            WHERE order_id = %(order_id)s
        """, before)

for msg in consumer:
    event = msg.value
    with db_conn.begin():
        sync_to_warehouse(db_conn, event)
```

---

## Handling Schema Changes in CDC

```python
# Schema Registry integration with Avro for schema evolution
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

schema_registry_client = SchemaRegistryClient({"url": "http://schema-registry:8081"})

def get_current_schema(topic: str) -> dict:
    """Fetch the latest schema for a topic from Schema Registry."""
    subject = f"{topic}-value"
    schema = schema_registry_client.get_latest_version(subject)
    return json.loads(schema.schema.schema_str)

# Handle backward-compatible schema changes:
# - Adding nullable columns: safe, set default in DW
# - Renaming columns: use aliases in consumers
# - Removing columns: consumer must handle missing keys gracefully

def safe_extract(event: dict, field: str, default=None):
    """Extract field with fallback for schema evolution."""
    return event.get(field, default)

def apply_cdc_event_resilient(event: dict) -> dict:
    return {
        "order_id": safe_extract(event, "order_id"),
        "customer_id": safe_extract(event, "customer_id"),
        "amount": safe_extract(event, "amount", 0.0),
        "new_field": safe_extract(event, "new_field", "default_value"),  # new column
    }
```

---

# 9. Orchestration Design

## DAG Design Principles

1. **Atomicity:** Each task should do one thing well and be independently retriable.
2. **Idempotency:** Re-running any task produces the same result.
3. **Minimal footprint:** Don't pass large data through XCom — use external storage.
4. **Observable:** Each task should emit meaningful logs and metrics.

```python
# Good DAG structure: clear, atomic tasks
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG("well_designed_dag", schedule_interval="@daily", start_date=datetime(2024,1,1)) as dag:
    
    # Each task is atomic, retriable, and observable
    extract = PythonOperator(task_id="extract", python_callable=extract_fn)
    validate = PythonOperator(task_id="validate", python_callable=validate_fn)
    transform = PythonOperator(task_id="transform", python_callable=transform_fn)
    load = PythonOperator(task_id="load", python_callable=load_fn)
    notify = PythonOperator(task_id="notify", python_callable=notify_fn)
    
    extract >> validate >> transform >> load >> notify
```

---

## Dynamic DAGs

```python
# Dynamic tasks from config or database
from airflow.decorators import dag, task
import yaml

TABLES = yaml.safe_load(open("config/tables.yaml"))["tables"]

with DAG("dynamic_table_ingestion", schedule_interval="@daily", start_date=datetime(2024,1,1)) as dag:
    
    def make_ingest_task(table_name: str):
        return PythonOperator(
            task_id=f"ingest_{table_name}",
            python_callable=ingest_table,
            op_kwargs={"table": table_name, "date": "{{ ds }}"},
        )
    
    ingest_tasks = [make_ingest_task(t) for t in TABLES]
    
    # All tables must finish before aggregation
    final_aggregate = PythonOperator(
        task_id="aggregate_all",
        python_callable=final_agg,
    )
    
    for task in ingest_tasks:
        task >> final_aggregate
```

---

## Retry & Timeout Strategies

```python
# Airflow: different retry strategies per task type
from airflow.utils.trigger_rule import TriggerRule

default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,   # 5m, 10m, 20m
    "max_retry_delay": timedelta(hours=1),
    "execution_timeout": timedelta(hours=2),
}

# For critical tasks: more retries, alerting
critical_task = PythonOperator(
    task_id="critical_load",
    python_callable=load_fn,
    retries=5,
    retry_delay=timedelta(minutes=2),
    on_failure_callback=page_oncall,
    execution_timeout=timedelta(hours=4),
)

# Cleanup task: always runs even if pipeline fails
cleanup = PythonOperator(
    task_id="cleanup",
    python_callable=cleanup_fn,
    trigger_rule=TriggerRule.ALL_DONE,  # runs regardless of upstream success/failure
)
```

---

## Alerting & SLA Monitoring

```python
import requests

def slack_alert(context):
    """Send Slack notification on DAG failure."""
    dag_id = context["dag"].dag_id
    task_id = context["task"].task_id
    run_id = context["run_id"]
    log_url = context["task_instance"].log_url
    
    message = {
        "text": f":red_circle: *Pipeline Failure*",
        "blocks": [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*DAG:* `{dag_id}`\n"
                    f"*Task:* `{task_id}`\n"
                    f"*Run ID:* `{run_id}`\n"
                    f"<{log_url}|View Logs>"
                )
            }
        }]
    }
    
    requests.post(
        url="https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
        json=message
    )

with DAG(
    "monitored_dag",
    default_args={"on_failure_callback": slack_alert},
    schedule_interval="@hourly",
    start_date=datetime(2024, 1, 1),
    sla_miss_callback=slack_alert,
) as dag:
    pass
```

---

# 10. Data Quality in Pipelines

## Validation at Ingestion

```python
import pandas as pd
from dataclasses import dataclass, field
from typing import List

@dataclass
class ValidationResult:
    passed: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    row_count: int = 0
    valid_row_count: int = 0

def validate_ingested_data(df: pd.DataFrame) -> ValidationResult:
    """Run validation checks on ingested data."""
    result = ValidationResult(passed=True, row_count=len(df))
    errors = []
    warnings = []
    
    # Check 1: Required columns
    required_cols = {"order_id", "customer_id", "amount", "order_date"}
    missing = required_cols - set(df.columns)
    if missing:
        errors.append(f"Missing required columns: {missing}")
    
    # Check 2: Null rates
    null_rates = df.isnull().mean()
    for col, rate in null_rates.items():
        if col in required_cols and rate > 0:
            errors.append(f"Required column '{col}' has {rate:.1%} nulls")
        elif rate > 0.2:
            warnings.append(f"Column '{col}' has high null rate: {rate:.1%}")
    
    # Check 3: Duplicates
    dup_count = df.duplicated(subset=["order_id"]).sum()
    if dup_count > 0:
        errors.append(f"{dup_count} duplicate order_ids found")
    
    # Check 4: Value ranges
    if "amount" in df.columns:
        invalid_amounts = (df["amount"] <= 0).sum()
        if invalid_amounts > 0:
            errors.append(f"{invalid_amounts} records with non-positive amount")
    
    # Check 5: Freshness
    if "order_date" in df.columns:
        max_date = pd.to_datetime(df["order_date"]).max()
        staleness = (pd.Timestamp.now() - max_date).days
        if staleness > 2:
            warnings.append(f"Data may be stale: latest record is {staleness} days old")
    
    result.errors = errors
    result.warnings = warnings
    result.passed = len(errors) == 0
    result.valid_row_count = len(df.dropna(subset=list(required_cols & set(df.columns))))
    
    return result
```

---

## Data Quality Gates

```python
# Airflow DQ gate: fail pipeline if quality checks don't pass
from airflow.exceptions import AirflowException

def run_quality_gate(date: str, **context):
    """Data quality gate — fails the pipeline if checks don't pass."""
    df = load_processed_data(date)
    result = validate_ingested_data(df)
    
    for warning in result.warnings:
        print(f"[WARNING] {warning}")
    
    if not result.passed:
        error_summary = "\n".join(result.errors)
        raise AirflowException(
            f"Data quality gate FAILED for {date}:\n{error_summary}"
        )
    
    print(f"[PASS] Quality gate passed: {result.valid_row_count}/{result.row_count} valid rows")

quality_gate = PythonOperator(
    task_id="data_quality_gate",
    python_callable=run_quality_gate,
    op_kwargs={"date": "{{ ds }}"},
)

transform >> quality_gate >> load
```

---

## Quarantine Pattern

```python
def quarantine_bad_records(df: pd.DataFrame, rules: list) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split records into clean and quarantined sets.
    Quarantined records are stored for review without blocking the pipeline.
    """
    mask = pd.Series([True] * len(df), index=df.index)
    
    for rule_name, rule_fn in rules:
        failed = ~rule_fn(df)
        df.loc[failed, "_quarantine_reason"] = rule_name
        mask &= ~failed
    
    clean_df = df[mask].drop(columns=["_quarantine_reason"], errors="ignore")
    quarantine_df = df[~mask]
    
    return clean_df, quarantine_df

# Usage
rules = [
    ("positive_amount", lambda df: df["amount"] > 0),
    ("valid_customer_id", lambda df: df["customer_id"].str.match(r"^CUST\d{6}$")),
    ("not_duplicate", lambda df: ~df.duplicated(subset=["order_id"], keep="first")),
]

clean, quarantined = quarantine_bad_records(raw_df, rules)

# Store quarantined records for review
quarantined.to_parquet(f"s3://bucket/quarantine/date={run_date}/records.parquet")
print(f"Clean: {len(clean)}, Quarantined: {len(quarantined)}")

# Process only clean records
process_and_load(clean)
```

---

# 11. Pipeline Observability

## Pipeline Logging Design

```python
import logging
import json
import time
from contextlib import contextmanager

# Structured logging for machine-readable logs
class PipelineLogger:
    def __init__(self, pipeline_name: str, run_id: str):
        self.pipeline_name = pipeline_name
        self.run_id = run_id
        self.logger = logging.getLogger(pipeline_name)
    
    def _log(self, level: str, message: str, **kwargs):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "pipeline": self.pipeline_name,
            "run_id": self.run_id,
            "message": message,
            **kwargs
        }
        getattr(self.logger, level.lower())(json.dumps(log_entry))
    
    def info(self, msg: str, **kwargs): self._log("INFO", msg, **kwargs)
    def warning(self, msg: str, **kwargs): self._log("WARNING", msg, **kwargs)
    def error(self, msg: str, **kwargs): self._log("ERROR", msg, **kwargs)
    
    @contextmanager
    def task(self, task_name: str):
        start = time.time()
        self.info(f"Task started: {task_name}", task=task_name)
        try:
            yield
            duration = time.time() - start
            self.info(f"Task completed: {task_name}", task=task_name, duration_seconds=duration)
        except Exception as e:
            duration = time.time() - start
            self.error(f"Task failed: {task_name}", task=task_name, error=str(e), duration_seconds=duration)
            raise

# Usage
logger = PipelineLogger("orders_pipeline", run_id="2024-01-15-001")

with logger.task("extract_orders"):
    df = extract_from_source()

with logger.task("validate"):
    result = validate_ingested_data(df)
    logger.info("Validation complete", rows=len(df), valid_rows=result.valid_row_count)
```

---

## Metrics to Track

```python
# Key pipeline metrics with Prometheus-style counters
from prometheus_client import Counter, Histogram, Gauge, push_to_gateway

# Counters
records_processed = Counter("pipeline_records_processed_total", "Records processed", ["pipeline", "stage"])
records_failed = Counter("pipeline_records_failed_total", "Records failed", ["pipeline", "stage", "error_type"])

# Histograms (latency)
task_duration = Histogram("pipeline_task_duration_seconds", "Task duration", ["pipeline", "task"])

# Gauges (current state)
pipeline_lag = Gauge("pipeline_lag_seconds", "Seconds behind real-time", ["pipeline"])

# In pipeline code:
def instrumented_process(records: list, pipeline: str) -> list:
    with task_duration.labels(pipeline=pipeline, task="process").time():
        results = []
        for rec in records:
            try:
                results.append(transform(rec))
                records_processed.labels(pipeline=pipeline, stage="process").inc()
            except Exception as e:
                records_failed.labels(
                    pipeline=pipeline, stage="process", error_type=type(e).__name__
                ).inc()
        return results

# Push metrics to Pushgateway
push_to_gateway("http://pushgateway:9091", job="orders_pipeline", registry=REGISTRY)
```

---

## Data Lineage Tracking

```python
# Simple lineage metadata tracking
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class LineageEvent:
    pipeline: str
    run_id: str
    task: str
    input_dataset: str
    output_dataset: str
    input_row_count: int
    output_row_count: int
    transformation_logic: str
    executed_at: str
    upstream_run_ids: Optional[List[str]] = None

def track_lineage(event: LineageEvent, lineage_db_conn):
    """Persist lineage event to lineage database (e.g., Marquez, OpenLineage)."""
    lineage_db_conn.execute("""
        INSERT INTO pipeline_lineage 
        (pipeline, run_id, task, input_dataset, output_dataset,
         input_rows, output_rows, logic, executed_at)
        VALUES (%(pipeline)s, %(run_id)s, %(task)s, %(input_dataset)s, %(output_dataset)s,
                %(input_row_count)s, %(output_row_count)s, %(transformation_logic)s, %(executed_at)s)
    """, event.__dict__)

# OpenLineage integration (standard lineage protocol)
from openlineage.client import OpenLineageClient
from openlineage.client.run import RunEvent, RunState, Run, Job

client = OpenLineageClient.from_environment()

def emit_openlineage_start(job_name: str, run_id: str):
    client.emit(RunEvent(
        eventType=RunState.START,
        eventTime=datetime.utcnow().isoformat(),
        run=Run(runId=run_id),
        job=Job(namespace="my_pipeline", name=job_name),
        inputs=[],
        outputs=[],
    ))
```

---

# 12. Performance & Optimization

## Parallelism & Concurrency in Pipelines

```python
# PySpark: tune parallelism for large jobs
spark = SparkSession.builder \
    .config("spark.default.parallelism", "400") \
    .config("spark.sql.shuffle.partitions", "400") \
    .config("spark.executor.instances", "50") \
    .config("spark.executor.cores", "4") \
    .config("spark.executor.memory", "8g") \
    .getOrCreate()

# Airflow: control DAG-level concurrency
dag = DAG(
    "parallel_pipeline",
    max_active_runs=2,          # max concurrent DAG runs
    concurrency=8,              # max concurrent tasks in this DAG
    schedule_interval="@hourly",
)
```

---

## Avoiding Data Skew

```python
# Problem: One partition much larger than others (hot keys)
# Solution 1: Salting

from pyspark.sql import functions as F
import random

def add_salt(df, salt_factor: int = 10):
    """Add random salt to high-cardinality join key to distribute load."""
    return df.withColumn("salt", (F.rand() * salt_factor).cast("int")) \
             .withColumn("salted_key", F.concat_ws("_", F.col("customer_id"), F.col("salt")))

# Solution 2: Broadcast join (avoid shuffle for small tables)
from pyspark.sql.functions import broadcast

result = large_df.join(broadcast(small_lookup_df), on="product_id", how="left")

# Solution 3: Repartition to balance
df_balanced = df.repartition(200, "order_date")  # partition by date for even distribution
```

---

## Small File Problem & Compaction

```python
# Problem: Many small Parquet files → slow reads (S3 metadata overhead)
# Solution: Compact small files periodically

from pyspark.sql import SparkSession

def compact_partitions(spark, table_path: str, partition_date: str, target_file_size_mb: int = 128):
    """Compact many small files into fewer larger files."""
    path = f"{table_path}/date={partition_date}"
    df = spark.read.parquet(path)
    
    # Estimate optimal partitions
    total_size_bytes = get_partition_size(path)  # custom function to get S3 size
    target_partitions = max(1, int(total_size_bytes / (target_file_size_mb * 1024 * 1024)))
    
    df.coalesce(target_partitions) \
      .write.mode("overwrite") \
      .parquet(path)
    
    print(f"Compacted {partition_date} to {target_partitions} files")

# Delta Lake auto-compaction
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.minNumFiles", "50")
```

---

## Caching in Pipelines

```python
# PySpark: cache intermediate DataFrames used multiple times
from pyspark.storagelevel import StorageLevel

orders_df = spark.read.parquet("s3://bucket/orders/") \
    .filter(F.col("date") == "2024-01-15") \
    .cache()  # or .persist(StorageLevel.MEMORY_AND_DISK)

# Use cached df in multiple operations
daily_totals = orders_df.groupBy("region").agg(F.sum("amount"))
daily_counts = orders_df.groupBy("product_id").count()

# Unpersist when done
orders_df.unpersist()

# Python: functools.lru_cache for repeated function calls
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_customer_segment(customer_id: str) -> str:
    """Cache customer segment lookups to avoid repeated DB queries."""
    return db.query_one("SELECT segment FROM customers WHERE id = %s", customer_id)
```

---

## Pushdown Optimization

```python
# Predicate pushdown: filter at the data source (Parquet column stats)
# Bad: reads all data then filters
df_all = spark.read.parquet("s3://bucket/orders/")
df_filtered = df_all.filter("date = '2024-01-15' AND region = 'US'")

# Good: partition pruning + predicate pushdown at read time
df_optimized = spark.read.parquet("s3://bucket/orders/date=2024-01-15/") \
    .filter(F.col("region") == "US")

# Column pruning: only read needed columns
df_projected = spark.read.parquet("s3://bucket/orders/") \
    .select("order_id", "amount", "date")  # only reads these columns from Parquet

# Explain plan to verify pushdown
df_optimized.explain(extended=True)
```

---

# 13. Security in Pipelines

## Encryption at Rest & In Transit

```python
# At rest: S3 server-side encryption
import boto3

s3 = boto3.client("s3")

# Write with SSE-S3 encryption
s3.put_object(
    Bucket="my-bucket",
    Key="data/orders.parquet",
    Body=data,
    ServerSideEncryption="aws:kms",
    SSEKMSKeyId="arn:aws:kms:us-east-1:123456789012:key/your-key-id"
)

# In transit: always use TLS — enable in Kafka
kafka_config = {
    "bootstrap.servers": "kafka:9093",
    "security.protocol": "SSL",
    "ssl.ca.location": "/path/to/ca.crt",
    "ssl.certificate.location": "/path/to/client.crt",
    "ssl.key.location": "/path/to/client.key",
}
```

---

## PII Detection & Masking

```python
import hashlib
import re

def detect_pii(df: pd.DataFrame) -> dict:
    """Detect columns that likely contain PII."""
    pii_patterns = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "credit_card": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
    }
    
    pii_columns = {}
    for col in df.select_dtypes(include="object").columns:
        sample = df[col].dropna().head(100).astype(str)
        for pii_type, pattern in pii_patterns.items():
            if sample.str.match(pattern).mean() > 0.5:
                pii_columns[col] = pii_type
                break
    
    return pii_columns

def mask_pii(df: pd.DataFrame, pii_columns: dict) -> pd.DataFrame:
    """Apply appropriate masking to PII columns."""
    df = df.copy()
    
    for col, pii_type in pii_columns.items():
        if pii_type == "email":
            # Pseudonymize: hash preserves joins but hides value
            df[col] = df[col].apply(
                lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16] + "@masked.com"
                if pd.notna(x) else x
            )
        elif pii_type == "phone":
            df[col] = df[col].str.replace(r"\d", "*", regex=True)
        elif pii_type in ("ssn", "credit_card"):
            # Full redaction
            df[col] = "REDACTED"
    
    return df
```

---

## Secrets Management

```python
import boto3
import json
from functools import lru_cache

@lru_cache(maxsize=20)
def get_secret(secret_name: str, region: str = "us-east-1") -> dict:
    """Retrieve secret from AWS Secrets Manager (cached)."""
    client = boto3.client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

# Usage — never hardcode credentials
def get_db_connection():
    secret = get_secret("prod/orders-db/credentials")
    engine = create_engine(
        f"postgresql://{secret['username']}:{secret['password']}"
        f"@{secret['host']}/{secret['dbname']}"
    )
    return engine

# Airflow: use Connections (never put creds in code)
from airflow.hooks.postgres_hook import PostgresHook

def load_data(**context):
    hook = PostgresHook(postgres_conn_id="my_postgres")  # defined in Airflow UI
    conn = hook.get_conn()
```

---

# 14. Pipeline Design Patterns

## Fan-in & Fan-out Pattern

```python
# Fan-out: one source → multiple parallel consumers
with DAG("fan_out_dag") as dag:
    source = PythonOperator(task_id="extract_source", python_callable=extract)
    
    # Fan-out: parallel processing branches
    process_us = PythonOperator(task_id="process_us", python_callable=lambda: process_region("US"))
    process_eu = PythonOperator(task_id="process_eu", python_callable=lambda: process_region("EU"))
    process_ap = PythonOperator(task_id="process_ap", python_callable=lambda: process_region("AP"))
    
    # Fan-in: merge results
    merge = PythonOperator(task_id="merge_results", python_callable=merge_fn)
    
    source >> [process_us, process_eu, process_ap] >> merge
```

---

## Idempotent Write Pattern

```python
def idempotent_write(df: pd.DataFrame, conn, table: str, partition_key: str, partition_value: str):
    """
    Write pattern that is safe to run multiple times:
    1. Delete existing partition
    2. Insert new data
    Both within a single transaction.
    """
    with conn.begin() as txn:
        conn.execute(
            f"DELETE FROM {table} WHERE {partition_key} = :val",
            {"val": partition_value}
        )
        df.to_sql(table, conn, if_exists="append", index=False)
```

---

## Slowly Changing Dimension (SCD) Patterns

```python
# SCD Type 1: Overwrite (no history)
def scd_type1(df_updates: pd.DataFrame, conn, table: str, key: str):
    df_updates.to_sql(table, conn, if_exists="replace", index=False)  # simple overwrite

# SCD Type 2: Keep full history with effective dates
def scd_type2_upsert(spark, updates_df, target_path: str, key_col: str):
    """Implement SCD Type 2: expire old rows, insert new rows."""
    from delta.tables import DeltaTable
    
    target = DeltaTable.forPath(spark, target_path)
    
    # Stage updates with metadata
    staged = updates_df \
        .withColumn("effective_start", F.current_timestamp()) \
        .withColumn("effective_end", F.lit(None).cast("timestamp")) \
        .withColumn("is_current", F.lit(True))
    
    # Merge: expire current rows that changed, insert new versions
    (target.alias("t")
        .merge(staged.alias("s"), f"t.{key_col} = s.{key_col} AND t.is_current = true")
        .whenMatchedUpdate(
            condition="t.record_hash != s.record_hash",  # changed record
            set={
                "effective_end": "s.effective_start",
                "is_current": "false"
            }
        )
        .whenNotMatchedInsertAll()
        .execute()
    )
```

---

## Lambda Architecture Pattern

```python
# Lambda: Batch layer (accuracy) + Speed layer (low latency)
# Batch layer: full historical recompute nightly
def batch_layer_daily(spark, date: str):
    """Accurate historical aggregate — runs nightly."""
    df = spark.read.parquet(f"s3://datalake/raw/orders/")
    daily_agg = df.groupBy("date", "region").agg(F.sum("amount").alias("revenue"))
    daily_agg.write.mode("overwrite").parquet(f"s3://datalake/batch_views/daily_revenue/")

# Speed layer: real-time incremental (approximate)
# (Kafka + Spark Streaming, updates last few hours)

# Serving layer: query router — recent data from speed, historical from batch
def query_serving_layer(spark, start_date: str, end_date: str):
    cutoff = "2024-01-14"  # yesterday
    if end_date <= cutoff:
        return spark.read.parquet(f"s3://datalake/batch_views/daily_revenue/")
    else:
        batch = spark.read.parquet(f"s3://datalake/batch_views/daily_revenue/")
        realtime = spark.read.parquet(f"s3://datalake/speed_views/hourly_revenue/")
        return batch.union(realtime).groupBy("date", "region").agg(F.sum("revenue"))
```

---

## Kappa Architecture Pattern

```python
# Kappa: Single streaming layer for everything
# Reprocess historical data by replaying Kafka from beginning

# Set Kafka retention to cover reprocessing window
kafka_config = {
    "retention.ms": str(30 * 24 * 60 * 60 * 1000),  # 30 days
    "retention.bytes": str(1024 * 1024 * 1024 * 1024),  # 1 TB
}

# For reprocessing: start from earliest offset
query = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "orders")
    .option("startingOffsets", "earliest")  # replay from beginning
    .load()
)

# Write to new output path for clean reprocessing
query.writeStream \
    .format("delta") \
    .option("path", "s3://bucket/delta/orders_v2/") \
    .option("checkpointLocation", "s3://bucket/checkpoints/orders_v2/") \
    .start()
```

---

# 15. Classic Pipeline Design Problems

## Problem 1: Batch Ingestion Pipeline (S3 → Glue → Redshift)

```python
# Architecture: S3 (raw) → AWS Glue (transform) → Redshift (DW)

# Step 1: Glue Job (PySpark on AWS Glue)
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME", "run_date", "s3_input", "redshift_table"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Read raw data from S3
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [f"{args['s3_input']}/date={args['run_date']}/"]},
    format="parquet"
)

# Apply transformations
from awsglue.dynamicframe import DynamicFrame

df = datasource.toDF()
df_transformed = df \
    .dropDuplicates(["order_id"]) \
    .filter("amount > 0") \
    .withColumn("run_date", F.lit(args["run_date"]))

# Write to Redshift
glueContext.write_dynamic_frame.from_jdbc_conf(
    frame=DynamicFrame.fromDF(df_transformed, glueContext, "output"),
    catalog_connection="my_redshift_conn",
    connection_options={
        "dbtable": args["redshift_table"],
        "database": "analytics_db",
        "preactions": f"DELETE FROM {args['redshift_table']} WHERE run_date = '{args['run_date']}'"
    },
    redshift_tmp_dir="s3://my-bucket/glue-temp/"
)
job.commit()
```

---

## Problem 2: Real-time Streaming Pipeline (Kafka → Spark → S3)

```python
# Full implementation of Kafka → PySpark Structured Streaming → S3 Delta Lake

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("streaming_pipeline")

spark = SparkSession.builder \
    .appName("RealtimeOrdersPipeline") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.sql.shuffle.partitions", "100") \
    .getOrCreate()

schema = StructType([
    StructField("order_id", StringType(), False),
    StructField("customer_id", StringType(), False),
    StructField("amount", DoubleType()),
    StructField("region", StringType()),
    StructField("product_id", StringType()),
    StructField("event_time", TimestampType()),
    StructField("status", StringType()),
])

# Read from Kafka
stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "orders") \
    .option("startingOffsets", "latest") \
    .option("maxOffsetsPerTrigger", "10000") \
    .load()

# Parse and clean
orders = (
    stream
    .select(F.from_json(F.col("value").cast("string"), schema).alias("d"))
    .select("d.*")
    .filter(F.col("order_id").isNotNull() & (F.col("amount") > 0))
    .withColumn("processing_time", F.current_timestamp())
    .withWatermark("event_time", "15 minutes")
)

# Write raw stream to Delta (Bronze)
bronze_query = orders.writeStream \
    .outputMode("append") \
    .format("delta") \
    .option("path", "s3://datalake/delta/bronze/orders/") \
    .option("checkpointLocation", "s3://datalake/checkpoints/bronze/orders/") \
    .partitionBy("region") \
    .trigger(processingTime="30 seconds") \
    .start()

# Aggregate to Gold
windowed_revenue = (
    orders
    .groupBy(
        F.window("event_time", "1 hour", "15 minutes"),
        "region"
    )
    .agg(
        F.sum("amount").alias("revenue"),
        F.count("order_id").alias("order_count"),
        F.avg("amount").alias("avg_order_value")
    )
    .select("window.start", "window.end", "region", "revenue", "order_count", "avg_order_value")
)

gold_query = windowed_revenue.writeStream \
    .outputMode("append") \
    .format("delta") \
    .option("path", "s3://datalake/delta/gold/hourly_revenue/") \
    .option("checkpointLocation", "s3://datalake/checkpoints/gold/hourly_revenue/") \
    .trigger(processingTime="1 minute") \
    .start()

spark.streams.awaitAnyTermination()
```

---

## Problem 3: CDC Pipeline (MySQL → Debezium → Kafka → DW)

```python
# Step 1: Register Debezium connector (via Kafka Connect REST API)
import requests

connector_config = {
    "name": "mysql-cdc-connector",
    "config": {
        "connector.class": "io.debezium.connector.mysql.MySqlConnector",
        "database.hostname": "mysql-prod",
        "database.port": "3306",
        "database.user": "debezium",
        "database.password": "${file:/opt/secrets.properties:mysql.password}",
        "database.server.id": "1",
        "database.server.name": "prod",
        "database.include.list": "ecommerce",
        "table.include.list": "ecommerce.orders,ecommerce.customers",
        "database.history.kafka.bootstrap.servers": "kafka:9092",
        "database.history.kafka.topic": "schema-history.ecommerce",
        "snapshot.mode": "initial",
        "transforms": "unwrap",
        "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    }
}
requests.post("http://kafka-connect:8083/connectors", json=connector_config)

# Step 2: PySpark Structured Streaming consumer → Redshift
def cdc_to_redshift_pipeline(spark):
    """Consume CDC events from Kafka, apply to Redshift incrementally."""
    
    cdc_schema = StructType([
        StructField("order_id", LongType()),
        StructField("customer_id", LongType()),
        StructField("amount", DoubleType()),
        StructField("status", StringType()),
        StructField("updated_at", LongType()),
        StructField("__op", StringType()),  # Debezium operation flag
        StructField("__deleted", StringType()),
    ])
    
    stream = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("subscribe", "prod.ecommerce.orders")
        .load()
        .select(F.from_json(F.col("value").cast("string"), cdc_schema).alias("d"))
        .select("d.*")
    )
    
    def process_micro_batch(batch_df, batch_id):
        """Upsert CDC micro-batch to Redshift."""
        if batch_df.isEmpty():
            return
        
        # Separate deletes from upserts
        deletes = batch_df.filter(F.col("__deleted") == "true")
        upserts = batch_df.filter(F.col("__deleted") != "true")
        
        # Write upserts to staging table in Redshift
        upserts.write \
            .format("jdbc") \
            .option("url", "jdbc:redshift://host:5439/db") \
            .option("dbtable", "staging_orders_cdc") \
            .option("user", "admin") \
            .option("password", get_secret("redshift/password")["password"]) \
            .mode("overwrite") \
            .save()
        
        # Apply MERGE in Redshift
        redshift_merge_sql = """
            MERGE INTO orders_dw USING staging_orders_cdc AS src
            ON orders_dw.order_id = src.order_id
            WHEN MATCHED THEN UPDATE SET
                customer_id = src.customer_id,
                amount = src.amount,
                status = src.status,
                updated_at = src.updated_at
            WHEN NOT MATCHED THEN INSERT
                (order_id, customer_id, amount, status, updated_at)
                VALUES (src.order_id, src.customer_id, src.amount, src.status, src.updated_at)
        """
        execute_redshift_sql(redshift_merge_sql)
        print(f"Applied batch {batch_id}: {upserts.count()} upserts, {deletes.count()} deletes")
    
    stream.writeStream \
        .foreachBatch(process_micro_batch) \
        .option("checkpointLocation", "s3://bucket/checkpoints/cdc/orders/") \
        .trigger(processingTime="1 minute") \
        .start() \
        .awaitTermination()
```

---

## Problem 4: Airflow Orchestrated ELT Pipeline

```python
# Full ELT pipeline: S3 → Snowflake (raw) → dbt transforms
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

with DAG(
    "elt_pipeline",
    schedule_interval="0 2 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
) as dag:

    # E: Load raw files from S3 → Snowflake (COPY INTO)
    load_raw = SnowflakeOperator(
        task_id="load_raw_to_snowflake",
        snowflake_conn_id="snowflake_conn",
        sql="""
            COPY INTO RAW.ORDERS
            FROM @my_s3_stage/orders/date={{ ds }}/
            FILE_FORMAT = (TYPE = 'PARQUET')
            ON_ERROR = 'CONTINUE'
            PURGE = FALSE;
        """,
    )
    
    # L: Validate load
    validate_load = SnowflakeOperator(
        task_id="validate_raw_load",
        snowflake_conn_id="snowflake_conn",
        sql="""
            SELECT CASE WHEN COUNT(*) > 0 THEN 'PASS' ELSE 'FAIL' END AS status
            FROM RAW.ORDERS
            WHERE DATE(loaded_at) = '{{ ds }}'
        """,
    )
    
    # T: Run dbt transformations
    dbt_run = BashOperator(
        task_id="dbt_transform",
        bash_command=(
            "cd /opt/dbt/project && "
            "dbt run --models orders+ --vars '{run_date: {{ ds }}}' "
            "--profiles-dir /opt/dbt/profiles"
        ),
    )
    
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/dbt/project && dbt test --models orders+",
    )
    
    load_raw >> validate_load >> dbt_run >> dbt_test
```

---

## Problem 5: Multi-hop Medallion Pipeline

```python
# Full Medallion: Bronze → Silver → Gold with Airflow orchestration
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

with DAG(
    "medallion_pipeline",
    schedule_interval="0 4 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    ingest_bronze = SparkSubmitOperator(
        task_id="ingest_bronze",
        application="s3://code/spark/ingest_bronze.py",
        application_args=["--date", "{{ ds }}", "--source", "orders"],
        conf={"spark.executor.memory": "4g", "spark.executor.instances": "5"},
    )

    transform_silver = SparkSubmitOperator(
        task_id="bronze_to_silver",
        application="s3://code/spark/bronze_to_silver.py",
        application_args=["--date", "{{ ds }}"],
        conf={"spark.executor.memory": "8g", "spark.executor.instances": "10"},
    )

    aggregate_gold = SparkSubmitOperator(
        task_id="silver_to_gold",
        application="s3://code/spark/silver_to_gold.py",
        application_args=["--date", "{{ ds }}"],
    )

    quality_check = PythonOperator(
        task_id="gold_quality_check",
        python_callable=run_gold_quality_checks,
        op_kwargs={"date": "{{ ds }}"},
    )

    ingest_bronze >> transform_silver >> aggregate_gold >> quality_check
```

---

## Problem 6: Data Quality Pipeline

```python
# Dedicated DQ pipeline with Great Expectations
import great_expectations as gx
from great_expectations.checkpoint import Checkpoint

context = gx.get_context()

# Define expectations for orders table
def define_orders_expectations(context, suite_name: str):
    suite = context.create_expectation_suite(suite_name, overwrite_existing=True)
    validator = context.get_validator(
        datasource_name="my_spark_datasource",
        data_asset_name="orders",
        expectation_suite=suite,
    )
    
    validator.expect_column_to_exist("order_id")
    validator.expect_column_values_to_not_be_null("order_id")
    validator.expect_column_values_to_be_unique("order_id")
    validator.expect_column_values_to_be_between("amount", min_value=0, max_value=1_000_000)
    validator.expect_column_values_to_be_in_set("status", ["pending", "completed", "cancelled"])
    validator.expect_table_row_count_to_be_between(min_value=1000, max_value=10_000_000)
    
    validator.save_expectation_suite()
    return suite

# Run in Airflow
def run_great_expectations_checkpoint(date: str, **kwargs):
    results = context.run_checkpoint(
        checkpoint_name="orders_daily_checkpoint",
        batch_request={"runtime_parameters": {"query": f"SELECT * FROM orders WHERE date = '{date}'"}},
    )
    
    if not results["success"]:
        failed = [
            r["expectation_config"]["expectation_type"]
            for r in results["results"]
            if not r["success"]
        ]
        raise AirflowException(f"Great Expectations FAILED: {failed}")
    
    print("All DQ checks passed!")
```

---

## Problem 7: Reverse ETL Pipeline

```python
# Full Reverse ETL: Snowflake segment → Salesforce CRM sync

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd

def extract_segment_from_dw(**context):
    """Query Snowflake for customer segment updates."""
    from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
    hook = SnowflakeHook(snowflake_conn_id="snowflake_conn")
    
    df = hook.get_pandas_df("""
        SELECT 
            customer_id,
            email,
            ltv_score,
            segment,
            predicted_churn_probability,
            updated_at
        FROM GOLD.CUSTOMER_SEGMENTS
        WHERE DATE(updated_at) = '{{ ds }}'
        AND segment != prev_segment  -- only changed segments
    """)
    
    return df.to_dict("records")

def sync_to_salesforce(records: list, **context):
    """Upsert records to Salesforce via REST API."""
    from airflow.models import Variable
    
    sf_token = Variable.get("salesforce_access_token", deserialize_json=False)
    sf_instance = Variable.get("salesforce_instance_url")
    
    headers = {
        "Authorization": f"Bearer {sf_token}",
        "Content-Type": "application/json"
    }
    
    success_count, fail_count = 0, 0
    
    for rec in records:
        try:
            # Upsert using external ID (customer_id mapped to External_ID__c)
            response = requests.patch(
                f"{sf_instance}/services/data/v57.0/sobjects/Contact/External_ID__c/{rec['customer_id']}",
                json={
                    "LTV_Score__c": rec["ltv_score"],
                    "Segment__c": rec["segment"],
                    "Churn_Risk__c": rec["predicted_churn_probability"],
                },
                headers=headers
            )
            if response.status_code in (200, 201, 204):
                success_count += 1
            else:
                fail_count += 1
                print(f"Failed {rec['customer_id']}: {response.text}")
        except Exception as e:
            fail_count += 1
    
    print(f"Sync complete: {success_count} success, {fail_count} failures")

with DAG("reverse_etl_to_salesforce", schedule_interval="@daily", start_date=datetime(2024,1,1)) as dag:
    extract = PythonOperator(task_id="extract_segments", python_callable=extract_segment_from_dw)
    sync = PythonOperator(task_id="sync_to_salesforce", python_callable=sync_to_salesforce,
                          op_args=["{{ ti.xcom_pull(task_ids='extract_segments') }}"])
    extract >> sync
```

---

## Interview Quick Reference

### Common Interview Questions & Key Points

**Q: How do you ensure idempotency in a batch pipeline?**
> Delete the target partition before inserting. Use `overwrite` with dynamic partition mode in Spark. Use MERGE/UPSERT in databases. Never use plain APPEND.

**Q: What is watermarking in stream processing?**
> Watermarks define how long the engine waits for late-arriving data before finalizing a time window. `withWatermark("event_time", "10 minutes")` means windows won't be finalized until 10 minutes after the max event time seen.

**Q: ETL vs ELT — when to use each?**
> ETL when: sensitive data (transform before loading), limited DW compute, complex transformations. ELT when: modern cloud DW with cheap compute (BigQuery, Snowflake), dbt-based transformations, need to preserve raw data.

**Q: How do you handle late data in a streaming pipeline?**
> Use watermarks to define tolerance window. Use `append` output mode for finalized results. Store late events in a separate late-data topic for reprocessing if needed.

**Q: What's the difference between Lambda and Kappa architecture?**
> Lambda has two separate code paths (batch + streaming) which adds complexity but provides high accuracy. Kappa uses only streaming (single code path) with Kafka retention for replay — simpler but requires sufficient Kafka retention for historical reprocessing.

**Q: How do you backfill a daily pipeline 6 months retroactively?**
> Set `catchup=True` and `start_date` in Airflow. Use `max_active_runs` to limit concurrency. Ensure the pipeline is idempotent. Run `airflow dags backfill` CLI or trigger via Airflow UI with date range.

**Q: What metrics do you monitor for a production pipeline?**
> Freshness lag, record count (vs expected), error rate, task duration (vs SLA), DLQ size, null rates on critical columns, duplicate rate.

---

*End of Data Pipeline Design Complete Guide*
