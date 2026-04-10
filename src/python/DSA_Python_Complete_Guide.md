  
**DATA STRUCTURES &**

**ALGORITHMS**

*A Complete Python Guide*

| Covers: Arrays • Linked Lists • Stacks • Queues • Trees • Graphs • Hash Tables Sorting • Searching • Dynamic Programming • Greedy • Backtracking |
| :---: |

**With Time & Space Complexity Analysis**

# **Table of Contents**

1\. Big-O Notation & Complexity 3

2\. Arrays 4

3\. Linked Lists 5

4\. Stacks 7

5\. Queues 8

6\. Hash Tables (Dictionaries) 9

7\. Trees 10

8\. Heaps & Priority Queues13

9\. Graphs14

10\. Sorting Algorithms16

11\. Searching Algorithms20

12\. Dynamic Programming22

13\. Greedy Algorithms24

14\. Backtracking25

15\. Trie (Prefix Tree)26

16\. Complexity Cheat Sheet27

# **1\. Big-O Notation & Complexity Analysis**

Big-O notation describes the upper bound of an algorithm's time or space usage as the input size grows. It helps us compare algorithms independently of hardware.

**Common Complexity Classes (Best to Worst)**

| Notation | Name | Example Use Case |
| :---: | :---: | :---: |
| O(1) | **Constant** | **Best — independent of input size** |
| O(log n) | **Logarithmic** | **Excellent — binary search, balanced trees** |
| O(n) | **Linear** | **Good — single loop through input** |
| O(n log n) | **Linearithmic** | **Fair — efficient sorts (merge, heap)** |
| O(n²) | **Quadratic** | **Poor — nested loops** |
| O(2ⁿ) | **Exponential** | **Bad — recursive without memoization** |
| O(n\!) | **Factorial** | **Worst — brute-force permutations** |

**How to Analyze Code**

Step 1: Identify the dominant term (drop constants and lower-order terms).

Step 2: Focus on the worst case unless stated otherwise.

Step 3: Space complexity includes call stack for recursion.

| \# O(1) \- Constant def get\_first(arr):     return arr\[0\]           \# single operation regardless of size   \# O(n) \- Linear def find\_max(arr):     max\_val \= arr\[0\]     for x in arr:           \# loop runs n times         if x \> max\_val:             max\_val \= x     return max\_val   \# O(n²) \- Quadratic def bubble\_sort\_pass(arr):     for i in range(len(arr)):         for j in range(len(arr) \- 1):  \# nested loop → n \* n             if arr\[j\] \> arr\[j+1\]:                 arr\[j\], arr\[j+1\] \= arr\[j+1\], arr\[j\]   \# O(log n) \- Logarithmic def binary\_search(arr, target):     lo, hi \= 0, len(arr) \- 1     while lo \<= hi:          \# halves search space each iteration         mid \= (lo \+ hi) // 2         if arr\[mid\] \== target: return mid         elif arr\[mid\] \< target: lo \= mid \+ 1         else: hi \= mid \- 1     return \-1 |
| :---- |

# **2\. Arrays (Lists in Python)**

| What is an Array? A contiguous block of memory storing elements of the same type. Python's list is a dynamic array that auto-resizes. Supports random access via index in O(1). |
| :---- |

**Complexity Overview**

| Operation | Time Complexity | Space Complexity |
| :---: | :---: | :---: |
| Access by index | **O(1)** | **O(1)** |
| Search (unsorted) | **O(n)** | **O(1)** |
| Search (sorted) | **O(log n)** | **O(1)** |
| Insert at end | **O(1) amortized** | **O(1)** |
| Insert at index | **O(n)** | **O(1)** |
| Delete at end | **O(1)** | **O(1)** |
| Delete at index | **O(n)** | **O(1)** |

**Python Implementation & Core Operations**

| \# \--- Array Creation \--- arr \= \[1, 2, 3, 4, 5\] matrix \= \[\[1,2,3\],\[4,5,6\],\[7,8,9\]\]   \# 2D array   \# \--- Access & Update \--- print(arr\[0\])          \# O(1) — first element: 1 print(arr\[-1\])         \# O(1) — last element:  5 arr\[2\] \= 99            \# O(1) — update index 2   \# \--- Insert \--- arr.append(6)          \# O(1) amortized — add to end arr.insert(1, 10\)      \# O(n) — insert at position 1 (shifts elements)   \# \--- Delete \--- arr.pop()              \# O(1) — remove last arr.pop(0)             \# O(n) — remove first (shifts all right elements) arr.remove(99)         \# O(n) — search \+ remove first occurrence   \# \--- Slicing \--- sub \= arr\[1:4\]         \# O(k) — returns new list of slice length k   \# \--- Common Patterns \--- \# Two Pointer def two\_sum\_sorted(arr, target):     l, r \= 0, len(arr) \- 1     while l \< r:         s \= arr\[l\] \+ arr\[r\]         if s \== target:   return \[l, r\]         elif s \< target:  l \+= 1         else:             r \-= 1     return \[\] \# Time: O(n), Space: O(1)   \# Sliding Window def max\_subarray\_sum(arr, k):     window \= sum(arr\[:k\])     best \= window     for i in range(k, len(arr)):         window \+= arr\[i\] \- arr\[i-k\]         best \= max(best, window)     return best \# Time: O(n), Space: O(1)   \# Kadane's Algorithm (Maximum Subarray) def kadane(arr):     max\_sum \= cur \= arr\[0\]     for x in arr\[1:\]:         cur \= max(x, cur \+ x)         max\_sum \= max(max\_sum, cur)     return max\_sum \# Time: O(n), Space: O(1) |
| :---- |

| When to Use Arrays Use arrays when you need fast random access, when data size is known, or for cache-friendly sequential processing. Avoid when frequent insertions/deletions at arbitrary positions are needed. |
| :---- |

# **3\. Linked Lists**

| What is a Linked List? A sequence of nodes where each node stores a value and a pointer to the next node. Unlike arrays, nodes are NOT stored contiguously in memory. No random access — must traverse from head. |
| :---- |

**Singly Linked List Complexity**

