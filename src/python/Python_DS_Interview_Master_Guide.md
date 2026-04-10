

| 🐍  PYTHON DATA STRUCTURES INTERVIEW MASTER GUIDE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Amazon  •  Walmart  •  Fintech  •  FAANG 160 Questions  |  Easy → Advanced 8 Core Topics  |  Full I/O Examples  |  Expert Explanations |
| :---: |

| 📋 Lists | 📖 Dict | 🔤 String | 🔢 Numeric | 🔷 Sets | 📦 Tuples | 🔄 Mutable | 🔒 Immutable |  |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |

| 📋  LISTS — 20 Interview Questions |
| :---: |

| ⚡ EASY |
| :---: |

**Q1. What is a list and how do you create one in Python?**

|  📥  INPUT \# Creating lists nums \= \[1, 2, 3, 4, 5\] mixed \= \[1, "hello", 3.14, True\] empty \= \[\] nested \= \[\[1,2\],\[3,4\]\]  |  |  📤  OUTPUT nums   → \[1, 2, 3, 4, 5\] mixed  → \[1, 'hello', 3.14, True\] empty  → \[\] nested → \[\[1, 2\], \[3, 4\]\]  |
| :---- | :---- | :---- |

| *💡 Lists are ordered, mutable sequences that allow duplicate elements. They support mixed data types and are zero-indexed.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q2. How do you access and slice elements from a list?**

|  📥  INPUT lst \= \[10, 20, 30, 40, 50\] print(lst\[0\]) print(lst\[-1\]) print(lst\[1:4\]) print(lst\[::2\]) print(lst\[::-1\])  |  |  📤  OUTPUT 10 50 \[20, 30, 40\] \[10, 30, 50\] \[50, 40, 30, 20, 10\]  |
| :---- | :---- | :---- |

| *💡 Slicing uses \[start:stop:step\]. Negative indices count from the end. lst\[::-1\] reverses the list.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q3. What is the difference between append() and extend()?**

|  📥  INPUT a \= \[1, 2, 3\] b \= \[1, 2, 3\] a.append(\[4, 5\]) b.extend(\[4, 5\]) print(a) print(b)  |  |  📤  OUTPUT \[1, 2, 3, \[4, 5\]\] \[1, 2, 3, 4, 5\]  |
| :---- | :---- | :---- |

| *💡 append() adds a single element (even a list) as-is. extend() iterates over the argument and adds each element individually.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q4. How do you remove duplicates from a list while preserving order?**

|  📥  INPUT lst \= \[3, 1, 4, 1, 5, 9, 2, 6, 5, 3\] seen \= set() result \= \[\] for x in lst:     if x not in seen:         seen.add(x)         result.append(x) print(result)  |  |  📤  OUTPUT \[3, 1, 4, 5, 9, 2, 6\]  |
| :---- | :---- | :---- |

| *💡 Using a set for O(1) lookup preserves insertion order. Simply doing list(set(lst)) does NOT guarantee order — critical in data pipelines.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q5. How do you sort a list in ascending and descending order?**

|  📥  INPUT nums \= \[5, 2, 8, 1, 9, 3\] nums.sort() print(nums) nums.sort(reverse=True) print(nums) orig \= \[5,2,8,1\] s \= sorted(orig) print(orig, s)  |  |  📤  OUTPUT \[1, 2, 3, 5, 8, 9\] \[9, 8, 5, 3, 2, 1\] \[5, 2, 8, 1\] \[1, 2, 5, 8\]  |
| :---- | :---- | :---- |

| *💡 sort() mutates in-place, sorted() returns a new list. Use key= for custom comparators — very common in Amazon OA questions.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q6. How do you flatten a nested list?**

|  📥  INPUT nested \= \[\[1,2,3\],\[4,5\],\[6,7,8,9\]\] \# Method 1: list comprehension flat \= \[x for sub in nested for x in sub\] \# Method 2: itertools import itertools flat2 \= list(itertools.chain.from\_iterable(nested)) print(flat)  |  |  📤  OUTPUT \[1, 2, 3, 4, 5, 6, 7, 8, 9\]  |
| :---- | :---- | :---- |

| *💡 List comprehension works for 1-level nesting. For arbitrary depth, use recursion. itertools.chain is most efficient for production code.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q7. Find the second largest element in a list without sorting.**

|  📥  INPUT def second\_largest(lst):     first \= second \= float('-inf')     for n in lst:         if n \> first:             second \= first             first \= n         elif n \> second and n \!= first:             second \= n     return second   print(second\_largest(\[3,1,4,1,5,9,2,6\]))  |  |  📤  OUTPUT 6  |
| :---- | :---- | :---- |

| *💡 O(n) single-pass solution. Edge case: handle duplicates (9,9 → should return 6, not 9). Common at fintech interviews for efficiency focus.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q8. How do you rotate a list by k positions to the right?**

|  📥  INPUT def rotate(lst, k):     n \= len(lst)     k \= k % n     return lst\[-k:\] \+ lst\[:-k\]   print(rotate(\[1,2,3,4,5\], 2)) print(rotate(\[1,2,3,4,5\], 7))  |  |  📤  OUTPUT \[4, 5, 1, 2, 3\] \[4, 5, 1, 2, 3\]  |
| :---- | :---- | :---- |

| *💡 k % n handles k \> len(lst). Slicing is O(n). For in-place rotation use the reverse algorithm: reverse all, reverse first k, reverse rest — O(1) space.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q9. Group a list of integers into even and odd using list comprehension.**

|  📥  INPUT nums \= \[1,2,3,4,5,6,7,8,9,10\] even \= \[x for x in nums if x % 2 \== 0\] odd  \= \[x for x in nums if x % 2 \!= 0\] \# Also: partition in single pass from itertools import filterfalse, tee a, b \= tee(nums) even2 \= list(filter(lambda x: x%2==0, a))  |  |  📤  OUTPUT even → \[2, 4, 6, 8, 10\] odd  → \[1, 3, 5, 7, 9\]  |
| :---- | :---- | :---- |

| *💡 Single-pass with tee avoids iterating twice — important for large data streams in backend ETL pipelines.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q10. Implement a sliding window maximum on a list.**

|  📥  INPUT from collections import deque def slide\_max(nums, k):     dq, res \= deque(), \[\]     for i, n in enumerate(nums):         while dq and dq\[0\] \< i-k+1:             dq.popleft()         while dq and nums\[dq\[-1\]\] \< n:             dq.pop()         dq.append(i)         if i \>= k-1:             res.append(nums\[dq\[0\]\])     return res print(slide\_max(\[1,3,-1,-3,5,3,6,7\], 3))  |  |  📤  OUTPUT \[3, 3, 5, 5, 6, 7\]  |
| :---- | :---- | :---- |

| *💡 Classic deque-based O(n) solution. Common in Amazon data engineering rounds for streaming analytics windows.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q11. How do you merge two sorted lists into one sorted list efficiently?**

|  📥  INPUT import heapq def merge\_sorted(l1, l2):     return list(heapq.merge(l1, l2))   \# Manual O(n+m) def merge\_manual(l1, l2):     res, i, j \= \[\], 0, 0     while i \< len(l1) and j \< len(l2):         if l1\[i\] \<= l2\[j\]: res.append(l1\[i\]); i+=1         else: res.append(l2\[j\]); j+=1     return res \+ l1\[i:\] \+ l2\[j:\] print(merge\_sorted(\[1,3,5,7\],\[2,4,6,8\]))  |  |  📤  OUTPUT \[1, 2, 3, 4, 5, 6, 7, 8\]  |
| :---- | :---- | :---- |

| *💡 heapq.merge is lazy (generator-based). Manual two-pointer is O(n+m) time, O(n+m) space. Critical for Walmart's data pipeline merge operations.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q12. Find all pairs in a list that sum to a target value.**

|  📥  INPUT def two\_sum\_pairs(lst, target):     seen \= set()     pairs \= \[\]     for num in lst:         complement \= target \- num         if complement in seen:             pairs.append((complement, num))         seen.add(num)     return pairs   print(two\_sum\_pairs(\[1,2,3,4,5,6,7,8\], 9))  |  |  📤  OUTPUT \[(1, 8), (2, 7), (3, 6), (4, 5)\]  |
| :---- | :---- | :---- |

| *💡 Hash set approach is O(n) vs O(n²) brute force. This pattern appears in nearly every FAANG/fintech interview — master it\!* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q13. How do you implement a stack and queue using Python lists?**

|  📥  INPUT \# Stack (LIFO) stack \= \[\] stack.append(1); stack.append(2); stack.append(3) print("Pop:", stack.pop())   \# Queue (FIFO) — use deque for O(1) from collections import deque q \= deque(\[1,2,3\]) q.append(4) print("Dequeue:", q.popleft()) print("Queue:", list(q))  |  |  📤  OUTPUT Pop: 3 Dequeue: 1 Queue: \[2, 3, 4\]  |
| :---- | :---- | :---- |

| *💡 list.pop() is O(1) for stack. list.pop(0) for queue is O(n) — always use collections.deque for queues in production code.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q14. Given a list of transactions, find the maximum profit from buy/sell.**

|  📥  INPUT def max\_profit(prices):     if not prices: return 0     min\_p, max\_p \= prices\[0\], 0     for p in prices\[1:\]:         max\_p \= max(max\_p, p \- min\_p)         min\_p \= min(min\_p, p)     return max\_p   print(max\_profit(\[7,1,5,3,6,4\])) print(max\_profit(\[7,6,4,3,1\]))  |  |  📤  OUTPUT 5 0  |
| :---- | :---- | :---- |

| *💡 Classic fintech interview question\! Single-pass O(n) greedy. Track minimum price seen so far and max profit. 0 means no profitable trade exists.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q15. Implement an LRU Cache using a list and dict combination.**

|  📥  INPUT from collections import OrderedDict class LRUCache:     def \_\_init\_\_(self, cap):         self.cap \= cap         self.cache \= OrderedDict()     def get(self, key):         if key not in self.cache: return \-1         self.cache.move\_to\_end(key)         return self.cache\[key\]     def put(self, key, val):         self.cache\[key\] \= val         self.cache.move\_to\_end(key)         if len(self.cache) \> self.cap:             self.cache.popitem(last=False) lru \= LRUCache(2) lru.put(1,1); lru.put(2,2) print(lru.get(1)) lru.put(3,3) print(lru.get(2))  |  |  📤  OUTPUT 1 \-1  |
| :---- | :---- | :---- |

| *💡 OrderedDict maintains insertion order with O(1) move\_to\_end. Amazon backend services use LRU for API response caching.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q16. Find the longest increasing subsequence length in a list.**

|  📥  INPUT import bisect def lis\_length(nums):     tails \= \[\]     for n in nums:         pos \= bisect.bisect\_left(tails, n)         if pos \== len(tails):             tails.append(n)         else:             tails\[pos\] \= n     return len(tails)   print(lis\_length(\[10,9,2,5,3,7,101,18\])) print(lis\_length(\[0,1,0,3,2,3\]))  |  |  📤  OUTPUT 4 4  |
| :---- | :---- | :---- |

| *💡 O(n log n) patience sorting algorithm. tails\[i\] holds the smallest tail of increasing subsequence of length i+1. Amazon asks this for time-series analytics.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q17. How do you implement a circular buffer (ring buffer) using a list?**

|  📥  INPUT class CircularBuffer:     def \_\_init\_\_(self, size):         self.buf \= \[None\] \* size         self.size \= size         self.head \= self.tail \= self.count \= 0     def enqueue(self, val):         self.buf\[self.tail\] \= val         self.tail \= (self.tail \+ 1\) % self.size         self.count \= min(self.count+1, self.size)     def dequeue(self):         val \= self.buf\[self.head\]         self.head \= (self.head \+ 1\) % self.size         return val cb \= CircularBuffer(3) cb.enqueue(1); cb.enqueue(2); cb.enqueue(3) print(cb.dequeue())  |  |  📤  OUTPUT 1  |
| :---- | :---- | :---- |

| *💡 Circular buffers avoid expensive list.pop(0) O(n) shifts. Used in streaming data ingestion, Kafka consumer buffers, and log pipelines.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q18. Partition a list around a pivot (Dutch National Flag problem).**

|  📥  INPUT def dutch\_flag(lst, pivot):     low \= mid \= 0     high \= len(lst) \- 1     while mid \<= high:         if lst\[mid\] \< pivot:             lst\[low\], lst\[mid\] \= lst\[mid\], lst\[low\]             low \+= 1; mid \+= 1         elif lst\[mid\] \== pivot:             mid \+= 1         else:             lst\[mid\], lst\[high\] \= lst\[high\], lst\[mid\]             high \-= 1     return lst print(dutch\_flag(\[3,1,2,1,3,2,1\], 2))  |  |  📤  OUTPUT \[1, 1, 1, 2, 2, 3, 3\]  |
| :---- | :---- | :---- |

| *💡 3-way partition in O(n) time, O(1) space. Used in QuickSort optimization and data classification pipelines at scale.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q19. Implement matrix multiplication using nested lists.**

|  📥  INPUT def mat\_mul(A, B):     rows\_A, cols\_A \= len(A), len(A\[0\])     cols\_B \= len(B\[0\])     C \= \[\[0\]\*cols\_B for \_ in range(rows\_A)\]     for i in range(rows\_A):         for j in range(cols\_B):             for k in range(cols\_A):                 C\[i\]\[j\] \+= A\[i\]\[k\] \* B\[k\]\[j\]     return C A \= \[\[1,2\],\[3,4\]\] B \= \[\[5,6\],\[7,8\]\] print(mat\_mul(A, B))  |  |  📤  OUTPUT \[\[19, 22\], \[43, 50\]\]  |
| :---- | :---- | :---- |

| *💡 O(n³) naive; use numpy for production. Demonstrates understanding of nested list indexing — often asked in data engineering for feature transformation.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q20. Given a list of intervals, merge all overlapping intervals.**

|  📥  INPUT def merge\_intervals(intervals):     if not intervals: return \[\]     intervals.sort(key=lambda x: x\[0\])     merged \= \[intervals\[0\]\]     for start, end in intervals\[1:\]:         if start \<= merged\[-1\]\[1\]:             merged\[-1\]\[1\] \= max(merged\[-1\]\[1\], end)         else:             merged.append(\[start, end\])     return merged print(merge\_intervals(\[\[1,3\],\[2,6\],\[8,10\],\[15,18\]\]))  |  |  📤  OUTPUT \[\[1, 6\], \[8, 10\], \[15, 18\]\]  |
| :---- | :---- | :---- |

| *💡 Sort by start time O(n log n), then single-pass merge O(n). Critical for calendar event merging, network packet analysis, and data deduplication at Amazon/Walmart.* |
| :---- |

| 📖  DICTIONARY — 20 Interview Questions |
| :---: |

| ⚡ EASY |
| :---: |

**Q1. How do you create, access, and update a dictionary?**

|  📥  INPUT d \= {"name":"Alice","age":30,"city":"NY"} print(d\["name"\]) print(d.get("salary", 0)) d\["age"\] \= 31 d\["dept"\] \= "Engineering" print(d)  |  |  📤  OUTPUT Alice 0 {'name':'Alice','age':31,'city':'NY','dept':'Engineering'}  |
| :---- | :---- | :---- |

| *💡 dict.get(key, default) avoids KeyError — always prefer over direct \[\] access in production code for safer ETL pipelines.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q2. How do you iterate over keys, values, and items?**

|  📥  INPUT emp \= {"id":101,"name":"Bob","sal":75000} for k in emp.keys():    print("K:", k) for v in emp.values():  print("V:", v) for k,v in emp.items(): print(f"{k}={v}")  |  |  📤  OUTPUT K: id  K: name  K: sal V: 101  V: Bob  V: 75000 id=101  name=Bob  sal=75000  |
| :---- | :---- | :---- |

| *💡 dict.items() returns key-value tuples. In Python 3.7+ dicts are insertion-ordered. Extremely common in data transformation tasks.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q3. How do you merge two dictionaries?**

|  📥  INPUT d1 \= {"a":1, "b":2} d2 \= {"b":3, "c":4} \# Python 3.9+ merged \= d1 | d2 \# Python 3.5+ merged2 \= {\*\*d1, \*\*d2} d1.update(d2) print(merged) print(merged2)  |  |  📤  OUTPUT {'a': 1, 'b': 3, 'c': 4} {'a': 1, 'b': 3, 'c': 4}  |
| :---- | :---- | :---- |

| *💡 Later dict overwrites earlier on duplicate keys. The | operator (Python 3.9+) is clean but update() modifies in-place — know both for interviews.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q4. Count frequency of elements using a dictionary.**

|  📥  INPUT from collections import Counter words \= \["apple","banana","apple","cherry","banana","apple"\] freq \= Counter(words) print(freq) print(freq.most\_common(2))  |  |  📤  OUTPUT Counter({'apple':3,'banana':2,'cherry':1}) \[('apple', 3), ('banana', 2)\]  |
| :---- | :---- | :---- |

| *💡 Counter is a dict subclass with powerful methods. Ubiquitous in data engineering for log analysis, word counts, and event tracking.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q5. What is a defaultdict and when should you use it?**

|  📥  INPUT from collections import defaultdict graph \= defaultdict(list) edges \= \[(1,2),(1,3),(2,4),(3,4)\] for u,v in edges:     graph\[u\].append(v)     graph\[v\].append(u) print(dict(graph))  |  |  📤  OUTPUT {1:\[2,3\], 2:\[1,4\], 3:\[1,4\], 4:\[2,3\]}  |
| :---- | :---- | :---- |

| *💡 defaultdict never raises KeyError — auto-initializes missing keys. Essential for building adjacency lists, grouping records, and avoiding repetitive setdefault() calls.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q6. Invert a dictionary (swap keys and values).**

|  📥  INPUT original \= {"a":1, "b":2, "c":3} inverted \= {v:k for k,v in original.items()} print(inverted)   \# Handle duplicate values multi \= {"a":1,"b":2,"c":1} inv\_multi \= defaultdict(list) for k,v in multi.items():     inv\_multi\[v\].append(k) print(dict(inv\_multi))  |  |  📤  OUTPUT {1:'a', 2:'b', 3:'c'} {1: \['a', 'c'\], 2: \['b'\]}  |
| :---- | :---- | :---- |

