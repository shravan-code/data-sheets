import os

# Subpages definition
subpages = [
    {
        "id": "core-concepts",
        "title": "1. Core Concepts",
        "icon": "book-open",
        "description": "What is Data Engineering, lifecycles, and team roles.",
        "content": """
<h2>What is Data Engineering?</h2>
<p>Data engineering is the practice of designing, building, and maintaining the systems and architecture that collect, store, and process data at scale. It transforms raw, messy data into clean, structured formats that downstream users (like data scientists and business analysts) can easily query and analyze.</p>

<div class="my-8">
<div class="mermaid">
flowchart LR
    A[Raw Data sources] -->|Extract & Load| B(Data Storage/Lake)
    B -->|Transform| C(Data Warehouse)
    C --> D[BI Dashboards]
    C --> E[Machine Learning]
    style A fill:#3b82f6,color:#fff
    style C fill:#8b5cf6,color:#fff
</div>
</div>

<h2>Data Engineer vs Data Scientist vs Data Analyst</h2>
<div class="grid grid-cols-1 md:grid-cols-3 gap-4 not-prose my-6">
    <div class="p-4 bg-blue-50 dark:bg-blue-500/10 border border-blue-100 dark:border-blue-500/20 rounded-xl">
        <h3 class="font-bold text-blue-700 dark:text-blue-400 mb-2">Data Engineer</h3>
        <p class="text-sm text-slate-600 dark:text-slate-300">Builds pipelines and architecture. Focuses on scalability, performance, and data quality. Tools: Spark, Kafka, SQL, Python.</p>
    </div>
    <div class="p-4 bg-violet-50 dark:bg-violet-500/10 border border-violet-100 dark:border-violet-500/20 rounded-xl">
        <h3 class="font-bold text-violet-700 dark:text-violet-400 mb-2">Data Scientist</h3>
        <p class="text-sm text-slate-600 dark:text-slate-300">Builds predictive models and algorithms. Focuses on statistics and machine learning. Tools: Pandas, Scikit-Learn, PyTorch.</p>
    </div>
    <div class="p-4 bg-orange-50 dark:bg-orange-500/10 border border-orange-100 dark:border-orange-500/20 rounded-xl">
        <h3 class="font-bold text-orange-700 dark:text-orange-400 mb-2">Data Analyst</h3>
        <p class="text-sm text-slate-600 dark:text-slate-300">Analyzes data to answer business questions. Focuses on reporting and visualization. Tools: SQL, Tableau, PowerBI.</p>
    </div>
</div>

<h2>Data Engineering Lifecycle</h2>
<ol>
    <li><strong>Generation:</strong> Data is created by upstream systems (apps, IoT devices, third-party APIs).</li>
    <li><strong>Storage:</strong> Raw data is stored reliably (e.g., in an Amazon S3 Data Lake).</li>
    <li><strong>Ingestion:</strong> Moving data from source to storage (Batch or Streaming).</li>
    <li><strong>Transformation:</strong> Cleaning, joining, and aggregating data (e.g., using dbt or Spark).</li>
    <li><strong>Serving:</strong> Delivering structured data to data warehouses or serving layers for querying.</li>
</ol>

<h2>Upstream & Downstream Systems</h2>
<p><strong>Upstream systems</strong> are the sources of data (the origin). If an upstream system changes its database schema without warning, the data pipeline breaks. This is a common pain point!</p>
<p><strong>Downstream systems</strong> consume the data produced by pipelines. These are BI tools, ML models, and business reports. They rely on the data being timely, accurate, and structured.</p>
        """
    },
    {
        "id": "pipeline-basics",
        "title": "2. Data Pipeline Basics",
        "icon": "git-branch",
        "description": "ETL vs ELT, batch vs streaming, and pipeline design principles.",
        "content": """
<h2>What is a Data Pipeline?</h2>
<p>A data pipeline is a set of automated processes that extract data from various sources, transform it into a usable format, and load it into a destination system for analysis.</p>

<h2>ETL vs ELT</h2>
<div class="flex flex-col gap-6 my-6">
    <div class="flex gap-4 items-start">
        <div class="w-16 h-16 shrink-0 bg-slate-100 dark:bg-slate-800 rounded-lg flex items-center justify-center font-bold text-xl text-slate-700 dark:text-slate-300">ETL</div>
        <div>
            <h3 class="font-bold mt-0 text-slate-900 dark:text-white">Extract, Transform, Load</h3>
            <p class="text-sm text-slate-600 dark:text-slate-400">Data is transformed in a separate processing engine (like Spark) <em>before</em> being loaded into the warehouse. Ideal for on-premise systems where warehouse compute is expensive or when heavy transformations are required before loading (e.g., masking PII).</p>
        </div>
    </div>
    <div class="flex gap-4 items-start">
        <div class="w-16 h-16 shrink-0 bg-blue-100 dark:bg-blue-900/50 rounded-lg flex items-center justify-center font-bold text-xl text-blue-700 dark:text-blue-400">ELT</div>
        <div>
            <h3 class="font-bold mt-0 text-slate-900 dark:text-white">Extract, Load, Transform</h3>
            <p class="text-sm text-slate-600 dark:text-slate-400">Data is loaded raw into the warehouse first, then transformed using the warehouse's own scalable compute (e.g., using dbt inside Snowflake or BigQuery). This is the modern standard for cloud data engineering.</p>
        </div>
    </div>
</div>

<h2>Batch vs Streaming vs Micro-batch</h2>
<ul>
    <li><strong>Batch Processing:</strong> Processing data in large, bounded chunks at scheduled intervals (e.g., every night at 2 AM). Tools: Airflow, Spark.</li>
    <li><strong>Streaming Processing:</strong> Processing data continuously as it arrives with sub-second latency. Tools: Flink, Kafka Streams.</li>
    <li><strong>Micro-batch:</strong> A hybrid approach where data is processed in very small, frequent batches (e.g., every 5 seconds). Tools: Spark Structured Streaming.</li>
</ul>

<h2>Pipeline Design Principles</h2>
<p>Modern data pipelines must be resilient. These three concepts are critical:</p>

<div class="grid grid-cols-1 gap-4 my-6 not-prose">
    <div class="border-l-4 border-emerald-500 pl-4 py-2">
        <h4 class="font-bold text-slate-900 dark:text-white">1. Idempotency</h4>
        <p class="text-sm text-slate-600 dark:text-slate-400">An idempotent pipeline produces the exact same result whether it is run once or a hundred times for the same time window. It prevents duplicate data if a job crashes and restarts.</p>
    </div>
    <div class="border-l-4 border-blue-500 pl-4 py-2">
        <h4 class="font-bold text-slate-900 dark:text-white">2. Replayability</h4>
        <p class="text-sm text-slate-600 dark:text-slate-400">The ability to easily re-run past data. If a bug is discovered in a transformation logic, you should be able to "replay" the pipeline for the last 30 days to fix the historical data.</p>
    </div>
    <div class="border-l-4 border-violet-500 pl-4 py-2">
        <h4 class="font-bold text-slate-900 dark:text-white">3. Backfilling</h4>
        <p class="text-sm text-slate-600 dark:text-slate-400">The process of loading historical data into a new pipeline or table. A well-designed pipeline allows you to pass a custom date range to compute past data.</p>
    </div>
</div>
        """
    },
    {
        "id": "data-storage",
        "title": "3. Data Storage",
        "icon": "database",
        "description": "Warehouses, Lakes, OLTP vs OLAP, and file formats.",
        "content": """
<h2>Databases vs Data Warehouses vs Data Lakes vs Lakehouse</h2>
<div class="overflow-x-auto my-6 not-prose">
    <table class="min-w-full text-sm text-left text-slate-600 dark:text-slate-300">
        <thead class="text-xs uppercase bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200">
            <tr>
                <th class="px-6 py-3">System</th>
                <th class="px-6 py-3">Data Type</th>
                <th class="px-6 py-3">Use Case</th>
                <th class="px-6 py-3">Examples</th>
            </tr>
        </thead>
        <tbody>
            <tr class="border-b dark:border-slate-800">
                <td class="px-6 py-4 font-bold">Database (OLTP)</td>
                <td class="px-6 py-4">Highly structured, normalized</td>
                <td class="px-6 py-4">Application backends, fast transactions</td>
                <td class="px-6 py-4">PostgreSQL, MySQL, MongoDB</td>
            </tr>
            <tr class="border-b dark:border-slate-800">
                <td class="px-6 py-4 font-bold">Data Warehouse (OLAP)</td>
                <td class="px-6 py-4">Structured, denormalized (Star Schema)</td>
                <td class="px-6 py-4">Analytics, BI reporting, aggregations</td>
                <td class="px-6 py-4">Snowflake, Redshift, BigQuery</td>
            </tr>
            <tr class="border-b dark:border-slate-800">
                <td class="px-6 py-4 font-bold">Data Lake</td>
                <td class="px-6 py-4">Structured, semi-structured, unstructured (images, text)</td>
                <td class="px-6 py-4">Cheap storage, Machine Learning, staging area</td>
                <td class="px-6 py-4">Amazon S3, Azure ADLS Gen2</td>
            </tr>
            <tr class="border-b dark:border-slate-800">
                <td class="px-6 py-4 font-bold">Lakehouse</td>
                <td class="px-6 py-4">Structured & unstructured with ACID transactions</td>
                <td class="px-6 py-4">Combines Warehouse reliability with Lake cheap storage</td>
                <td class="px-6 py-4">Databricks (Delta Lake), Apache Iceberg</td>
            </tr>
        </tbody>
    </table>
</div>

<h2>Row-based vs Columnar Storage</h2>
<p><strong>Row-based (e.g., PostgreSQL, CSV):</strong> Data is stored sequentially row by row. Great for writing new records quickly (OLTP).</p>
<p><strong>Columnar (e.g., Redshift, Parquet):</strong> Data is stored column by column. Great for analytics (OLAP) because reading only the specific columns you need is lightning fast, and identical data types compress beautifully.</p>

<h2>File Formats</h2>
<ul>
    <li><strong>Parquet:</strong> The king of data engineering. Columnar, highly compressed, strongly typed.</li>
    <li><strong>ORC:</strong> Similar to Parquet, heavily optimized for Hive environments.</li>
    <li><strong>Avro:</strong> Row-based, excellent for schema evolution. Heavily used with Kafka.</li>
    <li><strong>JSON:</strong> Semi-structured, human-readable, but slow to parse and uncompressed.</li>
    <li><strong>CSV:</strong> Text format. Prone to parsing errors (delimiters inside strings). Avoid for big data!</li>
</ul>

<h2>Storage Partitioning</h2>
<p>Partitioning means dividing your data into separate directories based on a column (usually a date). Instead of scanning a 10TB table, a query filtering `WHERE year=2023 AND month=10` will only scan the `/year=2023/month=10/` directory, drastically improving speed and reducing costs.</p>
        """
    },
    {
        "id": "data-modelling",
        "title": "4. Data Modelling",
        "icon": "layout-template",
        "description": "Star schemas, fact vs dimension tables, and SCDs.",
        "content": """
<h2>Fact Tables vs Dimension Tables</h2>
<p>Data modeling for analytics revolves around separating metrics from context.</p>
<ul>
    <li><strong>Fact Tables:</strong> Store quantitative, measurable events (e.g., Sales, Clicks, Transactions). They contain foreign keys to dimension tables and numeric metrics (e.g., amount, quantity). They are massive and append-only.</li>
    <li><strong>Dimension Tables:</strong> Store descriptive context (e.g., Customers, Products, Time). They contain primary keys and textual attributes. They are relatively small and frequently updated.</li>
</ul>

<h2>Star Schema vs Snowflake Schema</h2>
<div class="grid grid-cols-1 md:grid-cols-2 gap-8 my-6">
    <div>
        <h3 class="mt-0">Star Schema</h3>
        <p class="text-sm">A central Fact table directly connected to heavily denormalized Dimension tables. Forms a star shape. Fast to query due to fewer JOINs. The standard for BI.</p>
    </div>
    <div>
        <h3 class="mt-0">Snowflake Schema</h3>
        <p class="text-sm">Dimension tables are normalized (split into sub-dimensions). Saves storage space but requires complex, slow JOINs. Forms a snowflake shape.</p>
    </div>
</div>

<div class="my-8">
<div class="mermaid">
erDiagram
    FACT_SALES {
        int order_id
        int customer_id FK
        int product_id FK
        int date_id FK
        float total_amount
    }
    DIM_CUSTOMER {
        int customer_id PK
        string name
        string city
    }
    DIM_PRODUCT {
        int product_id PK
        string product_name
        string category
    }
    FACT_SALES }|--|| DIM_CUSTOMER : "made by"
    FACT_SALES }|--|| DIM_PRODUCT : "includes"
</div>
</div>

<h2>Slowly Changing Dimensions (SCD)</h2>
<p>How do we handle a user changing their address over time? SCD strategies solve this.</p>
<ul>
    <li><strong>Type 0:</strong> Never changes. (e.g., Date of Birth)</li>
    <li><strong>Type 1:</strong> Overwrite old data. You lose history. (e.g., correcting a typo in a name)</li>
    <li><strong>Type 2:</strong> Add a new row. Track history using `start_date`, `end_date`, and an `is_current` boolean flag. <strong>(The most common pattern)</strong></li>
    <li><strong>Type 3:</strong> Add a new column to the existing row for the "previous_value". Only keeps one level of history.</li>
</ul>

<h2>Data Vault</h2>
<p>An advanced modeling technique focused on agility and scale, consisting of Hubs (business keys), Links (relationships), and Satellites (descriptive attributes). Excellent for integrating dozens of source systems in enterprise lakes, but overkill for simple startups.</p>
        """
    },
    {
        "id": "ingestion-patterns",
        "title": "5. Data Ingestion Patterns",
        "icon": "download-cloud",
        "description": "CDC, Incremental vs Full Load, API and event-driven patterns.",
        "content": """
<h2>Full Load vs Incremental Load</h2>
<div class="bg-slate-100 dark:bg-slate-800/50 p-6 rounded-xl my-6 not-prose">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
            <h3 class="font-bold text-lg text-slate-900 dark:text-white mb-2">Full Load (Truncate & Load)</h3>
            <p class="text-sm text-slate-600 dark:text-slate-400">The entire source table is extracted and overwrites the destination table. Very simple, highly robust, but slow and expensive for large tables.</p>
        </div>
        <div>
            <h3 class="font-bold text-lg text-slate-900 dark:text-white mb-2">Incremental Load (Append/Merge)</h3>
            <p class="text-sm text-slate-600 dark:text-slate-400">Only extract rows that have been added or updated since the last run (using a `updated_at` watermark column). Fast and cheap, but logic is complex and prone to data drift if deletes occur.</p>
        </div>
    </div>
</div>

<h2>Change Data Capture (CDC)</h2>
<p>CDC is the ultimate solution for incremental ingestion. Instead of querying the database periodically, a CDC tool (like Debezium) reads the database's internal Write-Ahead Log (WAL or binlog).</p>
<ul>
    <li>It captures every single `INSERT`, `UPDATE`, and `DELETE` operation in real-time.</li>
    <li>It streams these events into Kafka.</li>
    <li><strong>Advantage:</strong> Near zero impact on the source database performance, and it captures hard deletes natively!</li>
</ul>

<h2>Event-driven Ingestion</h2>
<p>Data isn't pulled from a database; instead, the application pushes events (e.g., "UserClickedButton", "OrderPlaced") directly to an event bus (Kafka/Kinesis) the moment they occur. This is the foundation of real-time analytics.</p>

<h2>API-based Ingestion</h2>
<p>Pulling data from third-party SaaS applications (Salesforce, Zendesk, Stripe) using HTTP requests. Major challenges include handling rate limits, pagination, handling JSON nesting, and authentication (OAuth tokens). Tools like Fivetran and Airbyte dominate this space.</p>

<h2>File-based Ingestion</h2>
<p>Upstream systems dump CSV or JSON files into an S3 bucket or SFTP server daily. An orchestration tool (Airflow) triggers a job when the file arrives (e.g., using an S3 Sensor) to load it into the warehouse.</p>
        """
    },
    {
        "id": "processing-concepts",
        "title": "6. Data Processing Concepts",
        "icon": "cpu",
        "description": "Distributed computing, shuffling, skew, and evaluation strategies.",
        "content": """
<h2>Distributed Computing Basics</h2>
<p>When data is too large to fit in the RAM or hard drive of a single machine, we use distributed computing (like Spark). Data is split into chunks, and a cluster of computers (workers) processes the chunks in parallel, coordinated by a central master node.</p>

<h2>MapReduce Paradigm</h2>
<p>The foundational concept of big data processing, popularized by Hadoop.</p>
<ul>
    <li><strong>Map phase:</strong> Apply a function to every row independently in parallel across nodes. (e.g., convert text to uppercase).</li>
    <li><strong>Reduce phase:</strong> Bring related data together across the network to aggregate it. (e.g., SUM or COUNT).</li>
</ul>

<h2>Partitioning & Bucketing</h2>
<p>These are physical data organization techniques to speed up reads.</p>
<ul>
    <li><strong>Partitioning:</strong> Creating separate folders for unique values of a column (e.g., `/date=2023-01-01/`).</li>
    <li><strong>Bucketing:</strong> Dividing data into a fixed number of files based on a hash of a column (e.g., `hash(user_id) % 10`). Perfect for speeding up JOINs because the engine knows exactly which bucket contains which `user_id`.</li>
</ul>

<h2>Shuffling & Data Skew</h2>
<p><strong>Shuffling:</strong> When data must be moved between different nodes over the network (e.g., during a `GROUP BY` or `JOIN`). Shuffling is the most expensive, slowest operation in big data. Try to avoid it!</p>
<p><strong>Data Skew:</strong> When one node gets significantly more data to process than others because the data isn't distributed evenly (e.g., grouping by `country` where 90% of users are from the US). The whole job is bottlenecked by that single slow node. Solutions include salting (adding random numbers to keys).</p>

<h2>Lazy vs Eager Evaluation</h2>
<p><strong>Eager Evaluation (Pandas):</strong> As soon as you write a line of code, the data is processed immediately.</p>
<p><strong>Lazy Evaluation (Spark):</strong> Spark doesn't process anything when you define transformations. It waits until you call an "Action" (like `.show()` or `.write()`), looks at your entire pipeline, optimizes the query execution plan, and then executes it efficiently in one go.</p>

<h2>In-memory vs Disk-based Processing</h2>
<p>Hadoop MapReduce wrote intermediate results to disk after every step, making it extremely slow. Spark keeps intermediate results in RAM (in-memory), making it up to 100x faster, though it requires more expensive hardware.</p>
        """
    },
    {
        "id": "streaming-concepts",
        "title": "7. Streaming Concepts",
        "icon": "activity",
        "description": "Event time, windowing, watermarks, and exactly-once semantics.",
        "content": """
<h2>Event Streaming vs Message Queue</h2>
<ul>
    <li><strong>Message Queue (RabbitMQ, SQS):</strong> Designed for task queuing. Once a message is read by a consumer, it is deleted. Good for async microservices.</li>
    <li><strong>Event Stream (Kafka, Kinesis):</strong> An immutable, append-only log of events. Messages are kept for a retention period (e.g., 7 days) and can be read by multiple different consumers simultaneously. You can also "rewind" and replay events.</li>
</ul>

<h2>Event Time vs Processing Time</h2>
<div class="my-6 p-4 border-l-4 border-orange-500 bg-orange-50 dark:bg-orange-900/20 text-slate-800 dark:text-slate-200">
    <p class="mb-2"><strong>Event Time:</strong> The exact timestamp when the event actually occurred on the device (e.g., when the user clicked the button on their phone while offline in a tunnel).</p>
    <p><strong>Processing Time:</strong> The timestamp when your streaming server finally receives and processes the event (e.g., when the user exits the tunnel and regains signal, pushing the event 10 minutes later).</p>
    <p class="text-sm mt-2 opacity-80">Robust streaming systems MUST calculate metrics based on Event Time.</p>
</div>

<h2>Windowing</h2>
<p>Streaming data never ends. To calculate aggregates (like "clicks per minute"), we cut the stream into "windows".</p>
<ul>
    <li><strong>Tumbling Window:</strong> Fixed-size, non-overlapping windows. (e.g., 1:00-1:05, 1:05-1:10).</li>
    <li><strong>Sliding Window:</strong> Overlapping windows. (e.g., a 5-minute window that slides every 1 minute).</li>
    <li><strong>Session Window:</strong> Dynamic windows based on user activity. It groups events separated by a period of inactivity (e.g., group all clicks until the user goes idle for 30 mins).</li>
</ul>

<h2>Watermarking & Late-arriving Data</h2>
<p>If an event happened at 1:04 PM but arrives at the server at 1:15 PM due to network lag, how long should the 1:00-1:05 window wait before closing?</p>
<p>A <strong>Watermark</strong> is a threshold. If we set a watermark of 10 minutes, the 1:05 window won't be closed and finalized until the system sees an event with an event time of 1:15. Any data arriving later than the watermark is ignored or sent to a dead-letter queue.</p>

<h2>Delivery Semantics</h2>
<ul>
    <li><strong>At-most-once:</strong> Fire and forget. Messages might be lost, but never duplicated.</li>
    <li><strong>At-least-once:</strong> Guaranteed delivery. Messages will not be lost, but might be processed multiple times if a crash occurs. (Requires idempotent downstream pipelines).</li>
    <li><strong>Exactly-once:</strong> The holy grail. Guaranteed delivery with zero duplicates. Very complex and adds latency, supported by modern Kafka and Flink via transactional states.</li>
</ul>
        """
    },
    {
        "id": "data-quality",
        "title": "8. Data Quality",
        "icon": "check-circle",
        "description": "Validation, profiling, schema evolution, and data contracts.",
        "content": """
<h2>Dimensions of Data Quality</h2>
<p>Data quality is usually measured across these key dimensions:</p>
<ul>
    <li><strong>Accuracy:</strong> Does the data represent reality? (e.g., A negative user age is inaccurate).</li>
    <li><strong>Completeness:</strong> Is required data missing? (e.g., Too many NULL values in the email column).</li>
    <li><strong>Consistency:</strong> Is the data the same across different systems?</li>
    <li><strong>Timeliness:</strong> Is the data available when expected? (Stale data is useless).</li>
    <li><strong>Uniqueness:</strong> Are there accidental duplicate records?</li>
</ul>

<h2>Data Validation & Profiling</h2>
<p><strong>Profiling</strong> involves analyzing your raw data to understand its distribution, min/max values, and null rates (e.g., using Pandas Profiling or Great Expectations).<br>
<strong>Validation</strong> is the automated testing of data against rules. In dbt, this means writing tests to assert that `id` is `NOT NULL` and `UNIQUE`, or that `status IN ('active', 'pending', 'deleted')`.</p>

<h2>Schema Enforcement & Evolution</h2>
<p>When the upstream source adds a new column, or changes an `int` to a `string`, what happens?</p>
<ul>
    <li><strong>Schema Enforcement:</strong> The pipeline strictly rejects any data that doesn't match the expected schema (saving the warehouse from corruption).</li>
    <li><strong>Schema Evolution:</strong> The pipeline automatically detects the new column and safely alters the destination table to add it dynamically. Supported strongly by Delta Lake and Avro.</li>
</ul>

<h2>Data Contracts</h2>
<p>An emerging best practice. A Data Contract is an agreement between the Software Engineers (who generate data) and Data Engineers (who consume it). It defines the strict schema of events. If a software engineer tries to deploy a code change that breaks the contract (e.g., dropping a required field), the CI/CD pipeline fails, preventing data engineering pipelines from breaking in production.</p>

<h2>Null Handling & Deduplication</h2>
<p><strong>Nulls:</strong> You must decide whether to drop rows with NULLs, fill them with a default value (e.g., `0` or `"Unknown"`), or leave them. SQL handles NULLs weirdly (e.g., `NULL = NULL` is false).</p>
<p><strong>Deduplication:</strong> Easiest done using the `ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC)` window function in SQL, filtering for `row_num = 1` to keep only the most recent version of a record.</p>
        """
    },
    {
        "id": "governance",
        "title": "9. Data Governance & Observability",
        "icon": "shield",
        "description": "Lineage, cataloging, metadata, and access control.",
        "content": """
<h2>Data Lineage</h2>
<p>Lineage tracks the lifecycle of data from its origin, through all transformations, to its final destination in a BI dashboard. It answers the question: <em>"If I change this source column, which downstream reports will break?"</em> Tools like dbt automatically generate DAGs (Directed Acyclic Graphs) that visualize this lineage.</p>

<h2>Data Cataloging & Metadata Management</h2>
<p>As a data platform grows to thousands of tables, users can't find what they need. A Data Catalog (e.g., Alation, Atlan, AWS Glue Catalog) is a searchable inventory of all data assets. It stores <strong>metadata</strong> (data about data): table descriptions, column definitions, owners, and tags.</p>

<h2>Data Observability</h2>
<p>Inspired by software observability (Datadog/New Relic). It's the practice of monitoring the health of data pipelines automatically. Good observability tools (like Monte Carlo) use machine learning to detect anomalies without manual tests (e.g., "This table usually receives 10,000 rows a day, but today it received 0. Send an alert!").</p>

<h2>Access Control (RBAC vs ABAC)</h2>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6 not-prose">
    <div class="bg-slate-50 dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700">
        <h3 class="font-bold text-slate-900 dark:text-white mb-2">Role-Based Access Control (RBAC)</h3>
        <p class="text-sm text-slate-600 dark:text-slate-400">Permissions are granted based on user roles (e.g., `Marketing_Role` gets read access to the `marketing_db`). Simple and most common.</p>
    </div>
    <div class="bg-slate-50 dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700">
        <h3 class="font-bold text-slate-900 dark:text-white mb-2">Attribute-Based Access Control (ABAC)</h3>
        <p class="text-sm text-slate-600 dark:text-slate-400">Dynamic permissions based on attributes. (e.g., "A user can only see sales data if `user.region == data.region`"). Complex but highly secure.</p>
    </div>
</div>

<h2>PII & Data Masking</h2>
<p>Personally Identifiable Information (PII) like names, SSNs, and emails must be protected for GDPR/CCPA compliance.</p>
<ul>
    <li><strong>Masking:</strong> Replacing parts of data (e.g., `***-**-1234`).</li>
    <li><strong>Hashing:</strong> Running data through a one-way algorithm (e.g., SHA-256) so it's anonymized but still joinable across tables.</li>
    <li><strong>Tokenization:</strong> Replacing sensitive data with a random token, storing the mapping securely in a separate vault.</li>
</ul>
        """
    },
    {
        "id": "architecture-patterns",
        "title": "10. Pipeline Architecture Patterns",
        "icon": "layers",
        "description": "Lambda, Kappa, Medallion, and Event-driven architectures.",
        "content": """
<h2>Lambda Architecture</h2>
<p>An older architecture designed to handle both massive historical data and real-time data simultaneously.</p>
<ul>
    <li><strong>Batch Layer:</strong> Computes accurate, comprehensive views over all historical data (slow).</li>
    <li><strong>Speed Layer:</strong> Processes only recent, real-time data (fast, but potentially inaccurate).</li>
    <li><strong>Serving Layer:</strong> Merges the batch and speed views when a user queries.</li>
</ul>
<p><em>Downside:</em> You have to maintain two completely separate codebases for batch and streaming.</p>

<h2>Kappa Architecture</h2>
<p>A modern alternative to Lambda. It treats <strong>everything as a stream</strong>. Batch processing is just streaming over historical data very quickly. You use a single processing engine (like Flink or Kafka Streams) and a single codebase for both real-time and historical backfilling.</p>

<h2>Medallion Architecture</h2>
<p>The standard architectural pattern for Data Lakehouses (popularized by Databricks), organizing data into logical layers of increasing quality:</p>
<div class="space-y-4 my-6">
    <div class="p-4 bg-yellow-900/10 border-l-4 border-yellow-700 rounded-r-xl">
        <h3 class="font-bold text-yellow-800 dark:text-yellow-500 m-0">Bronze (Raw)</h3>
        <p class="text-sm mt-1 mb-0">Raw data exactly as it arrived from source systems. Unfiltered, unstructured, append-only history.</p>
    </div>
    <div class="p-4 bg-slate-300/20 border-l-4 border-slate-400 rounded-r-xl">
        <h3 class="font-bold text-slate-700 dark:text-slate-300 m-0">Silver (Cleaned & Conformed)</h3>
        <p class="text-sm mt-1 mb-0">Data is filtered, cleaned, deduplicated, and normalized. Joined to reference data. The "single source of truth" for the enterprise.</p>
    </div>
    <div class="p-4 bg-amber-200/20 border-l-4 border-amber-500 rounded-r-xl">
        <h3 class="font-bold text-amber-700 dark:text-amber-400 m-0">Gold (Aggregated & Business-ready)</h3>
        <p class="text-sm mt-1 mb-0">Highly aggregated star schemas, heavily optimized for specific BI dashboards and ML algorithms.</p>
    </div>
</div>

<h2>Event-driven Architecture</h2>
<p>Instead of running an Airflow job every hour to process files, the architecture reacts to events. When a file lands in S3, S3 sends an event to AWS Lambda, which immediately triggers the ingestion pipeline. Leads to lower latency.</p>

<h2>Microservices vs Monolithic Pipelines</h2>
<p><strong>Monolithic:</strong> A single massive Spark script reads data, cleans it, joins it, and writes it. Hard to debug and scale.</p>
<p><strong>Microservices (Modular):</strong> Breaking the pipeline into small, independent tasks (e.g., Task A extracts, Task B validates, Task C transforms). Managed by an orchestrator like Airflow. If Task B fails, you only rerun Task B.</p>
        """
    },
    {
        "id": "performance-scalability",
        "title": "11. Performance & Scalability",
        "icon": "zap",
        "description": "Scaling strategies, CAP theorem, and optimization techniques.",
        "content": """
<h2>Horizontal vs Vertical Scaling</h2>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6 not-prose">
    <div class="p-5 border border-slate-200 dark:border-slate-700 rounded-xl shadow-sm">
        <h3 class="font-bold text-slate-900 dark:text-white flex items-center gap-2"><i data-lucide="arrow-up" class="w-5 h-5 text-blue-500"></i> Vertical Scaling (Scale Up)</h3>
        <p class="text-sm text-slate-600 dark:text-slate-400 mt-2">Adding more RAM and CPU to a single machine. Easy to do (no code changes), but hits a physical limit and gets extremely expensive.</p>
    </div>
    <div class="p-5 border border-slate-200 dark:border-slate-700 rounded-xl shadow-sm">
        <h3 class="font-bold text-slate-900 dark:text-white flex items-center gap-2"><i data-lucide="arrow-right-left" class="w-5 h-5 text-green-500"></i> Horizontal Scaling (Scale Out)</h3>
        <p class="text-sm text-slate-600 dark:text-slate-400 mt-2">Adding more cheap machines to the cluster. Infinite scalability, but requires distributed computing software (Spark/Hadoop) to manage.</p>
    </div>
</div>

<h2>CAP Theorem</h2>
<p>In a distributed data system, you can only guarantee TWO of the following three properties simultaneously:</p>
<ul>
    <li><strong>Consistency (C):</strong> Every read receives the most recent write.</li>
    <li><strong>Availability (A):</strong> Every request receives a non-error response (system is always up).</li>
    <li><strong>Partition Tolerance (P):</strong> The system continues to operate despite network failures dropping messages between nodes.</li>
</ul>
<p>Since network failures (P) are unavoidable, you must choose between CP (consistent but might go offline) and AP (always online but data might be stale for a few seconds).</p>

<h2>Consistency Models</h2>
<p><strong>Strong Consistency:</strong> Once data is written, all subsequent reads instantly see it (relational DBs).</p>
<p><strong>Eventual Consistency:</strong> After writing data, it might take a few seconds to propagate across all servers. Reads might return old data briefly (e.g., DynamoDB, Cassandra). Highly available and scalable.</p>

<h2>Caching Strategies</h2>
<p>Caching stores frequently accessed data in fast RAM (e.g., Redis) rather than slow disks.</p>
<ul>
    <li><strong>Read-through:</strong> App asks cache. If miss, cache loads from DB and returns.</li>
    <li><strong>Write-through:</strong> App writes to cache, cache writes to DB synchronously.</li>
    <li><strong>Write-behind:</strong> App writes to cache, cache asynchronously writes to DB in batches (fastest, but risky if cache crashes).</li>
</ul>

<h2>The Small File Problem</h2>
<p>HDFS and S3 hate millions of tiny 10KB files. They cause massive metadata overhead, making listing and reading agonizingly slow. Big data engines (like Spark) perform best with files around 128MB to 1GB. <br><strong>Solution:</strong> Run periodic compaction jobs that read thousands of tiny streaming files and rewrite them as a few large Parquet files.</p>
        """
    },
    {
        "id": "devops",
        "title": "12. DevOps for DE",
        "icon": "settings",
        "description": "CI/CD, testing, monitoring, and SLAs for pipelines.",
        "content": """
<h2>Version Control for Pipelines</h2>
<p>Data engineering has evolved. We no longer write stored procedures manually in a production database. All SQL queries, Spark scripts, and infrastructure configurations (Terraform) must be committed to Git. This provides an audit trail, rollback capabilities, and peer review via Pull Requests.</p>

<h2>CI/CD for Data Pipelines</h2>
<p><strong>Continuous Integration (CI):</strong> When code is pushed, automated servers (GitHub Actions) run tests to ensure SQL syntax is correct and Python code passes linting.</p>
<p><strong>Continuous Deployment (CD):</strong> If tests pass, the code is automatically deployed to a staging environment, tested against dummy data, and then promoted to production orchestration tools.</p>

<h2>Testing Data Pipelines</h2>
<ul>
    <li><strong>Unit Testing:</strong> Testing a single Python transformation function using `pytest` with a small, mocked DataFrame.</li>
    <li><strong>Integration Testing:</strong> Running the full pipeline on a localized database or staging environment to ensure all components talk to each other correctly.</li>
    <li><strong>Data Testing:</strong> Testing the actual data running through production (e.g., dbt tests asserting no nulls).</li>
</ul>

<h2>Monitoring & Alerting</h2>
<p>Pipelines fail silently if not monitored. You must monitor:</p>
<ul>
    <li><strong>Infrastructure metrics:</strong> CPU, Memory, Disk space.</li>
    <li><strong>Pipeline metrics:</strong> Job execution time, failure rates.</li>
    <li><strong>Data metrics:</strong> Volume of rows ingested, percentage of nulls.</li>
</ul>
<p>Alerts should be routed to Slack or PagerDuty, but avoid <em>Alert Fatigue</em> by only alarming on critical issues.</p>

<h2>SLA / SLO / SLI for Pipelines</h2>
<p>Borrowed from Site Reliability Engineering (SRE):</p>
<div class="my-6 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-200 dark:border-slate-700 not-prose">
    <p><strong>Service Level Indicator (SLI):</strong> The actual metric you measure. (e.g., "The pipeline finishes by 8:00 AM on 95% of days").</p>
    <p class="mt-2"><strong>Service Level Objective (SLO):</strong> The internal target you want to hit. (e.g., "We aim for 99% completion by 8:00 AM").</p>
    <p class="mt-2"><strong>Service Level Agreement (SLA):</strong> The external, legally binding promise to stakeholders. (e.g., "If the dashboard is not updated by 9:00 AM, we owe a financial penalty").</p>
</div>
        """
    }
]