| Operation | Time Complexity | Space Complexity |
| :---: | :---: | :---: |
| Access by index | **O(n)** | **O(1)** |
| Search | **O(n)** | **O(1)** |
| Insert at head | **O(1)** | **O(1)** |
| Insert at tail | **O(n)\*** | **O(1)** |
| Insert at index | **O(n)** | **O(1)** |
| Delete at head | **O(1)** | **O(1)** |
| Delete at index | **O(n)** | **O(1)** |

\* O(1) if tail pointer is maintained.

| class Node:     def \_\_init\_\_(self, val=0, next=None):         self.val \= val         self.next \= next   class LinkedList:     def \_\_init\_\_(self):         self.head \= None         self.size \= 0       \# Insert at head — O(1)     def prepend(self, val):         self.head \= Node(val, self.head)         self.size \+= 1       \# Insert at end — O(n)     def append(self, val):         new\_node \= Node(val)         if not self.head:             self.head \= new\_node             return         cur \= self.head         while cur.next:             cur \= cur.next         cur.next \= new\_node         self.size \+= 1       \# Delete by value — O(n)     def delete(self, val):         if not self.head: return         if self.head.val \== val:             self.head \= self.head.next             return         cur \= self.head         while cur.next:             if cur.next.val \== val:                 cur.next \= cur.next.next                 return             cur \= cur.next       \# Reverse in-place — O(n), Space O(1)     def reverse(self):         prev, cur \= None, self.head         while cur:             nxt \= cur.next             cur.next \= prev             prev \= cur             cur \= nxt         self.head \= prev       def to\_list(self):         result, cur \= \[\], self.head         while cur:             result.append(cur.val)             cur \= cur.next         return result   \# ── Classic Linked List Patterns ──   \# Floyd's Cycle Detection — O(n), Space O(1) def has\_cycle(head):     slow \= fast \= head     while fast and fast.next:         slow \= slow.next         fast \= fast.next.next         if slow \== fast:             return True     return False   \# Find middle (slow/fast pointers) — O(n) def find\_middle(head):     slow \= fast \= head     while fast and fast.next:         slow \= slow.next         fast \= fast.next.next     return slow          \# slow is at the middle   \# Merge two sorted lists — O(n+m) def merge\_sorted(l1, l2):     dummy \= cur \= Node(0)     while l1 and l2:         if l1.val \<= l2.val:             cur.next \= l1; l1 \= l1.next         else:             cur.next \= l2; l2 \= l2.next         cur \= cur.next     cur.next \= l1 or l2     return dummy.next |
| :---- |

**Doubly Linked List**

| class DNode:     def \_\_init\_\_(self, val=0):         self.val  \= val         self.prev \= None         self.next \= None   class DoublyLinkedList:     def \_\_init\_\_(self):         \# Sentinel nodes eliminate edge cases         self.head \= DNode(0)         self.tail \= DNode(0)         self.head.next \= self.tail         self.tail.prev \= self.head       def insert\_after(self, node, val):     \# O(1)         new \= DNode(val)         new.prev, new.next \= node, node.next         node.next.prev \= new         node.next \= new       def remove(self, node):                \# O(1)         node.prev.next \= node.next         node.next.prev \= node.prev |
| :---- |

# **4\. Stacks**

| What is a Stack? A Last-In First-Out (LIFO) data structure. Think of a stack of plates — you can only add or remove from the top. All core operations run in O(1) time. |
| :---- |

| Operation | Time Complexity | Space Complexity |
| :---: | :---: | :---: |
| Push (add to top) | **O(1)** | **O(1)** |
| Pop (remove top) | **O(1)** | **O(1)** |
| Peek (view top) | **O(1)** | **O(1)** |
| Search | **O(n)** | **O(1)** |
| Space (n elements) | **—** | **O(n)** |

| \# Python list as stack (most common approach) stack \= \[\] stack.append(10)   \# push — O(1) stack.append(20) stack.append(30) top \= stack\[-1\]    \# peek — O(1) → 30 val \= stack.pop()  \# pop  — O(1) → 30   \# ── OOP Stack ── class Stack:     def \_\_init\_\_(self):         self.\_data \= \[\]       def push(self, val):  return self.\_data.append(val)     def pop(self):        return self.\_data.pop() if self.\_data else None     def peek(self):       return self.\_data\[-1\] if self.\_data else None     def is\_empty(self):   return len(self.\_data) \== 0     def size(self):       return len(self.\_data)   \# ── Classic Stack Problems ──   \# Valid Parentheses — O(n), Space O(n) def is\_valid(s):     stack \= \[\]     mapping \= {')': '(', '}': '{', '\]': '\['}     for ch in s:         if ch in mapping:             top \= stack.pop() if stack else '\#'             if mapping\[ch\] \!= top:                 return False         else:             stack.append(ch)     return not stack   \# Next Greater Element — O(n), Space O(n) (Monotonic Stack) def next\_greater(nums):     result \= \[-1\] \* len(nums)     stack \= \[\]   \# stores indices     for i, n in enumerate(nums):         while stack and nums\[stack\[-1\]\] \< n:             result\[stack.pop()\] \= n         stack.append(i)     return result   \# Min Stack — O(1) for all operations class MinStack:     def \_\_init\_\_(self):         self.stack \= \[\]         self.min\_stack \= \[\]       def push(self, val):         self.stack.append(val)         m \= min(val, self.min\_stack\[-1\] if self.min\_stack else val)         self.min\_stack.append(m)       def pop(self):         self.stack.pop(); self.min\_stack.pop()       def get\_min(self): return self.min\_stack\[-1\] |
| :---- |

# **5\. Queues**

| What is a Queue? A First-In First-Out (FIFO) data structure. Think of a checkout line — first person in is first served. Use collections.deque for O(1) enqueue/dequeue in Python. |
| :---- |

| Operation | Time Complexity | Space Complexity |
| :---: | :---: | :---: |
| Enqueue (add rear) | **O(1)** | **O(1)** |
| Dequeue (remove front) | **O(1)** | **O(1)** |
| Peek front | **O(1)** | **O(1)** |
| Search | **O(n)** | **O(1)** |
| Space (n elements) | **—** | **O(n)** |

