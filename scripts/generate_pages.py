import os

pages = [
    # (filename, title, icon, category, cat_color, description, topics)
    ("python.html", "Python", "file-code", "Programming", "blue",
     "Core Python concepts for Data Engineers: syntax, OOP, data structures, file handling and best practices.",
     ["Variables, data types and operators", "Control flow: if/else, loops, comprehensions",
      "Functions, lambda, decorators and closures", "OOP: classes, inheritance, dunder methods",
      "Data structures: lists, dicts, sets, tuples", "File I/O: CSV, JSON, Parquet reading and writing",
      "Error handling and logging", "Virtual environments and package management"]),

    ("sql.html", "SQL", "database", "Programming", "blue",
     "SQL fundamentals through advanced techniques for querying, transforming and analyzing data at scale.",
     ["SELECT, WHERE, GROUP BY, HAVING, ORDER BY", "JOINs: INNER, LEFT, RIGHT, FULL, CROSS, SELF",
      "Subqueries and CTEs (WITH clause)", "Window functions: ROW_NUMBER, RANK, LAG, LEAD",
      "Aggregate functions and HAVING", "Indexes, query planning and EXPLAIN",
      "DDL and DML: CREATE, ALTER, INSERT, UPDATE, DELETE", "Database normalization and schema design"]),

    ("bash.html", "Bash Scripting", "terminal", "Programming", "blue",
     "Essential Bash commands and scripting for automating data workflows and system tasks.",
     ["Basic commands: ls, cd, cp, mv, rm", "File permissions and ownership (chmod, chown)",
      "Pipes (|) and redirections (>, >>, 2>)", "Variables and environment variables",
      "Control flow: if/else, for/while loops", "Functions and script arguments",
      "Text processing: grep, sed, awk", "Process management and job control"]),

    ("spark.html", "Apache Spark (PySpark)", "zap", "Tools", "orange",
     "Distributed data processing with Apache Spark and PySpark for large-scale data engineering.",
     ["Spark architecture: Driver, Executors, DAG", "RDDs, DataFrames and Datasets",
      "Transformations vs Actions", "PySpark DataFrames API",
      "Spark SQL and catalyst optimizer", "Partitioning, shuffling and skew handling",
      "Reading and writing: Parquet, Delta, JDBC", "Streaming with Structured Streaming"]),

    ("flink.html", "Apache Flink", "waves", "Tools", "orange",
     "Stateful stream processing with Apache Flink for real-time data pipelines.",
     ["Flink architecture and execution model", "DataStream API and Table API",
      "Event time vs processing time", "Watermarks and late data handling",
      "State management and checkpointing", "Windows: tumbling, sliding, session",
      "Connectors: Kafka, JDBC, S3", "Flink SQL for stream and batch processing"]),

    ("kafka.html", "Apache Kafka", "message-square", "Tools", "orange",
     "Event streaming platform for building real-time data pipelines and event-driven applications.",
     ["Kafka architecture: brokers, topics, partitions", "Producers, consumers and consumer groups",
      "Offsets, retention and replay", "Kafka Connect for source and sink connectors",
      "Kafka Streams for stream processing", "Schema Registry and Avro/Protobuf",
      "Replication, ISR and fault tolerance", "Kafka deployment and monitoring"]),

    ("dbt.html", "dbt (Data Build Tool)", "refresh-cw", "Tools", "orange",
     "Transform data in your warehouse using SQL with dbt — the T in modern ELT pipelines.",
     ["dbt project structure and configuration", "Models: staging, intermediate, mart layers",
      "Refs, sources and the DAG", "Jinja templating and macros",
      "Tests: schema tests and custom tests", "Snapshots for slowly changing dimensions",
      "dbt documentation and lineage graphs", "dbt Cloud vs dbt Core deployment"]),

    ("pandas.html", "Pandas", "table", "Tools", "orange",
     "Data manipulation and analysis with Pandas DataFrames for data engineering workflows.",
     ["Series and DataFrame fundamentals", "Reading data: CSV, JSON, Parquet, SQL",
      "Indexing: loc, iloc and boolean masks", "GroupBy, pivot_table and crosstab",
      "Merging, joining and concatenating", "Handling missing data",
      "Apply, map and vectorized operations", "Performance tips and chunked processing"]),

    ("numpy.html", "NumPy", "hash", "Tools", "orange",
     "Numerical computing with NumPy arrays for efficient data processing and mathematical operations.",
     ["ndarray creation and shape manipulation", "Indexing, slicing and boolean indexing",
      "Broadcasting rules and universal functions", "Linear algebra: dot, matmul, linalg",
      "Statistical functions: mean, std, percentile", "Vectorization vs Python loops",
      "Random number generation", "Saving and loading with .npy and .npz"]),

    ("airflow.html", "Apache Airflow", "wind", "Tools", "orange",
     "Workflow orchestration with Apache Airflow for scheduling and monitoring complex data pipelines.",
     ["DAGs: Directed Acyclic Graphs", "Operators: PythonOperator, BashOperator, sensors",
      "Task dependencies and trigger rules", "Variables, connections and secrets",
      "XComs for inter-task communication", "Scheduling with CRON expressions",
      "Dynamic DAG generation", "Airflow deployment: local, Docker, Kubernetes, MWAA"]),

    ("aws.html", "AWS for Data Engineering", "server", "Cloud", "cyan",
     "Amazon Web Services data engineering services: storage, processing, warehousing and orchestration.",
     ["S3: storage classes, lifecycle, partitioning", "Glue: crawlers, ETL jobs, Data Catalog",
      "Redshift: architecture, distribution, sort keys", "Lambda for serverless data processing",
      "EMR for Spark and Hadoop workloads", "Kinesis: Data Streams and Firehose",
      "Step Functions for orchestration", "Lake Formation and data governance"]),

    ("gcp.html", "GCP for Data Engineering", "server", "Cloud", "cyan",
     "Google Cloud Platform data engineering services: BigQuery, Dataflow, Pub/Sub and more.",
     ["BigQuery: architecture, slots, partitioning", "BigQuery SQL: arrays, structs, scripting",
      "Dataflow (Apache Beam) for ETL", "Pub/Sub for event streaming",
      "Cloud Composer (managed Airflow)", "Cloud Storage and data lake patterns",
      "Dataproc for Spark on GCP", "Data Catalog and Dataplex governance"]),

    ("azure.html", "Azure for Data Engineering", "server", "Cloud", "cyan",
     "Microsoft Azure data engineering stack: Synapse, Data Factory, ADLS and Databricks.",
     ["Azure Data Lake Storage Gen2 (ADLS)", "Azure Data Factory: pipelines and activities",
      "Azure Synapse Analytics: SQL pools", "Azure Databricks integration",
      "Event Hubs for streaming ingestion", "Azure Stream Analytics",
      "Azure Purview for data governance", "Azure DevOps for data pipeline CI/CD"]),

    ("snowflake.html", "Snowflake", "snowflake", "Cloud", "cyan",
     "Cloud data warehouse platform with a unique multi-cluster, shared-data architecture.",
     ["Snowflake architecture: virtual warehouses, storage", "Data loading: COPY INTO, Snowpipe",
      "Time Travel and Fail-Safe", "Streams and Tasks for CDC and automation",
      "Zero-copy cloning and data sharing", "Micro-partitions and clustering",
      "Snowpark for Python and Java", "Cost management and query profiling"]),

    ("databricks.html", "Databricks", "box", "Cloud", "cyan",
     "Unified analytics and data engineering platform built on Apache Spark with Delta Lake.",
     ["Databricks workspace and clusters", "Delta Lake: ACID transactions, versioning",
      "Unity Catalog for governance", "Databricks notebooks and jobs",
      "Delta Live Tables (DLT) pipelines", "Auto Loader for incremental ingestion",
      "MLflow for experiment tracking", "Databricks Asset Bundles (CI/CD)"]),

    ("regex.html", "Regex", "search", "Tools", "orange",
     "Master Regular Expressions for data cleaning, pattern matching and text processing in Python, SQL and Bash.",
     ["Literals and character classes ([a-z], \d, \s)", "Quantifiers (*, +, ?, {n,m})",
      "Anchors (^, $) and Word Boundaries (\\b)", "Groups and Capturing ((...), (?:...))",
      "Alternation (|) and Escaping (\\)", "Lookahead and Lookbehind assertions",
      "Regex in Python (re module)", "Regex in SQL (REGEXP, SIMILAR TO)"]),

    ("docker.html", "Docker", "container", "CI/CD", "green",
     "Containerization with Docker for consistent, reproducible data engineering environments.",
     ["Containers vs virtual machines", "Dockerfile: FROM, RUN, COPY, CMD, ENTRYPOINT",
      "Building and tagging images", "Docker volumes and bind mounts",
      "Docker Compose for multi-service apps", "Networking: bridge, host, overlay",
      "Docker registries: Docker Hub, ECR, GCR", "Best practices: layers, .dockerignore, multi-stage"]),

    ("kubernetes.html", "Kubernetes", "network", "CI/CD", "green",
     "Container orchestration with Kubernetes for deploying and scaling data engineering workloads.",
     ["Kubernetes architecture: control plane and nodes", "Pods, ReplicaSets and Deployments",
      "Services: ClusterIP, NodePort, LoadBalancer", "ConfigMaps and Secrets",
      "Persistent Volumes and PVCs", "Namespaces and RBAC",
      "Helm charts for package management", "Running Spark and Airflow on Kubernetes"]),

    ("terraform.html", "Terraform", "blocks", "CI/CD", "green",
     "Infrastructure as Code with Terraform for provisioning and managing cloud data infrastructure.",
     ["Terraform core concepts: providers, resources", "HCL syntax: variables, outputs, locals",
      "State management and remote backends", "Modules for reusable infrastructure",
      "Workspaces for environment management", "Data sources and dependencies",
      "Terraform plan, apply and destroy", "Provisioning DE infra: S3, Redshift, EMR"]),

    ("github.html", "GitHub & Git", "github", "CI/CD", "green",
     "Version control with Git and automation with GitHub Actions for data engineering workflows.",
     ["Git fundamentals: init, clone, add, commit, push", "Branching: GitFlow, trunk-based development",
      "Merging, rebasing and conflict resolution", "Pull requests and code review workflows",
      "GitHub Actions: workflows, triggers, jobs, steps", "CI pipelines for dbt, Python, SQL",
      "Secrets management in GitHub Actions", "Monorepo vs polyrepo patterns for DE"]),

    ("de-architectures.html", "DE Architectures", "map", "Design", "rose",
     "Modern data engineering architecture patterns: Lambda, Kappa, Data Mesh and Lakehouse.",
     ["Lambda Architecture: batch and speed layers", "Kappa Architecture: stream-only processing",
      "Data Lakehouse: Delta/Iceberg/Hudi", "Data Mesh: domain-oriented ownership",
      "Data Fabric and active metadata", "Medallion Architecture: Bronze, Silver, Gold",
      "Event-driven vs request-driven architectures", "Choosing the right architecture"]),
]

