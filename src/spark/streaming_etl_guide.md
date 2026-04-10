**STREAMING ETL PIPELINE**

A-to-Z Guide

Apache Kafka · Spark Structured Streaming · Flink · AWS Kinesis · Kafka Streams · Debezium · PostgreSQL · AWS

Real-Time Pipeline Flows | Interview & Production Grade Examples | Tech Stack

# **1\. Streaming ETL Pipeline — Fundamentals**

## **1.1 What Is a Streaming Pipeline?**

A streaming (or real-time) ETL pipeline processes data continuously as events arrive, rather than in scheduled batches. Each record (or micro-batch) is processed and persisted with milliseconds to seconds of latency.

Core characteristics:

* Unbounded data: The input data stream has no defined end — it grows indefinitely.

* Low latency: Results are visible seconds (or milliseconds) after events occur.

* Event-driven: Processing is triggered by new data, not by a schedule.

* Fault tolerance: Must recover from failures without losing or duplicating events.

* Exactly-once semantics: Each event is processed exactly once (no duplicates, no drops).

## **1.2 Streaming vs Batch — When to Use Streaming**

| Criterion | Streaming |
| :---- | :---- |
| Latency | Sub-second to seconds |
| Data model | Unbounded, continuous event stream |
| Triggers | Event arrival (not schedule) |
| Complexity | Higher — windowing, watermarks, state management |
| Cost | Higher — always-on compute |
| Use cases | Fraud detection, real-time dashboards, IoT alerts, CDC, clickstream |

## **1.3 Key Streaming Concepts**

* Event time vs Processing time: Event time \= when event occurred. Processing time \= when system processed it. Difference \= event skew.

* Watermarks: A threshold of how late an event can arrive and still be included in a window. Events older than the watermark are dropped.

* Windows: Group events by time range. Tumbling (non-overlapping), Sliding (overlapping), Session (activity-based).

* State: Information maintained across events (e.g. per-user running total, session tracking).

* Backpressure: Mechanism to slow producers when consumers can't keep up.

* Offset: Position in a Kafka partition. Used for tracking progress and recovery.

* Consumer Group: Set of consumers sharing partition assignment for a topic. Enables parallel consumption.

* Exactly-once semantics: Guaranteed by Kafka transactions \+ idempotent producers \+ transactional consumers.

## **1.4 Streaming Architecture Patterns**

| Pattern | Description |
| :---- | :---- |
| Lambda Architecture | Batch \+ streaming in parallel. Speed layer (streaming) \+ batch layer (accuracy). Complex to maintain. |
| Kappa Architecture | Streaming only. All processing via event log (Kafka). Simpler — one code path. |
| Event Sourcing | All state changes stored as an immutable event log. Current state is derived by replaying events. |
| CQRS | Separate read and write models. Writes go to event stream; read models built from stream. |
| Micro-batch | Small batch intervals (0.5-30s) to approximate streaming. Spark Structured Streaming default mode. |
| True Streaming | Record-by-record (Flink, Kafka Streams). Sub-millisecond latency possible. |

# **2\. Apache Kafka — Core Concepts & Producer/Consumer**

## **2.1 Kafka Architecture**

Kafka is a distributed event streaming platform. It acts as the central nervous system for most real-time data architectures.

* Broker: A Kafka server. A cluster has multiple brokers. Each broker stores partitions.

* Topic: Named category for events. Like a database table but append-only and distributed.

* Partition: Ordered, immutable sequence of records. Each topic has N partitions. Partitions enable parallelism.

* Offset: Sequential ID of a message within a partition. Consumer commits offset after processing.

* Producer: Writes records to topics. Can specify partition key for ordering guarantees.

* Consumer: Reads records from topics. Part of a consumer group.

* ZooKeeper / KRaft: Cluster metadata management. KRaft (Kafka 3.x) replaces ZooKeeper.

* Schema Registry: Central store for Avro/JSON/Protobuf schemas. Enforces compatibility.

* Connector (Kafka Connect): Pre-built connectors for databases, S3, Elasticsearch, etc.

## **2.2 Kafka Message Delivery Semantics**

| Semantic | Guarantee | When to Use |
| :---- | :---- | :---- |
| At-most-once | Message may be lost, never duplicated | Metrics, logs where loss is acceptable |
| At-least-once | Message delivered at least once, may duplicate | Default for most pipelines. Use idempotent consumers. |
| Exactly-once | Processed exactly once, no duplicates, no loss | Financial transactions, billing |

## **2.3 Example 1 — Kafka Producer: Clickstream Events**

### **Scenario**

A web application sends user clickstream events to Kafka. Producer uses JSON serialization with a partition key on user\_id (ensuring all events from one user go to the same partition, preserving order).

### **Pipeline Flow**

| Flow Web App  →  kafka-python Producer  →  Kafka Topic: user\_clicks  Partition key: user\_id (ordering guarantee per user)  Serialization: JSON (Schema Registry in production: use Avro)  Delivery: acks=all (leader \+ all in-sync replicas confirm) |
| :---- |

### **producer.py**

from confluent\_kafka import Producer

from confluent\_kafka.serialization import JSONSerializer, SerializationContext, MessageField

import json, logging, uuid

from datetime import datetime

logger \= logging.getLogger(\_\_name\_\_)

KAFKA\_CONFIG \= {

    'bootstrap.servers': 'kafka-broker-1:9092,kafka-broker-2:9092',

    'acks': 'all',              \# Wait for all in-sync replicas

    'enable.idempotence': True, \# Exactly-once producer

    'retries': 5,

    'retry.backoff.ms': 300,

    'compression.type': 'lz4', \# Compress batches

    'batch.size': 65536,        \# 64 KB batch size

    'linger.ms': 5,             \# Wait 5ms to fill batch

}

CLICK\_SCHEMA \= {

    'type': 'object',

    'properties': {

        'event\_id':   {'type': 'string'},

        'user\_id':    {'type': 'string'},

        'session\_id': {'type': 'string'},

        'event\_type': {'type': 'string'},

        'page\_url':   {'type': 'string'},

        'event\_time': {'type': 'string'},

        'properties': {'type': 'object'},

    },

    'required': \['event\_id','user\_id','event\_time'\]

}

producer \= Producer(KAFKA\_CONFIG)

def delivery\_callback(err, msg):

    if err:

        logger.error(f'Delivery failed: {err}')

    else:

        logger.debug(f'Delivered to {msg.topic()}\[{msg.partition()}\]@{msg.offset()}')

def send\_click\_event(user\_id: str, event\_type: str, page\_url: str,

                     session\_id: str, properties: dict \= None):

    event \= {

        'event\_id':   str(uuid.uuid4()),

        'user\_id':    user\_id,

        'session\_id': session\_id,

        'event\_type': event\_type,

        'page\_url':   page\_url,

        'event\_time': datetime.utcnow().isoformat(),

        'properties': properties or {},

    }

    producer.produce(

        topic='user\_clicks',

        key=user\_id.encode('utf-8'),   \# Partition by user\_id

        value=json.dumps(event).encode('utf-8'),

        on\_delivery=delivery\_callback,

    )

    producer.poll(0)  \# Trigger delivery callbacks

def flush():

    producer.flush(timeout=30)

## **2.4 Example 2 — Kafka Consumer: Real-Time Event Enrichment**

