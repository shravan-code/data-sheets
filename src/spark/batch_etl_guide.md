**BATCH ETL PIPELINE**

A-to-Z Guide

Python · Pandas · PySpark · PySpark Pandas · Databricks · PostgreSQL · AWS

Interview & Production Grade Examples | Pipeline Flows | Tech Stack

# **1\. Batch ETL Pipeline — Fundamentals**

## **1.1 What Is a Batch ETL Pipeline?**

A Batch ETL (Extract, Transform, Load) pipeline is a data engineering pattern that processes data in discrete, scheduled chunks rather than continuously. Data is collected over a time window, processed as a whole unit, and then persisted to a target system.

Three core phases:

* Extract: Read raw data from one or more source systems (databases, flat files, APIs, cloud storage).

* Transform: Clean, validate, enrich, aggregate, or reshape the data using business logic.

* Load: Write the processed data to a destination (data warehouse, data lake, database, file system).

## **1.2 Batch vs Streaming — When to Use Batch**

| Criterion | Batch ETL |
| :---- | :---- |
| Latency | Minutes to hours (acceptable delay) |
| Data volume | Very large historical datasets |
| Complexity | Complex multi-step transformations |
| Cost | Lower — compute spun up on schedule |
| Use cases | Reporting, BI dashboards, nightly loads, ML training |
| Trigger | Schedule (cron), event (file arrival), manual |

## **1.3 Common Batch Pipeline Architecture**

A typical production batch pipeline consists of:

1. Source systems: OLTP databases, REST APIs, S3/GCS/ADLS, Kafka compacted topics.

2. Orchestration layer: Apache Airflow, Prefect, Dagster, AWS Step Functions.

3. Compute layer: Python scripts, PySpark on Databricks/EMR/GKE, dbt.

4. Storage layer: PostgreSQL, Redshift, BigQuery, Snowflake, Delta Lake, Parquet on S3.

5. Monitoring: Great Expectations, Soda, custom alerting via PagerDuty/Slack.

## **1.4 Key Concepts**

* Idempotency: Running the same pipeline twice produces the same result — essential for safe reruns.

* Incremental loading: Only process new or changed records (watermark/CDC-based).

* Full refresh: Truncate and reload the entire target table on each run.

* Partitioning: Split data by date/key to allow parallel processing and partition pruning.

* Data quality: Schema validation, null checks, deduplication, referential integrity.

* Lineage & observability: Track what data came from where and when.

* SLA management: Define completion deadlines and alert on breaches.

# **2\. Batch ETL Pipeline Using Pure Python**

## **2.1 Overview & Pipeline Flow**

| Pipeline Flow CSV / API / PostgreSQL  ──►  Python ETL Script  ──►  PostgreSQL / JSON / CSV  (extract.py)                (transform.py)            (load.py)                    Orchestrated by: cron / Airflow |
| :---- |

Pure Python pipelines use only the standard library plus lightweight third-party packages (requests, psycopg2, csv, json, sqlite3). Ideal when PySpark is overkill and data fits in memory.

## **2.2 Tech Stack**

| Component | Technology |
| :---- | :---- |
| Language | Python 3.10+ |
| Data I/O | csv, json, requests, boto3 |
| Database | psycopg2 (PostgreSQL), sqlite3 |
| Scheduling | cron / Apache Airflow PythonOperator |
| Logging | Python logging module |
| Config | python-dotenv / os.environ |

## **2.3 Example 1 — CSV → Transform → PostgreSQL**

### **Scenario**

A retail company receives a daily sales CSV from an SFTP server. We extract it, clean/transform the records, and load into a PostgreSQL sales\_fact table.

### **Pipeline Flow**

| Detailed Flow Step 1: Read sales\_YYYYMMDD.csv from /data/raw/Step 2: Validate schema (check required columns exist)Step 3: Clean data (strip whitespace, cast types, remove nulls)Step 4: Enrich (add etl\_run\_date, derive revenue \= qty \* unit\_price)Step 5: Deduplicate (on order\_id)Step 6: UPSERT into PostgreSQL sales\_factStep 7: Log record counts & write audit row |
| :---- |

### **config.py**

import os

from dotenv import load\_dotenv

load\_dotenv()

DB\_CONFIG \= {

    'host': os.getenv('PG\_HOST', 'localhost'),

    'port': int(os.getenv('PG\_PORT', 5432)),

    'dbname': os.getenv('PG\_DB', 'warehouse'),

    'user': os.getenv('PG\_USER', 'etl\_user'),

    'password': os.getenv('PG\_PASSWORD'),

}

RAW\_PATH  \= os.getenv('RAW\_PATH', '/data/raw')

STAGE\_PATH \= os.getenv('STAGE\_PATH', '/data/stage')

### **extract.py**

import csv, os, logging

from datetime import date

from config import RAW\_PATH

logger \= logging.getLogger(\_\_name\_\_)

EXPECTED\_COLS \= {'order\_id','order\_date','product\_id',

                 'quantity','unit\_price','customer\_id'}

def extract\_sales(run\_date: str \= None) \-\> list\[dict\]:

    run\_date \= run\_date or date.today().strftime('%Y%m%d')

    filepath \= os.path.join(RAW\_PATH, f'sales\_{run\_date}.csv')

    if not os.path.exists(filepath):

        raise FileNotFoundError(f'Source file not found: {filepath}')

    rows \= \[\]

    with open(filepath, newline='', encoding='utf-8') as f:

        reader \= csv.DictReader(f)

        cols \= set(reader.fieldnames or \[\])

        missing \= EXPECTED\_COLS \- cols

        if missing:

            raise ValueError(f'Missing columns: {missing}')

        for row in reader:

            rows.append(dict(row))

    logger.info(f'Extracted {len(rows)} rows from {filepath}')

    return rows

### **transform.py**

import logging

from datetime import datetime

logger \= logging.getLogger(\_\_name\_\_)

def transform\_sales(rows: list\[dict\]) \-\> list\[dict\]:

    cleaned, skipped \= \[\], 0

    seen\_ids \= set()

    for row in rows:

        \# 1\. Strip whitespace

        row \= {k: v.strip() for k, v in row.items()}

        \# 2\. Skip rows with null critical fields

        if not all(\[row.get('order\_id'), row.get('quantity'),

                    row.get('unit\_price')\]):

            skipped \+= 1

            continue

        \# 3\. Type casting

        try:

            qty   \= int(row\['quantity'\])

            price \= float(row\['unit\_price'\])

        except ValueError:

            skipped \+= 1

            continue

        \# 4\. Deduplication

        order\_id \= row\['order\_id'\]

        if order\_id in seen\_ids:

            skipped \+= 1

            continue

        seen\_ids.add(order\_id)

        \# 5\. Derived fields

        cleaned.append({

            'order\_id':    order\_id,

            'order\_date':  row\['order\_date'\],

            'product\_id':  row\['product\_id'\],

            'customer\_id': row\['customer\_id'\],

            'quantity':    qty,

            'unit\_price':  price,

            'revenue':     round(qty \* price, 2),

            'etl\_run\_date': datetime.utcnow().isoformat(),

        })

    logger.info(f'Transformed: {len(cleaned)} clean, {skipped} skipped')

    return cleaned

### **load.py**

import psycopg2, psycopg2.extras, logging

from config import DB\_CONFIG

logger \= logging.getLogger(\_\_name\_\_)

UPSERT\_SQL \= '''

    INSERT INTO sales\_fact

        (order\_id, order\_date, product\_id, customer\_id,

         quantity, unit\_price, revenue, etl\_run\_date)

    VALUES %s

    ON CONFLICT (order\_id) DO UPDATE SET

        quantity     \= EXCLUDED.quantity,

        unit\_price   \= EXCLUDED.unit\_price,

        revenue      \= EXCLUDED.revenue,

        etl\_run\_date \= EXCLUDED.etl\_run\_date;

'''

def load\_sales(records: list\[dict\]) \-\> int:

    if not records:

        logger.warning('No records to load.')

        return 0

    cols \= ('order\_id','order\_date','product\_id','customer\_id',

            'quantity','unit\_price','revenue','etl\_run\_date')

    values \= \[tuple(r\[c\] for c in cols) for r in records\]

    with psycopg2.connect(\*\*DB\_CONFIG) as conn:

        with conn.cursor() as cur:

            psycopg2.extras.execute\_values(cur, UPSERT\_SQL, values, page\_size=500)

            conn.commit()

    logger.info(f'Loaded {len(values)} rows into sales\_fact')

    return len(values)

### **pipeline.py — Orchestrator**

import logging, sys

from extract import extract\_sales

from transform import transform\_sales

from load import load\_sales