| *💡 Simple inversion works when values are unique. Always handle duplicate values by grouping — critical for reverse-lookup tables in backend systems.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q7. Group a list of records by a key field.**

|  📥  INPUT from collections import defaultdict records \= \[     {"dept":"Eng","name":"Alice"},     {"dept":"HR","name":"Bob"},     {"dept":"Eng","name":"Carol"},     {"dept":"HR","name":"Dave"}, \] grouped \= defaultdict(list) for r in records:     grouped\[r\["dept"\]\].append(r\["name"\]) print(dict(grouped))  |  |  📤  OUTPUT {'Eng': \['Alice', 'Carol'\], 'HR': \['Bob', 'Dave'\]}  |
| :---- | :---- | :---- |

| *💡 This is essentially a SQL GROUP BY in Python. Extremely common in data engineering ETL, Walmart inventory grouping, Amazon order aggregation.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q8. Implement word frequency count from a text string.**

|  📥  INPUT import re from collections import Counter text \= "the quick brown fox jumps over the lazy dog the fox" words \= re.findall(r'w+', text.lower()) freq \= Counter(words) top3 \= freq.most\_common(3) print(dict(freq)) print("Top 3:", top3)  |  |  📤  OUTPUT {'the':3,'quick':1,'brown':1,'fox':2,...} Top 3: \[('the',3),('fox',2),('quick',1)\]  |
| :---- | :---- | :---- |

| *💡 Real-world NLP preprocessing step. re.findall handles punctuation. Counter.most\_common() uses a heap internally — O(n log k) for top-k.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q9. Find two numbers in a list that sum to target using a dict.**

|  📥  INPUT def two\_sum(nums, target):     seen \= {}     for i, n in enumerate(nums):         complement \= target \- n         if complement in seen:             return \[seen\[complement\], i\]         seen\[n\] \= i     return \[\]   print(two\_sum(\[2,7,11,15\], 9)) print(two\_sum(\[3,2,4\], 6))  |  |  📤  OUTPUT \[0, 1\] \[1, 2\]  |
| :---- | :---- | :---- |

| *💡 O(n) time, O(n) space using hash map vs O(n²) brute force. This is LeetCode's most solved problem — every FAANG company asks a variant.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q10. Implement a phone book using nested dictionaries.**

|  📥  INPUT phonebook \= {} def add\_contact(name, phone, email):     phonebook\[name\] \= {"phone":phone,"email":email} def lookup(name):     return phonebook.get(name, "Not found") add\_contact("Alice","555-1234","alice@co.com") add\_contact("Bob","555-5678","bob@co.com") print(lookup("Alice")) print(lookup("Charlie"))  |  |  📤  OUTPUT {'phone':'555-1234','email':'alice@co.com'} Not found  |
| :---- | :---- | :---- |

| *💡 Nested dicts model real-world entities. In production, this becomes a NoSQL document (DynamoDB at Amazon), but the Python dict pattern is identical.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q11. Detect if two strings are anagrams using a dictionary.**

|  📥  INPUT def is\_anagram(s1, s2):     if len(s1) \!= len(s2): return False     count \= {}     for c in s1:         count\[c\] \= count.get(c, 0\) \+ 1     for c in s2:         count\[c\] \= count.get(c, 0\) \- 1         if count\[c\] \< 0: return False     return True print(is\_anagram("listen","silent")) print(is\_anagram("hello","world"))  |  |  📤  OUTPUT True False  |
| :---- | :---- | :---- |

| *💡 O(n) time. Alternative: Counter(s1) \== Counter(s2). String comparison questions always appear in Amazon OA rounds.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q12. LRU Cache using OrderedDict — full implementation.**

|  📥  INPUT from collections import OrderedDict class LRUCache:     def \_\_init\_\_(self, cap): self.cap=cap; self.d=OrderedDict()     def get(self, k):         if k not in self.d: return \-1         self.d.move\_to\_end(k); return self.d\[k\]     def put(self, k, v):         if k in self.d: self.d.move\_to\_end(k)         self.d\[k\]=v         if len(self.d)\>self.cap: self.d.popitem(0) c=LRUCache(2) c.put(1,1); c.put(2,2) print(c.get(1)); c.put(3,3) print(c.get(2))  |  |  📤  OUTPUT 1 \-1  |
| :---- | :---- | :---- |

| *💡 OrderedDict gives O(1) operations. Real systems use Redis for distributed LRU — but this pattern is asked at every fintech interview.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q13. Implement a trie using nested dictionaries.**

|  📥  INPUT class Trie:     def \_\_init\_\_(self): self.root \= {}     def insert(self, word):         node \= self.root         for c in word:             node \= node.setdefault(c, {})         node\['\#'\] \= True     def search(self, word):         node \= self.root         for c in word:             if c not in node: return False             node \= node\[c\]         return '\#' in node t \= Trie() t.insert("apple"); t.insert("app") print(t.search("apple")) print(t.search("ap"))  |  |  📤  OUTPUT True False  |
| :---- | :---- | :---- |

| *💡 Nested dicts naturally model trie nodes. Used in autocomplete, spell-checkers, and URL routing — common at Amazon search team interviews.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q14. Find all subarrays with a given sum using prefix-sum dict.**

|  📥  INPUT def subarray\_sum(nums, k):     count \= 0     prefix \= {0: 1}     curr \= 0     for n in nums:         curr \+= n         count \+= prefix.get(curr \- k, 0\)         prefix\[curr\] \= prefix.get(curr, 0\) \+ 1     return count   print(subarray\_sum(\[1,1,1\], 2)) print(subarray\_sum(\[3,4,7,2,-3,1,4,2\], 7))  |  |  📤  OUTPUT 2 4  |
| :---- | :---- | :---- |

| *💡 Prefix sum \+ hash map gives O(n). This is a fundamental pattern in data analytics — counting windows matching a threshold in time-series data.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q15. Deep merge two nested dictionaries recursively.**

|  📥  INPUT def deep\_merge(base, override):     result \= dict(base)     for k, v in override.items():         if k in result and isinstance(result\[k\],dict) and isinstance(v,dict):             result\[k\] \= deep\_merge(result\[k\], v)         else:             result\[k\] \= v     return result d1 \= {"a":1,"b":{"x":10,"y":20},"c":3} d2 \= {"b":{"y":99,"z":30},"d":4} print(deep\_merge(d1, d2))  |  |  📤  OUTPUT {'a':1,'b':{'x':10,'y':99,'z':30},'c':3,'d':4}  |
| :---- | :---- | :---- |

| *💡 Shallow merge with \*\* loses nested keys. Deep merge is essential for config management systems (infrastructure-as-code, feature flags) at FAANG companies.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q16. Implement a consistent hash ring for distributed caching.**

|  📥  INPUT import hashlib class HashRing:     def \_\_init\_\_(self, nodes, replicas=3):         self.ring \= {}         self.keys \= \[\]         for node in nodes:             for i in range(replicas):                 h \= int(hashlib.md5(f"{node}-{i}".encode()).hexdigest(),16)                 self.ring\[h\] \= node                 self.keys.append(h)         self.keys.sort()     def get\_node(self, key):         h \= int(hashlib.md5(key.encode()).hexdigest(),16)         for k in self.keys:             if h \<= k: return self.ring\[k\]         return self.ring\[self.keys\[0\]\] ring \= HashRing(\["S1","S2","S3"\]) print(ring.get\_node("user:1001"))  |  |  📤  OUTPUT S2  |
| :---- | :---- | :---- |

| *💡 Consistent hashing minimizes remapping when nodes join/leave. Core concept behind Amazon DynamoDB and Redis Cluster routing.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q17. Build an inverted index for full-text search.**

|  📥  INPUT from collections import defaultdict def build\_index(docs):     index \= defaultdict(set)     for doc\_id, text in docs.items():         for word in text.lower().split():             index\[word\].add(doc\_id)     return index def search(index, query):     terms \= query.lower().split()     result \= index\[terms\[0\]\]     for t in terms\[1:\]:         result \= result & index\[t\]     return result docs \= {1:"python data engineering",2:"python backend dev",3:"data science ml"} idx \= build\_index(docs) print(search(idx, "python data"))  |  |  📤  OUTPUT {1}  |
| :---- | :---- | :---- |

| *💡 Inverted indexes power Elasticsearch and search engines. AND queries use set intersection — directly maps to how Amazon product search works.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q18. Implement memoization using a dictionary decorator.**

|  📥  INPUT import functools def memoize(func):     cache \= {}     @functools.wraps(func)     def wrapper(\*args):         if args not in cache:             cache\[args\] \= func(\*args)         return cache\[args\]     return wrapper   @memoize def fib(n):     if n \< 2: return n     return fib(n-1) \+ fib(n-2)   print(\[fib(i) for i in range(10)\]) \# Built-in: @functools.lru\_cache(maxsize=None)  |  |  📤  OUTPUT \[0,1,1,2,3,5,8,13,21,34\]  |
| :---- | :---- | :---- |

| *💡 Manual memoization shows deep understanding. Use functools.lru\_cache in production. Dynamic programming with memoization is asked at Amazon SDE-2/SDE-3.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q19. Detect cycle in a directed graph using dict adjacency list.**

|  📥  INPUT def has\_cycle(graph):     WHITE,GRAY,BLACK \= 0,1,2     color \= {n:WHITE for n in graph}     def dfs(node):         color\[node\] \= GRAY         for nei in graph.get(node,\[\]):             if color\[nei\]==GRAY: return True             if color\[nei\]==WHITE and dfs(nei): return True         color\[node\] \= BLACK         return False     return any(dfs(n) for n in graph if color\[n\]==WHITE) g \= {0:\[1\],1:\[2\],2:\[0\],3:\[4\],4:\[\]} print(has\_cycle(g))  |  |  📤  OUTPUT True  |
| :---- | :---- | :---- |

| *💡 3-color DFS: WHITE=unvisited, GRAY=in-stack, BLACK=done. GRAY→GRAY edge \= cycle. Used in dependency resolution and build systems (Gradle, Maven).* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q20. Implement a time-based key-value store.**

|  📥  INPUT from collections import defaultdict import bisect class TimeMap:     def \_\_init\_\_(self): self.store \= defaultdict(list)     def set(self, key, val, ts):         self.store\[key\].append((ts, val))     def get(self, key, ts):         if key not in self.store: return ""         pairs \= self.store\[key\]         i \= bisect.bisect\_right(pairs, (ts, chr(127)))         return pairs\[i-1\]\[1\] if i \> 0 else "" tm \= TimeMap() tm.set("foo","bar",1); tm.set("foo","bar2",4) print(tm.get("foo",3)) print(tm.get("foo",5))  |  |  📤  OUTPUT bar bar2  |
| :---- | :---- | :---- |

| *💡 Binary search on sorted timestamps gives O(log n) get. Directly models time-series storage used in trading platforms, IoT systems, and Walmart price tracking.* |
| :---- |

| 🔤  STRINGS — 20 Interview Questions |
| :---: |

| ⚡ EASY |
| :---: |

**Q1. Are Python strings mutable? Demonstrate string immutability.**

|  📥  INPUT s \= "hello" print(id(s)) s \= s \+ " world" print(id(s)) \# s\[0\] \= 'H'  ← TypeError: 'str' does not support item assignment print(s)  |  |  📤  OUTPUT 140234567890  (original id) 140234567999  (new object id) hello world  |
| :---- | :---- | :---- |

| *💡 Strings are immutable — every 'modification' creates a new object. Use list join for building large strings (O(n) vs O(n²) concatenation).* |
| :---- |

| ⚡ EASY |
| :---: |

**Q2. How do you reverse a string in Python?**

|  📥  INPUT s \= "Hello, World\!" rev \= s\[::-1\] rev2 \= ''.join(reversed(s)) \# Word reversal words\_rev \= ' '.join(s.split()\[::-1\]) print(rev) print(rev2) print(words\_rev)  |  |  📤  OUTPUT \!dlroW ,olleH \!dlroW ,olleH World\! Hello,  |
| :---- | :---- | :---- |

| *💡 Slice \[::-1\] is most Pythonic. reversed() is a lazy iterator. Word reversal is a common variant asked at Amazon OA.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q3. Check if a string is a palindrome.**

|  📥  INPUT def is\_palindrome(s):     s \= ''.join(c.lower() for c in s if c.isalnum())     return s \== s\[::-1\]   print(is\_palindrome("A man a plan a canal Panama")) print(is\_palindrome("race a car")) print(is\_palindrome("Was it a car or a cat I saw"))  |  |  📤  OUTPUT True False True  |
| :---- | :---- | :---- |

| *💡 Clean alphanumeric-only comparison handles punctuation/spaces. Two-pointer approach uses O(1) space — ask interviewers which variant they want.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q4. Count occurrences of each character in a string.**

|  📥  INPUT from collections import Counter s \= "mississippi" freq \= Counter(s) print(dict(freq)) print(freq.most\_common(3)) \# Manual approach manual \= {} for c in s: manual\[c\] \= manual.get(c,0) \+ 1  |  |  📤  OUTPUT {'m':1,'i':4,'s':4,'p':2} \[('i',4),('s',4),('p',2)\]  |
| :---- | :---- | :---- |

| *💡 Counter is O(n). In Python 3.10+ Counter preserves insertion order. Used heavily in string parsing for log analysis.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q5. How do you split and join strings?**

|  📥  INPUT csv \= "Alice,30,Engineer,New York" parts \= csv.split(",") print(parts) print(parts\[0\], parts\[2\])   words \= \["Python", "is", "awesome"\] sentence \= " ".join(words) pipe \= " | ".join(words) print(sentence) print(pipe)  |  |  📤  OUTPUT \['Alice', '30', 'Engineer', 'New York'\] Alice Engineer Python is awesome Python | is | awesome  |
| :---- | :---- | :---- |

| *💡 split/join are fundamental for CSV parsing in ETL pipelines. ''.join(list) is O(n) while repeated \+= is O(n²) — critical performance difference.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q6. Find the longest substring without repeating characters.**

|  📥  INPUT def length\_of\_longest(s):     char\_idx \= {}     left \= max\_len \= 0     for right, c in enumerate(s):         if c in char\_idx and char\_idx\[c\] \>= left:             left \= char\_idx\[c\] \+ 1         char\_idx\[c\] \= right         max\_len \= max(max\_len, right \- left \+ 1\)     return max\_len print(length\_of\_longest("abcabcbb")) print(length\_of\_longest("pwwkew"))  |  |  📤  OUTPUT 3 3  |
| :---- | :---- | :---- |

| *💡 Sliding window with hash map — O(n). Window contracts when duplicate found. Appears in Amazon, Walmart, and virtually every fintech interview.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q7. Implement string compression (run-length encoding).**

|  📥  INPUT def compress(s):     if not s: return s     result, count \= \[\], 1     for i in range(1, len(s)):         if s\[i\] \== s\[i-1\]:             count \+= 1         else:             result.append(s\[i-1\] \+ (str(count) if count\>1 else ''))             count \= 1     result.append(s\[-1\] \+ (str(count) if count\>1 else ''))     compressed \= ''.join(result)     return compressed if len(compressed) \< len(s) else s print(compress("aabcccdddd")) print(compress("abc"))  |  |  📤  OUTPUT a2bc3d4 abc  |
| :---- | :---- | :---- |

| *💡 Only return compressed if shorter — real-world requirement\! Used in data compression pipelines, image encoding, and network packet optimization.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q8. Check if one string is a rotation of another.**

|  📥  INPUT def is\_rotation(s1, s2):     if len(s1) \!= len(s2): return False     return s2 in (s1 \+ s1)   print(is\_rotation("abcde", "cdeab")) print(is\_rotation("abcde", "abced")) print(is\_rotation("waterbottle","erbottlewat"))  |  |  📤  OUTPUT True False True  |
| :---- | :---- | :---- |

| *💡 Elegant O(n) trick: s2 is always a substring of s1+s1 if it's a rotation. Naive O(n²) check of all rotations is wrong for interviews.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q9. Find all anagram substrings in a string.**

|  📥  INPUT from collections import Counter def find\_anagrams(s, p):     res, pc \= \[\], Counter(p)     wc \= Counter(s\[:len(p)\])     if wc \== pc: res.append(0)     for i in range(len(p), len(s)):         wc\[s\[i\]\] \+= 1         old \= s\[i-len(p)\]         wc\[old\] \-= 1         if wc\[old\] \== 0: del wc\[old\]         if wc \== pc: res.append(i-len(p)+1)     return res print(find\_anagrams("cbaebabacd","abc"))  |  |  📤  OUTPUT \[0, 6\]  |
| :---- | :---- | :---- |

| *💡 Sliding window with Counter comparison: O(n). Comparing entire Counter each step makes it O(n\*k) — use difference tracking for true O(n).* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q10. Implement atoi (string to integer) manually.**

|  📥  INPUT def my\_atoi(s):     s \= s.lstrip()     if not s: return 0     sign, i, result \= 1, 0, 0     INT\_MAX, INT\_MIN \= 2\*\*31-1, \-(2\*\*31)     if s\[0\] in '+-':         sign \= \-1 if s\[0\]=='-' else 1         i \= 1     while i \< len(s) and s\[i\].isdigit():         result \= result\*10 \+ int(s\[i\])         i \+= 1     result \*= sign     return max(INT\_MIN, min(INT\_MAX, result)) print(my\_atoi("  \-42abc")) print(my\_atoi("2147483648"))  |  |  📤  OUTPUT \-42 2147483647  |
| :---- | :---- | :---- |

| *💡 Edge cases: leading whitespace, sign, non-digit chars, overflow (clamp to INT\_MAX/MIN). Common in fintech for parsing financial data feeds.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q11. Find the minimum window substring containing all chars of pattern.**

|  📥  INPUT from collections import Counter def min\_window(s, t):     need, have \= Counter(t), {}     formed, l, res \= 0, 0, (float('inf'),0,0)     req \= len(need)     for r, c in enumerate(s):         have\[c\] \= have.get(c,0) \+ 1         if c in need and have\[c\]==need\[c\]: formed+=1         while formed==req:             if r-l+1\<res\[0\]: res=(r-l+1,l,r)             have\[s\[l\]\]-=1             if s\[l\] in need and have\[s\[l\]\]\<need\[s\[l\]\]: formed-=1             l+=1     return s\[res\[1\]:res\[2\]+1\] if res\[0\]\!=float('inf') else "" print(min\_window("ADOBECODEBANC","ABC"))  |  |  📤  OUTPUT BANC  |
| :---- | :---- | :---- |

