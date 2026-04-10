   
   
   
   
 

| 🐼 Pandas The Complete Engineering Guide ───────────────────────────────────────────────── Architecture  ·  Memory Management  ·  All Methods & Modules DataFrame  ·  Series  ·  Index  ·  GroupBy  ·  Time Series  ·  I/O What It Solves  ·  Why It Was Built  ·  Real-World Scenarios |
| :---: |

   
   
Version 1.0  |  March 2026  |  Comprehensive Reference Edition

**TABLE OF CONTENTS**

*Auto-generated — right-click in Word and select 'Update Field' to populate all page numbers*

# **Chapter 1 — Why Pandas? The Problem It Solves**

| The Origin Story · The Data Manipulation Problem · Why Python Needed Pandas |
| :---: |

 

*▲ What Pandas Solves — The Complete Problem Space*

## **1.1  The Pre-Pandas World (Before 2008\)**

In 2008, Wes McKinney was working at AQR Capital Management on quantitative financial analysis. Python was already powerful, but working with tabular data — the kind you get from spreadsheets, databases, and CSV files — was painful. Every operation required writing custom code that was slow, error-prone, and hard to read.

 

| Problem | What You Had to Do (Pre-Pandas) | Pain Level |
| :---- | :---- | :---- |
| Read a CSV file | csv.reader() loop, manual type conversion, dict building | Very High |
| Filter rows by condition | List comprehension or manual for-loop with if statements | High |
| Compute group averages | Build dicts manually: defaultdict, sort keys, then compute | Very High |
| Handle missing data | Check for None/'' everywhere; no consistent NaN propagation | Very High |
| Join two datasets | Manual key-matching loops or dump to SQL database | Extreme |
| Time series resampling | Custom datetime bucketing code every single time | Extreme |
| String operations on a column | List comprehension: \[s.upper() for s in col\] | Medium |
| Compute rolling average | Manual sliding-window loop with deques | High |
| Pivot a table | Nested dict loops \+ custom sort logic | Very High |

 

## **1.2  What Pandas Was Built to Solve**

Pandas was designed as a high-level data manipulation library that brings the power of R's data.frame and SQL's relational algebra to Python. The name comes from 'Panel Data' — a term from econometrics for multi-dimensional structured datasets. It was open-sourced in 2009 and became the backbone of the Python data science ecosystem.

 

| Core Design Goal | How Pandas Achieves It |
| :---- | :---- |
| Label-based data access | DataFrame columns have names; rows can have meaningful labels (Index). Access by name, not just position. |
| Automatic alignment | Operations on Series/DataFrame auto-align on the Index — no manual key matching needed. |
| Missing data as first class | NaN (Not a Number) propagates through all operations. isna(), fillna(), dropna() are built-in. |
| Flexible I/O | 50+ read\_\*/to\_\* functions for CSV, Excel, JSON, SQL, Parquet, HDF5, Feather, Clipboard, and more. |
| SQL-style operations | merge(), groupby(), pivot(), melt() — relational algebra in Python without a database. |
| Time series intelligence | DatetimeIndex, resample(), rolling(), shift() — financial and scientific time series built-in. |
| Performance via NumPy | Column operations are vectorized through NumPy C-extensions — no Python loops needed. |
| Interoperability | Works natively with NumPy, Matplotlib, scikit-learn, SQLAlchemy, PyArrow. |

 

## **1.3  Pandas in the Python Ecosystem**

*▲ Pandas Architecture — Foundation Libraries & Ecosystem*

## **1.4  When to Use Pandas (and When Not To)**

| Scenario | Use Pandas? | Reason |
| :---- | :---- | :---- |
| Data fits in RAM (\< \~5 GB) | YES | In-memory operations are fast and convenient |
| EDA / prototyping on any size | YES | Interactive, great Jupyter notebook experience |
| ML feature engineering | YES | scikit-learn, XGBoost etc. all accept Pandas DataFrames |
| Time series analysis | YES | DatetimeIndex, resample, rolling are unmatched |
| Reading/writing Excel, CSV, JSON | YES | Best-in-class I/O API |
| Data \> RAM (10GB+) | CONSIDER Polars/Dask | Pandas loads all data into RAM — OOM risk |
| Distributed cluster computing | Use PySpark | Pandas is single-machine; Spark scales to clusters |
| Real-time streaming data | Use Kafka+Spark | Pandas has no streaming capability |
| Deep learning tensor ops | Use PyTorch/TF | Different data model; use .values to pass to tensors |

# **Chapter 2 — Architecture & Memory Management**

| Internal Architecture · BlockManager · dtypes · Memory Optimization |
| :---: |

 

*▲ Pandas Memory Architecture — DataFrame Internals & dtype Guide*

## **2.1  How DataFrame Stores Data Internally**

A DataFrame is not a 2D array. Internally, Pandas uses a BlockManager that groups columns by dtype into contiguous NumPy arrays called 'blocks'. All int64 columns share one NumPy block, all float64 columns share another. This is why vectorized operations on same-dtype columns are fast but mixed-type operations require copying.

| PYTHON | import pandas as pd import numpy as np \# Create a DataFrame df \= pd.DataFrame({     'name':    \['Alice', 'Bob', 'Carol', 'Dave', 'Eve'\],     'age':     \[34, 28, 45, 31, 29\],     'salary':  \[95000.0, 72000.0, 110000.0, 68000.0, 88000.0\],     'active':  \[True, False, True, False, True\],     'dept':    \['Engineering', 'Marketing', 'Engineering', 'Marketing', 'HR'\],     'score':   pd.Categorical(\['A', 'C', 'A', 'B', 'A'\]), }) \# Inspect memory usage df.info(memory\_usage='deep')      \# deep=True counts actual string bytes print(df.memory\_usage(deep=True)) \# bytes per column print(df.memory\_usage(deep=True).sum() / 1024, 'KB') \# Inspect internal block structure print(df.\_data)                   \# BlockManager object print(df.\_data.blocks)            \# list of internal blocks |
| :---: | :---- |

 

| OUTPUT | \<class 'pandas.core.frame.DataFrame'\> RangeIndex: 5 entries, 0 to 4 Data columns (total 6 columns):  \#   Column   Non-Null Count  Dtype  0   name     5 non-null      object  1   age      5 non-null      int64  2   salary   5 non-null      float64  3   active   5 non-null      bool  4   dept     5 non-null      object  5   score    5 non-null      category dtypes: bool(1), category(1), float64(1), int64(1), object(2) memory usage: 934.0+ bytes |
| :---: | :---- |

 

## **2.2  Memory Optimization Techniques**

| PYTHON | \# BEFORE optimization print(df.memory\_usage(deep=True).sum())  \# e.g. 2,400,000 bytes \# Technique 1: Downcast integers df\['age'\] \= pd.to\_numeric(df\['age'\], downcast='integer')      \# int64 \-\> int8 df\['salary'\] \= pd.to\_numeric(df\['salary'\], downcast='float')  \# float64 \-\> float32 \# Technique 2: Convert low-cardinality strings to category df\['dept'\]  \= df\['dept'\].astype('category')   \# object \-\> category (90%+ savings) df\['score'\] \= df\['score'\].astype('category') \# Technique 3: Use string\[pyarrow\] for text (Pandas 2.0+) df\['name'\] \= df\['name'\].astype('string')      \# better than object \# even better with PyArrow backend: df\['name'\] \= df\['name'\].astype('string\[pyarrow\]') \# Technique 4: Use nullable integer types (pd.Int8Dtype etc.) df\['age'\] \= df\['age'\].astype(pd.Int8Dtype())   \# allows NaN \+ uses less RAM \# Technique 5: Use boolean instead of object 'yes'/'no' df\['active'\] \= df\['active'\].astype(bool) \# Technique 6: Specify dtypes on read (avoids inference cost too) df2 \= pd.read\_csv('file.csv', dtype={     'age': 'int8', 'salary': 'float32',     'dept': 'category', 'active': bool }) \# AFTER optimization — check savings print(df.memory\_usage(deep=True).sum())  \# e.g. 480,000 bytes (5x reduction) \# Technique 7: Read in chunks for very large files chunks \= pd.read\_csv('huge\_file.csv', chunksize=100\_000) results \= \[chunk\[chunk\['salary'\] \> 80000\] for chunk in chunks\] df\_filtered \= pd.concat(results, ignore\_index=True) \# Technique 8: Use select\_dtypes to work on column subsets numeric\_cols \= df.select\_dtypes(include='number').columns.tolist() cat\_cols     \= df.select\_dtypes(include='category').columns.tolist() string\_cols  \= df.select\_dtypes(include='object').columns.tolist() |
| :---: | :---- |

 

## **2.3  Copy vs View — A Critical Memory Concept**

One of the most common sources of bugs in Pandas is confusing copies with views. A view shares memory with the original; a copy does not. Modifying a view modifies the original; modifying a copy does not. Pandas 2.0 introduced Copy-on-Write (CoW) to make this deterministic.

| PYTHON | import pandas as pd, numpy as np df \= pd.DataFrame({'a':\[1,2,3,4,5\], 'b':\[10,20,30,40,50\]}) \# ── VIEWS (share underlying memory) view\_col  \= df\['a'\]              \# single column selection \= view view\_rows \= df\[df\['a'\] \> 2\]      \# boolean selection MAY return view or copy view\_iloc \= df.iloc\[0:3\]         \# slice CAN be a view \# ── COPIES (own their memory) copy\_col  \= df\['a'\].copy()       \# explicit copy copy\_df   \= df.copy()            \# deep copy of entire DataFrame copy\_df2  \= df.copy(deep=False)  \# shallow copy (shares data blocks) \# ── SettingWithCopyWarning — always use .loc on originals \# WRONG (may not work): df\[df\['a'\] \> 2\]\['b'\] \= 99        \# SettingWithCopyWarning\! \# CORRECT: df.loc\[df\['a'\] \> 2, 'b'\] \= 99   \# always use .loc for conditional assignment \# ── Copy-on-Write (CoW) — Pandas 2.0+ pd.options.mode.copy\_on\_write \= True   \# enable globally \# Now every modification creates a new object — predictable, no bugs \# ── Check if two objects share memory print(np.shares\_memory(df\['a'\].values, view\_col.values))  \# True \= view \# ── Flags: is the array writable? print(df\['a'\].values.flags\['WRITEABLE'\])  \# True if not a locked view |
| :---: | :---- |

 

# **Chapter 3 — Core Data Structures**

| Series · DataFrame · Index · MultiIndex — Construction & Attributes |
| :---: |

 

## **3.1  Series — 1D Labeled Array**

A Series is a one-dimensional labeled array capable of holding any data type. It is the building block of a DataFrame — each column is a Series. Think of it as a dictionary with ordered labels.

| PYTHON | import pandas as pd import numpy as np \# ── Creating Series s1 \= pd.Series(\[10, 20, 30, 40, 50\])                     \# default 0..4 index s2 \= pd.Series(\[10, 20, 30\], index=\['a', 'b', 'c'\])      \# custom index s3 \= pd.Series({'Alice': 95000, 'Bob': 72000, 'Carol': 110000})  \# from dict s4 \= pd.Series(5, index=range(5))                         \# scalar broadcast s5 \= pd.Series(np.random.randn(100), name='returns')      \# from numpy s6 \= pd.Series(pd.date\_range('2024-01-01', periods=5))    \# datetime Series \# ── Series Attributes print(s3.values)       \# numpy array: \[95000 72000 110000\] print(s3.index)        \# Index(\['Alice', 'Bob', 'Carol'\]) print(s3.dtype)        \# int64 print(s3.shape)        \# (3,) print(s3.size)         \# 3 print(s3.ndim)         \# 1 print(s3.name)         \# None (or 'salary' if set) print(s3.nbytes)       \# bytes in underlying array print(s3.hasnans)      \# False print(s3.is\_unique)    \# True print(s3.is\_monotonic\_increasing)  \# False print(s3.empty)        \# False print(s3.memory\_usage(deep=True))  \# bytes including index \# ── Accessing elements print(s3\['Alice'\])     \# 95000  (label-based) print(s3.iloc\[0\])      \# 95000  (position-based) print(s3.loc\['Bob'\])   \# 72000  (explicit label) print(s3.at\['Carol'\])  \# 110000 (fast scalar access) print(s3.iat\[2\])       \# 110000 (fast positional scalar) \# ── Operations auto-align on index s\_a \= pd.Series(\[1,2,3\], index=\['x','y','z'\]) s\_b \= pd.Series(\[10,20,30\], index=\['y','z','w'\]) print(s\_a \+ s\_b)  \# x=NaN, y=12, z=23, w=NaN (aligned by label) |
| :---: | :---- |

 

| OUTPUT | s3\['Alice'\] \= 95000 s\_a \+ s\_b: w     NaN x     NaN y    12.0 z    23.0 dtype: float64 |
| :---: | :---- |

 

## **3.2  DataFrame — 2D Labeled Table**

| PYTHON | import pandas as pd import numpy as np \# ── Creating DataFrames — all methods \# From dict of lists (most common) df \= pd.DataFrame({     'name':   \['Alice','Bob','Carol','Dave','Eve','Frank'\],     'age':    \[34, 28, 45, 31, 29, 52\],     'dept':   \['Engineering','Marketing','Engineering','Marketing','HR','Finance'\],     'salary': \[95000., 72000., 110000., 68000., 88000., 105000.\],     'active': \[True, False, True, False, True, True\] }) \# From list of dicts df2 \= pd.DataFrame(\[     {'name':'Alice', 'salary':95000},     {'name':'Bob',   'salary':72000}, \]) \# From numpy array df3 \= pd.DataFrame(np.random.randn(5,3), columns=\['A','B','C'\]) \# From dict of Series (index aligns automatically) df4 \= pd.DataFrame({'salary': s3, 'bonus': s3 \* 0.1}) \# From CSV (most common in practice) \# df \= pd.read\_csv('data.csv', parse\_dates=\['date'\], index\_col='id') \# ── DataFrame Attributes print(df.shape)          \# (6, 5\) print(df.columns)        \# Index(\['name','age','dept','salary','active'\]) print(df.index)          \# RangeIndex(start=0, stop=6, step=1) print(df.dtypes)         \# dtype of each column print(df.ndim)           \# 2 print(df.size)           \# 30 (6\*5) print(df.empty)          \# False print(df.axes)           \# \[row\_index, col\_index\] print(df.values)         \# 2D numpy array (converts all to common dtype) print(df.to\_numpy())     \# preferred over .values in modern Pandas print(df.T)              \# transpose \# ── Inspect data df.head(3)               \# first 3 rows df.tail(3)               \# last 3 rows df.sample(3)             \# 3 random rows df.sample(frac=0.5)      \# 50% random sample df.info()                \# schema \+ memory df.describe()            \# count/mean/std/min/25%/50%/75%/max df.describe(include='all')  \# includes object/category columns df.describe(include=\['object'\])   \# only strings df.nunique()             \# unique count per column df.value\_counts('dept')  \# frequency per dept |
| :---: | :---- |

 

*▲ Pandas Index Architecture — Types, Alignment & Operations*

## **3.3  MultiIndex — Hierarchical Indexing**

| PYTHON | import pandas as pd \# ── Create MultiIndex arrays \= \[\['Engineering','Engineering','Marketing','Marketing'\],           \['Alice','Bob','Carol','Dave'\]\] idx \= pd.MultiIndex.from\_arrays(arrays, names=\['dept','name'\]) \# From tuples idx2 \= pd.MultiIndex.from\_tuples(\[('Eng','Alice'),('Eng','Bob'),('Mkt','Carol')\]) \# From product idx3 \= pd.MultiIndex.from\_product(\[\['2022','2023'\],\['Q1','Q2','Q3','Q4'\]\],                                     names=\['year','quarter'\]) \# Create DataFrame with MultiIndex df\_mi \= pd.DataFrame({     'salary': \[95000,72000,110000,68000\],     'bonus':  \[9500,7200,11000,6800\] }, index=idx) print(df\_mi) \# ── MultiIndex access df\_mi.loc\['Engineering'\]           \# all Engineering rows df\_mi.loc\[('Engineering','Alice')\]  \# specific row df\_mi.xs('Alice', level='name')    \# cross-section by level \# ── MultiIndex operations df\_mi.reset\_index()               \# MultiIndex \-\> regular columns df\_mi.stack()                     \# pivot inner column to row level df\_mi.unstack()                   \# pivot inner row level to column df\_mi.swaplevel()                 \# swap level 0 and 1 df\_mi.sort\_index()                \# sort lexicographically df\_mi.droplevel(0)                \# remove outer level \# ── set\_index / reset\_index df.set\_index('name')              \# name column \-\> index df.set\_index(\['dept','name'\])     \# MultiIndex from two columns df.reset\_index()                  \# index \-\> column df.reset\_index(drop=True)         \# discard old index |
| :---: | :---- |

 

# **Chapter 4 — Indexing, Selection & Filtering**

| loc · iloc · at · iat · Boolean Indexing · Query · where/mask |
| :---: |

 

## **4.1  The Four Indexers**

| Indexer | Type | Rows | Columns | Best For |
| :---- | :---- | :---- | :---- | :---- |
| df.loc\[\] | Label-based | Row label(s) | Column name(s) | Named access — most readable |
| df.iloc\[\] | Position-based | Integer position(s) | Integer position(s) | Pure positional access |
| df.at\[\] | Label scalar | Single row label | Single column name | Fast single-cell by label |
| df.iat\[\] | Position scalar | Single position | Single position | Fast single-cell by position |
| df\[\] | Mixed shorthand | Slice/boolean | Column name(s) | Quick column grab or boolean filter |

 