logging.basicConfig(

    level=logging.INFO,

    format='%(asctime)s %(levelname)s %(name)s \- %(message)s'

)

logger \= logging.getLogger('pipeline')

def run\_pipeline(run\_date: str \= None):

    logger.info(f'=== Pipeline START run\_date={run\_date} \===')

    try:

        raw     \= extract\_sales(run\_date)

        clean   \= transform\_sales(raw)

        loaded  \= load\_sales(clean)

        logger.info(f'=== Pipeline DONE: {loaded} rows loaded \===')

    except Exception as e:

        logger.exception(f'Pipeline FAILED: {e}')

        sys.exit(1)

if \_\_name\_\_ \== '\_\_main\_\_':

    import argparse

    parser \= argparse.ArgumentParser()

    parser.add\_argument('--date', default=None)

    args \= parser.parse\_args()

    run\_pipeline(args.date)

## **2.4 Example 2 — REST API → Transform → PostgreSQL**

### **Scenario**

Pull order data from an external REST API with pagination, transform it, and load into a staging table. Demonstrates incremental loading with a watermark.

### **Pipeline Flow**

| Flow PostgreSQL (read watermark) → REST API (paginated) → Transform → PostgreSQL (write \+ update watermark) |
| :---- |

### **api\_extract.py — Paginated REST API Extraction**

import requests, time, logging

logger \= logging.getLogger(\_\_name\_\_)

BASE\_URL \= 'https://api.example.com/v1/orders'

API\_KEY  \= 'Bearer \<TOKEN\>'

def fetch\_orders\_since(since\_ts: str, page\_size: int \= 100\) \-\> list\[dict\]:

    headers \= {'Authorization': API\_KEY, 'Accept': 'application/json'}

    all\_records, page \= \[\], 1

    while True:

        params \= {'since': since\_ts, 'page': page, 'per\_page': page\_size}

        resp \= requests.get(BASE\_URL, headers=headers, params=params, timeout=30)

        resp.raise\_for\_status()

        data \= resp.json()

        records \= data.get('orders', \[\])

        if not records:

            break

        all\_records.extend(records)

        logger.info(f'Page {page}: {len(records)} records')

        if not data.get('has\_more', False):

            break

        page \+= 1

        time.sleep(0.2)   \# rate-limit safety

    logger.info(f'Total extracted: {len(all\_records)}')

    return all\_records

### **watermark.py — Incremental State Management**

import psycopg2, logging

from config import DB\_CONFIG

logger \= logging.getLogger(\_\_name\_\_)

def get\_watermark(pipeline\_name: str) \-\> str:

    with psycopg2.connect(\*\*DB\_CONFIG) as conn:

        with conn.cursor() as cur:

            cur.execute(

                'SELECT last\_run\_ts FROM etl\_watermarks WHERE pipeline=%s',

                (pipeline\_name,)

            )

            row \= cur.fetchone()

            return row\[0\].isoformat() if row else '1970-01-01T00:00:00'

def update\_watermark(pipeline\_name: str, new\_ts: str):

    with psycopg2.connect(\*\*DB\_CONFIG) as conn:

        with conn.cursor() as cur:

            cur.execute('''

                INSERT INTO etl\_watermarks (pipeline, last\_run\_ts)

                VALUES (%s, %s)

                ON CONFLICT (pipeline) DO UPDATE

                SET last\_run\_ts \= EXCLUDED.last\_run\_ts;

            ''', (pipeline\_name, new\_ts))

            conn.commit()

## **2.5 Interview Questions — Pure Python ETL**

| Question | Answer / Key Points |
| :---- | :---- |
| How do you ensure idempotency? | Use UPSERT (ON CONFLICT), watermark table to track progress, run-id deduplication. |
| How do you handle API rate limits? | Exponential backoff, respect Retry-After headers, add sleep between pages. |
| How would you backfill 2 years of data? | Parameterize pipeline with date range, run in parallel chunks (e.g. monthly), use \--date arg. |
| How do you handle partial failures? | Commit in batches with checkpoints; on re-run replay only failed batches using watermark. |
| How do you test your pipeline? | Unit test transform logic with pytest, mock DB/API calls, integration test with local PG \+ fixtures. |

# **3\. Batch ETL Pipeline Using Python Pandas**

## **3.1 Overview**

Pandas is the standard for in-memory tabular data processing in Python. It excels for datasets that fit comfortably in RAM (roughly \< 10 GB). Pandas DataFrames provide SQL-like operations with a rich API for cleaning, aggregating, and reshaping data.

## **3.2 Tech Stack**

