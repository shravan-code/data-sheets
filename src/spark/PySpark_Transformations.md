

| ⚡ PySpark DataFrame API Every Transformation You Need 47 transformations · 6 categories · Real code with table outputs · 100-row DataFrame |
| :---: |

| 🟢  NARROW Transformation Data stays in the same partition. No data moves between machines. Fast & cheap. Examples: .select(), .filter(), .withColumn(), .cast() | 🔴  WIDE (Shuffle) Transformation Data moves between partitions/machines over the network. Slower but necessary. Examples: .groupBy(), .join(), .distinct(), .orderBy() |
| :---- | :---- |

**📊  Our Sample DataFrame (100 rows)**

All examples below operate on this employee DataFrame. Showing first 5 of 100 rows:

| from pyspark.sql import SparkSession, functions as F from pyspark.sql.functions import col, broadcast from pyspark.sql.window import Window spark \= SparkSession.builder.getOrCreate() \# 100 employee records: name, dept, salary, age, city, join\_year, rating, skills data \= \[("Alice","Engineering",87600,28,"New York",2019,3.5,\["Python","Spark"\]),         ("Bob","Marketing",50000,35,"San Francisco",2016,4.0,\["Excel","SQL"\]),         ... \# 100 rows total cols \= \["name","dept","salary","age","city","join\_year","rating","skills"\] df \= spark.createDataFrame(data, cols) |
| :---- |

**Sample data preview:**

| name | dept | salary | age | city | join\_year | rating |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Alice | Engineering | 50000 | 22 | New York | 2015 | 3.5 |
| Bob | Marketing | 50487 | 35 | San Francisco | 2016 | 4 |
| Carol | HR | 50974 | 48 | Chicago | 2017 | 5.5 |
| Dave | Finance | 51461 | 33 | Austin | 2018 | 3 |
| Eve | Sales | 51948 | 46 | Seattle | 2019 | 4.5 |
| ... | ... | ... | ... | ... | ... | ... |
| *100 rows total* | *100 rows total* | *100 rows total* | *100 rows total* | *100 rows total* | *100 rows total* | *100 rows total* |

| 🔲  SELECTION & COLUMNS |
| :---- |

| .select() | 📌 What: Pick only specific columns. Like choosing which columns to display. 💡 Why: Drop unneeded columns early — less data to carry through the pipeline. Code: df.select("name", "dept", "salary").show(5) Output (sample rows): name dept salary Alice Engineering 50000 Bob Marketing 50487 Carol HR 50974 Dave Finance 51461 Eve Sales 51948  |
| :---- | :---- |

| .selectExpr() | 📌 What: Select columns using SQL-style string expressions. Supports math & aliases inline. 💡 Why: Quick computations without importing functions. Readable for SQL users. Code: df.selectExpr("name", "salary", "salary \* 1.1 as new\_salary").show(5) Output (sample rows): name salary new\_salary Alice 50000 55000.0 Bob 50487 55535.7 Carol 50974 56071.4 Dave 51461 56607.1 Eve 51948 57142.8  |
| :---- | :---- |

| .withColumn() | 📌 What: Add a new column OR overwrite an existing one. All other columns are kept. 💡 Why: Feature engineering: compute tax, flags, categories — most common transformation. Code: df.withColumn("tax", col("salary") \* 0.30).select("name","salary","tax").show(5) Output (sample rows): name salary tax Alice 50000 15000.0 Bob 50487 15146.1 Carol 50974 15292.2 Dave 51461 15438.3 Eve 51948 15584.4  |
| :---- | :---- |

| .withColumnRenamed() | 📌 What: Rename an existing column to a new name. Content stays the same. 💡 Why: Raw data often has cryptic column names. Rename for readability. Code: df.withColumnRenamed("dept", "department")   .select("name","department","salary").show(5) Output (sample rows): name department salary Alice Engineering 50000 Bob Marketing 50487 Carol HR 50974 Dave Finance 51461 Eve Sales 51948  |
| :---- | :---- |