| PYTHON | import pandas as pd df \= pd.DataFrame({     'name':   \['Alice','Bob','Carol','Dave','Eve'\],     'dept':   \['Eng','Mkt','Eng','Mkt','HR'\],     'salary': \[95000.,72000.,110000.,68000.,88000.\],     'age':    \[34,28,45,31,29\] }, index=\['r0','r1','r2','r3','r4'\]) \# ── df.loc — label-based (inclusive on both ends for slices) df.loc\['r0'\]                     \# single row as Series df.loc\['r0', 'salary'\]           \# single cell df.loc\['r0':'r2'\]                \# row slice (inclusive) df.loc\['r0':'r2', 'name':'dept'\] \# row+col slice df.loc\[\['r0','r2','r4'\]\]         \# list of row labels df.loc\[:, \['name','salary'\]\]     \# all rows, specific cols df.loc\[df\['salary'\] \> 80000\]     \# boolean index on rows df.loc\[df\['dept'\].isin(\['Eng','HR'\]), 'salary'\]  \# filtered col \# ── df.iloc — position-based (exclusive end like Python slices) df.iloc\[0\]                       \# first row df.iloc\[0, 2\]                    \# row 0, col 2 df.iloc\[0:3\]                     \# rows 0,1,2 df.iloc\[0:3, 0:2\]                \# rows 0-2, cols 0-1 df.iloc\[\[0,2,4\]\]                 \# specific rows by position df.iloc\[:, \-1\]                   \# last column df.iloc\[::2\]                     \# every other row \# ── df.at / df.iat — fastest single cell access df.at\['r0', 'salary'\]            \# label-based (100x faster than .loc for scalar) df.iat\[0, 2\]                     \# position-based \# ── df\[\] shorthand df\['salary'\]                     \# single column \-\> Series df\[\['name','salary'\]\]            \# multiple columns \-\> DataFrame df\[df\['salary'\] \> 80000\]         \# boolean filter (rows) df\[:3\]                           \# row slice (only for slices) \# ── Boolean Indexing — all patterns df\[df\['dept'\] \== 'Eng'\]                            \# equality df\[df\['salary'\] \> 80000\]                           \# comparison df\[(df\['dept'\] \== 'Eng') & (df\['age'\] \< 40)\]       \# AND df\[(df\['dept'\] \== 'Eng') | (df\['dept'\] \== 'HR')\]   \# OR df\[\~(df\['dept'\] \== 'Mkt')\]                         \# NOT df\[df\['dept'\].isin(\['Eng','HR'\])\]                  \# isin df\[df\['name'\].str.startswith('A')\]                 \# string condition df\[df\['salary'\].between(70000, 100000)\]             \# between df\[df\['salary'\].isna()\]                             \# null check df\[df\['age'\].notna()\]                               \# not null \# ── Query method — SQL-like string syntax df.query("dept \== 'Eng' and salary \> 80000") df.query("salary \> @min\_sal")        \# @variable reference df.query("dept in \['Eng','HR'\]") df.query('index \> 0')                  \# query on index \# ── where / mask df\['salary'\].where(df\['salary'\] \> 80000\)         \# keep if True, else NaN df\['salary'\].where(df\['salary'\] \> 80000, other=0) \# keep if True, else 0 df\['salary'\].mask(df\['salary'\] \> 100000, other=99999) \# replace if True \# ── Assignment via indexers df.loc\[df\['dept'\]=='Mkt', 'salary'\] \*= 1.10      \# 10% raise for Marketing df.loc\['r0', 'active'\] \= True                     \# set single cell df.iloc\[0:2, 3\] \= 100000                          \# set by position |
| :---: | :---- |

 

## **4.2  Conditional Selection Scenarios**

| PYTHON | \# Scenario: Select top earners by department top\_earners \= df.groupby('dept')\['salary'\] \\                 .nlargest(2) \\                 .reset\_index(level=0) \# Scenario: Filter with multiple complex conditions senior\_eng \= df\[     (df\['dept'\] \== 'Engineering') &     (df\['age'\] \>= 30\) &     (df\['salary'\] \>= 90000\) &     (df\['active'\] \== True) \] \# Scenario: Select rows where any value matches has\_keyword \= df\[df.apply(lambda row: row.astype(str).str.contains('Alice').any(), axis=1)\] \# Scenario: Select columns by dtype numeric\_df  \= df.select\_dtypes(include=\['number'\]) string\_df   \= df.select\_dtypes(include=\['object', 'string'\]) category\_df \= df.select\_dtypes(include=\['category'\]) \# Scenario: Select columns by name pattern sal\_cols \= df.filter(like='salary')        \# columns containing 'salary' q\_cols   \= df.filter(regex='^Q\[1-4\]\_')     \# columns matching regex |
| :---: | :---- |

 

# **Chapter 5 — Data Manipulation — All Methods**

| Add/Remove Columns · Rename · Sort · Apply · Map · Pipe · Transform |
| :---: |

 

## **5.1  Adding, Modifying & Removing Columns**

| PYTHON | import pandas as pd import numpy as np df \= pd.DataFrame({     'name':   \['Alice','Bob','Carol','Dave','Eve'\],     'dept':   \['Engineering','Marketing','Engineering','Marketing','HR'\],     'salary': \[95000.,72000.,110000.,68000.,88000.\],     'age':    \[34,28,45,31,29\] }) \# ── Add columns df\['bonus'\]       \= df\['salary'\] \* 0.15                \# arithmetic df\['total\_comp'\]  \= df\['salary'\] \+ df\['bonus'\]         \# from other cols df\['level'\]       \= 'Senior'                           \# scalar broadcast df\['name\_upper'\]  \= df\['name'\].str.upper()             \# string op df\['salary\_k'\]    \= (df\['salary'\] / 1000).round(1)    \# derived \# assign() — chainable, returns new df df \= df.assign(     tax       \= lambda x: x\['salary'\] \* 0.3,     net\_pay   \= lambda x: x\['salary'\] \- x\['salary'\] \* 0.3,     grade     \= lambda x: pd.cut(x\['age'\], bins=\[0,30,40,100\],                                   labels=\['Junior','Mid','Senior'\]) ) \# insert() — add at specific position df.insert(loc=2, column='emp\_id', value=range(1, len(df)+1)) \# ── Modify existing columns df\['salary'\]  \= df\['salary'\] \* 1.05                    \# in-place update df.loc\[df\['dept'\]=='HR','salary'\] \+= 5000              \# conditional update \# ── Remove columns df.drop(columns=\['bonus'\])                              \# drop one df.drop(columns=\['bonus','tax'\])                        \# drop many df.drop('bonus', axis=1)                               \# axis=1 for columns del df\['bonus'\]                                         \# Python del (in-place) df.pop('bonus')                                         \# removes \+ returns \# ── Rename columns df.rename(columns={'salary':'annual\_salary', 'age':'years\_old'}, inplace=True) df.rename(columns=str.upper)                            \# function applied to all df.columns \= \['name','dept','salary','age','bonus'\]     \# replace all at once df.add\_prefix('col\_')                                   \# add prefix to all cols df.add\_suffix('\_2024')                                  \# add suffix to all cols \# ── Reorder columns df \= df\[\['name','emp\_id','dept','salary','age'\]\]        \# explicit order df \= df.reindex(columns=\['name','dept','salary'\])       \# reindex (drops unspecified) |
| :---: | :---- |

 

## **5.2  apply, map, applymap, transform, pipe**

| PYTHON | \# ── Series.map() — element-wise (Series only) df\['dept\_code'\] \= df\['dept'\].map({     'Engineering': 'ENG',     'Marketing':   'MKT',     'HR':          'HR ' }) df\['name\_len'\] \= df\['name'\].map(len)              \# function per element \# ── Series.apply() — element-wise function on Series df\['salary\_band'\] \= df\['salary'\].apply(lambda x:     'Senior' if x \>= 90000 else ('Mid' if x \>= 70000 else 'Junior')) \# ── DataFrame.apply() — function on rows or columns \# axis=0 (default): function called once per COLUMN col\_means \= df\[\['salary','age'\]\].apply(np.mean, axis=0) \# axis=1: function called once per ROW df\['name\_dept'\] \= df.apply(lambda row: f"{row\['name'\]} ({row\['dept'\]})", axis=1) \# ── applymap() / map() for DataFrames (Pandas 2.1+: use map()) \# Element-wise on every cell df\_num \= df\[\['salary','age'\]\].map(lambda x: round(x, \-3)) \# ── transform() — like apply but must return same-shape result \# Useful for creating new columns based on group operations df\['dept\_avg\_sal'\]  \= df.groupby('dept')\['salary'\].transform('mean') df\['sal\_vs\_dept'\]   \= df\['salary'\] \- df.groupby('dept')\['salary'\].transform('mean') df\['sal\_pct\_rank'\]  \= df.groupby('dept')\['salary'\].transform(lambda x: x.rank(pct=True)) df\['normalized\_sal'\]= df.groupby('dept')\['salary'\].transform(     lambda x: (x \- x.mean()) / x.std()) \# ── pipe() — method chaining with external functions def add\_salary\_percentile(df):     df\['pctile'\] \= df\['salary'\].rank(pct=True)     return df def flag\_active(df, threshold=90000):     df\['high\_earner'\] \= df\['salary'\] \> threshold     return df result \= (df     .assign(bonus=lambda x: x\['salary'\]\*0.1)     .pipe(add\_salary\_percentile)     .pipe(flag\_active, threshold=90000)     .sort\_values('salary', ascending=False) ) |
| :---: | :---- |

 

## **5.3  Sorting**

| PYTHON | \# Sort by values df.sort\_values('salary')                                  \# ascending df.sort\_values('salary', ascending=False)                 \# descending df.sort\_values(\['dept','salary'\], ascending=\[True,False\]) \# multi-col df.sort\_values('salary', na\_position='last')              \# NaN at end df.sort\_values('salary', key=lambda col: col.abs())       \# custom key \# Sort by index df.sort\_index()                          \# ascending index df.sort\_index(ascending=False)           \# descending df.sort\_index(axis=1)                    \# sort columns alphabetically \# nlargest / nsmallest (faster than sort for top-N) df.nlargest(3, 'salary')                \# top 3 salary rows df.nsmallest(2, 'age')                  \# youngest 2 df.nlargest(3, \['salary','age'\])        \# break ties by age \# rank df\['salary\_rank'\] \= df\['salary'\].rank(ascending=False)        \# 1=highest df\['salary\_rank'\] \= df\['salary'\].rank(method='dense')         \# no gaps df\['salary\_rank'\] \= df\['salary'\].rank(method='first')         \# by order of appearance df\['dept\_rank'\]   \= df.groupby('dept')\['salary'\].rank(ascending=False) |
| :---: | :---- |

 

## **5.4  String Methods — str Accessor**

| PYTHON | \# All accessed via .str accessor s \= df\['name'\] \# Case s.str.upper()             \# ALICE, BOB... s.str.lower()             \# alice, bob... s.str.title()             \# Alice, Bob... s.str.capitalize()        \# First char upper s.str.swapcase()          \# Toggle case \# Contains / match s.str.contains('Ali', case=True, na=False)    \# boolean Series s.str.startswith('A')                          \# boolean s.str.endswith('e')                            \# boolean s.str.match(r'^\[A-C\]')                         \# regex match from start s.str.fullmatch(r'Alice')                      \# complete string match s.str.find('li')                               \# position of substring s.str.count('a')                               \# count occurrences \# Extraction s.str\[0\]                                       \# first character s.str\[0:3\]                                     \# slice s.str.slice(0, 3\)                              \# explicit slice s.str.extract(r'(A\\w+)')                      \# capture group \-\> DataFrame s.str.extractall(r'(\\w+)')                    \# all matches s.str.findall(r'\[aeiou\]')                      \# find all matches \-\> list \# Replace s.str.replace('e', 'E')                        \# replace all s.str.replace(r'\\s+', '\_', regex=True)        \# regex replace s.str.replace('Carol', 'Caroline', n=1)        \# first occurrence \# Split / join df\['dept'\].str.split('e')                      \# split \-\> list df\['dept'\].str.split('e', expand=True)         \# split \-\> DataFrame df\['dept'\].str.split('e', n=1)                 \# max 1 split df\['dept'\].str.rsplit('e', n=1)                \# split from right pd.Series(\[\['a','b'\],\['c'\]\]).str.join('-')      \# join lists \# Padding / alignment s.str.pad(10, side='left', fillchar='\*')       \# left pad s.str.pad(10, side='right')                    \# right pad s.str.center(10, '-')                          \# center s.str.ljust(10)                                \# left justify s.str.rjust(10)                                \# right justify s.str.zfill(5)                                 \# zero-fill (like 00Alice) \# Clean s.str.strip()                                  \# remove leading/trailing spaces s.str.lstrip('A')                              \# left strip character s.str.rstrip('e')                              \# right strip character s.str.strip('\*-') \# Type checking s.str.isdigit()                                \# all digits? s.str.isalpha()                                \# all alpha? s.str.isalnum()                                \# alphanumeric? s.str.isnumeric()                              \# numeric? s.str.isspace()                                \# all whitespace? s.str.islower()                                \# all lower? s.str.isupper()                                \# all upper? \# Other s.str.len()                                    \# string length s.str.encode('utf-8')                          \# encode s.str.decode('utf-8')                          \# decode bytes s.str.get\_dummies(sep='|')                     \# one-hot from delimited string s.str.cat(sep=', ')                            \# concatenate all values s.str.repeat(2)                                \# repeat string s.str.normalize('NFC')                         \# Unicode normalization s.str.wrap(20)                                 \# wrap at width s.str.translate(str.maketrans('abc','ABC'))    \# translate chars |
| :---: | :---- |

 

## **5.5  Categorical Data**

| PYTHON | \# Create categorical cat \= pd.Categorical(\['a','b','a','c','b'\], categories=\['c','b','a'\], ordered=True) df\['grade'\] \= pd.Categorical(\['A','B','A','C'\], categories=\['C','B','A'\], ordered=True) \# Convert to category df\['dept'\] \= df\['dept'\].astype('category') \# cat accessor df\['dept'\].cat.categories          \# Index(\['Engineering','HR','Marketing'\]) df\['dept'\].cat.codes               \# integer codes: 0,1,2... df\['dept'\].cat.ordered             \# False df\['dept'\].cat.rename\_categories({'Engineering': 'Eng'}) df\['dept'\].cat.reorder\_categories(\['HR','Marketing','Engineering'\]) df\['dept'\].cat.add\_categories(\['Legal'\]) df\['dept'\].cat.remove\_categories(\['Legal'\]) df\['dept'\].cat.remove\_unused\_categories() df\['dept'\].cat.set\_categories(\['Engineering','Marketing'\], ordered=True) df\['dept'\].cat.as\_ordered()        \# make ordered df\['dept'\].cat.as\_unordered() |
| :---: | :---- |

 

# **Chapter 6 — Handling Missing Data**

| isna · fillna · dropna · interpolate · Nullable Types |
| :---: |

 

## **6.1  Detecting Missing Values**

| PYTHON | import pandas as pd import numpy as np df \= pd.DataFrame({     'name':   \['Alice',None,'Carol',np.nan,'Eve'\],     'salary': \[95000, 72000, np.nan, 68000, 88000\],     'age':    \[34, 28, 45, None, 29\],     'dept':   \['Eng', '', 'Eng', 'Mkt', np.nan\] }) \# Detect nulls df.isna()                      \# True where null/NaN/None df.isnull()                    \# alias for isna() df.notna()                     \# inverse — True where not null df.notnull()                   \# alias for notna() \# Count nulls df.isna().sum()                \# nulls per column df.isna().sum(axis=1)          \# nulls per row df.isna().mean()               \# null fraction per column df.isna().any()                \# any null per column? bool df.isna().all()                \# all null per column? bool df.isna().sum().sum()          \# total nulls in DataFrame \# Null percentage report null\_report \= pd.DataFrame({     'null\_count': df.isna().sum(),     'null\_pct':   (df.isna().mean() \* 100).round(2) }).query('null\_count \> 0') print(null\_report) \# Check Series pd.isna(df\['salary'\])          \# Series of booleans pd.notna(df\['salary'\]) \# is NaN (numeric NaN only) import numpy as np df\['salary'\].apply(lambda x: np.isnan(x) if isinstance(x, float) else False) |
| :---: | :---- |

 

## **6.2  Filling Missing Values**

| PYTHON | \# ── fillna — replace NaN with a value df\['salary'\].fillna(0)                           \# fill with constant df\['salary'\].fillna(df\['salary'\].mean())         \# fill with mean df\['salary'\].fillna(method='ffill')              \# forward fill (last valid) df\['salary'\].fillna(method='bfill')              \# backward fill (next valid) df\['salary'\].fillna(method='ffill', limit=2)     \# fill max 2 consecutive \# Fill different columns with different values df.fillna({'salary': 0, 'name': 'Unknown', 'age': df\['age'\].median()}) \# ── ffill / bfill — chained methods (Pandas 2.0+) df\['salary'\].ffill()                             \# forward fill df\['salary'\].bfill()                             \# backward fill \# ── interpolate — estimate missing values df\['salary'\].interpolate()                       \# linear (default) df\['salary'\].interpolate(method='polynomial', order=2) df\['salary'\].interpolate(method='nearest') df\['salary'\].interpolate(method='index')         \# use index for spacing df\['salary'\].interpolate(method='time')          \# for DatetimeIndex df\['salary'\].interpolate(limit=2, limit\_direction='forward') \# ── replace — replace specific values (not just NaN) df.replace(np.nan, 0\)                            \# replace NaN with 0 df.replace('', np.nan)                           \# empty string \-\> NaN df.replace({'salary': {0: np.nan}})              \# dict-based replace df.replace(\[-999, \-998\], np.nan)                 \# multiple sentinel values df\['name'\].replace(r'^\\s\*$', np.nan, regex=True)  \# whitespace \-\> NaN \# ── where — fill where condition is False df\['salary'\].where(df\['salary'\] \> 0, other=0)   \# replace negatives with 0 |
| :---: | :---- |

 

## **6.3  Dropping Missing Values**

| PYTHON | \# ── dropna df.dropna()                          \# drop rows with ANY null df.dropna(how='all')                 \# drop rows where ALL are null df.dropna(how='any')                 \# same as default df.dropna(subset=\['salary','age'\])   \# drop if null in these columns only df.dropna(axis=1)                    \# drop COLUMNS with any null df.dropna(axis=1, how='all')         \# drop columns that are entirely null df.dropna(thresh=3)                  \# keep rows with at least 3 non-null values \# ── Scenario: clean pipeline clean \= (df     .replace('', np.nan)             \# treat empty strings as null     .dropna(subset=\['name','salary'\]) \# require name and salary     .fillna({'age': df\['age'\].median(), 'dept': 'Unknown'})     .reset\_index(drop=True) ) |
| :---: | :---- |

 

# **Chapter 7 — GroupBy & Aggregation**

| Split-Apply-Combine · Named Agg · transform · filter · Pivot Tables |
| :---: |

 

*▲ GroupBy Split-Apply-Combine Execution Model*

## **7.1  GroupBy Basics**

| PYTHON | import pandas as pd import numpy as np df \= pd.DataFrame({     'name':   \['Alice','Bob','Carol','Dave','Eve','Frank'\],     'dept':   \['Eng','Mkt','Eng','Mkt','HR','Eng'\],     'salary': \[95000.,72000.,110000.,68000.,88000.,105000.\],     'age':    \[34,28,45,31,29,52\],     'active': \[True,False,True,False,True,True\] }) \# ── Basic groupby g \= df.groupby('dept')               \# GroupBy object (lazy) g \= df.groupby(\['dept','active'\])    \# multiple keys g \= df.groupby('dept', sort=True)    \# sort groups g \= df.groupby('dept', dropna=False) \# include NaN groups g \= df.groupby('dept', observed=True)\# for Categorical — only observed combos \# Access a group g.get\_group('Eng')                   \# DataFrame for group 'Eng' \# Iterate over groups for name, group in df.groupby('dept'):     print(name, len(group)) \# ── Single aggregations df.groupby('dept')\['salary'\].mean()   \# mean salary per dept df.groupby('dept')\['salary'\].sum()    \# total payroll per dept df.groupby('dept')\['salary'\].max()    \# max salary per dept df.groupby('dept')\['salary'\].min() df.groupby('dept')\['salary'\].std() df.groupby('dept')\['salary'\].var() df.groupby('dept')\['salary'\].median() df.groupby('dept')\['salary'\].count()  \# non-null count df.groupby('dept').size()             \# total rows per group df.groupby('dept').first()            \# first row per group df.groupby('dept').last()             \# last row per group df.groupby('dept')\['salary'\].nth(0)   \# nth element per group df.groupby('dept')\['salary'\].nunique() df.groupby('dept')\['name'\].unique() df.groupby('dept')\['name'\].apply(list) |
| :---: | :---- |

 