### **Scenario**

Consume click events from Kafka, enrich each event with user profile data (from Redis cache or PostgreSQL fallback), and write enriched events to a downstream Kafka topic.

### **Pipeline Flow**

| Flow Kafka: user\_clicks  →  Consumer (Python)  →  Enrich (Redis/PG)  →  Kafka: enriched\_clicks       (offset commit only after successful enrichment \+ produce)       Consumer group: click-enricher-group (N parallel consumers) |
| :---- |

### **consumer\_enricher.py**

from confluent\_kafka import Consumer, Producer, KafkaError

import json, logging, redis, psycopg2

from config import KAFKA\_CONFIG, REDIS\_CONFIG, DB\_CONFIG

logger \= logging.getLogger(\_\_name\_\_)

CONSUMER\_CONFIG \= {

    \*\*KAFKA\_CONFIG,

    'group.id': 'click-enricher-group',

    'auto.offset.reset': 'earliest',

    'enable.auto.commit': False,   \# Manual commit for exactly-once

    'max.poll.interval.ms': 300000,

}

redis\_client \= redis.Redis(\*\*REDIS\_CONFIG, decode\_responses=True)

def get\_user\_profile(user\_id: str) \-\> dict:

    \# Try Redis cache first

    cached \= redis\_client.get(f'user:{user\_id}')

    if cached:

        return json.loads(cached)

    \# Fallback to PostgreSQL

    with psycopg2.connect(\*\*DB\_CONFIG) as conn:

        with conn.cursor() as cur:

            cur.execute(

                'SELECT country, plan\_tier, signup\_date FROM users WHERE user\_id=%s',

                (user\_id,)

            )

            row \= cur.fetchone()

            if not row:

                return {}

            profile \= {'country': row\[0\], 'plan\_tier': row\[1\], 'signup\_date': str(row\[2\])}

            \# Cache for 10 minutes

            redis\_client.setex(f'user:{user\_id}', 600, json.dumps(profile))

            return profile

def run\_enricher(topics=\['user\_clicks'\]):

    consumer \= Consumer(CONSUMER\_CONFIG)

    producer \= Producer(KAFKA\_CONFIG)

    consumer.subscribe(topics)

    try:

        while True:

            msg \= consumer.poll(timeout=1.0)

            if msg is None:

                continue

            if msg.error():

                if msg.error().code() \== KafkaError.\_PARTITION\_EOF:

                    continue

                raise Exception(f'Consumer error: {msg.error()}')

            event \= json.loads(msg.value().decode('utf-8'))

            user\_id \= event.get('user\_id')

            \# Enrich

            profile \= get\_user\_profile(user\_id) if user\_id else {}

            enriched \= {\*\*event, \*\*profile, '\_enriched': True}

            \# Produce to downstream topic

            producer.produce(

                topic='enriched\_clicks',

                key=msg.key(),

                value=json.dumps(enriched).encode('utf-8'),

            )

            producer.flush()

            \# Commit offset only after successful downstream produce

            consumer.commit(message=msg, asynchronous=False)

    except KeyboardInterrupt:

        logger.info('Shutting down consumer')

    finally:

        consumer.close()

if \_\_name\_\_ \== '\_\_main\_\_':

    run\_enricher()

## **2.5 Interview Questions — Kafka**