hub_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DE Fundamentals Roadmap — Data Cake</title>
    <meta name="description" content="Master the core principles of data engineering with our 11-phase structured roadmap.">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <style>
        .roadmap-hero-bg {{
            background-image: radial-gradient(circle at 2px 2px, rgba(0,0,0,0.03) 1px, transparent 0);
            background-size: 24px 24px;
        }}
        .dark .roadmap-hero-bg {{
            background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.03) 1px, transparent 0);
        }}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <div id="ds-main-content">
        <main class="relative z-10 pt-24 pb-20 px-6 max-w-5xl mx-auto">
            <!-- HERO -->
            <header class="roadmap-hero-bg mb-20 p-10 md:p-14 rounded-[48px] border-2 border-violet-100 dark:border-slate-800 bg-white dark:bg-slate-900 relative overflow-hidden shadow-2xl shadow-violet-500/10">
                <div class="absolute -top-24 -right-24 w-80 h-80 bg-violet-500/10 blur-[100px] rounded-full"></div>
                <div class="absolute -bottom-24 -left-24 w-80 h-80 bg-violet-500/5 blur-[100px] rounded-full"></div>
                
                <div class="relative z-10">
                    <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-violet-100 text-violet-700 rounded-full text-xs font-black uppercase tracking-widest mb-8 border-2 border-violet-200/50">
                        <i data-lucide="layers" class="w-4 h-4"></i>
                        Core Concepts
                    </div>
                    <h1 class="font-display text-5xl md:text-7xl font-black text-slate-900 dark:text-white mb-6 tracking-tight leading-[1.1]">
                        DE <span class="bg-gradient-to-r from-violet-600 to-violet-400 bg-clip-text text-transparent">Fundamentals</span>
                    </h1>
                    <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl leading-relaxed mb-0 font-medium italic">
                        "The definitive guide to the foundational principles of Data Engineering. From lifecycles and storage to distributed computing and observability."
                    </p>
                </div>
            </header>

            <!-- ROADMAP TIMELINE -->
            <div class="max-w-4xl mx-auto">
                {phases_html}
            </div>
        </main>
    </div>