## **7.2  Named Aggregation (Best Practice)**

| PYTHON | \# Named agg — most expressive pattern summary \= df.groupby('dept').agg(     headcount       \= ('name',    'count'),     avg\_salary      \= ('salary',  'mean'),     max\_salary      \= ('salary',  'max'),     min\_age         \= ('age',     'min'),     active\_count    \= ('active',  'sum'),     salary\_std      \= ('salary',  'std'),     median\_salary   \= ('salary',  'median'),     all\_names       \= ('name',    list),     top\_salary      \= ('salary',  lambda x: x.nlargest(1).iat\[0\]), ) print(summary.round(2)) \# Multi-function on same column (old style — still works) df.groupby('dept')\['salary'\].agg(\['mean','std','min','max'\]) \# Different functions per column (dict agg) df.groupby('dept').agg({     'salary': \['mean','std'\],     'age':    \['min','max'\],     'name':   'count' }) |
| :---: | :---- |

 

| OUTPUT |              headcount  avg\_salary  max\_salary  min\_age  active\_count dept Eng                  3    103333.3    110000.0       34             2 HR                   1     88000.0     88000.0       29             1 Mkt                  2     70000.0     72000.0       28             0 |
| :---: | :---- |

 

## **7.3  transform, filter, apply**

| PYTHON | \# ── transform() — returns same-shape Series/DataFrame \# Great for creating new columns relative to group stats df\['dept\_avg'\]       \= df.groupby('dept')\['salary'\].transform('mean') df\['dept\_rank'\]      \= df.groupby('dept')\['salary'\].transform('rank') df\['z\_score'\]        \= df.groupby('dept')\['salary'\].transform(     lambda x: (x \- x.mean()) / x.std()) df\['cummax\_salary'\]  \= df.groupby('dept')\['salary'\].transform('cummax') df\['group\_size'\]     \= df.groupby('dept')\['salary'\].transform('size') \# ── filter() — keep/remove entire groups \# Keep only departments with more than 1 employee df.groupby('dept').filter(lambda g: len(g) \> 1\) \# Keep groups where average salary \> 85000 df.groupby('dept').filter(lambda g: g\['salary'\].mean() \> 85000\) \# Keep groups with at least one active employee df.groupby('dept').filter(lambda g: g\['active'\].any()) \# ── apply() — most flexible, custom function per group \# Each group is a DataFrame, return anything def top\_2\_earners(group):     return group.nlargest(2, 'salary') df.groupby('dept', group\_keys=False).apply(top\_2\_earners) \# Normalize salary within group def normalize(group):     group \= group.copy()     mn, mx \= group\['salary'\].min(), group\['salary'\].max()     group\['sal\_norm'\] \= (group\['salary'\] \- mn) / (mx \- mn) if mx \> mn else 0     return group df.groupby('dept', group\_keys=False).apply(normalize) \# ── cumulative group operations df.groupby('dept')\['salary'\].cumsum() df.groupby('dept')\['salary'\].cummax() df.groupby('dept')\['salary'\].cummin() df.groupby('dept')\['salary'\].cumprod() df.groupby('dept')\['salary'\].cumcount()   \# count within group df.groupby('dept')\['salary'\].rank() df.groupby('dept')\['salary'\].pct\_change() df.groupby('dept')\['salary'\].diff() df.groupby('dept')\['salary'\].shift(1)     \# lag within group df.groupby('dept')\['salary'\].expanding().mean() df.groupby('dept')\['salary'\].rolling(2).mean() df.groupby('dept')\['salary'\].ewm(span=2).mean() |
| :---: | :---- |

 

## **7.4  Pivot Tables & Cross-Tabulation**

| PYTHON | \# ── pivot\_table — like Excel PivotTable pt \= df.pivot\_table(     values='salary',     index='dept',     columns='active',     aggfunc=\['mean','count'\],     fill\_value=0,     margins=True,        \# add totals row/column     margins\_name='Total' ) \# ── pivot — reshape without aggregation (unique index+col combos required) df\_wide \= df.pivot(index='name', columns='dept', values='salary') \# ── crosstab — frequency table of two categorical variables pd.crosstab(df\['dept'\], df\['active'\]) pd.crosstab(df\['dept'\], df\['active'\], normalize='index')  \# row % pd.crosstab(df\['dept'\], df\['active'\], values=df\['salary'\], aggfunc='mean') pd.crosstab(df\['dept'\], df\['active'\], margins=True) \# ── melt — wide to long (unpivot) df\_wide \= pd.DataFrame({'name':\['Alice','Bob'\], 'Q1':\[100,90\], 'Q2':\[110,95\]}) df\_long \= pd.melt(df\_wide, id\_vars=\['name'\], var\_name='quarter', value\_name='score') \# ── stack / unstack df.set\_index(\['dept','name'\]).stack()    \# wide \-\> long df.set\_index(\['dept','name'\]).unstack()  \# long \-\> wide \# ── wide\_to\_long pd.wide\_to\_long(df, stubnames=\['Q'\], i='name', j='quarter') |
| :---: | :---- |

 

# **Chapter 8 — Merging, Joining & Combining DataFrames**

| merge · join · concat · combine\_first · update |
| :---: |

 

## **8.1  pd.merge — SQL-Style Joins**

| PYTHON | import pandas as pd employees \= pd.DataFrame({     'emp\_id':  \[1,2,3,4,5\],     'name':    \['Alice','Bob','Carol','Dave','Eve'\],     'dept\_id': \[10,20,10,20,30\] }) departments \= pd.DataFrame({     'dept\_id':   \[10,20,40\],     'dept\_name': \['Engineering','Marketing','Finance'\],     'budget':    \[500000,200000,300000\] }) \# ── Join types \# INNER — only matching rows in both pd.merge(employees, departments, on='dept\_id', how='inner') \# LEFT — all left rows, NaN for no match on right pd.merge(employees, departments, on='dept\_id', how='left') \# RIGHT — all right rows, NaN for no match on left pd.merge(employees, departments, on='dept\_id', how='right') \# OUTER — all rows from both, NaN for non-matches pd.merge(employees, departments, on='dept\_id', how='outer') \# CROSS — cartesian product pd.merge(employees, departments, how='cross') \# ── Join on different column names pd.merge(employees, departments, left\_on='dept\_id', right\_on='dept\_id') \# ── Join on index pd.merge(employees, departments, left\_index=True, right\_index=True) \# ── Handle duplicate column names pd.merge(employees, departments, on='dept\_id', suffixes=('\_emp','\_dept')) \# ── Validate join (catch unexpected duplicates) pd.merge(employees, departments, on='dept\_id', how='left',          validate='many\_to\_one')  \# 'one\_to\_one','one\_to\_many','many\_to\_many' \# ── indicator — adds '\_merge' column showing source result \= pd.merge(employees, departments, on='dept\_id', how='outer', indicator=True) \# \_merge column: 'left\_only', 'right\_only', 'both' \# ── Join on multiple keys pd.merge(df1, df2, on=\['country','city'\], how='inner') |
| :---: | :---- |

 

## **8.2  DataFrame.join — Index-Based Join**

| PYTHON | \# join() aligns on INDEX by default (vs merge which aligns on column) df1 \= pd.DataFrame({'a':\[1,2,3\]}, index=\['x','y','z'\]) df2 \= pd.DataFrame({'b':\[4,5,6\]}, index=\['y','z','w'\]) df1.join(df2)                        \# left join on index (default) df1.join(df2, how='inner')           \# inner join df1.join(df2, how='outer')           \# outer join df1.join(df2, lsuffix='\_l', rsuffix='\_r') \# join on a column (must set\_index first) employees.set\_index('dept\_id').join(departments.set\_index('dept\_id')) |
| :---: | :---- |

 

## **8.3  pd.concat — Stack DataFrames**

| PYTHON | \# ── concat along rows (axis=0, default) df\_2022 \= pd.DataFrame({'name':\['Alice','Bob'\],'salary':\[90000,70000\]}) df\_2023 \= pd.DataFrame({'name':\['Carol','Dave'\],'salary':\[100000,75000\]}) combined \= pd.concat(\[df\_2022, df\_2023\], ignore\_index=True)  \# resets index combined \= pd.concat(\[df\_2022, df\_2023\], keys=\['2022','2023'\])  \# adds key level \# ── concat along columns (axis=1) df\_names \= pd.DataFrame({'name':\['Alice','Bob','Carol'\]}) df\_salary= pd.DataFrame({'salary':\[95000,72000,110000\]}) combined \= pd.concat(\[df\_names, df\_salary\], axis=1) \# Alignment: outer vs inner (for concat on columns with different indices) pd.concat(\[df1, df2\], axis=1, join='outer')   \# NaN for missing pd.concat(\[df1, df2\], axis=1, join='inner')   \# only common index \# ── append (deprecated in 2.0) — use concat instead pd.concat(\[df, new\_row.to\_frame().T\], ignore\_index=True) \# ── combine\_first — fill NaN from other DataFrame df\_a \= pd.DataFrame({'x':\[1,np.nan,3\],'y':\[4,5,np.nan\]}) df\_b \= pd.DataFrame({'x':\[10,20,30\],'y':\[40,50,60\]}) df\_a.combine\_first(df\_b)  \# use df\_b where df\_a is NaN \# ── update — update in-place with values from another df\_a.update(df\_b)         \# df\_a gets df\_b values where NOT NaN \# ── combine — element-wise custom function df\_a.combine(df\_b, lambda s1, s2: s1.where(s1 \> s2, s2)) \# ── compare — show differences between two DataFrames df\_a.compare(df\_b)        \# shows where values differ df\_a.compare(df\_b, align\_axis=0, keep\_shape=True) |
| :---: | :---- |

 

# **Chapter 9 — Time Series Analysis**

| DatetimeIndex · Resample · Rolling · Shift · Lag · Seasonal Decomp |
| :---: |

 

*▲ Time Series Architecture — DatetimeIndex, Resampling & Rolling Windows*

## **9.1  Creating & Parsing Dates**

| PYTHON | import pandas as pd import numpy as np \# ── Create date ranges dr \= pd.date\_range('2024-01-01', periods=365, freq='D')   \# daily pd.date\_range('2024-01-01', '2024-12-31', freq='B')       \# business days pd.date\_range('2024-01-01', periods=12, freq='MS')        \# month starts pd.date\_range('2024-01-01', periods=12, freq='ME')        \# month ends (2.2+) pd.date\_range('2024-01-01', periods=4, freq='QS')         \# quarter starts pd.date\_range('2024-01-01', periods=52, freq='W-MON')     \# weekly on Monday pd.bdate\_range('2024-01-01','2024-03-31')                  \# business date range pd.period\_range('2024-01', periods=12, freq='M')           \# Period objects pd.timedelta\_range('0 days','10 days', freq='6H')          \# timedelta range \# ── Parse dates from strings pd.to\_datetime('2024-01-15')                               \# single string pd.to\_datetime(\['2024-01-01','2024-06-15','2024-12-31'\])   \# list pd.to\_datetime('15/01/2024', format='%d/%m/%Y')           \# custom format pd.to\_datetime('Jan 15 2024')                              \# natural language pd.to\_datetime(1704067200, unit='s')                       \# unix timestamp pd.to\_datetime(df\['date\_str'\], errors='coerce')            \# coerce bad dates to NaT \# ── Parse dates when reading df \= pd.read\_csv('file.csv', parse\_dates=\['date','start\_date'\]) df \= pd.read\_csv('file.csv', parse\_dates={'dt': \['year','month','day'\]}) \# ── Common DatetimeIndex operations s \= pd.Series(np.random.randn(365), index=pd.date\_range('2024', periods=365, freq='D')) \# Partial string indexing s\['2024-03'\]                   \# all of March 2024 s\['2024-Q2'\]                   \# Q2 2024 s\['2024-01':'2024-03'\]         \# Jan through March s.loc\['2024-01-15'\]            \# specific date \# dt accessor (for Series with datetime dtype) df\['date'\].dt.year df\['date'\].dt.month df\['date'\].dt.day df\['date'\].dt.hour df\['date'\].dt.minute df\['date'\].dt.second df\['date'\].dt.microsecond df\['date'\].dt.nanosecond df\['date'\].dt.quarter df\['date'\].dt.week           \# ISO week number df\['date'\].dt.dayofweek      \# 0=Monday df\['date'\].dt.day\_name()     \# 'Monday' df\['date'\].dt.month\_name()   \# 'January' df\['date'\].dt.dayofyear df\['date'\].dt.days\_in\_month df\['date'\].dt.is\_month\_start df\['date'\].dt.is\_month\_end df\['date'\].dt.is\_quarter\_start df\['date'\].dt.is\_quarter\_end df\['date'\].dt.is\_year\_start df\['date'\].dt.is\_year\_end df\['date'\].dt.is\_leap\_year df\['date'\].dt.tz\_localize('UTC') df\['date'\].dt.tz\_convert('US/Eastern') df\['date'\].dt.normalize()    \# truncate to midnight df\['date'\].dt.date           \# Python date object df\['date'\].dt.time           \# Python time object df\['date'\].dt.floor('H')     \# floor to hour df\['date'\].dt.ceil('H')      \# ceil to hour df\['date'\].dt.round('H')     \# round to hour df\['date'\].dt.to\_period('M') \# convert to Period df\['date'\].dt.strftime('%Y-%m-%d')  \# format string df\['date'\].dt.total\_seconds()       \# timedelta \-\> seconds |
| :---: | :---- |

 

## **9.2  Resampling**

| PYTHON | \# Resample \= time-based groupby \# Create daily data dates \= pd.date\_range('2024-01-01', periods=365, freq='D') prices \= pd.Series(100 \+ np.cumsum(np.random.randn(365)), index=dates, name='price') \# ── Downsample (higher frequency \-\> lower) monthly\_avg  \= prices.resample('ME').mean()       \# month end monthly\_last \= prices.resample('ME').last()       \# last value monthly\_first= prices.resample('MS').first()      \# month start, first val weekly\_sum   \= prices.resample('W').sum() quarterly    \= prices.resample('QS').ohlc()       \# Open/High/Low/Close annual       \= prices.resample('YE').agg(\['min','max','mean','std'\]) \# ── Upsample (lower frequency \-\> higher) — requires fill hourly \= prices.resample('H').ffill()             \# forward fill hourly \= prices.resample('H').bfill()             \# backward fill hourly \= prices.resample('H').interpolate('linear') \# ── Custom resample with agg prices.resample('W').agg(\['mean','std','min','max'\]) prices.resample('ME').agg(     avg\_price    \= ('price','mean'),     volatility   \= ('price','std'),     monthly\_high \= ('price','max'),     monthly\_low  \= ('price','min') ) \# ── Resample on DataFrame df\_ts \= pd.DataFrame({'price':prices,'volume':np.random.randint(1000,5000,365)},                       index=dates) df\_ts.resample('W').agg({'price':'mean','volume':'sum'}) \# ── Period offset aliases \# 'D'=day, 'B'=business day, 'W'=week, 'ME'=month end, 'MS'=month start \# 'QS'=quarter start, 'QE'=quarter end, 'YS'=year start, 'YE'=year end \# 'H'=hour, 'min'=minute, 'S'=second, 'ms'=millisecond, 'us'=microsecond \# 'ns'=nanosecond, '2H'=2 hours, '15min'=15 minutes |
| :---: | :---- |

 

## **9.3  Rolling, Expanding & EWM**

| PYTHON | \# ── rolling() — fixed-size trailing window prices.rolling(7).mean()              \# 7-day moving average prices.rolling(7).std()               \# 7-day rolling std dev prices.rolling(7).min()               \# 7-day rolling minimum prices.rolling(7).max()               \# 7-day rolling maximum prices.rolling(7).sum()               \# 7-day rolling sum prices.rolling(7).var()               \# 7-day rolling variance prices.rolling(7).skew()              \# 7-day rolling skewness prices.rolling(7).kurt()              \# 7-day rolling kurtosis prices.rolling(7).quantile(0.75)      \# 7-day rolling 75th pctile prices.rolling(7).median()            \# 7-day rolling median prices.rolling(7, min\_periods=3).mean() \# need min 3 valid values prices.rolling(7, center=True).mean()   \# centered window prices.rolling(window=7, win\_type='gaussian').mean(std=1) \# Rolling correlation and covariance prices.rolling(30).corr(other\_series)  \# 30-day rolling correlation prices.rolling(30).cov(other\_series)   \# 30-day rolling covariance \# Rolling apply with custom function prices.rolling(30).apply(lambda x: (x\[-1\]-x\[0\])/x\[0\], raw=True)  \# 30-day return \# ── expanding() — grows from start (cumulative) prices.expanding().mean()             \# expanding mean (all-time) prices.expanding(min\_periods=5).std() \# require 5 periods minimum \# ── ewm() — exponentially weighted (recent \= more weight) prices.ewm(span=12).mean()            \# EWMA with span 12 prices.ewm(alpha=0.3).mean()          \# explicit alpha (0-1) prices.ewm(halflife=6).mean()         \# half-life in periods prices.ewm(com=5).var()               \# using center of mass \# ── Scenario: full financial analysis pipeline analysis \= pd.DataFrame({     'price':   prices,     'ma7':     prices.rolling(7).mean(),     'ma30':    prices.rolling(30).mean(),     'ma90':    prices.rolling(90).mean(),     'ewma12':  prices.ewm(span=12).mean(),     'vol30':   prices.rolling(30).std(),     'ret1d':   prices.pct\_change(1),     'ret5d':   prices.pct\_change(5),     'ret30d':  prices.pct\_change(30),     'hi52w':   prices.rolling(252).max(),     'lo52w':   prices.rolling(252).min(),     'rsi14':   prices.rolling(14).apply(lambda x:                    100-100/(1+(x\[x\>0\].mean()/((-x\[x\<0\]).mean()+1e-9))),raw=False) }) |
| :---: | :---- |

 

# **Chapter 10 — Input / Output — All Formats**

| CSV · Excel · JSON · Parquet · SQL · HDF5 · Feather · Clipboard |
| :---: |

 

*▲ Pandas I/O Architecture — All Read/Write Formats*

## **10.1  CSV**