| .drop() | 📌 What: Remove one or more columns from the DataFrame. 💡 Why: After temporary columns are used, drop them to keep the output schema clean. Code: df.drop("skills", "rating").show(5) Output (sample rows): name dept salary age city join\_year Alice Engineering 50000 22 New York 2015 Bob Marketing 50487 35 San Francisco 2016 Carol HR 50974 48 Chicago 2017 Dave Finance 51461 33 Austin 2018 Eve Sales 51948 46 Seattle 2019  |
| :---- | :---- |

| .alias() | 📌 What: Rename a column expression result — used inside .select() or .agg(). 💡 Why: Computed columns get ugly auto-names like 'sum(salary)'. alias() gives clean names. Code: df.select(   col("name"),   (col("salary") / 12).alias("monthly\_pay") ).show(5) Output (sample rows): name monthly\_pay Alice 4166.67 Bob 4207.25 Carol 4247.83 Dave 4288.42 Eve 4329.00  |
| :---- | :---- |

| .cast() | 📌 What: Change a column's data type — e.g., string → integer, integer → double. 💡 Why: CSV files load everything as strings. Cast to numbers before doing math. Code: df.withColumn("salary\_dbl", col("salary").cast("double"))   .select("name","salary","salary\_dbl").show(5) Output (sample rows): name salary (int) salary\_dbl (double) Alice 50000 50000.0 Bob 50487 50487.0 Carol 50974 50974.0 Dave 51461 51461.0 Eve 51948 51948.0  |
| :---- | :---- |

| .columns | 📌 What: A property (not a function) that returns the list of all column names. 💡 Why: Inspect schema quickly, or loop over columns programmatically. Code: print(df.columns) \# → \["name","dept","salary","age","city","join\_year","rating","skills"\] Output (sample rows): index column\_name 0 name 1 dept 2 salary 3 age 4 city  |
| :---- | :---- |

| 🔍  FILTERING & SORTING |
| :---- |

| .filter() | 📌 What: Keep only the rows where the condition is True. Drops all other rows. 💡 Why: The SQL WHERE clause equivalent. Most fundamental row-level operation. Code: df.filter(col("salary") \> 90000\)   .select("name","dept","salary").show(5) Output (sample rows): name dept salary Hana Finance 90421 Ike Sales 90908 Jen Engineering 91395 Kirk Marketing 91882 Lana HR 92369  |
| :---- | :---- |

| .where() | 📌 What: Exact alias for .filter(). Accepts both Column expressions and SQL strings. 💡 Why: Prefer this when writing SQL-like string conditions — more readable. Code: df.where("dept \= 'Engineering' AND age \< 30")   .select("name","dept","age").show(5) Output (sample rows): name dept age Alice Engineering 22 Julia Engineering 29 Zara Engineering 28 Omar Engineering 27 Evan Engineering 26  |
| :---- | :---- |

| .distinct()  WIDE  | 📌 What: Remove completely duplicate rows, keeping only unique rows. 💡 Why: Clean up accidental duplicates from data ingestion or faulty joins. Code: df.select("dept").distinct().show() Output (sample rows): dept Engineering Marketing HR Finance Sales  |
| :---- | :---- |

| .dropDuplicates()  WIDE  | 📌 What: Remove duplicates based on specific columns. Keeps first occurrence. 💡 Why: More precise than .distinct(). Keep one record per department/email/ID. Code: df.dropDuplicates(\["dept"\])   .select("dept","name","salary").show(5) Output (sample rows): dept name salary Engineering Alice 50000 Marketing Bob 50487 HR Carol 50974 Finance Dave 51461 Sales Eve 51948  |
| :---- | :---- |

| .orderBy()  WIDE  | 📌 What: Sort the full DataFrame by one or more columns globally. Use .desc() for descending. 💡 Why: Get top/bottom N records. Produce ranked output for reports. Code: df.orderBy(col("salary").desc())   .select("name","dept","salary").show(5) Output (sample rows): name dept salary Xio Sales 98213 Warren Finance 97726 Val HR 97239 Uri Marketing 96752 Thea Engineering 96265  |
| :---- | :---- |