</body>
</html>'''

subpage_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Data Sheets</title>
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        const isDark = document.documentElement.classList.contains('dark');
        mermaid.initialize({{ startOnLoad: true, theme: isDark ? 'dark' : 'default', themeVariables: {{ fontFamily: 'Inter' }} }});
    </script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>

<div class="flex justify-center max-w-[1440px] mx-auto">
    <main class="relative z-10 pt-28 pb-32 px-6 w-full max-w-3xl">
        <a href="../de-fundamentals.html" class="inline-flex items-center gap-2 text-sm font-medium text-violet-600 dark:text-violet-400 hover:text-violet-700 dark:hover:text-violet-300 transition-colors mb-6 group no-underline">
            <i data-lucide="arrow-left" class="w-4 h-4 transition-transform group-hover:-translate-x-1"></i>
            Back to DE Fundamentals
        </a>

        <h1 class="font-display font-bold text-4xl md:text-5xl text-slate-900 dark:text-white mb-4 leading-tight">{title}</h1>
        <p class="text-xl text-slate-600 dark:text-slate-400 mb-12">{description}</p>
        
        <div class="prose prose-slate dark:prose-invert prose-lg max-w-none">
            {content}
        </div>
        
        <div class="mt-20"></div>
    </main>

    <aside class="toc-container">
        <div class="toc-title">On this page</div>
        <ul class="toc-list"></ul>
        {topics_list_html}
    </aside>
</div>
</body>
</html>'''