| PYTHON | \# ── read\_csv — all key parameters df \= pd.read\_csv(     'data.csv',     sep=',',                    \# delimiter: ',' '\\t' '|' etc.     header=0,                   \# row number for column names (None \= no header)     names=\['a','b','c'\],        \# override column names     index\_col='id',             \# column(s) to use as index     usecols=\['name','salary'\],  \# load only these columns     dtype={'age':'int8','dept':'category'},  \# specify dtypes     parse\_dates=\['hire\_date'\],  \# parse as datetime     date\_format='%Y-%m-%d',     \# date format string     na\_values=\['NA','N/A','-'\], \# additional strings to treat as NaN     keep\_default\_na=True,       \# keep defaults like '' and 'NULL'     nrows=1000,                 \# read only first N rows     skiprows=\[0,1,3\],           \# skip specific rows     skipfooter=2,               \# skip last N rows     chunksize=50000,            \# read in chunks (returns iterator)     compression='gzip',         \# 'gzip','bz2','zip','xz','zstd'     encoding='utf-8',           \# file encoding     encoding\_errors='replace',  \# how to handle bad chars     thousands=',',              \# thousands separator     decimal='.',                \# decimal point char     quotechar='"',             \# quote character     escapechar='\\\\',          \# escape character     comment='\#',               \# skip lines starting with this     low\_memory=False,           \# don't infer dtype in chunks     memory\_map=True,            \# memory-map file for speed     engine='python',            \# 'c' (fast) or 'python' (flexible)     on\_bad\_lines='skip',        \# 'error','warn','skip' ) \# ── to\_csv df.to\_csv('output.csv',     sep=',',     index=False,                \# don't write row index     header=True,     columns=\['name','salary'\],  \# write only these columns     na\_rep='',                  \# NaN representation     float\_format='%.2f',        \# format floats     date\_format='%Y-%m-%d',     compression='gzip',     encoding='utf-8',     quoting=1,                  \# csv.QUOTE\_ALL \= 1     line\_terminator='\\n',     chunksize=10000,            \# write in chunks ) |
| :---: | :---- |

 

## **10.2  Excel**

| PYTHON | \# ── read\_excel df \= pd.read\_excel(     'data.xlsx',     sheet\_name='Sheet1',        \# or 0 (first), or None (all \-\> dict)     header=0,     index\_col=None,     usecols='A:D',              \# range string or list     dtype={'salary': float},     parse\_dates=\['hire\_date'\],     na\_values=\['N/A'\],     nrows=500,     skiprows=2,     engine='openpyxl',          \# 'openpyxl'(xlsx) 'xlrd'(xls) 'calamine' ) \# Read all sheets at once all\_sheets \= pd.read\_excel('data.xlsx', sheet\_name=None)  \# returns dict df\_sheet1 \= all\_sheets\['Sales'\] \# ── to\_excel df.to\_excel('output.xlsx', sheet\_name='Employees', index=False) \# Write multiple sheets with pd.ExcelWriter('report.xlsx', engine='openpyxl') as writer:     df\_sales.to\_excel(writer, sheet\_name='Sales', index=False)     df\_hr.to\_excel(writer, sheet\_name='HR', index=False)     \# formatting (with openpyxl)     ws \= writer.sheets\['Sales'\]     ws.column\_dimensions\['A'\].width \= 20 |
| :---: | :---- |

 

## **10.3  JSON, Parquet, SQL, HDF5 & Others**

| PYTHON | \# ── JSON df \= pd.read\_json('data.json') df \= pd.read\_json('data.json', orient='records')   \# \[{col:val,...}\] df \= pd.read\_json('data.json', orient='columns')   \# {col:{idx:val}} df \= pd.read\_json('data.json', orient='index')     \# {idx:{col:val}} df \= pd.read\_json('data.json', orient='split')     \# {columns,index,data} df \= pd.read\_json('data.json', lines=True)         \# JSON Lines (NDJSON) df \= pd.read\_json('data.json', dtype={'age':'int8'}) df \= pd.read\_json('https://api.example.com/data')  \# URL support df.to\_json('output.json', orient='records', lines=True, date\_format='iso') \# ── Parquet (recommended for analytics) df \= pd.read\_parquet('data.parquet', engine='pyarrow') df \= pd.read\_parquet('data.parquet', columns=\['name','salary'\]) df \= pd.read\_parquet('s3://bucket/data/', storage\_options={...}) df.to\_parquet('output.parquet', engine='pyarrow', compression='snappy', index=False) \# ── Feather (fastest for inter-process, not long-term storage) df \= pd.read\_feather('data.feather') df.to\_feather('output.feather') \# ── SQL (via SQLAlchemy) from sqlalchemy import create\_engine engine \= create\_engine('postgresql://user:pw@host:5432/db') df \= pd.read\_sql('SELECT \* FROM employees WHERE salary \> 80000', con=engine) df \= pd.read\_sql\_table('employees', con=engine) df \= pd.read\_sql\_query('SELECT \* FROM emp', con=engine, index\_col='id',                          parse\_dates=\['hire\_date'\], chunksize=10000) df.to\_sql('employees\_clean', con=engine, if\_exists='replace', index=False,           chunksize=1000, method='multi') \# ── HDF5 / PyTables df.to\_hdf('data.h5', key='employees', mode='w', format='table') df \= pd.read\_hdf('data.h5', key='employees', where='salary \> 80000') \# ── Other formats pd.read\_clipboard()               \# from clipboard df.to\_clipboard(index=False) pd.read\_html('https://...')       \# parse HTML tables (returns list) df.to\_html('output.html') pd.read\_xml('data.xml')           \# XML (Pandas 1.3+) df.to\_xml('output.xml') pd.read\_orc('data.orc')           \# ORC format pd.read\_spss('data.sav')          \# SPSS pd.read\_stata('data.dta')         \# Stata pd.read\_sas('data.sas7bdat')      \# SAS pd.read\_pickle('data.pkl')        \# Python pickle df.to\_pickle('output.pkl') |
| :---: | :---- |

 

# **Chapter 11 — Statistical & Numeric Methods**

| Descriptive Stats · Correlation · Sampling · Window · Rank · Numeric Ops |
| :---: |

 

## **11.1  Descriptive Statistics — Full Reference**

| Method | Returns | Description |
| :---- | :---- | :---- |
| df.describe() | DataFrame | count, mean, std, min, 25%, 50%, 75%, max |
| df.describe(include='all') | DataFrame | Includes object/category columns |
| df.mean() | Series | Column means (numeric) |
| df.median() | Series | Column medians |
| df.mode() | DataFrame | Most frequent value(s) |
| df.std() | Series | Sample standard deviation |
| df.var() | Series | Sample variance |
| df.sem() | Series | Standard error of mean |
| df.skew() | Series | Skewness (asymmetry) |
| df.kurtosis() | Series | Kurtosis (tail weight) |
| df.min() | Series | Column minimums |
| df.max() | Series | Column maximums |
| df.sum() | Series | Column sums |
| df.prod() | Series | Column products |
| df.cumsum() | DataFrame | Cumulative sum |
| df.cumprod() | DataFrame | Cumulative product |
| df.cummax() | DataFrame | Cumulative maximum |
| df.cummin() | DataFrame | Cumulative minimum |
| df.count() | Series | Non-null count per column |
| df.nunique() | Series | Unique value count per column |
| df.value\_counts() | Series | Frequency of unique values |
| df.abs() | DataFrame | Absolute values |
| df.round(2) | DataFrame | Round to N decimals |
| df.clip(lower,upper) | DataFrame | Clip values to range |
| df.quantile(0.75) | Series | 75th percentile |
| df.quantile(\[.25,.5,.75\]) | DataFrame | Multiple percentiles |
| df.pct\_change() | DataFrame | % change from prior row |
| df.diff() | DataFrame | Absolute diff from prior row |
| df.rank() | DataFrame | Rank of values |
| df.corr() | DataFrame | Pearson correlation matrix |
| df.cov() | DataFrame | Covariance matrix |
| df.autocorr(lag=1) | float | Autocorrelation at lag |

 

| PYTHON | import pandas as pd import numpy as np df \= pd.DataFrame({     'salary': \[95000,72000,110000,68000,88000,105000\],     'age':    \[34,28,45,31,29,52\],     'score':  \[8.5,6.2,9.1,5.8,7.7,8.9\] }) \# Correlation matrix corr \= df.corr()                      \# Pearson (default) corr \= df.corr(method='spearman')     \# Spearman rank corr \= df.corr(method='kendall')      \# Kendall tau \# Correlation with specific column df\['salary'\].corr(df\['age'\]) \# Statistical tests (use with scipy) from scipy import stats t\_stat, p\_val \= stats.ttest\_ind(df\['salary'\], df\['score'\]) \# Value counts with normalize df\['salary'\].value\_counts()                   \# absolute df\['salary'\].value\_counts(normalize=True)     \# relative frequency df\['salary'\].value\_counts(bins=5)             \# histogram bins df\['salary'\].value\_counts(dropna=False)       \# include NaN \# Quantile / percentile df\['salary'\].quantile(0.9)            \# 90th percentile df\['salary'\].quantile(\[.1,.25,.5,.75,.9\]) \# Binning pd.cut(df\['salary'\], bins=3)          \# 3 equal-width bins pd.cut(df\['salary'\], bins=\[0,70000,90000,200000\],        labels=\['Low','Mid','High'\]) pd.qcut(df\['salary'\], q=4)            \# 4 quantile-based bins pd.qcut(df\['salary'\], q=4, labels=\['Q1','Q2','Q3','Q4'\]) |
| :---: | :---- |

 

## **11.2  Random Sampling & Shuffling**

| PYTHON | \# ── Random sample df.sample(n=3)                        \# 3 random rows df.sample(frac=0.2)                   \# 20% of rows df.sample(n=3, replace=True)          \# with replacement df.sample(n=3, random\_state=42)       \# reproducible df.sample(n=3, weights='salary')      \# weighted by column df.sample(frac=1, random\_state=42)    \# full shuffle \# ── Train/test split train \= df.sample(frac=0.8, random\_state=42) test  \= df.drop(train.index) \# ── Stratified sample from sklearn.model\_selection import train\_test\_split train, test \= train\_test\_split(df, test\_size=0.2, stratify=df\['dept'\]) |
| :---: | :---- |

 

# **Chapter 12 — Visualization with Pandas**

| Built-in Plots · Matplotlib Integration · Plotly/Seaborn |
| :---: |

 

## **12.1  Built-in Plotting (df.plot)**

| PYTHON | import pandas as pd import numpy as np import matplotlib.pyplot as plt df \= pd.DataFrame({     'salary': \[95000,72000,110000,68000,88000\],     'age':    \[34,28,45,31,29\],     'name':   \['Alice','Bob','Carol','Dave','Eve'\] }) \# ── Line plot (default) df\['salary'\].plot()                   \# simple line df\[\['salary','age'\]\].plot()           \# multiple lines df.plot(x='name', y='salary')         \# specify x,y \# ── Bar charts df.plot.bar(x='name', y='salary')             \# vertical bars df.plot.barh(x='name', y='salary')            \# horizontal bars df.plot.bar(stacked=True)                     \# stacked bars \# ── Histogram df\['salary'\].plot.hist(bins=20) df.plot.hist(bins=10, alpha=0.7)      \# overlapping histograms df\['salary'\].hist(by=df\['dept'\])      \# grouped histograms \# ── Box plot df.plot.box() df.boxplot(column='salary', by='dept') \# ── Scatter plot df.plot.scatter(x='age', y='salary') df.plot.scatter(x='age', y='salary', c='salary', colormap='viridis', s=50) \# ── KDE (Kernel Density Estimate) df\['salary'\].plot.kde() df\['salary'\].plot.density()           \# alias \# ── Pie chart df.set\_index('name')\['salary'\].plot.pie(autopct='%1.1f%%') \# ── Area chart df\['salary'\].plot.area(alpha=0.5) \# ── Hexbin (2D density) df.plot.hexbin(x='age', y='salary', gridsize=20) \# ── All plot options df.plot(     kind='bar',            \# 'line','bar','barh','hist','box','kde',                            \# 'density','area','pie','scatter','hexbin'     figsize=(12, 6),       \# figure size in inches     title='Employee Data', \# plot title     xlabel='Employee',     \# x-axis label     ylabel='Salary',       \# y-axis label     legend=True,           \# show legend     grid=True,             \# show grid     color='steelblue',     \# or list of colors     alpha=0.8,             \# transparency     fontsize=12,           \# label font size     rot=45,                \# x-tick rotation     logx=False,            \# log scale on x     logy=False,            \# log scale on y     xlim=(0,100),          \# x-axis limits     ylim=(0,200000),       \# y-axis limits     table=False,           \# show data table     style='--o',           \# matplotlib line style     secondary\_y=False,     \# secondary y-axis     mark\_right=True,       \# label secondary axis ) plt.tight\_layout() plt.savefig('plot.png', dpi=150, bbox\_inches='tight') plt.show() |
| :---: | :---- |

 

## **12.2  Seaborn Integration (Scenario-Based)**

| PYTHON | import seaborn as sns \# ── EDA scenario: distribution analysis fig, axes \= plt.subplots(2, 2, figsize=(12, 10)) sns.histplot(df\['salary'\], kde=True, ax=axes\[0,0\]) sns.boxplot(x='dept', y='salary', data=df, ax=axes\[0,1\]) sns.scatterplot(x='age', y='salary', hue='dept', data=df, ax=axes\[1,0\]) sns.heatmap(df.corr(), annot=True, fmt='.2f', cmap='coolwarm', ax=axes\[1,1\]) plt.tight\_layout() \# ── Pairplot for correlation overview sns.pairplot(df\[\['salary','age','score'\]\], diag\_kind='kde') \# ── Violin plot sns.violinplot(x='dept', y='salary', data=df, inner='quart') \# ── Categorical plot sns.catplot(x='dept', y='salary', kind='box', data=df, height=5) |
| :---: | :---- |

 

# **Chapter 13 — Performance & Best Practices**

| Vectorization · eval/query · Profiling · Anti-patterns · Production Tips |
| :---: |

 

*▲ Pandas vs Modern Alternatives — When to Use What*

## **13.1  Vectorization vs Loops**

| PYTHON | import pandas as pd import numpy as np import time df \= pd.DataFrame({'salary': np.random.randint(50000, 150000, 100000)}) \# ── BAD: Python loop (never do this) start \= time.time() result \= \[\] for i in range(len(df)):     result.append(df.iloc\[i\]\['salary'\] \* 1.1) print(f'Loop: {time.time()-start:.2f}s')  \# \~8 seconds for 100k rows \# ── BETTER: apply (still slow for numeric) start \= time.time() df\['raised'\] \= df\['salary'\].apply(lambda x: x \* 1.1) print(f'Apply: {time.time()-start:.2f}s')  \# \~0.2 seconds \# ── BEST: vectorized NumPy operation start \= time.time() df\['raised'\] \= df\['salary'\] \* 1.1 print(f'Vectorized: {time.time()-start:.4f}s')  \# \~0.002 seconds — 100x faster\! \# ── Best: use built-in methods whenever possible df\['salary'\].sum()                \# NOT df\['salary'\].apply(sum) df\['salary'\].mean()               \# NOT df\['salary'\].apply(np.mean) df\['dept'\].str.upper()            \# NOT df\['dept'\].apply(str.upper) pd.to\_datetime(df\['date'\])        \# NOT df\['date'\].apply(pd.Timestamp) df\['salary'\].clip(0, 200000\)      \# NOT df\['salary'\].apply(lambda x: min(max(x,0),200000)) |
| :---: | :---- |

 

## **13.2  eval() and query() for Large DataFrames**

| PYTHON | \# eval() and query() use numexpr — faster on large DataFrames \# and avoid creating intermediate arrays \# ── query() — filter with string expression df.query('salary \> 80000 and age \< 40')           \# cleaner than boolean index df.query('dept \== "Engineering"')                 \# double quotes inside df.query('salary \> @min\_salary')                  \# reference variable with @ df.query('index \> 100')                            \# filter on index \# ── eval() — compute new column expressions df.eval('total \= salary \+ salary \* 0.15')          \# adds 'total' column df.eval('z\_score \= (salary \- salary.mean()) / salary.std()', inplace=True) \# Multi-line eval df.eval('''     bonus     \= salary \* 0.10     total     \= salary \+ bonus     tax       \= total \* 0.30     net       \= total \- tax ''', inplace=True) \# ── eval with local variables mean\_sal \= df\['salary'\].mean() df.eval('above\_avg \= salary \> @mean\_sal', inplace=True) |
| :---: | :---- |

 

## **13.3  Production Best Practices**

| Rule | Bad Practice | Good Practice |
| :---- | :---- | :---- |
| Avoid loops on rows | for i, row in df.iterrows() | Use vectorized ops, apply, or transform |
| Choose right dtype | All columns as float64/object | int8/category/string for memory savings |
| Use method chaining | temp1 \= ...; temp2 \= ...; temp3 \= ... | result \= df.pipe().query().assign().groupby() |
| Copy when needed | df\_slice\['col'\] \= 0  (may warn) | df.loc\[condition, 'col'\] \= 0 |
| Use inplace sparingly | df.sort\_values(inplace=True) | df \= df.sort\_values() (clearer) |
| Specify dtypes on read | pd.read\_csv('f.csv') | pd.read\_csv('f.csv', dtype={...}) |
| Filter early | Read all then filter | Use usecols, nrows, query on read |
| Prefer built-in aggregations | apply(np.mean) on groupby | groupby().mean() — uses optimized C |
| Use categorical for strings | 'Engineering' as object 100k times | astype('category') — stores once |
| Use Parquet not CSV | Save as .csv for sharing | Save as .parquet for pipelines |

## **13.4  Common Real-World Scenarios**

| PYTHON | \# ── Scenario 1: Clean a messy CSV import df \= pd.read\_csv('messy.csv') df.columns \= df.columns.str.strip().str.lower().str.replace(' ','\_') df \= df.replace({'': np.nan, 'NULL': np.nan, 'N/A': np.nan}) df \= df.dropna(subset=\['id','name'\])  \# require key columns df\['salary'\] \= pd.to\_numeric(df\['salary'\], errors='coerce') df\['hire\_date'\] \= pd.to\_datetime(df\['hire\_date'\], errors='coerce') df\['dept'\] \= df\['dept'\].astype('category') df \= df.drop\_duplicates(subset=\['id'\]) df \= df.reset\_index(drop=True) \# ── Scenario 2: Daily report aggregation daily \= (df     .groupby(\[df\['date'\].dt.date, 'dept'\])     .agg(         total\_sales   \= ('amount',   'sum'),         num\_orders    \= ('order\_id', 'count'),         avg\_order\_val \= ('amount',   'mean'),         unique\_cust   \= ('cust\_id',  'nunique')     )     .reset\_index()     .sort\_values(\['date','total\_sales'\], ascending=\[True,False\]) ) \# ── Scenario 3: Feature engineering for ML df\['salary\_log'\]     \= np.log1p(df\['salary'\]) df\['age\_sq'\]         \= df\['age'\] \*\* 2 df\['tenure\_months'\]  \= (pd.Timestamp.now() \- df\['hire\_date'\]).dt.days // 30 df\['salary\_pctile'\]  \= df\['salary'\].rank(pct=True) df\['dept\_avg\_sal'\]   \= df.groupby('dept')\['salary'\].transform('mean') df\['sal\_vs\_dept\_avg'\]= df\['salary'\] \- df\['dept\_avg\_sal'\] \# One-hot encode categoricals df\_encoded \= pd.get\_dummies(df, columns=\['dept'\], drop\_first=True, dtype=int) \# ── Scenario 4: Time series forecast prep ts \= df.set\_index('date').sort\_index() ts\['lag\_1'\]    \= ts\['sales'\].shift(1) ts\['lag\_7'\]    \= ts\['sales'\].shift(7) ts\['ma\_7'\]     \= ts\['sales'\].rolling(7).mean() ts\['ma\_30'\]    \= ts\['sales'\].rolling(30).mean() ts\['day\_of\_wk'\]= ts.index.dayofweek ts\['is\_wkend'\] \= ts.index.dayofweek \>= 5 ts\['month'\]    \= ts.index.month ts\['year'\]     \= ts.index.year ts \= ts.dropna()  \# remove NaN rows from rolling/lag |
| :---: | :---- |

 