| .sortWithinPartitions() | 📌 What: Sort rows within each partition independently — no cross-partition shuffle. 💡 Why: Much faster than .orderBy() when you only need local order, not a global sort. Code: df.sortWithinPartitions("dept", "salary")   .select("name","dept","salary").show(5) Output (sample rows): name dept salary Alice Engineering 50000 Frank Engineering 52435 Karen Engineering 54870 Paul Engineering 57305 Uma Engineering 59740  |
| :---- | :---- |

| .limit() | 📌 What: Return only the first N rows of the DataFrame. 💡 Why: Sample large datasets without reading everything. Quick checks during development. Code: df.limit(5).select("name","dept","salary").show() Output (sample rows): name dept salary Alice Engineering 50000 Bob Marketing 50487 Carol HR 50974 Dave Finance 51461 Eve Sales 51948  |
| :---- | :---- |

| .sample() | 📌 What: Randomly sample a fraction of rows (e.g., 0.05 \= \~5 rows from 100). 💡 Why: Test your pipeline on a small subset before running on billions of rows. Code: df.sample(fraction=0.05, seed=42)   .select("name","dept","salary").show() Output (sample rows): name dept salary Alice Engineering 87600 Frank Finance 66730 Grace Sales 73217 Mark Finance 82390 Pam Engineering 91045  |
| :---- | :---- |

| 📊  AGGREGATION |
| :---- |

| .groupBy().agg()  WIDE  | 📌 What: Group rows by column(s), then apply one or more aggregate functions to each group. 💡 Why: Core of analytics — totals, averages, counts per department/region/date. Code: df.groupBy("dept").agg(    F.count("\*").alias("headcount"),    F.avg("salary").alias("avg\_salary") ).show() Output (sample rows): dept headcount avg\_salary Engineering 20 87400.0 Marketing 20 68900.0 HR 20 61200.0 Finance 20 74800.0 Sales 20 72100.0  |
| :---- | :---- |

| F.count() | 📌 What: Count rows per group. F.count('\*') counts all rows, F.count('col') excludes nulls. 💡 Why: Most basic aggregation — how many records exist per category? Code: df.groupBy("dept")   .agg(F.count("\*").alias("total\_employees")).show() Output (sample rows): dept total\_employees Engineering 20 Marketing 20 HR 20 Finance 20 Sales 20  |
| :---- | :---- |

| F.sum() / F.avg() | 📌 What: F.sum() adds all values in a group. F.avg() computes the mean. 💡 Why: Total revenue per region, average salary per department — classic reporting. Code: df.groupBy("dept").agg(   F.sum("salary").alias("total\_sal"),   F.avg("salary").alias("avg\_sal") ).show() Output (sample rows): dept total\_sal avg\_sal Engineering 1748000 87400.0 Marketing 1378000 68900.0 HR 1224000 61200.0 Finance 1496000 74800.0 Sales 1442000 72100.0  |
| :---- | :---- |

| F.min() / F.max() | 📌 What: Find the minimum or maximum value in a column within each group. 💡 Why: Highest salary per dept, earliest join year per city — min/max analysis. Code: df.groupBy("dept").agg(   F.min("salary").alias("min\_sal"),   F.max("salary").alias("max\_sal") ).show() Output (sample rows): dept min\_sal max\_sal Engineering 51974 109000 Marketing 50000 98760 HR 50487 87930 Finance 52461 103200 Sales 51948 98760  |
| :---- | :---- |

| F.collect\_list() | 📌 What: Gather all values in a column into one array, including duplicates. 💡 Why: List all employee names per department. Aggregate tags/items per user into one row. Code: df.groupBy("dept")   .agg(F.collect\_list("name").alias("members")).show() Output (sample rows): dept members (first 3 shown) Engineering \[Alice, Frank, Karen, ...\] Marketing \[Bob, Glen, Laura, ...\] HR \[Carol, Holly, Matt, ...\] Finance \[Dave, Ian, Nina, ...\] Sales \[Eve, Jade, Oscar, ...\]  |
| :---- | :---- |