| from collections import deque   \# ── Basic Queue ── q \= deque() q.append(1)       \# enqueue — O(1) q.append(2) q.append(3) front \= q\[0\]      \# peek    — O(1) val \= q.popleft() \# dequeue — O(1) ← use deque NOT list.pop(0)   \# list.pop(0) is O(n)\! Always use deque for queues.   \# ── OOP Queue ── class Queue:     def \_\_init\_\_(self):         self.\_data \= deque()       def enqueue(self, val):  self.\_data.append(val)     def dequeue(self):       return self.\_data.popleft() if self.\_data else None     def peek(self):          return self.\_data\[0\] if self.\_data else None     def is\_empty(self):      return len(self.\_data) \== 0   \# ── Priority Queue (Min-Heap) ── import heapq   pq \= \[\] heapq.heappush(pq, (1, "low priority")) heapq.heappush(pq, (10, "high priority")) heapq.heappush(pq, (5, "medium")) print(heapq.heappop(pq))   \# (1, "low priority") — smallest first \# heappush/heappop: O(log n)   \# ── BFS using Queue (core graph/tree pattern) ── from collections import defaultdict   def bfs(graph, start):     visited \= set(\[start\])     queue \= deque(\[start\])     order \= \[\]     while queue:         node \= queue.popleft()         order.append(node)         for neighbor in graph\[node\]:             if neighbor not in visited:                 visited.add(neighbor)                 queue.append(neighbor)     return order \# Time: O(V+E), Space: O(V)   \# ── Circular Queue ── class CircularQueue:     def \_\_init\_\_(self, k):         self.q \= \[None\] \* k         self.head \= self.tail \= \-1         self.k \= k; self.size \= 0       def enqueue(self, val):         if self.size \== self.k: return False         self.tail \= (self.tail \+ 1\) % self.k         self.q\[self.tail\] \= val         if self.head \== \-1: self.head \= 0         self.size \+= 1; return True       def dequeue(self):         if self.size \== 0: return False         self.head \= (self.head \+ 1\) % self.k         self.size \-= 1; return True |
| :---- |

# **6\. Hash Tables (Dictionaries & Sets)**

| What is a Hash Table? Maps keys to values using a hash function. Python's dict and set are hash tables. Provides average O(1) for insert, delete, and lookup. Worst case O(n) due to hash collisions. |
| :---- |

| Operation | Time Complexity | Space Complexity |
| :---: | :---: | :---: |
| Insert | **O(1) avg / O(n) worst** | **O(1)** |
| Delete | **O(1) avg / O(n) worst** | **O(1)** |
| Lookup | **O(1) avg / O(n) worst** | **O(1)** |
| Iteration | **O(n)** | **O(1)** |
| Space total | **—** | **O(n)** |

| \# ── dict (key-value store) ── d \= {} d\["name"\] \= "Alice"       \# insert  — O(1) d\["age"\]  \= 30 val \= d.get("name", None) \# lookup  — O(1), returns None if missing del d\["age"\]              \# delete  — O(1) "name" in d               \# check   — O(1)   \# ── set (unique keys, no values) ── s \= {1, 2, 3} s.add(4)                  \# O(1) s.discard(2)              \# O(1) 3 in s                    \# O(1) s1 & s2                   \# intersection — O(min(len(s1), len(s2))) s1 | s2                   \# union         — O(len(s1) \+ len(s2))   \# ── Common Hash Table Patterns ──   \# Frequency Counter — O(n) from collections import Counter def top\_k\_frequent(nums, k):     count \= Counter(nums)     return \[x for x, \_ in count.most\_common(k)\]   \# Two Sum — O(n), Space O(n) def two\_sum(nums, target):     seen \= {}     for i, n in enumerate(nums):         complement \= target \- n         if complement in seen:             return \[seen\[complement\], i\]         seen\[n\] \= i     return \[\]   \# Group Anagrams — O(n \* k log k) where k \= word length def group\_anagrams(strs):     from collections import defaultdict     groups \= defaultdict(list)     for s in strs:         key \= tuple(sorted(s))   \# canonical form         groups\[key\].append(s)     return list(groups.values())   \# LRU Cache using OrderedDict — O(1) get/put from collections import OrderedDict class LRUCache:     def \_\_init\_\_(self, capacity):         self.cap \= capacity         self.cache \= OrderedDict()       def get(self, key):         if key not in self.cache: return \-1         self.cache.move\_to\_end(key)         return self.cache\[key\]       def put(self, key, value):         if key in self.cache: self.cache.move\_to\_end(key)         self.cache\[key\] \= value         if len(self.cache) \> self.cap:             self.cache.popitem(last=False)  \# remove least recently used |
| :---- |

# **7\. Trees**

| What is a Tree? A hierarchical data structure with a root node and children. Trees have no cycles. A Binary Tree has at most 2 children per node. A BST adds the ordering property: left \< node \< right. |
| :---- |

**Binary Search Tree (BST) Complexity**

| Operation | Time Complexity | Space Complexity |
| :---: | :---: | :---: |
| Search | **O(log n) avg / O(n) worst** | **O(h)** |
| Insert | **O(log n) avg / O(n) worst** | **O(h)** |
| Delete | **O(log n) avg / O(n) worst** | **O(h)** |
| Min/Max | **O(log n) avg / O(n) worst** | **O(h)** |
| In-order traversal | **O(n)** | **O(h)** |

h \= tree height. For balanced BST: h \= O(log n). Worst case (skewed): h \= O(n).

