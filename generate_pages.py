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
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Data Sheets</title>
    <meta name="description" content="{desc}">
    <script>(function(){{const s=localStorage.getItem('ds-theme');if(s==='light')document.documentElement.classList.remove('dark');else document.documentElement.classList.add('dark');}})();</script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body{{font-family:'Inter',sans-serif;}}
        .font-display,h1,h2,h3{{font-family:'Outfit',sans-serif;}}
        .grid-bg{{background-image:linear-gradient(rgba(0,0,0,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.05) 1px,transparent 1px);background-size:40px 40px;}}
        .dark .grid-bg{{background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);}}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen transition-colors duration-300">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>
<div class="fixed top-0 left-0 w-96 h-96 bg-{cat_color}-600/8 rounded-full blur-3xl pointer-events-none z-0"></div>

<!-- NAV -->
<nav class="fixed top-0 w-full z-50 bg-white/90 dark:bg-slate-950/90 backdrop-blur-xl border-b border-slate-200 dark:border-slate-800/60 transition-colors duration-300">
    <div class="max-w-7xl mx-auto px-4 md:px-6 py-3 md:py-4 flex items-center justify-between">
        <a href="../../index.html" class="no-underline"><span style="font-family:'Outfit',sans-serif;font-weight:700;letter-spacing:-.02em;" class="text-base md:text-xl text-slate-900 dark:text-slate-100 transition-colors duration-300">Data Sheets</span></a>
        <div class="flex items-center gap-1">
            <a href="../learn.html" class="px-3 md:px-5 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800/60 transition-all duration-200 no-underline">Learn</a>
            <a href="../practice.html" class="px-3 md:px-5 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800/60 transition-all duration-200 no-underline">Practice</a>
        </div>
        <button id="theme-toggle" title="Toggle theme" class="w-9 h-9 flex items-center justify-center rounded-lg text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-all duration-200">
            <i data-lucide="sun" class="w-5 h-5 hidden dark:block"></i>
            <i data-lucide="moon" class="w-5 h-5 block dark:hidden"></i>
        </button>
    </div>
</nav>

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
            <span class="inline-block px-3 py-1 rounded-full text-xs font-semibold mb-2 transition-colors border border-{cat_color}-200 dark:border-transparent" style="background:rgba(var(--cat-rgb),.1);color:var(--cat-text)">{cat}</span>
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

<script>
    lucide.createIcons();
    document.getElementById('theme-toggle').addEventListener('click',()=>{{const d=document.documentElement.classList.toggle('dark');localStorage.setItem('ds-theme',d?'dark':'light');}});
</script>
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
    # For light theme, we want a slightly darker version of the text color for the badge, or just use the same text color.
    # In dark mode, it looks good. Let's just pass them.
    topics_html = "\n".join(
        f'            <li class="flex items-start gap-3 text-slate-600 dark:text-slate-300 transition-colors"><i data-lucide="chevron-right" class="w-4 h-4 mt-0.5" style="color:{text}"></i><span>{t}</span></li>'
        for t in topics
    )
    badge_style = f"--cat-rgb:{rgb};--cat-text:{text}"
    content = template.format(
        title=title, icon=icon, cat=cat, cat_color=cat_color,
        desc=desc, topics_html=topics_html, badge_style=badge_style
    )
    # inline the style into the badge span directly
    content = content.replace(
        'style="background:rgba(var(--cat-rgb),.1);color:var(--cat-text)"',
        f'style="background:rgba({rgb},.15);color:{text}"'
    )
    path = os.path.join("pages", "learn", fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

print("Done!")


import glob
import os


def inject_sidebar_into_all_html():
    SIDEBAR_TEMPLATE = '''
<!-- SIDEBAR -->
<aside class="fixed top-16 left-0 h-[calc(100vh-4rem)] w-64 border-r border-slate-200 dark:border-slate-800/60 bg-white/50 dark:bg-slate-950/50 backdrop-blur-xl z-40 hidden lg:block overflow-y-auto py-8 px-6">
    <div class="mb-8">
        <a href="{prefix}learn.html" class="font-display font-bold text-slate-900 dark:text-white mb-4 text-sm uppercase tracking-wider block no-underline hover:text-blue-600 dark:hover:text-blue-400">Learn</a>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Programming</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/python.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Python</a></li>
                <li><a href="{prefix}learn/sql.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">SQL</a></li>
                <li><a href="{prefix}learn/bash.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Bash</a></li>
                <li><a href="{prefix}learn/powershell.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">PowerShell</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Concepts</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/de-fundamentals.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">DE Fundamentals</a></li>
                <li><a href="{prefix}learn/dsa-de.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">DSA for DE</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Tools</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/spark.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Spark</a></li>
                <li><a href="{prefix}learn/flink.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Flink</a></li>
                <li><a href="{prefix}learn/kafka.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Kafka</a></li>
                <li><a href="{prefix}learn/dbt.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">dbt</a></li>
                <li><a href="{prefix}learn/pandas.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Pandas</a></li>
                <li><a href="{prefix}learn/numpy.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">NumPy</a></li>
                <li><a href="{prefix}learn/airflow.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Airflow</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Cloud</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/aws.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">AWS</a></li>
                <li><a href="{prefix}learn/gcp.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">GCP</a></li>
                <li><a href="{prefix}learn/azure.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Azure</a></li>
                <li><a href="{prefix}learn/snowflake.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Snowflake</a></li>
                <li><a href="{prefix}learn/databricks.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Databricks</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">CI/CD</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/docker.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Docker</a></li>
                <li><a href="{prefix}learn/kubernetes.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Kubernetes</a></li>
                <li><a href="{prefix}learn/terraform.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Terraform</a></li>
                <li><a href="{prefix}learn/github.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">GitHub</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Design</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/system-design.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">System Design</a></li>
                <li><a href="{prefix}learn/pipeline-design.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Pipeline Design</a></li>
                <li><a href="{prefix}learn/de-architectures.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">DE Architectures</a></li>
            </ul>
        </div>
    </div>
    <div>
        <a href="{prefix}practice.html" class="font-display font-bold text-slate-900 dark:text-white mb-4 text-sm uppercase tracking-wider block no-underline hover:text-blue-600 dark:hover:text-blue-400">Practice</a>
        <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
            <li><a href="{prefix}practice.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Coming Soon</a></li>
        </ul>
    </div>
</aside>
'''
    html_files = glob.glob('pages/**/*.html', recursive=True)
    for html_file in html_files:
        if html_file.replace(chr(92)*2, '/').replace(chr(92), '/') in ['pages/learn.html', 'pages/practice.html']:
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '<!-- SIDEBAR -->' in content:
            continue
            
        normalized = html_file.replace(chr(92)*2, '/').replace(chr(92), '/')
        depth = len(normalized.split('/')) - 1
        prefix = '../' * (depth - 1)
        
        sidebar_rendered = SIDEBAR_TEMPLATE.replace('{prefix}', prefix)
        
        if '</nav>' in content:
            content = content.replace('</nav>', '</nav>\n' + sidebar_rendered + '\n<div class="lg:pl-64 w-full">')
            content = content.replace('</body>', '</div>\n</body>')
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)

inject_sidebar_into_all_html()