| F.collect\_set() | 📌 What: Like collect\_list() but keeps only unique values — removes duplicates. 💡 Why: Get distinct categories, unique tags per user. No duplicate noise. Code: df.groupBy("dept")   .agg(F.collect\_set("city").alias("unique\_cities")).show() Output (sample rows): dept unique\_cities Engineering {New York, Boston, Denver} Marketing {San Francisco, Austin} HR {Chicago, Miami, Seattle} Finance {Austin, New York} Sales {Denver, Boston}  |
| :---- | :---- |

| F.countDistinct() | 📌 What: Count only the unique (non-duplicate) values in a column per group. 💡 Why: How many unique cities does each dept have employees in? Avoid double-counting. Code: df.groupBy("dept").agg(   F.countDistinct("city").alias("unique\_cities") ).show() Output (sample rows): dept unique\_cities Engineering 5 Marketing 4 HR 6 Finance 4 Sales 5  |
| :---- | :---- |

| .pivot()  WIDE  | 📌 What: Rotate unique row values of a column into separate column headers (long → wide). 💡 Why: Create cross-tab reports — dept vs city headcount in a spreadsheet-style table. Code: df.groupBy("dept")   .pivot("city", \["New York","Chicago","Austin"\])   .count().show() Output (sample rows): dept New York Chicago Austin Engineering 4 3 3 Marketing 3 4 4 HR 4 3 3 Finance 3 3 4 Sales 3 4 4  |
| :---- | :---- |

| 🔗  JOINS |
| :---- |

| "inner" join  WIDE  | 📌 What: Return only rows that have matching keys in BOTH DataFrames. No match \= dropped. 💡 Why: Most common join. Get orders that have a matching customer record. Code: \# dept\_info: {"Engineering":{"budget":500000}, ...} employees.join(dept\_budget, "dept", "inner")          .select("name","dept","salary","budget").show(5) Output (sample rows): name dept salary budget Alice Engineering 87600 500000 Bob Marketing 50000 300000 Carol HR 56970 200000 Dave Finance 52461 400000 Eve Sales 51948 250000  |
| :---- | :---- |

| "left" join  WIDE  | 📌 What: All rows from LEFT DataFrame \+ matching from right. Non-matching right \= null. 💡 Why: Keep all your employees, enrich with bonus data when it exists. Code: employees.join(bonuses, "emp\_id", "left")          .select("name","salary","bonus").show(5) Output (sample rows): name salary bonus Alice 87600 8760 Bob 50000 null Carol 56970 5697 Dave 52461 null Eve 51948 5195  |
| :---- | :---- |

| "right" join  WIDE  | 📌 What: All rows from RIGHT DataFrame \+ matching from left. Non-matching left \= null. 💡 Why: Keep all budget entries; attach employee details where available. Code: employees.join(dept\_budget, "dept", "right")          .select("name","dept","budget").show(5) Output (sample rows): name dept budget Alice Engineering 500000 Frank Engineering 500000 null Legal 150000 Bob Marketing 300000 null Admin 100000  |
| :---- | :---- |

| "outer" join  WIDE  | 📌 What: ALL rows from both DataFrames. Non-matching sides filled with null. 💡 Why: Full picture — see every record from both sides including non-matches. Code: employees.join(dept\_budget, "dept", "outer")          .select("name","dept","budget").show(5) Output (sample rows): name dept budget Alice Engineering 500000 null Legal 150000 Bob Marketing 300000 null Admin 100000 Carol HR 200000  |
| :---- | :---- |

| "semi" join  WIDE  | 📌 What: Returns left rows WHERE a match exists in right. Does NOT add right columns. 💡 Why: Filter employees to only those who exist in the 'active\_list' table. Memory-efficient. Code: employees.join(active\_list, "emp\_id", "semi")          .select("name","dept","salary").show(5) Output (sample rows): name dept salary Alice Engineering 87600 Carol HR 56970 Eve Sales 51948 Henry Marketing 73217 Karen Finance 82390  |
| :---- | :---- |