# 1. Build Hub Page
subpages.sort(key=lambda x: int(x['title'].split('.')[0]))
phases = [
    {"name": "The Foundation", "items": [subpages[0]]},
    {"name": "Pipeline Basics", "items": [subpages[1]]},
    {"name": "Storage Strategy", "items": [subpages[2]]},
    {"name": "Data Modelling", "items": [subpages[3]]},
    {"name": "Ingestion Patterns", "items": [subpages[4]]},
    {"name": "Processing Core", "items": [subpages[5]]},
    {"name": "Streaming Mastery", "items": [subpages[6]]},
    {"name": "Data Quality", "items": [subpages[7]]},
    {"name": "Governance & Observability", "items": [subpages[8]]},
    {"name": "Advanced Architectures", "items": [subpages[9]]},
    {"name": "Performance & DevOps", "items": [subpages[10], subpages[11]]}
]

phases_html = ""
for i, phase in enumerate(phases):
    num = i + 1
    items_html = ""
    for page in phase["items"]:
        items_html += f"""
        <a href="de-fundamentals/{page['id']}.html" class="flex items-center gap-3 p-3 bg-violet-50/30 dark:bg-slate-900 border border-violet-100/50 dark:border-slate-800 rounded-xl transition-all hover:bg-violet-50 dark:hover:bg-violet-900/20 hover:border-violet-200 group/item no-underline">
            <div class="w-8 h-8 rounded-lg bg-violet-100 dark:bg-violet-900/50 flex items-center justify-center text-violet-600 dark:text-violet-400 group-hover/item:bg-violet-600 group-hover/item:text-white transition-all">
                <i data-lucide="{page['icon']}" class="w-4 h-4"></i>
            </div>
            <span class="text-sm font-semibold text-slate-700 dark:text-slate-300 group-hover/item:text-violet-700 transition-colors">{page['title']}</span>
        </a>"""

    phases_html += f"""
    <section class="mb-12">
        <div class="flex items-center gap-4 mb-8">
            <div class="w-10 h-10 rounded-xl bg-violet-500/10 flex items-center justify-center text-violet-600">
                <span class="text-sm font-black">{num}</span>
            </div>
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white font-display tracking-tight">{phase['name']}</h2>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {items_html}
        </div>
    </section>"""