| class TreeNode:     def \_\_init\_\_(self, val=0, left=None, right=None):         self.val   \= val         self.left  \= left         self.right \= right   \# ── BST Operations ── class BST:     def \_\_init\_\_(self):         self.root \= None       def insert(self, val):                        \# O(log n) avg         def \_insert(node, val):             if not node: return TreeNode(val)             if val \< node.val:   node.left  \= \_insert(node.left,  val)             elif val \> node.val: node.right \= \_insert(node.right, val)             return node         self.root \= \_insert(self.root, val)       def search(self, val):                        \# O(log n) avg         node \= self.root         while node:             if val \== node.val:   return True             elif val \< node.val:  node \= node.left             else:                 node \= node.right         return False   \# ── Tree Traversals ──   def inorder(root):     \# Left → Root → Right (sorted for BST)     return inorder(root.left) \+ \[root.val\] \+ inorder(root.right) if root else \[\]   def preorder(root):    \# Root → Left → Right     return \[root.val\] \+ preorder(root.left) \+ preorder(root.right) if root else \[\]   def postorder(root):   \# Left → Right → Root     return postorder(root.left) \+ postorder(root.right) \+ \[root.val\] if root else \[\]   def level\_order(root): \# BFS — level by level     if not root: return \[\]     from collections import deque     result, q \= \[\], deque(\[root\])     while q:         level \= \[\]         for \_ in range(len(q)):             node \= q.popleft()             level.append(node.val)             if node.left:  q.append(node.left)             if node.right: q.append(node.right)         result.append(level)     return result   \# ── Classic Tree Algorithms ──   def max\_depth(root):           \# O(n), Space O(h)     if not root: return 0     return 1 \+ max(max\_depth(root.left), max\_depth(root.right))   def is\_balanced(root):         \# O(n)     def check(node):         if not node: return 0         l \= check(node.left);  r \= check(node.right)         if l \== \-1 or r \== \-1 or abs(l-r) \> 1: return \-1         return 1 \+ max(l, r)     return check(root) \!= \-1   def lowest\_common\_ancestor(root, p, q):   \# O(n)     if not root or root \== p or root \== q: return root     left  \= lowest\_common\_ancestor(root.left,  p, q)     right \= lowest\_common\_ancestor(root.right, p, q)     if left and right: return root     return left or right   def diameter(root):            \# O(n) — longest path between any 2 nodes     res \= \[0\]     def depth(node):         if not node: return 0         l, r \= depth(node.left), depth(node.right)         res\[0\] \= max(res\[0\], l \+ r)         return 1 \+ max(l, r)     depth(root)     return res\[0\] |
| :---- |

**AVL Tree (Self-Balancing BST)**

| \# AVL Tree maintains |balance\_factor| \<= 1 after every insert/delete. \# Balance factor \= height(left) \- height(right)   class AVLNode:     def \_\_init\_\_(self, val):         self.val, self.left, self.right \= val, None, None         self.height \= 1   def get\_height(n): return n.height if n else 0   def rotate\_right(y):     x \= y.left; T2 \= x.right     x.right \= y; y.left \= T2     y.height \= 1 \+ max(get\_height(y.left), get\_height(y.right))     x.height \= 1 \+ max(get\_height(x.left), get\_height(x.right))     return x   def rotate\_left(x):     y \= x.right; T2 \= y.left     y.left \= x; x.right \= T2     x.height \= 1 \+ max(get\_height(x.left), get\_height(x.right))     y.height \= 1 \+ max(get\_height(y.left), get\_height(y.right))     return y \# AVL guarantees O(log n) for all operations at all times |
| :---- |

# **8\. Heaps & Priority Queues**

| What is a Heap? A complete binary tree satisfying the heap property: in a min-heap, every parent \<= its children. Python's heapq module implements a min-heap. To get a max-heap, negate values. |
| :---- |

| Operation | Time Complexity | Space Complexity |
| :---: | :---: | :---: |
| heappush (insert) | **O(log n)** | **O(1)** |
| heappop (remove min) | **O(log n)** | **O(1)** |
| heappeek (view min) | **O(1)** | **O(1)** |
| heapify (build heap) | **O(n)** | **O(1)** |
| nlargest / nsmallest | **O(n log k)** | **O(k)** |

| import heapq   \# ── Min-Heap ── heap \= \[\] heapq.heappush(heap, 3\) heapq.heappush(heap, 1\) heapq.heappush(heap, 4\) print(heap\[0\])              \# peek min — O(1)  → 1 print(heapq.heappop(heap))  \# pop  min — O(log n) → 1   \# Build heap from list — O(n) arr \= \[5, 3, 8, 1, 9, 2\] heapq.heapify(arr)   \# Max-Heap (negate values) max\_heap \= \[\] heapq.heappush(max\_heap, \-10) heapq.heappush(max\_heap, \-5) max\_val \= \-heapq.heappop(max\_heap)  \# → 10   \# K Largest Elements — O(n log k) def k\_largest(nums, k):     return heapq.nlargest(k, nums)   \# Kth Largest — O(n log k) def kth\_largest(nums, k):     heap \= nums\[:k\]     heapq.heapify(heap)     for n in nums\[k:\]:         if n \> heap\[0\]:             heapq.heapreplace(heap, n)     return heap\[0\]   \# Merge K Sorted Lists — O(n log k) def merge\_k\_sorted(lists):     result \= \[\]     heap \= \[(lst\[0\], i, 0\) for i, lst in enumerate(lists) if lst\]     heapq.heapify(heap)     while heap:         val, i, j \= heapq.heappop(heap)         result.append(val)         if j \+ 1 \< len(lists\[i\]):             heapq.heappush(heap, (lists\[i\]\[j+1\], i, j+1))     return result   \# Median from Data Stream — O(log n) per add, O(1) per find class MedianFinder:     def \_\_init\_\_(self):         self.lo \= \[\]   \# max-heap (lower half)         self.hi \= \[\]   \# min-heap (upper half)       def add\_num(self, num):         heapq.heappush(self.lo, \-num)         heapq.heappush(self.hi, \-heapq.heappop(self.lo))         if len(self.hi) \> len(self.lo):             heapq.heappush(self.lo, \-heapq.heappop(self.hi))       def find\_median(self):         if len(self.lo) \> len(self.hi):             return \-self.lo\[0\]         return (-self.lo\[0\] \+ self.hi\[0\]) / 2 |
| :---- |

# **9\. Graphs**

| What is a Graph? A set of vertices (nodes) connected by edges. Can be directed or undirected, weighted or unweighted, cyclic or acyclic. Represented as adjacency list (most common) or adjacency matrix. |
| :---- |

| Operation | Time Complexity | Space Complexity |
| :---: | :---: | :---: |
| BFS / DFS | **O(V \+ E)** | **O(V)** |
| Dijkstra (heap) | **O((V+E) log V)** | **O(V)** |
| Bellman-Ford | **O(V \* E)** | **O(V)** |
| Floyd-Warshall | **O(V³)** | **O(V²)** |
| Topological Sort | **O(V \+ E)** | **O(V)** |
| Union-Find | **O(α(V)) ≈ O(1)** | **O(V)** |