# **Chapter 14 — Quick Reference Cards**

| At-a-Glance Reference — All Methods, Attributes & Config |
| :---: |

 

## **14.1  Complete DataFrame Method Quick Reference**

| Method | Description | Example |
| :---- | :---- | :---- |
| pd.DataFrame() | Create from dict/list/array | pd.DataFrame({'a':\[1,2\],'b':\[3,4\]}) |
| pd.read\_csv() | Read CSV file | pd.read\_csv('f.csv', dtype={'age':'int8'}) |
| pd.read\_excel() | Read Excel file | pd.read\_excel('f.xlsx', sheet\_name=0) |
| pd.read\_parquet() | Read Parquet | pd.read\_parquet('f.parquet') |
| pd.read\_json() | Read JSON | pd.read\_json('f.json', orient='records') |
| pd.read\_sql() | Read from DB | pd.read\_sql(query, con=engine) |
| pd.read\_html() | Parse HTML tables | pd.read\_html('https://...')\[0\] |
| pd.concat() | Stack DataFrames | pd.concat(\[df1,df2\], ignore\_index=True) |
| pd.merge() | Join two DataFrames | pd.merge(df1,df2,on='key',how='left') |
| pd.get\_dummies() | One-hot encode | pd.get\_dummies(df, columns=\['dept'\]) |
| pd.cut() | Equal-width bins | pd.cut(df\['age'\], bins=4) |
| pd.qcut() | Quantile-based bins | pd.qcut(df\['sal'\], q=4, labels=\['Q1','Q4'\]) |
| pd.to\_datetime() | Parse dates | pd.to\_datetime(df\['dt'\], errors='coerce') |
| pd.to\_numeric() | Parse numbers | pd.to\_numeric(df\['sal'\], errors='coerce') |
| pd.isna() | Check nulls | pd.isna(df\['col'\]) |
| pd.notna() | Check non-nulls | pd.notna(df\['col'\]) |
| df.head(n) | First n rows | df.head(10) |
| df.tail(n) | Last n rows | df.tail(5) |
| df.sample(n) | Random sample | df.sample(100, random\_state=42) |
| df.info() | Schema \+ memory | df.info(memory\_usage='deep') |
| df.describe() | Summary statistics | df.describe(include='all') |
| df.shape | (rows, cols) tuple | print(df.shape) |
| df.columns | Column names | df.columns.tolist() |
| df.dtypes | Column dtypes | df.dtypes |
| df.index | Row index | df.index |
| df.values | NumPy array | df.values |
| df.to\_numpy() | NumPy array (preferred) | df.to\_numpy() |
| df.select\_dtypes() | Filter by dtype | df.select\_dtypes(include='number') |
| df.memory\_usage() | Bytes per column | df.memory\_usage(deep=True) |
| df.copy() | Deep copy | df2 \= df.copy() |
| df.loc\[\] | Label-based access | df.loc\[df\['sal'\]\>80000,'name'\] |
| df.iloc\[\] | Position-based | df.iloc\[0:5, 0:3\] |
| df.at\[\] | Fast scalar by label | df.at\['r0','salary'\] |
| df.iat\[\] | Fast scalar by pos | df.iat\[0, 2\] |
| df.filter() | Select cols by pattern | df.filter(like='salary') |
| df.query() | SQL-like filter | df.query('age\>30 and dept=="Eng"') |
| df.where() | Keep if True | df\['sal'\].where(df\['sal'\]\>0) |
| df.mask() | Replace if True | df\['sal'\].mask(df\['sal'\]\>100000,100000) |
| df.assign() | Add columns (chainable) | df.assign(bonus=lambda x:x.sal\*0.1) |
| df.drop() | Remove rows/cols | df.drop(columns=\['tmp'\]) |
| df.rename() | Rename cols/index | df.rename(columns={'old':'new'}) |
| df.reindex() | Conform to new index | df.reindex(columns=\['a','b','c'\]) |
| df.set\_index() | Column to index | df.set\_index('name') |
| df.reset\_index() | Index to column | df.reset\_index(drop=True) |
| df.sort\_values() | Sort by column | df.sort\_values('sal',ascending=False) |
| df.sort\_index() | Sort by index | df.sort\_index() |
| df.nlargest() | Top N rows | df.nlargest(5,'salary') |
| df.nsmallest() | Bottom N rows | df.nsmallest(3,'age') |
| df.groupby() | Group for agg | df.groupby('dept').agg(n=('id','count')) |
| df.pivot\_table() | Excel-style pivot | df.pivot\_table('sal','dept','active','mean') |
| df.pivot() | Reshape without agg | df.pivot('name','metric','value') |
| df.melt() | Wide to long | pd.melt(df, id\_vars=\['name'\], var\_name='q') |
| df.stack() | Columns to rows | df.stack() |
| df.unstack() | Rows to columns | df.unstack(level=0) |
| df.merge() | Join (instance method) | df1.merge(df2, on='key', how='inner') |
| df.join() | Index-based join | df1.join(df2, how='left') |
| df.append() (dep.) | Add rows (use concat) | pd.concat(\[df,new\_row.T\]) |
| df.apply() | Apply function | df.apply(np.mean, axis=0) |
| df.applymap()/map() | Element-wise func | df.map(lambda x: x\*2) |
| df.transform() | Same-shape apply | df.groupby('dept')\['sal'\].transform('mean') |
| df.pipe() | Chainable transform | df.pipe(my\_func).pipe(another) |
| df.fillna() | Fill missing values | df.fillna({'sal':0,'name':'Unk'}) |
| df.dropna() | Drop missing rows | df.dropna(subset=\['name','salary'\]) |
| df.replace() | Replace values | df.replace(np.nan, 0\) |
| df.interpolate() | Estimate missing | df\['sal'\].interpolate(method='linear') |
| df.ffill() | Forward fill | df.ffill() |
| df.bfill() | Backward fill | df.bfill() |
| df.astype() | Change dtypes | df.astype({'age':'int8','dept':'category'}) |
| df.convert\_dtypes() | Best dtypes auto | df.convert\_dtypes() |
| df.infer\_objects() | Infer better types | df.infer\_objects() |
| df.duplicated() | Find duplicates | df\[df.duplicated(subset=\['name'\])\] |
| df.drop\_duplicates() | Remove duplicates | df.drop\_duplicates(subset=\['emp\_id'\]) |
| df.isna() / isnull() | Null mask | df.isna().sum() |
| df.notna() / notnull() | Not-null mask | df.notna().all() |
| df.nunique() | Unique count | df.nunique() |
| df.value\_counts() | Freq per value | df\['dept'\].value\_counts(normalize=True) |
| df.corr() | Correlation matrix | df.corr(method='pearson') |
| df.cov() | Covariance matrix | df.cov() |
| df.mean() | Mean | df\['salary'\].mean() |
| df.median() | Median | df\['salary'\].median() |
| df.mode() | Mode | df\['salary'\].mode()\[0\] |
| df.std() | Std deviation | df\['salary'\].std() |
| df.var() | Variance | df\['salary'\].var() |
| df.sum() | Sum | df\['salary'\].sum() |
| df.min() / max() | Min/max | df\['salary'\].min() |
| df.cumsum() | Cumulative sum | df\['sales'\].cumsum() |
| df.cumprod() | Cumulative product | df\['growth'\].cumprod() |
| df.pct\_change() | % change | df\['price'\].pct\_change() |
| df.diff() | Absolute diff | df\['price'\].diff() |
| df.rank() | Rank values | df\['salary'\].rank(method='dense') |
| df.clip() | Clip to range | df\['salary'\].clip(50000, 200000\) |
| df.abs() | Absolute value | df\['return'\].abs() |
| df.round() | Round numbers | df.round({'salary':0,'score':2}) |
| df.T | Transpose | df.T |
| df.equals() | Equality check | df1.equals(df2) |
| df.compare() | Show differences | df1.compare(df2) |
| df.combine\_first() | Fill from other | df1.combine\_first(df2) |
| df.update() | Update in place | df1.update(df2) |
| df.eval() | Evaluate expression | df.eval('total=sal+bonus',inplace=True) |
| df.to\_csv() | Write CSV | df.to\_csv('out.csv',index=False) |
| df.to\_excel() | Write Excel | df.to\_excel('out.xlsx',index=False) |
| df.to\_parquet() | Write Parquet | df.to\_parquet('out.parquet') |
| df.to\_json() | Write JSON | df.to\_json('out.json',orient='records') |
| df.to\_sql() | Write to DB | df.to\_sql('tbl',engine,if\_exists='replace') |
| df.to\_html() | Write HTML | df.to\_html('report.html') |
| df.to\_dict() | Convert to dict | df.to\_dict(orient='records') |
| df.to\_list() | Series to list | df\['name'\].to\_list() |
| df.to\_frame() | Series to DF | series.to\_frame('salary') |
| df.to\_records() | To numpy recarray | df.to\_records(index=False) |
| df.plot() | Plot (wraps mpl) | df\['sal'\].plot.hist(bins=20) |
| df.boxplot() | Box plot | df.boxplot(column='sal',by='dept') |
| df.hist() | Histogram | df.hist(bins=20, figsize=(12,8)) |
| df.resample() | Time-based groupby | df.resample('ME').mean() |
| df.rolling() | Rolling window | df\['price'\].rolling(30).mean() |
| df.expanding() | Expanding window | df\['sales'\].expanding().sum() |
| df.ewm() | Exponential weighting | df\['price'\].ewm(span=12).mean() |
| df.shift() | Shift values | df\['price'\].shift(1) |
| df.diff() | Difference | df\['price'\].diff(1) |

# **Chapter 15 — apply · map · transform · pipe — Deep Dive**

| Element-wise · Row/Col-wise · Group-wise · Chaining |
| :---: |

 

*▲ apply / map / transform / pipe — Execution Model & When to Use Each*

## **15.1  Series.map() — Element-wise Replacement**

map() is Series-only and the fastest way to replace values using a dictionary, another Series, or a function. It is ideal for lookups and simple transformations.

| PYTHON | import pandas as pd import numpy as np df \= pd.DataFrame({     'name':   \['Alice','Bob','Carol','Dave','Eve'\],     'dept':   \['Eng','Mkt','Eng','Mkt','HR'\],     'salary': \[95000,72000,110000,68000,88000\],     'grade':  \['A','C','A','B','B'\] }) \# ── Map with dictionary (fastest lookup pattern) dept\_map \= {'Eng':'Engineering','Mkt':'Marketing','HR':'Human Resources'} df\['dept\_full'\] \= df\['dept'\].map(dept\_map)          \# NaN if key missing \# ── Map with function df\['name\_len'\]   \= df\['name'\].map(len) df\['name\_lower'\] \= df\['name'\].map(str.lower) df\['salary\_k'\]   \= df\['salary'\].map(lambda x: f'{x/1000:.0f}k') \# ── Map with Series (aligns on index) bonus\_map \= pd.Series({'Eng':0.15,'Mkt':0.10,'HR':0.12}) df\['bonus\_rate'\] \= df\['dept'\].map(bonus\_map) \# ── na\_action — skip NaN values df\['dept'\].map(str.upper, na\_action='ignore')       \# skip NaN, don't apply \# ── Handle missing keys df\['dept\_full'\] \= df\['dept'\].map(dept\_map).fillna(df\['dept'\])  \# keep original if no match |
| :---: | :---- |

 

| OUTPUT |    name dept  salary grade dept\_full  name\_len  salary\_k  bonus\_rate 0 Alice  Eng   95000     A  Engineering       5       95k        0.15 1   Bob  Mkt   72000     C    Marketing       3       72k        0.10 2 Carol  Eng  110000     A  Engineering       5      110k        0.15 3  Dave  Mkt   68000     B    Marketing       4       68k        0.10 4   Eve   HR   88000     B  Human Resources  3       88k        0.12 |
| :---: | :---- |

 

## **15.2  Series.apply() — Flexible Element-wise**

| PYTHON | \# ── Basic apply with function df\['level'\] \= df\['salary'\].apply(lambda x:     'Principal' if x \>= 100000 else     'Senior'    if x \>= 85000 else     'Mid'       if x \>= 70000 else 'Junior') \# ── apply with extra arguments def categorize(value, low, high, labels):     if value \< low:   return labels\[0\]     if value \< high:  return labels\[1\]     return labels\[2\] df\['salary'\].apply(categorize, args=(70000, 90000, \['Junior','Mid','Senior'\])) \# ── apply returning Series (creates DataFrame) def salary\_stats(salary):     return pd.Series({         'monthly': salary / 12,         'daily':   salary / 252,         'bonus':   salary \* 0.15     }) \# Each call returns a Series → result is DataFrame salary\_breakdown \= df\['salary'\].apply(salary\_stats) print(salary\_breakdown) \# ── convert\_dtypes works better for simple conversions df\['salary'\].astype(float)             \# better than df\['salary'\].apply(float) df\['name'\].str.upper()                 \# better than df\['name'\].apply(str.upper) |
| :---: | :---- |

 

## **15.3  DataFrame.apply() — Row-wise and Column-wise**

| PYTHON | \# ── axis=0 (default): function called ONCE PER COLUMN \# Input: a column as Series. Use for column-level summaries. df\[\['salary','name\_len'\]\].apply(np.mean, axis=0)    \# mean of each column df\[\['salary','name\_len'\]\].apply(lambda s: s.max() \- s.min())  \# range per col \# ── axis=1: function called ONCE PER ROW \# Input: a row as Series. Use for row-level derived features. df\['summary'\] \= df.apply(     lambda row: f"{row\['name'\]} \[{row\['dept'\]}\] ${row\['salary'\]:,}",     axis=1 ) \# ── result\_type parameter (axis=1 only) \# 'expand' → splits returned list/tuple into columns def parse\_name(row):     return \[row\['name'\].upper(), len(row\['name'\])\] df\[\['NAME\_UPPER','NAME\_LEN'\]\] \= df.apply(parse\_name, axis=1, result\_type='expand') \# 'reduce' → always returns a Series \# 'broadcast' → returns same shape as input \# ── apply on specific columns df\[\['salary','name\_len'\]\].apply(lambda x: (x \- x.mean()) / x.std()) \# ── raw=True for speed (passes numpy array, not Series) df\['salary'\].apply(lambda arr: arr \* 1.1, raw=True)  \# 3-5x faster |
| :---: | :---- |

 

## **15.4  DataFrame.map() — Cell-wise**

| PYTHON | \# DataFrame.map() — called on EVERY SINGLE CELL \# Renamed from applymap() in Pandas 2.1 \# ── Format all numbers df\[\['salary','name\_len'\]\].map(lambda x: f'{x:,.0f}') \# ── Type check every cell df.map(type)                         \# dtype of every cell df.map(lambda x: isinstance(x, str))  \# bool mask where string \# ── Clip with custom function df\[\['salary'\]\].map(lambda x: min(max(x, 50000), 200000)) \# ── na\_action parameter df.map(str.upper, na\_action='ignore')  \# skip NaN cells \# IMPORTANT: For numeric ops, prefer vectorized: \# BAD:  df\[\['salary'\]\].map(lambda x: x \* 1.1) \# GOOD: df\[\['salary'\]\] \* 1.1                    \# 100x faster |
| :---: | :---- |

 

## **15.5  pipe() — The Chainable Pattern**

| PYTHON | import pandas as pd import numpy as np \# ── Define composable pipeline functions def clean\_columns(df):     df \= df.copy()     df.columns \= df.columns.str.strip().str.lower().str.replace(' ','\_')     return df def drop\_nulls(df, subset=None):     return df.dropna(subset=subset).reset\_index(drop=True) def add\_features(df):     df \= df.copy()     df\['salary\_k'\]    \= df\['salary'\] / 1000     df\['dept\_avg\_sal'\]= df.groupby('dept')\['salary'\].transform('mean')     df\['z\_score'\]     \= df.groupby('dept')\['salary'\].transform(         lambda x: (x \- x.mean()) / x.std())     return df def cast\_dtypes(df):     df \= df.copy()     df\['dept'\] \= df\['dept'\].astype('category')     df\['salary'\] \= pd.to\_numeric(df\['salary'\], errors='coerce')     return df def filter\_active(df, min\_salary=0):     return df\[df\['salary'\] \>= min\_salary\] \# ── Chain everything with pipe() result \= (df     .pipe(clean\_columns)     .pipe(drop\_nulls, subset=\['name', 'salary'\])     .pipe(cast\_dtypes)     .pipe(add\_features)     .pipe(filter\_active, min\_salary=70000)     .sort\_values('salary', ascending=False)     .reset\_index(drop=True) ) \# ── pipe with (func, arg) tuple syntax df.pipe((pd.merge, 'left'), right=dept\_df, on='dept') |
| :---: | :---- |

 

# **Chapter 16 — Advanced Reshaping & MultiIndex**

| MultiIndex · stack/unstack · pivot · melt · crosstab · cut/qcut |
| :---: |

 

*▲ Advanced Indexing — MultiIndex, stack/unstack, pivot, melt*

## **16.1  MultiIndex — Hierarchical Data**