hub_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DE Fundamentals — Data Cake</title>
    <meta name="description" content="Master the core principles of data engineering with our structured guide.">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <div id="ds-main-content">
        <main class="relative z-10 pt-24 pb-20 px-6 max-w-5xl mx-auto">
            <!-- HERO -->
            <header class="mb-20 text-center">
                <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-violet-100 text-violet-700 rounded-full text-[10px] font-black uppercase tracking-widest mb-8 border-2 border-violet-200/50">
                    <i data-lucide="layers" class="w-3 h-3"></i> Core Concepts
                </div>
                <h1 class="font-display text-5xl md:text-7xl font-black text-slate-900 dark:text-white mb-6 tracking-tight leading-tight">
                    DE <span class="bg-gradient-to-r from-violet-600 to-violet-400 bg-clip-text text-transparent">Fundamentals</span>
                </h1>
                <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed font-medium italic">
                    "The definitive guide to the foundational principles of Data Engineering. From lifecycles and storage to distributed computing and observability."
                </p>
            </header>

            <!-- CARD CONTENT -->
            <div class="space-y-16">
                {phases_html}
            </div>
            
            <footer class="mt-20 py-10 border-t border-slate-200 dark:border-slate-800 text-center">
                <p class="text-slate-400 font-medium text-xs tracking-widest uppercase text-[10px]">\u00a9 2026 Data Cake \u2022 Foundations Mastery</p>
            </footer>
        </main>
    </div>
    <script>lucide.createIcons();</script>