| from collections import defaultdict, deque import heapq   \# ── Graph Representation ── graph \= defaultdict(list)           \# adjacency list (undirected) graph\[0\].append(1); graph\[1\].append(0) graph\[0\].append(2); graph\[2\].append(0) graph\[1\].append(3); graph\[3\].append(1)   \# ── DFS (Depth-First Search) — O(V+E) ── def dfs(graph, start, visited=None):     if visited is None: visited \= set()     visited.add(start)     print(start, end=" ")     for neighbor in graph\[start\]:         if neighbor not in visited:             dfs(graph, neighbor, visited)   def dfs\_iterative(graph, start):     visited, stack \= set(), \[start\]     while stack:         node \= stack.pop()         if node in visited: continue         visited.add(node)         stack.extend(graph\[node\])     return visited   \# ── BFS (Breadth-First Search) — O(V+E) ── def bfs(graph, start):     visited \= {start}     queue \= deque(\[start\])     order \= \[\]     while queue:         node \= queue.popleft()         order.append(node)         for nbr in graph\[node\]:             if nbr not in visited:                 visited.add(nbr)                 queue.append(nbr)     return order   \# ── Dijkstra's Shortest Path — O((V+E) log V) ── def dijkstra(graph, src, n):     dist \= \[float('inf')\] \* n     dist\[src\] \= 0     heap \= \[(0, src)\]              \# (distance, node)     while heap:         d, u \= heapq.heappop(heap)         if d \> dist\[u\]: continue  \# stale entry         for v, w in graph\[u\]:     \# (neighbor, weight)             if dist\[u\] \+ w \< dist\[v\]:                 dist\[v\] \= dist\[u\] \+ w                 heapq.heappush(heap, (dist\[v\], v))     return dist   \# ── Topological Sort (Kahn's BFS) — O(V+E) ── def topo\_sort(n, prerequisites):     indegree \= \[0\] \* n     adj \= defaultdict(list)     for a, b in prerequisites:         adj\[b\].append(a)         indegree\[a\] \+= 1     queue \= deque(\[i for i in range(n) if indegree\[i\] \== 0\])     order \= \[\]     while queue:         node \= queue.popleft()         order.append(node)         for nbr in adj\[node\]:             indegree\[nbr\] \-= 1             if indegree\[nbr\] \== 0:                 queue.append(nbr)     return order if len(order) \== n else \[\]   \# empty \= cycle detected   \# ── Union-Find (Disjoint Set Union) — near O(1) per op ── class UnionFind:     def \_\_init\_\_(self, n):         self.parent \= list(range(n))         self.rank   \= \[0\] \* n       def find(self, x):               \# path compression         if self.parent\[x\] \!= x:             self.parent\[x\] \= self.find(self.parent\[x\])         return self.parent\[x\]       def union(self, x, y):           \# union by rank         px, py \= self.find(x), self.find(y)         if px \== py: return False         if self.rank\[px\] \< self.rank\[py\]: px, py \= py, px         self.parent\[py\] \= px         if self.rank\[px\] \== self.rank\[py\]: self.rank\[px\] \+= 1         return True   \# ── Detect Cycle in Directed Graph ── def has\_cycle(n, edges):     adj \= defaultdict(list)     for u, v in edges: adj\[u\].append(v)     WHITE, GRAY, BLACK \= 0, 1, 2     color \= \[WHITE\] \* n       def dfs(u):         color\[u\] \= GRAY         for v in adj\[u\]:             if color\[v\] \== GRAY: return True     \# back edge \= cycle             if color\[v\] \== WHITE and dfs(v): return True         color\[u\] \= BLACK         return False       return any(dfs(i) for i in range(n) if color\[i\] \== WHITE) |
| :---- |

# **10\. Sorting Algorithms**

**Complexity Comparison**

| Algorithm | Time (Best/Avg/Worst) | Space — Stability |
| :---: | :---: | :---: |
| Bubble Sort | **O(n²) / O(n²) / O(n)** | **O(1) — Stable** |
| Selection Sort | **O(n²) / O(n²) / O(n²)** | **O(1) — Unstable** |
| Insertion Sort | **O(n²) / O(n²) / O(n)** | **O(1) — Stable** |
| Merge Sort | **O(n log n) all cases** | **O(n) — Stable** |
| Quick Sort | **O(n log n) / O(n²) worst** | **O(log n) — Unstable** |
| Heap Sort | **O(n log n) all cases** | **O(1) — Unstable** |
| Counting Sort | **O(n \+ k)** | **O(n \+ k) — Stable** |
| Radix Sort | **O(d \* (n \+ k))** | **O(n \+ k) — Stable** |