| PYTHON | import pandas as pd import numpy as np \# ── Create MultiIndex \# From arrays arrays \= \[\['Eng','Eng','Mkt','Mkt'\], \['Alice','Bob','Carol','Dave'\]\] mi \= pd.MultiIndex.from\_arrays(arrays, names=\['dept','name'\]) \# From tuples mi2 \= pd.MultiIndex.from\_tuples(\[('Eng','Alice'),('Mkt','Bob')\],                                   names=\['dept','name'\]) \# From product (all combinations) mi3 \= pd.MultiIndex.from\_product(     \[\['2022','2023'\], \['Q1','Q2','Q3','Q4'\]\],     names=\['year','quarter'\] ) \# From existing DataFrame columns mi4 \= pd.MultiIndex.from\_frame(df\[\['dept','name'\]\]) \# ── Create DataFrame with MultiIndex df\_mi \= pd.DataFrame({     'salary': \[95000, 72000, 110000, 68000\],     'bonus':  \[9500,  7200,  11000,  6800\] }, index=mi) \# ── MultiIndex access patterns df\_mi.loc\['Eng'\]                          \# all Engineering rows df\_mi.loc\[('Eng','Alice')\]                \# single row by tuple df\_mi.loc\['Eng','Alice'\]                  \# same, without tuple df\_mi.loc\[\['Eng','Mkt'\]\]                  \# multiple level-0 values df\_mi.loc\['Eng':'Mkt'\]                    \# slice on level-0 \# xs — cross-section (cleanest for inner levels) df\_mi.xs('Alice', level='name')           \# get all Alice rows df\_mi.xs(('Eng','Alice'), level=(0,1))    \# tuple for multiple levels \# ── Modifying MultiIndex df\_mi.reset\_index()                       \# MultiIndex \-\> regular columns df\_mi.reset\_index(level='dept')           \# only reset outer level df\_mi.reset\_index(level=0, drop=True)     \# drop outer level df\_mi.swaplevel('dept','name')            \# swap level order df\_mi.sort\_index()                        \# lexicographic sort df\_mi.sort\_index(level='name')            \# sort by specific level df\_mi.droplevel('dept')                   \# remove a level df\_mi.rename\_axis(\['Division','Employee'\])\# rename level names \# ── Operations that use MultiIndex df\_mi.groupby(level='dept').mean()        \# aggregate at level df\_mi.groupby(level=0).sum()              \# level by position df\_mi\['salary'\].unstack(level='name')     \# MultiIndex Series \-\> wide DF \# ── set\_index for MultiIndex creation from columns df.set\_index(\['dept','name'\])             \# set two columns as MultiIndex df.set\_index(\['dept','name'\],append=True) \# keep existing \+ add levels |
| :---: | :---- |

 

## **16.2  stack() and unstack() — Pivoting Levels**

| PYTHON | \# Setup: wide DataFrame df\_wide \= pd.DataFrame({     'Q1': \[100,200,150\], 'Q2': \[110,220,160\], 'Q3': \[120,230,170\] }, index=\['Alice','Bob','Carol'\]) print(df\_wide) \# ── stack() — columns become innermost row level df\_long \= df\_wide.stack()            \# MultiIndex: (name, quarter) print(df\_long) \# ── unstack() — innermost row level becomes columns df\_back \= df\_long.unstack()          \# back to wide df\_back \= df\_long.unstack(level=0)   \# different level \# ── stack with dropna df\_wide.stack(dropna=True)           \# default True: drop NaN df\_wide.stack(dropna=False)          \# keep NaN \# ── Scenario: reshape from wide survey to long survey \= pd.DataFrame({     'user\_id': \[1,2,3\],     'q1\_score': \[8,7,9\], 'q2\_score': \[6,8,7\], 'q3\_score': \[9,6,8\] }) long \= survey.set\_index('user\_id').stack().reset\_index() long.columns \= \['user\_id','question','score'\] print(long) |
| :---: | :---- |

 

## **16.3  pivot\_table & crosstab — Tabular Summaries**

| PYTHON | import pandas as pd df \= pd.DataFrame({     'dept':   \['Eng','Mkt','Eng','Mkt','HR','Eng'\],     'active': \[True,False,True,False,True,True\],     'salary': \[95000,72000,110000,68000,88000,105000\],     'years':  \[5,3,10,2,7,8\] }) \# ── pivot\_table — full options pt \= pd.pivot\_table(df,     values   \= 'salary',           \# column(s) to aggregate     index    \= 'dept',              \# rows     columns  \= 'active',            \# columns     aggfunc  \= 'mean',              \# or list: \['mean','count'\]     fill\_value \= 0,                 \# fill NaN in result     margins  \= True,                \# add All row/column     margins\_name \= 'Total',     observed \= True,                \# for Categorical: only observed combos     dropna   \= True ) print(pt) \# ── Multiple values \+ functions pd.pivot\_table(df,     values  \= \['salary','years'\],     index   \= 'dept',     columns \= 'active',     aggfunc \= {'salary':\['mean','max'\], 'years':'mean'} ) \# ── crosstab — frequency tables ct \= pd.crosstab(df\['dept'\], df\['active'\]) print(ct) \# Normalize — proportions pd.crosstab(df\['dept'\], df\['active'\], normalize='index')  \# row % pd.crosstab(df\['dept'\], df\['active'\], normalize='columns')\# col % pd.crosstab(df\['dept'\], df\['active'\], normalize='all')    \# grand total % \# crosstab with aggregation pd.crosstab(df\['dept'\], df\['active'\],     values=df\['salary'\], aggfunc='mean') \# crosstab with margins pd.crosstab(df\['dept'\], df\['active'\], margins=True, margins\_name='All') |
| :---: | :---- |

 

| OUTPUT | \# pivot\_table output: active        False     True dept Eng             NaN  103333.3 HR              NaN   88000.0 Mkt         70000.0       NaN Total       70000.0  100000.0 \# crosstab output: active  False  True dept Eng         0     3 HR          0     1 Mkt         2     0 |
| :---: | :---- |

 

## **16.4  melt() — Unpivot Wide to Long**

| PYTHON | \# melt() — the opposite of pivot df\_wide \= pd.DataFrame({     'name':  \['Alice','Bob','Carol'\],     'Q1\_sales': \[100,200,150\],     'Q2\_sales': \[110,220,160\],     'Q3\_sales': \[120,230,170\] }) \# Basic melt df\_long \= pd.melt(     df\_wide,     id\_vars    \= \['name'\],          \# keep as identifier column(s)     value\_vars \= \['Q1\_sales','Q2\_sales','Q3\_sales'\],  \# columns to melt     var\_name   \= 'quarter',         \# name for the variable column     value\_name \= 'sales'            \# name for the value column ) print(df\_long) \# ── pd.wide\_to\_long — smarter pattern-based melt \# When column names have a stub \+ number pattern df\_w2l \= pd.wide\_to\_long(     df\_wide.rename(columns={'name':'id'}),     stubnames  \= \['Q'\],             \# column stub     i          \= 'id',             \# identifier column     j          \= 'quarter',        \# new variable column     sep        \= '\_sales\_',        \# separator between stub and suffix     suffix     \= r'\\d+'           \# regex for suffix ) |
| :---: | :---- |

 

| OUTPUT |     name   quarter  sales 0  Alice  Q1\_sales    100 1    Bob  Q1\_sales    200 2  Carol  Q1\_sales    150 3  Alice  Q2\_sales    110 4    Bob  Q2\_sales    220 5  Carol  Q2\_sales    160 6  Alice  Q3\_sales    120 7    Bob  Q3\_sales    230 8  Carol  Q3\_sales    170 |
| :---: | :---- |

 

# **Chapter 17 — Numeric, Statistical & Window Methods**

| Full Arithmetic · Comparison · Reduction · Cumulative · Rolling · Expanding · EWM |
| :---: |

 

## **17.1  Arithmetic & Comparison Operators**

| PYTHON | import pandas as pd import numpy as np df \= pd.DataFrame({'a':\[1,2,3,4\], 'b':\[10,20,30,40\]}) s  \= pd.Series(\[1,2,3,4\]) \# ── Arithmetic (all support fill\_value for NaN) df \+ 10               \# scalar add df \* 2                \# scalar multiply df / 3                \# true division df // 3               \# floor division df % 3                \# modulo df \*\* 2               \# power \# Operator methods with fill\_value df.add(other\_df, fill\_value=0)    \# NaN \-\> 0 before op df.sub(other\_df, fill\_value=0) df.mul(other\_df, fill\_value=1) df.div(other\_df, fill\_value=1)    \# true div df.floordiv(other\_df) df.mod(other\_df) df.pow(other\_df) df.radd(other\_df)                 \# reverse add (other \+ df) df.rsub(other\_df) df.rmul(other\_df) df.rdiv(other\_df) \# ── Comparison operators df \> 2                \# boolean DataFrame df \>= 2 df \< 2 df \<= 2 df \== 2 df \!= 2 \# Methods df.eq(2)              \# \== element-wise df.ne(2)              \# \!= df.lt(2)              \# \< df.le(2)              \# \<= df.gt(2)              \# \> df.ge(2)              \# \>= \# ── Boolean operators (df \> 1\) & (df \< 4\)   \# AND (df \< 2\) | (df \> 3\)   \# OR \~(df \> 2\)             \# NOT (df \> 1).all()        \# all True per column (df \> 1).any()        \# any True per column (df \> 1).all(axis=1)  \# all True per row |
| :---: | :---- |

 

## **17.2  Reduction & Aggregation Methods — Full List**

| Method | axis | Description | Notes |
| :---- | :---- | :---- | :---- |
| sum(skipna=True) | 0/1 | Sum of values | skipna=True ignores NaN |
| prod(skipna=True) | 0/1 | Product of values | Can overflow for large floats |
| mean(skipna=True) | 0/1 | Arithmetic mean | Use numeric\_only=True for mixed |
| median(skipna=True) | 0/1 | 50th percentile |  |
| mode(dropna=True) | 0/1 | Most frequent value | Returns DataFrame (may have multi-mode) |
| min(skipna=True) | 0/1 | Minimum value | Works on strings too (alphabetical) |
| max(skipna=True) | 0/1 | Maximum value |  |
| std(ddof=1) | 0/1 | Sample std deviation | ddof=0 for population std |
| var(ddof=1) | 0/1 | Sample variance |  |
| sem(ddof=1) | 0/1 | Standard error of mean | std/sqrt(n) |
| skew() | 0/1 | Skewness (asymmetry) | Positive \= right tail |
| kurtosis() | 0/1 | Excess kurtosis | 0 \= normal distribution |
| count() | 0/1 | Non-null count |  |
| nunique() | 0/1 | Distinct value count | dropna=True by default |
| idxmin() | 0/1 | Index label of minimum |  |
| idxmax() | 0/1 | Index label of maximum |  |
| first\_valid\_index() | — | First non-null index | Series only |
| last\_valid\_index() | — | Last non-null index | Series only |
| quantile(q) | 0/1 | q-th quantile (0-1) | q can be list |
| describe() | — | Summary statistics | include='all' for object cols |

 

## 

## **17.3  Cumulative Methods**

| PYTHON | s \= pd.Series(\[1,2,np.nan,4,5\]) s.cumsum()                      \# cumulative sum   \[1,3,NaN,7,12\] s.cumsum(skipna=True)           \# default — NaN propagates then resumes s.cumprod()                     \# cumulative product s.cummax()                      \# running maximum s.cummin()                      \# running minimum \# DataFrame versions work column-wise by default (axis=0) df.cumsum()                     \# cumulative sum per column df.cumsum(axis=1)               \# cumulative sum per row \# Practical: cumulative returns daily\_returns \= prices.pct\_change().dropna() cumulative    \= (1 \+ daily\_returns).cumprod() \# Practical: running total with reset at group boundary df\['running\_dept\_payroll'\] \= df.groupby('dept')\['salary'\].cumsum() |
| :---: | :---- |

 

## **17.4  Rolling Window — Complete Reference**

| PYTHON | import pandas as pd import numpy as np prices \= pd.Series(\[100,102,101,105,108,107,110,109,112,115\],     index=pd.date\_range('2024-01', periods=10, freq='B')) \# ── Basic rolling prices.rolling(window=3).mean()        \# 3-period moving average prices.rolling(window=3).sum() prices.rolling(window=3).std() prices.rolling(window=3).var() prices.rolling(window=3).min() prices.rolling(window=3).max() prices.rolling(window=3).median() prices.rolling(window=3).skew() prices.rolling(window=3).kurt() prices.rolling(window=3).sem() prices.rolling(window=3).quantile(0.75) prices.rolling(window=3).count()       \# count of non-NaN in window \# ── Parameters prices.rolling(7, min\_periods=3)       \# require at least 3 valid values prices.rolling(7, center=True)         \# window is centered (not trailing) prices.rolling(7, closed='both')       \# include both endpoints prices.rolling(7, closed='left')       \# left endpoint only prices.rolling(7, closed='right')      \# right endpoint only (default) prices.rolling(7, closed='neither') \# ── Window types (weighted) prices.rolling(7, win\_type='gaussian').mean(std=1.0) prices.rolling(7, win\_type='triang').mean() prices.rolling(7, win\_type='blackman').mean() prices.rolling(7, win\_type='hamming').mean() prices.rolling(7, win\_type='bartlett').mean() prices.rolling(7, win\_type='parzen').mean() prices.rolling(7, win\_type='bohman').mean() prices.rolling(7, win\_type='blackmanharris').mean() prices.rolling(7, win\_type='nuttall').mean() prices.rolling(7, win\_type='barthann').mean() \# ── Rolling on time-based offset (DatetimeIndex required) prices.rolling('7D').mean()            \# 7 calendar days window prices.rolling('30D').std()            \# 30-day rolling std \# ── Rolling custom function prices.rolling(5).apply(lambda x: x\[-1\] \- x\[0\], raw=True)  \# 5-day change prices.rolling(5).apply(np.nanmean, raw=True)               \# with NaN handling \# ── Rolling correlation and covariance s1 \= pd.Series(\[1,2,3,4,5,6,7,8,9,10\]) s2 \= pd.Series(\[2,3,2,5,4,7,6,9,8,11\]) s1.rolling(5).corr(s2)               \# 5-period rolling correlation s1.rolling(5).cov(s2)                \# 5-period rolling covariance s1.rolling(5).corr()                 \# autocorrelation \# ── Rolling aggregate dict prices.rolling(5).agg(\['mean','std','min','max'\]) |
| :---: | :---- |

 

## **17.5  Expanding & EWM**

| PYTHON | \# ── expanding() — window grows from start (all-time cumulative) prices.expanding().mean()             \# all-time average prices.expanding(min\_periods=5).std() \# require 5+ values prices.expanding().max()              \# all-time high prices.expanding().apply(np.std, raw=True)   \# custom function \# ── ewm() — exponentially weighted (recent data matters more) \# Three ways to specify decay: prices.ewm(span=12).mean()            \# span s: alpha \= 2/(s+1) prices.ewm(alpha=0.1).mean()          \# direct alpha (0 \< alpha \<= 1\) prices.ewm(halflife=6).mean()         \# half-life in periods prices.ewm(com=10).mean()             \# center-of-mass: alpha \= 1/(1+com) \# ── EWM parameters prices.ewm(span=12, min\_periods=3).mean()  \# require 3 observations prices.ewm(span=12, adjust=True).mean()    \# adjusted (divide by weight sum) prices.ewm(span=12, adjust=False).mean()   \# recursive formula prices.ewm(span=12, ignore\_na=False).mean()\# NaN breaks the weights prices.ewm(span=12, ignore\_na=True).mean() \# NaN is skipped \# ── EWM operations prices.ewm(span=12).mean()            \# EWMA prices.ewm(span=12).std()             \# EW std prices.ewm(span=12).var()             \# EW variance prices.ewm(span=12).corr(other)          \# EW correlation prices.ewm(span=12).cov(other)           \# EW covariance \# ── Practical: MACD (Moving Average Convergence Divergence) ema12  \= prices.ewm(span=12).mean() ema26  \= prices.ewm(span=26).mean() macd   \= ema12 \- ema26 signal \= macd.ewm(span=9).mean() hist   \= macd \- signal |
| :---: | :---- |

 

# **Chapter 18 — Modern Pandas 2.x, Arrow & Extension Types**

| PyArrow Backend · Copy-on-Write · Nullable Types · pd.NA |
| :---: |

 

*▲ Modern Pandas 2.x — Arrow Backend, Copy-on-Write, Extension Types*

## **18.1  PyArrow-Backed DataFrames (Pandas 2.0+)**

Starting with Pandas 2.0, you can use PyArrow as the memory backend for DataFrames. This gives you Arrow columnar memory layout, zero-copy reads from Parquet, better string performance, and richer type support including timezone-aware timestamps and nested types.

| PYTHON | import pandas as pd import pyarrow as pa \# ── Read with Arrow backend df \= pd.read\_parquet('data.parquet', dtype\_backend='pyarrow') df \= pd.read\_csv('data.csv',         dtype\_backend='pyarrow') df \= pd.read\_json('data.json',       dtype\_backend='pyarrow') df \= pd.read\_feather('data.feather', dtype\_backend='pyarrow') \# ── Convert existing DataFrame to Arrow-backed df\_arrow \= df.convert\_dtypes(dtype\_backend='pyarrow') print(df\_arrow.dtypes) \# name       string\[pyarrow\] \# age         int64\[pyarrow\] \# salary    double\[pyarrow\] \# active      bool\[pyarrow\] \# dept       string\[pyarrow\] \# ── Create with explicit Arrow dtype df2 \= pd.DataFrame({     'name':   pd.array(\['Alice','Bob'\], dtype='string\[pyarrow\]'),     'salary': pd.array(\[95000,72000\],  dtype='int64\[pyarrow\]'), }) \# ── ArrowDtype directly import pyarrow as pa df3 \= pd.DataFrame({'x': pd.array(\[1,2,3\], dtype=pd.ArrowDtype(pa.int8()))}) \# ── Convert back to numpy-backed df\_numpy \= df\_arrow.astype({     'name':   'object',     'salary': 'int64',     'active': bool }) \# ── Check backend isinstance(df\['name'\].dtype, pd.ArrowDtype)  \# True if Arrow-backed |
| :---: | :---- |

 

## **18.2  Copy-on-Write (CoW)**

| PYTHON | import pandas as pd \# ── Enable Copy-on-Write globally (recommended for Pandas 2.x) pd.options.mode.copy\_on\_write \= True \# or: pd.set\_option('mode.copy\_on\_write', True) \# ── What CoW changes \# BEFORE CoW (Pandas 1.x behaviour — unpredictable): df \= pd.DataFrame({'a':\[1,2,3\], 'b':\[4,5,6\]}) subset \= df\[\['a','b'\]\]         \# may be view OR copy subset\['a'\] \= 0                 \# may or may not modify df\! \# WITH CoW (Pandas 2.x, CoW=True — always predictable): subset \= df\[\['a','b'\]\]         \# always a lazy copy subset\['a'\] \= 0                 \# creates NEW object, df unchanged \# Never SettingWithCopyWarning again\! \# ── Correct patterns that work both ways: \# Use .loc for in-place conditional assignment df.loc\[df\['a'\] \> 1, 'b'\] \= 99  \# always correct \# Use .copy() for explicit copies df2 \= df.copy()                 \# explicit deep copy df3 \= df.copy(deep=False)       \# shallow copy \# ── assign() always returns a new object (CoW-compatible) df\_new \= df.assign(c \= df\['a'\] \+ df\['b'\]) \# ── Check if CoW is enabled print(pd.options.mode.copy\_on\_write)  \# True or False |
| :---: | :---- |

 

## **18.3  Nullable Extension Types**

