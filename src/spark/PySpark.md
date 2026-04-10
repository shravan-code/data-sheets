   
   
   
   
 

| 🔥 PySpark The Complete Engineering Guide ───────────────────────────────────────────── Architecture  ·  Memory  ·  DataFrame API  ·  All Methods & Modules Data Warehouse  ·  Data Lake  ·  Lakehouse  ·  Data Mesh AWS  ·  Azure  ·  GCP  — With Clean Architecture Diagrams |
| :---: |

   
   
Version 2.0  |  March 2026  |  Comprehensive Reference Edition

# **Chapter 1 — Why PySpark? The Problem It Solves**

| Understanding the Big Data Problem & the Birth of Apache Spark |
| :---: |

 

## **1.1  The Traditional Single-Machine Bottleneck**

Before Spark, engineers used tools like Pandas, SQL on a single server, or custom scripts. These tools work perfectly for datasets that fit in RAM — typically up to a few GB. As organizations began generating terabytes and petabytes of data daily, single-machine tools became impossibly slow or simply crashed.

 

| Challenge | Scale | Impact Without Spark |
| :---- | :---- | :---- |
| Volume — Logs, IoT, Transactions | Terabytes to Petabytes daily | Single machine runs out of RAM/disk; jobs take days |
| Velocity — Real-time event streams | Millions of events per second | Batch tools can't keep up; stale data for decisions |
| Variety — JSON, CSV, images, blobs | All data types simultaneously | Single-schema tools can't handle semi/unstructured |
| Fault Tolerance — Hardware fails | Any node can die anytime | One failure kills the entire job — no recovery |
| Cost Scaling — Bigger machine | Single-node scale-up is $$$ | 10x data \= 10x hardware cost on one machine |

 

## **1.2  The Hadoop Era — MapReduce's Limitations**

Apache Hadoop (2006) introduced distributed storage (HDFS) and processing (MapReduce). It solved the scale problem but introduced new pain: every intermediate step wrote results to disk, making iterative algorithms (like ML training) extremely slow. A 10-iteration ML job would read/write disk 20+ times.

 

## **1.3  Apache Spark — Born at UC Berkeley AMPLab (2009)**

Spark was designed from scratch to overcome MapReduce's disk-I/O bottleneck. The key insight: keep data in distributed RAM (memory) across a cluster and only write to disk when absolutely necessary. The result: 10-100x faster than MapReduce for iterative workloads.

 

| Dimension | Hadoop MapReduce | Apache Spark |
| :---- | :---- | :---- |
| Processing Model | Disk-bound (read/write every step) | In-memory DAG (writes to disk only on spill) |
| Speed | Baseline | 10-100x faster for iterative workloads |
| Language APIs | Java only (originally) | Scala, Java, Python (PySpark), R, SQL |
| Data Abstraction | Key-Value pairs only | RDD → DataFrame → Dataset (typed) |
| Streaming | No native streaming | Structured Streaming built-in |
| Machine Learning | Mahout (external) | MLlib built-in |
| SQL | Hive (external, slow) | Spark SQL with Catalyst optimizer |
| Fault Tolerance | Replicates data to HDFS | Recomputes via lineage (DAG) — no replication needed |

 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## **1.4  Why Python? PySpark's Role**

Spark is written in Scala/Java. PySpark is the Python API for Spark, introduced to democratize Spark for the vast Python data community. It uses Py4J — a library that lets Python programs communicate with JVM objects. Your Python code drives the logic; the JVM and cluster do the heavy lifting.

 

▲ PySpark Cluster Architecture — Client, Driver, Cluster Manager, Worker Nodes

# 

# 

# 

# 

# 

# 

# **Chapter 2 — PySpark Architecture Deep Dive**

| Master-Worker Architecture · DAG · Transformations vs Actions |
| :---: |

 

## **2.1  SparkSession — The Entry Point**

SparkSession (introduced in Spark 2.0) is the unified entry point. It combines SparkContext, SQLContext, and HiveContext. Every PySpark application starts by creating a SparkSession.

| from pyspark.sql import SparkSession spark \= SparkSession.builder \\     .appName('MyApp') \\     .master('yarn')                        \# yarn | local\[\*\] | k8s://... | spark://host:7077     .config('spark.executor.memory', '4g') \\     .config('spark.executor.cores', '2') \\     .config('spark.executor.instances', '10') \\     .config('spark.dynamicAllocation.enabled', 'true') \\     .config('spark.sql.adaptive.enabled', 'true') \\   \# AQE — Spark 3.0+     .config('spark.serializer', 'org.apache.spark.serializer.KryoSerializer') \\     .enableHiveSupport() \\                            \# optional: Hive metastore     .getOrCreate()                                     \# reuse if already exists sc  \= spark.sparkContext                  \# access SparkContext sql \= spark.sql                           \# run SQL print(spark.version)                      \# '3.5.0' print(sc.master)                          \# 'yarn' print(sc.defaultParallelism)              \# depends on cluster spark.stop()                              \# always stop when done |
| :---- |

 

| OUTPUT | Spark Version: 3.5.0 Master: yarn Default Parallelism: 40 |
| :---: | :---- |

 

## 

## 

## 

## 

## **2\.  The DAG — Directed Acyclic Graph**

When you write PySpark code, nothing executes immediately. Spark builds a DAG of transformations. Only when you call an Action does Spark submit the DAG to the cluster for execution. The DAGScheduler converts the logical plan into Stages and Tasks.

▲ DAG Execution Pipeline — From User Code to Parallel Cluster Tasks

 

## 

## 

## 

## 

## 

## 

## 

## **2.3  Transformations vs Actions — The Fundamental Distinction**

This is the single most important concept in Spark. Transformations are lazy — they describe what to do without doing it. Actions trigger all accumulated transformations to execute.

 

| Type | Method | Description | Triggers Execution? |
| :---- | :---- | :---- | :---- |
| Transformation | filter() / where() | Keep rows matching condition | No |
| Transformation | select() / selectExpr() | Select/derive columns | No |
| Transformation | withColumn() | Add or replace a column | No |
| Transformation | groupBy() | Group rows by key(s) | No |
| Transformation | join() | Join two DataFrames | No |
| Transformation | repartition() / coalesce() | Change partition count | No |
| Transformation | orderBy() / sort() | Sort rows | No |
| Transformation | distinct() / dropDuplicates() | Remove duplicates | No |
| Transformation | union() / unionByName() | Stack DataFrames | No |
| Transformation | cache() / persist() | Mark for caching | No (caches on first action) |
| ACTION | show() | Print N rows to console | YES — triggers full DAG |
| ACTION | count() | Return row count as int | YES — triggers full DAG |
| ACTION | collect() | Return all rows to driver | YES — careful with large data |
| ACTION | take(n) / head(n) | Return first N rows | YES — triggers full DAG |
| ACTION | first() | Return first row | YES — triggers full DAG |
| ACTION | write.\*(...) | Write to storage | YES — triggers full DAG |
| ACTION | toPandas() | Convert to Pandas DataFrame | YES — triggers full DAG |
| ACTION | foreach() / foreachPartition() | Apply function to rows | YES — triggers full DAG |
| ACTION | reduce() | Aggregate with function | YES — triggers full DAG |
| ACTION | aggregate() | RDD-style aggregate | YES — triggers full DAG |

 

# **Chapter 3 — Memory Architecture & Management**

| Unified Memory Model · Off-Heap · Caching · Serialization · Tuning |
| :---: |

 

## **3.1  Executor Memory Architecture**

Every executor is a JVM process running on a worker node. Its memory is divided into four regions. Understanding this is critical for preventing OOM errors and tuning performance.

 

▲ Spark Executor Memory Architecture — Unified Memory Model with Configuration Parameters

 

## **3.2  Storage Levels for Caching**

| from pyspark import StorageLevel df \= spark.read.parquet('s3://bucket/large-dataset/') \# Default — MEMORY\_AND\_DISK (deserialized) df.cache()      \# same as persist(StorageLevel.MEMORY\_AND\_DISK\_DESER) \# Explicit storage levels (use based on memory vs speed trade-off) df.persist(StorageLevel.MEMORY\_ONLY)           \# fastest, OOM risk on large data df.persist(StorageLevel.MEMORY\_ONLY\_SER)       \# serialized — less RAM, slower access df.persist(StorageLevel.MEMORY\_AND\_DISK)       \# spills to disk if RAM full df.persist(StorageLevel.MEMORY\_AND\_DISK\_SER)   \# serialized \+ disk spill df.persist(StorageLevel.DISK\_ONLY)             \# no RAM used at all df.persist(StorageLevel.DISK\_ONLY\_2)           \# replicated on 2 nodes on disk df.persist(StorageLevel.MEMORY\_ONLY\_2)         \# replicated on 2 nodes in memory df.persist(StorageLevel.MEMORY\_AND\_DISK\_2)     \# replicated on 2 nodes df.persist(StorageLevel.OFF\_HEAP)              \# Tungsten off-heap memory \# Check if cached print(df.is\_cached)                            \# True / False \# View cached datasets in storage spark.catalog.isCached('my\_table')             \# check table cache spark.catalog.cacheTable('my\_table')           \# cache a table spark.catalog.uncacheTable('my\_table') \# ALWAYS free memory when done df.unpersist()                                 \# removes from cache immediately |
| :---- |

 

## **3.3  Serialization**

| \# Kryo serialization — 2-10x faster, smaller than default Java serializer spark \= SparkSession.builder \\     .config('spark.serializer', 'org.apache.spark.serializer.KryoSerializer') \\     .config('spark.kryo.registrationRequired', 'false') \\     .config('spark.kryo.registrator', 'my.CustomRegistrator') \\  \# optional     .getOrCreate() \# Enable off-heap (Tungsten) — no JVM GC pressure spark.conf.set('spark.memory.offHeap.enabled', 'true') spark.conf.set('spark.memory.offHeap.size', '4g') |
| :---- |

 

# **Chapter 4 — DataFrame API: Complete Method Reference**

| Every Method with Code Examples and Output |
| :---: |

 

## **4.1  Creating DataFrames**

| from pyspark.sql import SparkSession, Row from pyspark.sql.types import \* from pyspark.sql import functions as F from pyspark.sql.functions import col, lit, expr spark \= SparkSession.builder.appName('Demo').master('local\[\*\]').getOrCreate() \# ── Method 1: From list of tuples with explicit schema data \= \[('Alice',34,'Engineering',95000.0,True),         ('Bob',  28,'Marketing',  72000.0,False),         ('Carol',45,'Engineering',110000.0,True),         ('Dave', 31,'Marketing',  68000.0,False),         ('Eve',  29,'Engineering',88000.0,True),         ('Frank',52,'HR',          95000.0,True),         ('Grace',33,'Finance',    105000.0,True)\] schema \= StructType(\[     StructField('name',    StringType(),  nullable=True),     StructField('age',     IntegerType(), nullable=True),     StructField('dept',    StringType(),  nullable=True),     StructField('salary',  DoubleType(),  nullable=True),     StructField('active',  BooleanType(), nullable=True), \]) df \= spark.createDataFrame(data, schema) df.show() \# ── Method 2: From Row objects rows \= \[Row(name='Alice', age=34), Row(name='Bob', age=28)\] df2 \= spark.createDataFrame(rows) \# ── Method 3: From Pandas DataFrame import pandas as pd pdf \= pd.DataFrame({'x':\[1,2,3\],'y':\['a','b','c'\]}) df3 \= spark.createDataFrame(pdf) \# ── Method 4: From CSV df4 \= spark.read.option('header','true').option('inferSchema','true').csv('path/') \# ── Method 5: From JSON (multiline) df5 \= spark.read.option('multiline','true').json('path/data.json')  \# ── Method 6: From Parquet (columnar — preferred) df6 \= spark.read.parquet('s3://bucket/data/') \# ── Method 7: From Delta Lake df7 \= spark.read.format('delta').load('s3://bucket/delta/') \# ── Method 8: From JDBC (databases) df8 \= spark.read.format('jdbc') \\     .option('url','jdbc:postgresql://host:5432/db') \\     .option('dbtable','public.employees') \\     .option('user','user').option('password','pass').load() \# ── Method 9: From ORC df9 \= spark.read.orc('path/data.orc') \# ── Method 10: From Avro df10 \= spark.read.format('avro').load('path/data.avro') \# ── Method 11: SQL on table/view df.createOrReplaceTempView('emp') df11 \= spark.sql('SELECT \* FROM emp WHERE salary \> 90000') \# ── Method 12: range / sequence df12 \= spark.range(0, 100, step=2)           \# 0,2,4,...,98 |
| :---- |

 

| OUTPUT | \+-----+---+-----------+--------+------+ | name|age|       dept|  salary|active| \+-----+---+-----------+--------+------+ |Alice| 34|Engineering| 95000.0|  true| |  Bob| 28|  Marketing| 72000.0| false| |Carol| 45|Engineering|110000.0|  true| | Dave| 31|  Marketing| 68000.0| false| |  Eve| 29|Engineering| 88000.0|  true| |Frank| 52|         HR| 95000.0|  true| |Grace| 33|    Finance|105000.0|  true| \+-----+---+-----------+--------+------+ |
| :---: | :---- |

 

## **4.2  Schema Inspection Methods**

| \# Print schema tree df.printSchema() \# root \#  |-- name: string (nullable \= true) \#  |-- age: integer ... df.schema                    \# returns StructType object df.columns                   \# \['name','age','dept','salary','active'\] df.dtypes                    \# \[('name','string'), ('age','int'), ...\] df.count()                   \# 7  (action) df.describe().show()         \# count, mean, stddev, min, max per numeric col df.summary().show()          \# extended: also 25%, 50%, 75% percentiles df.explain()                 \# physical execution plan (short) df.explain('extended')       \# all 4 plans: parsed, analyzed, optimized, physical df.explain('formatted')      \# human-readable with indentation (Spark 3.0+) df.explain('codegen')        \# show generated Java bytecode df.explain('cost')           \# with cost estimates df.rdd.getNumPartitions()    \# number of partitions df.isEmpty()                 \# True if no rows |
| :---- |

 

## **4.3  Select & Column Expressions**

| from pyspark.sql.functions import col, lit, expr, when, coalesce \# Basic select df.select('name', 'salary').show() \# Using col() — preferred for expressions df.select(col('name'), col('salary')).show() \# Arithmetic expressions df.select(     col('name'),     (col('salary') \* 1.10).alias('salary\_10pct\_raise'),     (col('salary') / 12).alias('monthly'),     (col('salary') \- 60000).alias('above\_base'),     (col('age') \* 365).alias('age\_in\_days'),     lit('India').alias('country'),          \# constant value     expr('salary \* 0.3').alias('tax'),      \# SQL expression ).show(3) \# selectExpr — SQL string expressions df.selectExpr(     'name',     'salary \* 1.1 AS raised\_salary',     'CASE WHEN salary \> 90000 THEN "Senior" ELSE "Mid" END AS level',     'upper(name) AS name\_upper' ).show() \# withColumn — add or replace df.withColumn('bonus', col('salary') \* 0.15) \\   .withColumn('dept\_upper', F.upper(col('dept'))) \\   .withColumn('is\_senior', col('age') \> 40\) \\   .show() \# withColumnRenamed df.withColumnRenamed('salary','annual\_salary').show() \# drop columns df.drop('active','age').show() |
| :---- |

 

## 

## **4.4  Filter & Where — All Patterns**

| \# Simple equality df.filter(col('dept') \== 'Engineering').show() df.where(col('dept') \== 'Engineering').show()     \# where \= alias for filter \# Inequality / comparison df.filter(col('salary') \> 80000).show() df.filter(col('salary') \>= 80000).show() df.filter(col('salary') \!= 72000).show() \# Multiple conditions df.filter((col('dept') \== 'Engineering') & (col('age') \< 40)).show() df.filter((col('dept') \== 'HR') | (col('dept') \== 'Finance')).show() df.filter(\~(col('dept') \== 'Marketing')).show()  \# NOT \# SQL-style where df.where("dept \= 'Engineering' AND salary \> 90000").show() \# isin / \~isin df.filter(col('dept').isin(\['Engineering','Finance'\])).show() df.filter(\~col('dept').isin(\['HR','Marketing'\])).show() \# between (inclusive) df.filter(col('salary').between(80000, 110000)).show() df.filter(col('age').between(28, 35)).show() \# Null checks df.filter(col('name').isNull()).show() df.filter(col('name').isNotNull()).show() df.filter(F.isnull(col('salary'))).show() \# String patterns df.filter(col('name').like('A%')).show()           \# SQL LIKE df.filter(col('name').rlike('^\[AE\]')).show()       \# regex df.filter(col('name').startswith('A')).show() df.filter(col('name').endswith('e')).show() df.filter(col('name').contains('li')).show() \# Filter on array contains from pyspark.sql.functions import array\_contains df\_arr \= df.withColumn('tags', F.array(lit('new'), lit('active'))) df\_arr.filter(array\_contains(col('tags'), 'new')).show() |
| :---- |

 

## 

## 

## 

## **4.5  GroupBy & Aggregations — Full Reference**

| from pyspark.sql.functions import (     count, countDistinct, sum, avg, mean, min, max,     stddev, stddev\_pop, variance, var\_pop,     first, last, kurtosis, skewness,     collect\_list, collect\_set,     approx\_count\_distinct, percentile\_approx,     sumDistinct, grouping, grouping\_id ) \# Basic groupBy \+ agg df.groupBy('dept').agg(     count('\*').alias('headcount'),     countDistinct('name').alias('unique\_names'),     sum('salary').alias('total\_payroll'),     avg('salary').alias('avg\_salary'),     mean('salary').alias('mean\_salary'),     min('salary').alias('min\_salary'),     max('salary').alias('max\_salary'),     stddev('salary').alias('salary\_stddev'),     variance('salary').alias('salary\_var'),     first('name').alias('first\_person'),     last('name').alias('last\_person'),     collect\_list('name').alias('all\_names'),     collect\_set('active').alias('active\_values'),     approx\_count\_distinct('name').alias('approx\_distinct'),     percentile\_approx('salary', 0.5).alias('median\_salary'), ).show(truncate=False) \# Multiple groupBy columns df.groupBy('dept','active').agg(count('\*').alias('cnt'), avg('salary')).show() \# Global aggregate (no groupBy) df.agg(max('salary').alias('company\_max'), avg('salary').alias('company\_avg')).show() \# ROLLUP — subtotals df.rollup('dept','active').agg(count('\*'), sum('salary')).show() \# CUBE — all combinations df.cube('dept','active').agg(count('\*')).show() \# PIVOT — rotate rows to columns df.groupBy('dept').pivot('active').agg(count('\*')).show() |
| :---- |

 