| *💡 Variable-size sliding window O(n). The 'formed' counter tracks when all required chars meet their frequency — key insight for this type.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q12. Validate balanced parentheses in a string.**

|  📥  INPUT def is\_balanced(s):     stack \= \[\]     mapping \= {')':'(', '}':'{', '\]':'\['}     for c in s:         if c in mapping:             top \= stack.pop() if stack else '\#'             if mapping\[c\] \!= top: return False         else:             stack.append(c)     return not stack   print(is\_balanced("()\[\]{()}")) print(is\_balanced("(\[)\]")) print(is\_balanced("{\[()\]}"))  |  |  📤  OUTPUT True False True  |
| :---- | :---- | :---- |

| *💡 Stack-based O(n) solution handles all bracket types. Variations include counting minimum additions/removals — asked at Amazon SDE rounds for parser validation.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q13. Implement KMP string matching algorithm.**

|  📥  INPUT def kmp\_search(text, pattern):     def build\_lps(p):         lps, length, i \= \[0\]\*len(p), 0, 1         while i \< len(p):             if p\[i\]==p\[length\]: length+=1; lps\[i\]=length; i+=1             elif length: length=lps\[length-1\]             else: lps\[i\]=0; i+=1         return lps     lps \= build\_lps(pattern)     i \= j \= 0; positions \= \[\]     while i \< len(text):         if text\[i\]==pattern\[j\]: i+=1; j+=1         if j==len(pattern): positions.append(i-j); j=lps\[j-1\]         elif i\<len(text) and text\[i\]\!=pattern\[j\]:             if j: j=lps\[j-1\]             else: i+=1     return positions print(kmp\_search("ABABDABACDABABCABAB","ABABCABAB"))  |  |  📤  OUTPUT \[10\]  |
| :---- | :---- | :---- |