| \# ── Bubble Sort — O(n²) ── def bubble\_sort(arr):     n \= len(arr)     for i in range(n):         swapped \= False         for j in range(n \- i \- 1):             if arr\[j\] \> arr\[j+1\]:                 arr\[j\], arr\[j+1\] \= arr\[j+1\], arr\[j\]                 swapped \= True         if not swapped: break   \# already sorted — O(n) best case     return arr   \# ── Insertion Sort — O(n²) but great for small/nearly sorted arrays ── def insertion\_sort(arr):     for i in range(1, len(arr)):         key \= arr\[i\]         j \= i \- 1         while j \>= 0 and arr\[j\] \> key:             arr\[j+1\] \= arr\[j\]             j \-= 1         arr\[j+1\] \= key     return arr   \# ── Merge Sort — O(n log n), Stable, O(n) space ── def merge\_sort(arr):     if len(arr) \<= 1: return arr     mid \= len(arr) // 2     left  \= merge\_sort(arr\[:mid\])     right \= merge\_sort(arr\[mid:\])     return merge(left, right)   def merge(left, right):     result \= \[\]     i \= j \= 0     while i \< len(left) and j \< len(right):         if left\[i\] \<= right\[j\]: result.append(left\[i\]);  i \+= 1         else:                   result.append(right\[j\]); j \+= 1     return result \+ left\[i:\] \+ right\[j:\]   \# ── Quick Sort — O(n log n) avg, O(n²) worst ── def quick\_sort(arr, lo=0, hi=None):     if hi is None: hi \= len(arr) \- 1     if lo \< hi:         p \= partition(arr, lo, hi)         quick\_sort(arr, lo, p \- 1\)         quick\_sort(arr, p \+ 1, hi)     return arr   def partition(arr, lo, hi):     pivot \= arr\[hi\]     i \= lo \- 1     for j in range(lo, hi):         if arr\[j\] \<= pivot:             i \+= 1             arr\[i\], arr\[j\] \= arr\[j\], arr\[i\]     arr\[i+1\], arr\[hi\] \= arr\[hi\], arr\[i+1\]     return i \+ 1   \# ── Heap Sort — O(n log n), In-place ── def heap\_sort(arr):     import heapq     heapq.heapify(arr)     return \[heapq.heappop(arr) for \_ in range(len(arr))\]   \# ── Counting Sort — O(n+k), good when k is small ── def counting\_sort(arr, k=None):     if not arr: return arr     if k is None: k \= max(arr)     count \= \[0\] \* (k \+ 1\)     for x in arr: count\[x\] \+= 1     for i in range(1, k+1): count\[i\] \+= count\[i-1\]     output \= \[0\] \* len(arr)     for x in reversed(arr):         output\[count\[x\]-1\] \= x         count\[x\] \-= 1     return output   \# ── Python built-in (TimSort) — use this in practice\! ── arr.sort()                      \# in-place,  O(n log n), stable sorted\_arr \= sorted(arr)        \# new list,  O(n log n), stable arr.sort(key=lambda x: x\[1\])   \# sort by second element |
| :---- |

# **11\. Searching Algorithms**

| Operation | Time Complexity | Space Complexity |
| :---: | :---: | :---: |
| Linear Search | **O(n)** | **O(1)** |
| Binary Search | **O(log n)** | **O(1) iterative / O(log n) recursive** |
| Jump Search | **O(√n)** | **O(1)** |
| Interpolation Search | **O(log log n) avg** | **O(1)** |
| Exponential Search | **O(log n)** | **O(log n)** |

| \# ── Linear Search — O(n) ── def linear\_search(arr, target):     for i, x in enumerate(arr):         if x \== target: return i     return \-1   \# ── Binary Search — O(log n) ── REQUIRES SORTED ARRAY def binary\_search(arr, target):     lo, hi \= 0, len(arr) \- 1     while lo \<= hi:         mid \= lo \+ (hi \- lo) // 2     \# avoid overflow (same as (lo+hi)//2)         if arr\[mid\] \== target:   return mid         elif arr\[mid\] \< target:  lo \= mid \+ 1         else:                    hi \= mid \- 1     return \-1   \# ── Binary Search Variants ──   \# Find first position of target — O(log n) def search\_first(arr, target):     lo, hi, result \= 0, len(arr)-1, \-1     while lo \<= hi:         mid \= (lo \+ hi) // 2         if arr\[mid\] \== target:             result \= mid; hi \= mid \- 1   \# keep searching left         elif arr\[mid\] \< target: lo \= mid \+ 1         else:                   hi \= mid \- 1     return result   \# Find last position — O(log n) def search\_last(arr, target):     lo, hi, result \= 0, len(arr)-1, \-1     while lo \<= hi:         mid \= (lo \+ hi) // 2         if arr\[mid\] \== target:             result \= mid; lo \= mid \+ 1   \# keep searching right         elif arr\[mid\] \< target: lo \= mid \+ 1         else:                   hi \= mid \- 1     return result   \# Search in rotated sorted array — O(log n) def search\_rotated(nums, target):     lo, hi \= 0, len(nums) \- 1     while lo \<= hi:         mid \= (lo \+ hi) // 2         if nums\[mid\] \== target: return mid         if nums\[lo\] \<= nums\[mid\]:            \# left half is sorted             if nums\[lo\] \<= target \< nums\[mid\]: hi \= mid \- 1             else:                              lo \= mid \+ 1         else:                                \# right half is sorted             if nums\[mid\] \< target \<= nums\[hi\]: lo \= mid \+ 1             else:                              hi \= mid \- 1     return \-1   \# Binary search on answer — O(n log n) def min\_capacity\_ships(weights, days):     lo, hi \= max(weights), sum(weights)     while lo \< hi:         mid \= (lo \+ hi) // 2         used\_days \= 1; cur\_weight \= 0         for w in weights:             if cur\_weight \+ w \> mid:                 used\_days \+= 1; cur\_weight \= 0             cur\_weight \+= w         if used\_days \<= days: hi \= mid         else:                 lo \= mid \+ 1     return lo   \# Python built-in bisect — O(log n) import bisect arr \= \[1, 3, 5, 7, 9\] pos \= bisect.bisect\_left(arr, 5\)    \# leftmost position for 5 → 2 bisect.insort(arr, 6\)               \# insert maintaining sort order |
| :---- |

# **12\. Dynamic Programming (DP)**

| What is Dynamic Programming? An optimization technique that solves complex problems by breaking them into overlapping subproblems and storing results (memoization/tabulation) to avoid recomputation. Key condition: optimal substructure \+ overlapping subproblems. |
| :---- |

**Top-Down (Memoization) vs Bottom-Up (Tabulation)**