template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Data Cake</title>
    <meta name="description" content="{desc}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>
<div class="fixed top-0 left-0 w-96 h-96 bg-{cat_color}-600/8 rounded-full blur-3xl pointer-events-none z-0"></div>

<main class="relative z-10 pt-28 pb-20 px-6 max-w-4xl mx-auto">
    <a href="../learn.html" class="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm mb-8 no-underline transition-colors duration-200">
        <i data-lucide="arrow-left" class="w-4 h-4"></i>
        Back to Learn
    </a>

    <div class="flex items-start gap-5 mb-6">
        <div class="w-12 h-12 rounded-xl flex items-center justify-center bg-{cat_color}-100 dark:bg-{cat_color}-500/20 text-{cat_color}-600 dark:text-{cat_color}-400 transition-colors">
            <i data-lucide="{icon}" class="w-6 h-6"></i>
        </div>
        <div>
            <span class="inline-block px-3 py-1 rounded-full text-xs font-semibold mb-2 transition-colors border border-{cat_color}-200 dark:border-transparent" style="background:rgba({rgb},.15);color:{text}">{cat}</span>
            <h1 class="font-display font-bold text-3xl md:text-4xl text-slate-900 dark:text-white leading-tight transition-colors">{title}</h1>
        </div>
    </div>

    <p class="text-slate-600 dark:text-slate-400 text-lg mb-10 leading-relaxed max-w-2xl transition-colors">{desc}</p>

    <div class="bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-2xl p-8 mb-6 transition-colors shadow-sm dark:shadow-none">
        <h2 class="font-display font-bold text-xl text-slate-900 dark:text-white mb-6 transition-colors">What you'll learn</h2>
        <ul class="space-y-3">
{topics_html}
        </ul>
    </div>

    <div class="bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl p-8 text-center transition-colors shadow-sm dark:shadow-none">
        <div class="flex justify-center mb-3 text-slate-400 dark:text-slate-500 transition-colors">
            <i data-lucide="hammer" class="w-8 h-8"></i>
        </div>
        <h2 class="font-display font-bold text-xl text-slate-900 dark:text-white mb-2 transition-colors">Content Coming Soon</h2>
        <p class="text-slate-500 dark:text-slate-400 text-sm transition-colors">Detailed notes, cheat sheets and examples are being prepared.</p>
    </div>
</main>
</body>
</html>'''

color_map = {
    "blue": ("59,130,246", "#60a5fa"),
    "violet": ("139,92,246", "#a78bfa"),
    "orange": ("249,115,22", "#fb923c"),
    "cyan": ("6,182,212", "#22d3ee"),
    "green": ("34,197,94", "#4ade80"),
    "rose": ("244,63,94", "#fb7185"),
}

os.makedirs("pages/learn", exist_ok=True)

for fname, title, icon, cat, cat_color, desc, topics in pages:
    rgb, text = color_map[cat_color]
    topics_html = "\n".join(
        f'            <li class="flex items-start gap-3 text-slate-600 dark:text-slate-300 transition-colors"><i data-lucide="chevron-right" class="w-4 h-4 mt-0.5" style="color:{text}"></i><span>{t}</span></li>'
        for t in topics
    )
    content = template.format(
        title=title, icon=icon, cat=cat, cat_color=cat_color,
        desc=desc, topics_html=topics_html, rgb=rgb, text=text
    )
    path = os.path.join("pages", "learn", fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

print("Done!")