| PYTHON | import pandas as pd import numpy as np \# ── Problem with numpy int \+ NaN (pre-nullable types) s \= pd.Series(\[1, 2, np.nan, 4\])  \# forced to float64\! print(s.dtype)  \# float64 (because NaN is a float concept in numpy) \# ── Solution: Nullable Integer types s\_int  \= pd.array(\[1, 2, pd.NA, 4\], dtype='Int64')   \# capital I\! s\_int8 \= pd.array(\[1, 2, pd.NA, 4\], dtype='Int8')    \# 1 byte per value s\_bool \= pd.array(\[True, False, pd.NA\], dtype='boolean') s\_str  \= pd.array(\['Alice', None, 'Carol'\], dtype='string') s\_f32  \= pd.array(\[1.1, 2.2, pd.NA\], dtype='Float32') \# ── All nullable type strings \# Integer:  'Int8','Int16','Int32','Int64' \# Unsigned: 'UInt8','UInt16','UInt32','UInt64' \# Float:    'Float32','Float64' \# Boolean:  'boolean' \# String:   'string' or 'string\[pyarrow\]' \# ── astype to nullable df\['age'\]    \= df\['age'\].astype('Int8')         \# allows NaN \+ smaller df\['active'\] \= df\['active'\].astype('boolean')   \# allows pd.NA df\['name'\]   \= df\['name'\].astype('string')      \# better than object \# ── pd.NA vs np.nan vs None pd.NA                          \# pandas missing value sentinel pd.isna(pd.NA)                 \# True pd.NA \+ 1                      \# pd.NA (propagates) pd.NA | True                   \# True (logical short-circuit) pd.NA & False                  \# False (logical short-circuit) pd.NA \== pd.NA                 \# pd.NA (not True\!) pd.NA is pd.NA                 \# True (singleton) \# ── convert\_dtypes() — auto-select best nullable dtype df\_better \= df.convert\_dtypes()  \# int64 \-\> Int64, object \-\> string print(df\_better.dtypes) |
| :---: | :---- |

 

## **18.4  pd.Categorical — Memory-Efficient Strings**

| PYTHON | import pandas as pd \# ── Create categorical cat \= pd.Categorical(\['red','blue','red','green','blue'\],                       categories=\['green','blue','red'\],                       ordered=True) \# As Series s \= pd.Series(cat) df\['dept'\] \= df\['dept'\].astype('category') \# ── Why: memory comparison n \= 1\_000\_000 s\_obj \= pd.Series(\['Engineering','Marketing','HR'\] \* (n//3)) s\_cat \= s\_obj.astype('category') print(s\_obj.memory\_usage(deep=True))  \# \~65 MB (stores each string) print(s\_cat.memory\_usage(deep=True))  \# \~1 MB (stores code \+ 3 strings) \# ── cat accessor — all operations s.cat.categories                    \# Index of unique categories s.cat.codes                         \# integer codes (0,1,2...) s.cat.ordered                       \# bool s.cat.dtype                         \# CategoricalDtype s.cat.rename\_categories({'HR':'Human Resources'}) s.cat.reorder\_categories(\['HR','Mkt','Eng'\]) s.cat.add\_categories(\['Legal'\]) s.cat.remove\_categories(\['Legal'\]) s.cat.remove\_unused\_categories() s.cat.set\_categories(\['Eng','Mkt'\], ordered=True) s.cat.as\_ordered()                  \# make ordered s.cat.as\_unordered() \# ── Ordered categorical for proper comparison grade\_order \= pd.CategoricalDtype(\['D','C','B','A'\], ordered=True) df\['grade'\] \= df\['grade'\].astype(grade\_order) df\[df\['grade'\] \>= 'B'\]             \# comparison works correctly df.sort\_values('grade')             \# sorts by category order |
| :---: | :---- |

 

# **Chapter 19 — Real-World Scenarios & Complete Patterns**

| EDA Pipeline · ETL · ML Prep · Financial Analysis · Report Generation |
| :---: |

 

*▲ Pandas Real-World Pipelines — EDA, ETL, ML, Finance, Reports*

## **19.1  Complete EDA Pipeline**

| PYTHON | import pandas as pd import numpy as np import matplotlib.pyplot as plt import seaborn as sns def full\_eda(filepath):     \# ── 1\. Load & basic inspection     df \= pd.read\_csv(filepath, dtype\_backend='pyarrow')     print(f'Shape: {df.shape}')     print(f'Columns: {df.columns.tolist()}')     df.info(memory\_usage='deep')     \# ── 2\. Missing values report     null\_report \= pd.DataFrame({         'null\_count': df.isna().sum(),         'null\_pct':   (df.isna().mean()\*100).round(2),         'dtype':      df.dtypes     }).query('null\_count \> 0').sort\_values('null\_pct', ascending=False)     print('\\nNULL REPORT:')     print(null\_report)     \# ── 3\. Numeric summary     print('\\nNUMERIC SUMMARY:')     print(df.describe(percentiles=\[.05,.25,.5,.75,.95\]))     \# ── 4\. Categorical summary     cat\_cols \= df.select\_dtypes(include=\['object','category','string'\]).columns     for col in cat\_cols:         print(f'\\n{col}: {df\[col\].nunique()} unique')         print(df\[col\].value\_counts().head(10))     \# ── 5\. Correlations     numeric \= df.select\_dtypes(include='number')     if len(numeric.columns) \> 1:         corr \= numeric.corr()         print('\\nTop correlations (|r| \> 0.5):')         \# Get upper triangle         mask \= np.triu(np.ones\_like(corr, dtype=bool))         corr\_pairs \= corr.where(\~mask).stack()         strong \= corr\_pairs\[corr\_pairs.abs() \> 0.5\]         print(strong.sort\_values(key=abs, ascending=False))     \# ── 6\. Outlier detection (IQR method)     for col in numeric.columns:         Q1  \= df\[col\].quantile(0.25)         Q3  \= df\[col\].quantile(0.75)         IQR \= Q3 \- Q1         outliers \= df\[(df\[col\] \< Q1 \- 1.5\*IQR) | (df\[col\] \> Q3 \+ 1.5\*IQR)\]         if len(outliers) \> 0:             print(f'Outliers in {col}: {len(outliers)} rows')     return df df \= full\_eda('employees.csv') |
| :---: | :---- |

 

## **19.2  Production ETL Pipeline**

| PYTHON | import pandas as pd import numpy as np from typing import Optional class EmployeeETL:     '''Production-grade ETL pipeline for employee data.'''     REQUIRED\_COLS \= \['emp\_id','name','salary','hire\_date','dept'\]     VALID\_DEPTS   \= {'Engineering','Marketing','HR','Finance','Legal'}     def extract(self, path: str) \-\> pd.DataFrame:         return pd.read\_csv(path,             dtype    \= {'emp\_id':'string','name':'string','dept':'string'},             parse\_dates \= \['hire\_date'\],             dtype\_backend \= 'pyarrow'         )     def validate(self, df: pd.DataFrame) \-\> pd.DataFrame:         \# Check required columns         missing \= set(self.REQUIRED\_COLS) \- set(df.columns)         if missing: raise ValueError(f'Missing columns: {missing}')         \# Check row count         if len(df) \== 0: raise ValueError('Empty DataFrame')         \# Log validation issues         null\_rows  \= df\[df\[self.REQUIRED\_COLS\].isna().any(axis=1)\]         bad\_salary \= df\[df\['salary'\] \<= 0\]         bad\_dept   \= df\[\~df\['dept'\].isin(self.VALID\_DEPTS)\]         print(f'Null rows: {len(null\_rows)}, Bad salary: {len(bad\_salary)}, Bad dept: {len(bad\_dept)}')         return df     def transform(self, df: pd.DataFrame) \-\> pd.DataFrame:         return (df             \# Clean             .assign(name \= lambda x: x\['name'\].str.strip().str.title(),                     dept \= lambda x: x\['dept'\].str.strip())             .replace({'':np.nan})             .dropna(subset=self.REQUIRED\_COLS)             .drop\_duplicates(subset=\['emp\_id'\])             \# Enrich             .assign(                 salary      \= lambda x: pd.to\_numeric(x\['salary'\], errors='coerce'),                 dept        \= lambda x: x\['dept'\].astype('category'),                 tenure\_days \= lambda x: (pd.Timestamp.now()-x\['hire\_date'\]).dt.days,                 dept\_avg    \= lambda x: x.groupby('dept')\['salary'\].transform('mean'),                 salary\_band \= lambda x: pd.cut(x\['salary'\],                     bins=\[0,60000,80000,100000,float('inf')\],                     labels=\['Junior','Mid','Senior','Principal'\])             )             .reset\_index(drop=True)         )     def load(self, df: pd.DataFrame, path: str) \-\> None:         df.to\_parquet(path, index=False, engine='pyarrow', compression='snappy')         print(f'Written {len(df)} rows to {path}')     def run(self, src: str, dst: str) \-\> pd.DataFrame:         df \= self.extract(src)         df \= self.validate(df)         df \= self.transform(df)         self.load(df, dst)         return df etl \= EmployeeETL() result \= etl.run('raw/employees.csv', 'processed/employees.parquet') |
| :---: | :---- |

 

## **19.3  ML Feature Engineering Pipeline**

| PYTHON | import pandas as pd import numpy as np def engineer\_features(df: pd.DataFrame) \-\> pd.DataFrame:     df \= df.copy()     \# ── Numeric transformations     df\['salary\_log'\]       \= np.log1p(df\['salary'\])     df\['salary\_sqrt'\]      \= np.sqrt(df\['salary'\])     df\['age\_squared'\]      \= df\['age'\] \*\* 2     df\['salary\_age\_ratio'\] \= df\['salary'\] / (df\['age'\] \+ 1\)     \# ── Percentile / rank features     df\['salary\_pctile'\]    \= df\['salary'\].rank(pct=True)     df\['salary\_dept\_rank'\] \= df.groupby('dept')\['salary'\].rank(pct=True)     \# ── Group statistics     df\['dept\_mean\_sal'\]    \= df.groupby('dept')\['salary'\].transform('mean')     df\['dept\_std\_sal'\]     \= df.groupby('dept')\['salary'\].transform('std')     df\['sal\_vs\_dept\_avg'\]  \= df\['salary'\] \- df\['dept\_mean\_sal'\]     df\['sal\_z\_within\_dept'\]= df\['sal\_vs\_dept\_avg'\] / df\['dept\_std\_sal'\]     \# ── Date features     if 'hire\_date' in df.columns:         df\['tenure\_days'\]  \= (pd.Timestamp.now() \- df\['hire\_date'\]).dt.days         df\['hire\_year'\]    \= df\['hire\_date'\].dt.year         df\['hire\_month'\]   \= df\['hire\_date'\].dt.month         df\['hire\_quarter'\] \= df\['hire\_date'\].dt.quarter         df\['hire\_dow'\]     \= df\['hire\_date'\].dt.dayofweek         df\['is\_q1\_hire'\]   \= df\['hire\_date'\].dt.quarter \== 1     \# ── Categorical encoding     \# One-hot encode low-cardinality     df \= pd.get\_dummies(df, columns=\['dept'\], drop\_first=True, dtype=int)     \# Ordinal encode ordered categorical     if df\['salary\_band'\].dtype.name \== 'category':         df\['salary\_band\_ord'\] \= df\['salary\_band'\].cat.codes     \# ── Interaction features     df\['age\_x\_tenure'\]     \= df\['age'\] \* df.get('tenure\_days', 0\) / 365     \# ── Binning     df\['age\_bin'\]    \= pd.qcut(df\['age'\], q=4, labels=\['Q1','Q2','Q3','Q4'\])     df\['sal\_bucket'\] \= pd.cut(df\['salary'\],         bins=\[0,60000,80000,100000,150000,float('inf')\],         labels=\['\<60k','60-80k','80-100k','100-150k','\>150k'\])     \# ── Drop originals if needed     df \= df.select\_dtypes(include='number')  \# keep only numeric for ML     return df.fillna(0)                      \# fill any remaining NaN \# Train/test split features \= engineer\_features(df) train \= features.sample(frac=0.8, random\_state=42) test  \= features.drop(train.index) X\_train, y\_train \= train.drop('target',axis=1), train\['target'\] X\_test,  y\_test  \= test.drop('target',axis=1),  test\['target'\] |
| :---: | :---- |

 

## **19.4  Financial Time Series Analysis**

| PYTHON | import pandas as pd import numpy as np \# ── Load price data prices \= pd.read\_csv('prices.csv', index\_col='Date',                       parse\_dates=True)\['Close'\] \# ── Returns daily\_ret   \= prices.pct\_change()              \# simple daily return log\_ret     \= np.log(prices / prices.shift(1)) \# log return cum\_ret     \= (1 \+ daily\_ret).cumprod()        \# cumulative return total\_ret   \= cum\_ret.iloc\[-1\] \- 1             \# total period return \# ── Risk metrics vol\_annual  \= daily\_ret.std() \* np.sqrt(252)   \# annualized volatility sharpe      \= (daily\_ret.mean()\*252) / vol\_annual  \# Sharpe ratio max\_dd      \= (cum\_ret / cum\_ret.cummax() \- 1).min()  \# max drawdown calmar      \= (total\_ret) / abs(max\_dd)         \# Calmar ratio \# ── Technical indicators ma\_20   \= prices.rolling(20).mean()             \# 20-day moving average ma\_50   \= prices.rolling(50).mean()             \# 50-day moving average ma\_200  \= prices.rolling(200).mean()            \# 200-day moving average bb\_mid  \= prices.rolling(20).mean()             \# Bollinger Band middle bb\_std  \= prices.rolling(20).std() bb\_upper= bb\_mid \+ 2 \* bb\_std                   \# upper band bb\_lower= bb\_mid \- 2 \* bb\_std                   \# lower band ewma12  \= prices.ewm(span=12).mean() ewma26  \= prices.ewm(span=26).mean() macd    \= ewma12 \- ewma26 signal  \= macd.ewm(span=9).mean() \# ── RSI delta   \= prices.diff() gain    \= delta.where(delta \> 0, 0).rolling(14).mean() loss    \= (-delta.where(delta \< 0, 0)).rolling(14).mean() rs      \= gain / loss rsi     \= 100 \- (100 / (1 \+ rs)) \# ── Portfolio analysis (multiple assets) port \= pd.read\_csv('portfolio.csv', index\_col='Date', parse\_dates=True) ret\_matrix \= port.pct\_change().dropna() corr\_matrix= ret\_matrix.corr()                  \# correlation matrix cov\_matrix \= ret\_matrix.cov()                   \# covariance matrix weights \= pd.Series(\[0.4, 0.3, 0.3\], index=port.columns) port\_ret \= (ret\_matrix \* weights).sum(axis=1)   \# weighted portfolio return port\_vol \= np.sqrt(weights @ cov\_matrix @ weights) \* np.sqrt(252) \# ── Monthly performance table monthly \= prices.resample('ME').last().pct\_change() monthly.index \= monthly.index.to\_period('M') pivot \= monthly.groupby(\[monthly.index.year, monthly.index.month\]).first().unstack() |
| :---: | :---- |

 

# **Chapter 20 — Performance Deep Dive**

| Benchmarking · Profiling · Vectorization · Memory · eval/query |
| :---: |

 

*▲ Pandas Performance — Speed Comparisons, Memory Strategies & Anti-patterns*

## **20.1  Benchmarking Operations**

| PYTHON | import pandas as pd import numpy as np import time N \= 1\_000\_000 df \= pd.DataFrame({     'a': np.random.randn(N),     'b': np.random.randint(0, 100, N),     'dept': np.random.choice(\['Eng','Mkt','HR'\], N) }) def bench(label, fn):     t0 \= time.perf\_counter()     result \= fn()     t1 \= time.perf\_counter()     print(f'{label:\<40}: {(t1-t0)\*1000:.2f} ms')     return result \# Iteration (SLOWEST — never do this for transforms) bench('iterrows() loop',   lambda: \[row\['a'\]\*2 for \_,row in df.iterrows()\]) \# iterrows: \~2500 ms \# itertuples (faster than iterrows — avoids boxing) bench('itertuples() loop', lambda: \[r.a\*2 for r in df.itertuples()\]) \# itertuples: \~200 ms \# Series apply (row-by-row Python overhead) bench('apply(lambda)',     lambda: df\['a'\].apply(lambda x: x\*2)) \# apply: \~80 ms \# Vectorized pandas bench('vectorized \* 2',   lambda: df\['a'\] \* 2\) \# vectorized: \~2 ms — 1250x faster than iterrows\! \# NumPy directly bench('numpy \* 2',        lambda: df\['a'\].values \* 2\) \# numpy: \~1 ms \# eval() bench('eval a\*2',         lambda: df.eval('a\*2')) \# eval: \~1.5 ms (numexpr backend) \# GroupBy comparison bench('groupby apply',    lambda: df.groupby('dept')\['a'\].apply(np.mean)) bench('groupby mean',     lambda: df.groupby('dept')\['a'\].mean()) \# apply: \~50ms vs mean: \~3ms — 17x faster with native method |
| :---: | :---- |

 

## **20.2  Memory Profiling**

| PYTHON | import pandas as pd import numpy as np \# ── df.info() — quick overview df.info(memory\_usage='deep')        \# deep=True counts actual string bytes \# ── df.memory\_usage() — per column usage \= df.memory\_usage(deep=True) print(usage.sort\_values(ascending=False)) print(f'Total: {usage.sum()/1e6:.2f} MB') \# ── Before/after dtype optimization def memory\_mb(df): return df.memory\_usage(deep=True).sum() / 1e6 print(f'Before: {memory\_mb(df):.2f} MB') \# Optimize df\_opt \= df.copy() for col in df\_opt.select\_dtypes('int64').columns:     df\_opt\[col\] \= pd.to\_numeric(df\_opt\[col\], downcast='integer') for col in df\_opt.select\_dtypes('float64').columns:     df\_opt\[col\] \= pd.to\_numeric(df\_opt\[col\], downcast='float') for col in df\_opt.select\_dtypes('object').columns:     if df\_opt\[col\].nunique() / len(df\_opt) \< 0.5:  \# \< 50% unique         df\_opt\[col\] \= df\_opt\[col\].astype('category')     else:         df\_opt\[col\] \= df\_opt\[col\].astype('string') print(f'After:  {memory\_mb(df\_opt):.2f} MB') \# ── Chunk processing for out-of-memory files result\_chunks \= \[\] for chunk in pd.read\_csv('huge\_file.csv', chunksize=100\_000,                           dtype={'salary':'float32','dept':'category'}):     \# Process each chunk     filtered \= chunk\[chunk\['salary'\] \> 80000\]     summary  \= filtered.groupby('dept')\['salary'\].mean()     result\_chunks.append(summary) \# Combine chunks final \= pd.concat(result\_chunks).groupby(level=0).mean() |
| :---: | :---- |

 

## **20.3  eval() and query() — numexpr Acceleration**