| \# ── Fibonacci: naive O(2^n) vs DP O(n) ──   \# Naive recursion — O(2^n), Space O(n) call stack def fib\_naive(n):     if n \<= 1: return n     return fib\_naive(n-1) \+ fib\_naive(n-2)   \# Top-Down (Memoization) — O(n), Space O(n) from functools import lru\_cache   @lru\_cache(maxsize=None) def fib\_memo(n):     if n \<= 1: return n     return fib\_memo(n-1) \+ fib\_memo(n-2)   \# Bottom-Up (Tabulation) — O(n), Space O(n) def fib\_tab(n):     if n \<= 1: return n     dp \= \[0\] \* (n+1)     dp\[1\] \= 1     for i in range(2, n+1):         dp\[i\] \= dp\[i-1\] \+ dp\[i-2\]     return dp\[n\]   \# Optimized — O(n), Space O(1) def fib\_opt(n):     a, b \= 0, 1     for \_ in range(n): a, b \= b, a \+ b     return a   \# ── 0/1 Knapsack — O(n\*W), Space O(n\*W) ── def knapsack(weights, values, W):     n \= len(weights)     dp \= \[\[0\]\*(W+1) for \_ in range(n+1)\]     for i in range(1, n+1):         for w in range(W+1):             dp\[i\]\[w\] \= dp\[i-1\]\[w\]                         \# skip item             if weights\[i-1\] \<= w:                 dp\[i\]\[w\] \= max(dp\[i\]\[w\],                                dp\[i-1\]\[w-weights\[i-1\]\] \+ values\[i-1\])  \# take item     return dp\[n\]\[W\]   \# ── Longest Common Subsequence (LCS) — O(m\*n) ── def lcs(s1, s2):     m, n \= len(s1), len(s2)     dp \= \[\[0\]\*(n+1) for \_ in range(m+1)\]     for i in range(1, m+1):         for j in range(1, n+1):             if s1\[i-1\] \== s2\[j-1\]: dp\[i\]\[j\] \= dp\[i-1\]\[j-1\] \+ 1             else:                   dp\[i\]\[j\] \= max(dp\[i-1\]\[j\], dp\[i\]\[j-1\])     return dp\[m\]\[n\]   \# ── Longest Increasing Subsequence (LIS) — O(n log n) ── import bisect def lis(nums):     tails \= \[\]     for x in nums:         pos \= bisect.bisect\_left(tails, x)         if pos \== len(tails): tails.append(x)         else:                 tails\[pos\] \= x     return len(tails)   \# ── Coin Change — O(n \* amount), Space O(amount) ── def coin\_change(coins, amount):     dp \= \[float('inf')\] \* (amount \+ 1\)     dp\[0\] \= 0     for coin in coins:         for a in range(coin, amount \+ 1):             dp\[a\] \= min(dp\[a\], dp\[a-coin\] \+ 1\)     return dp\[amount\] if dp\[amount\] \!= float('inf') else \-1   \# ── Edit Distance (Levenshtein) — O(m\*n) ── def edit\_distance(s1, s2):     m, n \= len(s1), len(s2)     dp \= \[\[0\]\*(n+1) for \_ in range(m+1)\]     for i in range(m+1): dp\[i\]\[0\] \= i     for j in range(n+1): dp\[0\]\[j\] \= j     for i in range(1, m+1):         for j in range(1, n+1):             if s1\[i-1\] \== s2\[j-1\]: dp\[i\]\[j\] \= dp\[i-1\]\[j-1\]             else: dp\[i\]\[j\] \= 1 \+ min(dp\[i-1\]\[j\], dp\[i\]\[j-1\], dp\[i-1\]\[j-1\])     return dp\[m\]\[n\] |
| :---- |

# **13\. Greedy Algorithms**

| What is a Greedy Algorithm? Makes the locally optimal choice at each step, hoping it leads to the global optimum. Greedy works when the problem has the 'greedy choice property' — a local optimum leads to a global one. Faster than DP but not always correct. |
| :---- |

| \# ── Activity Selection — O(n log n) ── def activity\_selection(activities):     \# activities \= \[(start, end), ...\]     activities.sort(key=lambda x: x\[1\])  \# sort by end time     selected \= \[activities\[0\]\]     last\_end \= activities\[0\]\[1\]     for start, end in activities\[1:\]:         if start \>= last\_end:             selected.append((start, end))             last\_end \= end     return selected   \# ── Huffman Coding — O(n log n) ── import heapq def huffman\_codes(freq):     heap \= \[\[f, \[sym, ""\]\] for sym, f in freq.items()\]     heapq.heapify(heap)     while len(heap) \> 1:         lo \= heapq.heappop(heap)         hi \= heapq.heappop(heap)         for pair in lo\[1:\]: pair\[1\] \= '0' \+ pair\[1\]         for pair in hi\[1:\]: pair\[1\] \= '1' \+ pair\[1\]         heapq.heappush(heap, \[lo\[0\]+hi\[0\]\] \+ lo\[1:\] \+ hi\[1:\])     return sorted(heapq.heappop(heap)\[1:\], key=lambda x: len(x\[1\]))   \# ── Jump Game — O(n) ── def can\_jump(nums):     max\_reach \= 0     for i, n in enumerate(nums):         if i \> max\_reach: return False         max\_reach \= max(max\_reach, i \+ n)     return True   \# ── Minimum number of platforms (Interval Scheduling) — O(n log n) ── def min\_platforms(arrivals, departures):     arrivals.sort(); departures.sort()     platforms \= max\_platforms \= 0     i \= j \= 0     while i \< len(arrivals):         if arrivals\[i\] \< departures\[j\]:             platforms \+= 1; i \+= 1             max\_platforms \= max(max\_platforms, platforms)         else:             platforms \-= 1; j \+= 1     return max\_platforms   \# ── Gas Station — O(n) ── def can\_complete\_circuit(gas, cost):     if sum(gas) \< sum(cost): return \-1     tank \= start \= 0     for i in range(len(gas)):         tank \+= gas\[i\] \- cost\[i\]         if tank \< 0:             start \= i \+ 1; tank \= 0     return start |
| :---- |

# **14\. Backtracking**

| What is Backtracking? A refined brute-force that builds solutions incrementally and abandons (backtracks) a path as soon as it determines the path cannot lead to a valid solution. Uses recursion and undoing choices. |
| :---- |

| Operation | Time Complexity | Space Complexity |
| :---: | :---: | :---: |
| Permutations | **O(n \* n\!)** | **O(n)** |
| Combinations | **O(k \* C(n,k))** | **O(k)** |
| Subsets | **O(n \* 2^n)** | **O(n)** |
| N-Queens | **O(n\!)** | **O(n)** |
| Sudoku Solver | **O(9^(n\*n))** | **O(n²)** |