| OUTPUT | \+-----------+---------+------------+----------+------------+ |       dept|headcount|total\_payroll| avg\_salary|  all\_names | \+-----------+---------+------------+----------+------------+ |Engineering|        3|    293000.0| 97666.67 |\[Alice,Carol| |    Finance|        1|    105000.0|105000.0  |    \[Grace\] | |         HR|        1|     95000.0| 95000.0  |    \[Frank\] | |  Marketing|        2|    140000.0| 70000.0  | \[Bob,Dave\] | \+-----------+---------+------------+----------+------------+ |
| :---: | :---- |

   
4.6  Joins — All Types

| \# Create second DataFrame dept\_data \= \[('Engineering','New York','Tech',500),              ('Marketing','Chicago','Business',200),              ('Finance','Boston','Business',80),              ('HR','Austin','Support',50),              ('Legal','New York','Support',30)\] dept\_df \= spark.createDataFrame(dept\_data, \['dept','city','division','team\_size'\]) \# INNER JOIN — only matching rows df.join(dept\_df, on='dept', how='inner').show() \# LEFT JOIN — all left rows, null for non-matching right df.join(dept\_df, on='dept', how='left').show() df.join(dept\_df, on='dept', how='left\_outer').show()  \# same \# RIGHT JOIN df.join(dept\_df, on='dept', how='right').show() \# FULL OUTER JOIN df.join(dept\_df, on='dept', how='outer').show() df.join(dept\_df, on='dept', how='full').show()  \# same \# SEMI JOIN — rows in left that have match in right df.join(dept\_df, on='dept', how='semi').show() df.join(dept\_df, on='dept', how='left\_semi').show()  \# same \# ANTI JOIN — rows in left that have NO match in right df.join(dept\_df, on='dept', how='anti').show() df.join(dept\_df, on='dept', how='left\_anti').show()  \# same \# CROSS JOIN — Cartesian product df.crossJoin(dept\_df).show()      \# every row paired with every row \# Multiple join conditions df.join(dept\_df,     (df.dept \== dept\_df.dept) & (df.salary \> 90000),     how='inner' ).show() \# Avoid ambiguity — drop duplicate column result \= df.join(dept\_df, df.dept \== dept\_df.dept, 'inner') result \= result.drop(dept\_df.dept)   \# drop right dept \# Broadcast join — force small table to be broadcast from pyspark.sql.functions import broadcast df.join(broadcast(dept\_df), on='dept').show()   \# eliminates shuffle |
| :---- |

 

## 

## **4.7  Window Functions — Full Reference**

Window functions compute a value for each row based on a sliding 'window' of related rows — essential for rankings, running totals, lag/lead comparisons, and moving averages.

| from pyspark.sql.window import Window from pyspark.sql.functions import (     rank, dense\_rank, row\_number, percent\_rank, cume\_dist, ntile,     lag, lead,     sum as fsum, avg as favg, min as fmin, max as fmax, count as fcount,     first, last, stddev, ) \# Window specifications w\_dept      \= Window.partitionBy('dept').orderBy(col('salary').desc()) w\_dept\_rows \= Window.partitionBy('dept').orderBy('salary').rowsBetween(-1, 1\) w\_dept\_range= Window.partitionBy('dept').orderBy('salary').rangeBetween(-5000, 5000\) w\_global    \= Window.orderBy(col('salary').desc())  \# global ranking w\_unbounded \= Window.partitionBy('dept').orderBy('salary').rowsBetween(Window.unboundedPreceding, Window.currentRow) df.select(     'name','dept','salary',     \# Ranking functions     rank().over(w\_dept).alias('rank'),              \# gaps on tie (1,1,3)     dense\_rank().over(w\_dept).alias('dense\_rank'),  \# no gaps (1,1,2)     row\_number().over(w\_dept).alias('row\_num'),     \# unique (1,2,3)     percent\_rank().over(w\_dept).alias('pct\_rank'),  \# 0.0 to 1.0     cume\_dist().over(w\_dept).alias('cume\_dist'),    \# cumulative distribution     ntile(3).over(w\_dept).alias('tercile'),         \# divide into N buckets     \# Lag / Lead     lag('salary', 1).over(w\_dept).alias('prev\_salary'),     \# previous row     lag('salary', 1, 0).over(w\_dept).alias('prev\_sal\_0'),   \# default 0     lead('salary', 1).over(w\_dept).alias('next\_salary'),    \# next row     \# Running aggregates     fsum('salary').over(w\_unbounded).alias('running\_total'),     favg('salary').over(w\_unbounded).alias('running\_avg'),     fmax('salary').over(w\_dept).alias('dept\_max'),           \# partition max     fmin('salary').over(w\_dept).alias('dept\_min'),     fcount('\*').over(w\_dept).alias('dept\_headcount'),     \# Row-based sliding window (3-row moving average)     favg('salary').over(w\_dept\_rows).alias('moving\_avg\_3'), ).orderBy('dept', col('salary').desc()).show(truncate=False) |
| :---- |

 

| OUTPUT | \+-----+-----------+--------+----+----------+-------+-----------+-----------+-------------+ | name|       dept|  salary|rank|dense\_rank|row\_num|prev\_salary|next\_salary|running\_total| \+-----+-----------+--------+----+----------+-------+-----------+-----------+-------------+ |Carol|Engineering|110000.0|   1|         1|      1|       null|    95000.0|     110000.0| |Alice|Engineering| 95000.0|   2|         2|      2|   110000.0|    88000.0|     205000.0| |  Eve|Engineering| 88000.0|   3|         3|      3|    95000.0|       null|     293000.0| |Grace|    Finance|105000.0|   1|         1|      1|       null|       null|     105000.0| |  Bob|  Marketing| 72000.0|   1|         1|      1|       null|    68000.0|      72000.0| | Dave|  Marketing| 68000.0|   2|         2|      2|    72000.0|       null|     140000.0| \+-----+-----------+--------+----+----------+-------+-----------+-----------+-------------+ |
| :---- | :---- |

 

## **4.8  String Functions — Complete Reference**

| from pyspark.sql.functions import (     upper, lower, initcap, trim, ltrim, rtrim,     length, char\_length, octet\_length,     substring, substr, left, right,     concat, concat\_ws, format\_string, printf,     split, regexp\_replace, regexp\_extract, regexp\_like,     instr, locate, position, find\_in\_set,     lpad, rpad, repeat, reverse, overlay,     translate, replace, soundex,     encode, decode, base64, unbase64,     ltrim, rtrim, btrim,     ascii, chr, hex, unhex,     like, ilike, rlike,     endswith, startswith, contains,     sentences, words, levenshtein,     url\_encode, url\_decode, ) df.select(     upper(col('name')).alias('upper'),     lower(col('name')).alias('lower'),     initcap(col('name')).alias('titlecase'),     length(col('name')).alias('len'),     trim(lit('  hello  ')).alias('trimmed'),     lpad(col('name'), 10, '\*').alias('lpadded'),     rpad(col('name'), 10, '-').alias('rpadded'),     substring(col('name'), 1, 3).alias('substr'),     concat(col('name'), lit(' @ '), col('dept')).alias('combined'),     concat\_ws(' | ', col('name'), col('dept')).alias('piped'),     split(col('name'), 'a').alias('split\_a'),     regexp\_replace(col('dept'), 'ing', 'ION').alias('replaced'),     regexp\_extract(col('dept'), '(\\w+)ing', 1).alias('extracted'),     instr(col('name'), 'li').alias('li\_pos'),     reverse(col('name')).alias('reversed'),     repeat(col('name'), 2).alias('doubled'),     levenshtein(col('name'), lit('Alice')).alias('edit\_dist'),     soundex(col('name')).alias('soundex'), ).show(3, False) |
| :---- |

 

## **4.9  Date & Time Functions — Complete Reference**

| from pyspark.sql.functions import (     current\_date, current\_timestamp,     year, month, dayofmonth, dayofweek, dayofyear,     hour, minute, second, quarter,     weekofyear, last\_day, next\_day,     date\_add, date\_sub, add\_months,     datediff, months\_between,     to\_date, to\_timestamp, to\_utc\_timestamp, from\_utc\_timestamp,     date\_format, unix\_timestamp, from\_unixtime,     trunc, date\_trunc,     make\_date, make\_timestamp,     window, session\_window,     now, localtimestamp, ) date\_data \= \[('Alice','2023-01-15 09:30:45'), ('Bob','2022-11-20 23:15:00')\] ddf \= spark.createDataFrame(date\_data, \['name','hire\_ts'\]) ddf.select(     'name',     to\_timestamp('hire\_ts').alias('ts'),     year('hire\_ts').alias('yr'),     month('hire\_ts').alias('mo'),     dayofmonth('hire\_ts').alias('dom'),     dayofweek('hire\_ts').alias('dow'),     \# 1=Sunday     dayofyear('hire\_ts').alias('doy'),     hour('hire\_ts').alias('hr'),     minute('hire\_ts').alias('min'),     second('hire\_ts').alias('sec'),     quarter('hire\_ts').alias('qtr'),     weekofyear('hire\_ts').alias('woy'),     date\_add(to\_date('hire\_ts'), 90).alias('90d\_after'),     date\_sub(to\_date('hire\_ts'), 7).alias('7d\_before'),     add\_months(to\_date('hire\_ts'), 3).alias('3m\_after'),     last\_day(to\_date('hire\_ts')).alias('month\_end'),     datediff(current\_date(), to\_date('hire\_ts')).alias('days\_since'),     months\_between(current\_date(), to\_date('hire\_ts')).alias('mo\_since'),     date\_format(to\_date('hire\_ts'), 'dd/MM/yyyy').alias('fmt'),     trunc(to\_date('hire\_ts'), 'month').alias('month\_start'),     date\_trunc('hour', to\_timestamp('hire\_ts')).alias('hour\_trunc'),     unix\_timestamp(to\_timestamp('hire\_ts')).alias('epoch'), ).show(truncate=False) |
| :---- |

 

## **4.10  Math & Numeric Functions**

| from pyspark.sql.functions import (     abs, ceil, floor, round, bround, signum, sign,     sqrt, cbrt, exp, expm1, log, log2, log10, log1p,     pow, pmod, factorial, greatest, least,     sin, cos, tan, asin, acos, atan, atan2, sinh, cosh, tanh,     degrees, radians,     rand, randn,     bin, hex, unhex, shiftLeft, shiftRight, shiftRightUnsigned,     bitwiseNOT,     hypot, rint, ) df.select(     abs(col('salary') \- 90000).alias('dist\_from\_90k'),     ceil(col('salary') / 1000).alias('k\_ceil'),     floor(col('salary') / 1000).alias('k\_floor'),     round(col('salary') / 1000, 1).alias('k\_round1dp'),     sqrt(col('salary')).alias('sqrt\_sal'),     log(col('salary')).alias('ln\_sal'),     log10(col('salary')).alias('log10\_sal'),     pow(col('age'), 2).alias('age\_sq'),     greatest(col('salary'), lit(90000)).alias('min\_90k'),     least(col('salary'), lit(100000)).alias('cap\_100k'),     rand(seed=42).alias('random'), ).show(3) |
| :---- |

 

## **4.11  Null & Conditional Functions**

| from pyspark.sql.functions import (     when, otherwise, coalesce, nvl, nvl2, nullif,     ifnull, isnull, isnan, isnotnull,     nanvl, decode, ) \# when / otherwise — vectorized CASE WHEN df.withColumn('level',     when(col('salary') \>= 100000, 'Senior')     .when(col('salary') \>= 80000,  'Mid')     .when(col('salary') \>= 60000,  'Junior')     .otherwise('Intern') ).show() \# coalesce — first non-null df.withColumn('safe\_sal', coalesce(col('salary'), lit(0))).show() \# nullif — returns null if two values are equal df.withColumn('no\_eng', F.nullif(col('dept'), lit('Engineering'))).show() \# fillna / na.fill df.fillna(0, \['salary'\]).show() df.fillna({'salary':0, 'dept':'Unknown'}).show() df.na.fill(0).show() \# dropna df.dropna().show()                  \# any null in any column df.dropna(how='all').show()         \# only rows where ALL columns null df.dropna(subset=\['name'\]).show()   \# null in specific columns df.na.drop(thresh=3).show()         \# keep rows with at least 3 non-null \# replace df.replace('Marketing', 'Mktg').show() df.na.replace({'Marketing':'Mktg','HR':'Human Resources'}).show() |
| :---- |

 

## 

## 

## 

## 

## 

## **4.12  Array & Map Functions — Complete Reference**

| from pyspark.sql.functions import (     array, array\_contains, array\_distinct, array\_except, array\_intersect,     array\_union, array\_join, array\_max, array\_min, array\_position,     array\_remove, array\_repeat, array\_reverse, array\_sort, array\_zip,     array\_compact, array\_append, array\_prepend, array\_insert,     array\_size, cardinality, size,     element\_at, get,     explode, explode\_outer, posexplode, posexplode\_outer,     inline, inline\_outer,     flatten, sequence, shuffle, slice, sort\_array,     transform, filter as arr\_filter, aggregate, exists, forall, zip\_with,     map\_from\_arrays, map\_from\_entries, map\_keys, map\_values,     map\_contains\_key, map\_entries, map\_filter, map\_zip\_with,     map\_concat, map\_merge, str\_to\_map, create\_map,     struct, named\_struct,     from\_json, to\_json, get\_json\_object, json\_tuple, schema\_of\_json, ) \# Create complex types complex \= spark.createDataFrame(\[     ('Alice', \[90,85,92\], {'py':90,'sql':85}),     ('Bob',   \[70,75,80\], {'py':70,'sql':75}) \], \['name','scores','skills'\]) \# Array operations complex.select(     'name',     size('scores').alias('num\_scores'),     array\_max('scores').alias('best'),     array\_min('scores').alias('worst'),     array\_sort('scores').alias('sorted'),     array\_distinct('scores').alias('distinct'),     array\_contains('scores', 90).alias('has\_90'),     array\_position('scores', 85).alias('pos\_of\_85'),     array\_remove('scores', 70).alias('no\_70'),     slice('scores', 1, 2).alias('first\_2'),     flatten(array(col('scores'), col('scores'))).alias('doubled'), ).show(truncate=False) \# Higher-order functions (Spark 3.0+) complex.select(     transform('scores', lambda x: x \* 1.1).alias('boosted'),     F.filter('scores', lambda x: x \> 80).alias('above\_80'),     aggregate('scores', lit(0), lambda acc,x: acc+x).alias('sum'),     exists('scores', lambda x: x \> 85).alias('any\_above\_85'),     forall('scores', lambda x: x \> 60).alias('all\_above\_60'), ).show(truncate=False) \# Explode array → multiple rows complex.select('name', F.explode('scores').alias('score')).show() complex.select('name', F.posexplode('scores').alias('idx','score')).show() \# Map operations complex.select(     'name',     map\_keys('skills').alias('skill\_names'),     map\_values('skills').alias('skill\_scores'),     col('skills')\['py'\].alias('python\_score'),     element\_at('skills', 'sql').alias('sql\_score'),     map\_contains\_key('skills','py').alias('has\_py'), ).show() |
| :---- |

 

## **4.13  JSON Functions**

| from pyspark.sql.functions import from\_json, to\_json, get\_json\_object, json\_tuple, schema\_of\_json from pyspark.sql.types import StructType, StringType, IntegerType json\_data \= \[('1', '{"name":"Alice","age":34,"scores":\[90,85\]}'),              ('2', '{"name":"Bob","age":28,"scores":\[70,75\]}')\] jdf \= spark.createDataFrame(json\_data, \['id','json\_str'\]) \# Infer schema from JSON inferred \= spark.read.json(jdf.rdd.map(lambda r: r.json\_str)) \# from\_json — parse JSON string to struct schema \= StructType().add('name',StringType()).add('age',IntegerType()) jdf.withColumn('parsed', from\_json(col('json\_str'), schema)).select('id','parsed.\*').show() \# get\_json\_object — extract single field with JSONPath jdf.withColumn('name', get\_json\_object(col('json\_str'), '$.name')).show() \# json\_tuple — extract multiple fields at once jdf.select('id', F.json\_tuple(col('json\_str'), 'name','age').alias('name','age')).show() \# to\_json — convert struct/map/array column to JSON string df.select(F.to\_json(F.struct('name','salary')).alias('json')).show() \# schema\_of\_json — infer schema from JSON string literal print(schema\_of\_json('{"name":"Alice","age":34}')) |
| :---- |

 

## 

## 

## 

## 

## **4.14  Sort, Deduplicate & Ordering**

| \# Sort / orderBy df.orderBy('salary').show()                           \# ascending default df.orderBy(col('salary').desc()).show()               \# descending df.orderBy(col('dept').asc(), col('salary').desc()).show()  \# multi-col df.sort(col('salary').desc\_nulls\_last()).show()       \# nulls at end df.sort(col('salary').asc\_nulls\_first()).show()       \# nulls at start \# distinct — all columns df.distinct().show() \# dropDuplicates — specific columns df.dropDuplicates(\['dept'\]).show()             \# first occurrence per dept df.dropDuplicates(\['dept','active'\]).show() \# limit — first N rows (lazy) df.limit(3).show() \# sample df.sample(fraction=0.5, seed=42).show() df.sample(withReplacement=True, fraction=0.8).show() \# sampleBy — stratified sample fracs \= {'Engineering':0.5, 'Marketing':1.0, 'HR':1.0, 'Finance':1.0} df.sampleBy('dept', fractions=fracs, seed=42).show() |
| :---- |

 

## **4.15  Partitioning, Bucketing & Repartitioning**

| \# Check current partition count print(df.rdd.getNumPartitions()) \# repartition — shuffle, creates N balanced partitions df.repartition(20).rdd.getNumPartitions()         \# 20 df.repartition(5, 'dept').rdd.getNumPartitions()  \# hash partition by dept df.repartition(8, 'dept', 'active')               \# multi-column hash \# coalesce — reduce partitions WITHOUT shuffle (faster) df.coalesce(1).write.csv('output\_single\_file/') \# repartitionByRange — range partitioning (sorted output) df.repartitionByRange(4, 'salary').show() \# Write with partition columns (partition pruning at read time) df.write.mode('overwrite').partitionBy('dept','active').parquet('s3://bucket/employees/') \# Write with bucketing (co-located join optimization) df.write.mode('overwrite') \\     .bucketBy(16, 'dept') \\     .sortBy('salary') \\     .saveAsTable('employees\_bucketed') |
| :---- |

 

## **4.16  Writing DataFrames — All Formats & Options**

| \# Common write options df.write \\     .mode('overwrite')          \# overwrite | append | ignore | errorIfExists     .option('compression','snappy')  \# snappy|gzip|lz4|brotli|zstd|none     .parquet('s3://bucket/output/') \# CSV df.write.csv('output/',header=True, sep=',', quote='"', escape='\\\\') \# JSON df.write.json('output/', compression='gzip') \# ORC df.write.orc('output/', compression='zlib') \# Avro df.write.format('avro').save('output/') \# Delta Lake df.write.format('delta').mode('overwrite').save('s3://bucket/delta/') \# JDBC df.write.format('jdbc') \\     .option('url','jdbc:postgresql://host/db') \\     .option('dbtable','public.out') \\     .option('user','user').option('password','pw') \\     .mode('append').save() \# saveAsTable — writes to Hive metastore df.write.mode('overwrite').saveAsTable('hr\_db.employees') \# insertInto — appends to existing table schema df.write.insertInto('hr\_db.employees', overwrite=True) |
| :---- |

 

## 

## 

## 

## 

## 

## **4.17  UDFs — User Defined Functions**

| from pyspark.sql.functions import udf, pandas\_udf from pyspark.sql.types import StringType, DoubleType, ArrayType import pandas as pd \# ── Regular UDF (row-by-row — Python overhead per row) @udf(returnType=StringType()) def classify\_salary(salary):     if salary is None:   return 'Unknown'     if salary \< 60000:   return 'Junior'     if salary \< 85000:   return 'Mid'     if salary \< 110000:  return 'Senior'     return 'Principal' df.withColumn('level', classify\_salary(col('salary'))).show() \# Register for SQL use spark.udf.register('classify\_salary', classify\_salary) spark.sql("SELECT name, classify\_salary(salary) AS level FROM emp").show() \# ── Pandas UDF (Series→Series) — vectorized, 10-100x faster @pandas\_udf(DoubleType()) def salary\_with\_tax(salary: pd.Series) \-\> pd.Series:     return salary \* 0.7    \# 30% tax df.withColumn('net\_salary', salary\_with\_tax(col('salary'))).show() \# ── Pandas UDF (Iterator of Series) — load resources once per batch from pyspark.sql.functions import PandasUDFType from typing import Iterator @pandas\_udf(DoubleType()) def batch\_salary(iterator: Iterator\[pd.Series\]) \-\> Iterator\[pd.Series\]:     \# Load model once, apply to each batch     for batch in iterator:         yield batch \* 1.2 \# ── Pandas UDF (DataFrame → DataFrame) — grouped map from pyspark.sql.functions import pandas\_udf schema\_out \= df.schema @F.pandas\_udf(schema\_out) def normalize\_group(pdf: pd.DataFrame) \-\> pd.DataFrame:     pdf\['salary'\] \= (pdf\['salary'\] \- pdf\['salary'\].mean()) / pdf\['salary'\].std()     return pdf df.groupBy('dept').applyInPandas(normalize\_group, schema=df.schema).show() |
| :---- |

 

# **Chapter 5 — Spark SQL, Catalyst Optimizer & Catalog**

| SQL Interface · Views · Optimizer Pipeline · Metastore |
| :---: |

 

## **5.1  SQL Interface**

| \# Register temp view df.createOrReplaceTempView('emp')          \# session-scoped df.createOrReplaceTempView('emp')          \# replaces if exists df.createTempView('emp\_v2')                \# fails if already exists \# Global temp view — across sessions df.createOrReplaceGlobalTempView('global\_emp') spark.sql('SELECT \* FROM global\_temp.global\_emp').show() \# Run SQL result \= spark.sql('''     SELECT         dept,         COUNT(\*) AS headcount,         ROUND(AVG(salary),2) AS avg\_salary,         MAX(salary) AS top\_salary,         PERCENTILE\_APPROX(salary, 0.5) AS median,         RANK() OVER (ORDER BY AVG(salary) DESC) AS salary\_rank     FROM emp     WHERE active \= true     GROUP BY dept     HAVING COUNT(\*) \> 0     ORDER BY salary\_rank ''') result.show() \# Database / catalog management spark.sql('CREATE DATABASE IF NOT EXISTS hr\_db COMMENT "HR Data"') spark.sql('USE hr\_db') spark.sql('SHOW DATABASES').show() spark.sql('SHOW TABLES IN hr\_db').show() spark.sql('DESCRIBE TABLE hr\_db.employees').show() spark.sql('DESCRIBE EXTENDED hr\_db.employees').show() \# Create managed table spark.sql('''     CREATE TABLE IF NOT EXISTS hr\_db.employees (         name    STRING,         age     INT,         dept    STRING,         salary  DOUBLE     ) USING PARQUET     PARTITIONED BY (dept)     COMMENT 'Employee table' ''') \# Create external table spark.sql('''     CREATE EXTERNAL TABLE IF NOT EXISTS hr\_db.emp\_ext     USING PARQUET     LOCATION 's3://bucket/employees/' ''') |
| :---- |

 

## **5.2  Catalog API**

| PYTHON | \# Full Catalog API spark.catalog.listDatabases()                        \# list all databases spark.catalog.listTables('hr\_db')                   \# list tables in db spark.catalog.listColumns('hr\_db', 'employees')     \# list columns spark.catalog.listFunctions()                       \# list functions spark.catalog.tableExists('hr\_db.employees')        \# True/False spark.catalog.databaseExists('hr\_db')               \# True/False spark.catalog.functionExists('my\_udf')              \# True/False spark.catalog.currentDatabase()                     \# current db name spark.catalog.setCurrentDatabase('hr\_db') spark.catalog.cacheTable('employees') spark.catalog.uncacheTable('employees') spark.catalog.isCached('employees') spark.catalog.refreshTable('employees')             \# reload metadata spark.catalog.recoverPartitions('employees')        \# rediscover partitions spark.catalog.clearCache()                          \# clear all cached tables spark.catalog.dropTempView('emp') spark.catalog.dropGlobalTempView('global\_emp') |
| :---: | :---- |

 

## 

## 

## 

## 

## 

## **5.3  The Catalyst Optimizer**

Catalyst is Spark's extensible query optimizer. Every SQL query and DataFrame operation passes through a 5-stage pipeline before being executed. This automatic optimization is why Spark SQL is often faster than hand-written RDD code.

 

![][image1]

▲ Catalyst Optimizer Pipeline — 5 Stages from SQL Text to JVM Bytecode

 

| Optimization | What It Does | Speedup |
| :---- | :---- | :---- |
| Predicate Pushdown | Moves filter() operations as close to data source as possible — read less data | Up to 10x |
| Column Pruning | Scans only the columns referenced — skips irrelevant Parquet columns | 2-5x |
| Partition Pruning | Skips reading partitions not matching filter (e.g. WHERE year=2024) | 10-100x |
| Broadcast Join | Auto-broadcasts tables \< threshold — eliminates shuffle | 5-50x |
| Constant Folding | Pre-computes constant expressions at plan time (5\*12 → 60\) | Minor |
| Join Reordering | Smaller table joined first to reduce data flowing through | Variable |
| AQE Skew Handling | Splits skewed partitions at runtime (Spark 3.0+) | 2-10x |
| AQE Join Strategy | Changes join type at runtime based on actual data sizes | Variable |

# **Chapter 6 — RDDs, Accumulators & Broadcast Variables**

| Low-Level API · Pair RDDs · Distributed Shared State |
| :---: |

 

## **6.1  RDD — Full API Reference**

| PYTHON | sc \= spark.sparkContext \# ── Creating RDDs rdd \= sc.parallelize(\[1,2,3,4,5,6,7,8,9,10\], numSlices=4) rdd2 \= sc.textFile('s3://bucket/logs/\*.log')         \# one line \= one record rdd3 \= sc.wholeTextFiles('s3://bucket/files/')       \# (filename, content) rdd4 \= ysc.range(0, 100, step=2)                      \# 0,2,4,... rdd5 \= sc.emptyRDD() rdd6 \= df.rdd                                         \# from DataFrame \# ── Transformations (lazy) rdd.map(lambda x: x\*2)                               \# transform each rdd.flatMap(lambda x: \[x, x+1\])                      \# map \+ flatten rdd.filter(lambda x: x%2==0)                         \# keep matching rdd.distinct()                                        \# remove dups rdd.sample(False, 0.5, seed=42)                      \# random sample rdd.union(rdd2)                                       \# combine rdd.intersection(rdd2)                               \# common elements rdd.subtract(rdd2)                                   \# left \- right rdd.cartesian(rdd2)                                  \# cross product rdd.zip(rdd2)                                        \# pair (a,b) elementwise rdd.zipWithIndex()                                   \# (element, index) rdd.zipWithUniqueId()                                \# unique non-consecutive id rdd.sortBy(lambda x: x, ascending=False)             \# sort rdd.glom()                                           \# collect each partition to list rdd.coalesce(2)                                      \# reduce partitions rdd.repartition(10)                                  \# shuffle repartition rdd.mapPartitions(lambda it: map(lambda x:x\*2, it)) \# transform per partition rdd.mapPartitionsWithIndex(lambda i,it: map(str,it)) \# with partition id rdd.pipe('wc \-l')                                    \# pipe through shell cmd \# ── Pair RDD Transformations (key-value) pair \= rdd.map(lambda x: (x%3, x))                  \# create pairs pair.groupByKey()                                    \# group values by key pair.reduceByKey(lambda a,b: a+b)                   \# reduce within key pair.aggregateByKey(0, lambda a,v:a+v, lambda a,b:a+b)  \# agg with combiner pair.foldByKey(0, lambda a,b: a+b)                  \# fold within key pair.combineByKey(lambda v: \[v\], lambda a,v:a+\[v\], lambda a,b:a+b) pair.sortByKey(ascending=True)                       \# sort by key pair.keys()                                          \# just keys pair.values()                                        \# just values pair.mapValues(lambda v: v\*2)                        \# transform values pair.flatMapValues(lambda v: range(v))               \# flatMap values pair.join(pair2)                                     \# inner join on key pair.leftOuterJoin(pair2)                            \# left join pair.rightOuterJoin(pair2)                           \# right join pair.fullOuterJoin(pair2)                            \# full outer join pair.cogroup(pair2)                                  \# group together pair.subtractByKey(pair2)                            \# keys in left not right pair.partitionBy(4)                                  \# hash partition by key \# ── Actions (trigger execution) rdd.collect()                                        \# return all to driver rdd.count()                                          \# count rows rdd.countByValue()                                   \# count each unique value rdd.first()                                          \# first element rdd.take(5)                                          \# first N elements rdd.takeSample(False, 5\)                             \# random N elements rdd.top(3)                                           \# top N elements rdd.min()                                            \# minimum rdd.max()                                            \# maximum rdd.sum()                                            \# sum rdd.mean()                                           \# mean rdd.stdev()                                          \# std deviation rdd.variance()                                       \# variance rdd.stats()                                          \# count,mean,stdev,max,min rdd.histogram(\[0,5,10,15\])                           \# histogram buckets rdd.reduce(lambda a,b: a+b)                          \# reduce to single value rdd.fold(0, lambda a,b: a+b)                         \# fold with zero value rdd.aggregate(0, lambda a,v:a+v, lambda a,b:a+b)    \# aggregate with combiner rdd.foreach(lambda x: print(x))                      \# apply fn per element rdd.foreachPartition(lambda it: \[print(x) for x in it\]) rdd.saveAsTextFile('output/') rdd.saveAsPickleFile('output/') pair.saveAsSequenceFile('output/') pair.countByKey()                                    \# count per key pair.lookup(2)                                       \# values for key=2 pair.collectAsMap()                                  \# {key:\[values\]...} |
| :---: | :---- |

 

## **6.2  Broadcast Variables**

| PYTHON | \# Broadcast — efficiently share large read-only data with ALL executors \# Without broadcast: data is sent with every task (very slow for large lookups) \# With broadcast: data is sent ONCE to each executor, cached in memory dept\_lookup \= {'Engineering':'Tech','Marketing':'Business','HR':'People',                'Finance':'Business','Legal':'Compliance'} broadcast\_lookup \= sc.broadcast(dept\_lookup) @udf(StringType()) def get\_division(dept):     return broadcast\_lookup.value.get(dept, 'Unknown') df.withColumn('division', get\_division(col('dept'))).show() \# Broadcast a model for inference import pickle with open('model.pkl','rb') as f:     model \= pickle.load(f) bc\_model \= sc.broadcast(model) @udf(DoubleType()) def predict(features):     return float(bc\_model.value.predict(\[features\])\[0\]) \# Destroy broadcast when done broadcast\_lookup.destroy() broadcast\_lookup.unpersist()          \# remove from executor memory |
| :---: | :---- |

 

## **6.3  Accumulators**

| PYTHON | \# Accumulators — distributed write-only counters \# Workers ADD to them; only driver can READ the value error\_count  \= sc.accumulator(0) null\_count   \= sc.accumulator(0) total\_salary \= sc.accumulator(0.0) \# Custom accumulator (for complex types) from pyspark import AccumulatorParam class SetAccumulatorParam(AccumulatorParam):     def zero(self, init): return init     def addInPlace(self, v1, v2): v1.update(v2); return v1 dept\_set \= sc.accumulator(set(), SetAccumulatorParam()) def validate\_and\_count(row):     if row\['salary'\] is None or row\['salary'\] \<= 0:         error\_count.add(1)     if row\['name'\] is None:         null\_count.add(1)     total\_salary.add(float(row\['salary'\] or 0))     dept\_set.add({row\['dept'\]}) df.rdd.foreach(validate\_and\_count) print(f'Errors:    {error\_count.value}') print(f'Nulls:     {null\_count.value}') print(f'Total sal: {total\_salary.value}') print(f'Depts:     {dept\_set.value}') |
| :---: | :---- |

 

# **Chapter 7 — Structured Streaming**

| Real-Time Data Processing · Kafka · Watermarks · Stateful Ops |
| :---: |

 

Structured Streaming treats live data as an unbounded table growing over time. You query it with the same DataFrame/SQL API as batch — but results update continuously.

 

![][image2]

▲ Structured Streaming Architecture — Sources, Engine, Output Modes, Sinks

 

## **7.1  Reading Streams**

| PYTHON | \# From Kafka kafka\_df \= spark.readStream \\     .format('kafka') \\     .option('kafka.bootstrap.servers','broker1:9092,broker2:9092') \\     .option('subscribe','events-topic') \\                  \# single topic     .option('subscribePattern','events-.\*') \\              \# OR regex pattern     .option('startingOffsets','latest') \\                  \# latest|earliest|json     .option('maxOffsetsPerTrigger','10000') \\     .option('failOnDataLoss','false') \\     .load() \# Kafka schema: key, value (bytes), topic, partition, offset, timestamp from pyspark.sql.functions import from\_json, col from pyspark.sql.types import StructType, StringType, LongType event\_schema \= StructType() \\     .add('user\_id',  StringType()) \\     .add('event',    StringType()) \\     .add('ts',       LongType()) events \= kafka\_df \\     .select(from\_json(col('value').cast('string'), event\_schema).alias('d')) \\     .select('d.\*') \# From files (auto-detect new files) file\_stream \= spark.readStream \\     .format('csv') \\     .option('header','true') \\     .schema(schema) \\                    \# REQUIRED for file streaming     .option('maxFilesPerTrigger','100') \\     .load('s3://bucket/incoming/') \# From Delta (change data feed) delta\_stream \= spark.readStream \\     .format('delta') \\     .option('readChangeFeed','true') \\     .load('s3://bucket/delta-table/') |
| :---: | :---- |

 

## **7.2  Writing Streams — All Sinks & Triggers**

| PYTHON | from pyspark.sql.functions import window, col \# Windowed aggregation with watermark windowed \= events \\     .withColumn('event\_time', (col('ts')/1000).cast('timestamp')) \\     .withWatermark('event\_time', '10 minutes') \\      \# wait 10min for late data     .groupBy(         window(col('event\_time'), '5 minutes', '1 minute'),  \# 5-min window, 1-min slide         col('user\_id')     ).count() \# ── Console sink (development only) q1 \= windowed.writeStream \\     .outputMode('update') \\     .format('console') \\     .option('truncate', False) \\     .trigger(processingTime='30 seconds') \\     .start() \# ── File sink (parquet) q2 \= events.writeStream \\     .outputMode('append') \\     .format('parquet') \\     .option('path','s3://bucket/stream-out/') \\     .option('checkpointLocation','s3://bucket/checkpoint/q2/') \\     .trigger(processingTime='1 minute') \\     .partitionBy('event') \\     .start() \# ── Delta sink q3 \= events.writeStream \\     .outputMode('append') \\     .format('delta') \\     .option('path','s3://bucket/delta/events/') \\     .option('checkpointLocation','s3://bucket/checkpoint/q3/') \\     .trigger(availableNow=True) \\        \# process all then stop     .start() \# ── Kafka sink q4 \= events.selectExpr('CAST(user\_id AS STRING) AS key', "to\_json(struct(\*)) AS value") \\     .writeStream.format('kafka') \\     .option('kafka.bootstrap.servers','broker:9092') \\     .option('topic','output-topic') \\     .option('checkpointLocation','s3://bucket/checkpoint/q4/') \\     .outputMode('append').start() \# ── Memory sink (for testing/querying) q5 \= windowed.writeStream \\     .format('memory') \\     .queryName('events\_table') \\     .outputMode('complete') \\     .start() spark.sql('SELECT \* FROM events\_table').show() \# ── ForeachBatch sink (custom logic per batch) def write\_to\_db(batch\_df, batch\_id):     batch\_df.write.mode('append').jdbc(url, 'events', props) q6 \= events.writeStream \\     .foreachBatch(write\_to\_db) \\     .option('checkpointLocation', 's3://bucket/chk/') \\     .trigger(processingTime='60 seconds') \\     .start() \# ── Trigger types .trigger(processingTime='30 seconds')    \# micro-batch every 30s .trigger(once=True)                      \# one batch then stop (Spark 3.2-) .trigger(availableNow=True)              \# all pending data then stop (3.3+) .trigger(continuous='1 second')          \# low-latency \~1ms (experimental) \# Query management q1.id                     \# query UUID q1.name                   \# query name q1.isActive               \# True/False q1.status                 \# detailed status dict q1.lastProgress           \# metrics of last batch q1.recentProgress         \# last N batches q1.awaitTermination()     \# block until stopped q1.awaitTermination(60)   \# timeout after 60 seconds q1.stop()                 \# stop gracefully q1.exception()            \# if failed, returns exception spark.streams.active      \# list of active queries spark.streams.awaitAnyTermination() |
| :---: | :---- |

 

# **Chapter 8 — MLlib: Distributed Machine Learning**

| Pipelines · Feature Engineering · Algorithms · Evaluation · MLOps |
| :---: |

 

## **8.1  ML Pipeline Architecture**

| PYTHON | from pyspark.ml import Pipeline, PipelineModel from pyspark.ml.feature import (     StringIndexer, IndexToString, OneHotEncoder, VectorAssembler,     StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler,     Normalizer, Binarizer, Bucketizer, QuantileDiscretizer,     PCA, ChiSqSelector, UnivariateFeatureSelector,     Word2Vec, HashingTF, IDF, Tokenizer, RegexTokenizer,     StopWordsRemover, NGram, CountVectorizer,     SQLTransformer, VectorIndexer, Interaction,     ElementwiseProduct, PolynomialExpansion,     DCT, StringIndexer, VectorSizeHint,     Imputer, FeatureHasher, ) from pyspark.ml.classification import (     LogisticRegression, RandomForestClassifier, GBTClassifier,     DecisionTreeClassifier, LinearSVC, NaiveBayes,     MultilayerPerceptronClassifier, OneVsRest,     FMClassifier, ) from pyspark.ml.regression import (     LinearRegression, RandomForestRegressor, GBTRegressor,     DecisionTreeRegressor, GeneralizedLinearRegression,     IsotonicRegression, AFTSurvivalRegression,     FMRegressor, ) from pyspark.ml.clustering import (     KMeans, BisectingKMeans, GaussianMixture,     LDA, PowerIterationClustering, ) from pyspark.ml.recommendation import ALS from pyspark.ml.evaluation import (     BinaryClassificationEvaluator, MulticlassClassificationEvaluator,     RegressionEvaluator, ClusteringEvaluator, RankingEvaluator, ) from pyspark.ml.tuning import CrossValidator, TrainValidationSplit, ParamGridBuilder \# ── Full Pipeline Example train \= spark.createDataFrame(\[     ('Alice','Engineering',34,95000.0,1.0),     ('Bob','Marketing',28,72000.0,0.0),     ('Carol','Engineering',45,110000.0,1.0),     ('Dave','Marketing',31,68000.0,0.0),     ('Eve','Engineering',29,88000.0,1.0), \], \['name','dept','age','salary','label'\]) \# Stage 1: Index department string indexer \= StringIndexer(inputCol='dept', outputCol='dept\_idx') \# Stage 2: One-hot encode encoder \= OneHotEncoder(inputCol='dept\_idx', outputCol='dept\_vec') \# Stage 3: Assemble features assembler \= VectorAssembler(     inputCols=\['dept\_vec','age','salary'\],     outputCol='raw\_features',     handleInvalid='keep' ) \# Stage 4: Scale features scaler \= StandardScaler(inputCol='raw\_features', outputCol='features',                          withStd=True, withMean=True) \# Stage 5: Classifier rf \= RandomForestClassifier(featuresCol='features', labelCol='label',                              numTrees=100, maxDepth=5, seed=42) \# Build and fit pipeline pipeline \= Pipeline(stages=\[indexer, encoder, assembler, scaler, rf\]) model \= pipeline.fit(train) \# Predict predictions \= model.transform(train) predictions.select('name','salary','label','prediction','probability').show() \# Evaluate evaluator \= BinaryClassificationEvaluator(rawPredictionCol='rawPrediction',                                            metricName='areaUnderROC') auc \= evaluator.evaluate(predictions) print(f'AUC: {auc:.4f}') \# Hyperparameter tuning param\_grid \= ParamGridBuilder() \\     .addGrid(rf.numTrees, \[50, 100, 200\]) \\     .addGrid(rf.maxDepth, \[3, 5, 7\]) \\     .build() cv \= CrossValidator(estimator=pipeline, evaluator=evaluator,                     estimatorParamMaps=param\_grid, numFolds=3, seed=42) cv\_model \= cv.fit(train) print('Best AUC:', cv\_model.avgMetrics) \# Save / load model model.write().overwrite().save('s3://bucket/models/rf\_pipeline/') loaded \= PipelineModel.load('s3://bucket/models/rf\_pipeline/') |
| :---: | :---- |

 

# **Chapter 9 — Data Architecture Patterns**

| Data Warehouse · Data Lake · Lakehouse · Data Mesh · Data Fabric |
| :---: |

 

Modern data engineering involves choosing the right architecture for your organization's needs. Each pattern solves different problems and PySpark plays a key role in all of them.

 

▲ Data Architecture Comparison — DWH → Lake → Lakehouse → Mesh

 

## **9.1  Data Warehouse**

A centralized repository of cleaned, structured, historical data optimized for analytical SQL queries. Schema is defined before data is loaded (schema-on-write). Designed for BI, reporting, and dashboards.

| Aspect | Details |
| :---- | :---- |
| Schema | Schema-on-write — define structure before loading data |
| Data Types | Structured only — rows and columns |
| Transactions | Full ACID — consistent, isolated transactions |
| Query Performance | Excellent for SQL aggregations — columnar storage, indices |
| Scalability | Scale-up (more RAM/CPU) or scale-out (MPP) — expensive |
| Limitation | Cannot store unstructured data; costly to change schema; expensive at scale |
| AWS Service | Amazon Redshift |
| Azure Service | Azure Synapse Analytics |
| GCP Service | Google BigQuery |
| PySpark Role | PySpark used for the ETL — transform and clean before loading into DWH |

 

## **9.2  Data Lake**

A centralized repository storing raw data at any scale in its native format. No transformation required to store. Schema applied when reading (schema-on-read). Cheap object storage. PySpark is the primary compute engine.

| Aspect | Details |
| :---- | :---- |
| Schema | Schema-on-read — store anything, define schema when you read |
| Data Types | All — structured (CSV/Parquet), semi-structured (JSON/XML), unstructured (images/logs) |
| Zones | Bronze (raw) → Silver (cleaned) → Gold (aggregated/curated) medallion pattern |
| Transactions | No ACID — raw files only (unless using Delta/Iceberg on top) |
| Cost | Very cheap — S3 \~$23/TB/month; Redshift \~$250/TB/month |
| Limitation | No ACID, data quality issues, 'data swamp' risk without governance |
| AWS | S3 \+ EMR/Glue for compute |
| Azure | ADLS Gen2 \+ Databricks/Synapse Spark |
| GCP | GCS \+ Dataproc |
| PySpark Role | THE primary compute engine — all ETL, ML, and analytics are PySpark jobs |

 

## **9.3  Data Lakehouse**

The Lakehouse architecture combines the low-cost flexible storage of a Data Lake with the ACID transactions, governance, and performance of a Data Warehouse. Built on open table formats (Delta Lake, Apache Iceberg, Apache Hudi) sitting on top of object storage.

| PYTHON | \# Delta Lake — most popular Lakehouse format for PySpark from delta.tables import DeltaTable \# Write df.write.format('delta').mode('overwrite').save('s3://bucket/delta/emp/') \# Time travel — read historical version spark.read.format('delta').option('versionAsOf', 5).load('s3://...') spark.read.format('delta').option('timestampAsOf','2024-01-01').load('s3://...') \# MERGE (upsert — CDC pattern) target \= DeltaTable.forPath(spark, 's3://bucket/delta/emp/') source \= spark.read.parquet('s3://bucket/staging/') target.alias('t').merge(source.alias('s'), 't.id \= s.id') \\     .whenMatchedUpdateAll() \\     .whenNotMatchedInsertAll() \\     .whenNotMatchedBySourceDelete() \\     .execute() \# OPTIMIZE — compact small files \+ Z-order spark.sql("OPTIMIZE delta.\`s3://bucket/delta/emp/\` ZORDER BY (dept)") \# VACUUM — remove old files spark.sql("VACUUM delta.\`s3://bucket/delta/emp/\` RETAIN 168 HOURS") \# Show history DeltaTable.forPath(spark, 's3://bucket/delta/emp/').history().show() \# Apache Iceberg df.write.format('iceberg').mode('overwrite').save('catalog.db.emp') spark.table('catalog.db.emp').show() |
| :---: | :---- |

 

## **9.4  Data Mesh**

Data Mesh is a sociotechnical architecture that decentralizes data ownership to domain teams. Each domain team owns, builds, and operates its own 'data products'. A central platform team provides self-serve infrastructure. PySpark is used within each domain for their own ETL and data product pipelines.

| Principle | Description | PySpark Role |
| :---- | :---- | :---- |
| Domain Ownership | Business domain teams own their data end-to-end | Each domain writes PySpark ETL jobs for their data |
| Data as a Product | Domain data is treated as a product with SLAs, docs | PySpark pipelines produce versioned, quality-checked data |
| Self-Serve Platform | Central team provides reusable data infra | PySpark on shared Databricks/EMR platform |
| Federated Governance | Central policies, decentralized enforcement | Common PySpark quality checks \+ shared catalog |

 

## **9.5  Data Fabric**

Data Fabric is an architecture using AI/ML and unified metadata to automatically connect, manage, and optimize data access across distributed environments (on-prem, cloud, hybrid). Think of it as an intelligence layer sitting on top of all your data assets.

## **9.6  Modern Data Stack — Full Comparison**

| Pattern | Storage | Compute | Transactions | Best For | Cost |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Data Warehouse | Columnar (MPP) | In-database | Full ACID | BI, reporting, dashboards | High |
| Data Lake | Object store (S3/ADLS) | PySpark/Presto | None (raw files) | ML, raw storage, variety | Low |
| Data Lakehouse | Object store \+ table format | PySpark \+ SQL | ACID via Delta/Iceberg | Unified batch+stream+ML | Medium |
| Data Mesh | Any (domain-owned) | Domain choice | Depends on format | Large orgs, domain ownership | Variable |
| Data Fabric | Metadata layer, any | AI-augmented | Depends | Enterprise governance \+ AI | High |
| Kappa Architecture | Kafka \+ object store | Stream-first | Eventual | All-stream, no batch | Medium |
| Lambda Architecture | DWH \+ Data Lake | Batch \+ streaming layers | Batch: yes, stream: no | Historical \+ real-time together | High |

 

# **Chapter 10 — PySpark on Cloud Platforms**

| AWS · Microsoft Azure · Google Cloud Platform — Services, Diagrams & Code |
| :---: |

 

## **10.1  AWS — Amazon Web Services**

▲ AWS Big Data Architecture — Ingestion to Analytics with PySpark

 

| Service | Category | PySpark Integration |
| :---- | :---- | :---- |
| Amazon S3 | Storage | Primary data lake; Spark reads s3:// via Hadoop-AWS connector; native partitioning |
| AWS EMR | Compute | Fully managed Spark clusters; spot instances; EMR Serverless option |
| AWS Glue | Serverless ETL | PySpark-based serverless ETL; auto-generates boilerplate; Glue Data Catalog |
| Glue Data Catalog | Metastore | Hive-compatible metastore; Spark reads table metadata from Glue Catalog |
| Amazon Kinesis | Streaming | Spark Structured Streaming reads from Kinesis Data Streams |
| Amazon MSK | Streaming | Managed Kafka; Spark reads using kafka connector |
| Amazon Redshift | DWH | Redshift Spectrum queries S3 Parquet; Spark-Redshift connector for writes |
| Amazon Athena | Query | Serverless SQL on S3; complementary to Spark for ad-hoc queries |
| AWS Lake Formation | Governance | Fine-grained access control on data lake; integrates with Glue Catalog |
| Amazon SageMaker | ML | PySpark for feature engineering; SageMaker Processing runs Spark jobs |
| AWS Step Functions | Orchestration | Orchestrates Spark job sequences; triggers EMR steps |
| AWS EventBridge | Events | Triggers Glue/EMR jobs on schedule or events |

 

| PYTHON | \# AWS Glue PySpark ETL job import sys from awsglue.transforms import \* from awsglue.utils import getResolvedOptions from pyspark.context import SparkContext from awsglue.context import GlueContext from awsglue.job import Job from awsglue.dynamicframe import DynamicFrame args \= getResolvedOptions(sys.argv, \['JOB\_NAME','bucket','table'\]) sc \= SparkContext() glueContext \= GlueContext(sc) spark \= glueContext.spark\_session job \= Job(glueContext) job.init(args\['JOB\_NAME'\], args) \# Read from Glue Catalog (backed by S3) dyf \= glueContext.create\_dynamic\_frame.from\_catalog(     database='hr\_database',     table\_name='employees\_raw',     push\_down\_predicate="dept='Engineering'"  \# partition pushdown ) \# Convert to Spark DataFrame df \= dyf.toDF() \# Transform from pyspark.sql.functions import col, upper, current\_date cleaned \= df \\     .filter(col('salary') \> 0\) \\     .withColumn('dept\_upper', upper(col('dept'))) \\     .withColumn('load\_date', current\_date()) \# Write to S3 Silver layer as Parquet, partition by dept cleaned.write.mode('overwrite') \\     .partitionBy('dept') \\     .parquet(f's3://{args\["bucket"\]}/silver/employees/') \# Also write to Delta for lakehouse cleaned.write.format('delta').mode('overwrite') \\     .save(f's3://{args\["bucket"\]}/delta/employees/') job.commit() \# ── EMR Spark Submit CLI \# aws emr add-steps \--cluster-id j-XXXX \\ \# \--steps Type=spark,Args=\[--deploy-mode,cluster,s3://bucket/job.py\] |
| :---: | :---- |

 

## **10.2  Microsoft Azure**

▲ Azure Big Data Architecture — ADLS, Databricks, Synapse with PySpark

 

| Service | Category | PySpark Integration |
| :---- | :---- | :---- |
| Azure ADLS Gen2 | Storage | Primary data lake; Spark reads abfss:// via ABFS driver; hierarchical NS |
| Azure Databricks | Compute | Best-in-class Spark; Delta Lake native; Unity Catalog; MLflow; collaborative notebooks |
| Azure Synapse Analytics | Compute \+ DWH | Synapse Spark Pools (PySpark); SQL Pools (MPP); Pipeline orchestration; linked services |
| Azure Event Hubs | Streaming | Kafka-compatible protocol; Spark Structured Streaming reads directly |
| Azure IoT Hub | Streaming | Device telemetry ingestion; route to Event Hubs then Spark |
| Azure Data Factory | Orchestration | Triggers PySpark notebooks; 90+ source/sink connectors; monitors runs |
| Azure ML | ML | MLOps for PySpark models; AutoML; MLflow tracking; model registry |
| Microsoft Fabric | Unified SaaS | OneLake (single data lake); Lakehouse; Direct Lake mode; PySpark notebooks |
| Azure Key Vault | Security | Secure storage of connection strings/secrets accessed from PySpark |
| Azure Purview | Governance | Data catalog and lineage for PySpark pipelines |

 

| PYTHON | \# Azure Databricks / Synapse Spark — reading from ADLS Gen2 \# Option 1: Service Principal auth spark.conf.set(     'fs.azure.account.auth.type.myaccount.dfs.core.windows.net', 'OAuth') spark.conf.set(     'fs.azure.account.oauth.provider.type.myaccount.dfs.core.windows.net',     'org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider') spark.conf.set(     'fs.azure.account.oauth2.client.id.myaccount.dfs.core.windows.net',     dbutils.secrets.get('kv-scope', 'sp-client-id')) spark.conf.set(     'fs.azure.account.oauth2.client.secret.myaccount.dfs.core.windows.net',     dbutils.secrets.get('kv-scope', 'sp-client-secret')) spark.conf.set(     'fs.azure.account.oauth2.client.endpoint.myaccount.dfs.core.windows.net',     f'https://login.microsoftonline.com/{tenant\_id}/oauth2/token') \# Option 2: Managed Identity (simpler, recommended in Databricks) spark.conf.set(     'fs.azure.account.auth.type.myaccount.dfs.core.windows.net',     'SharedKey') \# Read from Bronze (raw) bronze \= spark.read.json(     'abfss://bronze@myaccount.dfs.core.windows.net/events/\*.json' ) \# Write Delta to Silver bronze.write.format('delta') \\     .mode('append') \\     .save('abfss://silver@myaccount.dfs.core.windows.net/events\_delta/') \# Read from Azure SQL Database jdbc\_df \= spark.read.format('jdbc') \\     .option('url','jdbc:sqlserver://server.database.windows.net:1433;database=hrdb') \\     .option('dbtable','dbo.employees') \\     .option('accessToken', access\_token) \\     .load() |
| :---: | :---- |

 

## **10.3  Google Cloud Platform**

▲ GCP Big Data Architecture — GCS, Dataproc, BigQuery with PySpark

 

| Service | Category | PySpark Integration |
| :---- | :---- | :---- |
| Google Cloud Storage (GCS) | Storage | Primary data lake; Spark reads gs:// via GCS connector natively on Dataproc |
| Cloud Dataproc | Compute | Managed Spark/Hadoop; 90-second startup; preemptible VMs; Dataproc Serverless |
| Dataproc Serverless | Compute | Submit PySpark without cluster management; auto-scale; pay per use |
| Google BigQuery | DWH | BigQuery Spark connector writes/reads from BQ; BQ also has Spark Stored Procedures |
| Cloud Pub/Sub | Streaming | Kafka-like messaging; Spark Structured Streaming reads Pub/Sub natively |
| Cloud Dataflow | Streaming/Batch | Apache Beam managed service; Beam Spark runner can run Spark jobs on Dataflow |
| Vertex AI | ML | PySpark feature engineering; Vertex AI Pipelines orchestrates Spark jobs |
| Cloud Dataplex | Governance | Unified data governance; auto-discovers Spark-produced data in GCS |
| Cloud Composer | Orchestration | Managed Apache Airflow; DAGs trigger Dataproc PySpark jobs |
| Cloud Dataform | Transformation | SQL-based transformations on BigQuery; complements PySpark |

 

| PYTHON | \# GCP Dataproc — PySpark job reading from GCS, writing to BigQuery from pyspark.sql import SparkSession spark \= SparkSession.builder \\     .appName('GCPDataprocJob') \\     .config('spark.jars.packages',             'com.google.cloud.spark:spark-bigquery-with-dependencies\_2.12:0.36.1') \\     .getOrCreate() \# Read Parquet from GCS df \= spark.read.parquet('gs://my-silver-bucket/employees/') \# Transform from pyspark.sql.functions import col, avg, count summary \= df.groupBy('dept').agg(     count('\*').alias('headcount'),     avg('salary').alias('avg\_salary') ) \# Write to BigQuery summary.write \\     .format('bigquery') \\     .option('table', 'my\_project.hr\_dataset.dept\_summary') \\     .option('temporaryGcsBucket', 'my-temp-bucket') \\     .option('createDisposition', 'CREATE\_IF\_NEEDED') \\     .option('writeDisposition', 'WRITE\_TRUNCATE') \\     .option('partitionType', 'DAY') \\     .mode('overwrite') \\     .save() \# Read from BigQuery bq\_df \= spark.read \\     .format('bigquery') \\     .option('table', 'bigquery-public-data.samples.shakespeare') \\     .load() \# Dataproc Serverless — submit via CLI \# gcloud dataproc batches submit pyspark job.py \\ \#   \--region=us-central1 \\ \#   \--deps-bucket=gs://my-bucket \\ \#   \--properties=spark.executor.memory=4g |
| :---: | :---- |

 

# **Chapter 11 — Performance Tuning & Optimization**

| Skew · AQE · Broadcast · Partition Tuning · File Formats · Best Practices |
| :---: |

 

## **11.1  Data Skew & Salting**

| PYTHON | \# Data skew: one partition has 95% of data → job waits for one slow task \# Fix 1: Salting technique from pyspark.sql.functions import rand, floor, concat, lit, array, explode SALT \= 10 \# Salt the skewed large table salted\_large \= large\_df.withColumn(     'salted\_key',     concat(col('skewed\_key'), lit('\_'), (floor(rand()\*SALT)).cast('string')) ) \# Explode small dimension table small\_exploded \= small\_df \\     .withColumn('salt\_range', array(\[lit(i) for i in range(SALT)\])) \\     .withColumn('salt', explode('salt\_range')) \\     .withColumn('salted\_key', concat(col('key'), lit('\_'), col('salt').cast('string'))) \\     .drop('salt\_range','salt') result \= salted\_large.join(small\_exploded, 'salted\_key').drop('salted\_key') \# Fix 2: AQE (Adaptive Query Execution) — Spark 3.0+ auto-handles skew spark.conf.set('spark.sql.adaptive.enabled', 'true') spark.conf.set('spark.sql.adaptive.skewJoin.enabled', 'true') spark.conf.set('spark.sql.adaptive.skewJoin.skewedPartitionFactor', '5') spark.conf.set('spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes','256m') spark.conf.set('spark.sql.adaptive.coalescePartitions.enabled', 'true') spark.conf.set('spark.sql.adaptive.coalescePartitions.minPartitionSize','1m') |
| :---: | :---- |

 

## **11.2  Broadcast Join**

| PYTHON | from pyspark.sql.functions import broadcast \# Manual broadcast for small lookup table result \= large\_df.join(broadcast(small\_df), 'key') \# Configure auto-broadcast threshold (default 10MB) spark.conf.set('spark.sql.autoBroadcastJoinThreshold', '50m')  \# 50MB spark.conf.set('spark.sql.autoBroadcastJoinThreshold', '-1')   \# disable \# Broadcast hint in SQL spark.sql('''     SELECT /\*+ BROADCAST(small\_table) \*/ \*     FROM large\_table l JOIN small\_table s ON l.key \= s.key ''') |
| :---: | :---- |

 

## **11.3  Complete Performance Config Reference**

| Category | Parameter | Recommended Value | Purpose |
| :---- | :---- | :---- | :---- |
| Memory | spark.executor.memory | 4g-16g | JVM heap per executor — tune to data size |
| Memory | spark.executor.memoryOverhead | 1g or 10% | Off-heap for Python/native — increase if OOM |
| Memory | spark.driver.memory | 4g | Driver heap — increase for large collects/broadcasts |
| Memory | spark.memory.fraction | 0.6 | Spark memory fraction of heap |
| Memory | spark.memory.offHeap.enabled | true | Tungsten off-heap — reduce GC pressure |
| CPU | spark.executor.cores | 2-5 | Cores per executor — sweet spot is 2-5 |
| CPU | spark.executor.instances | varies | \# executors; use dynamic allocation instead |
| CPU | spark.dynamicAllocation.enabled | true | Auto-scale executors based on load |
| Shuffle | spark.sql.shuffle.partitions | 200 → tune | Post-shuffle partitions — target 128-256MB each |
| Shuffle | spark.shuffle.compress | true | Compress shuffle data — saves network I/O |
| Shuffle | spark.shuffle.spill.compress | true | Compress when shuffle spills to disk |
| I/O | spark.hadoop.fs.s3a.fast.upload | true | Faster S3 writes using multi-part upload |
| I/O | spark.sql.files.maxPartitionBytes | 134217728 | 128MB target partition size when reading files |
| I/O | spark.sql.files.openCostInBytes | 4194304 | Cost to open a file — avoid tiny file overhead |
| Serialize | spark.serializer | KryoSerializer | 2-10x faster than Java serializer |
| AQE | spark.sql.adaptive.enabled | true | Enable AQE for runtime optimization |
| AQE | spark.sql.adaptive.skewJoin.enabled | true | Auto-fix skewed joins |
| Joins | spark.sql.autoBroadcastJoinThreshold | 100m | Increase broadcast threshold for larger dims |

 

## **11.4  File Format Decision Guide**

| Format | When To Use | Compression | Schema | Analytics Speed |
| :---- | :---- | :---- | :---- | :---- |
| Parquet | Default choice for analytics — columnar, splittable | Snappy/ZSTD | Yes (embedded) | Excellent |
| Delta Lake | Production lakehouse — need ACID \+ time travel \+ CDC | Snappy/ZSTD | Yes \+ history | Excellent \+ ACID |
| Apache Iceberg | Multi-engine (Spark+Flink+Trino) — partition evolution | Any | Yes \+ evolution | Excellent |
| Apache Hudi | High-frequency upserts/deletes — CDC use cases | Any | Yes \+ CDC | Good for upserts |
| ORC | Legacy Hive workloads — slightly better for Hive | ZLIB | Yes | Excellent for Hive |
| Avro | Streaming/Kafka serialization — schema evolution | Snappy/Deflate | Schema registry | Poor for analytics |
| JSON | Raw API data, semi-structured, nested data | gzip | None (inferred) | Poor |
| CSV | Dev/testing only — human readable | gzip | None (inferred) | Very Poor |

# **Chapter 12 — Complete PySpark Module & Ecosystem Reference**

| Every Module, Class, and Integration |
| :---: |

 

▲ PySpark Module Map & External Ecosystem

 

## **12.1  pyspark.sql — Core Module**

| Class / Object | Purpose |
| :---- | :---- |
| SparkSession | Entry point; createDataFrame, read, sql, catalog, streams, udf |
| DataFrame | Distributed table; all transformation and action methods |
| Column | Column expression; col(), F.\*, operators, alias, cast, when... |
| Row | Named tuple; used when creating DataFrames from lists of Rows |
| GroupedData | Returned by groupBy(); add agg(), pivot(), apply() |
| DataFrameNaFunctions (df.na) | Null handling: fill(), drop(), replace() |
| DataFrameStatFunctions (df.stat) | Statistics: corr(), cov(), approxQuantile(), crosstab(), freqItems(), sampleBy() |
| DataFrameReader (spark.read) | Read data: csv, json, parquet, orc, avro, jdbc, delta, format().load() |
| DataFrameWriter (df.write) | Write data: csv, json, parquet, saveAsTable, insertInto, format().save() |
| DataStreamReader (spark.readStream) | Read streaming: kafka, file, delta, socket |
| DataStreamWriter (df.writeStream) | Write streaming: outputMode, trigger, start(), foreachBatch() |
| StreamingQuery | Running stream query; status, stop(), awaitTermination() |
| Catalog (spark.catalog) | Manage databases, tables, views, columns, functions, caching |

 

## **12.2  pyspark.sql.functions — All Function Categories**

| Category | Key Functions |
| :---- | :---- |
| Aggregate | count, countDistinct, sum, avg, mean, min, max, stddev, variance, first, last, collect\_list, collect\_set, approx\_count\_distinct, percentile\_approx, kurtosis, skewness, bit\_and, bit\_or, bit\_xor, bool\_and, bool\_or, product, regr\_\*, every, some |
| String | upper, lower, initcap, trim, ltrim, rtrim, length, char\_length, substring, substr, left, right, concat, concat\_ws, format\_string, split, regexp\_replace, regexp\_extract, regexp\_like, instr, locate, lpad, rpad, repeat, reverse, overlay, translate, replace, soundex, encode, decode, base64, unbase64, ascii, chr, hex, unhex, levenshtein, sentences, word, find\_in\_set, url\_encode, url\_decode, endswith, startswith, contains, ilike |
| Date/Time | current\_date, current\_timestamp, year, month, dayofmonth, dayofweek, dayofyear, hour, minute, second, quarter, weekofyear, last\_day, next\_day, date\_add, date\_sub, add\_months, datediff, months\_between, to\_date, to\_timestamp, date\_format, unix\_timestamp, from\_unixtime, trunc, date\_trunc, make\_date, make\_timestamp, from\_utc\_timestamp, to\_utc\_timestamp, window, session\_window |
| Math | abs, ceil, floor, round, bround, sqrt, cbrt, exp, expm1, log, log2, log10, pow, pmod, factorial, greatest, least, sin, cos, tan, asin, acos, atan, atan2, degrees, radians, rand, randn, signum, bin, hex, shiftLeft, shiftRight, hypot, rint, bitwiseNOT |
| Array | array, array\_contains, array\_distinct, array\_except, array\_intersect, array\_union, array\_join, array\_max, array\_min, array\_position, array\_remove, array\_repeat, array\_reverse, array\_sort, array\_zip, array\_compact, array\_append, array\_prepend, array\_insert, size, cardinality, element\_at, get, explode, explode\_outer, posexplode, flatten, sequence, shuffle, slice, sort\_array, transform, filter, aggregate, exists, forall, zip\_with |
| Map | map\_from\_arrays, map\_from\_entries, map\_keys, map\_values, map\_contains\_key, map\_entries, map\_filter, map\_zip\_with, map\_concat, str\_to\_map, create\_map, element\_at |
| JSON | from\_json, to\_json, get\_json\_object, json\_tuple, schema\_of\_json, schema\_of\_csv, from\_csv, to\_csv |
| Struct | struct, named\_struct, create\_struct, unpack |
| Window | rank, dense\_rank, row\_number, percent\_rank, cume\_dist, ntile, lag, lead, first, last |
| Misc | when, otherwise, coalesce, lit, col, expr, broadcast, typedLit, udf, pandas\_udf, callUDF, spark\_partition\_id, monotonically\_increasing\_id, input\_file\_name, current\_user, hash, xxhash64, sha1, sha2, md5, crc32, assert\_true, raise\_error, try\_add, try\_divide, try\_multiply, try\_subtract, try\_element\_at, ifnull, isnan, isnull, nvl, nvl2, nullif, nullifzero, zeroifnull, iff, decode, mask |

 

## **12.3  pyspark.sql.types — Schema Types**

| Type Class | Equivalent | Example Value |
| :---- | :---- | :---- |
| StringType() | string | 'hello' |
| IntegerType() | int | 42 |
| LongType() | bigint / long | 9876543210 |
| ShortType() | smallint | 32767 |
| ByteType() | tinyint | 127 |
| FloatType() | float | 3.14 |
| DoubleType() | double | 3.14159265358979 |
| DecimalType(p,s) | decimal(10,2) | Decimal('99.99') |
| BooleanType() | boolean | True |
| DateType() | date | date(2024,1,15) |
| TimestampType() | timestamp | datetime(2024,1,15,9,30) |
| TimestampNTZType() | timestamp\_ntz | timestamp without timezone |
| BinaryType() | binary | bytearray(b'abc') |
| NullType() | void/null | None |
| ArrayType(elem) | array\<elem\> | \[1,2,3\] |
| MapType(k,v) | map\<k,v\> | {'a':1,'b':2} |
| StructType(fields) | struct\<...\> | Row(name='Alice',age=34) |
| StructField(name,type,nullable) | column definition | StructField('age',IntegerType(),True) |
| VectorUDT() | ml vector | SparseVector / DenseVector |
| MatrixUDT() | ml matrix | SparseMatrix / DenseMatrix |

 

## **12.4  pyspark.ml — All MLlib Modules**

| Module | Classes Available |
| :---- | :---- |
| pyspark.ml.feature | StringIndexer, IndexToString, OneHotEncoder, VectorAssembler, StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler, Normalizer, Binarizer, Bucketizer, QuantileDiscretizer, PCA, Word2Vec, HashingTF, IDF, Tokenizer, RegexTokenizer, StopWordsRemover, NGram, CountVectorizer, ChiSqSelector, UnivariateFeatureSelector, Imputer, FeatureHasher, Interaction, DCT, ElementwiseProduct, PolynomialExpansion, SQLTransformer, VectorIndexer, VectorSizeHint |
| pyspark.ml.classification | LogisticRegression, RandomForestClassifier, GBTClassifier, DecisionTreeClassifier, LinearSVC, NaiveBayes, MultilayerPerceptronClassifier, OneVsRest, FMClassifier |
| pyspark.ml.regression | LinearRegression, RandomForestRegressor, GBTRegressor, DecisionTreeRegressor, GeneralizedLinearRegression, IsotonicRegression, AFTSurvivalRegression, FMRegressor |
| pyspark.ml.clustering | KMeans, BisectingKMeans, GaussianMixture, LDA, PowerIterationClustering |
| pyspark.ml.recommendation | ALS (Alternating Least Squares collaborative filtering) |
| pyspark.ml.evaluation | BinaryClassificationEvaluator (AUROC, AUPR), MulticlassClassificationEvaluator (accuracy, f1, precision, recall), RegressionEvaluator (rmse, mse, r2, mae, var), ClusteringEvaluator (silhouette), RankingEvaluator |
| pyspark.ml.tuning | CrossValidator, TrainValidationSplit, ParamGridBuilder |
| pyspark.ml.stat | Correlation, ChiSquareTest, Summarizer, KolmogorovSmirnovTest |
| pyspark.ml.fpm | FPGrowth (frequent pattern mining), PrefixSpan |
| pyspark.ml.linalg | DenseVector, SparseVector, DenseMatrix, SparseMatrix, Vectors, Matrices |
| pyspark.ml.image | ImageSchema (read images as DataFrames) |
| pyspark.ml.param | Param, ParamMap, HasFeaturesCol, HasLabelCol, etc. |

 

## **12.5  pyspark.pandas — Pandas API on Spark**

| PYTHON | import pyspark.pandas as ps \# Read data — same as pandas but distributed psdf \= ps.read\_csv('s3://bucket/large.csv') psdf \= ps.read\_parquet('s3://bucket/data/') psdf \= ps.read\_json('s3://bucket/data.json') psdf \= ps.from\_spark(df)              \# convert Spark DataFrame psdf \= ps.DataFrame({'a':\[1,2\],'b':\[3,4\]}) \# Use pandas-style operations — distributed psdf.head()                           \# first 5 rows psdf.describe()                       \# stats psdf.dtypes                           \# column types psdf.shape                            \# (rows, cols) psdf.columns                          \# column names psdf.index                            \# index psdf\['salary'\].mean()                 \# mean of column psdf\[psdf\['salary'\] \> 80000\]          \# filter psdf.groupby('dept')\['salary'\].mean() \# groupby psdf.merge(psdf2, on='id')            \# join psdf.sort\_values('salary')            \# sort psdf.fillna(0)                        \# fill nulls psdf.drop\_duplicates()                \# dedup psdf.rename(columns={'old':'new'})    \# rename \# Convert to/from Spark spark\_df \= psdf.to\_spark() pandas\_df \= psdf.to\_pandas()          \# careful — pulls to driver \# Apply function per group (distributed) def normalize(pdf):                   \# receives pandas DataFrame     pdf\['salary'\] \= (pdf\['salary'\]-pdf\['salary'\].mean())/pdf\['salary'\].std()     return pdf psdf.groupby('dept').apply(normalize) |
| :---: | :---- |

 

# **Chapter 13 — Orchestration, Testing & Production Patterns**

| Apache Airflow · Unit Testing · Data Quality · Best Practices |
| :---: |

 

## **13.1  Orchestrating PySpark with Apache Airflow**

| PYTHON | from airflow import DAG from airflow.providers.amazon.aws.operators.emr import (     EmrAddStepsOperator, EmrStepSensor) from airflow.providers.google.cloud.operators.dataproc import (     DataprocSubmitPySparkJobOperator) from airflow.providers.microsoft.azure.operators.databricks import (     DatabricksSubmitRunOperator) from datetime import datetime, timedelta with DAG('pyspark\_etl\_pipeline',          schedule\_interval='0 2 \* \* \*',          start\_date=datetime(2024,1,1),          default\_args={'retries':2,'retry\_delay':timedelta(minutes=5)},          catchup=False) as dag:     \# AWS EMR step     emr\_step \= EmrAddStepsOperator(         task\_id='run\_on\_emr',         job\_flow\_id='j-XXXX',         steps=\[{'Name':'EmpETL','ActionOnFailure':'CONTINUE',                 'HadoopJarStep':{'Jar':'command-runner.jar',                 'Args':\['spark-submit','s3://bucket/employee\_etl.py'\]}}\]     )     \# GCP Dataproc     dataproc\_job \= DataprocSubmitPySparkJobOperator(         task\_id='run\_on\_dataproc',         main='gs://bucket/employee\_etl.py',         cluster\_name='my-cluster',         region='us-central1',         project\_id='my-project'     )     \# Azure Databricks     databricks\_job \= DatabricksSubmitRunOperator(         task\_id='run\_on\_databricks',         json={'run\_name':'emp\_etl',               'existing\_cluster\_id':'xxxx-cluster',               'notebook\_task':{'notebook\_path':'/etl/employee\_etl'}}     ) |
| :---: | :---- |

 

## **13.2  Unit Testing PySpark Jobs**

| PYTHON | import pytest from pyspark.sql import SparkSession from pyspark.sql.functions import col from pyspark.sql.types import StructType, StructField, StringType, DoubleType \# Shared SparkSession fixture @pytest.fixture(scope='session') def spark():     return SparkSession.builder \\         .master('local\[2\]') \\         .appName('TestSuite') \\         .config('spark.sql.shuffle.partitions','2') \\         .getOrCreate() \# Test transformation def test\_salary\_filter(spark):     data \= \[('Alice',95000.0),('Bob',60000.0),('Carol',110000.0)\]     df \= spark.createDataFrame(data, \['name','salary'\])     result \= df.filter(col('salary') \> 80000\)     assert result.count() \== 2     names \= {r.name for r in result.collect()}     assert names \== {'Alice','Carol'} \# Test schema def test\_schema(spark):     schema \= StructType(\[         StructField('name',StringType(),True),         StructField('salary',DoubleType(),True)     \])     df \= spark.createDataFrame(\[('Alice',95000.0)\], schema)     assert df.schema \== schema     assert df.schema\['salary'\].dataType \== DoubleType() \# Test aggregation def test\_group\_avg(spark):     from pyspark.sql.functions import avg, round as fround     data \= \[('Eng',90000.0),('Eng',100000.0),('Mkt',70000.0)\]     df \= spark.createDataFrame(data, \['dept','salary'\])     result \= df.groupBy('dept').agg(fround(avg('salary'),0).alias('avg'))     row \= result.filter(col('dept')=='Eng').first()     assert row\['avg'\] \== 95000.0 |
| :---: | :---- |

 

## 

## 

## **13.3  Data Quality Checks**

| PYTHON | def run\_data\_quality\_checks(df, spark, table\_name):     '''Comprehensive DQ checks — returns pass/fail dict'''     results \= {}     total \= df.count()     \# 1\. Completeness — no nulls in required columns     null\_counts \= df.select(\[         F.sum(F.isnull(c).cast('int')).alias(c) for c in df.columns     \]).first().asDict()     results\['completeness'\] \= {k: v==0 for k,v in null\_counts.items()}     \# 2\. Uniqueness — check primary key     dedup\_count \= df.dropDuplicates(\['name'\]).count()     results\['unique\_names'\] \= (dedup\_count \== total)     \# 3\. Range validity     invalid\_salary \= df.filter((col('salary')\<=0)|(col('salary')\>5\_000\_000)).count()     results\['salary\_valid\_range'\] \= (invalid\_salary \== 0\)     \# 4\. Referential integrity     valid\_depts \= {'Engineering','Marketing','HR','Finance','Legal'}     bad\_dept \= df.filter(\~col('dept').isin(list(valid\_depts))).count()     results\['dept\_referential'\] \= (bad\_dept \== 0\)     \# 5\. Timeliness — no future dates     from pyspark.sql.functions import current\_date     future \= df.filter(col('hire\_date') \> current\_date()).count() if 'hire\_date' in df.columns else 0     results\['no\_future\_dates'\] \= (future \== 0\)     \# 6\. Row count threshold     results\['min\_row\_count'\] \= (total \>= 100\)     \# Summary     all\_pass \= all(v if isinstance(v,bool) else all(v.values()) for v in results.values())     print(f'DQ for {table\_name}: {"PASS" if all\_pass else "FAIL"}')     return results, all\_pass |
| :---: | :---- |

 

## **13.4  Production Best Practices**

| Rule | Recommendation | Why |
| :---- | :---- | :---- |
| DO | Use DataFrames over RDDs | Catalyst optimizer; 10x+ faster in most cases |
| DO | Use Pandas UDFs over regular UDFs | Vectorized via Arrow; 10-100x faster than row-by-row UDFs |
| DO | Filter & select early in the pipeline | Reduces data volume before expensive shuffles |
| DO | Cache DataFrames used multiple times | Avoids redundant recomputation — use .cache() \+ .unpersist() |
| DO | Enable AQE (spark.sql.adaptive.enabled=true) | Runtime optimization; auto-handles skew, coalesces partitions |
| DO | Broadcast small lookup tables | Eliminates join shuffle — critical for performance |
| DO | Write Parquet with partitionBy() | Partition pruning at read time — scan only needed files |
| DO | Tune shuffle partitions to data size | Default 200 is rarely right — target 128-256MB per partition |
| DO | Use Delta Lake for production tables | ACID \+ time travel \+ schema evolution \+ CDC |
| DO | Checkpoint streaming queries to durable storage | Fault tolerance — resume from last checkpoint on failure |
| AVOID | df.collect() on large DataFrames | Pulls ALL data to driver — causes OOM for large data |
| AVOID | Python for loops over DataFrame rows | Kills performance — use vectorized DataFrame operations |
| AVOID | Joining two large skewed DataFrames without salting | One executor becomes bottleneck — job hangs |
| AVOID | Nesting UDFs inside UDFs | Compounded serialization overhead |
| AVOID | Creating millions of tiny files | Read performance degrades — use repartition \+ coalesce |
| AVOID | Ignoring shuffle partitions setting | Default 200 often causes too many or too few partitions |

# **Chapter 14 — Quick Reference Cards**

| At-a-Glance Reference for Daily Engineering Work |
| :---: |

 

## **14.1  Complete DataFrame Method Quick Reference**

| Method | Returns | Description |
| :---- | :---- | :---- |
| show(n,truncate,vertical) | void | Print first n rows. truncate=False for full. vertical=True for one col per line |
| printSchema() | void | Print schema tree with types and nullability |
| describe(\*cols) | DataFrame | Count, mean, stddev, min, max for numeric columns |
| summary(\*stats) | DataFrame | Extended stats: count, mean, stddev, min, 25%, 50%, 75%, max |
| explain(mode) | void | Print execution plan. Modes: simple|extended|codegen|cost|formatted |
| count() | long | Total row count — triggers execution |
| collect() | list\[Row\] | All rows to driver — dangerous with large data |
| take(n) | list\[Row\] | First N rows to driver |
| head(n) | list\[Row\] | Alias for take(n) |
| first() | Row | First row |
| isEmpty() | bool | True if no rows |
| schema | StructType | Schema object |
| columns | list\[str\] | List of column names |
| dtypes | list\[tuple\] | List of (name, type) tuples |
| select(\*cols) | DataFrame | Select columns or expressions |
| selectExpr(\*strs) | DataFrame | Select using SQL string expressions |
| withColumn(name, expr) | DataFrame | Add or replace column |
| withColumnRenamed(old,new) | DataFrame | Rename column |
| withMetadata(col,meta) | DataFrame | Attach metadata dict to column |
| drop(\*cols) | DataFrame | Drop specified columns |
| filter(cond)/where(cond) | DataFrame | Keep rows matching condition |
| groupBy(\*cols) | GroupedData | Group for aggregation |
| agg(\*exprs) | DataFrame | Aggregate (global or after groupBy) |
| orderBy(\*cols)/sort(\*cols) | DataFrame | Sort rows ascending by default |
| distinct() | DataFrame | Remove duplicate rows |
| dropDuplicates(cols) | DataFrame | Remove duplicates by specified columns |
| limit(n) | DataFrame | Return first N rows (lazy) |
| sample(frac,seed) | DataFrame | Random sample fraction |
| sampleBy(col,fracs) | DataFrame | Stratified sample by column |
| union(df2) | DataFrame | Stack two DataFrames (by position) |
| unionByName(df2) | DataFrame | Stack by column name (handles different order) |
| join(df2,cond,how) | DataFrame | Join: inner|left|right|outer|semi|anti|cross |
| crossJoin(df2) | DataFrame | Cartesian product — every row × every row |
| repartition(n,\*cols) | DataFrame | Shuffle into N balanced partitions |
| coalesce(n) | DataFrame | Reduce partitions without shuffle |
| repartitionByRange(n,col) | DataFrame | Range-based repartitioning (sorted) |
| cache() | DataFrame | Mark for caching on first use (MEMORY\_AND\_DISK) |
| persist(level) | DataFrame | Cache with explicit StorageLevel |
| unpersist() | DataFrame | Remove from cache |
| is\_cached | bool | True if cached |
| createOrReplaceTempView(name) | void | Register as session-scoped SQL view |
| createOrReplaceGlobalTempView(n) | void | Register as cluster-scoped SQL view |
| createTempView(name) | void | Register (fails if exists) |
| dropTempView(name) | bool | Remove temp view |
| write | DataFrameWriter | Access write methods |
| writeStream | DataStreamWriter | Access streaming write methods |
| toDF(\*cols) | DataFrame | Rename all columns at once |
| toPandas() | pd.DataFrame | Convert to Pandas — collects to driver |
| toJSON() | RDD\[str\] | Convert to RDD of JSON strings |
| toLocalIterator() | Iterator | Iterate rows one at a time (less memory) |
| rdd | RDD | Access underlying RDD |
| na | DataFrameNaFunctions | Access null-handling functions |
| stat | DataFrameStatFunctions | Access statistical functions |
| rollup(\*cols) | GroupedData | Multi-level rollup aggregation |
| cube(\*cols) | GroupedData | All combinations aggregation |
| pivot(col,values) | GroupedData | Pivot rows to columns |
| applyInPandas(fn,schema) | DataFrame | Apply pandas UDF to groups |
| mapInPandas(fn,schema) | DataFrame | Apply pandas UDF to partitions |
| mapInArrow(fn,schema) | DataFrame | Apply Arrow UDF to partitions |
| observe(name,\*exprs) | DataFrame | Add metrics observation to query |
| hint(name,\*params) | DataFrame | Add optimizer hint: broadcast, coalesce, etc |
| transform(fn) | DataFrame | Apply custom function to DataFrame |
| when(cond,val) | Column | Conditional expression (in column context) |
| replace(to\_replace,value) | DataFrame | Replace values in columns |
| fillna(value,subset) | DataFrame | Fill null values |
| dropna(how,thresh,subset) | DataFrame | Drop rows with nulls |
| to\_pandas\_on\_spark() | pyspark.pandas.DataFrame | Convert to pandas-on-spark |
| checkpoint(eager) | DataFrame | Checkpoint to truncate DAG lineage |
| localCheckpoint(eager) | DataFrame | Checkpoint to executor local storage |

 

## **14.2  SparkContext Key Methods**

| Method/Property | Purpose |
| :---- | :---- |
| sc.parallelize(data, numSlices) | Create RDD from local Python collection |
| sc.textFile(path) | Create RDD from text file (one line \= one record) |
| sc.wholeTextFiles(path) | Create RDD of (filename, content) pairs |
| sc.binaryFiles(path) | Binary files as (path, bytes) pairs |
| sc.sequenceFile(path) | Hadoop SequenceFile |
| sc.pickleFile(path) | Pickled Python objects |
| sc.range(start,end,step) | Numeric range RDD |
| sc.broadcast(value) | Broadcast variable — share read-only data to all executors |
| sc.accumulator(val) | Create accumulator (distributed counter) |
| sc.addFile(path) | Distribute file to each worker |
| sc.addPyFile(path) | Add Python .py/.zip to worker PYTHONPATH |
| sc.setJobDescription(desc) | Label current job in Spark UI |
| sc.setLocalProperty(key,val) | Set thread-local Spark property |
| sc.version | Spark version string |
| sc.master | Master URL |
| sc.appName | Application name |
| sc.applicationId | Unique application ID |
| sc.defaultParallelism | Default parallelism (usually 2x cores) |
| sc.defaultMinPartitions | Min partitions for textFile etc |
| sc.getConf() | SparkConf object |
| sc.stop() | Stop SparkContext |
| sc.uiWebUrl | Spark UI URL |
| sc.runJob(rdd,fn,partitions) | Run job on specific partitions |
| sc.cancelAllJobs() | Cancel all running jobs |
| sc.cancelJob(jobId) | Cancel specific job |
| sc.setCheckpointDir(dir) | Set checkpoint directory |
| sc.emptyRDD() | Empty RDD |

 

## **14.3  Spark Configuration Cheat Sheet**

| Parameter | Good Default | Notes |
| :---- | :---- | :---- |
| spark.master | yarn / local\[\*\] | yarn in cluster; local\[\*\] for dev |
| spark.app.name | MyApp | Shows in Spark UI |
| spark.executor.memory | 4g-8g | JVM heap — tune to workload |
| spark.executor.cores | 2-4 | Sweet spot; too many → GC pressure |
| spark.executor.memoryOverhead | 10% or 1g | Off-heap; Python, native, OS |
| spark.driver.memory | 2g-8g | Increase for large broadcasts/collects |
| spark.driver.maxResultSize | 1g | Max size of collect() result |
| spark.sql.shuffle.partitions | 200 (tune\!) | Target 128-256 MB per partition |
| spark.default.parallelism | auto | 2-4x number of cores in cluster |
| spark.dynamicAllocation.enabled | true | Auto scale executors |
| spark.dynamicAllocation.minExecutors | 1 | Minimum executors |
| spark.dynamicAllocation.maxExecutors | 100 | Maximum executors |
| spark.sql.adaptive.enabled | true | Enable AQE (Spark 3.0+) |
| spark.sql.adaptive.coalescePartitions.enabled | true | Auto-merge small partitions |
| spark.sql.adaptive.skewJoin.enabled | true | Auto-fix skewed joins |
| spark.sql.autoBroadcastJoinThreshold | 10m (tune) | Increase for larger dims |
| spark.serializer | KryoSerializer | 2-10x faster than Java |
| spark.memory.offHeap.enabled | true | Tungsten off-heap |
| spark.memory.offHeap.size | 2g | Off-heap allocation |
| spark.memory.fraction | 0.6 | 60% of heap for Spark operations |
| spark.sql.files.maxPartitionBytes | 128m | Target partition size when reading |
| spark.rdd.compress | true | Compress cached RDDs |
| spark.io.compression.codec | lz4 | Fast compression codec |
| spark.speculation | true | Re-launch slow tasks on another node |
| spark.task.maxFailures | 4 | Retry failed tasks before failing job |
| spark.hadoop.fs.s3a.fast.upload | true | Faster S3 multipart uploads |

 

   
   
   
 

| 🎯  You now hold the complete PySpark Engineering Reference. |
| :---: |

   
   
 

| This guide covers: Chapters 1-14 encompass PySpark architecture, DAG execution, memory management, the complete DataFrame API (60+ methods), all pyspark.sql.functions categories (300+ functions), full RDD API, structured streaming with Kafka, MLlib pipelines with all algorithms, data warehouse / data lake / data lakehouse / data mesh patterns, AWS EMR+Glue+S3, Azure Databricks+Synapse+ADLS, GCP Dataproc+BigQuery architectures, performance tuning (AQE, skew, broadcast, file formats), orchestration with Airflow, unit testing, data quality, and production best practices. |
| :---- |

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,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AwAAAACwCzAzAAAAAAC7ADMDAAAAALALMDMAAAAAALsAMwMAAAAAsAswMwAAAAAAuwAzAwAAAACwCzAzAAAAAAC7UGBmllb1H92DfPnBebX1ClchZyA4zzRt7h7kywcAAAAUBWNm0l0cj5yEIEh3cTZyBoIg3cXxyEkAAAAAmAIwM2ktLkFOhURai3uQsyGR1uIS5FQAAAAAWaGbmfQVVyEnxED6inuQs2EgfcVVyAkBAAAAYGYhISfEQPqKe5CzYSBlxVXICQEAAABCMjNpKm5DzomOlBW3IedER8qK25BzAgAAwOXAzEJCzomONBW3IedER5qK25BzAgAAwOXAzEJCzomONBW3IedER5qK25BzAgAAwOXAzEJCzomONBW3IedER5qK25BzAgAAwOXAzEJCzomONBW3IedER5qK25BzAgAAwOXAzEJCzomONBW3IedER5qK25BzAgAAwOXAzEJCzomONBW3IedER5qK25BzAgAAwOXAzEJCzomONBW3IedER5qK25BzAgAAwOXAzEJCzomONBW3IedER5qK25BzAgAAwOXAzEJCzomONBW3IedER5qK25BzAgAAwOXAzEJCzomONBW3IedER5qK25BzAgAAwOXAzEJCzomONBW3IedER5qK25BzAgAAwOXAzEJCzomONBW3IedER5qK25BzAgAAwOVEhpl5vd775xNlfV650rHY/ZSjDy6fvVT/hQLpUM6JjjQVtyHnREeaSuHwr23bH7t4UdYXPnJOAAAAuJzCM7P0Vm96fSFX5YpFM/M+fMD935jW/n7q8UsNXzYa3N2/hhtEnJnRsE9fusU/5VrbIudER5pKKOw8c/b23bvJV6+1XrRYrtUJbmZpN278fVS0rD9x6bKsDBE5JwAAAFxO4ZnZwyupj+7fvb069vr45mk+N2JRo7ja58s0n36RWt1eOTKtxv+mxavdPr6bsIXq7p3YrVo+uJLCvd07Hvco89ad9RMv1vkvtQs2M4r7Zw89rvEF7Zq6vXcqnhfvHtqgzCx78cBavZkx7ODIOdGRpmKdhw8fFe26zqj0BjWzv7RffebSrVI91neec3DE6kTZoPCRc6IjTSXf/L5n76Npaf8U3UbVfDh8xM2srJSMjH+OaUeLG0+cyLiTGXfmzDOamdF8rko4WnzosG2nTl24fn3Mtu1Jly/zwUCh9/83LaKKDBos9xsick4AAAC4nMIzM7rVZe1emh791r0Tu9JyzOxa3/KXm//p0Z0bl+o9T5UXv/kXqrw+pjGVH2XdJlVS21Kkty3i9T3xutzytbtHt5KT0WLm5hk/78JnZg8uJHFviltLfuQN759L4AKb2Y2p7TLjFl6s+X+MZtaRc6IjTcU6hpl5n3xmVnt03O27Dy7fyCrSaY1q81X/zacu3nq348819cfspGYXMzLf77yWOzl8LoML6TezqH+eWIrvRu7YffIKFQ6evab3Py8uWfWWD+Sc6EhTyTd/HxVNg8+8d6/T8hWkYr/t0Svr/v3/aN/xu2nT5+7b/3L3HqRor/bpy43ZzKIWLKRVf9si6s69e5uSkj6PHeP12ZjfZ2Yfjxj1i2Yt5H5DRM4JAAAAl1NIZnax9n8qCaC4tag/mxmvpcKdtePubJhCkkTl2ytHcCWpkmrAj7ge3cuin2RUtxYNkHthM6M2VPi55w1Tro9vwfvSzezR7YxHmTfTW/9FNrOOnBMdaSrWCWJm/ZdkvwoOsi59q/k7k9MyMqk+8cKN/kuPUoEqX2uz4t6Dh2/ErPTmiJdXMzPV/4QNJ7ms968a5A85JzrSVELnwcOHNGayLq9Ps/5bsxZ3HzxotXBR37XrVBsys2t37tzIyvpj7z7P+J6c9V6zVq2VZkadpGZk6DUFhZwTAAAALqeQzOz62Ca3FvzAZTKnB+nnjGdmN2d3Ize61OBFb46ZGc/MdDNLj3qDVqVH/9nYC5vZ1R++fnQvM2N4bd6Qur2XuNMrzIw6vNr904cZF/kLcHoz68g50ZGmYp1gZpajXIGgbamBXzM7nGw+M1P9/2xmufVvHTknOtJU8s1LXbt/MHjIP0W3uXPvXvLVa8Yzs19375mSkfGn3j9wY35mVmzIMJKw3/XsnXnvXoomXomXLr3YpZve+dsDBpHGyZ2GjpwTAAAALqeQzEyiPzOLXOSc6EhTsU4QM6PFurE7b2Xep8Vl8amqTfFu6y7fyCIJ2510pcqQbVTTYMyuO3cfXLqexZ9mDlh6NOP2Pa8vDDP7buSOPdqnmar/EBVNzomONBV7QhpXZeJkWR86ck4AAAC4HJhZSMg50ZGm4jbknOhIU3Ebck4AAAC4nLCZmTOQc6IjTcVtyDnRkabiNuScAAAAcDkws5CQc6IjTcVtyDnRkabiNuScAAAAcDkws5CQc6IjTcVtyDnRkabiNuScAAAAcDkws5CQc6IjTcVtyDnRkabiNuScAAAAcDkws5CQc6IjTcVtyDnRkabiNuScAAAAcDkws5CQc6IjTcVtyDnRkabiNuScAAAAcDkws5CQc6IjTcVtyDnRkabiNuScAAAAcDm2NrPMHfMvfvOv/PdOvdn/rGmQbJPe6s3M7fNkPXFn/QRZWbDIOdGRppInxv/0+I/yh4WiXdet3Hde1ucJOSc60lRswus/9Ju0c6esN9rIyrwi5wQAAIDLsa+ZXfz23+4dj+NyVvyq9LZFZJvgXBtQWVYWLHJOdKSp5IlSPdbTz0W7U25l3q89Ou61Niuu3b7H/wOA2J10hX7Oi0veczK78FHPn0heb2be33L0Ei9yszdiVlIPSWk3qQe1YcVBW3YlpZ+5dKvbvENUU2HQlltZ94+lXjcaz41LrvjjVn1IeUXOiY40lVzZevIU/Vx77Pg3U6fN2hsvGxj8rmdvWUlsSDzBhWc7daF5u3Tzpr7WMLOJcTuvZ2YWHzrMaKMv5g85JwAAAFyOfc0svc3b6mEYmdmNqW0v1vmvq73KZq9qW+Ry8z9dbvHKxToefmZ29+D6Sw1+SatuTIlJq/Y/H/cQ/ZbstmCRc6IjTcU65Qdu4cLq/efJybhMhe/H7uJy9WHb6eeyvanDVx0fvOIYqdi+01d5Vd3YncrMGozZRT2obidsOEkbzt+ZrGrazti/YOc5v42/6r95w5GLajEfyDnRkaaSK3uTz5GWcZnMjPRoc9LJa3fukKhRTZ81a89evVp6VOyvu/c8fP7Cg4cP2cxo8eGjR7So+nl7wCAukJk94/u3m//QqvX7Pw7hSup2+ZEj6bduNZg1mxZnx8f/t2YteNXwzVvo5/6UFGqz4/RpaqP6zAdyTgAAALgc+5qZ8czs9sqRapV6fpbe9l02s+uxDbnmUsNf3U3YcnNOj7QIf2amzKzz7IOkXyxkXq/3zt0HXM+6Fj01vsKgLScu3NDNrMOsA8rMuIele1O4h11J6bQhmRz3RjF4+TFelI2/GrD5p8NpalU+kHOiI00lV65nZh5NS+Mym9mLXbqReB1MPf/pyNEz9+4lx4o/d67F/AWdl694JueZGS3+IketGGVa/Mzssk+wdDNLycj4Vbcep9LT/3ebtrWmz5i6a/cnI0c986SZ0b6oDTXQe84Tck4AAAC4HPuaGXGl/ftcIDOj8qPMm/fPJ6b5zOzeid0Pb17NLvvM7NbSwQ9vXbs+pvGthf0e3cvM2r30Ur3nM7fPlX0WLHJOdKSp5ImSvk8zu88/9F7ntZevZ5Fv/aX9an5UFrsuiX52mXsw5zt4XjazYl3X9Vl0hJopM4uaEk89fNFvE/VAW307YgdVpmVktpm+74Mua7cnXn6305oL1zLf7biGDE9vTM3m7kiuNNiOn2YuOHDg/2veks2M60mVSo+KJX/SG29OOllu3Hgu/13LVrTI5R6rVqs2/MyM+U2Pnv8U3ebz2DHU7blr137ZtftJn5k1mDWbfp6/fp08bNupU9SG1lIbakDAzAAAABQgtjazQOTjO2dPCTknOtJU8gT/BsCcHWdv3Lk3YnXiX9uvvnP3wcm0m6/6Hn2pn6/6Pnb8pNcG8rNbmfe3Hnv8PTM2tnc6rKYe0m9mUQ/U/vU2K2ltxR+37k66cu7K7aErj2cv+r5ndjTlut64aJe1NvwNADaz/uvXT9gRZ5gZ/ey5eg295DNXrnBh4YGDr/bpy/WZ9+7RIjf+KTFRdaib2TO+Z3JDNm7iTzOv3L7Nn2aO2rL12p07/BBu8s5d1IafmcWdOUNt9M3zipwTAAAALicizcw+yDnRkabiNuSc6EhTcRtyTgAAALgcmFlIyDnRkabiNuSc6EhTcRtyTgAAALgcmFlIyDnRkabiNuSc6EhTcRtyTgAAALgcmFlIyDnRkabiNuSc6EhTcRtyTgAAALgcmFlIyDnRkabiNuSc6EhTcRtyTgAAALgcmFlIyDnRkabiNuSc6EhTcRtyTgAAALgcmFlIyDnRkabiNuSc6EhTcRtyTgAAALgcmFlIyDnRkabiNuSc6EhTcRtyTgAAALgcmFlIyDnRkabiNuSc6EhTcRtyTgAAALgcmFlIyDnRkabiNuSc6EhTcRtyTgAAALgcmFlIyDnRkabiNuSc6EhTcRtyTgAAALgcmFlIyDnRkabiNuSc6EhTcRtyTgAAALgcmFlIyDnRkabiNuSc6EhTcRtyTgAAALgcmFlIyDnRkabiNuSc6EhTcRtyTgAAALgcmFlIyDnRkabiNuSc6EhTcRtyTgAAALickMwsy/VyJifEQMqKe5CzYSBNxVXICQEAAABCNbMsF8uZnAqJ9BX3IGdDIn3FJcipAAAAALIKxMyyXClnchKCIK3F2cgZCIK0FscjJwEAAABgCsbMslwmZ/LlB0e6i7ORMxAc6S4ORr58AAAAQFFgZhYWPEUay0rA0ORgfoKAyQEAAGBDYGaOBWYWHEwOAAAAGwIzcywws+BgcgAAANgQmJljgZkFB5MDAADAhsDMHAvMLDiYHAAAADYEZuZYYGbBweQAAACwITAzxwIzCw4mBwAAgA2BmTkWmFlwMDkAAABsCMzMscDMgoPJAQAAYENgZo4FZhYcTA4AAAAbAjNzLDCz4GByAAAA2BCYmWOBmQUHkwMAAMCGwMwcC8wsOJgcAAAANiQizYydQ0e2cTOYnCDg4AEAAGBnYGYOBJMTBBw8AAAA7ExEmlnWk/dXudblYHKCg/kBAABgW2BmzgSTExzMDwAAAHsS8WYmV4EszE9uYHIAAADYk0g1syzcXHMD8xMETA4AAAB7AjNzLJifIGByAAAA2JOQzKxxVFcAQMEiTzQAAADuIf9mRreQNAQCUdABOQMAADeTTzMzbyYIBKLgAnIGAACuJT9mhqdlCMTTDsgZAAC4E5gZAmHHgJkBAIA7gZkhEHYMmBkAALgTmBkCYceAmQEAgDuBmSEQdgyYGQAAuBOYGQJhx4CZAQCAO4GZIRB2DJgZAAC4k3Ca2XPvNzmWeIoKniKN//BJNNdE9ZzEa6nyp237qIYKvyzW/J3ynbg++Vxqlx9nvfBBU9pk174E1Zi62r0vgQqqhrsqXfsH6odrqLfffBjVe8S8cympab7d8X/padZ1vFqkBiWr96A23A/H8nU7P/62Fw3jzS/a0eLLJVvwhsygcYu5ULRKt6nzf+JN1FruPG7vYSp/Gz1C9UmL/KJoMFT+7YdRPABeq6aCxs+V5y9coIG9VLz5W1+2rxMzSvXDjY2XlpYzgDR/o5WD0WPNpj1qGK+UbpN8LuXJ9bkHbR58KxotjcqsDRrUZ5GKnc3atLQaLYfRqsWrt1duOlgNWw/ekF6I37V6BHqxdGgZ2wYaTP/YhSt/2mXW5itgZgAA4E5sZ2akXHsPHONKZWbU7NXSMVt2HqD6qs2HUE1i0pmFq7bRVgcOJ3JjaWbUVdqTZkZt9h8+ToVyDQfqA+DgfVGDxp3HUeHCBbUmjbSpSIXORxNPxU5fxTULVm7T79bc+YtFm/FOVY1q0KH/9GffI8VsRiNXDbgH6tPjz8x4KpSZfd9xTJVmg0lGF6/ZUb3l0JyOHzc2Xlqar3/aI+/OGC0NxpPtuz8PRg9++VwOJCvBw/MUzCxQlKjWnXbHh0GQKBwz23foeIMOY8zafAXMDAAA3IntzKzLj7PIJzbHHfBoZsbwVlT4qkF/VS5bty8XDDMj7aCuqB/DzKhQt+1obqY6HztjtVrkzalNp4EzuUzxWpkYWlWmzg89h83lmkBm9mbZ7IdqXKM6J4mkwvbdh+jnp9/15gY0wsnz1kf3nszNpJnxVLCZDZ+8XN+dEWom1UujPZK90R55d3K0tFYfjB600w9r9uSykhW2kynz158/f+Gl4s1p2ucu26L32d5ne1z2+MyMJJJaJp06Sy3rt4tN842ThCbh2ElqYJhZ8rlU6mH0tJW8ecwPU/W1XEnb8jDmr9i6acf+v37dkeqLVu5KNQeOJPIzM9mAN9TNjAZG46eBUQ0PjMMwM35FNCTV594DR3/zYdTxE6e5T30eVD9UPpvsR+/yGjAzAABwJ7Yzs5Onzv7x09aVmvzo0czs1JlksrFJc9dx46+/H8A9eIKaGXVF/UgzqxMzipupAXDoYkRtOg/62czolsxPklQD6TrEr0u2XLNpj6pRnas9Fq+a/YCHK2mEZDm0yE99pJnxVDw2s0k/m5k+DNXYeGlUmLYg+3NVWty594gcLa3VB6NHEDPjSh4AQ2tpZl4tnW2uegOqHzj28Ye8xBuft+V60h0uKDPjHp57L/u1s5DxJqQ+/BJUn8rMuOaXxZqnBTAzvQFvqJuZHBiHerH6K6IhGa+dVYz6VJ3o/XhgZgAAAEIgnGb2ymdt9h8+nsb3zgrZnw2RYaRpN05lZlTZc9jcVr7vXdEi3TW5B75xcoG62rIz+0kbryLv4XoyHsPM3i7XkZsFMjMSJmozf8VWtYpj3ea91ObEST+fD1L5yLEk+slfROMa1flLxZvzK2K4Uo2QjJPHaZhZmm8qqJ4qN+3YTz9PnzlHlV/U66fvmhvrL42UTt9jp4Ez9dGe9D0rMgajx1tftqfUcDmQmXUcOIPLQycuo8VGncYa7khbDRizyOifFjsIM+MezqWkUg/RvSdTTVTPSfyQ8jcfRunbCjPLnsCgZvZ4hg0zo4Gp8euhXqz+imhIQcxM9qMOzhADZgYAAO4knGaWmHT6zbLt6PbZqtdkdg7WEYqxM1Z7NDN7/oOmZDwkTGnabwD8/uOffwOgadfx1BUpBXXFNXxXVv2k+e6p1NuvS7XsNdz8DQC6qatFalCiWndqw/1wfP39ALrjkiR9Ub8f10gzo/v3hm37qJB06izXqM7p5/J1O7kledXiNTvSckaoNvdrZryKK+nlF63S7cWizf7yVYdvWw1X23Jj/aWpr6al5WicPlpaKwejh/4bACOnrPAIJVq6No53QZw6nVypyY80KjVOij992prL1PI3PrOs23Y0LY6etvKNz9tyS2Vm3ANXsplxuXjV7jRsbsOVoZgZvRAalfpyGI1fHxiHerH6K1JmxrCvczN9HriffqMXLl//eG5DDJgZAAC4k3CaGcK2UaHRoJTU82YtImikpp6n9wZmbX4DZgYAAO4EZoZA2DFgZgAA4E5gZgiEHQNmBgAA7gRmhkDYMWBmAADgTmBmCIQdA2YGAADuBGaGQNgxYGYAAOBO8mNmhHkbQSAQBRfQMgAAcC35NLMsPDlDIJ5OQMsAAMDN5N/MsnxyBgAoWOSJBgAAwD2EZGYAAAAAAKAAgZkBAAAAANgFmBkAAAAAgF2AmQEAAAAA2AWYGQAAAACAXSgAM0ur+o8AAAAAyDfy3hqEZ5o2B/ZEJisfhGRm8tgCAAAAQP6Q91mJkgAvwk5hCzNTR5I5OgQCgUAgEHkJi3IGIbN5FIif5dPMoGUIBAKBQBRg5CpneFRm/yiQjzVDMjNzRAgEAoFAIPIbQcwMWhYpATNDIBAIBMIhATNzRoTBzKBlCAQCgUA8jQgkZzCzCAqYGQKBQCAQDgmYmQMCZoZAIBAIhEMCZuaAgJkhEAgEAuGQgJk5IGBmCAQCgUA4JGBmDgiYGQKBQCAQDgmYmQMCZoZAIBAIhEMCZuaAgJkhEAgEAuGQgJk5IGBmCAQCgUA4JGBmDgiYGQLhPwaOW+4p0jjtcsbN25kx/WYuWL1LraJ6Qi1Wazn8T5+1ocJH3/Sm+kePHnEbrqToPmwBLV7JuEnly1dvULlC48GZWfcSTqQsXR+vt7mUfv1xp0/2oPZI++LCxfQMKnxQuZtsbNTMWLr91yVbDpqwQl/rffIF7j18KtALlHvkF6hetRHVWmS3V5tn1/h6INZtO0SLc1fE6Q3UOLnZbz9slX7t5vWbd6g8dtZP3pxZ3XfkzN1795dv2EdTdzXjlupcbShruCvvky9H9qY2CT4MuRcEwoYBM3NAwMwQCP/xdrlOge7E+p3eq93UB09cSfVnUy9zG79mVqvNaLrr0y1fba63sW5meqXRWNZMmLuRFjfvOqY3sPgC5R75Bfo1s/MXrz33fpMv6g+gZvcfPORKZWZVmg+lxU++6/NisWZy5KpZx0FzdCWiApnl4x34C+lMeldeMVF+ezPMTA5D7gWBsGHAzBwQMDMEwn/UaTeG79BETL+Z+nMa/U7v1W7q/DxGtZFmtm3vcSoMmbRKbasir2bGT7AadZ6gN2CSz6cbm/OiesDGob/AP3zSOtALDLRHZTB64/cqdeVyxSZD6rSN1VtOXrCZfn7XejT9LFqlu9rE86SZ0eTQT6VE+ow16TqJ9zVq+jreVu9fQS9f76php/FcTy399qY6CTIMv3v5eQQIhG0CZuaAgJkhEP4j/drN+h3GqTtxtRbD1Sr9ju598p799feDVBtpZlv3ZJvB0Mmhmpna153Mu7Kx3xqPz4e09VZfYKA9KpXRQ204Z0XcC0Wb8YeJ3ANtSP733PtN/vJVxyBmRs3eKNt+865jHp8SGTPG/fs1M1nDXT37XhM1Kr+9qU2CDEPVP94BAmHXgJk5IGBmCETuQbfk338crS/qN2l1Ux80YQXVr9x0gNuQE2TdvUflhp3G/+7jaP56Vp4+zaQeVPl3vgHofqAPwxPUzEbPWEeLm3Yd1Rvo0enHuYFeoNwjv0BpZrcz79La7fGJqvGH3/TmltxD6sWrvy7Zkl57EDOjwoOHD3lH6tPM333USjX2WDYzr6+rYlWz96XvzuhNbRJ8GHIvCIQNI0LNbNBPG2h4Ry5cSMnIKDM6tvb0GVTp6dhZjZkK1SdPUWX9tVB56q7dPVatzhaa+/dVDRXqzJiptsq8d4/qd5w+rTa0bcDMEAj/UanpkHGzN9zJvJuSdpVuye0HzFar9Du6V7upk3OQdZWp24/K/FWqAWOX7Tl06jelon4YvYQbX7ry+DcASNqOn76w7KeAvwHAPdy6k0U9UIF70P2A9qXKnsBmNm3R1l+VaCF/A0B/gZ/X7R/oBco98guUZjZnRdxz7zehAfMid3LwWLJ0muBmxpWeHCUqUa0HlY+cSLl37wHXWzczCvJI3ooXZW9qk+DDkHtBIGwYEWpm/z0qWg0vNSODynFnzuTJzK7cvk2FXWfPqhovzMw6MDMEAoFAIJ5GRKiZ0dhIzvTFpnPn58nM8MxMATNDIBAIBMIuEblmZshWt5Wrnu3URTezmlOmBWpM/Fu7Dl+OGadqlJmprWBmwYCZIRAIBALxNCJCzaz/+vU0vIS0tFTf98y+nTrdm/Pls8u3bh06f/7/b95yT3IyN5Zmxh6m17w76Efa6n+1iVFbwcyCATNDIBAIBOJpRISaGcWc+H3/0Kr137Vs9UqfHx76fl+Kfv64YSNV/p+YdisTElTLXM2Mtvpj7z601fs/DlGVMLNgwMwQCAQCgXgaEblmhlABM0MgEAgEwiEBM3NARIyZvdp6BbAJZm5CCNk5CBdmbkII2TkIF2ZuQgjZOQgXZm60gJk5ICLAzBJSMoENMfOUx5AdAjtg5imPITsEdsDMUx5DdgjsgJknX8DMHBB2NzN6cyAPR2AHgr9vCx5Iq21BWh0J0upI/KYVZuaAsLWZ4Ypgc/xeF3INpNXmIK2OBGl1JDKtEWpm/Edl+Z8yeZ/87Usq/KFXH/lfm67duTNz797/3abtkkOHVWVOf9nxi2YtNied3H02ueaUaQdTz+urbB62NjN5FAK7YebMQshOgN0wc2YhZCfAbpg5sxCyE2A3jJRFtJn9fVR0+q1bZ65c+c8OnXi0/D+XViVk/89fv/+1aeSWrdT47oMHhpldvnXr71q2up5pzk9EBMwMhISZMwshOwF2w8yZhZCdALth5sxCyE6A3TBSFtFm9qfeP1Dhn2PaLT10mEc7bvuO4P+16f7Dh1RefPAQV+ovUy0+17nLofN4ZhYUmJmTMHNmIWQnwG6YObMQshNgN8ycWQjZCbAbRsoi2sxit23jcSozW3TwIBUy793jZs/4/muTbmYpvgdpO06flp9mxp87127JUu6w6qTJ+iqbB8wMhISZMwshOwF2w8yZhZCdALth5sxCyE6A3TBSFtFmphaVmXlzvmem/9cmbpxxJzPI98xo7eKDh9Ju3KgwfgLV/7hho1pl/4CZgZAwc2YhZCfAbpg5sxCyE2A3zJxZCNkJsBtGypxnZnPi9xUZNFj/r03c+L9HRb/QpVvFCRO5mf5p5sIDB+/cu0dr/0er1r/u3rP7ylW8YaQEzKwA8BRprNArR8/bKRs7DDNnFkJ2Yk9kWmeuPoy0BgrZiT1BWvMUshN7EiitsqXzMFIWoWaG0ANmVjCU+ravrHQDZs4shOzEtiCt1kN2YluQVushO7EtSCsHzMwBATMrGPiiQO/SarQet//0zYScZ2b0c8z8Xc++16Ri85F6edDUTbS4Mu4MLfYas4bKtCFvJTu3M2bOLITsxLYYaVUPV6yklRsjrTYEabUeshPb4jet/SdtsJ5WdemWndsZI2UwMwcEzKxgUBeFkXN2cI261u85ce0Pn7Thi4IqN+kx05Pz7L1mm3H0U20YWZg5sxCyE9tipFW/heeaVm6MtNoQpNV6yE5si9+0Nu01y3paZZ8RgZEymJkDAmZWMKiLgvq2Cl/rq0bFvlC0GZXpQqCXj5y706LPXL4o9IzNfmbGG0bc1cHMmYWQndgWI63qFm4lrapxAtJqM5BW6yE7sS1+03rg9E3raeV+Ij2tMDMHBMzsqUPn/4vFmtP7M6PsDMycWQjZSSSCtBohO4lEkFYjZCeRiKvSCjNzQMDMni78hqxqqzFxR6/oZdkyQjFzZiFkJxEH0ipDdhJxIK0yZCcRh9vSCjNzQMDMQEiYObMQshNgN8ycWQjZCbAbZs4shOwE2A0jZTAzBwTMDISEmTMLITsBdsPMmYWQnQC7YebMQshOgN0wUgYzc0DAzEBImDmzELITYDfMnFkI2QmwG2bOLITsBNgNI2UwMwcEzAyEhJkzCyE7AXbDzJmFkJ0Au2HmzELIToDdMFIGM3NAwMxASJg5sxCyE2A3zJxZCNkJsBtmziyE7ATYDSNlMDMHBMys8Fi986wnj38ph9o36DJN1tsHM2cWQnYC7IaZMwshOwF2w8yZhZCdALthpAxm5oCAmZnsOJrO/jRqblyFZiNlg6dNVN95eRW4MGLmzELIToDdMHNmIWQn4SXu6JW/fN35xWLNXy/bXq7VodPts7qDEvL13imyMHNmIWQnYYH/2oWsl83orazfN7R6ZaBE814mLY3nfwghG9gTI2X5MDOq33/1Gih8zEzkBMzMRJlZ/Mnrb37Zkc9hruk+etVbX3d+t2L3YTO30uIP49e98EH2n5Omco/Y1S8Vb/FB1V5U3nLoIl3oeSu9zF2pDl8o2uzg2VtHzt1p0jP7/4cQYxfuTnjSzDy+q8mKHafVJrR3+vle5R7GTsOFmTMLITuxP5sPpn3XbuLLJaOKVe89bOY22cBhmDmzELKTMLLv1I23y3cdOWfHnhMZc9cflQ10PDlm5njMnFkI2UlYeKVMu2ffayLr/cKXzSCVwc2Mrq6uMjNoWRjxmxEvzEzCZkb85sNWmw5coHO4bqcpVN96wEKqnLJ8f7+JP1GhzcDsRd6EVzFTVxxYsiXptx9FU/nXpVrpZd3MaKs+49aNmL0jZtAiXuw8fHlwM6PF6tFjqbBhXyr9NHYqX0jhYObMQshO7A9NcsNuM6iw/chlzoUy7PJNR5Bhk6a/U6ErLU5beZCMmQyejDmMeQkRM2cWQnYSRjoNW6ZOImLcwj20uDcpo1KLUXRKUu7I2ziVdEZ7xDMz2YDOSjpDqcBdNe01i7oiV5i/4RhvQmsnL9vXa8yalj/Mnb02QQ7JDpg5sxCyk8KnXqcp245cip2/c/TcuEWbEtsPXrL/9E26rqoGlCl+g+oRz8xeL9tBrXqnYre+E9Z7tIswZbNFn7n0JvxXJVruSMhOd7kmwxt2mz542maVa3XYLNh4nN6c05X/0zoDVN7tgJGyPJkZtMwOGEnhvMgMWsexZqYW6Rzmk5y0ieqb955TpWUsXZHHL8o+aekduVp14PRNtRWV+UmYXvZrZnS54X7KNhicJzOTOw0LZs4shOzE/tBUdxmxgsu/LNY8wd/Nu0brcaoxXe7J2PhyL3uzP2bOLITsJIwMm7lNnUQJOe+dqEBvqwZO2aTeblElnYMef2ZmNKCzsuPQpZ6cd0TqHZq6Q9NaMjO6f3t8vr5wU6IcVdgxc2YhZCeFzL6TN35dKopn9cuGQ6nmjS86DJm+had93Z5zvPalEi0SnjSzT+sMNFbVaj9pw77zHu0ibLy/9fjMjM7Z96v09OTkOiHnsDly7s7XjYd9+G2/Fz5oZqvvnBgpg5lFHEZSOC8yg9ZxoJmFhd2J16pGxS7bdkqusjlmziyE7MT+/LV8F3qPvuv41e/aTeQrslJ2T87N+5uY8dyYyjEDF8lOIggzZxZCdhJe6P761tedXyja7JXSbWmx68iVpNTvVOiaIHJHb7fIofUbttGgTofJLxVvwfdv7urNLztRV4Onb6FFWsuryMxY10gI6A2eHFLYMXNmIWQnhcwntQeozzFpbtsPXvJqmXZU6DVmDdWs2nmG1tLii773Sx7NzN6r3MNYRdAxULXVGJVo4i/lujz/QVOP79mYx2dmCb4nbSrX6rDhTt6t2P37rtN5F8ZQw4WRMphZxGEkhfMiM2gdmFkB8OaXHem6z18dizjMnFkI2Yn92XTgwjcxE+j+XbRar8HTNieIm3evsWvJ3jw5n2bS5Z7vBHS5l73ZHzNnFkJ2AuyGmTMLITsBdsNIGcwsCL9o3lJWhh0jKZwXmUHrwMzcjpkzCyE7AXbDzJmFkJ0Au2HmzELIToDdMFLmDDPj0cr6EIGZBQRm5iTMnFkI2QmwG2bOLITsBNgNM2cWQnYC7IaRMgeYWfyVq3/TIqry1OkdVq+lxY0pqTx4YtTuPWrx+a7daZEajIvf91q/Af/arkO5SVP09v/RodPg7Tuopvv6DVR+SrYXOkZSOC8yg9aBmbkdM2cWQnYC7IaZMwshOwF2w8yZhZCdALthpMwBZjZy1+4SI0YtOJ74at/++3NMa/jOXctOnvqH6DaLTyTx4v+KaUeLm1JS/y4q+s8DBg2N28kvR7Wnn8927rrweOIvmrd8sVuPtitX2/P1GknhvMgMWgdm5nbMnFkI2QmwG2bOLITsBNgNM2cWQnYC7IaRskg3s20X0si0eLRE3bnz2LR4LRX6bNz87x06Ufnj2DG0yEJWZ8481QO1Jw+jwt+2bEW0WbGKGtSaPXfnxUs2fL37YWagwDFzZiFkJ8BumDmzELITYDfMnFkI2QmwG0bKIt3MOq9dp0ZFXvV/O3bO/ZlZy1bsaoxhZguOJ/6iWQs8M8sFmJmTMHNmIWQnwG6YObMQshNgN8ycWQjZCbAbRsoi3cwk+jMzXmTxcgxGUjgvMoPWgZm5HTNnFkJ2AuyGmTMLITuJaJq26ycrIx0zZxZCdgLshpEymFnEYSSF8yIzaB1XmFm/kbNKla25+Kf9vPjRl99+VT1vf/05xKv8+l0nQ+zh6WHmzELITsJI9Xptin5WtVKtKLkqEKu2HZOV+WjDRHX+UVaGHTNnFkJ2YkMGj1sgK/1inHFr4+z4N/3zipkzCyE7sQltug/jAmfKtlfIQsBImfPMzPEYSeG8yAxaxxVm1nfEzD2JV6rVa03luISLm/cnz1y6XTbLEy06DJCVgYCZPSX2Jl6ZsnDTvqRrs1fEbT98QTbwi1/roju3nlO/bRL85R1mVggcOXeHC2xmlJ2qdVuX/LxGvRbdyMupZsOe0+VqNH23VHm1CZ1xO45coJqqdbP/P2ONBjFvl/h62uItJcvWLF2h3qzlO6iT+lHdS5SpPnbWmm4DJtCbt9HTVnQbOIEa0xGl9mgrzJxZCNmJHTh45mbZyt9vOXAuwbKZyVPPMRgpg5lFHEZSOC8yg9ZxhZnRJZguyot/yv7v1LHTV3Il38jpQt9n2HSuadauH93pK33Xksozl20nh1M98FWjdMV6ZHXlv2mWkHOZ4E02xZ/lvVBh9Y7jVJ4wZx1veDj59sS569nMeF92u+KbObMQspNwMWD0HFXuOmA8pYASRDdpWiRXU6lhaP558vVmdKumZvNW75ZmRttujD/zeaX6XEN57NR3LLehw6N2085cz0cF92YfzJxZCNlJeDlw+galZvT0lZ9VqKueeCkzMxqThNHJ+MPwGer8ojOOzvH3PqpE535CzjOzgbFz3ylZjqBK6qRlx+z/tlnh2xbqskBsPZDyTcP2Rv82wcyZhZCd2IHGbfpMXrCxXM3sa6lhZlMXbd574iqdmLzIl1B16jFcw+X6LbvTcVLxu+z/ralORv0M1S/s9sRIGcwsV1YdSpCVYcRICudFZtA6rjCzBN977q9rZP/vNnXCHzxzI+HJC7q6ZMcnXRsQ+/MtPyHnqqGu4wk5ZsabELSJulvsSbxSt3n2v2lTNwY2M94XXfRtJWdmziyE7CRcjM8xYGLIhIX6DVvdg9v2HMH3Zpp/mnzK9cptR1Uz5XbSzLjQJOYHymP1+tlPXL5v1ZPb0OGh7uV8VNgNM2cWQnZiQwKZGVPz+3YrtyZwmc64kVOW0T1+3Ozs/8+4ce8ZOu9mLd+x+9jjf1FPnfDzTjqj6S6u3ok1at27VZfBsnM7YObMQshOwg55UvHS1eiaSW97Vm8/ZpiZ/nZLXULVqaefjNxmzIxV9LNs5e8TtJNRP0P1C7vq2VYYKYsgM9tw4hRNLBXiL1+Ra58eMDM/RJyZRXUaVPTTKnNW7uTFj7789stqjbjcc/BkOrAaRvciUaNyqS++oXddvKrk5zX4jp6Qc9VQ13H6Sff4d0uV5024mbpb0KWEbglU2BR/tlTZmh37xLKZ8b7e/7gSS6FNMHNmIWQnYaRavdbZ3zPzvSE2btgqNQzNP00+5XrZpsOqku7WxT6rSscDvTWnnCpxf/x5WdmalErK45dVG1Ee6d055z3B94iOOh89bQU+zXQY3zRsJyttgpkzCyE7CTvfNe4wY+k2KqzblURyZpgZnZLFy1Tnb6GpS6g69fSTkdu37jaUTmH+SEQ/GdUZalzYbYiRssgys5pN2k5atV6ZWcmyNT6rWHfauk1Uue/K1enrN8enP161dO+ButFd6rfpRvXFSlf7skajnqMnGc3WHDlGGk2J5k2iew+mlgvisv9PAG1eo1FMic+r7/eZWeehYyeuXL/zfFqluuH/f01GUjgvMoPWcYWZgSCYObMQshNgN8ycWQjZiQuZvSJu+pKtst4mmDmzELITYDeMlEWcmVVtEM1mRoK1I+X8uqOJFWo3b9tv+LL4g50Gxy7cuZcbk1p9WqE2FcjGqNnMjdvmbttpNBs4ZQ6JmuqfTI5aUm+8+fpjJ0jd9vvMjMr1WncdPmfxgMmz5cAKGSMpnBeZQevAzNyOmTMLITsBdsPMmYWQnQC7YebMQshOgN0wUhZxZrYh8WTlelG0OG3dpm3JKbyqdlTn6o3aNOvSVz3TIrVq0W3Afs3M/Dbbc/FyjUYxXK7Xuhu1LF+rGW+u9sufZk5Zs7Flj4GqMowYSeG8yAxaB2bmdsycWQjZCbAbZs4shOwE2A0zZxZCdgLshpGyiDMzKrT+YQjXlPqy5tslvi5dqW6/iTNrNI4ZNnvR19804VXKzHyfZlb9onpDKhvNug0f//7HlRrEPP5rZ616/Ugt52/fxZur/bKZUT+LdsWryjBiJIXzIjNoHZiZ2zFzZiFkJ8BumDmzELITYDfMnFkI2QmwG0bKIsjMwsv640myMiwYSeG8yAxaB2bmdsycWQjZCbAbZs4shOwE2A0zZxZCdgLshpEymFnEYSSF8yIzaB2Ymdsxc2YhZCfAbpg5sxCyE2A3zJxZCNkJsBtGymBmEYeRFM6LzKB1nq6Zvdp6hTwKgX2gBJk5sxBIq81BWh0J0upIZFrzZGZeyFlY8ZsRr83NzIvrgo2RVwTrgbTaFqTVkSCtjsRvWvNqZl7IWfgwM5ETdjczr++6gEuDreCMmHnKYyCtdgNpdSRIqyMJktZ8mBnCbhEBZsbBByKwA2ZuQgjZOQgXZm5CCNk5CBdmbkII2TkIF2ZutICZOSAixswQCAQCgUAED5iZAwJmhkAgEAiEQwJm5oCAmSEQCAQC4ZDIn5nxWlDImGnIiWdgZggEAoFAOCPyYWbP4Hczw4SZiZyAmSEQCAQC4ZDIq5lJXQCFid+kwMwQCAQCgXBI5MnM8LTMDhhJ4bzIDFoHZoZAIBAIhF0CZhZxGEnhvMgMWqfwzOz59m+B8GKmJL/xTNvDILyYKQklYp8BYaaAosXrk0B4MVOSr4CZRRxGUjgvMoPWKQwzk4oAwoWZm7yHtAQQLszc5COkJYCwEHJISwDhwsxNHsPNZrYxJfXFbj1kvc0xksJ5kRm0zlM3M7KBhIxTwCaE6GdkA+duPAQ2ISQ5YyG4eQbYgtD8jGzgdoYX2IQQ5SxCzYxG8tHoMeuSz3VYvXbgtu2ygRUCmdm/tOtgn1cqMZLCeZEZtM7TNTP2AOkHIIzk28ygZXYjpCdn0DK7kV8zg5bZkFDkLBLNbHbC0f/Zpu2OtIuqJnbP3lf69v/3Dp3KT55Ci2RsPH5qRvV/27LVnwcMIg/jSuL5rt33a2Y2Ln7fa/0G/Gu7DuUmTXmuSzfVjFZR/f9o1Zrqt56/IEcSFoykcF5kBq3z1M1MmgEIO/mQM5YAKQcgvOTTzKBl9iTvcsYfn0kzAOEllI81I9HM2q9e89bAH/UaGljdufP2XblKErY3/QqZ2f/t2Jnr3xwwqO/mLVRgM/u39h2p/uPYMUPjdiozUyrGL1A9M4tevkLVk/bJkYQFIymcF5lB68DM3AjMzDHAzBwFzMwpuM3M5DMzn5nN181MKVeRIcN+2PSzmbFgSTOrM2ee6k2ZWatlK/R6m2AkhfMiM2gdmJkbgZk5BpiZo4CZOQW3mdl+39Osl3v0+vuoaPo5Pn7f6N17Xunb/9/ad1SfZgYyM+a5Lt32a59mjtkb/3r/gbyKFjutWffPbdvzKqr/h+g2VF967Hg5jLBgJIXzIjNoHZiZG4GZOQaYmaOAmTkFF5pZPmAz8/uV/8jCSArnRWbQOjAzNwIzcwwwM0cBM3MKMDNXYSSF8yIzaB2YmRuBmTkGmJmjgJk5BZiZqzCSwnmRGbQOzMyNwMwcA8zMUcDMnALMzFUYSeG8yAxaB2bmRmBmjgFm5ihgZk4BZuYqjKRwXmQGrQMzcyMwM8cAM3MUMDOn4AYz23Di1Nslvib0ysYd+9DPVYcSZPvgWNlk6d4DLboN4DLvyCYYSeG8yAxaB2bmRmBmjgFm5ihgZk7BJWYmK0MxsxX7Dzfr0lfV0KLRBmYWDJhZpAMzcwwwM0fhIDNLSb75fqXust4veWpMeIo0zlP7wsclZsbPzOZt2xXTbxjVlK/VzDAzcqlPK9SmwvT1m3eknF93NHHglDk9YyfzWt6KCWJm8elXxi5Z1WHQKOrtk/K11yYcL1O5Hu+oSacfqNsKtZurrcKCkRTOi8ygdWBmT5cdyUfoIiLrw4tLzOxQyg2afFmv89z7TWVlBAEzcxSRbGY3rz0qUa3XL4s1/02pVhu3nsiTbOWp8e3AZkb1Vy/dk/WFj0vMjAvztz82s3LfNZVmxrLVb+LMd0qWI9YkHCed6hU7Zd+Vq1bMbNPJM+99XJH8r35Md+qtcYfeVNmoQ2/eEfdJa+NSw/k/NI2kcF5kBq3jfDNr1n9Cr8nzqPDc+03ovF2+f9fENev82hJV7r+UKOtDAWZWCEQPmMcGdvziHSpsPHhu1rqDVICZBQzbmNn2bVvK1Or5UvHmf/myLddQyrKuJMmWQVZRDy+XaEGdjJwwhxZfL9OGWspmEUAkm1njTlPqxoxLOnH1zOnrC5fvy5Ns5alxEGBmhYkys9WHj1b7vvWUNRs/rVBbmhl//jht3aZtySlq2xqNYpbs2U9bkVHRhrwJSVudVtn/W5OhRbK3obMWxqWeH71wed3oLvwEbt2xE2Wq1OcdNevST+82XBhJ4bzIDFrH+WZGbvSn0q2p8IdPo4vV7Faj3bCP6/RiW6KfpGuvlY05dCXpL+U70CLXz9y8idq8UqZNve6x3AOv6j5hDheefa9xqVo9qcNP6/fZcfYId0VQV036jlftCWVmPSbO/bJp/30Xj8sRFj4OMzNlYB2GLS5Rs8937cZ/WneARzMzLhBvfNFh+ur9VDN6/nYqcyV38nHtfi+Ximrcc3rC+ZtUGbtgR5FK3V4s2iwpPYsWa3eYKPdrByLdzGhui1XupBaL5JyGvOr595v8+YuYTv3GG6vI535TqiUZ2I2044lH9lIPNy8l6n2qlps3b/q8dk/qpE3PMVdSjqpVM+YsoU6+rNubOmndI1YOLDxErJmNnb6ZZlWvIdmimhVrD9PPd8p1OZJw6VfFW6Sl3lm25lDjjpMTEi69XKJl/L4U1ZjMbPjE9XXajMtIf8A5Onbs8h8/bZOafOvw4bRfFmt+9syNqXN3UIPbOc/MuNme+HNq1x6YGQgHRlI4LzKD1nG+mSX4tGltwt6KUT+SNr3+RdsXijZ7uVQLXnXg8omoQZMGzl7MzfZfSqSW9OablGtCzqM1tquRS1ZuPX2ICnO3b6H21Gb14T202H7UDLUj6sqTY2PU/vDVk1zuPnEu/TyYfkKOLSw4zMyIIpW7bz+a9nmDH6P6zSXlejE7xVGGmc1en52+v5bvfM73qIzEa9C0Ddxga8KF96p0P3A2gxZrxoyln993m+rxXfcXbTmWnc252+RO7UCkm9kbn2c/3/q6fp8fR8/kGo/2YOzu1ZO9Bk/25DwA41Wnju37VYnm5GRr161v1mkk1VA9nY/UScaFY94nn5n9sliz4lU6z56/jGrYzBYvW/Xg+mlaRZ2Ua9CHOlGNw4+zzOytLztSga63LxVvQdbFJxTxZtkOIyb9pLenxtSMam5cfXjbJ1hvlG1PhXox48nkeFtavHXtEZ3aN6489OSYmdoF9+OBmYFwYCSF8yIzaB23mNk7lTst2Lltx9nHT7Paj5z+w7QFHp8t9Z2+kIyNm5GZsUVFD56iNie7eqdSJyqwmVFhfty2L5v2500a9Mx+rkaFOl1HUVce7TkZb0vlX5dq+YdPo+XAwoXzzGzMwjiSM5rqQ+euc4q7jlqumxl5GBVeLNacoALVtx28kJ+H0WK/Ses6DFv8uEHRZlWiRlN9tejY9kMWlak/6O0KXeUebUKkmxkTv3vH8+83uX7huDdHvyb6TqV7105OnrnI86SZxU7K/vDabydUT53oZkaFvsOmPrqRrWiXfCejak/lPkOnyn7CScSa2W3fp5kkUkknriafubFoxX71AeUvizUnDh9OIz87eOgCNz7ie2a270AqL3LjDVsSXyvd9tChND6FrTwzU7vgfqgm8Xi6HFvhU2hmRiFFARQmfpMCM8sdPs8PpidRmRyLyjM2bew5KdvAyNU+qtNLmdmG4/tXH97zy+LNXysboza3bmYf+T4nlWY2a8vm7Gdsh/YYAwsXzjOzXScu0zz/qkRLKpOEUXnh5qNBzOy595oYz8zer9JDPTMbNDW7nnRt7obsz2Ka9Jwh92gTIt3M6rUZErdj67FDe35VojnX0IQnJx0YO2U+FdJTEr7wnVP6qqSj8XQ2JR7Zy5VnE/dTDzcvJVIn/GW19yt2VJuQkJV48pmZ2jV18ucvYvTBhJ9INrMbVx+WqNor+3F1iZbkWIaZUWH9puO//bAVpaBhh+wBb9qaxIu3te+ZvVC02Rtl23tynq4VqdCVO1+z4ejLJVvSqvMpt28HNrNXPotRleGlMM0Mj83CiN+MeGFmIB84z8xcS6SbGXiCSDazAsQmdhUKhWlmHLwWFDJmGnLiGZgZyCswM8cAM3MUMDOnUPhmhrBVwMxAnoGZOQaYmaOAmTkFmJnLA2YG8gzMzDHAzBwFzMwpwMxcHjAzkGdgZo4BZuYoYGZOAWbm8oCZgTwDM3MMMDNHATNzCoVvZrwWFDJmGnLiGZgZyCswM8cAM3MUMDOnUJhm9gz+akb48JsRL8wM5AOYmWOAmTkKmJlTKEwzk7oAChO/SYGZgTwDM3MMMDNHATNzCoVmZnhgZgeMpHBeZAatAzNzIzAzxwAzcxQwM6cAM3MVRlI4LzKD1oGZuREHmFnixVvJ1x+oxWMXbsg2T4PaTTuezbgv68NFpJvZ7UvHGzVrLeut8NPqxc1btdNrbqQdrVSjgWwZhIbNWj+8fkrWhweYmVOAmbkKIymcF5lB67jUzAZMGEc/96QeMep3JR+SjQ0GT51kZaveo0dNWDJP1tsBB5hZxe+y//1lQkqGXPVU2XLgZIOo7H/BaRMi3cyqfdfoWuoRvabqtw1lM7+VZcp/Z9Tkw8wSD2439C6cRKyZzZm7ln5+Uy/6yMFkuVZRoUYT+ln522Z6pbFIXEy9xS2tcz75uupn5OhZskEhAzOjgW1MSV2adDLXEf6ieUtZ+S/tOuS6oX0wksJ5kRm0jkvNrNy3DROespmt3r+1TlRbWW8HIt3MEi/eKlOxHhXqtuj8domvm7Ttzc/MDp29EtV5QPHS1ZZu2ksNFq7fSZVlKtWjmlPpWXoPJT+vUalWi1HTFtMmbXsOLfZZ1cHj53zyda2uA8YkX39Qq2kHajN04jxu0Kb74OJlqh1KvkKVtLZU2ZpySOEi0s3si4q16Gd68qG6DaMolXNmTaWfBFXSzzLlvp0/ZwaXuZIalChdpWPn7vUaZbefPHH8maO7uCsqG2Y2cfzYj76oPmDAIOqf3K5kmaqNm7cxdvfwxmlqIwcWHiLWzEiM6Gfp8nXkKp3CMbOD+0/LBoUMzAxmJjNoHTea2ZYTe6WZbTu5b3fKYeVYy3Zt3JoUv//iscFTHnvYwm1rqYaaKTPjTRKeNDNVSZQsW13V2wrHmJl6ZqbMjBenLf6JfpauUHf8nJV8U2/Xa5jafNysFVxg8eJy76GT6OfYWcv7DJvMZjZk/Fy9wXeN25+DmRU0bGa3Lh7r80O/zt16njm2ix+P3biQENW6A+cuYd8WriRL4xq2tM++/oZ+0ibc1cQJ43Qzmzd7+rBhw6gwd9Y0UrEK1etT+VRCnLE7mFnonDpxiQuffl1LVZ45mZ6WcpMK9Zt0pJ/jJsyfMnVpEDOL236kUs2mKWeuUXs2sz27jn/XIObqxax+g8ZPnrKkyIcVNm86oDqvWqvFuTPX3vuoIjVo32WQbmbE9fT7+i4KH5iZYWZUpsLwnbv+V0y7f4hus/B4IgnZ+uRzbVeu1l/CrkuXabHz2vXKzJacSPrzgEFbz18YGrfz83ET5I7sgJEUzovMoHXcaGbxF45+VrFWQo6Z7U45Uqx0FbrWr9izSTnWiNnT+AYQ3bMP1wyfOZULZGb6Jgk5ZmZUHrl2Emb29OBPM5Mu3TmZnnlOmNn0JRvo52cV6qzfdTQ+KU3/Rhqxaju9qb508Gy6Ll7lv2lKLcnJyOo+LVf7wOnL1eu35gYrtuxPunynU99R1GzrwVP4NLMAqfZdo4zzjz/NnDNzaofO3ctWrJV15cSqZQtaRLdPTdpLpnVozyauPLh7Y/3GrR7dOM3t2czI4S6dOXD57IFaDZrrZhYft77KNw2vphz+vmk0mVmRD8tnpicOHz5c7Zp3d+IQPs0MlcsX7nCBzYyErETpanQljN+TdDvHzMaMmxfczGbMXDloyGQqTJ+5gs1s1uxVSsS79hxe6ZvsZtR58+ieXElmVvW7FlRJLXUzu3Xtkd5/WICZSTP7t/YdqfBx7BiqiVm5iut3Xrz0uHDp8r+26/CLZi1osebMWcrMopev4BdO/HuHTnJHdsBICudFZtA6bjSzhCe/ZxZ35kDRzyrXiWq7dNcGWnzv44rfx3SiwudV6rxTshwpmtqqxOfVKtRqRGZmbMJb1Y1qp1f2iR09Ht8ze2oYvwGQD3Ynpm45cFLWGyh1Y2o37Xjm2j3ZLFxEupmF8hsA1iEzq1G7saz3+n4D4EEGfgMgVPh7ZmxmKWeuFfusapOobrt3HafF4aNmkKh17z1CmVn7LoPe/7hSVEwf3pYXqTBqzOwPy9bs1TdWfZo5c9ZKugiThJF7VavVkjv/pl5r6vz7Zp3JzLiS1nI/3OfIWHzPLPzQwJouXlJr9lxlZs9oz8wWHE8kCdOfmbVevvKriZM2nEuhxerTZz7ftTvXL0o8QUK28Hii3IV9MJLCeZEZtI5LzSz+wtEj107K+gLk26bRh68kyXo74AAzCxG61n/ydS1ZLzHMzG5EupkVDkHMzF5ErJk1aNbJDk+qiKsXsxo07STrCxmYWfnJU/6jQ6f/7NSl2vQZ+3PMjHiuSzfyM6rpsm491/BL2HYh7W9aRPEimVmnNev+uW37F7v1oFWv9x9IMkf1pceOlzuyA0ZSOC8yg9ZxqZm5HJiZY4CZOYqINTNgADMzIDNjzXIkRlI4LzKD1oGZuRGYmWOAmTkKmJlTgJm5CiMpnBeZQevAzNwIzMwxwMwcBczMKcDMXIWRFM6LzKB1YGZuBGbmGGBmjgJm5hRgZq7CSArnRWbQOjAzNwIzcwwwM0cBM3MKrjKzmk3aFitdde62nUv3HpBr80Slun7+6qz9MZLCeZEZtA7MzI3AzBwDzMxRwMycgnvMLC71/Nglq+JSL3QYNBpmpudFZtA6MDM3AjNzDDAzRwEzcwruMbMxi1eqMplZjUYxJT6vPnrB8s2nsv+pWuX6URsST1J9vdZdub5Zl77Fy1SrWKcFte8ydGzJsjU+q1h335Wrzbv2j+49mOu5q7rRXeq36UaripWu9mWNRgvi9kxatZ4Wp6/fHJ9+Zc2RY19/0+TdUuXlkAofIymcF5lB68DM3AjMzDHAzBwFzMwpuNbMuFC+VrNNJ89U+741yVn9mO5UT+LF9aMXLqfCVzUb0893SpZjesZOzqlvpLoih6NC3/HTuebzqg0q14saOGVOnVZdfhg/ncyvSacfesVOIVdTAwgXRlI4LzKD1oGZuRGYmWOAmTkKmJlTcI+Z+f00kwxs6KyFbfuPIN+qG92F6lt0G8D1Ddv1pMafVqhNi8269NuWnEKFiSvXf9+u55Q1G7h+v8/MeJNJq9bvSDk/c+M22rZ2VOfqjdqQsakPPWs0ilmyZ78cVSFjJIXzIjNoHZiZG4GZOQaYmaOAmTkF95hZPoi/fKVRh96yPnIxksJ5kRm0DszMjcDMHAPMzFHAzJwCzCwQH3397bulyq8+fFSuilyMpHBeZAat89TNDHJmN/KhZRwwM7vBumzmyWJAzuxG3rWMA2ZmQ/KtZV6nm5kjMZLCeZEZtM7TNTMvHpvZDHZlM0mWA3JmK/KvZV6fmUHO7AOnI78BObMVoWiZN49mRiFFARQmfpNidzPz5jw5A3bAzE3eg5/TADtg5iYfwUIAwk7IwR+fATtg5iaPkVcz8+LJWfgwM5ETEWBmHNISQCFjpiS/IRUBFDJmSkIJaQmgkCmgkIoAChkzJfmKfJiZ16cCoPAx05ATz0SKmSEQCAQCgQge+TMzhK0CZoZAIBAIhEMCZuaACIOZZUHOEAgEAoEo6AikZVkws8gJzpTMoHVgZggEAoFA2CKCmFmWT87MDRD2i7CZWVaOnMHPEAgEAoEIMdQtVd5tdSBnNo/QtSwrFDPLgpwhEAgEAhFyWNSyLHymae8oEC3LKigzAwAAAECIyPushG//8DO7RUFpWVaIZqaQh1ek4CnSmJD1wAEgs04FmXUqrr0gy7tqrig/ixQos7LSScgc5ZuCMbPIhS8Esh44AGTWqSCzTgUXZAeDzFoHZoYLgWNBZp0KMutUcEF2MMisdWBmuBA4FmTWqSCzTgUXZAeDzFoHZoYLgWNBZp0KMutUcEF2MMisdWBmuBA4FmTWqSCzTgUXZAeDzFoHZoYLgWNBZp0KMutUcEF2MMisdWBmuBA4FmTWqSCzTgUXZAeDzFoHZoYLgWNBZp0KMutUcEF2MMisdWBmuBA4FmTWqSCzTgUXZAeDzFoHZoYLgWNBZp0KMutUcEF2MMisdWBmuBA4FmTWqSCzTgUXZAeDzFoHZoYLgWNBZp0KMutUcEF2MMisdWBmuBA4FmTWqSCzTgUXZAeDzFoHZoYLgWNBZp0KMutUcEF2MMisdWBmuBA4FmTWqSCzTgUXZAeDzFoHZoYLgWNBZp0KMutUcEF2MMisddxrZnwJUMgGIEJBZp2KkVkk10kgs04Fmc0HMDMcLk4DmXUqRmaRXCeBzDoVZDYfwMxwrDgQJNepILNOBZl1MEhuXnGvmWVph4tcBSIaXAgcDDLrVJBZp4ILcl6BmeFYcSDIrINBZp0KTlungszmFVebWRau8s4FmXUqyKyDQXKdCjKbJ2BmOFwcCzLrVJBZp4ILsoNBZq0TqpnxiQRsi0yZRWRXwG7IrFlEdgVshUyZRWRXwFbIlFlH9gZshUxZvsm/mfFQ0hD2jnwcMY8zW/Ufgc3Jd3L/679eBXYm35l9tfUKYGfynVnimabNgZ3JR3IDkU8z4xGYFoCwa+TpcMnOrJAAYE/ymlkpAcCe5Okqz42lBwB7Yj2znFwpAcCe5CmzQci/mZk3f4SNw/pVHloWcVjPLMwssrCYWU6uvP0D25KnC7K8/QM7YzGzwcmPmUHLIjGsHC58vZD3fmBnLF7loWWRiMXMyns/sDlWTltuI+/9wM5YyWyuwMzcElaOFZhZJGLxQgAzi0QsZlbe+IHNsXLawswiESuZzRWYmVvCyrECM4tELF4IYGaRiMXMyhs/sDlWTluYWSRiJbO5AjNzS1g5VmBmkYjFCwHMLBKxmFl54wc2x8ppCzOLRKxkNldgZm4JK8cKzCwSsXghgJlFIhYzK2/8wOZYOW1hZpGIlczmCszMLWHlWIGZRSIWLwQws0jEYmbljR/YHCunLcwsErGS2VyBmbklrBwrMLNIxOKFAGYWiVjMrLzxA5tj5bSFmUUiVjKbKzAzt4SVYwVmFolYvBDAzCIRi5mVN35gc6yctjCzSMRKZnMFZuaWsHKswMwiEYsXAphZJGIxs/LGD2yOldMWZhaJWMlsrsDM3BJWjhWYWSRi8UIAM4tELGZW3viBzbFy2sLMIhErmc0Vh5tZ5cr1fv/79155pXi5ct+Z6/IVzz77+oEDh83aSAgrx4o9zczriwfp5zK3z5NrH7d5+OBy49/Ker88vJKaMaKurFfQ7qz3FnYsXggi0cwuXLhIuWjatN0f/vDBkSPH1q/f8uKLbxltZs5cOGzYeC4/ePCQ2st+IheLmZU3frtxMSOTUrNw1zkqrz+Uxie1bOYerJy2kWJmnE0OuTYUHjzMPqNlvZ2xktlccbKZTZgw/Y9//GDevCUbN25t0KCVuTpfATMrfOjMJJHKGPrdo9sZ1/pXlA2y2+SYGTW+1q+CbKADM4sUlJkdOnSUClLLiM2bd7Ro0YnLMDPbwmaWdf9h0S5rHz58dPl6ljfHzFbsO3/petaWo5fK9ttEi+oen3r1ztGU63fuPlh3KO0v7VfTqk96baANb2be/3bEDlqkfrgld953cQJVLo9PVT3bGSunbQSZWY0pU2V96MDM8kBEmNmcOYvounby5ClVc/bs2b/+9VOP57W9e/e/+mrxbdt2UiW1IWkrW7YGFWhx2bLVtEgtN2/evnfvPipQ+4ULl1P7F154My3HzJKTk5999rVFi1b89rdFaFVS0km1F9uGlWPFzmZGhUuNf0PlK51LPjh/wvvo4eWo18nVLtb5r+w2gcysxj9Tzd2j2/QO/ZpZxuCa1JLLVEhv8zb9vDmjIy3K3dkKixeCyDWzzMysLVviXnrpL6r++effpPq4uL1UplWGmR09mkg//TaOOCxmVt747QbL04kLN6gQf/rq/2vvzKOqOrY0nu5eq1e/Ht573X9kvcbxdbT1JVFBTWKcJeqLRltN1EQ0cYqJRiXgPCFqRI04xjGiqFGJI46g4IggogiIgooCggJeRxxQCCj05laolLeAW2hIqrjft37rrrp1qvapU7vOqS/nmsUI/zPMP3msj4lLu0eF/XFZrIY+ey4IZ4UZO85vOH6VCj+EpXquj2EN2KGAiDTmzFgN2Tgqf+l3mj7PpmXLA9ANldvWRGf2h1Fjkm/fLiws/Ou0GVkPHrwxazZrEBgfT4V/GTXmWWFhh2XLs588oaM8Qi//tUVWB0YNqPD1jsCea/zfW7KMObP/HD/x2JUrrIH+qGTWLlXWma1cuc7Jara4AgK2U027dj2oPHr01FGjplqszuzYsQgvr9ms8ZYtO1u16urvvyk8PJJ14e1ZA+bMfvxxR6dOn9DXgQPdqX7FirXCeTSVylrR3JlZ+v2ZytnzetNnflIU1eRGbnuwqnjAZTqzPv9emF+8JYg1pToz1vLmgFdZkKc3kh8FeLF6+XRaofggMNeZkQYN8rA5lJdX/NLFqTRnRvLxWVRqY+NQzKy88esGc2Yztp+nzzEbYrkz891zgaWMqaHVdXWYeYQVRv8Quz4slQobw6/67i1+b8qiUeFo4k3RmS0LKbbjW0+m0yfFlAegGyq3rUHOjCmvoODD1WuoEJeRQfWLj4V9FxbGGjT1nUeFHn5rTqSmUuHHmGKfLQbJzc//t9Fju/utTrp5i1fyd2Y+IaE27bVFJbN2qbLOLCUltW7dZv7+AbymLGdGTmv6dF+nEhuXkHBh+/Y9ZLymTp1TjjPr0qUvj2yEVNaK5s7s4dpRz7JvlLwGi3iujeTMqEvB1bO3htQseppfVK4zo6PU0tL3T9TyzujGrCb3+KaCzCTqzr7anE4rFB8E5jozd/dJ9PnkSS7VsF8233ijdUFBAVU6leHMrlxJLbWxcShmVt74dYM5M/6VO7O3JoU8Kyz0XB/z8aKIHaeuNSzbmb09KeT63cdf+p3uNPtowdPCD+eHi86MCL94i77GpxvwwqxhlXNm/J1ZWc6supf3K1ZnFpaczDtSLzoUe/36P33tmf/0af2Zs8pyZtOC97OC/qhk1i5V1pmR/Pw2NGjQJjBwb3h45NChY9LS0t966+/818yIiCiL5Mz27g2Jioq+du3a8OHjFy5cSV34r5k1a/7ya2Z6enr16o3Itx07FkEtDxw4/PyZdZTKWtHZmYn/zoz9vHhzwKt3J7W8692+uI3gzB6uG0OFB98Py78SfeuLWkVWiQFlZ0YtH26YQAXuzG6PqF9cn3yGziKfTisUHwTmOjMyWNu27aFCt26f0X9Qxcaee/PN1iytTqU5sx079tFnnTrvyI2NQzGz8savG2U5M2JfbCYdPZeePXXLuYZlOzOqeX/W0dsP83JyCwatiGpY8u/MeEz2c6cRL8waVl1n9q+jx6bcucN/zXxz1hzWgDmzP1h/zST31niur1/kyUGbAuhQVFqaZ+BOKpAz479m9vZf137pz79mvgJnpoIpzozUq9fg+vWbv/56q+7d+9PX2Nj4/v1H1K3brHNnN9bA6XlnlpGR0bZt99q1mzZq1O769QyqofYNGrSl9kFBoRbh/wD4/HMPZ2fXjh17r1q1PjMzk59RW6msFW2dWVFh4dPb6blRgayGbFNuxObC3BxyVJZ+fy5uU+LMnlpSqHxvTo+bn/4XNSjua5UYkJwZr8+e/0nu8QDe8hdnNrzeT4lhVPgp/qB8Oq1QfBAY7cxq1HDeuTP40aOcHj0G5OQ85ulzKs2Z1arV5MSJ00ePniBzZtPYOBQzK2/8DkiTCQcKC4s6+hS7Ov1RuW1NdGZEbe/pW2PjHuTmhqek8AbMmREbo89k3L9PbmzgpoB/9hj1w+nTj6z/2KDI6syowfpTp6/dy14eHkE2Ds6sAhjkzCAulbWipzMD5aP4IDDRmQHFzMobv6OReP3+02eFf591VD6kJyq3rSnODIioZNYucGaOIpW1AmdmIooPAjgzE1HMrLzxA81RuW3hzExEJbN2gTNzFKmsFTgzE1F8EMCZmYhiZuWNH2iOym0LZ2YiKpm1C5yZo0hlrcCZmYjigwDOzEQUMytv/EBzVG5bODMTUcmsXeDMHEUqawXOzEQUHwRwZiaimFl54weao3LbwpmZiEpm7QJn5ihSWStwZiai+CCAMzMRxczKGz/QHJXbFs7MRFQyaxc4M0eRylqBMzMRxQcBnJmJKGZW3viB5qjctnBmJqKSWbvAmTmKVNZKFXBmdya2yNk9X64vi1tf1JIrzULxQQBnZiKKmZU3fv3pvShCrqworacdkiuNQOW2hTMzEZXM2sVxndn584m8/N57HwlHntOIERPCwk7Y1hoolbVSBZwZ+wOXFSJnl69caRCKDwKdndmePSEuLu/xr/HxiXKbSqJDh15ypT4oZlbe+DXnrUkh7A+Zfzi/+I+Xl8q+2Ey5UsbvcLJcqT8qt62JzmxLbKzTlKly/YvhPGeuXKk5Kpm1i4M6s/T0dPFrOc5s8+ZAL6/ZtrUGSmWtVAFnlhu5nT7vTGieF3fg2aO7D1a758UeyE86aXH7jyeH/Qsyk+56tbO4/bHw8QP6yrrknQmS4xiE4oNAZ2cWHR0nfq2oM3N1/XDHjn1yvQqLF/vJlfqgmFl549ecj+aHHzibRYW4q/eKioo81sXcf5yflf2Earp8G/assJD95SVSN98watlrYURM6r2HT/KpgfP4/Y9yC7ZFFf+RTeJo4k05vv6o3LYmOjP2B8vtsjH6jFwp4xMSKldqjkpm7eKgziwi4iQr9O07LCUl1cXFNTBwb3JySkxMHFWGh0d+9tnwtWsDvL2/jYw85eY2VOxrqFTWShVwZuydGTmz3JM7qJAbFZgbsZkKjwK8Hqwcain+802pVBa75OyaJ8cxCMUHgc7ObPfuA/Q5eLBHcPDhQYM8srIshw4dr1eveULCJarv0WNA+/a9QkKOfvBB3w0btl2/nvXOO+9fvHiZDvn6Lqte3Zk7sw4delFfKtB9Td3ffbczi//VV+NXrfqBjqanZ3Tp0i8n53GnTn1SUtLo0IEDR+Tx6INiZuWNX3Ns3pkt2HeR3FhhYdG7U0JdZxyOTrm7NOQye2fGnRnvuyjokhhq9RG8M9OIzTGxrBB68dKrkya3XLh46fFw+no2I8NjR+DUoGB2lDmzfQmJfxo3vv3SZa9YX4/VmOrdbP7Cpr7z/nuyF2u269w5+RSao5JZuzioM+PvzNas2UifLVp0+fbbJdWrN6pWrVFKylWq6dixd8+eg6OjYzdvDpwyZZbY11CprJUq4MzIit0aVoec2dO7Gbfd33h68+qTsI1Unz3/k7yY4Hs+XQvSzmUv6HNz4F/YH0e3WP9pmhzHIBQfBDo7M/bOzMdnkbv7JCpcvpzi6TmVCmlp1+izZs3G3t5z+/T5ctasRUOHjt22bS9VJiYWm7Zdu/ZHRka7un7EnRkrfPPNgmfPivd6urUpeFFRETkwOsr6MlfHInz33WqbwWiFYmbljV9/QuJv0GeXOcecx+0fvia6lfdBfqjpxAMxqffCL96iQ7Iz81wfQwZu5Noz7Ouv8u/VfntUblsTnRl/ZzZoUwB9tli4iDmzc5lZf5ns9WNMjFdQ8D+4ezBnNtDahlHqD5ezQg/KlZqjklm7OKgzIyUkXKDPfv2+Iivm4uK6ffuepKQr/Oi8ecu6dOlLhZEjJx47FsHrzZXKWqkCzuzupJY5u+eX/Jp578Fqd+bMLG5/fHJkXUHW5bve7Ut+zVxL9beG1JSDmIXig0BnZ7Z3b4izs+vgwR5BQYf69x+ZlWUJDT1Wr15zZp6IU6diX3vt7bNnExo1ard1626nEl9F1K7ddODArw8fDq9e3Zm8Fzvar9/w119vRYVx42asWRNAhu/QoeP8KOvLPum/weTx6INiZuWNX38+tjoq5/H7yUJ7rIvJzvmJDDTVrDqUnFfw7HCCJTrlLh2SnRl1yckt2G79NbO14OfMQuW2NdGZbY2NY2+82Duz//1mJnm1Lt+vup6dzRocT05pPNc3OPHCP7p77DmfIL4zk6O5fOsrV2qOSmbt4rjOzNGkslaqgDNjkDP72ZA5AIoPAp2dGSgLxczKG3/VhhzbhYwHcr1BqNy2JjozoJJZu8CZOYpU1kqVcWYOheKDAM7MRBQzK2/8QHNUbls4MxNRyaxd4MwcRSprBc7MRBQfBHBmJqKYWXnjB5qjctvCmZmISmbtAmfmKFJZK3BmJqL4IIAzMxHFzMobP9AcldsWzsxEVDJrFzgzR5HKWoEzMxHFBwGcmYkoZlbe+IHmqNy2cGYmopJZu8CZOYpU1gqcmYkoPgjgzExEMbPyxg80R+W2hTMzEZXM2gXOzFGkslbgzExE8UEAZ2YiipmVN36gOSq3LZyZiahk1i5wZo4ilbUCZ2Yiig8CODMTUcysvPEDzVG5beHMTEQls3aBM3MUqawVODMTUXwQwJmZiGJm5Y0faI7KbQtnZiIqmbULnJmjSGWtwJmZiOKDAM7MRBQzK2/8QHNUbls4MxNRyaxdXsSZ5cGcmSb1tQJnZhzqmYU5MwvFzLLkyns/0JYKPZDlvR/ojGJmywfOzCFUoQeBvPcDnVHPLJyZWShmliVX3v6BtlTogSzv/UBnFDNbPi/ozPL4L1+Q3lJ/BNhmVnIAQDdeOLmyCQBa8cKZlU0A0IoXzmw1WDTteYHklsWLO7M8YcUAzZFzVz5yBKAncu7KR44A9ETOnV3kIEBP5NyVjxwB6ImcuxfjpZxZHlaM9sgpU0QOBXRDzpoiciigFXLKFJFDAa2QU6aOHA1ohZyyF+ZlnRkAAAAAAPi1gDMDAAAAANAFODMAAAAAAF2AMwMAAAAA0AU4MwAAAAAAXYAzAwAAAADQBTgzAAAAAABdgDMDAAAAANAFODMAAAAAAF2AMwMAAAAA0AU4MwBApbN80+E2bt8kXL7Rb9SKas2He8zcSJWN/2/y5qDTVPD02cj/tsmDnHwqnzybyr5SG/r6OPfZ/DX73+3p/fBxAathR6nwlfe6UjsyOg6YU6PliOyHP0WfT4+/lMkD0nlZYV1gBItTv8MYPiTLncdU0+frpTxI+JlkCjJi2noWBAAAKg84MwBA5UJG57V2HqEnLlA5Pet+zZYjmbVSd2YsCBVOn0urkDOjmr+2+VqssXFmb/WY8ujxU9GZrdpyjKzYx+5LKCDV3Lj9iI7eyc4VgwAAQOUBZwYAqFx+2BnJvRTRfeiCijqzF35nNndVULWSvzd8LqmUd2Zv9/By6TpJdGascalBmnafwoIAAEDlAWcGAKhc9h2NJ1vDXkERbdy+YdanSTdVZ0Y06Dz+YspN1os3psKIaetL7ciJTbze/tNZdGio11oekDsz5hqrCc6sRe9p9PVoVJIYZOay3WIQAACoPODMAACVS1m/ZnYZMm/VlmNUGDTBr3xnJkajXqIz81m+p9SONkxdtOPT0St4QO7MHuc+Y1aMO7Mf950ip1jH1fN49BWbINSMBQEAgMoDzgwA8FvQ9Yv5dV09Xfv5rAg48iSvkGros63bTKrs9uWC0IhE1syuM6NeFIF6vfH+WN5L7shw81z2dg+v/2nrQfaLndTGmbGAojNjr/GGeq1l0e4/yqcgZNQoyLzVwSwIAABUHnBmAAAAAAC6AGcGAAAAAKALcGYAAAAAALpQYWc2fNQ0AAAAAACggmylyqfCzswCQRAEQRAEqami5qwCzoxC254NgiAIgiAIsifZVpVFBZyZ7UkgCIIgCIIgBam/OYMzgyAIgiAIqlzBmUEQBEEQBOkiODMIgiAIgiBdBGcGQRAEQRCki+DMIAiCIAiCdBGcGQRBEARBkC6CM4OqrK5cSbatKkPUsnnzzra1v54Ug7dt2922SlJi4gXbKknlXE45h34zqefFona9XBVqXEmaO3fJggXLbWvLFrW3rSpN4qVVaAIhG23atK1+/eY2leym+N1vDQhigjODjFRmZmbt2k1sa58X28AuXUqyqaeNc/z4GWLN7+VXMjIyJk6cmZBwwc9vw+rVG34tZyaLJqFVq662tfakMsmVrbKuV06rpezGljJmoNTKl5TozFTiV5Izs3veSlWp2dFEjRq1s60q0e/yEIAgWXBmkJESTYOTU0OiYcO2VI6KimaVtDuyDax79/501M1t6M89BWfm47Pgb39r4enpxZzZ4sXfN27cfuBA92vXrtFGSHvb0KFj4+MTWPClS1ezyrp1m3Xt2o+6U/tq1Ro1adKBlXlfdhZf36X0Scbru+/82BNfHCfTzp1BvGyx7qbDho2l4CkpqSxg3brvsID0lU5EsB06NPRIZOQpKg8ZMorGk5h40SJdjjhaPgnyIUvxIL9p06b78OHj2TCOHDnOCjbObPp0X1agK6JPPjyKRhNVp847dLGswfLl/qxAh2hOqNnOnftcXN7bunWXpcRY8Nljg6HuNNUNGrShS8jKusG6swjiNfIJ5FfEZ4Y1pgmkxjSBvHutWo2ppbgMeELFSnG2mTp1+oT1FbvQJPDMWqxXQb3oGqk8efKsevWa0zRyZybGly+N2rNpp0XLEjF79iKLdcxsPsUFI84Dd2Y2Y6Y2NGbqQqNifS3CqhDnWYxMomHTSNiw5XkoRywOTQuV2SVYrPcXv3A6O104nZ1fuDgMcfb4ehC7iLNNq04cG7s9qX7OnMX0ddy46Sy+xXrJPIJ4T7GjfGbEwYvvzHgu6ELYWWi08g0OQZUnODPISImm4eOPh9Dzmh6yZCmios6wSu7M5P98Z86MHvTkSCzFPmMV8yvsSU3Qo5z2j5Yti986XL6cTPFZPVW2bt2NKulpvmSJH3/xRl/Fvqyyb99he/bsd3efZCl54ovjZG1snBkPTluLTUB+LhoDbai0q7Eyq/zgAzf5csTR8pc38iHqOGXKLCrPmDGPReOS35nRFa1dG2ARLpnNFW+wYcOWhQtX8q/80OrVG+jTxcXVYh2DOHt8qpnhs1i3YS+vORQ8NjZevEbKBZ9Anlbx9SdvTBPICrQfd+7s9vnnHnwGxITySvFySoJZRoyYwPqKXSzWzNIkUGbFvPNpJDMhvzMTL40VxPa0aJkb8PFZaBGuQlww4jywhS2PmS6WxkwDpoD8vHxV8Hm2iczHRsOWY7JEiFANO2QTR3RmPDv87HThrDsfhjh74noQu1iE+8hmbPxaRo+eSktu5syfM24TQbyn2FEybZaSZcAHLzszygVdCD8LH6q4QiCokgRnBhkp0TT06jX44sWkmJizBw8epQfuuXMJ588ncmd29Wpaenq62Jc5s+Dgg/TYvXDhEj2ImV+hbTguLp61of2D/bZIezDFp+DM0LBKetCHhh5p1qzTjRvFbwKoLPZl2rUruH//EeHhkZaSJ744Ttam1F8zKThtMywgi0+ic0VGnrJYB3b4cFj79j1ZmTattLR02rfkyxFHS5PAXZHNoX37QqhMY2AxRcnOjK6InIHFesl8eKIzo2G3afPLb7L8kL//Jvp0dv55DOLs8cHQJVBMugRm43gEfo2UCz6BPK18ZlhjVhD36aysG4sWreQzICaUV4qXI4r1FbtYrJmlSaDMsryzXkFBoXQV5JhdXT/kzozHly+NtaeFSu1p0ZLbpnLHjr0swlWIC0acB7awyxozDXjAgJF0XpofcVXwebY8H5kWAA2bFgANu6yYZYnFoWmhOHQJ/Nbj2aGzU0A6O79wPgxx9sT1YNOF30c2Y+PXQvadllxS0hX21SaCeE+xo8yZsZzywYvOjF0I5YIuhJ9FvsEhqPIEZwZBpkq0RC+pM2di2VuWlxTZu5iYONtaSHvRAggLO2Fba4JSUlKx5KAqJjgzCDJVv5Yz69ixd4MGbdhPaS+jI0eO2/yvFZARcnJqyN4kGSdacjVquNjWQpDhgjODIAiCIAjSRXBmEARBEARBugjODIIgCIIgSBfBmUEQBEEQBOkiODMIgiAIgiBdVCnOjILangeCIAiCIAiyJ9lWlUUFnBnD9lQQBEEQBEFQGVJ/W8aosDOjEwAAAAAAABVkK1U+FXZmAAAAAACgkoAzAwAAAADQBTgzAAAAAABdgDMDAAAAANAFODMAAAAAAF2AMwMAAAAA0IX/B8dOzkGxYD7ZAAAAAElFTkSuQmCC>