</body>
</html>'''

hub_content = hub_template.format(phases_html=phases_html)
os.makedirs("pages/learn", exist_ok=True)
with open("pages/learn/de-fundamentals.html", "w", encoding="utf-8") as f:
    f.write(hub_content)

print("Created Hub: pages/learn/de-fundamentals.html")

# 2. Build Subpages
os.makedirs("pages/learn/de-fundamentals", exist_ok=True)
for i, page in enumerate(subpages):
    # Navigation logic
    prev_page = subpages[i-1] if i > 0 else None
    next_page = subpages[i+1] if i < len(subpages)-1 else None

    prev_html = ""
    if prev_page:
        prev_html = f"""
        <a href="{prev_page['id']}.html" class="nav-card prev">
            <span class="nav-label"><i data-lucide="arrow-left"></i> Previous</span>
            <span class="nav-title">{prev_page["title"]}</span>
        </a>"""
        
    next_html = ""
    if next_page:
        next_html = f"""
        <a href="{next_page['id']}.html" class="nav-card next">
            <span class="nav-label">Next <i data-lucide="arrow-right"></i></span>
            <span class="nav-title">{next_page["title"]}</span>
        </a>"""

    # Build list of all topics for the sidebar
    topics_html = '<div class="toc-title mt-8">Fundamentals</div><ul class="toc-list">'
    for p in subpages:
        active_cls = "active" if p['id'] == page['id'] else ""
        topics_html += f'<li><a href="{p["id"]}.html" class="toc-link {active_cls}">{p["title"]}</a></li>'
    topics_html += '</ul>'

    content = subpage_template.format(
        title=page["title"],
        description=page["description"],
        content=page["content"],
        topics_list_html=topics_html
    )

    # Inject Navigation Cards
    nav_html = f"""
    <div class="nav-container">
        {prev_html if prev_html else "<div></div>"}
        {next_html if next_html else "<div></div>"}
    </div>
    """
    content = content.replace('</main>', nav_html + '</main>')

    path = os.path.join("pages", "learn", "de-fundamentals", f"{page['id']}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created Subpage: {path}")

print("Successfully generated all Data Engineering Fundamentals subpages!")