| \# ── Permutations — O(n \* n\!) ── def permutations(nums):     result \= \[\]     def backtrack(path, remaining):         if not remaining:             result.append(path\[:\]); return         for i in range(len(remaining)):             path.append(remaining\[i\])             backtrack(path, remaining\[:i\] \+ remaining\[i+1:\])             path.pop()     backtrack(\[\], nums)     return result   \# ── Subsets (Power Set) — O(n \* 2^n) ── def subsets(nums):     result \= \[\]     def backtrack(start, path):         result.append(path\[:\])         for i in range(start, len(nums)):             path.append(nums\[i\])             backtrack(i \+ 1, path)             path.pop()     backtrack(0, \[\])     return result   \# ── Combination Sum — O(2^n) ── def combination\_sum(candidates, target):     result \= \[\]     candidates.sort()     def backtrack(start, path, remaining):         if remaining \== 0:             result.append(path\[:\]); return         for i in range(start, len(candidates)):             if candidates\[i\] \> remaining: break    \# pruning\!             path.append(candidates\[i\])             backtrack(i, path, remaining \- candidates\[i\])             path.pop()     backtrack(0, \[\], target)     return result   \# ── N-Queens — O(n\!) ── def solve\_n\_queens(n):     results \= \[\]     cols \= set(); diag1 \= set(); diag2 \= set()       def backtrack(row, board):         if row \== n:             results.append(\["".join(r) for r in board\]); return         for col in range(n):             if col in cols or (row-col) in diag1 or (row+col) in diag2:                 continue             cols.add(col); diag1.add(row-col); diag2.add(row+col)             board\[row\]\[col\] \= 'Q'             backtrack(row \+ 1, board)             board\[row\]\[col\] \= '.'             cols.discard(col); diag1.discard(row-col); diag2.discard(row+col)       board \= \[\['.'\]\*n for \_ in range(n)\]     backtrack(0, board)     return results |
| :---- |

# **15\. Trie (Prefix Tree)**

| What is a Trie? A tree for storing strings where each node represents a character. All children of a node share the same prefix. Used for autocomplete, spell-check, and IP routing. Insert/Search/StartsWith all run in O(L) where L is the word length. |
| :---- |

| Operation | Time Complexity | Space Complexity |
| :---: | :---: | :---: |
| Insert word | **O(L)** | **O(L)** |
| Search word | **O(L)** | **O(1)** |
| Starts with prefix | **O(L)** | **O(1)** |
| Delete word | **O(L)** | **O(1)** |
| Space (n words avg L) | **—** | **O(n \* L)** |

| class TrieNode:     def \_\_init\_\_(self):         self.children \= {}         self.is\_end   \= False   class Trie:     def \_\_init\_\_(self):         self.root \= TrieNode()       def insert(self, word):             \# O(L)         node \= self.root         for ch in word:             if ch not in node.children:                 node.children\[ch\] \= TrieNode()             node \= node.children\[ch\]         node.is\_end \= True       def search(self, word):             \# O(L)         node \= self.root         for ch in word:             if ch not in node.children: return False             node \= node.children\[ch\]         return node.is\_end       def starts\_with(self, prefix):      \# O(L)         node \= self.root         for ch in prefix:             if ch not in node.children: return False             node \= node.children\[ch\]         return True       def delete(self, word):             \# O(L)         def \_delete(node, word, depth):             if depth \== len(word):                 if node.is\_end: node.is\_end \= False                 return len(node.children) \== 0             ch \= word\[depth\]             if ch not in node.children: return False             should\_delete \= \_delete(node.children\[ch\], word, depth+1)             if should\_delete:                 del node.children\[ch\]                 return len(node.children) \== 0 and not node.is\_end             return False         \_delete(self.root, word, 0\)       def autocomplete(self, prefix):     \# O(L \+ total nodes)         node \= self.root         for ch in prefix:             if ch not in node.children: return \[\]             node \= node.children\[ch\]         results \= \[\]         def dfs(node, current):             if node.is\_end: results.append(current)             for ch, child in node.children.items():                 dfs(child, current \+ ch)         dfs(node, prefix)         return results   \# Usage trie \= Trie() for word in \["apple", "app", "application", "apply", "apt"\]:     trie.insert(word)   print(trie.search("app"))           \# True print(trie.starts\_with("appl"))     \# True print(trie.autocomplete("app"))     \# \['app', 'apple', 'application', 'apply'\] |
| :---- |

# **16\. Big-O Complexity Cheat Sheet**

| Data Structure | Best | Average | Worst | Space |
| ----- | :---: | :---: | :---: | :---: |
| **Array Access** | O(1) | O(1) | O(1) | O(n) |
| **Array Search** | O(1) | O(n) | O(n) | O(n) |
| **Array Insert/Delete** | O(1) | O(n) | O(n) | O(n) |
| **Linked List Access** | O(1) | O(n) | O(n) | O(n) |
| **Linked List Insert** | O(1) | O(1) | O(1) | O(n) |
| **Hash Table Lookup** | O(1) | O(1) | O(n) | O(n) |
| **BST Search** | O(1) | O(log n) | O(n) | O(n) |
| **BST Insert** | O(1) | O(log n) | O(n) | O(n) |
| **Heap Insert** | O(1) | O(log n) | O(log n) | O(n) |
| **Heap Remove Min** | O(1) | O(log n) | O(log n) | O(n) |
| **Bubble/Selection Sort** | O(n) | O(n²) | O(n²) | O(1) |
| **Insertion Sort** | O(n) | O(n²) | O(n²) | O(1) |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) |
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) |
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) |
| **Binary Search** | O(1) | O(log n) | O(log n) | O(1) |
| **BFS / DFS** | O(1) | O(V+E) | O(V+E) | O(V) |
| **Dijkstra** | — | O((V+E)log V) | O((V+E)log V) | O(V) |

| Quick Tips for Interviews 1\. Always ask for input constraints first — they hint at the expected complexity.2. Start with brute force, then optimize.3. Array \+ Hash Map solves \~40% of problems.4. Sliding window for subarray/substring problems.5. Two pointers for sorted arrays.6. DFS for tree/graph path problems, BFS for shortest path.7. DP when you see 'minimum/maximum/number of ways'. |
| :---- |

*Data Structures & Algorithms — Python Complete Guide*

Generated with Claude • Practice consistently • Happy coding\! 🚀