| *💡 KMP avoids redundant comparisons using the LPS (Longest Proper Prefix which is also Suffix) array — O(n+m) vs O(nm) naive. Asked at senior FAANG roles.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q14. Find the longest palindromic substring (Manacher's algorithm).**

|  📥  INPUT def longest\_palindrome(s):     t \= '\#' \+ '\#'.join(s) \+ '\#'     n, p, c, r \= len(t), \[0\]\*len(t), 0, 0     for i in range(n):         mirror \= 2\*c \- i         if i \< r: p\[i\] \= min(r-i, p\[mirror\])         while i+p\[i\]+1\<n and i-p\[i\]-1\>=0 and t\[i+p\[i\]+1\]==t\[i-p\[i\]-1\]:             p\[i\]+=1         if i+p\[i\]\>r: c,r=i,i+p\[i\]     max\_len,center \= max((v,i) for i,v in enumerate(p))     return s\[(center-max\_len)//2:(center+max\_len)//2\] print(longest\_palindrome("babad")) print(longest\_palindrome("cbbd"))  |  |  📤  OUTPUT bab bb  |
| :---- | :---- | :---- |

| *💡 Manacher's runs in O(n) vs O(n²) expand-around-center. The transformed string with \# handles even/odd lengths uniformly.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q15. Implement Rabin-Karp rolling hash for pattern matching.**

|  📥  INPUT def rabin\_karp(text, pattern):     BASE, MOD \= 256, 10\*\*9+7     n, m \= len(text), len(pattern)     if m \> n: return \[\]     ph \= th \= h \= 1     for \_ in range(m-1): h \= (h\*BASE) % MOD     for i in range(m):         ph \= (BASE\*ph \+ ord(pattern\[i\])) % MOD         th \= (BASE\*th \+ ord(text\[i\])) % MOD     result \= \[\]     for i in range(n-m+1):         if ph==th and text\[i:i+m\]==pattern: result.append(i)         if i\<n-m:             th=(BASE\*(th-ord(text\[i\])\*h)+ord(text\[i+m\]))%MOD     return result print(rabin\_karp("GEEKS FOR GEEKS","GEEK"))  |  |  📤  OUTPUT \[0, 10\]  |
| :---- | :---- | :---- |

| *💡 Rolling hash updates in O(1) per step — O(n+m) average. Used in plagiarism detection, file deduplication in distributed systems.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q16. Count distinct palindromic substrings.**

|  📥  INPUT def count\_distinct\_palindromes(s):     palindromes \= set()     n \= len(s)     def expand(l, r):         while l \>= 0 and r \< n and s\[l\] \== s\[r\]:             palindromes.add(s\[l:r+1\])             l \-= 1; r \+= 1     for i in range(n):         expand(i, i)    \# odd length         expand(i, i+1)  \# even length     return len(palindromes)   print(count\_distinct\_palindromes("abaab")) print(count\_distinct\_palindromes("abcba"))  |  |  📤  OUTPUT 5 6  |
| :---- | :---- | :---- |

| *💡 Using a set ensures distinctness. Expand-around-center finds all palindromic substrings in O(n²). A suffix automaton gives O(n) but is rarely required.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q17. Implement string tokenizer for a simple expression parser.**

|  📥  INPUT import re def tokenize(expr):     token\_spec \= \[         ('NUM',   r'd+.?d\*'),         ('OP',    r'\[+-\*/\]'),         ('LPAREN',r'('),         ('RPAREN',r')'),         ('SKIP',  r's+'),     \]     pattern \= '|'.join(f'(?P\<{name}\>{regex})' for name,regex in token\_spec)     tokens \= \[\]     for m in re.finditer(pattern, expr):         if m.lastgroup \!= 'SKIP':             tokens.append((m.lastgroup, m.group()))     return tokens print(tokenize("3.14 \+ (2 \* 5)"))  |  |  📤  OUTPUT \[('NUM','3.14'),('OP','+'),('LPAREN','('),  ('NUM','2'),('OP','\*'),('NUM','5'),('RPAREN',')')\]  |
| :---- | :---- | :---- |

| *💡 Named groups in regex enable clean tokenizers. Used in building DSLs, SQL parsers, and configuration file parsers in backend systems.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q18. Implement wildcard pattern matching (? and \*).**

|  📥  INPUT def wildcard\_match(s, p):     m, n \= len(s), len(p)     dp \= \[\[False\]\*(n+1) for \_ in range(m+1)\]     dp\[0\]\[0\] \= True     for j in range(1, n+1):         if p\[j-1\]=='\*': dp\[0\]\[j\] \= dp\[0\]\[j-1\]     for i in range(1, m+1):         for j in range(1, n+1):             if p\[j-1\]=='\*':                 dp\[i\]\[j\] \= dp\[i-1\]\[j\] or dp\[i\]\[j-1\]             elif p\[j-1\]=='?' or s\[i-1\]==p\[j-1\]:                 dp\[i\]\[j\] \= dp\[i-1\]\[j-1\]     return dp\[m\]\[n\] print(wildcard\_match("adceb","\*a\*b")) print(wildcard\_match("acdcb","a\*c?b"))  |  |  📤  OUTPUT True False  |
| :---- | :---- | :---- |

| *💡 DP solution O(m\*n). \* matches zero or more chars; ? matches exactly one. Used in file glob matching, S3 bucket policies, IAM permission patterns.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q19. Build a suffix array for efficient string queries.**

|  📥  INPUT def suffix\_array(s):     n \= len(s)     suffixes \= sorted(range(n), key=lambda i: s\[i:\])     return suffixes   def lcp\_array(s, sa):     n \= len(s)     rank \= \[0\]\*n     for i,v in enumerate(sa): rank\[v\]=i     lcp, h \= \[0\]\*n, 0     for i in range(n):         if rank\[i\]\>0:             j \= sa\[rank\[i\]-1\]             while i+h\<n and j+h\<n and s\[i+h\]==s\[j+h\]: h+=1             lcp\[rank\[i\]\] \= h             if h: h-=1     return lcp s \= "banana" sa \= suffix\_array(s) print("SA:", sa) print("LCP:", lcp\_array(s, sa))  |  |  📤  OUTPUT SA: \[5,3,1,0,4,2\] LCP: \[0,1,3,0,0,2\]  |
| :---- | :---- | :---- |

| *💡 Suffix arrays \+ LCP enable O(n log n) construction and O(log n) pattern search. Foundation of bioinformatics tools and database full-text indexing.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q20. Serialize and deserialize a binary tree to/from string.**

|  📥  INPUT class TreeNode:     def \_\_init\_\_(self,v,l=None,r=None): self.val=v;self.left=l;self.right=r def serialize(root):     if not root: return "null"     return f"{root.val},{serialize(root.left)},{serialize(root.right)}" def deserialize(data):     vals \= iter(data.split(','))     def helper():         v \= next(vals)         if v=="null": return None         node \= TreeNode(int(v))         node.left \= helper(); node.right \= helper()         return node     return helper() root \= TreeNode(1,TreeNode(2),TreeNode(3,TreeNode(4),TreeNode(5))) s \= serialize(root) print(s\[:30\],"...") tree \= deserialize(s) print(tree.val, tree.right.left.val)  |  |  📤  OUTPUT 1,2,null,null,3,4,null ... 1 4  |
| :---- | :---- | :---- |

| *💡 Pre-order serialization naturally reconstructs the tree. Used for caching tree structures in Redis, Kafka messaging, and distributed task queues.* |
| :---- |

| 🔢  NUMERIC — 20 Interview Questions |
| :---: |

| ⚡ EASY |
| :---: |

**Q1. What are Python's numeric types and their differences?**

|  📥  INPUT \# int: arbitrary precision a \= 10 \*\* 50 \# float: 64-bit IEEE 754 b \= 3.14 \# complex c \= 2 \+ 3j \# Decimal for exact finance math from decimal import Decimal d \= Decimal("0.1") \+ Decimal("0.2") print(0.1 \+ 0.2)       \# float error print(d)               \# exact  |  |  📤  OUTPUT 0.30000000000000004 0.3  |
| :---- | :---- | :---- |

| *💡 Critical for fintech\! Floats have rounding errors — always use Decimal for monetary calculations. Never use float for prices, interest rates, or balances.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q2. How do you check if a number is prime?**

|  📥  INPUT def is\_prime(n):     if n \< 2: return False     if n \== 2: return True     if n % 2 \== 0: return False     for i in range(3, int(n\*\*0.5)+1, 2):         if n % i \== 0: return False     return True   primes \= \[n for n in range(2,30) if is\_prime(n)\] print(primes)  |  |  📤  OUTPUT \[2, 3, 5, 7, 11, 13, 17, 19, 23, 29\]  |
| :---- | :---- | :---- |

| *💡 O(√n) trial division. Only check odd numbers after 2\. For generating many primes use Sieve of Eratosthenes O(n log log n).* |
| :---- |

| ⚡ EASY |
| :---: |

**Q3. Implement FizzBuzz with numeric operators.**

|  📥  INPUT for i in range(1, 21):     if i % 15 \== 0:   print("FizzBuzz")     elif i % 3 \== 0:  print("Fizz")     elif i % 5 \== 0:  print("Buzz")     else:             print(i)  |  |  📤  OUTPUT 1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz 16 17 Fizz 19 Buzz  |
| :---- | :---- | :---- |

| *💡 Check 15 FIRST (LCM of 3 and 5), not last. A classic screening question — wrong order is an immediate red flag in interviews.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q4. Find GCD and LCM of two numbers.**

|  📥  INPUT import math a, b \= 48, 18 gcd \= math.gcd(a, b) lcm \= abs(a\*b) // gcd print(f"GCD({a},{b}) \= {gcd}") print(f"LCM({a},{b}) \= {lcm}") \# Python 3.9+ supports multiple args print(math.gcd(12, 18, 24))  |  |  📤  OUTPUT GCD(48,18) \= 6 LCM(48,18) \= 144 6  |
| :---- | :---- | :---- |

| *💡 LCM \= (a\*b) / GCD. Used in scheduling systems (cron job interval calculations), signal processing, and fractional arithmetic in financial systems.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q5. How do you handle integer overflow in Python?**

|  📥  INPUT \# Python ints have arbitrary precision\! big \= 2 \*\* 1000 print(type(big)) print(str(big)\[:20\], "...")   \# sys.maxsize for platform max import sys print(sys.maxsize)   \# Simulating C-style 32-bit overflow def to\_int32(n):     n \= n & 0xFFFFFFFF     return n if n \< 2\*\*31 else n \- 2\*\*32 print(to\_int32(2\*\*31))  |  |  📤  OUTPUT \<class 'int'\> 10715086071862673209 ... 9223372036854775807 \-2147483648  |
| :---- | :---- | :---- |

| *💡 Python ints never overflow natively — unlike C/Java. For LeetCode-style problems requiring 32-bit bounds, use the masking technique shown.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q6. Implement binary search on a sorted array.**

|  📥  INPUT def binary\_search(arr, target):     left, right \= 0, len(arr)-1     while left \<= right:         mid \= left \+ (right-left)//2  \# Avoids overflow         if arr\[mid\] \== target:             return mid         elif arr\[mid\] \< target:             left \= mid \+ 1         else:             right \= mid \- 1     return \-1 arr \= \[1,3,5,7,9,11,13,15,17,19\] print(binary\_search(arr, 7)) print(binary\_search(arr, 6))  |  |  📤  OUTPUT 3 \-1  |
| :---- | :---- | :---- |

| *💡 Use mid \= left \+ (right-left)//2 to prevent integer overflow (critical in Java/C++; Python doesn't overflow but good habit). O(log n) — fundamental for sorted data.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q7. Find square root without using math.sqrt (Newton's method).**

|  📥  INPUT def my\_sqrt(n, precision=1e-10):     if n \< 0: raise ValueError("Negative input")     if n \== 0: return 0     x \= float(n)     while True:         x1 \= (x \+ n/x) / 2         if abs(x \- x1) \< precision:             return x1         x \= x1   \# Integer floor sqrt using binary search def int\_sqrt(n):     l,r \= 0,n     while l\<=r:         m=l+(r-l)//2         if m\*m\<=n\<(m+1)\*\*2: return m         elif m\*m\<n: l=m+1         else: r=m-1 print(round(my\_sqrt(16),5)) print(int\_sqrt(8))  |  |  📤  OUTPUT 4.0 2  |
| :---- | :---- | :---- |

| *💡 Newton-Raphson converges quadratically. Binary search version is O(log n) and avoids floating point for integer sqrt. Both approaches asked in senior interviews.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q8. Calculate power function efficiently (fast exponentiation).**

|  📥  INPUT def fast\_pow(base, exp, mod=None):     result \= 1     base \= base % mod if mod else base     while exp \> 0:         if exp % 2 \== 1:             result \= (result\*base%mod) if mod else result\*base         exp //= 2         base \= (base\*base%mod) if mod else base\*base     return result   print(fast\_pow(2, 10)) print(fast\_pow(2, 10, 1000)) print(fast\_pow(3, 100, 10\*\*9+7))  |  |  📤  OUTPUT 1024 24 981453966  |
| :---- | :---- | :---- |

| *💡 O(log n) vs O(n) naive. Modular exponentiation is essential in cryptography (RSA), hashing, and competitive programming. Asked in fintech system design.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q9. Find all prime factors of a number.**

|  📥  INPUT def prime\_factors(n):     factors \= \[\]     d \= 2     while d \* d \<= n:         while n % d \== 0:             factors.append(d)             n //= d         d \+= 1     if n \> 1:         factors.append(n)     return factors   print(prime\_factors(360)) print(prime\_factors(97)) print(prime\_factors(2\*\*5 \* 3\*\*2 \* 7))  |  |  📤  OUTPUT \[2, 2, 2, 3, 3, 5\] \[97\] \[2, 2, 2, 2, 2, 3, 3, 7\]  |
| :---- | :---- | :---- |

| *💡 Trial division up to √n is O(√n). For n up to 10^12, use Pollard's rho. Common in cryptography, LCM/GCD batch operations, and database sharding strategies.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q10. Count set bits (Hamming weight) in an integer.**

|  📥  INPUT def count\_bits(n):     count \= 0     while n:         count \+= n & 1         n \>\>= 1     return count   \# Brian Kernighan's algorithm: O(set bits) def count\_bits\_fast(n):     count \= 0     while n:         n &= (n-1)  \# Clears lowest set bit         count \+= 1     return count   print(count\_bits(255)) print(count\_bits\_fast(1023)) print(bin(255).count('1'))  |  |  📤  OUTPUT 8 10 8  |
| :---- | :---- | :---- |

| *💡 n & (n-1) clears the lowest set bit — Kernighan's trick. Used in network subnet masks, Redis bitmaps for user activity tracking, feature flag systems.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q11. Implement number to Roman numeral conversion.**

|  📥  INPUT def to\_roman(num):     vals \= \[1000,900,500,400,100,90,50,40,10,9,5,4,1\]     syms \= \["M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"\]     result \= ""     for v,s in zip(vals,syms):         while num \>= v:             result \+= s             num \-= v     return result for n in \[3749, 58, 1994\]:     print(f"{n} → {to\_roman(n)}")  |  |  📤  OUTPUT 3749 → MMMDCCXLIX 58 → LVIII 1994 → MCMXCIV  |
| :---- | :---- | :---- |

| *💡 Greedy from largest to smallest — always subtract the largest possible value. Subtractive notation (CM=900, CD=400) must come before their additive forms.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q12. Implement arbitrary precision addition without using Python's big int.**

|  📥  INPUT def big\_add(a: str, b: str) \-\> str:     i, j, carry \= len(a)-1, len(b)-1, 0     result \= \[\]     while i\>=0 or j\>=0 or carry:         x \= int(a\[i\]) if i\>=0 else 0         y \= int(b\[j\]) if j\>=0 else 0         total \= x \+ y \+ carry         carry, digit \= divmod(total, 10\)         result.append(str(digit))         i-=1; j-=1     return ''.join(reversed(result))   print(big\_add("9999999999999999999","1")) print(big\_add("999","999"))  |  |  📤  OUTPUT 10000000000000000000 1998  |
| :---- | :---- | :---- |

| *💡 Simulates how hardware adds numbers. Important for understanding arbitrary precision in Python and for implementing BigInteger in languages without it.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q13. Find the nth Fibonacci number in O(log n) using matrix exponentiation.**

|  📥  INPUT import numpy as np def fib\_matrix(n):     def mat\_mul(A, B):         return \[\[A\[0\]\[0\]\*B\[0\]\[0\]+A\[0\]\[1\]\*B\[1\]\[0\],                  A\[0\]\[0\]\*B\[0\]\[1\]+A\[0\]\[1\]\*B\[1\]\[1\]\],                 \[A\[1\]\[0\]\*B\[0\]\[0\]+A\[1\]\[1\]\*B\[1\]\[0\],                  A\[1\]\[0\]\*B\[0\]\[1\]+A\[1\]\[1\]\*B\[1\]\[1\]\]\]     def mat\_pow(M, n):         if n==1: return M         if n%2==0: half=mat\_pow(M,n//2); return mat\_mul(half,half)         return mat\_mul(M,mat\_pow(M,n-1))     M=\[\[1,1\],\[1,0\]\]     return mat\_pow(M,n)\[0\]\[1\] print(\[fib\_matrix(i) for i in range(1,11)\])  |  |  📤  OUTPUT \[1, 1, 2, 3, 5, 8, 13, 21, 34, 55\]  |
| :---- | :---- | :---- |

| *💡 Matrix exponentiation gives O(log n) Fibonacci — critical for n \> 10^18. The identity \[\[1,1\],\[1,0\]\]^n gives Fibonacci by the defining recurrence.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q14. Implement a Monte Carlo π estimation.**

|  📥  INPUT import random def estimate\_pi(n\_samples=1\_000\_000):     inside \= sum(         1 for \_ in range(n\_samples)         if random.random()\*\*2 \+ random.random()\*\*2 \<= 1     )     return 4 \* inside / n\_samples   \# Vectorized version (much faster) import random random.seed(42) pi\_est \= estimate\_pi(1000000) print(f"Estimated π: {pi\_est:.4f}") print(f"Actual π:    {3.14159:.4f}")  |  |  📤  OUTPUT Estimated π: 3.1416 Actual π:    3.1416  |
| :---- | :---- | :---- |

| *💡 Monte Carlo methods are fundamental in quantitative finance for option pricing, risk modeling (VaR), and portfolio simulation. Law of Large Numbers ensures convergence.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q15. Implement Sieve of Eratosthenes for prime generation.**

|  📥  INPUT def sieve(n):     is\_prime \= bytearray(\[1\]) \* (n+1)     is\_prime\[0\] \= is\_prime\[1\] \= 0     for i in range(2, int(n\*\*0.5)+1):         if is\_prime\[i\]:             is\_prime\[i\*i::i\] \= bytearray(len(is\_prime\[i\*i::i\]))     return \[i for i,v in enumerate(is\_prime) if v\]   primes \= sieve(50) print(primes) print(f"Primes up to 10^6: {len(sieve(10\*\*6))}",       f"(should be 78498)")  |  |  📤  OUTPUT \[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47\] Primes up to 10^6: 78498 (should be 78498\)  |
| :---- | :---- | :---- |

| *💡 O(n log log n) with bytearray for memory efficiency. Use slice assignment for vectorized crossing-out — 10x faster than element-by-element. Used in cryptographic key generation.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q16. Implement numerical integration (Simpson's rule).**

|  📥  INPUT def simpsons(f, a, b, n=1000):     if n % 2: n \+= 1  \# n must be even     h \= (b \- a) / n     result \= f(a) \+ f(b)     for i in range(1, n):         coeff \= 4 if i%2 else 2         result \+= coeff \* f(a \+ i\*h)     return result \* h / 3   import math \# Integrate sin(x) from 0 to π (should be 2.0) val \= simpsons(math.sin, 0, math.pi) print(f"∫sin(x)dx \[0,π\] \= {val:.6f}") \# Integrate x² from 0 to 1 (should be 1/3) print(f"∫x²dx \[0,1\] \= {simpsons(lambda x:x\*\*2, 0, 1):.6f}")  |  |  📤  OUTPUT ∫sin(x)dx \[0,π\] \= 2.000000 ∫x²dx \[0,1\] \= 0.333333  |
| :---- | :---- | :---- |

| *💡 Simpson's rule has O(h⁴) error vs O(h²) for trapezoidal. Used in quantitative finance for pricing exotic options and calculating portfolio Greeks.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q17. Implement RSA encryption (simplified) using numeric operations.**

|  📥  INPUT def gcd(a,b): return a if b==0 else gcd(b,a%b) def mod\_inv(e,phi):     g,x,\_=extended\_gcd(e,phi); return x%phi if g==1 else None def extended\_gcd(a,b):     if a==0: return b,0,1     g,x,y=extended\_gcd(b%a,a); return g,y-(b//a)\*x,x def rsa\_demo():     p,q=61,53     n=p\*q; phi=(p-1)\*(q-1)     e=17     d=mod\_inv(e,phi)     msg=65     encrypted=pow(msg,e,n)     decrypted=pow(encrypted,d,n)     return encrypted,decrypted enc,dec=rsa\_demo() print(f"Encrypted: {enc}, Decrypted: {dec}")  |  |  📤  OUTPUT Encrypted: 2790, Decrypted: 65  |
| :---- | :---- | :---- |

| *💡 RSA relies on modular exponentiation (fast\_pow) and extended Euclidean algorithm. Python's pow(base,exp,mod) is optimized for this — essential knowledge for security-focused fintech roles.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q18. Implement median of a data stream using two heaps.**

|  📥  INPUT import heapq class MedianFinder:     def \_\_init\_\_(self):         self.lo \= \[\]  \# max heap (negate values)         self.hi \= \[\]  \# min heap     def add(self, num):         heapq.heappush(self.lo, \-num)         heapq.heappush(self.hi, \-heapq.heappop(self.lo))         if len(self.hi) \> len(self.lo):             heapq.heappush(self.lo, \-heapq.heappop(self.hi))     def median(self):         if len(self.lo) \> len(self.hi): return \-self.lo\[0\]         return (-self.lo\[0\] \+ self.hi\[0\]) / 2.0 mf \= MedianFinder() for n in \[5,2,3,4,1,6\]: mf.add(n) print(mf.median())  |  |  📤  OUTPUT 3.5  |
| :---- | :---- | :---- |

| *💡 Two-heap approach maintains sorted halves: O(log n) add, O(1) median. Critical for real-time analytics dashboards, trading latency monitoring, and SLA tracking at Amazon/Walmart.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q19. Solve the Josephus problem numerically.**

|  📥  INPUT def josephus(n, k):     """Find 0-indexed survivor position"""     pos \= 0     for i in range(2, n+1):         pos \= (pos \+ k) % i     return pos   \# Simulate for verification def josephus\_sim(n, k):     circle \= list(range(n))     idx \= 0     while len(circle) \> 1:         idx \= (idx \+ k \- 1\) % len(circle)         circle.pop(idx)         if idx \== len(circle): idx \= 0     return circle\[0\]   print(josephus(7, 3))       \# Mathematical O(n) print(josephus\_sim(7, 3))   \# Simulation O(n²)  |  |  📤  OUTPUT 3 3  |
| :---- | :---- | :---- |

| *💡 Mathematical O(n) recurrence: f(1,k)=0, f(n,k)=(f(n-1,k)+k)%n. The simulation is O(n²) with list pop. Classic combinatorics problem in algorithm interviews.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q20. Implement a fixed-point iteration numerical solver.**

|  📥  INPUT def fixed\_point(g, x0, tol=1e-10, max\_iter=1000):     """Solve x \= g(x) iteratively"""     x \= x0     for i in range(max\_iter):         x\_new \= g(x)         if abs(x\_new \- x) \< tol:             return x\_new, i+1         x \= x\_new     return x, max\_iter   import math \# Solve cos(x) \= x sol, iters \= fixed\_point(math.cos, 1.0) print(f"cos(x)=x solution: x={sol:.8f} in {iters} iters") \# Solve x \= 1 \+ 1/x (Golden ratio) sol2, \_ \= fixed\_point(lambda x: 1+1/x, 1.0) print(f"Golden ratio: {sol2:.8f}")  |  |  📤  OUTPUT cos(x)=x solution: x=0.73908513 in 68 iters Golden ratio: 1.61803399  |
| :---- | :---- | :---- |

| *💡 Fixed-point iteration underpins Newton's method, EM algorithm, and PageRank computation. Convergence requires |g'(x\*)| \< 1 — Banach fixed-point theorem.* |
| :---- |

| 🔷  SETS — 20 Interview Questions |
| :---: |

| ⚡ EASY |
| :---: |

**Q1. What is a Python set and its key properties?**

|  📥  INPUT s \= {1, 2, 3, 3, 2, 1} print(s)                    \# Duplicates removed print(type(s)) empty\_set \= set()           \# NOT {} (that's dict) print(type({}))             \# dict\! print(type(empty\_set))      \# set s.add(4) s.discard(10)               \# No error if missing print(s)  |  |  📤  OUTPUT {1, 2, 3} \<class 'set'\> \<class 'dict'\> \<class 'set'\> {1, 2, 3, 4}  |
| :---- | :---- | :---- |

| *💡 Sets are unordered, no duplicates, O(1) average lookup/insert. {} creates dict not set\! Use set() for empty set — a common interview gotcha.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q2. Perform set operations: union, intersection, difference.**

|  📥  INPUT A \= {1, 2, 3, 4, 5} B \= {4, 5, 6, 7, 8} print("Union:",       A | B) print("Intersect:",   A & B) print("Diff A-B:",    A \- B) print("Diff B-A:",    B \- A) print("Sym Diff:",    A ^ B) print("Subset:",      {1,2} \<= A) print("Superset:",    A \>= {1,2,3})  |  |  📤  OUTPUT Union:       {1,2,3,4,5,6,7,8} Intersect:   {4,5} Diff A-B:    {1,2,3} Diff B-A:    {6,7,8} Sym Diff:    {1,2,3,6,7,8} Subset:      True Superset:    True  |
| :---- | :---- | :---- |

| *💡 All set operations have clean operator syntax. & (intersection) is extremely useful for finding common elements in two datasets — core to data deduplication at scale.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q3. Remove duplicates from a list using a set.**

|  📥  INPUT \# Simple removal (order NOT preserved) lst \= \[3,1,4,1,5,9,2,6,5,3,5\] no\_dups \= list(set(lst)) print("Unordered:", sorted(no\_dups))   \# Order-preserved (use dict) seen \= dict.fromkeys(lst) ordered \= list(seen.keys()) print("Ordered:", ordered)  |  |  📤  OUTPUT Unordered: \[1, 2, 3, 4, 5, 6, 9\] Ordered: \[3, 1, 4, 5, 9, 2, 6\]  |
| :---- | :---- | :---- |

| *💡 list(set()) loses order. dict.fromkeys() preserves insertion order in Python 3.7+. Order matters in ETL pipelines — choose the right approach\!* |
| :---- |

| ⚡ EASY |
| :---: |

**Q4. Check for common elements between two lists using sets.**

|  📥  INPUT def has\_common(l1, l2):     return bool(set(l1) & set(l2))   def common\_elements(l1, l2):     return list(set(l1) & set(l2))   l1 \= \[1,2,3,4,5\] l2 \= \[4,5,6,7,8\] print(has\_common(l1, l2)) print(common\_elements(l1, l2)) print(not set(l1).isdisjoint(l2))  |  |  📤  OUTPUT True \[4, 5\] True  |
| :---- | :---- | :---- |

| *💡 Set intersection is O(min(len(l1),len(l2))) average. isdisjoint() short-circuits on first common element — use when you only need True/False, not the elements.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q5. What elements are in one set but not both (symmetric difference)?**

|  📥  INPUT users\_jan \= {"Alice","Bob","Carol","Dave"} users\_feb \= {"Bob","Carol","Eve","Frank"} \# Churned (left Jan, not in Feb) churned \= users\_jan \- users\_feb \# New (joined Feb, not in Jan) new\_users \= users\_feb \- users\_jan \# Changed either way changed \= users\_jan ^ users\_feb print("Churned:", churned) print("New:", new\_users) print("Changed:", changed)  |  |  📤  OUTPUT Churned: {'Alice', 'Dave'} New: {'Eve', 'Frank'} Changed: {'Alice','Dave','Eve','Frank'}  |
| :---- | :---- | :---- |

| *💡 Symmetric difference \= elements in exactly one set. Classic business analytics pattern for churn analysis, A/B test user tracking, and monthly cohort comparison.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q6. Find the union of multiple sets efficiently.**

|  📥  INPUT sets \= \[{1,2,3},{2,3,4},{3,4,5},{4,5,6}\] \# Method 1: reduce from functools import reduce result \= reduce(lambda a,b: a|b, sets) \# Method 2: set.union(\*sets) \- most efficient result2 \= set.union(\*sets) print(result) print(result \== result2) print(set.intersection(\*sets))  |  |  📤  OUTPUT {1, 2, 3, 4, 5, 6} True {3}  |
| :---- | :---- | :---- |

| *💡 set.union(\*sets) is more efficient than chained |. set.intersection(\*sets) finds elements in ALL sets — perfect for finding users active across all time periods.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q7. Implement a set-based visited tracker for graph BFS.**

|  📥  INPUT from collections import deque def bfs(graph, start):     visited \= set()     queue \= deque(\[start\])     visited.add(start)     order \= \[\]     while queue:         node \= queue.popleft()         order.append(node)         for nei in sorted(graph\[node\]):             if nei not in visited:                 visited.add(nei)                 queue.append(nei)     return order graph \= {0:\[1,2\],1:\[0,3\],2:\[0,3\],3:\[1,2,4\],4:\[3\]} print(bfs(graph, 0))  |  |  📤  OUTPUT \[0, 1, 2, 3, 4\]  |
| :---- | :---- | :---- |

| *💡 Set gives O(1) membership check vs O(n) list. Never use a list as 'visited' — it makes BFS O(V²) instead of O(V+E). Critical for large-scale graph processing.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q8. Find longest consecutive sequence using a set.**

|  📥  INPUT def longest\_consecutive(nums):     num\_set \= set(nums)     best \= 0     for n in num\_set:         if n-1 not in num\_set:  \# Start of sequence             length \= 1             while n \+ length in num\_set:                 length \+= 1             best \= max(best, length)     return best   print(longest\_consecutive(\[100,4,200,1,3,2\])) print(longest\_consecutive(\[0,3,7,2,5,8,4,6,0,1\]))  |  |  📤  OUTPUT 4 9  |
| :---- | :---- | :---- |

| *💡 O(n) because each number is visited at most twice. The key insight: only start counting from sequence beginnings (n-1 not in set). Amazon classic\!* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q9. Implement a spell checker using a set dictionary.**

|  📥  INPUT def load\_dict():     return {"python","java","code","data","engine","engineer",             "algorithm","structure","interview","amazon","walmart"}   def spell\_check(text, dictionary):     words \= text.lower().split()     misspelled \= \[w for w in words if w not in dictionary\]     suggestions \= {}     for word in misspelled:         \# Simple 1-char deletion suggestions         sug \= {word\[:i\]+word\[i+1:\] for i in range(len(word))} & dictionary         suggestions\[word\] \= list(sug)     return misspelled, suggestions   d \= load\_dict() bad, sug \= spell\_check("pythn data enginr interveiw", d) print(bad)  |  |  📤  OUTPUT \['pythn', 'enginr', 'interveiw'\]  |
| :---- | :---- | :---- |

| *💡 Set lookup is O(1) making spell check O(n words). Edit distance suggestion generation shows set operations for near-miss matching — used in search autocorrect.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q10. Power set generation — all subsets of a set.**

|  📥  INPUT def power\_set(lst):     result \= \[set()\]     for elem in lst:         result \+= \[s | {elem} for s in result\]     return result   ps \= power\_set(\[1, 2, 3\]) print(f"Power set size: {len(ps)}") for s in sorted(ps, key=len):     print(s)  |  |  📤  OUTPUT Power set size: 8 set() {1}  {2}  {3} {1, 2}  {1, 3}  {2, 3} {1, 2, 3}  |
| :---- | :---- | :---- |

| *💡 2^n subsets for n elements. Used in feature selection in ML, combinatorial optimization, and generating all possible access permission combinations in IAM systems.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q11. Find k-th largest element using a set (sorted order trick).**

|  📥  INPUT import heapq def kth\_largest(nums, k):     \# Method 1: min-heap of size k     heap \= \[\]     for n in nums:         heapq.heappush(heap, n)         if len(heap) \> k:             heapq.heappop(heap)     return heap\[0\]   \# Method 2: sorted set (no duplicates) def kth\_largest\_unique(nums, k):     return sorted(set(nums), reverse=True)\[k-1\]   print(kth\_largest(\[3,2,1,5,6,4\], 2)) print(kth\_largest\_unique(\[3,2,1,5,6,4\], 2))  |  |  📤  OUTPUT 5 5  |
| :---- | :---- | :---- |

| *💡 Min-heap gives O(n log k). The set approach removes duplicates first — clarify requirements with interviewer. 'kth largest unique' vs 'kth position' are different problems\!* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q12. Implement a disjoint set (Union-Find) data structure.**

|  📥  INPUT class UnionFind:     def \_\_init\_\_(self, n):         self.parent \= list(range(n))         self.rank \= \[0\] \* n         self.components \= n     def find(self, x):         if self.parent\[x\] \!= x:             self.parent\[x\] \= self.find(self.parent\[x\])  \# Path compression         return self.parent\[x\]     def union(self, x, y):         px, py \= self.find(x), self.find(y)         if px \== py: return False         if self.rank\[px\] \< self.rank\[py\]: px,py=py,px         self.parent\[py\] \= px         if self.rank\[px\]==self.rank\[py\]: self.rank\[px\]+=1         self.components \-= 1         return True uf \= UnionFind(5) uf.union(0,1); uf.union(1,2); uf.union(3,4) print(uf.find(0)==uf.find(2)) print(uf.components)  |  |  📤  OUTPUT True 2  |
| :---- | :---- | :---- |

| *💡 Path compression \+ union by rank gives near-O(1) amortized (inverse Ackermann). Used in Kruskal's MST, network connectivity, and Amazon's distributed service mesh topology.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q13. Find all unique triplets that sum to zero (3Sum problem).**

|  📥  INPUT def three\_sum(nums):     nums.sort()     result \= set()     n \= len(nums)     for i in range(n-2):         if i \> 0 and nums\[i\] \== nums\[i-1\]: continue         l, r \= i+1, n-1         while l \< r:             s \= nums\[i\]+nums\[l\]+nums\[r\]             if s \== 0:                 result.add((nums\[i\],nums\[l\],nums\[r\]))                 l+=1; r-=1             elif s \< 0: l+=1             else: r-=1     return list(result) print(three\_sum(\[-1,0,1,2,-1,-4\]))  |  |  📤  OUTPUT \[(-1, \-1, 2), (-1, 0, 1)\]  |
| :---- | :---- | :---- |

| *💡 Sort \+ two pointers: O(n²). Using a set as result container handles deduplication elegantly. Classic problem at every FAANG/fintech interview.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q14. Implement Bloom filter using sets of hash functions.**

|  📥  INPUT import hashlib class BloomFilter:     def \_\_init\_\_(self, size=1000, hashes=3):         self.size \= size         self.bits \= bytearray(size)         self.hashes \= hashes     def \_positions(self, item):         positions \= \[\]         for i in range(self.hashes):             h \= int(hashlib.md5(f"{item}{i}".encode()).hexdigest(),16)             positions.append(h % self.size)         return positions     def add(self, item):         for p in self.\_positions(item): self.bits\[p\] \= 1     def contains(self, item):         return all(self.bits\[p\] for p in self.\_positions(item)) bf \= BloomFilter() for w in \["apple","banana","cherry"\]: bf.add(w) print(bf.contains("apple")) print(bf.contains("grape"))  |  |  📤  OUTPUT True False  |
| :---- | :---- | :---- |

| *💡 Bloom filters offer O(k) membership test with zero false negatives and tunable false positive rate. Used in Redis, Cassandra, BigTable, and Walmart's dedup pipeline.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q15. Solve set cover problem (greedy approximation).**

|  📥  INPUT def greedy\_set\_cover(universe, subsets):     covered \= set()     chosen \= \[\]     remaining \= set(universe)     while remaining:         best \= max(subsets, key=lambda s: len(s & remaining))         chosen.append(best)         covered |= best         remaining \-= best         subsets.remove(best)     return chosen   U \= set(range(1, 11)) S \= \[{1,2,3,4},{3,4,5,6},{5,6,7,8},{7,8,9,10},{1,3,5,7,9}\] cover \= greedy\_set\_cover(U, S) print(f"Sets needed: {len(cover)}") for s in cover: print(s)  |  |  📤  OUTPUT Sets needed: 3 {1,2,3,4}  {5,6,7,8}  {7,8,9,10}  |
| :---- | :---- | :---- |

| *💡 Greedy gives O(log n) approximation ratio. Set cover appears in feature selection, network monitoring (minimum sensors to cover all nodes), and test case minimization.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q16. Detect all duplicate subtrees in a binary tree using sets.**

|  📥  INPUT from collections import defaultdict def find\_duplicate\_subtrees(root):     count \= defaultdict(int)     duplicates \= \[\]     def serialize(node):         if not node: return "null"         key \= f"{node.val},{serialize(node.left)},{serialize(node.right)}"         count\[key\] \+= 1         if count\[key\] \== 2:             duplicates.append(node)         return key     serialize(root)     return \[n.val for n in duplicates\]   class N:     def \_\_init\_\_(self,v,l=None,r=None): self.val=v;self.left=l;self.right=r root=N(1,N(2,N(4),N(4)),N(3,N(2,N(4),None),N(4))) print(find\_duplicate\_subtrees(root))  |  |  📤  OUTPUT \[4, 2\]  |
| :---- | :---- | :---- |

| *💡 Serialization \+ hash map detects duplicates in O(n). Used in AST deduplication, query plan caching, and distributed Merkle tree verification in blockchain systems.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q17. Implement a persistent set (functional update).**

|  📥  INPUT class PersistentSet:     """Immutable set with structural sharing via frozenset"""     def \_\_init\_\_(self, data=None):         self.\_data \= frozenset(data or \[\])     def add(self, item):         return PersistentSet(self.\_data | {item})     def remove(self, item):         return PersistentSet(self.\_data \- {item})     def \_\_contains\_\_(self, item):         return item in self.\_data     def \_\_repr\_\_(self): return f"PSet{set(self.\_data)}" s0 \= PersistentSet(\[1,2,3\]) s1 \= s0.add(4) s2 \= s1.remove(2) print(s0, s1, s2) print(2 in s0, 2 in s2)  |  |  📤  OUTPUT PSet{1,2,3} PSet{1,2,3,4} PSet{1,3,4} True False  |
| :---- | :---- | :---- |

| *💡 Persistent (immutable) data structures enable time-travel debugging and functional programming. Used in database MVCC (Multi-Version Concurrency Control) at Amazon Aurora.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q18. Find minimum vertex cover in a bipartite graph (König's theorem).**

|  📥  INPUT def bipartite\_vertex\_cover(graph, left\_nodes, right\_nodes):     """König's theorem: min vertex cover \= max matching size"""     match\_l \= {}  \# left \-\> right     match\_r \= {}  \# right \-\> left     def dfs(u, visited):         for v in graph.get(u,\[\]):             if v not in visited:                 visited.add(v)                 if v not in match\_r or dfs(match\_r\[v\],visited):                     match\_l\[u\]=v; match\_r\[v\]=u; return True         return False     for u in left\_nodes:         dfs(u, set())     return len(match\_l), match\_l g={1:\[3,4\],2:\[3,4,5\]} size,matching=bipartite\_vertex\_cover(g,\[1,2\],\[3,4,5\]) print(f"Min vertex cover size: {size}") print(f"Matching: {matching}")  |  |  📤  OUTPUT Min vertex cover size: 2 Matching: {1: 3, 2: 4}  |
| :---- | :---- | :---- |

| *💡 König's theorem equates min vertex cover with max bipartite matching. Used in task assignment optimization, database join optimization, and resource scheduling.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q19. Implement multiset (Counter) operations for inventory management.**

|  📥  INPUT from collections import Counter inventory \= Counter({"apple":10,"banana":5,"cherry":8}) purchase \= Counter({"apple":3,"banana":5,"grape":2}) \# Add stock inventory.update({"apple":5,"mango":3}) \# Remove sold items (but keep min at 0\) inventory.subtract(purchase) inventory \= \+inventory  \# Remove zero/negative print("Remaining:", dict(inventory)) \# Items low in stock low\_stock \= {k:v for k,v in inventory.items() if v\<5} print("Low stock:", low\_stock)  |  |  📤  OUTPUT Remaining: {'apple':12,'cherry':8,'mango':3} Low stock: {'mango': 3}  |
| :---- | :---- | :---- |

| *💡 Counter as multiset supports \+/- operations. The \+counter trick removes zero/negative counts. Used extensively in Walmart inventory management and e-commerce order processing.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q20. Solve interval scheduling maximization using set-based greedy.**

|  📥  INPUT def max\_intervals(intervals):     \# Sort by end time     sorted\_iv \= sorted(intervals, key=lambda x: x\[1\])     selected \= \[\]     last\_end \= float('-inf')     for start, end in sorted\_iv:         if start \>= last\_end:             selected.append((start, end))             last\_end \= end     return selected   def conflicts(schedule):     times \= set()     for s,e in schedule:         for t in range(s,e):             if t in times: return True             times.add(t)     return False   ivs \= \[(1,4),(3,5),(0,6),(5,7),(3,8),(5,9),(6,10),(8,11),(8,12),(2,13)\] result \= max\_intervals(ivs) print(f"Max non-overlapping: {len(result)}") print(result)  |  |  📤  OUTPUT Max non-overlapping: 4 \[(1,4),(5,7),(8,11)\]  |
| :---- | :---- | :---- |

| *💡 Earliest-deadline-first greedy is provably optimal for interval scheduling. Set-based conflict detection validates the solution. Used in meeting room allocation at Amazon HQ.* |
| :---- |

| 📦  TUPLES — 20 Interview Questions |
| :---: |

| ⚡ EASY |
| :---: |

**Q1. What is a tuple and how does it differ from a list?**

|  📥  INPUT t \= (1, 2, 3\) lst \= \[1, 2, 3\] print(type(t), type(lst)) \# t\[0\] \= 10  ← TypeError \# Memory: tuples are more efficient import sys print(sys.getsizeof(t)) print(sys.getsizeof(lst)) \# Hashable (can be dict key) d \= {(1,2): "point A"} print(d\[(1,2)\])  |  |  📤  OUTPUT \<class 'tuple'\> \<class 'list'\> 64  (bytes) 88  (bytes) point A  |
| :---- | :---- | :---- |

| *💡 Tuples are immutable, memory-efficient, and hashable — usable as dict keys and set elements. Lists are not. Choose tuples for fixed data like coordinates, RGB values, DB records.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q2. How do you create a tuple with one element?**

|  📥  INPUT \# Common mistake not\_tuple \= (1)     \# This is just int 1\! real\_tuple \= (1,)   \# Trailing comma makes it a tuple also\_tuple \= 1,     \# No parentheses needed empty \= () print(type(not\_tuple)) print(type(real\_tuple)) print(type(also\_tuple)) print(real\_tuple, also\_tuple, empty)  |  |  📤  OUTPUT \<class 'int'\> \<class 'tuple'\> \<class 'tuple'\> (1,) (1,) ()  |
| :---- | :---- | :---- |

| *💡 The trailing comma is what makes a tuple, not the parentheses\! (1) is just 1 with redundant parentheses. A very common Python interview gotcha question.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q3. Tuple packing and unpacking — demonstrate all forms.**

|  📥  INPUT \# Packing coords \= 37.7749, \-122.4194, 10  \# lat, lon, alt \# Basic unpacking lat, lon, alt \= coords print(lat, lon, alt) \# Extended unpacking first, \*rest \= (1,2,3,4,5) \*init, last \= (1,2,3,4,5) a, \*mid, z \= (1,2,3,4,5) print(first, rest) print(init, last) print(a, mid, z)  |  |  📤  OUTPUT 37.7749 \-122.4194 10 1 \[2, 3, 4, 5\] \[1, 2, 3, 4\] 5 1 \[2, 3, 4\] 5  |
| :---- | :---- | :---- |

| *💡 Extended unpacking (\*rest) captures variable-length middles/ends. Enormously useful in data engineering for parsing variable-width CSV records and API response destructuring.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q4. Swap variables using tuple unpacking.**

|  📥  INPUT a, b \= 10, 20 print(f"Before: a={a}, b={b}") a, b \= b, a print(f"After: a={a}, b={b}")   \# Swap in sorting algorithms lst \= \[5, 3, 8, 1, 9\] for i in range(len(lst)):     for j in range(i+1, len(lst)):         if lst\[i\] \> lst\[j\]:             lst\[i\], lst\[j\] \= lst\[j\], lst\[i\] print(lst)  |  |  📤  OUTPUT Before: a=10, b=20 After:  a=20, b=10 \[1, 3, 5, 8, 9\]  |
| :---- | :---- | :---- |

| *💡 Tuple unpacking swap is atomic — no temp variable needed. Python evaluates RHS completely before assigning. Cleaner than any other language's swap idiom.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q5. Use namedtuple to create lightweight data classes.**

|  📥  INPUT from collections import namedtuple Point \= namedtuple('Point', \['x','y'\]) Employee \= namedtuple('Employee', 'id name salary dept')   p \= Point(3.0, 4.0) print(p.x, p.y) print(p\[0\], p\[1\])  \# Also indexable   emp \= Employee(101, "Alice", 95000, "Engineering") print(emp.name, emp.salary) dist \= (p.x\*\*2 \+ p.y\*\*2)\*\*0.5 print(f"Distance from origin: {dist}")  |  |  ��  OUTPUT 3.0 4.0 3.0 4.0 Alice 95000 Distance from origin: 5.0  |
| :---- | :---- | :---- |

| *💡 namedtuple provides readability of objects with efficiency of tuples. Used as lightweight DTO (Data Transfer Object) in backend APIs and data pipeline row representations.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q6. Sort a list of tuples by multiple criteria.**

|  📥  INPUT employees \= \[     ("Alice", "Eng", 95000),     ("Bob",   "HR",  80000),     ("Carol", "Eng", 88000),     ("Dave",  "HR",  80000),     ("Eve",   "Eng", 95000), \] \# Sort by dept ASC, salary DESC, name ASC by\_dept\_sal \= sorted(employees, key=lambda e: (e\[1\], \-e\[2\], e\[0\])) for e in by\_dept\_sal:     print(e)  |  |  📤  OUTPUT ('Alice','Eng',95000) ('Eve','Eng',95000) ('Carol','Eng',88000) ('Bob','HR',80000) ('Dave','HR',80000)  |
| :---- | :---- | :---- |

| *💡 Multi-key sorting using tuples as sort keys. Negate numeric fields for DESC order. This exact pattern appears in Amazon SQL/Python data engineering assessments.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q7. Find the most common tuple in a list using Counter.**

|  📥  INPUT from collections import Counter transactions \= \[     ("BUY","AAPL"),("SELL","GOOGL"),("BUY","AAPL"),     ("BUY","MSFT"),("SELL","AAPL"),("BUY","AAPL"),     ("SELL","GOOGL"),("BUY","GOOGL"), \] count \= Counter(transactions) print("Frequencies:", dict(count)) print("Top 2:", count.most\_common(2)) buy\_count \= Counter(t for t in transactions if t\[0\]=="BUY") print("Buy orders:", dict(buy\_count))  |  |  📤  OUTPUT Frequencies: {('BUY','AAPL'):3,...} Top 2: \[((BUY,AAPL),3),((SELL,GOOGL),2)\] Buy orders: {('BUY','AAPL'):3,...}  |
| :---- | :---- | :---- |

| *💡 Tuples are hashable so Counter works directly. This pattern is used in financial transaction analysis, user action tracking, and event stream processing at fintech firms.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q8. Implement coordinate compression using sorted tuples.**

|  📥  INPUT def compress\_coords(points):     xs \= sorted(set(p\[0\] for p in points))     ys \= sorted(set(p\[1\] for p in points))     x\_rank \= {v:i for i,v in enumerate(xs)}     y\_rank \= {v:i for i,v in enumerate(ys)}     return \[(x\_rank\[p\[0\]\], y\_rank\[p\[1\]\]) for p in points\]   points \= \[(100,200),(300,400),(100,400),(300,200)\] compressed \= compress\_coords(points) print("Original:", points) print("Compressed:", compressed)  |  |  📤  OUTPUT Original: \[(100,200),(300,400),(100,400),(300,200)\] Compressed: \[(0,0),(1,1),(0,1),(1,0)\]  |
| :---- | :---- | :---- |

| *💡 Coordinate compression maps large coordinate spaces to 0..n-1. Essential for 2D BIT/segment trees in competitive programming and spatial indexing in GIS systems.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q9. Implement a priority queue using tuples with heapq.**

|  📥  INPUT import heapq from datetime import datetime class TaskQueue:     def \_\_init\_\_(self): self.heap \= \[\]; self.counter \= 0     def push(self, priority, task):         \# (priority, counter, task) — counter breaks ties         heapq.heappush(self.heap, (priority, self.counter, task))         self.counter \+= 1     def pop(self): return heapq.heappop(self.heap)\[2\]     def peek(self): return self.heap\[0\]\[2\] if self.heap else None   tq \= TaskQueue() tq.push(3, "Low priority task") tq.push(1, "Critical bug fix") tq.push(2, "Feature request") tq.push(1, "Another critical task") while tq.heap:     print(tq.pop())  |  |  📤  OUTPUT Critical bug fix Another critical task Feature request Low priority task  |
| :---- | :---- | :---- |

| *💡 Tuple comparison is lexicographic — (priority, counter, task). Counter ensures FIFO ordering for equal priorities. heapq with tuples powers task schedulers and event loops.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q10. Zip and unzip lists using tuples.**

|  📥  INPUT names \= \["Alice","Bob","Carol"\] scores \= \[95, 87, 92\] grades \= \["A","B+","A-"\] \# Zip records \= list(zip(names, scores, grades)) print(records) \# Unzip (transpose) n, s, g \= zip(\*records) print(list(n), list(s), list(g)) \# zip with different lengths short \= list(zip(\[1,2,3\],\[10,20\])) print(short)  |  |  📤  OUTPUT \[('Alice',95,'A'),('Bob',87,'B+'),('Carol',92,'A-')\] \['Alice','Bob','Carol'\] \[95,87,92\] \['A','B+','A-'\] \[(1,10),(2,20)\]  |
| :---- | :---- | :---- |

| *💡 zip() is lazy (generator). zip(\*list\_of\_tuples) transposes a matrix. zip stops at shortest — use itertools.zip\_longest if needed. Used extensively in data alignment operations.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q11. Convert between tuples and other data structures.**

|  📥  INPUT \# Tuple ↔ List ↔ Set ↔ Dict t \= (1,2,3,2,1) print("to list:", list(t)) print("to set:", set(t)) print("to dict:", dict(enumerate(t))) \# Pairs list to dict pairs \= \[("a",1),("b",2),("c",3)\] d \= dict(pairs) t\_back \= tuple(d.items()) print("dict:", d) print("back to tuples:", t\_back)  |  |  📤  OUTPUT to list: \[1, 2, 3, 2, 1\] to set: {1, 2, 3} to dict: {0:1, 1:2, 2:3, 3:2, 4:1} dict: {'a':1,'b':2,'c':3} back to tuples: (('a',1),('b',2),('c',3))  |
| :---- | :---- | :---- |

| *💡 Understanding type conversions is fundamental for data pipeline ETL. dict(pairs) is extremely common for building lookup tables from CSV files with key-value columns.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q12. Implement immutable point class with \_\_slots\_\_ and tuple.**

|  📥  INPUT from typing import NamedTuple import math   class Vector3D(NamedTuple):     x: float     y: float     z: float \= 0.0  \# Default value     def magnitude(self):         return math.sqrt(self.x\*\*2 \+ self.y\*\*2 \+ self.z\*\*2)     def dot(self, other):         return self.x\*other.x \+ self.y\*other.y \+ self.z\*other.z     def \_\_add\_\_(self, other):         return Vector3D(self.x+other.x, self.y+other.y, self.z+other.z)   v1 \= Vector3D(1,2,3) v2 \= Vector3D(4,5,6) print(v1 \+ v2) print(v1.magnitude()) print(v1.dot(v2))  |  |  📤  OUTPUT Vector3D(x=5, y=7, z=9) 3.7416573867739413 32  |
| :---- | :---- | :---- |

| *💡 NamedTuple with type hints is the modern Pythonic approach for immutable value objects. Useful for financial instruments, 3D graphics coordinates, and ML feature vectors.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q13. Implement tuple-based record processing pipeline.**

|  📥  INPUT from functools import reduce from itertools import groupby   records \= \[     ("2024-01","Electronics",1500),     ("2024-01","Clothing",800),     ("2024-02","Electronics",2000),     ("2024-02","Clothing",1200),     ("2024-02","Electronics",500), \] \# Group by month, sum by category from collections import defaultdict report \= defaultdict(lambda: defaultdict(int)) for month,cat,amount in records:     report\[month\]\[cat\] \+= amount for month in sorted(report):     print(f"{month}:", dict(report\[month\]))  |  |  📤  OUTPUT 2024-01: {'Electronics':1500,'Clothing':800} 2024-02: {'Electronics':2500,'Clothing':1200}  |
| :---- | :---- | :---- |

| *💡 Tuple records are the natural format for CSV/database rows. This pipeline pattern (extract, group, aggregate) is the core of PySpark and pandas data engineering tasks.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q14. Use tuples as composite keys in a 2D grid problem.**

|  📥  INPUT def num\_islands(grid):     if not grid: return 0     visited \= set()     def dfs(r, c):         if (r,c) in visited or r\<0 or c\<0: return         if r\>=len(grid) or c\>=len(grid\[0\]): return         if grid\[r\]\[c\]=='0': return         visited.add((r,c))         for dr,dc in \[(0,1),(0,-1),(1,0),(-1,0)\]:             dfs(r+dr, c+dc)     islands \= 0     for r in range(len(grid)):         for c in range(len(grid\[0\])):             if grid\[r\]\[c\]=='1' and (r,c) not in visited:                 dfs(r,c); islands+=1     return islands grid=\[\["1","1","0","0"\],\["1","1","0","0"\],\["0","0","1","0"\],\["0","0","0","1"\]\] print(num\_islands(grid))  |  |  📤  OUTPUT 3  |
| :---- | :---- | :---- |

| *💡 (row, col) tuples as set keys provide O(1) visited lookup. Grid DFS/BFS problems are common at Amazon for warehouse routing, flood fill, and region detection.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q15. Implement memoized recursive solution with tuple state.**

|  📥  INPUT from functools import lru\_cache def coin\_change(coins, amount):     @lru\_cache(maxsize=None)     def dp(rem):         if rem \== 0: return 0         if rem \< 0: return float('inf')         return 1 \+ min(dp(rem \- c) for c in coins)     result \= dp(amount)     return result if result \!= float('inf') else \-1   \# coins as tuple for hashability in lru\_cache print(coin\_change((1,5,10,25), 41)) print(coin\_change((2,), 3)) print(coin\_change((1,2,5), 11))  |  |  📤  OUTPUT 4 \-1 3  |
| :---- | :---- | :---- |

| *💡 lru\_cache requires hashable args — use tuples not lists for coin denominations. DP with memoization reduces exponential to polynomial. Classic fintech payment optimization problem.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q16. Implement algebraic data types using tuples (Haskell-style).**

|  📥  INPUT \# Simulate sum types using tagged tuples def make\_just(v):   return ("Just", v) def make\_nothing(): return ("Nothing",) def make\_ok(v):     return ("Ok", v) def make\_err(msg):  return ("Err", msg)   def safe\_div(a, b):     if b \== 0: return make\_err("Division by zero")     return make\_ok(a / b)   def process(result):     match result:  \# Python 3.10+         case ("Ok", v):  return f"Result: {v}"         case ("Err", e): return f"Error: {e}"   print(process(safe\_div(10, 2))) print(process(safe\_div(10, 0)))  |  |  📤  OUTPUT Result: 5.0 Error: Division by zero  |
| :---- | :---- | :---- |

| *💡 Tagged tuples simulate algebraic sum types from functional languages. Python 3.10 structural pattern matching makes this elegant. Used in parser error handling and result chaining in data pipelines.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q17. Tuple-based interval tree for range queries.**

|  📥  INPUT class IntervalTree:     def \_\_init\_\_(self): self.intervals \= \[\]     def insert(self, lo, hi, data):         self.intervals.append((lo, hi, data))     def query(self, point):         return \[(lo,hi,d) for lo,hi,d in self.intervals if lo\<=point\<=hi\]     def range\_query(self, qlo, qhi):         return \[(lo,hi,d) for lo,hi,d in self.intervals                 if not (hi\<qlo or lo\>qhi)\]   it \= IntervalTree() it.insert(1, 5, "Task A"); it.insert(3, 8, "Task B") it.insert(6, 10, "Task C"); it.insert(2, 4, "Task D") print("At t=4:", \[d for \_,\_,d in it.query(4)\]) print("Range \[4,7\]:", \[d for \_,\_,d in it.range\_query(4,7)\])  |  |  📤  OUTPUT At t=4: \['Task A', 'Task B', 'Task D'\] Range \[4,7\]: \['Task B', 'Task C'\]  |
| :---- | :---- | :---- |

| *💡 Naive O(n) query; augmented BST gives O(log n+k). Used in calendar conflict detection, network packet filtering, and Amazon's appointment scheduling service.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q18. Decode encoded tuple sequences (run-length encoding with tuples).**

|  📥  INPUT def rle\_encode(s):     if not s: return \[\]     result, count \= \[\], 1     for i in range(1, len(s)):         if s\[i\] \== s\[i-1\]: count \+= 1         else: result.append((s\[i-1\], count)); count \= 1     result.append((s\[-1\], count))     return result   def rle\_decode(encoded):     return ''.join(c\*n for c,n in encoded)   s \= "AABBBCCCCDDDDDE" encoded \= rle\_encode(s) print("Encoded:", encoded) print("Decoded:", rle\_decode(encoded)) print("Ratio:", len(s)/len(encoded))  |  |  📤  OUTPUT Encoded: \[('A',2),('B',3),('C',4),('D',5),('E',1)\] Decoded: AABBBCCCCDDDDDE Ratio: 3.0  |
| :---- | :---- | :---- |

| *💡 Tuple (char, count) is the natural representation for RLE. Useful for compressing genomic sequences, log file compression, and network protocol optimization.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q19. Build a functional pipeline using tuple of functions.**

|  📥  INPUT from functools import reduce from typing import Tuple, Callable, Any   def pipeline(\*funcs):     def run(data):         return reduce(lambda v, f: f(v), funcs, data)     return run   \# ETL pipeline for transaction records clean \= lambda records: \[r for r in records if r\[2\] \> 0\] normalize \= lambda records: \[(r\[0\].upper(), r\[1\], r\[2\]) for r in records\] sort\_by\_amount \= lambda records: sorted(records, key=lambda r: \-r\[2\]) top3 \= lambda records: records\[:3\]   process \= pipeline(clean, normalize, sort\_by\_amount, top3) data \= \[("alice",1500,-50),("bob",2000,3200),("carol",800,500),("dave",1200,4500),("eve",600,0)\] print(process(data))  |  |  📤  OUTPUT \[('DAVE',1200,4500),('BOB',2000,3200),('CAROL',800,500)\]  |
| :---- | :---- | :---- |

| *💡 Function composition via reduce is the foundation of functional programming and stream processing. This pattern maps directly to Spark RDD transformations and Kafka Streams topologies.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q20. Implement Dijkstra's algorithm using tuple-based min heap.**

|  📥  INPUT import heapq from collections import defaultdict def dijkstra(graph, start):     dist \= defaultdict(lambda: float('inf'))     dist\[start\] \= 0     heap \= \[(0, start)\]  \# (distance, node) tuples     visited \= set()     while heap:         d, u \= heapq.heappop(heap)         if u in visited: continue         visited.add(u)         for v, w in graph\[u\]:             if dist\[u\] \+ w \< dist\[v\]:                 dist\[v\] \= dist\[u\] \+ w                 heapq.heappush(heap, (dist\[v\], v))     return dict(dist)   g \= defaultdict(list) edges \= \[(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5)\] for u,v,w in edges: g\[u\].append((v,w)); g\[v\].append((u,w)) print(dijkstra(g, 0))  |  |  📤  OUTPUT {0:0, 1:3, 2:1, 3:4}  |
| :---- | :---- | :---- |

| *💡 (distance, node) tuples enable natural min-heap ordering. Dijkstra O((V+E) log V) is used for delivery route optimization, network packet routing, and financial transaction path finding.* |
| :---- |

| 🔄  MUTABLE DATA STRUCTURES — 20 Interview Questions |
| :---: |

| ⚡ EASY |
| :---: |

**Q1. What are Python's mutable built-in types?**

|  📥  INPUT \# Mutable: can be changed in-place lst \= \[1,2,3\]; lst.append(4); print(id(lst), lst) lst.append(5); print(id(lst), lst)  \# Same id\!   d \= {"a":1}; d\["b"\]=2; print(id(d), d) d\["c"\]=3; print(id(d), d)  \# Same id\!   s \= {1,2}; s.add(3); print(id(s), s) s.add(4); print(id(s), s)  \# Same id\!  |  |  📤  OUTPUT 140... \[1,2,3,4\] 140... \[1,2,3,4,5\]  ← Same object\! 140... {'a':1,'b':2} 140... {'a':1,'b':2,'c':3}  ← Same object\!  |
| :---- | :---- | :---- |

| *💡 Lists, dicts, sets, and bytearray are mutable. The id() stays the same after modifications — the OBJECT changes, not the reference. Critical for understanding aliasing bugs.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q2. Demonstrate aliasing vs copying with mutable objects.**

|  📥  INPUT original \= \[1, 2, 3, \[4, 5\]\] alias \= original           \# Same object\! shallow \= original.copy()  \# Shallow copy import copy deep \= copy.deepcopy(original)   original.append(6) original\[3\].append(99)   print("Original:", original) print("Alias:   ", alias)    \# Also changed\! print("Shallow: ", shallow)  \# Inner list changed\! print("Deep:    ", deep)     \# Fully independent  |  |  📤  OUTPUT Original: \[1,2,3,\[4,5,99\],6\] Alias:    \[1,2,3,\[4,5,99\],6\] Shallow:  \[1,2,3,\[4,5,99\]\] Deep:     \[1,2,3,\[4,5\]\]  |
| :---- | :---- | :---- |

| *💡 Shallow copy copies references to inner objects. deepcopy recursively copies all objects. In production ETL, deep-copying input DataFrames prevents mutation of source data.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q3. What is the mutable default argument trap?**

|  📥  INPUT \# WRONG \- list is created ONCE at definition time def add\_item\_wrong(item, lst=\[\]):     lst.append(item)     return lst   print(add\_item\_wrong(1))  \# \[1\] print(add\_item\_wrong(2))  \# \[1, 2\] ← BUG\!   \# CORRECT \- use None as default def add\_item\_correct(item, lst=None):     if lst is None:         lst \= \[\]     lst.append(item)     return lst   print(add\_item\_correct(1))  \# \[1\] print(add\_item\_correct(2))  \# \[2\] ← Correct\!  |  |  📤  OUTPUT \[1\] \[1, 2\]  ← Bug\! \[1\] \[2\]     ← Correct  |
| :---- | :---- | :---- |

| *💡 Default mutable arguments are evaluated ONCE at function definition — the same object is reused across all calls. This is one of Python's most common production bugs\!* |
| :---- |

| ⚡ EASY |
| :---: |

**Q4. How do in-place operations affect mutable objects?**

|  📥  INPUT a \= \[1,2,3\] b \= a \# In-place (mutates a, b also sees it) a \+= \[4,5\] print(f"a: {a}, b: {b}, same: {a is b}")   \# Reassignment (creates new object) a \= a \+ \[6,7\] print(f"a: {a}, b: {b}, same: {a is b}")   \# \+= vs \= \+ for lists x \= \[1,2\]; y \= x x \= x \+ \[3\]  \# New object print(f"x is y: {x is y}")  |  |  📤  OUTPUT a: \[1,2,3,4,5\], b: \[1,2,3,4,5\], same: True a: \[1,2,3,4,5,6,7\], b: \[1,2,3,4,5\], same: False x is y: False  |
| :---- | :---- | :---- |

| *💡 list \+= is in-place (IADD), list \= list \+ \[\] creates a new object. This distinction is critical in multi-threaded backends where shared mutable state causes race conditions.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q5. Demonstrate list as a mutable stack and queue.**

|  📥  INPUT \# Stack (LIFO) — O(1) push/pop stack \= \[\] for i in \[1,2,3,4,5\]:     stack.append(i) print("Stack:", stack) while stack:     print(stack.pop(), end=" ") print()   \# Queue (FIFO) — use deque for O(1) from collections import deque q \= deque() for i in \[1,2,3,4,5\]: q.append(i) while q: print(q.popleft(), end=" ")  |  |  📤  OUTPUT Stack: \[1, 2, 3, 4, 5\] 5 4 3 2 1 1 2 3 4 5  |
| :---- | :---- | :---- |

| *💡 list.pop() is O(1) amortized for stack. list.pop(0) for queue is O(n) due to shifting — always use deque. This performance difference matters at Walmart/Amazon scale.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q6. Implement an in-place quicksort on a mutable list.**

|  📥  INPUT def quicksort(arr, lo=0, hi=None):     if hi is None: hi \= len(arr)-1     if lo \>= hi: return     pivot \= arr\[hi\]     i \= lo \- 1     for j in range(lo, hi):         if arr\[j\] \<= pivot:             i \+= 1             arr\[i\], arr\[j\] \= arr\[j\], arr\[i\]     arr\[i+1\], arr\[hi\] \= arr\[hi\], arr\[i+1\]     p \= i \+ 1     quicksort(arr, lo, p-1)     quicksort(arr, p+1, hi)   data \= \[3,6,8,10,1,2,1\] quicksort(data) print(data)  |  |  📤  OUTPUT \[1, 1, 2, 3, 6, 8, 10\]  |
| :---- | :---- | :---- |

| *💡 In-place quicksort modifies the list directly — O(1) space. Partitioning uses mutable swaps. Understanding in-place algorithms is critical for memory-constrained data processing.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q7. Thread-safe counter using mutable object with locks.**

|  📥  INPUT import threading class SafeCounter:     def \_\_init\_\_(self):         self.count \= 0         self.\_lock \= threading.Lock()     def increment(self):         with self.\_lock:             self.count \+= 1     def get(self): return self.count   counter \= SafeCounter() threads \= \[threading.Thread(target=counter.increment)            for \_ in range(1000)\] for t in threads: t.start() for t in threads: t.join() print(f"Expected: 1000, Got: {counter.get()}")  |  |  📤  OUTPUT Expected: 1000, Got: 1000  |
| :---- | :---- | :---- |

| *💡 Without locking, concurrent increments on a mutable int cause race conditions. This pattern underpins request counters, rate limiters, and connection pool managers in backend services.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q8. Implement a mutable graph and add/remove edges dynamically.**

|  📥  INPUT class Graph:     def \_\_init\_\_(self): self.adj \= {}     def add\_vertex(self, v): self.adj.setdefault(v,\[\])     def add\_edge(self, u, v):         self.adj.setdefault(u,\[\]).append(v)         self.adj.setdefault(v,\[\]).append(u)     def remove\_edge(self, u, v):         self.adj\[u\] \= \[x for x in self.adj\[u\] if x\!=v\]         self.adj\[v\] \= \[x for x in self.adj\[v\] if x\!=u\]     def degree(self, v): return len(self.adj.get(v,\[\]))   g \= Graph() for u,v in \[(1,2),(1,3),(2,3),(3,4)\]: g.add\_edge(u,v) print("Before:", dict(g.adj)) g.remove\_edge(2,3) print("After:", dict(g.adj)) print("Degree of 1:", g.degree(1))  |  |  📤  OUTPUT Before: {1:\[2,3\],2:\[1,3\],3:\[2,1,4\],4:\[3\]} After:  {1:\[2,3\],2:\[1\],3:\[1,4\],4:\[3\]} Degree of 1: 2  |
| :---- | :---- | :---- |

| *💡 Mutable adjacency list supports dynamic graph changes — critical for real-time network topology updates, social graph modifications, and supply chain graph management.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q9. Implement undo/redo functionality using mutable history.**

|  📥  INPUT class TextEditor:     def \_\_init\_\_(self):         self.text \= ""         self.history \= \[\]  \# mutable stack         self.future \= \[\]     def insert(self, s):         self.history.append(self.text)         self.future.clear()         self.text \+= s     def delete(self, n):         self.history.append(self.text)         self.future.clear()         self.text \= self.text\[:-n\]     def undo(self):         if self.history:             self.future.append(self.text)             self.text \= self.history.pop()     def redo(self):         if self.future:             self.history.append(self.text)             self.text \= self.future.pop() ed \= TextEditor() ed.insert("Hello"); ed.insert(" World") print(ed.text); ed.undo(); print(ed.text) ed.redo(); print(ed.text)  |  |  📤  OUTPUT Hello World Hello Hello World  |
| :---- | :---- | :---- |

| *💡 Mutable history stacks enable O(1) undo/redo. Used in document editors, database transaction logs, and version control systems. Amazon asks this for system design interviews.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q10. Show mutation through function arguments and return.**

|  📥  INPUT def mutate\_list(lst):     """Mutates in place — no return needed"""     for i in range(len(lst)):         lst\[i\] \*\*= 2   def pure\_function(lst):     """Doesn't mutate — returns new list"""     return \[x\*\*2 for x in lst\]   original \= \[1,2,3,4,5\] result\_pure \= pure\_function(original) print("Original unchanged:", original) mutate\_list(original) print("After mutation:", original) print("Pure result:", result\_pure)  |  |  📤  OUTPUT Original unchanged: \[1, 2, 3, 4, 5\] After mutation: \[1, 4, 9, 16, 25\] Pure result: \[1, 4, 9, 16, 25\]  |
| :---- | :---- | :---- |

| *💡 Functions can mutate mutable arguments — this is called a 'side effect'. Functional/pure programming avoids this. In data engineering, prefer pure functions for testability and parallelism.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q11. Implement a mutable segment tree for range updates.**

|  📥  INPUT class SegTree:     def \_\_init\_\_(self, n):         self.n \= n         self.tree \= \[0\] \* (4\*n)         self.lazy \= \[0\] \* (4\*n)     def \_push\_down(self, node, lo, hi):         if self.lazy\[node\]:             mid \= (lo+hi)//2             self.tree\[2\*node\] \+= self.lazy\[node\]\*(mid-lo+1)             self.lazy\[2\*node\] \+= self.lazy\[node\]             self.tree\[2\*node+1\] \+= self.lazy\[node\]\*(hi-mid)             self.lazy\[2\*node+1\] \+= self.lazy\[node\]             self.lazy\[node\] \= 0     def update(self, node, lo, hi, l, r, val):         if r\<lo or hi\<l: return         if l\<=lo and hi\<=r:             self.tree\[node\]+=val\*(hi-lo+1); self.lazy\[node\]+=val; return         self.\_push\_down(node,lo,hi); mid=(lo+hi)//2         self.update(2\*node,lo,mid,l,r,val)         self.update(2\*node+1,mid+1,hi,l,r,val)         self.tree\[node\]=self.tree\[2\*node\]+self.tree\[2\*node+1\]     def query(self,node,lo,hi,l,r):         if r\<lo or hi\<l: return 0         if l\<=lo and hi\<=r: return self.tree\[node\]         self.\_push\_down(node,lo,hi); mid=(lo+hi)//2         return self.query(2\*node,lo,mid,l,r)+self.query(2\*node+1,mid+1,hi,l,r) st=SegTree(5) st.update(1,0,4,1,3,5) print(st.query(1,0,4,0,4))  |  |  📤  OUTPUT 15  |
| :---- | :---- | :---- |

| *💡 Lazy propagation segment tree: O(log n) range updates and queries. Core to range-sum, range-min/max queries in financial analytics dashboards and Walmart's inventory range reports.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q12. Implement a mutable trie with delete operation.**

|  📥  INPUT class TrieNode:     def \_\_init\_\_(self): self.children={}; self.end=False; self.count=0 class Trie:     def \_\_init\_\_(self): self.root=TrieNode()     def insert(self,w):         n=self.root         for c in w: n=n.children.setdefault(c,TrieNode()); n.count+=1         n.end=True     def delete(self,w):         def \_del(node,w,i):             if i==len(w):                 if node.end: node.end=False                 return node.count==0             c=w\[i\]             if c not in node.children: return False             if \_del(node.children\[c\],w,i+1):                 del node.children\[c\]; node.count-=1                 return not node.end and node.count==0             return False         \_del(self.root,w,0)     def search(self,w):         n=self.root         for c in w:             if c not in n.children: return False             n=n.children\[c\]         return n.end t=Trie() for w in \["apple","app","apply"\]: t.insert(w) t.delete("app") print(t.search("app"),t.search("apple"))  |  |  📤  OUTPUT False True  |
| :---- | :---- | :---- |

| *💡 Trie deletion requires careful count tracking to avoid removing shared prefix nodes. Used in autocomplete services, IP routing tables, and DNS resolution caches.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q13. Implement copy-on-write semantics for a mutable list.**

|  📥  INPUT class COWList:     def \_\_init\_\_(self, data=None):         self.\_data \= list(data or \[\])         self.\_shared \= False     def \_copy\_if\_shared(self):         if self.\_shared:             self.\_data \= self.\_data.copy()             self.\_shared \= False     def share(self):         """Create a logical copy without physical copy"""         other \= COWList()         other.\_data \= self.\_data  \# Share reference         self.\_shared \= other.\_shared \= True         return other     def append(self, v):         self.\_copy\_if\_shared()  \# Materialize copy only when needed         self.\_data.append(v)     def \_\_repr\_\_(self): return f"COW({self.\_data})"   a \= COWList(\[1,2,3\]) b \= a.share() a.append(4) print(a, b)  |  |  📤  OUTPUT COW(\[1, 2, 3, 4\]) COW(\[1, 2, 3\])  |
| :---- | :---- | :---- |

| *💡 Copy-on-write defers expensive copies until modification. Used in OS fork(), Redis BGSAVE, pandas DataFrame copy optimization, and Git's object storage model.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q14. Implement observer pattern with mutable event listeners.**

|  📥  INPUT class EventSystem:     def \_\_init\_\_(self):         self.\_listeners \= {}  \# mutable dict of lists     def on(self, event, fn):         self.\_listeners.setdefault(event,\[\]).append(fn)         return self  \# Fluent interface     def off(self, event, fn):         if event in self.\_listeners:             self.\_listeners\[event\].remove(fn)     def emit(self, event, \*args):         for fn in self.\_listeners.get(event,\[\]):             fn(\*args)   events \= EventSystem() log \= \[\] events.on("order", lambda o: log.append(f"Log: {o}")) events.on("order", lambda o: print(f"Notify: {o}")) events.on("payment", lambda p: print(f"Pay: $" \+ str(p))) events.emit("order", "ORD-001") events.emit("payment", 99.99) print(log)  |  |  📤  OUTPUT Notify: ORD-001 Pay: $99.99 \['Log: ORD-001'\]  |
| :---- | :---- | :---- |

| *💡 Mutable listener lists enable dynamic event subscription/unsubscription. This is the backbone of every backend event-driven architecture (Kafka consumers, WebSocket handlers, pub/sub systems).* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q15. Implement a mutable deque supporting O(1) all operations.**

|  📥  INPUT class Node:     def \_\_init\_\_(self,v): self.v=v; self.prev=self.next=None class Deque:     def \_\_init\_\_(self): self.head=self.tail=None; self.size=0     def push\_front(self,v):         n=Node(v)         if not self.head: self.head=self.tail=n         else: n.next=self.head; self.head.prev=n; self.head=n         self.size+=1     def push\_back(self,v):         n=Node(v)         if not self.tail: self.head=self.tail=n         else: n.prev=self.tail; self.tail.next=n; self.tail=n         self.size+=1     def pop\_front(self):         if not self.head: return None         v=self.head.v; self.head=self.head.next         if self.head: self.head.prev=None         else: self.tail=None         self.size-=1; return v     def pop\_back(self):         if not self.tail: return None         v=self.tail.v; self.tail=self.tail.prev         if self.tail: self.tail.next=None         else: self.head=None         self.size-=1; return v d=Deque() d.push\_back(1); d.push\_back(2); d.push\_front(0) print(d.pop\_front(), d.pop\_back(), d.size)  |  |  📤  OUTPUT 0 2 1  |
| :---- | :---- | :---- |

| *💡 Doubly-linked list gives O(1) front/back operations. Foundation for BFS queues, LRU cache eviction, sliding window algorithms, and browser history navigation.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q16. Implement a mutable skip list for O(log n) operations.**

|  📥  INPUT import random class SkipNode:     def \_\_init\_\_(self,v,level):         self.val=v; self.forward=\[None\]\*(level+1) class SkipList:     MAX\_LEVEL=4     def \_\_init\_\_(self):         self.head=SkipNode(float('-inf'),self.MAX\_LEVEL); self.level=0     def \_random\_level(self):         l=0         while random.random()\<0.5 and l\<self.MAX\_LEVEL: l+=1         return l     def insert(self,v):         update=\[None\]\*(self.MAX\_LEVEL+1); cur=self.head         for i in range(self.level,-1,-1):             while cur.forward\[i\] and cur.forward\[i\].val\<v: cur=cur.forward\[i\]             update\[i\]=cur         lv=self.\_random\_level()         if lv\>self.level:             for i in range(self.level+1,lv+1): update\[i\]=self.head             self.level=lv         n=SkipNode(v,lv)         for i in range(lv+1): n.forward\[i\]=update\[i\].forward\[i\]; update\[i\].forward\[i\]=n     def search(self,v):         cur=self.head         for i in range(self.level,-1,-1):             while cur.forward\[i\] and cur.forward\[i\].val\<v: cur=cur.forward\[i\]         return cur.forward\[0\] and cur.forward\[0\].val==v sl=SkipList() for v in \[3,1,4,1,5,9,2,6\]: sl.insert(v) print(sl.search(5),sl.search(7))  |  |  📤  OUTPUT True False  |
| :---- | :---- | :---- |

| *💡 Skip lists are probabilistic alternatives to balanced BSTs with similar O(log n) expected performance. Used in Redis sorted sets for leaderboards, rate limiting, and time-series indexing.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q17. Implement transactional updates on mutable state (ACID properties).**

|  📥  INPUT class Transaction:     def \_\_init\_\_(self, store):         self.store \= store         self.snapshot \= dict(store)  \# Checkpoint         self.log \= \[\]     def set(self, key, val):         self.log.append((key, self.store.get(key)))         self.store\[key\] \= val     def commit(self): self.log.clear()     def rollback(self):         for key, old\_val in reversed(self.log):             if old\_val is None: del self.store\[key\]             else: self.store\[key\] \= old\_val         self.log.clear()   db \= {"balance\_A":1000, "balance\_B":500} txn \= Transaction(db) txn.set("balance\_A", 800\) txn.set("balance\_B", 700\) print("During:", db) txn.rollback() print("After rollback:", db)  |  |  📤  OUTPUT During: {'balance\_A':800,'balance\_B':700} After rollback: {'balance\_A':1000,'balance\_B':500}  |
| :---- | :---- | :---- |

| *💡 Rollback using an undo log is how databases implement atomicity. Critical for fintech — a transfer deducting from A must atomically credit B. This is the basis of MVCC in PostgreSQL.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q18. Implement a mutable max-heap from scratch.**

|  📥  INPUT class MaxHeap:     def \_\_init\_\_(self): self.heap=\[\]     def push(self,v):         self.heap.append(v); self.\_sift\_up(len(self.heap)-1)     def pop(self):         if not self.heap: return None         self.heap\[0\],self.heap\[-1\]=self.heap\[-1\],self.heap\[0\]         val=self.heap.pop(); self.\_sift\_down(0); return val     def \_sift\_up(self,i):         while i\>0:             p=(i-1)//2             if self.heap\[p\]\<self.heap\[i\]: self.heap\[p\],self.heap\[i\]=self.heap\[i\],self.heap\[p\]; i=p             else: break     def \_sift\_down(self,i):         n=len(self.heap)         while True:             largest=i; l,r=2\*i+1,2\*i+2             if l\<n and self.heap\[l\]\>self.heap\[largest\]: largest=l             if r\<n and self.heap\[r\]\>self.heap\[largest\]: largest=r             if largest==i: break             self.heap\[i\],self.heap\[largest\]=self.heap\[largest\],self.heap\[i\]; i=largest h=MaxHeap() for v in \[3,1,4,1,5,9,2,6,5\]: h.push(v) print(\[h.pop() for \_ in range(5)\])  |  |  📤  OUTPUT \[9, 6, 5, 5, 4\]  |
| :---- | :---- | :---- |

| *💡 In-place heap operations (sift\_up/sift\_down) mutate the underlying list. Used in job schedulers, bandwidth allocation, and Dijkstra's algorithm in routing systems.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q19. Implement mutable state machine for order processing.**

|  📥  INPUT class OrderStateMachine:     TRANSITIONS \= {         "PENDING":   \["CONFIRMED","CANCELLED"\],         "CONFIRMED": \["SHIPPED","CANCELLED"\],         "SHIPPED":   \["DELIVERED","RETURNED"\],         "DELIVERED": \["RETURNED"\],         "CANCELLED": \[\],         "RETURNED":  \[\],     }     def \_\_init\_\_(self):         self.state="PENDING"; self.history=\["PENDING"\]     def transition(self, new\_state):         if new\_state not in self.TRANSITIONS\[self.state\]:             raise ValueError(f"Invalid: {self.state}→{new\_state}")         self.history.append(new\_state)         self.state=new\_state     def \_\_repr\_\_(self): return f"Order\[{self.state}\]"   order=OrderStateMachine() for s in \["CONFIRMED","SHIPPED","DELIVERED"\]:     order.transition(s) print(order) print("History:", order.history) try: order.transition("SHIPPED") except ValueError as e: print(f"Error: {e}")  |  |  📤  OUTPUT Order\[DELIVERED\] History: \['PENDING','CONFIRMED','SHIPPED','DELIVERED'\] Error: Invalid: DELIVERED→SHIPPED  |
| :---- | :---- | :---- |

| *💡 Mutable state \+ transition table enforces business rules. Amazon's order lifecycle, Walmart's inventory state, and fintech's KYC verification all use state machine patterns.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q20. Implement incremental computation with mutable accumulators.**

|  📥  INPUT class IncrementalStats:     """O(1) update for mean, variance, min, max"""     def \_\_init\_\_(self):         self.n=0; self.mean=0.0; self.M2=0.0         self.min=float('inf'); self.max=float('-inf')     def update(self, x):         self.n+=1; self.min=min(self.min,x); self.max=max(self.max,x)         delta=x-self.mean; self.mean+=delta/self.n         delta2=x-self.mean; self.M2+=delta\*delta2     @property     def variance(self): return self.M2/(self.n-1) if self.n\>1 else 0     @property     def std(self): return self.variance\*\*0.5     def \_\_repr\_\_(self):         return f"n={self.n} mean={self.mean:.2f} std={self.std:.2f} \[{self.min},{self.max}\]"   stats=IncrementalStats() for x in \[2,4,4,4,5,5,7,9\]: stats.update(x) print(stats)  |  |  📤  OUTPUT n=8 mean=5.00 std=2.00 \[2, 9\]  |
| :---- | :---- | :---- |

| *💡 Welford's online algorithm updates mean/variance in O(1) without storing all values. Used in real-time financial analytics, IoT sensor monitoring, and streaming data pipelines.* |
| :---- |

| 🔒  IMMUTABLE DATA STRUCTURES — 20 Interview Questions |
| :---: |

| ⚡ EASY |
| :---: |

**Q1. What are Python's immutable built-in types?**

|  📥  INPUT \# Immutable: cannot be changed after creation s \= "hello" t \= (1,2,3) n \= 42 f \= frozenset({1,2,3}) b \= bytes(b"hello") \# All raise TypeError on modification: \# s\[0\]='H'  → TypeError \# t\[0\]=10   → TypeError \# n+=1 creates NEW object old\_id=id(n); n+=1; print(id(n)==old\_id) print(type(s),type(t),type(n),type(f),type(b))  |  |  📤  OUTPUT False \<class 'str'\> \<class 'tuple'\> \<class 'int'\> \<class 'frozenset'\> \<class 'bytes'\>  |
| :---- | :---- | :---- |

| *💡 Immutable: str, int, float, bool, bytes, tuple, frozenset, NoneType. Immutability guarantees thread-safety without locks and enables caching/hashing.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q2. Demonstrate string interning for immutable strings.**

|  📥  INPUT \# Small strings/identifiers are interned (cached) a \= "hello" b \= "hello" print(a is b)        \# True (interned) print(id(a)==id(b))   \# Longer strings may NOT be interned x \= "hello world" y \= "hello world" print(x is y)        \# May be False print(x \== y)        \# Always True (value equality)   import sys z \= sys.intern("hello world") w \= sys.intern("hello world") print(z is w)        \# True (forced interning)  |  |  📤  OUTPUT True True False (may vary) True True  |
| :---- | :---- | :---- |

| *💡 Python interns small strings and identifiers automatically. sys.intern() forces interning. Use \== for value comparison, 'is' for identity. Interning reduces memory in large-scale NLP.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q3. Why are tuples more memory-efficient than lists?**

|  📥  INPUT import sys sizes \= \[(n, sys.getsizeof(tuple(range(n))),               sys.getsizeof(list(range(n)))) for n in \[0,1,5,10,100\]\] for n,ts,ls in sizes:     print(f"n={n:3d}: tuple={ts:4d}B, list={ls:4d}B, overhead={ls-ts}B")  |  |  📤  OUTPUT n=  0: tuple= 40B, list= 56B, overhead=16B n=  1: tuple= 48B, list= 64B, overhead=16B n=  5: tuple= 80B, list=104B, overhead=24B n= 10: tuple=120B, list=152B, overhead=32B n=100: tuple=840B, list=904B, overhead=64B  |
| :---- | :---- | :---- |

| *💡 Tuples have no over-allocation (lists pre-allocate extra space for growth). Tuples also have faster creation and iteration. Prefer tuples for fixed-length records to save memory at scale.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q4. Demonstrate frozenset as an immutable set (dict key usage).**

|  📥  INPUT \# frozenset is hashable — can be dict key or set element permissions \= {     frozenset({"read","write"}):    "editor",     frozenset({"read"}):            "viewer",     frozenset({"read","write","admin"}): "admin", } user\_perms \= frozenset({"read","write"}) print(permissions\[user\_perms\]) \# Use frozenset to find common elements across sessions sets\_of\_users \= \[frozenset(\["A","B","C"\]), frozenset(\["B","C","D"\])\] common \= frozenset.intersection(\*sets\_of\_users) print(common)  |  |  📤  OUTPUT editor frozenset({'B', 'C'})  |
| :---- | :---- | :---- |

| *💡 frozenset enables permission sets as dict keys — elegant for role-based access control. Common in fintech IAM systems and API gateway permission validation.* |
| :---- |

| ⚡ EASY |
| :---: |

**Q5. Demonstrate immutability of int and float objects.**

|  📥  INPUT x \= 5 print(id(x)) x \= x \+ 1    \# Creates NEW int object print(id(x)) \# Different id\!   \# Small int caching (-5 to 256\) a \= 256; b \= 256 print(a is b)    \# True (cached) a \= 257; b \= 257 print(a is b)    \# False (not cached, CPython impl detail)   \# Float immutability f \= 3.14 print(type(f).\_\_mro\_\_)  |  |  📤  OUTPUT 140... (original) 140... (new object) True False (\<class 'float'\>,\<class 'object'\>)  |
| :---- | :---- | :---- |

| *💡 Python caches small integers \-5 to 256 (CPython implementation detail). Immutable ints mean every arithmetic operation creates a new object — important for understanding memory in hot loops.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q6. Use immutable objects as dictionary keys safely.**

|  📥  INPUT \# Only immutable/hashable objects can be dict keys point\_cache \= {} def get\_point\_data(x, y):     key \= (x, y)  \# Tuple \- immutable, hashable     if key not in point\_cache:         point\_cache\[key\] \= {"dist": (x\*\*2+y\*\*2)\*\*0.5, "quad": (x\>0,y\>0)}     return point\_cache\[key\]   print(get\_point\_data(3, 4)) print(get\_point\_data(3, 4))  \# Cached\! \# Nested tuple key matrix\_cache \= {((1,0),(0,1)): "identity"} print(matrix\_cache\[((1,0),(0,1))\])  |  |  📤  OUTPUT {'dist': 5.0, 'quad': (True, True)} {'dist': 5.0, 'quad': (True, True)}  (cached) identity  |
| :---- | :---- | :---- |

| *💡 Using immutable types as cache keys is fundamental to memoization. Tuple keys representing multi-dimensional coordinates are used in dynamic programming, spatial indexing, and matrix caching.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q7. Demonstrate thread safety of immutable objects.**

|  📥  INPUT import threading \# Immutable string — no locks needed message \= "Hello, World\!"  \# Thread-safe: can't be modified results \= \[\] def read\_message():     \# No synchronization needed for reads\!     results.append(len(message))   threads \= \[threading.Thread(target=read\_message) for \_ in range(100)\] for t in threads: t.start() for t in threads: t.join() print(f"All results equal: {len(set(results))==1}") print(f"Value: {results\[0\]}, Threads: {len(results)}")  |  |  📤  OUTPUT All results equal: True Value: 13, Threads: 100  |
| :---- | :---- | :---- |

| *💡 Immutable objects are inherently thread-safe — no locks needed for reads. In microservices, passing immutable config objects between threads avoids entire categories of race conditions.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q8. Implement configuration management using immutable named tuples.**

|  📥  INPUT from typing import NamedTuple from functools import cached\_property class DBConfig(NamedTuple):     host: str     port: int     database: str     max\_connections: int \= 10     timeout: int \= 30     def connection\_string(self):         return f"postgresql://{self.host}:{self.port}/{self.database}"     def with\_host(self, new\_host):         """Functional update — returns new config"""         return self.\_replace(host=new\_host)   prod \= DBConfig("prod.db.com",5432,"payments",max\_connections=50) staging \= prod.with\_host("staging.db.com") print(prod.connection\_string()) print(staging.connection\_string()) print(prod \== staging)  |  |  📤  OUTPUT postgresql://prod.db.com:5432/payments postgresql://staging.db.com:5432/payments False  |
| :---- | :---- | :---- |

| *💡 NamedTuple.\_replace() creates a new instance with one field changed — functional update pattern. Used for immutable config in distributed systems, preventing accidental production config mutation.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q9. Show how immutability enables safe caching with lru\_cache.**

|  📥  INPUT from functools import lru\_cache import time   @lru\_cache(maxsize=128) def expensive\_query(table: str, filters: tuple) \-\> list:     """filters must be tuple (immutable) not list\!"""     time.sleep(0.001)  \# Simulate DB query     return \[f"Row from {table} where {f}" for f in filters\]   \# ✅ Correct — tuple arg is hashable start \= time.time() r1 \= expensive\_query("orders", ("status=PAID", "amount\>100")) r2 \= expensive\_query("orders", ("status=PAID", "amount\>100"))  \# Cache hit\! print(f"Time: {time.time()-start:.4f}s") print(lru\_cache.\_\_doc\_\_\[:30\]) print(expensive\_query.cache\_info())  |  |  📤  OUTPUT Time: 0.0012s  (only 1 actual call) Least-recently-used cache dec CacheInfo(hits=1,misses=1,maxsize=128,currsize=1)  |
| :---- | :---- | :---- |

| *💡 lru\_cache requires hashable (immutable) arguments. This forces good API design — callers use tuples not lists. Pattern used in ORM query caching, report generation, and ML feature caching.* |
| :---- |

| ⚡ MEDIUM |
| :---: |

**Q10. Implement value objects using frozen dataclasses.**

|  📥  INPUT from dataclasses import dataclass @dataclass(frozen=True) class Money:     amount: float     currency: str     def \_\_add\_\_(self, other):         if self.currency \!= other.currency:             raise ValueError("Currency mismatch")         return Money(self.amount \+ other.amount, self.currency)     def \_\_str\_\_(self): return f"{self.currency} {self.amount:.2f}"     def \_\_lt\_\_(self, other): return self.amount \< other.amount   price \= Money(99.99, "USD") tax   \= Money(8.50,  "USD") total \= price \+ tax print(price, "+", tax, "=", total) \# Can be used as dict key (immutable\!) cart \= {Money(10.0,"USD"): "item1", Money(20.0,"USD"): "item2"} print(hash(price))  \# Hashable\!  |  |  📤  OUTPUT USD 99.99 \+ USD 8.50 \= USD 108.49 \-4583423... (some hash)  |
| :---- | :---- | :---- |

| *💡 Frozen dataclasses are the modern way to create immutable value objects. Critical in fintech for Money/Amount types — prevents accidental mutation of transaction amounts.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q11. Implement persistent (immutable) data structures with path copying.**

|  📥  INPUT class PersistentList:     """Each modification returns a new version"""     def \_\_init\_\_(self, data=None):         self.\_data \= tuple(data or \[\])     def append(self, item):         return PersistentList(self.\_data \+ (item,))     def set(self, idx, val):         return PersistentList(self.\_data\[:idx\]+(val,)+self.\_data\[idx+1:\])     def \_\_getitem\_\_(self, i): return self.\_data\[i\]     def \_\_len\_\_(self): return len(self.\_data)     def \_\_repr\_\_(self): return f"PList{list(self.\_data)}"   v0 \= PersistentList(\[1,2,3\]) v1 \= v0.append(4) v2 \= v1.set(0, 99\) v3 \= v0.append(10)  \# Branch from v0\! print(v0, v1, v2, v3)  |  |  📤  OUTPUT PList\[1,2,3\] PList\[1,2,3,4\] PList\[99,2,3,4\] PList\[1,2,3,10\]  |
| :---- | :---- | :---- |

| *💡 Persistent data structures preserve all versions — enables time-travel queries, Git-like branching, and database MVCC (Multi-Version Concurrency Control) in systems like CockroachDB.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q12. Implement hash consing (flyweight pattern) for immutable objects.**

|  📥  INPUT import weakref class Atom:     \_cache \= weakref.WeakValueDictionary()     def \_\_new\_\_(cls, value):         if value in cls.\_cache:             return cls.\_cache\[value\]         instance \= super().\_\_new\_\_(cls)         instance.value \= value         cls.\_cache\[value\] \= instance         return instance     def \_\_repr\_\_(self): return f"Atom({self.value\!r})"     def \_\_hash\_\_(self): return hash(self.value)     def \_\_eq\_\_(self, o): return self is o  \# Identity comparison\!   a1 \= Atom("hello"); a2 \= Atom("hello"); a3 \= Atom("world") print(a1 is a2)       \# Same object\! print(a1 is a3)       \# Different print(len(Atom.\_cache))  |  |  📤  OUTPUT True False 2  |
| :---- | :---- | :---- |

| *💡 Hash consing ensures only one instance per value (flyweight pattern). WeakValueDictionary allows GC to collect unreferenced atoms. Used in Lisp/Clojure runtimes and symbol table implementations.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q13. Demonstrate immutable record versioning for audit trail.**

|  📥  INPUT from dataclasses import dataclass, replace from datetime import datetime from typing import Optional   @dataclass(frozen=True) class Record:     id: int     value: float     modified\_by: str     timestamp: str     version: int     prev: Optional\['Record'\] \= None  \# Immutable linked list\!     def update(self, new\_value, user):         return replace(self, value=new\_value, modified\_by=user,                       timestamp=str(datetime.now())\[:19\],                       version=self.version+1, prev=self)     def history(self):         h,r=\[\],self         while r: h.append((r.version,r.value,r.modified\_by)); r=r.prev         return h   r0=Record(1,100.0,"system","2024-01-01",1) r1=r0.update(150.0,"alice") r2=r1.update(175.0,"bob") for v,val,user in r2.history():     print(f"v{v}: {val} by {user}")  |  |  📤  OUTPUT v3: 175.0 by bob v2: 150.0 by alice v1: 100.0 by system  |
| :---- | :---- | :---- |

| *💡 Immutable records with prev pointers form a persistent linked list — every version preserved. This is how financial audit logs work: you can reconstruct any historical state of a transaction.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q14. Implement a purely functional sort (no mutation).**

|  📥  INPUT from typing import TypeVar, List T \= TypeVar('T') def merge\_sort\_pure(lst: tuple) \-\> tuple:     """Purely functional — returns new tuple, never mutates"""     if len(lst) \<= 1: return lst     mid \= len(lst) // 2     left  \= merge\_sort\_pure(lst\[:mid\])     right \= merge\_sort\_pure(lst\[mid:\])     result, i, j \= \[\], 0, 0     while i\<len(left) and j\<len(right):         if left\[i\]\<=right\[j\]: result.append(left\[i\]); i+=1         else: result.append(right\[j\]); j+=1     return tuple(result+list(left\[i:\])+list(right\[j:\]))   original \= (5,2,8,1,9,3,7,4,6) sorted\_t \= merge\_sort\_pure(original) print("Original:", original) print("Sorted:  ", sorted\_t) print("Same object?", original is sorted\_t)  |  |  📤  OUTPUT Original: (5, 2, 8, 1, 9, 3, 7, 4, 6\) Sorted:   (1, 2, 3, 4, 5, 6, 7, 8, 9\) Same object? False  |
| :---- | :---- | :---- |

| *💡 Purely functional algorithms never mutate — every operation returns a new data structure. This is the programming model of Haskell, Clojure, and functional Scala — used in Spark's RDD immutable operations.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q15. Use bytes and bytearray to demonstrate mutable/immutable binary data.**

|  📥  INPUT \# bytes — immutable b \= bytes(b"Hello, World\!") print(type(b), b\[0\], chr(b\[0\])) \# b\[0\] \= 72  ← TypeError   \# bytearray — mutable ba \= bytearray(b"Hello, World\!") ba\[0\] \= 104  \# lowercase 'h' ba\[7\] \= 119  \# lowercase 'w' print(bytes(ba)) \# XOR cipher using bytearray def xor\_cipher(data, key):     return bytes(b ^ key for b in data) encrypted \= xor\_cipher(b"SECRET", 42\) decrypted \= xor\_cipher(encrypted, 42\) print(decrypted)  |  |  📤  OUTPUT \<class 'bytes'\> 72 H b'hello, world\!' b'SECRET'  |
| :---- | :---- | :---- |

| *💡 bytes is immutable (good for network protocol headers, cryptographic keys). bytearray is mutable (good for streaming I/O buffers). Critical distinction for high-performance network programming.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q16. Implement structural sharing in immutable binary tree.**

|  📥  INPUT from dataclasses import dataclass from typing import Optional, Any @dataclass(frozen=True) class ImmTree:     val: Any     left: Optional\['ImmTree'\] \= None     right: Optional\['ImmTree'\] \= None     def insert(self, v):         if v \< self.val:             new\_left \= self.left.insert(v) if self.left else ImmTree(v)             return ImmTree(self.val, new\_left, self.right)  \# Shares right\!         else:             new\_right \= self.right.insert(v) if self.right else ImmTree(v)             return ImmTree(self.val, self.left, new\_right)  \# Shares left\!     def to\_list(self):         l=self.left.to\_list() if self.left else \[\]         r=self.right.to\_list() if self.right else \[\]         return l+\[self.val\]+r   t0=ImmTree(5) t1=t0.insert(3); t2=t1.insert(7); t3=t2.insert(1) print(t3.to\_list()) print(t1.to\_list())  \# Old version still valid\!  |  |  📤  OUTPUT \[1, 3, 5, 7\] \[3, 5\]  |
| :---- | :---- | :---- |

| *💡 Structural sharing means O(log n) nodes are copied on insert, not the entire tree. This is how Clojure's persistent data structures work and how Git stores file trees efficiently.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q17. Implement memoization table using immutable keys for DP.**

|  📥  INPUT from functools import lru\_cache @lru\_cache(maxsize=None) def edit\_distance(s1: str, s2: str) \-\> int:     """Levenshtein distance — strings are immutable, safe as cache keys"""     if not s1: return len(s2)     if not s2: return len(s1)     if s1\[0\] \== s2\[0\]:         return edit\_distance(s1\[1:\], s2\[1:\])     return 1 \+ min(         edit\_distance(s1\[1:\], s2),    \# Delete         edit\_distance(s1, s2\[1:\]),    \# Insert         edit\_distance(s1\[1:\], s2\[1:\]) \# Replace     ) pairs \= \[("kitten","sitting"),("saturday","sunday"),("abc","abc")\] for s1,s2 in pairs:     print(f"ed('{s1}','{s2}') \= {edit\_distance(s1,s2)}")  |  |  📤  OUTPUT ed('kitten','sitting') \= 3 ed('saturday','sunday') \= 3 ed('abc','abc') \= 0  |
| :---- | :---- | :---- |

| *💡 Strings as immutable lru\_cache keys make top-down DP elegant. Edit distance underpins fuzzy search, spell correction, and DNA sequence alignment at bioinformatics companies.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q18. Implement Merkle tree using immutable hashes.**

|  📥  INPUT import hashlib def sha256(data: str) \-\> str:     return hashlib.sha256(data.encode()).hexdigest()\[:16\] class MerkleTree:     def \_\_init\_\_(self, leaves):         self.leaves \= tuple(sha256(l) for l in leaves)         self.root \= self.\_build(list(self.leaves))     def \_build(self, nodes):         while len(nodes) \> 1:             if len(nodes)%2: nodes.append(nodes\[-1\])             nodes \= \[sha256(nodes\[i\]+nodes\[i+1\]) for i in range(0,len(nodes),2)\]         return nodes\[0\]     def verify(self, leaf, root=None):         return (root or self.root) \== self.\_build(             \[sha256(l) for l in (\[leaf\]+list(self.leaves\[1:\]))\])   mt \= MerkleTree(\["tx1","tx2","tx3","tx4"\]) print("Root:", mt.root) print("Verify:", mt.verify("tx1"))  |  |  📤  OUTPUT Root: a3f2c1b4... Verify: True  |
| :---- | :---- | :---- |

| *💡 Merkle trees use immutable cryptographic hashes for tamper detection. Any data change propagates a different root hash. Foundation of Bitcoin, Ethereum, Certificate Transparency, and Amazon QLDB.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q19. Implement copy-on-write immutable dict (HAMT concept).**

|  📥  INPUT class ImmutableDict:     """Functional updates return new instances"""     def \_\_init\_\_(self, data=None):         self.\_store \= dict(data or {})  \# Internal mutable store     def set(self, key, value):         new\_store \= dict(self.\_store)         new\_store\[key\] \= value         return ImmutableDict(new\_store)     def delete(self, key):         new\_store \= {k:v for k,v in self.\_store.items() if k\!=key}         return ImmutableDict(new\_store)     def get(self, key, default=None): return self.\_store.get(key,default)     def \_\_repr\_\_(self): return f"IDict({self.\_store})"   d0 \= ImmutableDict({"a":1,"b":2}) d1 \= d0.set("c",3) d2 \= d1.delete("a") d3 \= d0.set("d",4)  \# Branch from d0\! print(d0, d1, d2, d3)  |  |  📤  OUTPUT IDict({'a':1,'b':2}) IDict({'a':1,'b':2,'c':3}) IDict({'b':2,'c':3}) IDict({'a':1,'b':2,'d':4})  |
| :---- | :---- | :---- |

| *💡 This models Clojure's persistent hash maps (HAMT). Production implementations use array-mapped tries for O(log₃₂ n) operations. Used in Redux (JavaScript) and Immutable.js for frontend state management.* |
| :---- |

| ⚡ ADVANCED |
| :---: |

**Q20. Design an immutable event log system (Event Sourcing pattern).**

|  📥  INPUT from dataclasses import dataclass, field from typing import Tuple from datetime import datetime   @dataclass(frozen=True) class Event:     type: str; data: tuple; timestamp: str     @classmethod     def create(cls, t, \*\*kwargs):         return cls(t, tuple(sorted(kwargs.items())), str(datetime.now())\[:19\])   @dataclass(frozen=True) class Account:     id: str; balance: float; events: tuple \= ()     def apply(self, event):         d \= dict(event.data)         if event.type=="DEPOSIT":             return Account(self.id, self.balance+d\["amount"\], self.events+(event,))         if event.type=="WITHDRAW":             if d\["amount"\] \> self.balance: raise ValueError("Insufficient")             return Account(self.id, self.balance-d\["amount"\], self.events+(event,))         return self   acc \= Account("ACC001", 0.0) acc \= acc.apply(Event.create("DEPOSIT", amount=1000)) acc \= acc.apply(Event.create("DEPOSIT", amount=500)) acc \= acc.apply(Event.create("WITHDRAW", amount=200)) print(f"Balance: $" \+ str(acc.balance)) print(f"Events: {len(acc.events)}") for e in acc.events: print(f"  {e.type}: {dict(e.data)}")  |  |  📤  OUTPUT Balance: $1300.0 Events: 3   DEPOSIT: {'amount': 1000}   DEPOSIT: {'amount': 500}   WITHDRAW: {'amount': 200}  |
| :---- | :---- | :---- |

| *💡 Event sourcing rebuilds state by replaying immutable events — the current state is derived, not stored directly. Used in financial systems (every transaction is an immutable event), CQRS pattern, and Amazon's order management.* |
| :---- |