| PYTHON | import pandas as pd import numpy as np N \= 5\_000\_000 df \= pd.DataFrame({'a':np.random.randn(N),'b':np.random.randn(N),                     'c':np.random.randn(N)}) \# ── eval() — expression evaluation using numexpr \# Avoids creating intermediate arrays → faster \+ less memory \# Scalar operations df.eval('result \= a \* b \+ c \*\* 2 \- a / b') \# Multi-expression (computed in one pass) df.eval('''     x \= a \+ b     y \= a \* c     z \= x / y ''', inplace=True) \# With Python variables threshold \= 0.5 df.eval('above \= a \> @threshold', inplace=True) \# Functions available in eval: \# abs, sin, cos, tan, arcsin, arccos, arctan \# sinh, cosh, tanh, arcsinh, arccosh, arctanh \# log, log2, log10, log1p \# exp, expm1, sqrt \# conj, real, imag \# ── query() — filter rows efficiently \# For large DataFrames much faster than boolean indexing \# Comparison operators df.query('a \> 0.5') df.query('a \> 0.5 and b \< 0.5') df.query('a \> 0.5 or b \> 0.5') df.query('not (a \> 0.5)') \# String operations df2 \= pd.DataFrame({'dept':\['Eng','Mkt','HR'\]\*1000}) df2.query('dept \== "Eng"') df2.query('dept in \["Eng", "HR"\]') \# Python variable references min\_val \= 0.3 df.query('a \> @min\_val and b \< @min\_val') \# Index queries df.query('index \> 1000') df.query('index in @idx\_list') \# ── Check if numexpr is installed and active import pandas.core.computation.ops as ops print(pd.core.computation.check\_expression('a \+ b')) |
| :---: | :---- |

 

## **20.4  Practical Optimization Checklist**

| Priority | Optimization | Typical Speedup | How To |
| :---- | :---- | :---- | :---- |
| 1 \- Critical | Avoid iterrows() / loops | 100-2500x | Use vectorized ops, .str, .dt |
| 2 \- Critical | Use native agg methods | 5-20x | groupby().mean() not .apply(np.mean) |
| 3 \- High | Specify dtypes on read | 2-5x load | pd.read\_csv(dtype={'col':'int8'}) |
| 4 \- High | category for strings | 10-50x memory | astype('category') for low-cardinality |
| 5 \- High | int8/float32 downcasting | 2-8x memory | pd.to\_numeric(downcast='integer') |
| 6 \- Medium | eval()/query() for large DF | 1.5-5x | Only helps with \>100k rows \+ numexpr |
| 7 \- Medium | Filter early | Varies | Read only needed columns \+ rows |
| 8 \- Medium | Use Parquet not CSV | 3-10x | pd.read\_parquet vs pd.read\_csv |
| 9 \- Medium | Copy-on-Write | 1.2-2x | pd.options.mode.copy\_on\_write=True |
| 10 \- Low | raw=True in apply | 1.3-3x | s.apply(fn, raw=True) passes numpy |
| 11 \- Low | PyArrow backend | 1.5-4x | dtype\_backend='pyarrow' on read |
| 12 \- Future | Switch to Polars | 3-20x | Complete rewrite but much faster |

# **Chapter 21 — Complete Series API Reference**

| Every Series Method · Attribute · Accessor · Property |
| :---: |

 

## **21.1  Series Attributes**

| Attribute | Type | Description |
| :---- | :---- | :---- |
| s.values | ndarray / ExtensionArray | Underlying data as numpy array or ArrowExtensionArray |
| s.index | Index | Labels for each element |
| s.dtype | dtype | Data type (int64, float64, object, category...) |
| s.name | str or None | Name of the Series (becomes column name in DataFrame) |
| s.shape | tuple | (n,) — number of elements |
| s.size | int | Total number of elements |
| s.ndim | int | Always 1 for Series |
| s.nbytes | int | Total bytes of underlying data |
| s.empty | bool | True if Series has no elements |
| s.hasnans | bool | True if any NaN values present |
| s.is\_unique | bool | True if all values are unique |
| s.is\_monotonic\_increasing | bool | True if values never decrease |
| s.is\_monotonic\_decreasing | bool | True if values never increase |
| s.T | Series | Transpose (returns self for 1D) |
| s.array | ExtensionArray | The underlying ExtensionArray |
| s.flags | Flags | Series flags (e.g., allows\_duplicate\_labels) |

 

## **21.2  Series Methods — Full Alphabetical Reference**

| Method | Description |
| :---- | :---- |
| s.abs() | Absolute value of each element |
| s.add(other) | Add element-wise (supports fill\_value) |
| s.add\_prefix(p) | Prefix all index labels with p |
| s.add\_suffix(s) | Suffix all index labels with s |
| s.agg(func) | Aggregate using one or more functions |
| s.align(other) | Align two Series on their index |
| s.all() | True if all non-NA values are True |
| s.any() | True if any non-NA value is True |
| s.apply(func) | Apply a function element-wise |
| s.argmax() | Position of the maximum value |
| s.argmin() | Position of the minimum value |
| s.argsort() | Index positions that would sort the Series |
| s.asfreq(freq) | Convert DatetimeIndex to specified frequency |
| s.asof(where) | Last observation up to given label (used with dates) |
| s.astype(dtype) | Cast to specified dtype |
| s.at\[label\] | Fast single-value access by label |
| s.autocorr(lag) | Autocorrelation at given lag |
| s.between(l,r) | Boolean: is value between left and right (inclusive) |
| s.bfill() | Backward fill missing values |
| s.bool() | Return bool value of single-element Series |
| s.clip(lower,upper) | Clip values to range |
| s.combine(other,func) | Combine two Series element-wise with function |
| s.combine\_first(other) | Fill NaN from other |
| s.compare(other) | Show where two Series differ |
| s.copy(deep=True) | Make a copy |
| s.corr(other) | Pearson correlation with another Series |
| s.count() | Count non-NA values |
| s.cov(other) | Covariance with another Series |
| s.cummax() | Cumulative maximum |
| s.cummin() | Cumulative minimum |
| s.cumprod() | Cumulative product |
| s.cumsum() | Cumulative sum |
| s.describe() | Summary statistics |
| s.diff(periods) | Lagged difference |
| s.div(other) | Divide element-wise |
| s.divmod(other) | Element-wise quotient and remainder |
| s.drop(labels) | Drop elements by label |
| s.drop\_duplicates() | Remove duplicate values |
| s.dropna() | Drop NaN values |
| s.dt | Datetime accessor for DatetimeSeries |
| s.duplicated() | Boolean: is element a duplicate? |
| s.eq(other) | Element-wise equality |
| s.equals(other) | Test whether two Series are identical |
| s.ewm(...) | Exponentially weighted operations |
| s.expanding(...) | Expanding window operations |
| s.explode() | Expand list-like elements into rows |
| s.factorize() | Encode as int codes \+ unique levels |
| s.ffill() | Forward fill missing values |
| s.fillna(value) | Replace NaN values |
| s.filter(items,like,regex) | Subset index labels |
| s.first(offset) | First rows within time offset |
| s.first\_valid\_index() | Label of first non-NA value |
| s.floordiv(other) | Floor division |
| s.ge(other) | \>= |
| s.get(key,default) | Get item or default if not found |
| s.groupby(...) | Group by values or function |
| s.gt(other) | Greater than |
| s.head(n) | First n elements |
| s.hist(...) | Draw histogram |
| s.iat\[pos\] | Fast single-value by position |
| s.idxmax() | Index label of maximum value |
| s.idxmin() | Index label of minimum value |
| s.iloc\[...\] | Position-based indexer |
| s.infer\_objects() | Infer better dtypes for object columns |
| s.interpolate(...) | Interpolate missing values |
| s.isin(values) | Boolean: is element in values? |
| s.isna() / isnull() | Boolean: is element NaN? |
| s.item() | Return scalar value (single-element only) |
| s.items() / iteritems() | Iterate over (index, value) pairs |
| s.keys() | Return index (alias) |
| s.kurt() / kurtosis() | Excess kurtosis |
| s.last(offset) | Last rows within time offset |
| s.last\_valid\_index() | Label of last non-NA value |
| s.le(other) | \<= |
| s.loc\[...\] | Label-based indexer |
| s.lt(other) | Less than |
| s.map(arg) | Map values using dict/function/Series |
| s.mask(cond,other) | Replace values where condition is True |
| s.max() | Maximum value |
| s.mean() | Mean value |
| s.median() | Median value |
| s.memory\_usage(deep) | Memory in bytes |
| s.min() | Minimum value |
| s.mod(other) | Modulo |
| s.mode() | Most frequent value(s) |
| s.mul(other) | Multiply |
| s.name | Name of Series |
| s.ne(other) | \!= |
| s.nlargest(n) | n largest values |
| s.notna() / notnull() | Inverse of isna() |
| s.nsmallest(n) | n smallest values |
| s.nunique() | Count of unique non-NA values |
| s.pct\_change(periods) | % change from prior period |
| s.pipe(func,\*args) | Apply function to Series |
| s.plot(...) | Draw plots |
| s.pop(item) | Remove and return element |
| s.pow(other) | Raise to power |
| s.prod() | Product of all values |
| s.quantile(q) | Value at given quantile |
| s.radd(other) | Reverse add |
| s.rank(...) | Rank of values |
| s.ravel() | Return underlying data as 1D ndarray |
| s.rdiv(other) | Reverse division |
| s.reindex(index) | Conform to new index |
| s.rename(index) | Alter index labels or Series name |
| s.rename\_axis(name) | Rename the index |
| s.repeat(repeats) | Repeat elements |
| s.replace(to\_replace,value) | Replace values |
| s.reset\_index(drop) | Reset index to 0..N-1 |
| s.resample(rule) | Resample time-series data |
| s.rfloordiv(other) | Reverse floor division |
| s.rmod(other) | Reverse mod |
| s.rmul(other) | Reverse multiply |
| s.rolling(window) | Rolling window calculations |
| s.round(decimals) | Round to given decimals |
| s.rpow(other) | Reverse power |
| s.rsub(other) | Reverse subtract |
| s.rtruediv(other) | Reverse true division |
| s.sample(n,frac) | Random sample |
| s.searchsorted(value) | Find insertion point |
| s.sem() | Standard error of mean |
| s.set\_axis(labels) | Set axis labels |
| s.shift(periods) | Shift values by periods |
| s.skew() | Skewness |
| s.sort\_index(...) | Sort by index |
| s.sort\_values(...) | Sort by values |
| s.std() | Standard deviation |
| s.str | String accessor (object/string dtype only) |
| s.sub(other) | Subtract |
| s.sum() | Sum of values |
| s.swapaxes(i,j) | Swap axes (deprecated 2.3) |
| s.tail(n) | Last n elements |
| s.to\_clipboard() | Copy to clipboard |
| s.to\_csv(path) | Write to CSV |
| s.to\_dict() | Convert to dict |
| s.to\_excel(...) | Write to Excel |
| s.to\_frame(name) | Convert to single-column DataFrame |
| s.to\_hdf(...) | Write to HDF5 |
| s.to\_json(...) | Write to JSON |
| s.to\_latex(...) | Convert to LaTeX |
| s.to\_list() / tolist() | Convert to Python list |
| s.to\_markdown(...) | Convert to Markdown table |
| s.to\_numpy() | Convert to NumPy array |
| s.to\_period(freq) | Convert DatetimeIndex to PeriodIndex |
| s.to\_pickle(path) | Serialize to pickle |
| s.to\_sql(...) | Write to SQL database |
| s.to\_string(...) | Render as string |
| s.to\_timestamp(freq) | Convert PeriodIndex to DatetimeIndex |
| s.transform(func) | Apply function, return same shape |
| s.truediv(other) | True division |
| s.truncate(before,after) | Truncate to index range |
| s.unique() | Return unique values as ndarray |
| s.unstack(level) | Unstack MultiIndex level to columns |
| s.update(other) | Update Series from another (where not NaN) |
| s.value\_counts(normalize) | Frequency of unique values |
| s.var() | Variance |
| s.view(dtype) | View data as different dtype |
| s.where(cond,other) | Keep where True, replace where False |
| s.xs(key,level) | Cross-section for MultiIndex |

# **Chapter 22 — Pandas with Databases, Cloud & Big Data**

| SQLAlchemy · S3/ADLS/GCS · Dask · Polars · PySpark Integration |
| :---: |

 

## **22.1  Database Integration via SQLAlchemy**

| PYTHON | import pandas as pd from sqlalchemy import create\_engine, text \# ── Connection strings \# PostgreSQL pg\_engine  \= create\_engine('postgresql://user:pw@host:5432/dbname') \# MySQL my\_engine  \= create\_engine('mysql+pymysql://user:pw@host:3306/db') \# SQLite (local file) sq\_engine  \= create\_engine('sqlite:///mydata.db') \# SQL Server ms\_engine  \= create\_engine('mssql+pyodbc://user:pw@server/db?driver=ODBC+Driver+17+for+SQL+Server') \# BigQuery bq\_engine  \= create\_engine('bigquery://my-project/my\_dataset') \# Snowflake sf\_engine  \= create\_engine('snowflake://user:pw@account/db/schema') \# ── Read from SQL df \= pd.read\_sql('SELECT \* FROM employees', con=pg\_engine) df \= pd.read\_sql\_table('employees', con=pg\_engine) df \= pd.read\_sql\_query(     'SELECT \* FROM emp WHERE salary \> %(min\_sal)s',     con=pg\_engine,     params={'min\_sal': 80000},     index\_col='emp\_id',     parse\_dates=\['hire\_date'\],     chunksize=10000            \# iterator for large tables ) \# ── Write to SQL df.to\_sql('employees\_clean', con=pg\_engine,     if\_exists='replace',       \# 'replace','append','fail'     index=False,     chunksize=1000,     method='multi',            \# faster bulk insert     dtype={'dept': sa.String(50)}  \# explicit column types ) \# ── Read with raw SQL using context manager with pg\_engine.connect() as conn:     df \= pd.read\_sql(text('SELECT \* FROM emp'), con=conn) |
| :---: | :---- |

 

## **22.2  Cloud Storage — S3, ADLS, GCS**

| PYTHON | import pandas as pd \# ── AWS S3 \# pip install s3fs df \= pd.read\_parquet('s3://my-bucket/path/data.parquet') df \= pd.read\_csv('s3://my-bucket/data/file.csv') df.to\_parquet('s3://my-bucket/output/result.parquet', index=False) \# With credentials storage\_options \= {     'key': 'AWS\_ACCESS\_KEY\_ID',     'secret': 'AWS\_SECRET\_ACCESS\_KEY',     'token': 'AWS\_SESSION\_TOKEN',  \# optional } df \= pd.read\_parquet('s3://bucket/data.parquet',                       storage\_options=storage\_options) \# Read all parquet files in S3 prefix import s3fs fs \= s3fs.S3FileSystem() files \= fs.glob('s3://bucket/data/year=2024/\*\*/\*.parquet') df \= pd.concat(\[pd.read\_parquet(f's3://{f}') for f in files\]) \# ── Azure ADLS Gen2 \# pip install adlfs storage\_options \= {'account\_name':'myaccount', 'account\_key':'key'} df \= pd.read\_parquet(     'abfs://container@myaccount.dfs.core.windows.net/path/data.parquet',     storage\_options=storage\_options ) \# ── Google Cloud Storage \# pip install gcsfs df \= pd.read\_parquet('gs://my-bucket/path/data.parquet') df.to\_parquet('gs://my-bucket/output/result.parquet', index=False) \# ── fsspec — universal filesystem abstraction \# Works with S3, GCS, ADLS, SFTP, HTTP, local import fsspec with fsspec.open('s3://bucket/file.json') as f:     df \= pd.read\_json(f) |
| :---: | :---- |

 

## **22.3  Dask — Parallel Pandas for Large Data**

| PYTHON | import dask.dataframe as dd import pandas as pd \# ── Read large files in parallel ddf \= dd.read\_csv('huge\_file\_\*.csv', dtype={'salary':'float32'}) ddf \= dd.read\_parquet('s3://bucket/data/\*\*/\*.parquet') \# ── Pandas-like API (lazy evaluation) result \= (ddf     \[ddf\['salary'\] \> 80000\]            \# filter (lazy)     .groupby('dept')\['salary'\]          \# groupby (lazy)     .mean()                             \# aggregate (lazy) ) \# ── Trigger computation df\_result \= result.compute()           \# execute all queued operations \# ── Convert between pandas and dask ddf \= dd.from\_pandas(df, npartitions=4)     \# pandas → dask (4 partitions) df  \= ddf.compute()                          \# dask → pandas \# ── When to use Dask \# \- Data \> RAM but fits on disk \# \- Same single machine (multi-core parallel) \# \- Familiar Pandas API wanted \# \- NOT: distributed cluster (use PySpark for that) |
| :---: | :---- |

 

## 

## 

## 

## 

## 

## 

## 

## 

## **22.4  Pandas → PySpark Bridge**

| PYTHON | \# ── Pandas ↔ PySpark conversion from pyspark.sql import SparkSession spark \= SparkSession.builder.getOrCreate() \# Pandas DataFrame → Spark DataFrame spark\_df \= spark.createDataFrame(pandas\_df) \# Spark DataFrame → Pandas DataFrame \# WARNING: collects all data to driver — only for small data\! pandas\_df \= spark\_df.toPandas() \# ── pyspark.pandas (Koalas) — Pandas API on Spark import pyspark.pandas as ps \# Create pyspark.pandas DataFrame (distributed) psdf \= ps.read\_parquet('s3://bucket/large-data/') psdf \= ps.from\_pandas(df)               \# from regular pandas \# Uses Pandas API but runs on Spark cluster result \= (psdf     \[psdf\['salary'\] \> 80000\]     .groupby('dept')\['salary'\]     .mean() ) \# Convert back pandas\_result \= result.to\_pandas()      \# collect to driver spark\_df      \= result.to\_spark()       \# keep as Spark DF \# ── Arrow for zero-copy transfer import pyarrow as pa \# Pandas → Arrow (no copy if Arrow-backed) arrow\_table \= pa.Table.from\_pandas(df) \# Arrow → Pandas df \= arrow\_table.to\_pandas() \# Write Arrow → Parquet (schema preserved) import pyarrow.parquet as pq pq.write\_table(arrow\_table, 'output.parquet') |
| :---: | :---- |

 

   
   
 

| 🐼  Pandas Complete Engineering Guide Extended Edition — 22 Chapters  |  All Methods  |  13 Diagrams This guide covers everything from Pandas internals to production-grade pipelines: Why Pandas was built · Architecture & memory · Series/DataFrame/MultiIndex · All 150+ DataFrame methods · All 80+ Series methods · String/Date/Categorical accessors · GroupBy/agg/transform/filter/apply · Merging/joining/concat · Time series & rolling · I/O (CSV/Excel/Parquet/SQL/JSON/HDF5) · Visualization · Performance optimization · Modern Pandas 2.x (Arrow, CoW, Nullable types) · EDA/ETL/ML/Finance scenarios · Cloud storage (S3/ADLS/GCS) · Database integration · Dask/Polars/PySpark bridges |
| :---: |