| "anti" join  WIDE  | 📌 What: Returns left rows WHERE NO match exists in right. The opposite of semi. 💡 Why: Find employees NOT in the 'resigned' list. Identify gaps — customers with no orders. Code: employees.join(resigned\_list, "emp\_id", "anti")          .select("name","dept","salary").show(5) Output (sample rows): name dept salary Bob Marketing 50000 Dave Finance 52461 Frank Engineering 66730 Grace Sales 73217 Ian HR 58923  |
| :---- | :---- |

| .crossJoin()  WIDE  | 📌 What: Cartesian product: every row in A paired with every row in B. 100 × 5 \= 500 rows\! 💡 Why: Generate all combinations — all employee × shift pairings, all product × region pairs. Code: employees.limit(3).crossJoin(dept\_budget)          .select("name","dept","budget").show(5) Output (sample rows): name emp\_dept budget\_dept budget Alice Engineering Engineering 500000 Alice Engineering Marketing 300000 Alice Engineering HR 200000 Bob Marketing Engineering 500000 Bob Marketing Marketing 300000  |
| :---- | :---- |

| broadcast()  NO SHUFFLE  | 📌 What: Copy a small table to ALL executor nodes so the big table never moves. No shuffle\! 💡 Why: When one table is small (\<200MB), broadcast avoids expensive network shuffle. Huge speedup. Code: from pyspark.sql.functions import broadcast employees.join(broadcast(dept\_budget), "dept")          .select("name","dept","salary","budget").show(5) Output (sample rows): name dept salary budget Alice Engineering 87600 500000 Bob Marketing 50000 300000 Carol HR 56970 200000 Dave Finance 52461 400000 Eve Sales 51948 250000  |
| :---- | :---- |

| 🔀  RESHAPING & STRING OPS |
| :---- |

| F.explode() | 📌 What: Takes an array column and creates one row per element. Array of 2 \= 2 rows. 💡 Why: If each employee has skills=\['Python','Spark'\], explode to analyze each skill separately. Code: df.select("name", F.explode("skills").alias("skill"))   .show(8) Output (sample rows): name skill Alice Python Alice Spark Bob Excel Bob SQL Carol Python Carol Java Dave Excel Eve Spark  |
| :---- | :---- |

| F.split() | 📌 What: Split a string column into an array using a delimiter character. 💡 Why: Parse 'New York' → \['New','York'\], or split comma-separated values into arrays. Code: df.withColumn("city\_parts", F.split(col("city"), " "))   .select("city","city\_parts").show(5) Output (sample rows): city city\_parts New York \[New, York\] San Francisco \[San, Francisco\] Chicago \[Chicago\] Austin \[Austin\] Seattle \[Seattle\]  |
| :---- | :---- |

| F.array() | 📌 What: Combine multiple columns into a single array column. 💡 Why: Bundle related fields together — useful for ML feature vectors or grouped metadata. Code: df.withColumn("profile",    F.array("name","dept","city"))   .select("name","profile").show(5) Output (sample rows): name profile Alice \[Alice, Engineering, New York\] Bob \[Bob, Marketing, San Francisco\] Carol \[Carol, HR, Chicago\] Dave \[Dave, Finance, Austin\] Eve \[Eve, Sales, Seattle\]  |
| :---- | :---- |

| F.struct() | 📌 What: Combine multiple columns into a single nested struct (object) column. 💡 Why: Package related data together for nested schemas, JSON output, or complex joins. Code: df.withColumn("employee\_info",    F.struct("name","age","salary"))   .select("employee\_info").show(5) Output (sample rows): employee\_info {Alice, 22, 50000} {Bob, 35, 50487} {Carol, 48, 50974} {Dave, 33, 51461} {Eve, 46, 51948}  |
| :---- | :---- |