| Question | Answer / Key Points |
| :---- | :---- |
| What happens when a consumer lags behind? | Consumer group lag grows. Monitor with kafka-consumer-groups.sh. Increase consumer instances (up to \# partitions). Optimize processing logic. |
| How do you guarantee ordering? | Messages with the same key go to the same partition. Ordering is guaranteed within a partition, not across partitions. |
| Explain Kafka retention. | Messages retained by time (retention.ms) or size (retention.bytes). Log compaction retains only latest value per key — useful for changelogs. |
| What is a consumer group rebalance? | Triggered when consumer joins/leaves group. Partitions are reassigned. Causes pause in consumption. Use cooperative sticky assignor to minimize rebalance scope. |
| How do you handle poison pill messages? | Catch deserialization errors, send to dead letter topic (DLT) for later investigation, commit offset and continue. |

# **3\. Spark Structured Streaming**

## **3.1 Overview**

Spark Structured Streaming is a scalable, fault-tolerant stream processing engine built on Spark SQL. It uses a micro-batch execution model (or continuous processing mode) and exposes a DataFrame/SQL API identical to batch processing.

* Continuous application: Streaming query runs as a long-lived process, processing new data as it arrives.

* Checkpoint: Tracks query progress (offsets, state). Stored in HDFS/S3/DBFS for fault tolerance.

* Trigger: Controls micro-batch interval: processingTime, once, availableNow, continuous.

* Output modes: append (new rows), complete (full result), update (changed rows).

* Watermark: Tells Spark how late data can arrive before being excluded from windows.

## **3.2 Tech Stack**

| Component | Technology |
| :---- | :---- |
| Compute | PySpark 3.x / Databricks |
| Source | Kafka, S3 (cloudFiles / Auto Loader), Delta, socket |
| Sink | Delta Lake, Kafka, PostgreSQL (foreachBatch), Cassandra |
| Checkpoints | S3 / DBFS / HDFS |
| Orchestration | Databricks Workflows / Kubernetes (always-on) |
| Monitoring | Spark UI Streaming tab, Databricks Lakehouse Monitoring |

## **3.3 Example 1 — Kafka → Spark Structured Streaming → Delta Lake**

### **Scenario**

Consume order events from Kafka, compute 5-minute tumbling window aggregates (orders and revenue per product category), and write to a Delta Lake table for real-time dashboards.

### **Pipeline Flow**

| Flow Kafka: order\_events  →  Spark readStream (Kafka source)        ▼  Parse JSON, cast types  Apply watermark: 10 min (tolerate late events)        ▼  Tumbling window: 5-min groups by (window, category)  Aggregate: order\_count, total\_revenue, avg\_order\_value        ▼  writeStream → Delta Lake (update mode)  Delta: streaming.order\_window\_metrics  Checkpoint: s3://checkpoints/order\_window/ |
| :---- |

### **order\_streaming.py**

from pyspark.sql import SparkSession

from pyspark.sql import functions as F

from pyspark.sql.types import \*

spark \= SparkSession.builder \\

    .appName('order\_window\_streaming') \\

    .config('spark.sql.extensions','io.delta.sql.DeltaSparkSessionExtension') \\

    .config('spark.sql.shuffle.partitions','50') \\

    .getOrCreate()

ORDER\_SCHEMA \= StructType(\[

    StructField('order\_id',    StringType(),  True),

    StructField('user\_id',     StringType(),  True),

    StructField('category',    StringType(),  True),

    StructField('amount',      DoubleType(),  True),

    StructField('order\_time',  StringType(),  True),

    StructField('status',      StringType(),  True),

\])

KAFKA\_CONFIG \= {

    'kafka.bootstrap.servers': 'kafka:9092',

    'subscribe': 'order\_events',

    'startingOffsets': 'latest',

    'kafka.security.protocol': 'SASL\_SSL',

    'failOnDataLoss': 'false',

    'maxOffsetsPerTrigger': '50000',  \# Backpressure control

}

\# ── READ STREAM ──────────────────────────────────────────

raw \= spark.readStream.format('kafka').options(\*\*KAFKA\_CONFIG).load()

\# Parse JSON payload

parsed \= raw.select(

    F.from\_json(

        F.col('value').cast('string'),

        ORDER\_SCHEMA

    ).alias('data')

).select('data.\*')

\# Cast and filter

orders \= parsed \\

    .withColumn('order\_ts', F.to\_timestamp('order\_time')) \\

    .filter(F.col('order\_ts').isNotNull()) \\

    .filter(F.col('status') \== 'COMPLETED') \\

    .filter(F.col('amount') \> 0\)

\# ── WATERMARK \+ WINDOW AGGREGATION ───────────────────────

windowed \= orders \\

    .withWatermark('order\_ts', '10 minutes') \\

    .groupBy(

        F.window('order\_ts', '5 minutes').alias('window'),

        'category'

    ).agg(

        F.count('order\_id').alias('order\_count'),

        F.sum('amount').alias('total\_revenue'),

        F.avg('amount').alias('avg\_order\_value'),

        F.approx\_count\_distinct('user\_id').alias('unique\_buyers'),

    ) \\

    .select(

        F.col('window.start').alias('window\_start'),

        F.col('window.end').alias('window\_end'),

        'category','order\_count','total\_revenue',

        F.round('avg\_order\_value',2).alias('avg\_order\_value'),

        'unique\_buyers'

    )

\# ── WRITE TO DELTA ────────────────────────────────────────

query \= windowed.writeStream \\

    .format('delta') \\

    .outputMode('update') \\

    .option('checkpointLocation', 's3://checkpoints/order\_window/') \\

    .trigger(processingTime='30 seconds') \\

    .table('streaming.order\_window\_metrics')

query.awaitTermination()

## **3.4 Example 2 — Streaming Deduplication with State**

### **Scenario**

High-volume payment events arrive from Kafka, but the upstream system may send duplicates within a 1-hour window. Implement stateful deduplication using Spark Structured Streaming.

### **Pipeline Flow**

| Flow Kafka: payment\_events  →  Spark readStream        ▼  Parse \+ validate  dropDuplicatesWithinWatermark(payment\_id, watermark=1hr)        ▼  foreachBatch → UPSERT to PostgreSQL  Checkpoint: maintains state of seen payment\_ids within watermark window |
| :---- |

### **dedup\_streaming.py**

from pyspark.sql import SparkSession, functions as F

from pyspark.sql.types import \*

import psycopg2, psycopg2.extras

spark \= SparkSession.builder.appName('payment\_dedup').getOrCreate()

PAYMENT\_SCHEMA \= StructType(\[

    StructField('payment\_id',   StringType(), True),

    StructField('order\_id',     StringType(), True),

    StructField('user\_id',      StringType(), True),

    StructField('amount',       DoubleType(), True),

    StructField('currency',     StringType(), True),

    StructField('payment\_time', StringType(), True),

    StructField('method',       StringType(), True),

\])

raw \= spark.readStream \\

    .format('kafka') \\

    .option('kafka.bootstrap.servers', 'kafka:9092') \\

    .option('subscribe', 'payment\_events') \\

    .load()

parsed \= raw.select(

    F.from\_json(F.col('value').cast('string'), PAYMENT\_SCHEMA).alias('d')

).select('d.\*') \\

 .withColumn('payment\_ts', F.to\_timestamp('payment\_time')) \\

 .filter(F.col('payment\_ts').isNotNull())

\# Stateful deduplication — Spark tracks seen payment\_ids within watermark

deduped \= parsed \\

    .withWatermark('payment\_ts', '1 hour') \\

    .dropDuplicatesWithinWatermark(\['payment\_id'\])

\# foreachBatch: write each micro-batch to PostgreSQL

DB\_URL \= 'postgresql://host:5432/payments'

def write\_to\_postgres(batch\_df, batch\_id):

    rows \= batch\_df.collect()

    if not rows:

        return

    vals \= \[(r.payment\_id, r.order\_id, r.user\_id, r.amount,

             r.currency, r.payment\_ts, r.method) for r in rows\]

    with psycopg2.connect(f'dbname=payments user=etl') as conn:

        with conn.cursor() as cur:

            psycopg2.extras.execute\_values(cur, '''

                INSERT INTO fact\_payments

                  (payment\_id, order\_id, user\_id, amount,

                   currency, payment\_ts, method)

                VALUES %s

                ON CONFLICT (payment\_id) DO NOTHING;

            ''', vals)

            conn.commit()

    print(f'Batch {batch\_id}: wrote {len(vals)} payments')

query \= deduped.writeStream \\

    .foreachBatch(write\_to\_postgres) \\

    .option('checkpointLocation', 's3://checkpoints/payment\_dedup/') \\

    .trigger(processingTime='10 seconds') \\

    .start()

query.awaitTermination()

## **3.5 Example 3 — Auto Loader: Continuous File Ingestion to Delta**

### **Scenario**

New JSON files are continuously dropped to S3 by IoT devices. Use Databricks Auto Loader to ingest them incrementally into Bronze Delta with schema evolution support.

### **Pipeline Flow**

| Flow S3://iot/events/  ←  IoT devices write JSON files continuously        ▼  Auto Loader (cloudFiles) — file notification via SQS  Detect new files, infer schema, track processed files        ▼  writeStream to Delta (append mode)  Bronze Delta: catalog.bronze.iot\_events  Schema evolution: new fields added automatically |
| :---- |

### **auto\_loader\_bronze.py**

from pyspark.sql import SparkSession, functions as F

spark \= SparkSession.builder.getOrCreate()

def start\_iot\_ingestion():

    df \= (

        spark.readStream

             .format('cloudFiles')

             .option('cloudFiles.format', 'json')

             .option('cloudFiles.schemaLocation', 'dbfs:/schemas/iot\_events')

             .option('cloudFiles.inferColumnTypes', 'true')

             .option('cloudFiles.schemaEvolutionMode', 'addNewColumns')

             .option('cloudFiles.useNotifications', 'true')  \# SQS notifications

             .load('s3://iot-bucket/events/')

    )

    \# Add metadata columns

    df \= df \\

        .withColumn('\_source\_file',  F.input\_file\_name()) \\

        .withColumn('\_ingested\_at',  F.current\_timestamp()) \\

        .withColumn('\_partition\_date', F.current\_date())

    query \= (

        df.writeStream

          .format('delta')

          .outputMode('append')

          .option('checkpointLocation', 'dbfs:/checkpoints/iot\_bronze')

          .option('mergeSchema', 'true')  \# Allow schema evolution

          .partitionBy('\_partition\_date')

          .trigger(processingTime='60 seconds')

          .table('catalog.bronze.iot\_events')

    )

    return query

q \= start\_iot\_ingestion()

q.awaitTermination()

## **3.6 Interview Questions — Spark Structured Streaming**

| Question | Answer / Key Points |
| :---- | :---- |
| What is a watermark and why is it needed? | Tells Spark how late an event can arrive and still be included in a window. Without watermark, Spark holds state forever. With watermark, old state is evicted. |
| Explain output modes. | Append: only new rows emitted (aggregations with watermark). Complete: full result table each trigger. Update: only changed rows emitted. |
| What happens if a streaming query fails? | On restart, Spark reads from the checkpoint to recover the last committed offset and state. Processing resumes from where it left off. |
| When to use foreachBatch? | When you need to write to a non-native sink (JDBC, custom API) or apply batch operations (MERGE) to each micro-batch. |
| What is maxOffsetsPerTrigger? | Limits Kafka offsets read per micro-batch. Used for backpressure — prevents a backlog from overwhelming the cluster on startup. |

# **4\. Kafka Streams & Python faust-streaming**

## **4.1 Kafka Streams Overview**

Kafka Streams is a client library for building streaming applications on top of Kafka. Unlike Spark, it runs as a lightweight Java/Python library inside your application — no separate cluster needed.

* Topology: DAG of source processors, stream processors, and sink processors.

* KStream: Unbounded stream of records. Each record is an event.

* KTable: Changelog stream. Represents the latest value per key (like a database table).

* GlobalKTable: KTable replicated to all instances — useful for small lookup tables.

* State stores: Local RocksDB stores for per-key state (aggregations, joins).

* Interactive queries: Query state stores from outside the application.

## **4.2 Python Alternative: Faust**

Faust is a Python stream processing library inspired by Kafka Streams. It runs as a Python service.

| Feature | Faust (Python) |
| :---- | :---- |
| Language | Python 3.8+ |
| Deployment | Python service (Docker, Kubernetes) |
| State | RocksDB or in-memory tables |
| Window support | Tumbling, Hopping, Session |
| Schema | Pydantic / dataclasses |
| Best for | Python-first teams, microservices |

## **4.3 Example — Faust: Real-Time Fraud Score Aggregation**

### **Scenario**

Consume transaction events, compute a per-user rolling 5-minute transaction count and total amount. If a user exceeds thresholds (\>10 txns OR \>$5000 in 5 min), emit a fraud alert to a separate topic.

### **Pipeline Flow**

| Flow Kafka: transactions  →  Faust Agent (consume)        ▼  Per-user state: update 5-min rolling window table  Check thresholds: count \> 10 OR amount \> 5000        ▼  If breach: produce to Kafka: fraud\_alerts  State store: RocksDB (per-user running totals \+ window) |
| :---- |

### **fraud\_detector.py**

import faust

from dataclasses import dataclass

from datetime import timedelta

import logging

logger \= logging.getLogger(\_\_name\_\_)

@dataclass

class Transaction(faust.Record, serializer='json'):

    transaction\_id: str

    user\_id: str

    amount: float

    merchant: str

    txn\_time: str

    country: str

@dataclass

class FraudAlert(faust.Record, serializer='json'):

    user\_id: str

    alert\_type: str

    window\_txn\_count: int

    window\_total\_amount: float

    triggered\_by: str

    alert\_time: str

app \= faust.App(

    'fraud-detector',

    broker='kafka://kafka:9092',

    store='rocksdb://',

    value\_serializer='json',

)

txn\_topic   \= app.topic('transactions',   value\_type=Transaction)

alert\_topic \= app.topic('fraud\_alerts',   value\_type=FraudAlert)

\# Tumbling 5-minute window table keyed by user\_id

txn\_counts \= app.Table('txn\_counts',  default=int).tumbling(timedelta(minutes=5))

txn\_totals \= app.Table('txn\_totals',  default=float).tumbling(timedelta(minutes=5))

ALERT\_THRESHOLD\_COUNT  \= 10

ALERT\_THRESHOLD\_AMOUNT \= 5000.0

@app.agent(txn\_topic)

async def process\_transactions(transactions):

    async for txn in transactions.group\_by(Transaction.user\_id):

        \# Increment windowed state

        txn\_counts\[txn.user\_id\] \+= 1

        txn\_totals\[txn.user\_id\] \+= txn.amount

        count  \= txn\_counts\[txn.user\_id\].current()

        total  \= txn\_totals\[txn.user\_id\].current()

        \# Check thresholds

        if count \> ALERT\_THRESHOLD\_COUNT:

            await alert\_topic.send(key=txn.user\_id, value=FraudAlert(

                user\_id=txn.user\_id,

                alert\_type='HIGH\_FREQUENCY',

                window\_txn\_count=count,

                window\_total\_amount=round(total, 2),

                triggered\_by=txn.transaction\_id,

                alert\_time=txn.txn\_time,

            ))

            logger.warning(f'FRAUD ALERT: {txn.user\_id} \- {count} txns in 5min')

        elif total \> ALERT\_THRESHOLD\_AMOUNT:

            await alert\_topic.send(key=txn.user\_id, value=FraudAlert(

                user\_id=txn.user\_id,

                alert\_type='HIGH\_AMOUNT',

                window\_txn\_count=count,

                window\_total\_amount=round(total, 2),

                triggered\_by=txn.transaction\_id,

                alert\_time=txn.txn\_time,

            ))

if \_\_name\_\_ \== '\_\_main\_\_':

    app.main()

# **5\. AWS Kinesis Streaming Pipeline**

## **5.1 AWS Kinesis Services**

| Service | Purpose |
| :---- | :---- |
| Kinesis Data Streams | Real-time data streaming. Shards (1 MB/s write, 2 MB/s read each). Retention 24h–365d. |
| Kinesis Data Firehose | Managed delivery to S3, Redshift, OpenSearch, Splunk. Buffer, compress, transform. |
| Kinesis Data Analytics | SQL or Apache Flink on streams. No cluster management. |
| MSK (Managed Kafka) | Managed Apache Kafka. Preferred for Kafka-native workloads. |

## **5.2 Tech Stack**

| Component | Technology |
| :---- | :---- |
| Producer | Python boto3 / Kinesis Agent / SDK |
| Stream | Kinesis Data Streams (N shards) |
| Processing | Lambda / Kinesis Data Analytics / Flink on EMR |
| Delivery | Kinesis Firehose → S3 (Parquet) → Glue Catalog |
| Consumption | Lambda trigger / KCL (Kinesis Client Library) |
| Monitoring | CloudWatch: GetRecords.IteratorAgeMilliseconds (lag metric) |

## **5.3 Example — Kinesis Producer \+ Lambda Consumer**

### **Scenario**

IoT temperature sensors publish readings to Kinesis. A Lambda function is triggered per shard batch, validates readings, and writes anomalies to DynamoDB and all records to S3 via Firehose.

### **Pipeline Flow**

| Flow IoT Devices  →  Kinesis Data Stream: sensor\_readings (10 shards)        ▼  Lambda trigger (batch size: 100, parallelization: 1/shard)  Validate readings (range check, device\_id exists)  Anomaly detection: temp \> 80°C OR \< \-40°C        ▼  DynamoDB: sensor\_anomalies (anomalies only)        ▼  Kinesis Firehose: all records → S3 Parquet → Glue Catalog |
| :---- |

### **kinesis\_producer.py — Sensor Data Producer**

import boto3, json, time, random

from datetime import datetime

kinesis \= boto3.client('kinesis', region\_name='us-east-1')

STREAM\_NAME \= 'sensor\_readings'

def send\_reading(device\_id: str, temperature: float, humidity: float):

    record \= {

        'device\_id':   device\_id,

        'temperature': round(temperature, 2),

        'humidity':    round(humidity, 2),

        'unit':        'celsius',

        'reading\_ts':  datetime.utcnow().isoformat(),

    }

    kinesis.put\_record(

        StreamName=STREAM\_NAME,

        Data=json.dumps(record).encode('utf-8'),

        PartitionKey=device\_id,  \# Shard routing by device

    )

def simulate\_sensors(n\_devices: int \= 100):

    devices \= \[f'SENSOR\_{i:04d}' for i in range(n\_devices)\]

    while True:

        batch \= \[\]

        for device\_id in devices:

            temp \= random.gauss(22, 5\)

            if random.random() \< 0.01:  \# 1% anomaly rate

                temp \= random.choice(\[random.uniform(85, 100), random.uniform(-50,-42)\])

            batch.append({

                'Data': json.dumps({'device\_id': device\_id, 'temperature': round(temp,2),

                                    'reading\_ts': datetime.utcnow().isoformat()}).encode(),

                'PartitionKey': device\_id

            })

        \# Batch put (max 500 records / 5 MB per call)

        for i in range(0, len(batch), 500):

            kinesis.put\_records(Records=batch\[i:i+500\], StreamName=STREAM\_NAME)

        time.sleep(1)

### **lambda\_consumer.py — Lambda Triggered by Kinesis**

import json, boto3, logging

from decimal import Decimal

from datetime import datetime

logger \= logging.getLogger(\_\_name\_\_)

logger.setLevel(logging.INFO)

dynamodb \= boto3.resource('dynamodb')

anomaly\_table \= dynamodb.Table('sensor\_anomalies')

TEMP\_MAX \=  80.0

TEMP\_MIN \= \-40.0

def lambda\_handler(event, context):

    records \= event\['Records'\]

    anomalies, valid, invalid \= 0, 0, 0

    for record in records:

        try:

            payload \= json.loads(record\['kinesis'\]\['data\_decoded'\]

                        if 'data\_decoded' in record\['kinesis'\]

                        else \_\_import\_\_('base64').b64decode(record\['kinesis'\]\['data'\]))

            device\_id   \= payload.get('device\_id')

            temperature \= payload.get('temperature')

            reading\_ts  \= payload.get('reading\_ts')

            if not all(\[device\_id, temperature is not None, reading\_ts\]):

                invalid \+= 1

                continue

            valid \+= 1

            \# Anomaly detection

            if temperature \> TEMP\_MAX or temperature \< TEMP\_MIN:

                anomaly\_table.put\_item(Item={

                    'device\_id':    device\_id,

                    'reading\_ts':   reading\_ts,

                    'temperature':  Decimal(str(temperature)),

                    'alert\_type':   'HIGH\_TEMP' if temperature \> TEMP\_MAX else 'LOW\_TEMP',

                    'processed\_at': datetime.utcnow().isoformat(),

                })

                anomalies \+= 1

        except Exception as e:

            logger.error(f'Failed to process record: {e}')

            invalid \+= 1

    logger.info(f'Processed {len(records)} records: {valid} valid, '

               f'{anomalies} anomalies, {invalid} invalid')

    return {'statusCode': 200, 'valid': valid, 'anomalies': anomalies}

## **5.4 Kinesis Firehose Configuration (Terraform snippet)**

resource "aws\_kinesis\_firehose\_delivery\_stream" "sensor\_delivery" {

  name        \= "sensor-to-s3"

  destination \= "extended\_s3"

  extended\_s3\_configuration {

    role\_arn            \= aws\_iam\_role.firehose.arn

    bucket\_arn          \= aws\_s3\_bucket.lake.arn

    prefix              \= "curated/sensors/year=\!{timestamp:yyyy}/month=\!{timestamp:MM}/"

    error\_output\_prefix \= "errors/sensors/"

    buffer\_interval     \= 60      \# seconds

    buffer\_size         \= 128     \# MB

    compression\_format  \= "SNAPPY"

    data\_format\_conversion\_configuration {

      enabled \= true

      input\_format\_configuration {

        deserializer { open\_x\_json\_ser\_de {} }

      }

      output\_format\_configuration {

        serializer { parquet\_ser\_de { compression \= "SNAPPY" } }

      }

      schema\_configuration {

        database\_name \= "raw\_db"

        table\_name    \= "sensor\_readings"

        role\_arn      \= aws\_iam\_role.firehose.arn

      }

    }

  }

}

## **5.5 Interview Questions — Kinesis**

| Question | Answer / Key Points |
| :---- | :---- |
| What is a Kinesis shard? | Unit of capacity. Each shard: 1 MB/s ingest, 2 MB/s consumption, up to 1000 PUT records/sec. Scale by splitting shards. |
| How do you scale Kinesis? | Increase shard count (UpdateShardCount). Use enhanced fan-out for multiple independent consumers at 2 MB/s each. |
| Kinesis vs Kafka — key differences? | Kinesis: managed, AWS-native, shard-based. Kafka: more control, community ecosystem, Confluent Cloud managed option. Kinesis easier ops; Kafka more flexible. |
| What is GetRecords.IteratorAgeMilliseconds? | CloudWatch metric \= difference between current time and oldest unread record's timestamp. High value \= consumer lag. Alert when \> 60s. |
| How do you replay Kinesis data? | Set ShardIteratorType=AT\_TIMESTAMP to replay from a point in the retention window (24h–365d). |

# **6\. Change Data Capture (CDC) with Debezium**

## **6.1 What Is CDC?**

Change Data Capture (CDC) is a technique that captures row-level changes (INSERT, UPDATE, DELETE) from a database's transaction log and streams them as events. Debezium is the most popular open-source CDC tool.

* Source: PostgreSQL WAL, MySQL binlog, MongoDB oplog, Oracle LogMiner.

* Debezium connector: Runs inside Kafka Connect, reads the DB transaction log, produces change events to Kafka.

* Event structure: Each event contains before (old row), after (new row), op (c/u/d), ts\_ms.

* Exactly-once: Debezium uses Kafka Connect's exactly-once semantics to prevent duplicate change events.

## **6.2 Tech Stack**

| Component | Technology |
| :---- | :---- |
| Source DB | PostgreSQL (wal\_level=logical) |
| CDC Tool | Debezium PostgreSQL Connector |
| Transport | Apache Kafka (via Kafka Connect) |
| Consumer | Python kafka-python / PySpark / Faust |
| Sink | Data Lake (Delta/Parquet) / Elasticsearch / Redis |

## **6.3 Example — Debezium CDC: PostgreSQL → Kafka → Delta Lake**

### **Scenario**

Replicate all changes from a PostgreSQL orders table in real-time to a Delta Lake table using Debezium. Maintain a current-state table (MERGE on primary key).

### **Pipeline Flow**

| Flow PostgreSQL: orders table (WAL/logical replication slot)        ▼  Debezium connector (Kafka Connect)  Kafka: postgres.public.orders  (CDC events with before/after)        ▼  PySpark Structured Streaming consumer  Parse CDC event: extract op \+ after record        ▼  foreachBatch: MERGE into Delta Lake  Delta: warehouse.orders (real-time replica, always current) |
| :---- |

### **debezium\_connector.json — Register via Kafka Connect REST API**

{

  "name": "orders-cdc-connector",

  "config": {

    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",

    "database.hostname": "pg-host",

    "database.port": "5432",

    "database.user": "debezium",

    "database.password": "${file:/opt/kafka/config/creds.properties:pg.password}",

    "database.dbname": "production",

    "database.server.name": "postgres",

    "table.include.list": "public.orders,public.order\_items",

    "plugin.name": "pgoutput",

    "slot.name": "debezium\_orders",

    "publication.name": "debezium\_pub",

    "topic.prefix": "cdc",

    "transforms": "unwrap",

    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",

    "transforms.unwrap.add.fields": "op,ts\_ms,db,table",

    "heartbeat.interval.ms": "10000",

    "snapshot.mode": "initial"

  }

}

### **cdc\_streaming.py — Consume CDC Events into Delta**

from pyspark.sql import SparkSession, functions as F

from pyspark.sql.types import \*

from delta.tables import DeltaTable

spark \= SparkSession.builder.appName('cdc\_orders').getOrCreate()

\# Debezium flattened schema (after ExtractNewRecordState SMT)

ORDERS\_SCHEMA \= StructType(\[

    StructField('order\_id',      LongType(),    False),

    StructField('customer\_id',   StringType(),  True),

    StructField('status',        StringType(),  True),

    StructField('total\_amount',  DoubleType(),  True),

    StructField('created\_at',    StringType(),  True),

    StructField('updated\_at',    StringType(),  True),

    StructField('\_\_op',          StringType(),  True),  \# c/u/d/r

    StructField('\_\_ts\_ms',       LongType(),    True),  \# source commit ts

    StructField('\_\_deleted',     BooleanType(), True),

\])

DELTA\_PATH \= 's3://warehouse/orders'

raw \= spark.readStream \\

    .format('kafka') \\

    .option('kafka.bootstrap.servers', 'kafka:9092') \\

    .option('subscribe', 'cdc.public.orders') \\

    .option('startingOffsets', 'latest') \\

    .load()

parsed \= raw.select(

    F.from\_json(F.col('value').cast('string'), ORDERS\_SCHEMA).alias('d')

).select('d.\*') \\

 .filter(F.col('order\_id').isNotNull())

def apply\_cdc\_batch(batch\_df, batch\_id):

    if batch\_df.isEmpty():

        return

    \# Keep only latest event per order\_id in this batch

    deduped \= batch\_df.orderBy('\_\_ts\_ms', ascending=False) \\

                      .dropDuplicates(\['order\_id'\])

    \# Separate deletes from upserts

    deletes \= deduped.filter(F.col('\_\_deleted') \== True)

    upserts \= deduped.filter(F.col('\_\_deleted') \!= True)

    if DeltaTable.isDeltaTable(spark, DELTA\_PATH):

        delta \= DeltaTable.forPath(spark, DELTA\_PATH)

        \# MERGE upserts

        if not upserts.isEmpty():

            delta.alias('t').merge(

                upserts.alias('s'),

                't.order\_id \= s.order\_id'

            ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

        \# Apply deletes (soft delete: set is\_deleted \= true)

        if not deletes.isEmpty():

            delta.alias('t').merge(

                deletes.alias('s'),

                't.order\_id \= s.order\_id'

            ).whenMatchedUpdate(set={'is\_deleted': F.lit(True),

                                     'deleted\_at': F.current\_timestamp()}

            ).execute()

    else:

        upserts.withColumn('is\_deleted', F.lit(False)) \\

               .write.format('delta').save(DELTA\_PATH)

    print(f'CDC Batch {batch\_id}: {upserts.count()} upserts, {deletes.count()} deletes')

query \= parsed.writeStream \\

    .foreachBatch(apply\_cdc\_batch) \\

    .option('checkpointLocation', 's3://checkpoints/cdc\_orders/') \\

    .trigger(processingTime='5 seconds') \\

    .start()

query.awaitTermination()

## **6.4 Interview Questions — CDC**

| Question | Answer / Key Points |
| :---- | :---- |
| Why use CDC over polling? | Polling misses deletes, causes load on source DB, has latency. CDC from WAL: real-time, zero source impact, captures all change types. |
| What is a Debezium snapshot? | Initial full-table read performed when connector first starts (snapshot.mode=initial). Sets baseline before streaming changes. |
| How do you handle schema changes in CDC? | Use schema registry for Avro. Debezium emits a schema change event. Consumers must handle added/removed fields gracefully. |
| What is a replication slot? | PostgreSQL mechanism for CDC. Holds WAL position so changes aren't discarded before Debezium reads them. Must monitor slot lag to avoid disk filling. |
| How do you handle out-of-order CDC events? | Debezium emits in order per table. For multi-table consistency, use LSN (log sequence number) for global ordering. |

# **7\. Production Interview Streaming Pipeline Examples**

## **7.1 Scenario A — Real-Time Fraud Detection System**

### **Business Problem**

A payments company needs to detect and block fraudulent transactions within 200ms of occurrence. The system must process 50,000 transactions per second at peak.

| Full Architecture INGEST:  Payment API → Kafka (transactions, 20 partitions, 3x replication)STREAM PROCESSING (Faust microservices, 10 instances):  Service 1: Enrich (user profile from Redis)  Service 2: Feature extraction (windowed counts/sums)  Service 3: Score (call ML model REST API)  Service 4: Decision (threshold → APPROVE/BLOCK/REVIEW)ACTIONS:  Decision API response: \<200ms (blocking path)  Kafka: fraud\_decisions topic → Payment API  PostgreSQL: fraud\_events table (async, for investigation)  SNS: alert fraud analysts for REVIEW decisionsMONITORING:  Prometheus \+ Grafana: lag, throughput, decision latency  PagerDuty: lag \> 1000ms or model API error rate \> 1%Tech: Python Faust \+ Redis \+ FastAPI ML service \+ Kafka \+ PG |
| :---- |

## **7.2 Scenario B — Real-Time Analytics Dashboard**

### **Business Problem**

Build a streaming pipeline for a SaaS company's real-time revenue dashboard showing orders per minute, revenue by product, and live conversion funnel — updated every 30 seconds.

| Full Architecture SOURCES:  order\_created events → Kafka  checkout\_started events → Kafka  payment\_completed events → KafkaPROCESSING (Spark Structured Streaming, Databricks):  Job 1: Tumbling 1-min windows → order\_metrics (orders/min, revenue/min)  Job 2: Sliding 5-min windows → product\_revenue (by category)  Job 3: Session funnel (checkout\_started → payment\_completed rate per 5min)STORAGE:  Delta: streaming.realtime\_metrics (30s trigger)  Redis: pre-aggregated KPIs (TTL 60s) for sub-5ms dashboard readsSERVING:  FastAPI → reads Redis → WebSocket push to React dashboard  Fallback: direct Delta query via Databricks SQL WarehouseTech: Spark Structured Streaming \+ Delta \+ Redis \+ FastAPI \+ Databricks |
| :---- |

## **7.3 Scenario C — Event-Driven Data Lake Ingestion**

### **Business Problem**

100+ microservices publish domain events to Kafka. A data platform team needs to ingest all events into a data lake for analytics, maintaining full history, schema evolution, and replay capability.

| Full Architecture PRODUCERS: 100 microservices → Kafka (50 topics)SCHEMA MANAGEMENT:  Confluent Schema Registry (Avro)  Schema compatibility: BACKWARD (consumers can read older schemas)INGESTION (Spark Structured Streaming, 1 job per topic group):  Read all topics via subscribe pattern: 'domain.\*'  Extract: topic name → domain \+ event\_type  Parse Avro with schema registry  Write: Bronze Delta partitioned by (domain, event\_type, date)REPLAY CAPABILITY:  Kafka retention: 30 days  Delta time travel: full history  Replay any topic from day 0 by resetting Spark checkpointSILVER LAYER:  Auto-triggered Silver jobs per domain after Bronze write  Databricks Workflows with trigger\_on\_job\_completionTech: Confluent Kafka \+ Avro \+ Spark Structured Streaming \+ Delta Lake \+ Databricks |
| :---- |

## **7.4 Scenario D — CDC-Based Microservices Sync**

### **Business Problem**

Synchronize user profile changes from a PostgreSQL monolith to 3 downstream microservices (notification service Redis cache, search service Elasticsearch, analytics Delta table) in real-time.

| Full Architecture SOURCE: PostgreSQL users table        ▼  Debezium CDC connectorKafka: cdc.public.users        ▼  3 separate consumer groupsConsumer 1 (Python): notification-sync-group  → Redis HSET user:\<id\> {email, name, preferences} (TTL 1hr)Consumer 2 (Python): search-sync-group  → Elasticsearch index: users  → Upsert on user\_id, delete on \_\_deleted=trueConsumer 3 (PySpark Streaming): analytics-sync-group  → Delta Lake MERGE into dim\_usersDEAD LETTER: failed events → Kafka: cdc.dlq.users  Retry worker processes DLQ with exponential backoffTech: Debezium \+ Kafka \+ Python kafka-python \+ Elasticsearch \+ Redis \+ Delta |
| :---- |

# **8\. Apache Flink — True Streaming Processing**

## **8.1 Flink vs Spark Streaming**

| Aspect | Apache Flink |
| :---- | :---- |
| Model | True streaming (record-by-record, not micro-batch) |
| Latency | Sub-millisecond to millisecond |
| State | Extremely powerful: keyed state, operator state, savepoints |
| Exactly-once | Native via distributed snapshots (Chandy-Lamport) |
| API | DataStream API, Table API, Flink SQL |
| Python | PyFlink (Table API, DataStream API) |
| Best for | Complex event processing, financial transactions, gaming |

## **8.2 Example — PyFlink: Real-Time User Session Analytics**

### **Scenario**

Track user sessions in real-time. A session ends after 30 minutes of inactivity. Emit session summaries to Kafka when a session closes.

### **Pipeline Flow**

| Flow Kafka: user\_events  →  PyFlink DataStream        ▼  KeyBy(user\_id)  Session window (gap: 30 min inactivity)        ▼  Aggregate: event\_count, pages\_visited, duration  Kafka: user\_sessions (session summary events)  State backend: RocksDB (for large state) |
| :---- |

### **flink\_sessions.py**

from pyflink.datastream import StreamExecutionEnvironment

from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink

from pyflink.datastream.window import EventTimeSessionWindows

from pyflink.common.time import Duration, Time

from pyflink.common.watermark\_strategy import WatermarkStrategy

from pyflink.datastream.functions import AggregateFunction, ProcessWindowFunction

import json

env \= StreamExecutionEnvironment.get\_execution\_environment()

env.set\_parallelism(8)

env.get\_checkpoint\_config().set\_checkpoint\_interval(30000)  \# 30s

env.set\_state\_backend('rocksdb')  \# for large state

\# Kafka source

kafka\_source \= KafkaSource.builder() \\

    .set\_bootstrap\_servers('kafka:9092') \\

    .set\_topics('user\_events') \\

    .set\_group\_id('flink-session-group') \\

    .set\_value\_only\_deserializer(SimpleStringSchema()) \\

    .build()

\# Watermark: tolerate up to 5 min late events

watermark\_strategy \= WatermarkStrategy \\

    .for\_bounded\_out\_of\_orderness(Duration.of\_minutes(5)) \\

    .with\_timestamp\_assigner(

        lambda event, \_: json.loads(event).get('event\_time\_ms', 0\)

    )

stream \= env.from\_source(

    kafka\_source, watermark\_strategy, 'UserEvents'

).map(lambda v: json.loads(v))

class SessionAggregator(AggregateFunction):

    def create\_accumulator(self):

        return {'event\_count': 0, 'pages': set(), 'min\_ts': None, 'max\_ts': None}

    def add(self, event, acc):

        acc\['event\_count'\] \+= 1

        acc\['pages'\].add(event.get('page\_url'))

        ts \= event.get('event\_time\_ms', 0\)

        acc\['min\_ts'\] \= min(ts, acc\['min\_ts'\] or ts)

        acc\['max\_ts'\] \= max(ts, acc\['max\_ts'\] or ts)

        return acc

    def get\_result(self, acc):

        return acc

    def merge(self, a, b):

        return {

            'event\_count': a\['event\_count'\] \+ b\['event\_count'\],

            'pages': a\['pages'\] | b\['pages'\],

            'min\_ts': min(a\['min\_ts'\] or 0, b\['min\_ts'\] or 0),

            'max\_ts': max(a\['max\_ts'\] or 0, b\['max\_ts'\] or 0),

        }

    def get\_result\_type(self): return Types.MAP(Types.STRING(), Types.PICKLED\_BYTE\_ARRAY())

    def get\_accumulator\_type(self): return Types.MAP(Types.STRING(), Types.PICKLED\_BYTE\_ARRAY())

sessions \= stream \\

    .key\_by(lambda e: e\['user\_id'\]) \\

    .window(EventTimeSessionWindows.with\_gap(Time.minutes(30))) \\

    .aggregate(SessionAggregator()) \\

    .map(lambda acc: json.dumps({

        'user\_id':       acc.get('user\_id'),

        'event\_count':   acc\['event\_count'\],

        'page\_count':    len(acc\['pages'\]),

        'duration\_ms':   (acc\['max\_ts'\] or 0\) \- (acc\['min\_ts'\] or 0),

    }))

env.execute('user\_session\_analytics')

# **9\. Streaming Monitoring, Observability & Best Practices**

## **9.1 Key Metrics to Monitor**

| Metric | What It Tells You |
| :---- | :---- |
| Consumer lag (records) | How far behind the consumer is from the latest offset. Alert if \> 10k records for critical topics. |
| Iterator age (Kinesis) | Age of oldest unprocessed record. High value \= consumer lag. |
| Processing time per batch | How long each micro-batch takes. Should be \< trigger interval. |
| Records per second (throughput) | Throughput at producer and consumer. Alert on sudden drops. |
| Dead letter queue depth | Failed events accumulating. Indicates a processing error pattern. |
| State store size | Growing indefinitely indicates a watermark/eviction issue. |
| Checkpoint duration | Time to take a checkpoint. High value indicates backpressure. |

## **9.2 Dead Letter Queue Pattern**

### **dlq\_handler.py**

from confluent\_kafka import Consumer, Producer

import json, logging, time

logger \= logging.getLogger(\_\_name\_\_)

def forward\_to\_dlq(producer: Producer, original\_topic: str,

                   msg\_value: bytes, error: Exception, attempt: int):

    dlq\_record \= {

        'original\_topic': original\_topic,

        'error\_type':     type(error).\_\_name\_\_,

        'error\_message':  str(error),

        'attempt':        attempt,

        'failed\_at':      time.time(),

        'payload':        msg\_value.decode('utf-8', errors='replace')

    }

    producer.produce(

        topic=f'{original\_topic}.dlq',

        value=json.dumps(dlq\_record).encode(),

    )

    producer.flush()

    logger.warning(f'Message forwarded to DLQ: {type(error).\_\_name\_\_}: {error}')

def retry\_with\_backoff(fn, max\_retries=3, base\_delay=1.0):

    for attempt in range(max\_retries):

        try:

            return fn()

        except Exception as e:

            if attempt \== max\_retries \- 1:

                raise

            delay \= base\_delay \* (2 \*\* attempt)

            logger.warning(f'Attempt {attempt+1} failed: {e}. Retrying in {delay}s')

            time.sleep(delay)

## **9.3 Streaming Best Practices**

* Idempotent consumers: Process the same message twice safely. Use ON CONFLICT DO NOTHING or check before writing.

* Avoid blocking in hot path: Database lookups in the critical path should use in-memory caches (Redis). Async enrichment where sub-second is not required.

* Schema evolution strategy: Use Avro \+ Schema Registry with backward/forward compatibility. Never break consumers by removing/renaming fields.

* Limit state accumulation: Always define watermarks. Without them, stateful operations hold state forever and cause OOM.

* Consumer group isolation: Separate consumer groups for each downstream consumer of the same topic. Each group maintains its own offset.

* Checkpoint frequently: For stateful Flink/Spark jobs, checkpoint every 30-60 seconds. Balance recovery time vs checkpoint overhead.

* Test with realistic data: Streaming bugs often appear with out-of-order, duplicate, or null events. Include these in test suites.

* Graceful shutdown: Handle SIGTERM in consumers. Flush in-flight messages, commit offsets, close connections cleanly.

## **9.4 Top 20 Streaming Interview Questions**

| Question | Key Answer Points |
| :---- | :---- |
| What is exactly-once processing? | Events processed precisely once — no loss, no duplicates. Requires idempotent producers \+ transactional consumers (Kafka) or distributed snapshots (Flink). |
| What is backpressure? | When a downstream system is slower than the upstream producer. Handled by: limiting maxOffsetsPerTrigger (Spark), consumer.pause() (Kafka), flow control (Flink). |
| Explain the difference between event time and processing time. | Event time: timestamp embedded in the event (when it happened). Processing time: when the system processes it. Difference matters for windowing and late data. |
| What is a tumbling vs sliding window? | Tumbling: non-overlapping fixed intervals (each event in exactly one window). Sliding: overlapping windows (one event in multiple windows). Session: dynamic gap-based. |
| How do you handle late-arriving data? | Define watermarks with acceptable lateness. Update existing windows (Flink: allowed lateness). Route very late events to a side output / DLT for manual review. |
| What is log compaction in Kafka? | Retains only the latest message per key. Older messages with same key are compacted away. Used for changelog topics and event sourcing read models. |
| How do you scale a streaming consumer? | Increase consumer instances in the group (up to \# partitions). Increase partition count of the topic. Optimize per-message processing time. |
| What is a savepoint in Flink? | Manually triggered persistent snapshot of job state. Used for: job upgrades, migration, A/B testing. Unlike checkpoints, savepoints are not deleted automatically. |
| How do you join two streams? | Flink: window join, interval join. Spark: stream-stream join with watermark. Kafka Streams: KStream-KTable join. Key consideration: alignment of watermarks. |
| What is the consumer group rebalance and how to minimize impact? | Triggered on join/leave of consumers. Use sticky partition assignor and incremental cooperative rebalance to minimize the number of partitions reassigned. |

# **10\. Quick Reference**

## **10.1 Streaming Tech Stack Comparison**

| Tool | Latency | Model | State | Best For |
| :---- | :---- | :---- | :---- | :---- |
| Kafka Consumer | 10-200ms | Event | None | Simple consume-process-produce |
| Faust (Python) | 10-500ms | Event | RocksDB | Python microservices, windowing |
| Spark Streaming | 0.5-30s | Micro-batch | Yes | Scale analytics, Delta Lake |
| Apache Flink | \<1ms-100ms | True stream | Very rich | CEP, financial, gaming |
| Kinesis+Lambda | 100ms-5s | Event | None | AWS-native, simple transforms |
| Kafka Streams | \<10ms | Event | RocksDB | Java-native, embedded in app |

## **10.2 Kafka Command Reference**

\# Create topic

kafka-topics.sh \--create \--topic my-topic \--partitions 12 \--replication-factor 3 \\

  \--bootstrap-server kafka:9092

\# Describe topic

kafka-topics.sh \--describe \--topic my-topic \--bootstrap-server kafka:9092

\# Check consumer group lag

kafka-consumer-groups.sh \--describe \--group my-group \--bootstrap-server kafka:9092

\# Reset offsets to beginning (for replay)

kafka-consumer-groups.sh \--reset-offsets \--to-earliest \--topic my-topic \\

  \--group my-group \--execute \--bootstrap-server kafka:9092

\# Reset offsets to timestamp

kafka-consumer-groups.sh \--reset-offsets \\

  \--to-datetime 2024-01-01T00:00:00.000 \\

  \--topic my-topic \--group my-group \--execute \\

  \--bootstrap-server kafka:9092

\# Produce test messages

kafka-console-producer.sh \--topic my-topic \--bootstrap-server kafka:9092

\# Consume from beginning

kafka-console-consumer.sh \--topic my-topic \--from-beginning \--bootstrap-server kafka:9092

## **10.3 Windowing Reference**

| Window Type | Definition | PySpark Example |
| :---- | :---- | :---- |
| Tumbling | Fixed, non-overlapping | F.window('ts', '5 minutes') |
| Sliding | Fixed, overlapping | F.window('ts', '10 minutes', '5 minutes') |
| Session | Dynamic, gap-based | EventTimeSessionWindows.with\_gap(30min) (Flink) |
| Global | No time bound, key-based | groupBy(key).agg(...)  (no window, infinite state) |

## **10.4 Glossary**

| Term | Definition |
| :---- | :---- |
| Offset | Position of a message within a Kafka partition. Consumers track offsets to know where they left off. |
| Consumer Group | Set of consumers sharing partition assignment. Each partition consumed by only one member at a time. |
| Watermark | A time threshold that defines how late an event can arrive and still be included in a window. |
| Checkpoint | Snapshot of a streaming job's state and progress. Used for fault tolerance and recovery. |
| Backpressure | Signal from a slow downstream to slow the upstream producer to prevent overload. |
| Dead Letter Topic | A Kafka topic that receives failed/unprocessable messages for later investigation and replay. |
| Exactly-once | Guarantee that each event is processed and results are committed exactly once. |
| State store | Persistent, queryable store for per-key state in streaming jobs (e.g. RocksDB). |
| Savepoint | User-triggered Flink state snapshot for intentional restarts, upgrades, or migrations. |
| CDC | Change Data Capture — capturing database row-level changes from the transaction log. |
| Shard | Kinesis unit of capacity. Fixed throughput per shard; scale by adding shards. |
| Schema Registry | Central store for Avro/Protobuf/JSON schemas. Enforces compatibility rules across producers/consumers. |

*── End of Streaming ETL Pipeline Guide ──*