| Component | Technology |
| :---- | :---- |
| Core library | pandas 2.x |
| Database I/O | SQLAlchemy \+ psycopg2, pandas.read\_sql / to\_sql |
| File I/O | pandas CSV, Parquet (pyarrow), Excel (openpyxl) |
| AWS S3 | s3fs / boto3 (read\_parquet / to\_parquet with s3:// paths) |
| Scheduling | Airflow / cron |
| Data quality | Great Expectations / custom assertions |

## **3.3 Example 1 — Multi-Source Join ETL: Orders \+ Products \+ Customers**

### **Scenario**

Combine three daily CSVs (orders, products, customers) from S3 into a single denormalized fact table in PostgreSQL. Apply business rules, aggregate by customer, and write the result.

### **Pipeline Flow**

| Flow S3: orders.csv \+ products.csv \+ customers.csv         ▼  pandas.read\_csv with s3fs   Validate schemas & data quality         ▼  merge / join  Derive fields: revenue, discount\_applied, customer\_tier         ▼  aggregate to customer\_daily\_summary  PostgreSQL: customer\_daily\_summary (UPSERT) |
| :---- |

### **pandas\_etl.py — Full Pipeline**

import pandas as pd

import numpy as np

from sqlalchemy import create\_engine, text

import logging, os

from datetime import date

logger \= logging.getLogger(\_\_name\_\_)

ENGINE  \= create\_engine(os.getenv('DB\_URL'))

S3\_BASE \= 's3://my-data-lake/raw'

\# ── EXTRACT ──────────────────────────────────────────────

def extract(run\_date: str) \-\> tuple\[pd.DataFrame, pd.DataFrame, pd.DataFrame\]:

    orders   \= pd.read\_csv(f'{S3\_BASE}/orders/dt={run\_date}/orders.csv')

    products \= pd.read\_csv(f'{S3\_BASE}/products/products\_master.csv')

    customers= pd.read\_csv(f'{S3\_BASE}/customers/customers\_master.csv')

    logger.info(f'orders={len(orders)}, products={len(products)}, customers={len(customers)}')

    return orders, products, customers

\# ── VALIDATE ─────────────────────────────────────────────

def validate(df: pd.DataFrame, required\_cols: list, name: str):

    missing \= set(required\_cols) \- set(df.columns)

    if missing:

        raise ValueError(f'{name}: missing columns {missing}')

    null\_pct \= df\[required\_cols\].isnull().mean()

    bad \= null\_pct\[null\_pct \> 0.05\]

    if not bad.empty:

        raise ValueError(f'{name}: high null rate: {bad.to\_dict()}')

\# ── TRANSFORM ────────────────────────────────────────────

def transform(orders: pd.DataFrame, products: pd.DataFrame,

              customers: pd.DataFrame) \-\> pd.DataFrame:

    \# Validate

    validate(orders,   \['order\_id','customer\_id','product\_id','quantity','unit\_price'\], 'orders')

    validate(customers,\['customer\_id','customer\_name','country','signup\_date'\], 'customers')

    validate(products, \['product\_id','category','cost\_price'\], 'products')

    \# Clean types

    orders\['order\_date'\] \= pd.to\_datetime(orders\['order\_date'\], errors='coerce')

    orders\['quantity'\]   \= pd.to\_numeric(orders\['quantity'\],   errors='coerce')

    orders\['unit\_price'\] \= pd.to\_numeric(orders\['unit\_price'\], errors='coerce')

    orders \= orders.dropna(subset=\['order\_date','quantity','unit\_price'\])

    orders \= orders.drop\_duplicates(subset=\['order\_id'\])

    \# Join enrichment

    df \= orders.merge(products\[\['product\_id','category','cost\_price'\]\],

                      on='product\_id', how='left')

    df \= df.merge(customers\[\['customer\_id','customer\_name','country','signup\_date'\]\],

                  on='customer\_id', how='left')

    \# Derived fields

    df\['revenue'\]        \= (df\['quantity'\] \* df\['unit\_price'\]).round(2)

    df\['gross\_profit'\]   \= (df\['revenue'\] \- df\['quantity'\] \* df\['cost\_price'\]).round(2)

    df\['margin\_pct'\]     \= ((df\['gross\_profit'\] / df\['revenue'\]) \* 100).round(1)

    df\['discount\_applied'\] \= df\['unit\_price'\] \< df\['cost\_price'\] \* 1.05

    \# Customer tier

    lifetime \= df.groupby('customer\_id')\['revenue'\].sum().rename('lifetime\_rev')

    df \= df.merge(lifetime, on='customer\_id', how='left')

    df\['customer\_tier'\] \= pd.cut(

        df\['lifetime\_rev'\],

        bins=\[0, 500, 2000, 10000, np.inf\],

        labels=\['Bronze','Silver','Gold','Platinum'\]

    ).astype(str)

    \# Aggregate to customer\_daily\_summary

    agg \= df.groupby(\['customer\_id','customer\_name','country',

                      'customer\_tier', orders\['order\_date'\].dt.date\]).agg(

        orders\_count  \= ('order\_id',   'count'),

        total\_revenue \= ('revenue',    'sum'),

        total\_profit  \= ('gross\_profit','sum'),

        avg\_margin    \= ('margin\_pct', 'mean'),

    ).reset\_index()

    agg.columns.name \= None

    agg\['etl\_run\_ts'\] \= pd.Timestamp.utcnow()

    logger.info(f'Transformed into {len(agg)} customer-day rows')

    return agg

\# ── LOAD ─────────────────────────────────────────────────

def load(df: pd.DataFrame, table: str \= 'customer\_daily\_summary'):

    \# Write to staging then swap

    stage \= f'{table}\_stage'

    df.to\_sql(stage, ENGINE, if\_exists='replace', index=False,

              method='multi', chunksize=1000)

    with ENGINE.begin() as conn:

        conn.execute(text(f'DELETE FROM {table} USING {stage} s '

            f'WHERE {table}.customer\_id=s.customer\_id AND {table}.order\_date=s.order\_date'))

        conn.execute(text(f'INSERT INTO {table} SELECT \* FROM {stage}'))

        conn.execute(text(f'DROP TABLE {stage}'))

    logger.info(f'Loaded {len(df)} rows into {table}')

\# ── MAIN ─────────────────────────────────────────────────

def run(run\_date: str \= None):

    run\_date \= run\_date or date.today().isoformat()

    orders, products, customers \= extract(run\_date)

    result \= transform(orders, products, customers)

    load(result)

if \_\_name\_\_ \== '\_\_main\_\_':

    import sys

    run(sys.argv\[1\] if len(sys.argv) \> 1 else None)

## **3.4 Example 2 — Pandas on AWS S3: Parquet-Based Data Lake ETL**

### **Scenario**

Read partitioned Parquet files from S3 (raw zone), apply transformations, and write to the curated zone as Parquet, partitioned by year/month for efficient querying.

### **Pipeline Flow**

| Flow S3://raw/events/dt=YYYY-MM-DD/  (Parquet files)        ▼  pd.read\_parquet with s3fs  Filter invalid records, extract session features        ▼  aggregate to session-level metricsS3://curated/sessions/year=YYYY/month=MM/  (Parquet, snappy) |
| :---- |

### **s3\_parquet\_etl.py**

import pandas as pd

import s3fs, logging

from datetime import datetime

logger \= logging.getLogger(\_\_name\_\_)

fs \= s3fs.S3FileSystem()

RAW\_BUCKET     \= 's3://my-lake/raw/events'

CURATED\_BUCKET \= 's3://my-lake/curated/sessions'

def extract\_parquet(run\_date: str) \-\> pd.DataFrame:

    path \= f'{RAW\_BUCKET}/dt={run\_date}/'

    files \= fs.ls(path)

    if not files:

        raise ValueError(f'No parquet files at {path}')

    df \= pd.read\_parquet(f's3://{path}', filesystem=fs, engine='pyarrow')

    logger.info(f'Read {len(df)} rows from {path}')

    return df

def transform\_events(df: pd.DataFrame) \-\> pd.DataFrame:

    df\['event\_time'\] \= pd.to\_datetime(df\['event\_time'\], utc=True, errors='coerce')

    df \= df.dropna(subset=\['session\_id','user\_id','event\_time'\])

    df \= df.sort\_values(\['session\_id','event\_time'\])

    agg \= df.groupby(\['session\_id','user\_id'\]).agg(

        session\_start   \= ('event\_time', 'min'),

        session\_end     \= ('event\_time', 'max'),

        event\_count     \= ('event\_type', 'count'),

        unique\_pages    \= ('page\_url',   'nunique'),

        first\_event     \= ('event\_type', 'first'),

        last\_event      \= ('event\_type', 'last'),

    ).reset\_index()

    agg\['duration\_seconds'\] \= (

        agg\['session\_end'\] \- agg\['session\_start'\]

    ).dt.total\_seconds().round(1)

    agg\['bounced'\] \= agg\['event\_count'\] \== 1

    agg\['year'\]    \= agg\['session\_start'\].dt.year

    agg\['month'\]   \= agg\['session\_start'\].dt.month

    return agg

def write\_curated(df: pd.DataFrame):

    df.to\_parquet(

        CURATED\_BUCKET,

        engine='pyarrow',

        compression='snappy',

        partition\_cols=\['year','month'\],

        filesystem=fs,

        existing\_data\_behavior='delete\_matching',  \# overwrite same partitions

    )

    logger.info(f'Written {len(df)} session rows to {CURATED\_BUCKET}')

def run(run\_date: str):

    raw       \= extract\_parquet(run\_date)

    sessions  \= transform\_events(raw)

    write\_curated(sessions)

## **3.5 Interview Questions — Pandas ETL**

| Question | Answer / Key Points |
| :---- | :---- |
| How do you handle OOM with Pandas? | Use chunked reading (chunksize param), Dask, or switch to PySpark for truly large data. |
| How do you do efficient UPSERT with Pandas? | Write to stage table via to\_sql, then use SQL MERGE/UPSERT in the database engine. |
| How do you avoid re-processing files? | Track processed file keys in a manifest table or S3 metadata; compare on each run. |
| Why use Parquet over CSV? | Columnar storage, compression (2-5x smaller), schema enforcement, 10-100x faster reads. |
| How do you unit test a Pandas transform? | Create small fixture DataFrames, call the function, assert output shape/values with pytest. |

# **4\. Batch ETL Pipeline Using PySpark**

## **4.1 Overview**

Apache Spark is a distributed compute engine for processing data at scale — from GBs to petabytes. PySpark is the Python API for Spark. It runs on Databricks, AWS EMR, GCP Dataproc, or self-managed clusters.

Key Spark concepts every engineer must know:

* RDD (Resilient Distributed Dataset): Fault-tolerant distributed collection. Low-level API.

* DataFrame: High-level tabular API with SQL-like operations. Backed by Catalyst optimizer.

* Transformations vs Actions: Transformations (filter, select, join) are lazy; actions (show, count, write) trigger execution.

* Partitions: Unit of parallelism. More partitions \= more parallelism (up to a point).

* DAG (Directed Acyclic Graph): Spark builds a logical plan of transformations before executing.

* Shuffle: Expensive data redistribution across nodes (caused by groupBy, join, distinct).

## **4.2 Tech Stack**

| Component | Technology |
| :---- | :---- |
| Compute | PySpark 3.x on Databricks / AWS EMR / local |
| Storage | Delta Lake / Parquet on S3 or ADLS |
| Database sink | Delta tables / JDBC (PostgreSQL, Redshift) |
| Orchestration | Databricks Workflows / Airflow SparkSubmitOperator |
| Data quality | Great Expectations with Spark backend |
| Catalog | Unity Catalog / AWS Glue / Hive Metastore |

## **4.3 Example 1 — Large-Scale Log Processing ETL**

### **Scenario**

Process 500 million web server log records stored as gzipped JSON on S3. Parse, clean, aggregate to hourly metrics, and write to Delta Lake.

### **Pipeline Flow**

| Flow S3://raw/logs/year=\*/month=\*/day=\*/  (gzip JSON, \~2 TB)        ▼  spark.read.json (schema inference off, manual schema)  Parse user\_agent, extract UTM params, validate IPs        ▼  repartition by hour  Aggregate: requests/hr, unique users/hr, error\_rate, p95\_latency        ▼  Delta MERGE (incremental upsert)  Delta: s3://curated/hourly\_metrics/  (Z-ordered by hour) |
| :---- |

### **schema.py — Explicit Schema Definition**

from pyspark.sql.types import \*

LOG\_SCHEMA \= StructType(\[

    StructField('timestamp',    StringType(),  True),

    StructField('method',       StringType(),  True),

    StructField('path',         StringType(),  True),

    StructField('status\_code',  IntegerType(), True),

    StructField('response\_ms',  DoubleType(),  True),

    StructField('ip\_address',   StringType(),  True),

    StructField('user\_agent',   StringType(),  True),

    StructField('session\_id',   StringType(),  True),

    StructField('user\_id',      StringType(),  True),

    StructField('utm\_source',   StringType(),  True),

    StructField('bytes\_sent',   LongType(),    True),

\])

### **pyspark\_logs\_etl.py**

from pyspark.sql import SparkSession

from pyspark.sql import functions as F

from pyspark.sql.window import Window

from delta.tables import DeltaTable

from schema import LOG\_SCHEMA

spark \= SparkSession.builder \\

    .appName('log\_etl') \\

    .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \\

    .config('spark.sql.catalog.spark\_catalog',

            'org.apache.spark.sql.delta.catalog.DeltaCatalog') \\

    .config('spark.sql.adaptive.enabled', 'true') \\

    .config('spark.sql.shuffle.partitions', '400') \\

    .getOrCreate()

RAW\_PATH    \= 's3://my-lake/raw/logs'

DELTA\_PATH  \= 's3://my-lake/curated/hourly\_metrics'

\# ── EXTRACT ──────────────────────────────────────────────

def extract(run\_date: str):

    path \= f'{RAW\_PATH}/dt={run\_date}/'

    df \= spark.read.schema(LOG\_SCHEMA).json(path)

    df \= df.withColumn('ts', F.to\_timestamp('timestamp')) \\

           .filter(F.col('ts').isNotNull())

    print(f'Extracted {df.count()} rows')

    return df

\# ── TRANSFORM ────────────────────────────────────────────

def transform(df):

    \# Derive time parts

    df \= df.withColumn('hour',    F.date\_trunc('hour', 'ts')) \\

           .withColumn('is\_error',F.col('status\_code') \>= 400\) \\

           .withColumn('is\_bot',

               F.lower('user\_agent').rlike('bot|crawler|spider'))

    \# Filter bots and nulls

    df \= df.filter(\~F.col('is\_bot'))

    df \= df.filter(F.col('ip\_address').isNotNull())

    \# Compute p95 latency via approx percentile

    agg \= df.groupBy('hour').agg(

        F.count('\*').alias('total\_requests'),

        F.approx\_count\_distinct('user\_id').alias('unique\_users'),

        F.approx\_count\_distinct('session\_id').alias('unique\_sessions'),

        F.sum(F.col('is\_error').cast('int')).alias('error\_count'),

        F.mean('response\_ms').alias('avg\_latency\_ms'),

        F.expr('percentile\_approx(response\_ms, 0.95)').alias('p95\_latency\_ms'),

        F.sum('bytes\_sent').alias('total\_bytes'),

    )

    agg \= agg.withColumn('error\_rate',

        (F.col('error\_count') / F.col('total\_requests') \* 100).round(2))

    agg \= agg.withColumn('etl\_ts', F.current\_timestamp())

    return agg

\# ── LOAD (Delta MERGE) ────────────────────────────────────

def load\_delta(df):

    if DeltaTable.isDeltaTable(spark, DELTA\_PATH):

        delta \= DeltaTable.forPath(spark, DELTA\_PATH)

        delta.alias('target').merge(

            df.alias('source'),

            'target.hour \= source.hour'

        ).whenMatchedUpdateAll()

         .whenNotMatchedInsertAll()

         .execute()

    else:

        df.write.format('delta').partitionBy('hour') \\

          .mode('overwrite').save(DELTA\_PATH)

    print(f'Delta MERGE complete. Path: {DELTA\_PATH}')

\# ── OPTIMIZE (Z-Order) ────────────────────────────────────

def optimize():

    spark.sql(f"OPTIMIZE delta.\`{DELTA\_PATH}\` ZORDER BY (hour)")

def run(run\_date: str):

    raw     \= extract(run\_date)

    result  \= transform(raw)

    load\_delta(result)

    optimize()

## **4.4 Example 2 — SCD Type 2 Dimension Table**

### **Scenario**

Implement a Slowly Changing Dimension (Type 2\) for a customers table using PySpark and Delta Lake. New records are inserted; changed records create a new version with a valid\_from/valid\_to date range.

### **Pipeline Flow**

| Flow Source: PostgreSQL customers table (daily snapshot)        ▼  Read via JDBC  Compute hash of tracked columns (name, email, address)        ▼  Compare hash with current active Delta records  MERGE: close old versions (set valid\_to), insert new versions  Delta: dim\_customers (SCD2) |
| :---- |

### **scd2\_pyspark.py**

from pyspark.sql import SparkSession, functions as F

from delta.tables import DeltaTable

spark \= SparkSession.builder.appName('scd2').getOrCreate()

DIM\_PATH \= 's3://warehouse/dimensions/dim\_customers'

JDBC\_URL \= 'jdbc:postgresql://host:5432/crm'

JDBC\_OPT \= {'user':'etl','password':'secret','driver':'org.postgresql.Driver'}

def read\_source():

    return spark.read.jdbc(JDBC\_URL, 'customers', properties=JDBC\_OPT) \\

               .withColumn('record\_hash',

                   F.md5(F.concat\_ws('|','name','email','address','country')))

def apply\_scd2(source):

    today \= F.lit(F.current\_date())

    far\_future \= F.lit('9999-12-31').cast('date')

    if not DeltaTable.isDeltaTable(spark, DIM\_PATH):

        source.withColumn('valid\_from', today) \\

              .withColumn('valid\_to', far\_future) \\

              .withColumn('is\_current', F.lit(True)) \\

              .write.format('delta').save(DIM\_PATH)

        return

    dim \= DeltaTable.forPath(spark, DIM\_PATH)

    \# Identify changed rows

    current \= dim.toDF().filter('is\_current \= true')

    changes \= source.alias('s').join(

        current.alias('t'), on='customer\_id', how='left'

    ).filter(

        F.col('t.customer\_id').isNull() |

        (F.col('s.record\_hash') \!= F.col('t.record\_hash'))

    ).select('s.\*')

    \# Stage: new rows to insert

    new\_rows \= changes \\

        .withColumn('valid\_from', today) \\

        .withColumn('valid\_to', far\_future) \\

        .withColumn('is\_current', F.lit(True))

    \# MERGE: expire old, insert new

    dim.alias('target').merge(

        new\_rows.alias('source'),

        'target.customer\_id \= source.customer\_id AND target.is\_current \= true'

    ).whenMatchedUpdate(set={

        'valid\_to':   F.current\_date(),

        'is\_current': F.lit(False)

    }).whenNotMatchedInsertAll().execute()

def run():

    source \= read\_source()

    apply\_scd2(source)

    print('SCD2 merge complete')

## **4.5 PySpark Performance Tuning Concepts**

* Broadcast joins: Use F.broadcast(small\_df) for tables \< 10 MB to avoid shuffle.

* Repartition vs Coalesce: repartition() does full shuffle (increase partitions); coalesce() reduces without shuffle.

* Caching: Use df.cache() or df.persist() for DataFrames reused multiple times.

* AQE (Adaptive Query Execution): Enabled by default in Spark 3; auto-optimizes joins and skew handling.

* Skew handling: Use spark.sql.adaptive.skewJoin.enabled=true or salting techniques.

* Partition pruning: Filter on partition columns early; Spark skips irrelevant files.

## **4.6 Interview Questions — PySpark ETL**

| Question | Answer / Key Points |
| :---- | :---- |
| Explain lazy evaluation. | Spark builds a DAG of transformations but only executes when an action is called. Allows Catalyst optimizer to reorder and prune. |
| What causes shuffle and how to minimize? | groupBy, join, distinct, repartition. Minimize with broadcast joins, pre-partitioning on join key, AQE. |
| How do you handle data skew? | Salting the skewed key, splitting into two joins, or enabling spark.sql.adaptive.skewJoin.enabled. |
| What is a Delta Lake MERGE? | Atomic upsert using MERGE INTO; ensures ACID compliance. Used for SCD2, deduplication, CDC application. |
| How do you tune shuffle partitions? | Set spark.sql.shuffle.partitions; rule of thumb: 128 MB per partition. Use AQE for dynamic sizing. |

# **5\. PySpark Pandas (Pandas API on Spark)**

## **5.1 What Is PySpark Pandas?**

PySpark Pandas (formerly Koalas, now merged into PySpark 3.2+ as pyspark.pandas) provides a pandas-compatible API on top of Spark. Engineers familiar with Pandas can scale their code to distributed data with minimal changes.

Import: import pyspark.pandas as ps  (replaces import pandas as pd)

| Aspect | Detail |
| :---- | :---- |
| Module | pyspark.pandas (PySpark 3.2+) |
| Compatibility | \~80-90% of pandas API |
| Best for | Teams migrating pandas code to Spark scale |
| Caveats | Some operations trigger full shuffle; different from native Spark performance |
| Config | ps.set\_option('compute.ops\_on\_diff\_frames', True) for cross-frame ops |

## **5.2 Pandas vs PySpark Pandas — Side by Side**

| Operation | PySpark Pandas (same syntax) |
| :---- | :---- |
| Read CSV | ps.read\_csv('s3://...') |
| Filter | df\[df\['revenue'\] \> 100\] |
| GroupBy agg | df.groupby('region')\['revenue'\].sum() |
| Merge/Join | df1.merge(df2, on='id', how='left') |
| Apply UDF | df\['col'\].apply(my\_func)  ← runs distributed |
| Write Parquet | df.to\_parquet('s3://...') |

## **5.3 Example — Customer Churn Feature Engineering at Scale**

### **Scenario**

Build an ML feature table for 200M customer records by computing RFM (Recency, Frequency, Monetary) features using PySpark Pandas. The code looks nearly identical to Pandas but runs on a 20-node Databricks cluster.

### **Pipeline Flow**

| Flow Delta: transactions table (200M rows)        ▼  ps.read\_delta (PySpark Pandas)  Filter last 12 months        ▼  groupby customer\_id  Compute: recency (days since last txn), frequency, monetary        ▼  percentile rank into RFM segments  Delta: ml\_features.rfm\_segments |
| :---- |

### **rfm\_features.py**

import pyspark.pandas as ps

from pyspark.sql import SparkSession

import pandas as pd

from datetime import date, timedelta

spark \= SparkSession.builder.appName('rfm\_features').getOrCreate()

ps.set\_option('compute.ops\_on\_diff\_frames', True)

TXNS\_PATH    \= 'dbfs:/mnt/delta/transactions'

FEATURES\_PATH= 'dbfs:/mnt/delta/ml\_features/rfm'

def compute\_rfm():

    today \= date.today()

    cutoff \= today \- timedelta(days=365)

    \# Read from Delta using PySpark Pandas

    txns \= ps.read\_delta(TXNS\_PATH)

    txns\['txn\_date'\] \= ps.to\_datetime(txns\['txn\_date'\])

    \# Filter last 12 months

    txns \= txns\[txns\['txn\_date'\] \>= str(cutoff)\]

    txns \= txns\[txns\['amount'\] \> 0\]

    txns \= txns.dropna(subset=\['customer\_id','amount','txn\_date'\])

    \# Compute RFM

    rfm \= txns.groupby('customer\_id').agg(

        last\_txn\_date \= ('txn\_date', 'max'),

        frequency     \= ('txn\_id', 'count'),

        monetary      \= ('amount', 'sum'),

    ).reset\_index()

    rfm\['recency\_days'\] \= (

        ps.to\_datetime(str(today)) \- rfm\['last\_txn\_date'\]

    ).dt.days

    rfm\['monetary'\] \= rfm\['monetary'\].round(2)

    \# Quantile-based RFM scoring (1-4)

    rfm\['R'\] \= ps.qcut(rfm\['recency\_days'\],  4, labels=\[4,3,2,1\]).astype(int)

    rfm\['F'\] \= ps.qcut(rfm\['frequency'\],      4, labels=\[1,2,3,4\]).astype(int)

    rfm\['M'\] \= ps.qcut(rfm\['monetary'\],        4, labels=\[1,2,3,4\]).astype(int)

    rfm\['rfm\_score'\] \= rfm\['R'\] \+ rfm\['F'\] \+ rfm\['M'\]

    rfm\['segment'\] \= ps.cut(

        rfm\['rfm\_score'\],

        bins=\[0, 4, 7, 9, 12\],

        labels=\['At Risk','Promising','Loyal','Champion'\]

    ).astype(str)

    \# Write back to Delta

    rfm.to\_delta(FEATURES\_PATH, mode='overwrite')

    print(f'RFM features written for {len(rfm)} customers')

    return rfm

if \_\_name\_\_ \== '\_\_main\_\_':

    compute\_rfm()

## **5.4 When to Use PySpark Pandas vs Native PySpark**

| Scenario | Recommendation |
| :---- | :---- |
| Migrating existing pandas code | PySpark Pandas — minimal changes |
| Net-new large-scale pipeline | Native PySpark — full control, better performance |
| Complex windowing / ranking | Native PySpark (Window API) |
| Quick prototyping at scale | PySpark Pandas |
| Production critical performance | Native PySpark \+ Spark SQL |

# **6\. Batch ETL Pipeline on Databricks**

## **6.1 Databricks Architecture Overview**

Databricks is a unified data analytics platform built on Apache Spark. Key components:

* Workspaces: Collaborative notebooks, workflows, and repos.

* Clusters: Managed Spark clusters (all-purpose or job clusters). Job clusters are cheaper — spun up/down per job.

* Delta Lake: Default table format. ACID transactions, time travel, schema enforcement.

* Unity Catalog: Centralized data governance — tables, volumes, credentials.

* Databricks Workflows: Native job scheduler with retry logic, alerting, dependency chaining.

* Photon Engine: Vectorized query engine (C++) — 2-8x faster than standard Spark for SQL workloads.

## **6.2 Tech Stack**

| Component | Technology |
| :---- | :---- |
| Compute | Databricks Job Clusters (auto-scaling) |
| Storage | Delta Lake on S3/ADLS/GCS |
| Catalog | Unity Catalog with 3-level namespace (catalog.schema.table) |
| Orchestration | Databricks Workflows (with DAG support) |
| Code | Python notebooks or .py files via Databricks Repos (Git) |
| Secrets | Databricks Secret Scopes (backed by Azure Key Vault / AWS Secrets Manager) |
| Monitoring | Databricks Lakehouse Monitoring, Spark UI |

## **6.3 Example — Full Databricks Batch Pipeline: E-commerce Data Lake**

### **Scenario**

Build a medallion architecture (Bronze → Silver → Gold) on Databricks for an e-commerce company. Each layer has its own job. Orchestrated by a Databricks Workflow DAG.

### **Medallion Architecture Flow**

| Architecture BRONZE (raw, as-is)  S3://raw/ (CSV, JSON, CDC)  →  Delta: catalog.bronze.\*  Job: bronze\_ingest.py  |  Schedule: every 15 minSILVER (cleaned, conformed)  Delta: catalog.bronze.\*  →  Delta: catalog.silver.\*  Job: silver\_transform.py  |  Schedule: hourlyGOLD (aggregated, business-ready)  Delta: catalog.silver.\*  →  Delta: catalog.gold.\*  Job: gold\_aggregate.py  |  Schedule: daily 2 AMConsumers: Tableau / PowerBI / ML models read from Gold layer |
| :---- |

### **bronze\_ingest.py**

from pyspark.sql import SparkSession, functions as F

from pyspark.sql.types import StructType, StructField, StringType, TimestampType

spark \= SparkSession.builder.getOrCreate()

\# Auto Loader — incremental ingestion with schema evolution

def ingest\_orders\_bronze():

    df \= (

        spark.readStream

             .format('cloudFiles')

             .option('cloudFiles.format', 'json')

             .option('cloudFiles.schemaLocation', 'dbfs:/checkpoints/orders/schema')

             .option('cloudFiles.inferColumnTypes', 'true')

             .load('s3://raw-bucket/orders/')

    )

    df \= df \\

        .withColumn('\_ingested\_at',  F.current\_timestamp()) \\

        .withColumn('\_source\_file',  F.input\_file\_name()) \\

        .withColumn('\_run\_date',     F.current\_date())

    (

        df.writeStream

          .format('delta')

          .outputMode('append')

          .option('checkpointLocation', 'dbfs:/checkpoints/orders/bronze')

          .trigger(availableNow=True)  \# Batch trigger — process backlog once

          .table('catalog.bronze.orders')

    ).awaitTermination()

ingest\_orders\_bronze()

### **silver\_transform.py**

from pyspark.sql import SparkSession, functions as F

from delta.tables import DeltaTable

spark \= SparkSession.builder.getOrCreate()

def silver\_orders():

    \# Read only new Bronze records using watermark

    bronze \= spark.read.table('catalog.bronze.orders')

    \# Filter to last run's new records (using \_run\_date partition)

    silver\_wm \= spark.sql(

        'SELECT MAX(\_run\_date) as wm FROM catalog.silver.orders'

    ).collect()\[0\]\['wm'\]

    new\_records \= bronze.filter(F.col('\_run\_date') \> silver\_wm)

    \# Transform: clean, validate, enrich

    clean \= new\_records \\

        .withColumn('order\_ts', F.to\_timestamp('order\_timestamp')) \\

        .withColumn('amount',   F.col('amount').cast('double')) \\

        .filter(F.col('order\_ts').isNotNull()) \\

        .filter(F.col('amount') \> 0\) \\

        .dropDuplicates(\['order\_id'\]) \\

        .withColumn('order\_day', F.to\_date('order\_ts')) \\

        .withColumn('order\_hour', F.hour('order\_ts')) \\

        .withColumn('\_silver\_ts', F.current\_timestamp())

    \# MERGE into silver

    if DeltaTable.isDeltaTable(spark, 'catalog.silver.orders'):

        silver \= DeltaTable.forName(spark, 'catalog.silver.orders')

        silver.alias('t').merge(

            clean.alias('s'), 't.order\_id \= s.order\_id'

        ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

    else:

        clean.write.format('delta') \\

             .partitionBy('order\_day') \\

             .saveAsTable('catalog.silver.orders')

silver\_orders()

### **gold\_aggregate.py**

from pyspark.sql import SparkSession, functions as F

spark \= SparkSession.builder.getOrCreate()

def gold\_daily\_sales():

    silver \= spark.read.table('catalog.silver.orders')

    products \= spark.read.table('catalog.silver.products')

    customers \= spark.read.table('catalog.silver.customers')

    df \= silver.join(F.broadcast(products), 'product\_id', 'left') \\

               .join(F.broadcast(customers), 'customer\_id', 'left')

    gold \= df.groupBy('order\_day','category','country').agg(

        F.count('order\_id').alias('orders'),

        F.sum('amount').alias('revenue'),

        F.approx\_count\_distinct('customer\_id').alias('unique\_customers'),

        F.avg('amount').alias('avg\_order\_value'),

        F.sum(F.when(F.col('is\_return'), F.col('amount')).otherwise(0)).alias('returns'),

    ).withColumn('net\_revenue', F.col('revenue') \- F.col('returns')) \\

     .withColumn('\_gold\_ts', F.current\_timestamp())

    gold.write.format('delta') \\

        .mode('overwrite') \\

        .option('replaceWhere', f'order\_day \= current\_date()') \\

        .saveAsTable('catalog.gold.daily\_sales\_summary')

gold\_daily\_sales()

## **6.4 Databricks Workflow YAML**

\# .databricks/bundle.yml (Databricks Asset Bundles)

resources:

  jobs:

    medallion\_etl:

      name: Medallion ETL Pipeline

      schedule:

        quartz\_cron\_expression: '0 0 2 \* \* ?'  \# 2 AM daily

        timezone\_id: UTC

      tasks:

        \- task\_key: bronze

          python\_wheel\_task:

            package\_name: my\_etl

            entry\_point: bronze\_ingest

          job\_cluster\_key: etl\_cluster

        \- task\_key: silver

          depends\_on: \[{task\_key: bronze}\]

          python\_wheel\_task:

            package\_name: my\_etl

            entry\_point: silver\_transform

          job\_cluster\_key: etl\_cluster

        \- task\_key: gold

          depends\_on: \[{task\_key: silver}\]

          python\_wheel\_task:

            package\_name: my\_etl

            entry\_point: gold\_aggregate

          job\_cluster\_key: etl\_cluster

      job\_clusters:

        \- job\_cluster\_key: etl\_cluster

          new\_cluster:

            spark\_version: 14.3.x-scala2.12

            node\_type\_id: m5.xlarge

            num\_workers: 4

            autoscale: {min\_workers: 2, max\_workers: 8}

## **6.5 Interview Questions — Databricks**

| Question | Answer / Key Points |
| :---- | :---- |
| What is the Medallion Architecture? | Bronze (raw) → Silver (clean) → Gold (aggregated). Each layer has increasing data quality. Supports replay from Bronze. |
| What is Auto Loader? | Databricks feature for incremental file ingestion using cloudFiles format. Uses file notifications (SQS/EventGrid) for scalability. Tracks processed files in checkpoint. |
| Difference: all-purpose vs job cluster? | All-purpose: shared, persistent, for dev/notebooks. Job cluster: ephemeral, cheaper, spun up per job run. |
| What is Delta Lake time travel? | Query historical versions: SELECT \* FROM table VERSION AS OF 5 or TIMESTAMP AS OF '2024-01-01'. Backed by transaction log. |
| How do you handle schema evolution? | Set mergeSchema=true in write options. Use ALTER TABLE ADD COLUMN. Auto Loader with inferColumnTypes handles source schema changes. |

# **7\. Batch ETL on AWS**

## **7.1 AWS ETL Services Overview**

| Service | Use Case |
| :---- | :---- |
| AWS Glue | Serverless Spark ETL. Auto-generates code, Glue Catalog, crawlers. |
| AWS EMR | Managed Hadoop/Spark clusters. More control, cheaper at scale. |
| AWS Lambda | Lightweight event-driven transforms. Max 15 min, 10 GB memory. |
| Step Functions | Orchestrates multi-step ETL workflows with retry/error handling. |
| S3 | Primary data lake storage for raw, staged, curated zones. |
| Redshift | Cloud data warehouse. Load via COPY command from S3. |
| Glue Data Catalog | Central Hive-compatible metastore for table schemas. |
| DMS (Database Migration Service) | CDC-based replication from OLTP sources to S3/Redshift. |

## **7.2 Example — AWS Glue ETL: S3 → Transform → Redshift**

### **Scenario**

Process daily JSON event files from S3 using an AWS Glue Job (PySpark). Transform and load into Amazon Redshift for BI reporting.

### **Pipeline Flow**

| Flow S3://raw/events/dt=YYYY-MM-DD/\*.json        ▼  AWS Glue Crawler (auto-catalog schema)  Glue ETL Job (PySpark \+ Glue DynamicFrame)        ▼  Transform: clean, flatten nested JSON, add partitions  S3://stage/events\_flat/  (Parquet, Glue Catalog registered)        ▼  Redshift COPY from S3  Redshift: analytics.fact\_events |
| :---- |

### **glue\_etl\_job.py**

import sys

from awsglue.transforms import \*

from awsglue.utils import getResolvedOptions

from awsglue.context import GlueContext

from awsglue.job import Job

from pyspark.context import SparkContext

from pyspark.sql import functions as F

args \= getResolvedOptions(sys.argv, \['JOB\_NAME','run\_date'\])

sc   \= SparkContext()

glue \= GlueContext(sc)

spark= glue.spark\_session

job  \= Job(glue)

job.init(args\['JOB\_NAME'\], args)

run\_date \= args\['run\_date'\]

\# Read from Glue Catalog (auto-crawled)

raw\_dyf \= glue.create\_dynamic\_frame.from\_catalog(

    database='raw\_events\_db',

    table\_name='events',

    push\_down\_predicate=f"dt \= '{run\_date}'"

)

\# Convert to Spark DataFrame for richer transforms

df \= raw\_dyf.toDF()

\# Flatten nested JSON: event\_properties is a struct

df \= df.select(

    'event\_id', 'user\_id', 'session\_id',

    F.to\_timestamp('event\_time').alias('event\_time'),

    'event\_type',

    F.col('event\_properties.page').alias('page'),

    F.col('event\_properties.product\_id').alias('product\_id'),

    F.col('device.type').alias('device\_type'),

    F.col('geo.country').alias('country'),

)

\# Data quality: drop records missing critical fields

df \= df.dropna(subset=\['event\_id','user\_id','event\_time'\])

df \= df.dropDuplicates(\['event\_id'\])

\# Add partition columns

df \= df.withColumn('year',  F.year('event\_time')) \\

       .withColumn('month', F.month('event\_time')) \\

       .withColumn('day',   F.dayofmonth('event\_time'))

\# Write to S3 stage as Parquet (register in Glue Catalog)

glue.write\_dynamic\_frame.from\_options(

    frame=DynamicFrame.fromDF(df, glue, 'result'),

    connection\_type='s3',

    format='parquet',

    connection\_options={

        'path': 's3://my-lake/stage/events/',

        'partitionKeys': \['year','month','day'\],

    },

    format\_options={'compression': 'snappy'}

)

job.commit()

### **redshift\_load.py — COPY from S3**

import boto3, psycopg2, logging

logger \= logging.getLogger(\_\_name\_\_)

COPY\_SQL \= '''

    COPY analytics.fact\_events

    FROM 's3://my-lake/stage/events/year={year}/month={month}/day={day}/'

    IAM\_ROLE 'arn:aws:iam::123456789:role/RedshiftS3Role'

    FORMAT AS PARQUET

    SERIALIZETOJSON;

'''

def load\_to\_redshift(year: int, month: int, day: int):

    ssm \= boto3.client('ssm', region\_name='us-east-1')

    db\_url \= ssm.get\_parameter(Name='/etl/redshift\_url', WithDecryption=True)\['Parameter'\]\['Value'\]

    conn \= psycopg2.connect(db\_url)

    with conn.cursor() as cur:

        cur.execute(f'DELETE FROM analytics.fact\_events WHERE year={year} AND month={month} AND day={day}')

        cur.execute(COPY\_SQL.format(year=year, month=month, day=day))

        conn.commit()

    logger.info(f'Redshift COPY complete for {year}-{month:02d}-{day:02d}')

    conn.close()

## **7.3 Example — AWS Step Functions ETL Orchestration**

### **step\_functions\_definition.json (simplified)**

{

  "Comment": "Daily ETL: S3 → Glue → Redshift",

  "StartAt": "RunGlueJob",

  "States": {

    "RunGlueJob": {

      "Type": "Task",

      "Resource": "arn:aws:states:::glue:startJobRun.sync",

      "Parameters": {

        "JobName": "events\_etl",

        "Arguments": {"--run\_date.$": "$.run\_date"}

      },

      "Next": "LoadToRedshift",

      "Catch": \[{"ErrorEquals": \["States.ALL"\], "Next": "NotifyFailure"}\]

    },

    "LoadToRedshift": {

      "Type": "Task",

      "Resource": "arn:aws:lambda:us-east-1:123:function:redshift\_loader",

      "Next": "NotifySuccess"

    },

    "NotifySuccess": {

      "Type": "Task",

      "Resource": "arn:aws:states:::sns:publish",

      "Parameters": {"TopicArn": "arn:aws:sns:...", "Message": "ETL SUCCESS"}

    },

    "NotifyFailure": {

      "Type": "Task",

      "Resource": "arn:aws:states:::sns:publish",

      "Parameters": {"TopicArn": "arn:aws:sns:...", "Message": "ETL FAILED"}

    }

  }

}

## **7.4 Interview Questions — AWS ETL**

| Question | Answer / Key Points |
| :---- | :---- |
| Glue vs EMR — when to use which? | Glue: serverless, managed, good for standard ETL, Glue Catalog integration. EMR: more control, cheaper for long-running/large jobs, supports non-Spark tools. |
| How do you partition S3 data for efficiency? | Partition by high-cardinality time dimensions (year/month/day). Use Hive-style paths for partition pruning in Athena/Glue/Spark. |
| How do you handle Redshift loading efficiently? | Use COPY command (parallel, fast). Pre-sort data by sort key. Use distribution keys matching join patterns. |
| How do you secure credentials in AWS ETL? | Secrets Manager or SSM Parameter Store. Never hardcode. Use IAM roles for service-to-service auth. |
| What is Glue Bookmark? | Tracks which S3 files/JDBC offsets have been processed. Enables incremental ETL without custom watermark tables. |

# **8\. Data Quality, Observability & Best Practices**

## **8.1 Data Quality Checks**

Production pipelines must validate data at every layer. The most common framework is Great Expectations.

### **great\_expectations\_checks.py**

import great\_expectations as gx

from great\_expectations.core.batch import RuntimeBatchRequest

context \= gx.get\_context()

def validate\_sales\_df(df):

    suite \= context.get\_expectation\_suite('sales\_suite')

    batch\_request \= RuntimeBatchRequest(

        datasource\_name='spark\_datasource',

        data\_connector\_name='runtime\_data\_connector',

        data\_asset\_name='sales\_batch',

        runtime\_parameters={'batch\_data': df},

        batch\_identifiers={'default\_identifier\_name': 'default'},

    )

    validator \= context.get\_validator(

        batch\_request=batch\_request,

        expectation\_suite=suite

    )

    \# Expectations

    validator.expect\_column\_to\_exist('order\_id')

    validator.expect\_column\_values\_to\_not\_be\_null('order\_id')

    validator.expect\_column\_values\_to\_be\_unique('order\_id')

    validator.expect\_column\_values\_to\_be\_between('quantity', min\_value=1, max\_value=10000)

    validator.expect\_column\_values\_to\_be\_between('unit\_price', min\_value=0.01)

    validator.expect\_column\_pair\_values\_a\_to\_be\_greater\_than\_b(

        'revenue', 'cost', or\_equal=True)

    results \= validator.validate()

    if not results.success:

        raise ValueError(f'Data quality checks failed: {results}')

    return results

## **8.2 Pipeline Monitoring Best Practices**

* Always log: pipeline name, run\_id, start\_time, end\_time, rows\_extracted, rows\_transformed, rows\_loaded, rows\_skipped.

* Write audit records to an etl\_audit table in PostgreSQL with each run's metadata.

* Alert on: zero rows loaded (empty run), high skip rate (\> 5%), duration SLA breach, unexpected schema.

* Use run IDs for every pipeline execution — tie all logs, metrics, and audit rows to the run\_id.

* Tag cloud resources (Glue jobs, EMR clusters) with pipeline name and environment for cost attribution.

### **audit\_logger.py**

import uuid, logging, time

import psycopg2

from datetime import datetime

from config import DB\_CONFIG

class PipelineAudit:

    def \_\_init\_\_(self, pipeline\_name: str):

        self.run\_id \= str(uuid.uuid4())

        self.pipeline \= pipeline\_name

        self.start\_ts \= datetime.utcnow()

        self.metrics \= {}

    def record(self, \*\*kwargs):

        self.metrics.update(kwargs)

    def complete(self, status='SUCCESS', error=None):

        with psycopg2.connect(\*\*DB\_CONFIG) as conn:

            with conn.cursor() as cur:

                cur.execute('''

                    INSERT INTO etl\_audit

                    (run\_id, pipeline, start\_ts, end\_ts, status,

                     rows\_extracted, rows\_loaded, rows\_skipped, error\_msg)

                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)

                ''', (

                    self.run\_id, self.pipeline, self.start\_ts,

                    datetime.utcnow(), status,

                    self.metrics.get('extracted', 0),

                    self.metrics.get('loaded', 0),

                    self.metrics.get('skipped', 0),

                    str(error) if error else None

                ))

                conn.commit()

## **8.3 Production Checklist**

| Category | Checklist Items |
| :---- | :---- |
| Idempotency | UPSERT/MERGE semantics. Watermarks for incremental. Safe reruns. |
| Error handling | Catch exceptions, log with context, exit with non-zero code. |
| Data quality | Schema validation, null checks, range checks, uniqueness. |
| Security | No hardcoded secrets. Use Secrets Manager. Least-privilege IAM/DB roles. |
| Observability | Structured logging, audit table, row count metrics, Slack/PagerDuty alerts. |
| Testing | Unit tests (pytest), integration tests, data contract tests. |
| Documentation | README with pipeline purpose, schedule, sources, targets, owner. |
| Recovery | Documented backfill procedure. Tested rollback. Partition-level re-run capability. |

# **9\. Production Interview Pipeline Examples**

## **9.1 Scenario A — Financial Transaction Reconciliation Pipeline**

### **Business Problem**

A fintech company needs to reconcile transactions between their payment processor (CSV) and core banking system (PostgreSQL) every night. Discrepancies must be flagged and reported.

| Full Pipeline Flow 1\. EXTRACT: Download payment\_processor\_YYYYMMDD.csv from SFTP2. EXTRACT: Read core\_banking.transactions from PostgreSQL (WHERE txn\_date \= run\_date)3. TRANSFORM: Standardize formats (currency, timestamps, IDs)4. RECONCILE: Full outer join on transaction\_id   \- Matched: status \= 'RECONCILED'   \- Payment only: status \= 'MISSING\_IN\_BANK' (likely delay)   \- Bank only: status \= 'MISSING\_IN\_PROCESSOR' (possible fraud/error)5. LOAD: Write recon\_results to PostgreSQL6. REPORT: Email CSV of discrepancies to Finance team7. AUDIT: Write summary to etl\_audit tableTech Stack: Python \+ Pandas \+ psycopg2 \+ smtplib \+ Airflow |
| :---- |

### **reconciliation.py — Core Logic**

import pandas as pd

import logging

from sqlalchemy import create\_engine

logger \= logging.getLogger(\_\_name\_\_)

def reconcile(processor\_df: pd.DataFrame,

              banking\_df: pd.DataFrame,

              run\_date: str) \-\> pd.DataFrame:

    \# Standardize

    for df in \[processor\_df, banking\_df\]:

        df\['transaction\_id'\] \= df\['transaction\_id'\].str.strip().str.upper()

        df\['amount'\] \= pd.to\_numeric(df\['amount'\], errors='coerce').round(2)

    \# Full outer join

    merged \= processor\_df.merge(

        banking\_df,

        on='transaction\_id',

        how='outer',

        suffixes=('\_proc','\_bank'),

        indicator=True

    )

    status\_map \= {

        'both':       'RECONCILED',

        'left\_only':  'MISSING\_IN\_BANK',

        'right\_only': 'MISSING\_IN\_PROCESSOR',

    }

    merged\['recon\_status'\] \= merged\['\_merge'\].map(status\_map)

    \# Flag amount mismatches in matched rows

    matched \= merged\['recon\_status'\] \== 'RECONCILED'

    merged.loc\[matched, 'amount\_diff'\] \= (

        (merged.loc\[matched,'amount\_proc'\] \-

         merged.loc\[matched,'amount\_bank'\]).round(2)

    )

    merged.loc\[matched & (merged\['amount\_diff'\].abs() \> 0.01),

               'recon\_status'\] \= 'AMOUNT\_MISMATCH'

    merged\['run\_date'\] \= run\_date

    discrepancies \= merged\[merged\['recon\_status'\] \!= 'RECONCILED'\]

    logger.info(f'Reconciled: {(matched).sum()} matched, {len(discrepancies)} discrepancies')

    return merged

## **9.2 Scenario B — E-commerce KPI Dashboard Pipeline**

### **Business Problem**

Build the daily refresh pipeline for an executive KPI dashboard. Aggregates from 4 tables into a single wide table consumed by Tableau.

| Full Pipeline Flow Tech Stack: PySpark on Databricks \+ Delta Lake \+ AirflowSOURCES (Silver layer):  silver.orders | silver.products | silver.customers | silver.returnsTRANSFORMATIONS:  1\. Filter to complete orders (status \= 'DELIVERED')  2\. Broadcast join small dims (products, customers) to orders  3\. Left join returns on order\_id to compute return rates  4\. Aggregate by date \+ category \+ region \+ customer\_segment:     \- gross\_revenue, net\_revenue, order\_count, units\_sold     \- return\_rate, new\_customer\_pct, avg\_order\_value     \- WoW and MoM growth (window functions over prior period rows)LOAD:  MERGE into gold.kpi\_daily (partition by report\_date)  Invalidate Tableau extract cache via REST APISLA: must complete by 6 AM for 8 AM executive meeting |
| :---- |

## **9.3 Scenario C — ML Training Data Pipeline**

### **Business Problem**

Prepare a 3-year feature table for training a customer churn prediction model. Combines transactional, behavioral, and demographic data. Runs monthly.

| Full Pipeline Flow Tech Stack: PySpark on AWS EMR \+ S3 \+ PostgreSQL (model registry)SOURCES:  S3 Parquet: clickstream (5B rows), transactions (500M rows)  PostgreSQL: customer\_profiles, subscriptions, support\_ticketsFEATURE ENGINEERING:  Per customer, per month window (36 months):  \- txn\_count\_30d, txn\_count\_90d, txn\_count\_365d  \- avg\_session\_duration, page\_views\_30d, login\_frequency  \- support\_tickets\_6m, days\_since\_last\_login  \- subscription\_tier, tenure\_months, plan\_change\_count  Window functions: LAG, LEAD, rolling averagesLABEL GENERATION:  churned \= 1 if no transaction in next 90 daysOUTPUT:  S3: ml\_features/churn/v3/  (Parquet, 50M rows x 40 features)  PostgreSQL: feature\_store.churn\_features (metadata only) |
| :---- |

## **9.4 Top 20 Batch ETL Interview Questions**

| Question | Key Answer Points |
| :---- | :---- |
| What is the difference between full load and incremental load? | Full: truncate+reload entire table each run. Incremental: only process new/changed records using watermarks, CDC, or timestamps. |
| How do you handle schema drift? | Detect with schema validation on extract. Use Delta Lake mergeSchema or Glue schema evolution. Alert on breaking changes. |
| Explain ACID in the context of ETL. | Atomicity: all-or-nothing write. Consistency: data constraints maintained. Isolation: concurrent writes don't interfere. Durability: committed data persists. Delta Lake provides ACID. |
| How do you design for failure and recovery? | Checkpoints, watermarks, idempotent writes, run\_id tracking, audit tables, re-runnable tasks. |
| What is a slowly changing dimension? | A dimension where attributes change slowly over time. SCD1: overwrite. SCD2: insert new version with valid\_from/valid\_to. SCD3: add column for previous value. |
| How would you backfill 2 years of data? | Parameterize pipeline with date range, partition work into manageable chunks, run in parallel, monitor memory/compute, validate results at each partition. |
| How do you handle duplicate data? | DROP DUPLICATES in Spark, deduplication CTE in SQL, ON CONFLICT in PostgreSQL, MERGE with match condition in Delta. |
| What is data partitioning and why does it matter? | Splitting data into logical subsets by key (date, region). Enables parallel processing, partition pruning (skip irrelevant files), and efficient incremental loads. |
| How do you monitor a batch pipeline? | Row counts at each stage, duration metrics, error rates, SLA breach alerts, data quality check results, lineage tracking. |
| What causes a Spark job to be slow? | Data skew, too few/many partitions, excessive shuffles, no caching of reused DataFrames, UDFs instead of built-in functions, driver bottleneck. |

# **10\. Quick Reference**

## **10.1 Tech Stack Comparison**

| Tool | Volume | Complexity | Cost | Best For |
| :---- | :---- | :---- | :---- | :---- |
| Pure Python | \< 1 GB | Low | $ | Simple scripts, quick jobs |
| Pandas | 1 GB – 10 GB | Medium | $$ | In-memory analytics, DS workflows |
| PySpark | 10 GB – PB | High | $$$ | Large-scale distributed ETL |
| PS Pandas | 10 GB – PB | Medium | $$$ | Scale Pandas code to clusters |
| Databricks | Any | High | $$$$ | Enterprise, Delta Lake, MLOps |
| AWS Glue | Any | Medium | $$$$ | Serverless, Glue Catalog, S3 |

## **10.2 Common SQL Patterns in Batch ETL**

\-- UPSERT (PostgreSQL)

INSERT INTO target (id, val, ts)

VALUES (%s, %s, %s)

ON CONFLICT (id) DO UPDATE

SET val \= EXCLUDED.val, ts \= EXCLUDED.ts;

\-- Incremental extract (watermark)

SELECT \* FROM source\_table

WHERE updated\_at \> :last\_run\_ts

ORDER BY updated\_at;

\-- Deduplication CTE

WITH ranked AS (

  SELECT \*, ROW\_NUMBER() OVER (PARTITION BY id ORDER BY updated\_at DESC) AS rn

  FROM source

)

SELECT \* FROM ranked WHERE rn \= 1;

\-- SCD2 MERGE (Databricks SQL)

MERGE INTO dim\_customers AS target

USING new\_customers AS source

ON target.customer\_id \= source.customer\_id AND target.is\_current \= true

WHEN MATCHED AND target.record\_hash \!= source.record\_hash THEN

  UPDATE SET target.valid\_to \= current\_date(), target.is\_current \= false

WHEN NOT MATCHED THEN

  INSERT (customer\_id, name, email, valid\_from, valid\_to, is\_current)

  VALUES (source.customer\_id, source.name, source.email,

          current\_date(), date('9999-12-31'), true);

## **10.3 Glossary**

| Term | Definition |
| :---- | :---- |
| Idempotency | Property where running a pipeline multiple times produces the same result as running it once. |
| Watermark | A stored timestamp or offset marking the last successfully processed record; used for incremental loads. |
| Partitioning | Dividing data into logical subsets (files/folders) by key columns to enable parallel processing and query pruning. |
| SCD | Slowly Changing Dimension. SCD2 maintains full history with valid\_from/valid\_to date range. |
| Delta Lake | Open-source storage layer on Parquet providing ACID transactions, time travel, and schema enforcement. |
| Medallion Architecture | Bronze (raw) → Silver (clean) → Gold (aggregated) data lake pattern. |
| Catalyst Optimizer | Spark's built-in query optimizer that rewrites logical plans for performance. |
| AQE | Adaptive Query Execution: Spark 3 feature that dynamically adjusts join strategies and partition sizes at runtime. |
| Shuffle | Expensive operation in Spark that redistributes data across nodes (triggered by joins, groupBys). |
| Backfill | Re-processing historical data, typically after a pipeline fix or for initial data load. |

*── End of Batch ETL Pipeline Guide ──*