| .union() | 📌 What: Stack two DataFrames vertically (append rows). Both must have matching columns. 💡 Why: Combine Jan \+ Feb data. Merge staging table with production. Append new records. Code: \# df\_engineering \= df.filter(col("dept")=="Engineering") \# df\_finance     \= df.filter(col("dept")=="Finance") df\_engineering.union(df\_finance)               .select("name","dept","salary").show(5) Output (sample rows): name dept salary Alice Engineering 87600 Frank Engineering 66730 Karen Engineering 82390 Dave Finance 52461 Nina Finance 91203  |
| :---- | :---- |

| F.when().otherwise() | 📌 What: Conditional logic — exactly like SQL CASE WHEN. If condition → value, else → other. 💡 Why: Categorize salaries, flag active users, create derived labels based on conditions. Code: df.withColumn("salary\_band",   F.when(col("salary") \> 90000, "High")    .when(col("salary") \> 70000, "Medium")    .otherwise("Low") ).select("name","salary","salary\_band").show(5) Output (sample rows): name salary salary\_band Alice 50000 Low Bob 50487 Low Carol 50974 Low Dave 51461 Low Eve 51948 Low  |
| :---- | :---- |

| F.concat\_ws() | 📌 What: Join multiple string columns into one, with a separator between them. 💡 Why: Build labels, keys, or IDs from multiple columns — 'Engineering\_New York\_2019'. Code: df.withColumn("key",    F.concat\_ws("\_", "dept", "city", "join\_year"))   .select("name","key").show(5) Output (sample rows): name key Alice Engineering\_New York\_2015 Bob Marketing\_San Francisco\_2016 Carol HR\_Chicago\_2017 Dave Finance\_Austin\_2018 Eve Sales\_Seattle\_2019  |
| :---- | :---- |

| F.regexp\_replace() | 📌 What: Find and replace text in a string column using Regular Expressions. 💡 Why: Mask sensitive data, remove special characters, clean messy text fields. Code: df.withColumn("city\_clean",   F.regexp\_replace("city", " ", "\_"))   .select("city","city\_clean").show(5) Output (sample rows): city city\_clean New York New\_York San Francisco San\_Francisco Chicago Chicago Austin Austin Seattle Seattle  |
| :---- | :---- |

| 🪟  WINDOW & PARTITIONING |
| :---- |

| F.row\_number() | 📌 What: Assign a unique sequential rank (1,2,3...) to each row within its partition. 💡 Why: Get the \#1 earner per dept. Deduplicate by keeping only the latest record per ID. Code: w \= Window.partitionBy("dept").orderBy(F.desc("salary")) df.withColumn("rank", F.row\_number().over(w))   .filter(col("rank") \<= 2\)   .select("dept","name","salary","rank").show(6) Output (sample rows): dept name salary rank Engineering Noah 109000 1 Engineering Irene 103200 2 Finance Dave 103200 1 Finance Nina 91203 2 HR Yusuf 98760 1 HR Holly 87930 2  |
| :---- | :---- |

| F.rank() / F.dense\_rank() | 📌 What: rank() assigns same rank to ties but skips numbers. dense\_rank() never skips. 💡 Why: Leaderboards and competition results. Use dense\_rank when gaps look wrong. Code: w \= Window.partitionBy("dept").orderBy(F.desc("salary")) df.withColumn("rnk", F.rank().over(w))   .withColumn("dense\_rnk", F.dense\_rank().over(w))   .select("dept","name","salary","rnk","dense\_rnk").show(5) Output (sample rows): dept name salary rnk dense\_rnk Engineering Noah 109000 1 1 Engineering Irene 103200 2 2 Engineering Alice 87600 3 3 Finance Dave 103200 1 1 HR Yusuf 98760 1 1  |
| :---- | :---- |

| F.lag() / F.lead() | 📌 What: F.lag() accesses the PREVIOUS row's value. F.lead() accesses the NEXT row's value. 💡 Why: Day-over-day salary change, compare each record to the prior one in sequence. Code: w \= Window.partitionBy("dept").orderBy("join\_year") df.withColumn("prev\_salary", F.lag("salary", 1).over(w))   .select("dept","name","join\_year","salary","prev\_salary").show(5) Output (sample rows): dept name join\_year salary prev\_salary Engineering Frank 2015 66730 null Engineering Noah 2017 109000 66730 Engineering Alice 2019 87600 109000 Finance Dave 2015 52461 null Finance Nina 2018 91203 52461  |
| :---- | :---- |

| F.ntile() | 📌 What: Divide the rows within each partition into N equal-sized buckets (1 to N). 💡 Why: Split employees into salary quartiles. Assign top 25%, bottom 25%, etc. Code: w \= Window.partitionBy("dept").orderBy(F.desc("salary")) df.withColumn("quartile", F.ntile(4).over(w))   .select("dept","name","salary","quartile").show(5) Output (sample rows): dept name salary quartile Engineering Noah 109000 1 Engineering Irene 103200 1 Engineering Alice 87600 1 Engineering Karen 82390 1 Engineering Eve 78430 2  |
| :---- | :---- |

| F.sum().over(w) | 📌 What: Running/cumulative sum: each row gets the sum of all rows up to and including itself. 💡 Why: Cumulative revenue, running headcount, progressive totals by date. Code: w \= Window.partitionBy("dept").orderBy("join\_year")          .rowsBetween(Window.unboundedPreceding, Window.currentRow) df.withColumn("cum\_salary", F.sum("salary").over(w))   .select("dept","name","join\_year","salary","cum\_salary").show(5) Output (sample rows): dept name join\_year salary cum\_salary Engineering Frank 2015 66730 66730 Engineering Noah 2017 109000 175730 Engineering Alice 2019 87600 263330 Finance Dave 2015 52461 52461 Finance Nina 2018 91203 143664  |
| :---- | :---- |

| .repartition()  WIDE  | 📌 What: Redistribute data into exactly N partitions, optionally partitioned by column value. 💡 Why: Fix data skew. Increase parallelism before heavy aggregations. Control output file count. Code: \# Before: df.rdd.getNumPartitions() → 2 df\_repartitioned \= df.repartition(10, "dept") \# After: df\_repartitioned.rdd.getNumPartitions() → 10 df\_repartitioned.select("name","dept","salary").show(5) Output (sample rows): name dept salary partition\_note Alice Engineering 87600 partition by dept Frank Engineering 66730 partition by dept Bob Marketing 50000 partition by dept Dave Finance 52461 partition by dept Carol HR 56970 partition by dept  |
| :---- | :---- |

| .coalesce() | 📌 What: Reduce the number of partitions WITHOUT a full shuffle. Can only decrease, not increase. 💡 Why: Before writing output, reduce 200 partitions to 4 files. Much faster than repartition(). Code: \# Before: df.rdd.getNumPartitions() → 200 df\_coalesced \= df.coalesce(4) \# After: df\_coalesced.rdd.getNumPartitions() → 4 df\_coalesced.write.parquet("output/employees/") Output (sample rows): metric before after num\_partitions 200 4 shuffle full shuffle no shuffle output\_files 200 small files 4 larger files write\_time slow fast use\_when need more partitions need fewer partitions  |
| :---- | :---- |

| Window spec | 📌 What: Defines which rows to consider together (partitionBy) and how to order them (orderBy). 💡 Why: Required for ALL window functions. Think of it as 'GROUP BY \+ ORDER BY combined'. Code: \# Basic: partition by dept, order by salary desc w1 \= Window.partitionBy("dept").orderBy(F.desc("salary")) \# With frame: only look at rows up to current row w2 \= Window.partitionBy("dept").orderBy("join\_year")            .rowsBetween(Window.unboundedPreceding, Window.currentRow) Output (sample rows): window\_param purpose example partitionBy('dept') Group rows like GROUP BY separate rank per dept orderBy(F.desc('salary')) Order within partition highest salary \= rank 1 rowsBetween(unbound, current) Frame: rows to include cumulative sum rangeBetween(-1,1) Frame: value range rolling average .over(w) Apply window to a function F.rank().over(w)  |
| :---- | :---- |

| ⭐  You now know all 47 PySpark transformations\! Practice NARROW transformations first (they're free\!), then master WIDE ones — always ask: can I broadcast? can I filter earlier? |
| :---: |

