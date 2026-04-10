  
**🐍 Python Complete Reference Guide**

*Built-in Functions • Built-in Modules • Interview Questions*

Interview-Ready Edition  |  Brute Force \+ Optimized Solutions

# **PART 1 — Python Built-in Functions**

*Python ships with 68 built-in functions that are always available without any import. Below every function is explained with its purpose, when to use it, and a practical code example.*

## **1.1  Type Conversion Functions**

### **int()**

Converts a value to an integer. Strips decimal places (truncates, does not round). Accepts strings representing integers and supports an optional base argument for binary/hex/octal strings.

*💡 Use when: reading numeric input from users, converting hex/binary strings, or coercing floats for indexing.*

int(3.9)          \# → 3   (truncates, not rounds)

int("42")         \# → 42

int("1010", 2\)    \# → 10  (binary string)

int("FF", 16\)     \# → 255 (hex string)

### **float()**

Converts a value to a floating-point number. Accepts strings like '3.14', 'inf', '-inf', 'nan'.

*💡 Use when: doing division that needs decimal precision, or converting integer measurements to floats.*

float("3.14")   \# → 3.14

float(7)        \# → 7.0

float("inf")    \# → inf

### **str()**

Converts any object to its string representation. Calls the object's \_\_str\_\_ method internally.

str(100)        \# → "100"

str(\[1, 2, 3\])  \# → "\[1, 2, 3\]"

str(None)       \# → "None"

### **bool()**

Converts a value to True or False. Falsy values: 0, 0.0, '', \[\], {}, set(), None. Everything else is truthy.

bool(0)         \# → False

bool("")        \# → False

bool(\[\])        \# → False

bool(42)        \# → True

bool("hi")      \# → True

### **list()**

Creates a list from any iterable (string, tuple, set, range, generator, dict-view, etc.).

list("abc")         \# → \["a","b","c"\]

list((1,2,3))       \# → \[1,2,3\]

list(range(5))      \# → \[0,1,2,3,4\]

list({1,2,3})       \# → \[1,2,3\] (order may vary)

### **tuple()**

Creates an immutable tuple from any iterable. Tuples are hashable and can be used as dict keys.

tuple(\[1,2,3\])      \# → (1,2,3)

tuple("abc")        \# → ("a","b","c")

### **set()**

Creates a mutable, unordered collection of unique items. Duplicates are automatically removed. O(1) average lookup.

set(\[1,2,2,3\])      \# → {1,2,3}

set("hello")        \# → {"h","e","l","o"}

### **dict()**

Creates a dictionary. Accepts keyword arguments, iterable of key-value pairs, or another mapping.

dict(a=1, b=2)         \# → {'a':1,'b':2}

dict(\[('x',10)\])       \# → {'x':10}

dict(zip('ab',\[1,2\]))  \# → {'a':1,'b':2}

### **frozenset()**

Creates an immutable set. Can be used as dictionary keys or set elements. Supports all set operations.

fs \= frozenset(\[1,2,3\])  \# immutable set

d \= {fs: 'value'}        \# can be dict key

### **complex()**

Creates a complex number. Rarely used except in scientific/mathematical code.

complex(2, 3\)    \# → (2+3j)

complex("3+4j")  \# → (3+4j)

### 

### **bytes() / bytearray() / memoryview()**

bytes creates an immutable byte sequence. bytearray is mutable. memoryview exposes a buffer interface without copying data — critical for performance with large binary data.

bytes("hello","utf-8")       \# → b"hello"

bytearray(\[65,66,67\])        \# → bytearray(b'ABC')

mv \= memoryview(b'abcdef')   \# zero-copy slice

mv\[2:4\].tobytes()            \# → b'cd'

## **1.2  Numeric & Math Functions**

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| abs(x) | Absolute value of any numeric type | abs(-7.5) → 7.5 |
| round(x,n) | Round to n decimal places (banker's rounding for .5) | round(2.675,2) → 2.67 |
| pow(x,y,mod) | x\*\*y optionally mod z; fast modular exponentiation | pow(2,10,1000) → 24 |
| divmod(x,y) | Returns (quotient, remainder) as a tuple | divmod(17,5) → (3,2) |
| min(iterable) | Smallest item; supports key= argument | min(\[3,1,2\]) → 1 |
| max(iterable) | Largest item; supports key= argument | max('zoo') → 'z' |
| sum(iterable,start) | Sum of items; start defaults to 0 | sum(\[1,2,3\],10) → 16 |
| bin(x) | Binary string representation of integer | bin(10) → '0b1010' |
| oct(x) | Octal string representation of integer | oct(8) → '0o10' |
| hex(x) | Hex string representation of integer | hex(255) → '0xff' |

### **abs()**

Returns the absolute (magnitude) value. Works on int, float, and complex numbers.

abs(-5)        \# → 5

abs(-3.14)     \# → 3.14

abs(3+4j)      \# → 5.0  (magnitude of complex)

### **round()**

Rounds to the given number of decimal places. Python uses banker's rounding (round half to even) — be aware of this when financial precision matters.

round(2.5)     \# → 2  (rounds to even\!)

round(3.5)     \# → 4

round(3.14159, 2\)  \# → 3.14

### 

### **divmod()**

Returns a tuple (quotient, remainder). More efficient than doing // and % separately. Extremely useful in base-conversion problems.

*💡 Interview trick: Use divmod() to convert decimal to any base in one loop.*

q, r \= divmod(17, 5\)  \# q=3, r=2

\# Convert 255 to base 16:

num, digits \= 255, \[\]

while num: num, r \= divmod(num, 16); digits.append(r)

### **pow(x, y, mod)**

Three-argument pow is MUCH faster than (x\*\*y) % mod for large numbers — it uses fast modular exponentiation under the hood. Essential for cryptography and competitive programming.

pow(2, 100\)           \# large number

pow(2, 100, 10\*\*9+7)  \# fast mod-exp → O(log y)

## **1.3  Sequence & Iteration Functions**

### **len()**

Returns the number of items in an object. Works on lists, tuples, strings, dicts, sets, and any object implementing \_\_len\_\_.

len("hello")       \# → 5

len(\[1,\[2,3\],4\])   \# → 3  (not recursive\!)

len({})            \# → 0

### **range()**

Generates an immutable sequence of integers. range(stop), range(start,stop), range(start,stop,step). Returns a lazy range object — does NOT store values in memory.

*💡 Memory tip: range(10\*\*9) uses \~48 bytes. list(range(10\*\*9)) would use \~8 GB.*

range(5)          \# 0,1,2,3,4

range(2,10,2)     \# 2,4,6,8

range(10,0,-1)    \# 10,9,...,1

5 in range(100)   \# → True  O(1) membership test\!

### **enumerate()**

Yields (index, value) pairs while iterating. Cleaner than using a counter variable. Accepts an optional start argument to offset the index.

*💡 Prefer enumerate() over range(len(seq)) — it's more Pythonic and works on any iterable.*

for i, v in enumerate(\['a','b','c'\]):

    print(i, v)   \# 0 a, 1 b, 2 c

for i, v in enumerate(\['a','b'\], start=1):

    print(i, v)   \# 1 a, 2 b

### **zip()**

Combines multiple iterables element-wise into tuples. Stops at the shortest iterable. Use itertools.zip\_longest() to fill missing values.

zip(\[1,2,3\], \['a','b','c'\])   \# (1,'a'),(2,'b'),(3,'c')

dict(zip(keys, values))        \# fast dict creation

list(zip(\*matrix))             \# transpose a matrix\!

### **map()**

Applies a function to every item in an iterable. Returns a lazy map object. Equivalent to a generator expression.

list(map(int, \['1','2','3'\]))     \# → \[1,2,3\]

list(map(str.upper, \['a','b'\]))   \# → \['A','B'\]

list(map(lambda x: x\*\*2, \[1,2,3\]))  \# → \[1,4,9\]

### **filter()**

Filters items where the function returns True. Returns a lazy filter object. filter(None, iterable) removes all falsy values.

list(filter(None, \[0,1,'',2,False,3\]))  \# → \[1,2,3\]

list(filter(str.isdigit, 'a1b2c3'))     \# → \['1','2','3'\]

### **sorted()**

Returns a NEW sorted list. Non-destructive. Supports key= and reverse= arguments. Timsort O(n log n) — stable sort.

sorted(\[3,1,2\])               \# → \[1,2,3\]

sorted('python')              \# → \['h','n','o','p','t','y'\]

sorted(words, key=len)        \# sort by string length

sorted(d.items(), key=lambda x: x\[1\])  \# sort dict by value

sorted(lst, key=lambda x: (x\[1\],-x\[0\]))  \# multi-key sort

### **reversed()**

Returns a reverse iterator — does NOT create a new list. More memory-efficient than lst\[::-1\] for large sequences.

list(reversed(\[1,2,3\]))   \# → \[3,2,1\]

for x in reversed(range(5)):  \# 4,3,2,1,0

    print(x)

### **any() / all()**

any() returns True if at least one element is truthy. all() returns True if every element is truthy. Both short-circuit (stop early).

*💡 Interview tip: any/all with generator expressions avoid building an intermediate list.*

any(\[0, '', False, 1\])     \# → True

all(\[1, 'a', True, 3.14\]) \# → True

all(x \> 0 for x in lst)  \# short-circuit, no list built

any(s.startswith('A') for s in names)

### **iter() / next()**

iter() returns an iterator from an iterable. next() retrieves the next value, with optional default to avoid StopIteration.

it \= iter(\[1,2,3\])

next(it)          \# → 1

next(it)          \# → 2

next(it, 'end')   \# → 3

next(it, 'end')   \# → 'end'  (default, no error)

## 

## **1.4  String & Character Functions**

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| chr(i) | Unicode character from code point | chr(65) → 'A' |
| ord(c) | Unicode code point from character | ord('Z') → 90 |
| format(val,spec) | Format a value using format spec language | format(3.14159,'.2f') → '3.14' |
| repr(obj) | Official string representation (unambiguous) | repr('hi\\n') → "'hi\\\\n'" |
| ascii(obj) | Like repr() but escapes non-ASCII chars | ascii('café') → "'caf\\\\xe9'" |
| print(\*args) | Print to stdout; supports sep, end, file, flush | print(1,2,3,sep='-') |
| input(prompt) | Read a line from stdin as a string | n=int(input('n=')) |

### **chr() and ord()**

chr converts an integer Unicode code point to its character. ord does the reverse. Together they power many string manipulation interview tricks.

*💡 Interview pattern: ord(c) \- ord('a') gives the 0-25 index of a lowercase letter.*

\# Shift cipher

def shift(c, k): return chr((ord(c)-ord('a')+k)%26+ord('a'))

shift('z', 3\)   \# → 'c'

\# Check if chars differ by one position

abs(ord('b') \- ord('a')) \== 1  \# → True

## **1.5  Object & Reflection Functions**

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| type(obj) | Returns the type/class of an object | type(3.14) → \<class 'float'\> |
| isinstance(obj,cls) | True if obj is instance of cls or its subclass | isinstance(True,int) → True |
| issubclass(cls,base) | True if cls is subclass of base | issubclass(bool,int) → True |
| id(obj) | Unique identity (memory address) of object | id(x) \== id(y) checks same object |
| hash(obj) | Integer hash of an immutable object | hash('key') → integer |
| dir(obj) | List of attributes and methods of an object | dir(\[\]) → all list methods |
| vars(obj) | Return \_\_dict\_\_ of object or current scope | vars(obj) → attribute dict |
| getattr(obj,name) | Get attribute by name string; supports default | getattr(obj,'x',0) |
| setattr(obj,name,v) | Set attribute by name string dynamically | setattr(obj,'x',10) |
| hasattr(obj,name) | True if attribute exists | hasattr(lst,'append') |
| callable(obj) | True if object can be called like a function | callable(print) → True |

### **isinstance() — Most Important for Interviews**

isinstance handles inheritance correctly. type() does exact matching only. Always prefer isinstance for type-checking in production code.

isinstance(True, int)    \# → True  (bool IS-A int)

type(True) \== int        \# → False (exact match fails)

\# Checking multiple types at once:

isinstance(x, (int, float))   \# True if int OR float

## **1.6  Functional Programming Functions**

### **lambda**

Anonymous inline function. Limited to a single expression. Commonly used with sorted, map, filter, max, min.

square \= lambda x: x\*\*2

add \= lambda x, y: x \+ y

sorted(students, key=lambda s: (s\['grade'\], s\['name'\]))

### **reduce() — from functools**

Applies a function cumulatively to a sequence, reducing it to a single value. Must import from functools.

from functools import reduce

reduce(lambda a,b: a\*b, \[1,2,3,4,5\])  \# → 120 (factorial)

reduce(lambda a,b: a+b, \[1,2,3\])      \# → 6

### **globals() / locals()**

globals() returns the global namespace dict. locals() returns the local namespace. Useful for debugging and dynamic variable access.

x \= 42

globals()\['x'\]   \# → 42  (access global by name string)

### 

### 

### 

### 

### **eval() / exec() / compile()**

eval evaluates a string expression and returns the result. exec executes a string as code (no return). compile converts source to bytecode. Use with caution — never on untrusted input.

eval('2 \+ 2')          \# → 4

eval('\[x\*\*2 for x in range(5)\]')  \# → \[0,1,4,9,16\]

exec('x \= 10; print(x)')  \# prints 10

### **open()**

Opens a file and returns a file object. Always use with a context manager (with statement) to ensure the file is closed.

with open('file.txt','r') as f:

    content \= f.read()       \# entire file as string

    lines \= f.readlines()    \# list of lines

with open('out.txt','w') as f:

    f.write('hello')         \# write string

    f.writelines(\['a','b'\])  \# write list of strings

### **\_\_import\_\_() / importlib**

\_\_import\_\_ is the low-level import function. In practice, use importlib.import\_module() for dynamic imports.

import importlib

mod \= importlib.import\_module('math')

mod.sqrt(16)   \# → 4.0

## **1.7  I/O & Miscellaneous Built-ins**

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| print() | Output to stdout; sep,end,file,flush params | print(\*lst, sep=',') |
| input() | Read string from stdin | name=input('Name: ') |
| open() | Open file, returns file object | open('f.txt','r') |
| help() | Interactive help system | help(str.split) |
| breakpoint() | Drop into pdb debugger (Python 3.7+) | breakpoint() |
| \_\_import\_\_() | Dynamic low-level import | \_\_import\_\_('os') |
| staticmethod() | Define static method in class | @staticmethod decorator |
| classmethod() | Define class method in class | @classmethod decorator |
| property() | Create managed attributes with getter/setter | @property decorator |
| super() | Access parent class methods | super().\_\_init\_\_() |
| object() | Base class of all Python classes | isinstance(x,object) |

# **PART 2 — String Methods**

*Strings are immutable in Python. All string methods return NEW strings. Strings support indexing, slicing, and iteration.*

## **2.1  Case Methods**

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| upper() | All uppercase | 'hello'.upper() → 'HELLO' |
| lower() | All lowercase | 'HELLO'.lower() → 'hello' |
| title() | Title case (first letter of each word) | 'hello world'.title() → 'Hello World' |
| capitalize() | First char uppercase, rest lower | 'hELLO'.capitalize() → 'Hello' |
| swapcase() | Swap upper↔lower of each character | 'Hello'.swapcase() → 'hELLO' |
| casefold() | Aggressive lowercase for case-insensitive compare | 'ß'.casefold() → 'ss' |

## **2.2  Search & Check Methods**

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| find(sub,s,e) | Index of first occurrence or \-1 if not found | 'hello'.find('l') → 2 |
| rfind(sub) | Index of last occurrence or \-1 | 'hello'.rfind('l') → 3 |
| index(sub) | Like find() but raises ValueError if not found | 'hello'.index('e') → 1 |
| rindex(sub) | Like rfind() but raises ValueError | 'hello'.rindex('l') → 3 |
| count(sub) | Count non-overlapping occurrences | 'banana'.count('an') → 2 |
| startswith(p) | True if string starts with prefix (can be tuple) | 'abc'.startswith('ab') → True |
| endswith(s) | True if string ends with suffix (can be tuple) | 'abc'.endswith(('c','d')) → True |
| in operator | Membership test — O(n) for strings | 'lo' in 'hello' → True |

## **2.3  Split & Join Methods**

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| split(sep,n) | Split by sep into list; default splits on whitespace | 'a,b,c'.split(',') → \['a','b','c'\] |
| rsplit(sep,n) | Split from right; n limits splits | 'a.b.c'.rsplit('.',1) → \['a.b','c'\] |
| splitlines() | Split on line boundaries (\\n, \\r\\n, etc.) | 'a\\nb'.splitlines() → \['a','b'\] |
| partition(sep) | Split at first sep → (before,sep,after) tuple | 'a:b:c'.partition(':') → ('a',':','b:c') |
| rpartition(sep) | Split at last sep → (before,sep,after) tuple | 'a:b:c'.rpartition(':') → ('a:b',':','c') |
| join(iterable) | Join iterable elements with string as separator | ','.join(\['a','b'\]) → 'a,b' |

## **2.4  Strip & Replace Methods**

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| strip(chars) | Remove leading+trailing chars (default: whitespace) | '  hi  '.strip() → 'hi' |
| lstrip(chars) | Remove leading chars only | '000hi'.lstrip('0') → 'hi' |
| rstrip(chars) | Remove trailing chars only | 'hi\!\!\!'.rstrip('\!') → 'hi' |
| replace(old,new,n) | Replace all (or n) occurrences of old with new | 'aaa'.replace('a','b',2) → 'bba' |
| expandtabs(n) | Replace tabs with spaces (default: tabsize=8) | 'a\\tb'.expandtabs(4) → 'a   b' |
| translate(table) | Map chars using str.maketrans() table | see below |

\# translate example — remove punctuation:

table \= str.maketrans('', '', '\!?.,')  \# remove these chars

'Hello, World\!'.translate(table)  \# → 'Hello World'

\# ROT13 substitution:

table \= str.maketrans('abcdefghijklmnopqrstuvwxyz',

                       'nopqrstuvwxyzabcdefghijklm')

'hello'.translate(table)  \# → 'uryyb'

## **2.5  Alignment & Padding Methods**

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| center(w,c) | Center with fill character | 'hi'.center(8,'\*') → '\*\*\*hi\*\*\*' |
| ljust(w,c) | Left-justify with fill char | 'hi'.ljust(5,'-') → 'hi---' |
| rjust(w,c) | Right-justify with fill char | 'hi'.rjust(5,'0') → '000hi' |
| zfill(w) | Pad with zeros on left; handles sign | '42'.zfill(5) → '00042' |
| format\_map(m) | Like format() but uses a mapping object | '{x}'.format\_map({'x':1}) |

## **2.6  Encode / Decode**

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| encode(enc) | Encode string to bytes using given encoding | 'hello'.encode('utf-8') → b'hello' |
| decode(enc) | Decode bytes to string (bytes method) | b'hello'.decode('utf-8') → 'hello' |

## **2.7  Validation (is\_\_\_ ) Methods**

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| isalpha() | All chars are alphabetic | 'abc'.isalpha() → True |
| isdigit() | All chars are digits (0-9) | '123'.isdigit() → True |
| isalnum() | All chars are alphanumeric | 'abc123'.isalnum() → True |
| isnumeric() | Numeric chars (includes unicode fractions) | '½'.isnumeric() → True |
| isdecimal() | Only decimal chars (strict: 0-9) | '123'.isdecimal() → True |
| isspace() | Only whitespace characters | '  \\t'.isspace() → True |
| isupper() | All cased chars are uppercase | 'ABC'.isupper() → True |
| islower() | All cased chars are lowercase | 'abc'.islower() → True |
| istitle() | Title-case format check | 'Hello World'.istitle() → True |
| isidentifier() | Valid Python identifier | 'my\_var'.isidentifier() → True |
| isprintable() | All chars are printable (no control chars) | 'hello'.isprintable() → True |
| isascii() | All chars in ASCII range (0–127) | 'hello'.isascii() → True |

# **PART 3 — List Methods**

*Lists are ordered, mutable, dynamic arrays. They support O(1) append/pop from the end, but O(n) insert/delete at arbitrary positions.*

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| append(x) | Add x to end — O(1) amortized | lst.append(4) |
| extend(iter) | Add all items from iterable — O(k) | lst.extend(\[4,5,6\]) |
| insert(i,x) | Insert x before index i — O(n) | lst.insert(1,'a') |
| remove(x) | Remove first occurrence of x — O(n); ValueError if missing | lst.remove(3) |
| pop(i=-1) | Remove & return item at index i — O(1) end, O(n) other | lst.pop() or lst.pop(0) |
| clear() | Remove all items — O(n) | lst.clear() |
| index(x,s,e) | Index of first x in range \[s,e); ValueError if missing | lst.index(3,2) |
| count(x) | Count occurrences of x — O(n) | \[1,2,1\].count(1) → 2 |
| sort(key,rev) | Sort in-place using Timsort — O(n log n) | lst.sort(key=abs,reverse=True) |
| reverse() | Reverse in-place — O(n) | lst.reverse() |
| copy() | Shallow copy — O(n) | new \= lst.copy() |

### **append vs extend — Interview Trap**

lst \= \[1, 2, 3\]

lst.append(\[4, 5\])   \# → \[1,2,3,\[4,5\]\]  adds AS ONE item

lst.extend(\[4, 5\])   \# → \[1,2,3,4,5\]    unpacks iterable

### **pop(0) is O(n) — Use collections.deque Instead**

\# BAD: pop from front of list is O(n)

queue \= \[1,2,3\]; queue.pop(0)  \# shifts all elements

\# GOOD: use deque for O(1) popleft

from collections import deque

dq \= deque(\[1,2,3\]); dq.popleft()   \# O(1)

### **sort() vs sorted()**

lst.sort()          \# in-place, returns None, modifies lst

new \= sorted(lst)   \# returns NEW list, lst unchanged

\# Multi-key sort:

students.sort(key=lambda s: (s\['grade'\], s\['age'\]))

\# Sort descending by abs value:

nums.sort(key=abs, reverse=True)

### **List Slicing — Full Reference**

lst \= \[0,1,2,3,4,5,6,7,8,9\]

lst\[2:5\]       \# → \[2,3,4\]          start:stop

lst\[::2\]       \# → \[0,2,4,6,8\]      every 2nd

lst\[::-1\]      \# → \[9,8,...,0\]       reversed

lst\[-3:\]       \# → \[7,8,9\]           last 3

lst\[1:8:3\]     \# → \[1,4,7\]           start:stop:step

lst\[:\] \= \[\]    \# clear list in-place (keeps same object)

# **PART 4 — Dictionary Methods**

*Dicts are hash maps. Average O(1) get/set/delete. Ordered by insertion (Python 3.7+). Keys must be hashable.*

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| get(k,default) | Return value for k or default (no KeyError) | d.get('x',0) |
| setdefault(k,v) | Return d\[k\] if exists, else set d\[k\]=v and return v | d.setdefault('x',\[\]) |
| update(other) | Merge another dict or key-value iterable | d.update({'a':1}) |
| keys() | View of all keys — updates live with dict | list(d.keys()) |
| values() | View of all values — updates live with dict | list(d.values()) |
| items() | View of (key,value) tuples — live view | for k,v in d.items() |
| pop(k,default) | Remove and return d\[k\]; optional default avoids KeyError | d.pop('key',None) |
| popitem() | Remove and return last inserted (key,value) pair | k,v \= d.popitem() |
| clear() | Remove all items | d.clear() |
| copy() | Shallow copy of dict | d2 \= d.copy() |
| fromkeys(keys,v) | Class method: create dict from keys with same value | dict.fromkeys('abc',0) |
| | operator | Merge dicts (Python 3.9+) — creates new dict | d3 \= d1 | d2 |
| |= operator | Update dict in-place (Python 3.9+) | d1 |= d2 |

### **setdefault() — Most Underused Dict Method**

*💡 Interview pattern: grouping / building a dict of lists without an explicit existence check.*

\# Group words by first letter:

groups \= {}

for w in \['apple','ant','bee','bad'\]:

    groups.setdefault(w\[0\], \[\]).append(w)

\# {'a':\['apple','ant'\], 'b':\['bee','bad'\]}

\# Same with defaultdict (often cleaner):

from collections import defaultdict

groups \= defaultdict(list)

for w in words: groups\[w\[0\]\].append(w)

### **Dict Comprehensions**

{k:v for k,v in d.items() if v \> 0}    \# filter

{v:k for k,v in d.items()}              \# invert dict

{x:x\*\*2 for x in range(5)}             \# {0:0,1:1,2:4,3:9,4:16}

\# Merge two dicts (Python 3.9+):

merged \= {\*\*d1, \*\*d2}   \# d2 overrides d1 on conflicts

### **Nested Dict Access Patterns**

data \= {'user':{'name':'Alice','age':30}}

\# Safe nested access:

data.get('user',{}).get('name','unknown')  \# → 'Alice'

\# Using walrus operator (Python 3.8+):

if user := data.get('user'):

    print(user.get('name'))

# **PART 5 — Set Methods**

*Sets are unordered collections of unique hashable items. O(1) average add/remove/membership. Powered by a hash table.*

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| add(x) | Add single element — O(1) | s.add(5) |
| remove(x) | Remove x; raises KeyError if missing | s.remove(3) |
| discard(x) | Remove x; no error if missing — safer | s.discard(99) |
| pop() | Remove and return an arbitrary element | x \= s.pop() |
| clear() | Remove all elements | s.clear() |
| copy() | Shallow copy of set | s2 \= s.copy() |
| union(t) / | | All elements in either set | s | t |
| intersection(t) / & | Elements in both sets | s & t |
| difference(t) / \- | Elements in s but not in t | s \- t |
| symmetric\_difference(t)/^ | Elements in exactly one set | s ^ t |
| issubset(t) / \<= | True if all of s is in t | s \<= t |
| issuperset(t) / \>= | True if s contains all of t | s \>= t |
| isdisjoint(t) | True if s and t share no elements | s.isdisjoint(t) |
| update(t) / |= | Add all elements from t to s in-place | s |= t |
| intersection\_update(t)/&= | Keep only elements found in both | s &= t |

### **Set vs List for Membership Testing**

*💡 O(1) for set vs O(n) for list — critical for performance in interview problems.*

\# O(n) per lookup:

seen \= \[\]; 5 in seen   \# O(n)

\# O(1) per lookup:

seen \= set(); 5 in seen   \# O(1)  ← always prefer this

\# Common pattern — find duplicates:

def has\_duplicate(lst):

    return len(lst) \!= len(set(lst))  \# O(n) time/space

# **PART 6 — Essential Built-in Modules**

## **6.1  collections**

The collections module provides specialized container datatypes beyond built-in list/dict/set/tuple.

### **defaultdict**

A dict subclass that never raises KeyError. The factory function provides the default value for missing keys.

from collections import defaultdict

\# Word frequency counter:

freq \= defaultdict(int)

for w in words: freq\[w\] \+= 1

\# Graph adjacency list:

graph \= defaultdict(list)

for u,v in edges: graph\[u\].append(v)

\# Nested defaultdict:

matrix \= defaultdict(lambda: defaultdict(int))

matrix\['a'\]\['b'\] \+= 1

### **Counter**

A subclass of dict designed for counting hashable objects. most\_common(n), arithmetic operations, and subtraction included.

*💡 Interview go-to: anagram check, frequency problems, top-k frequent elements.*

from collections import Counter

c \= Counter("mississippi")

\# Counter({'s':4,'i':4,'p':2,'m':1})

c.most\_common(2)        \# \[('s',4),('i',4)\]

c.total()               \# 11  (Python 3.10+)

sorted(c.elements())    \# expands back to sorted list

\# Arithmetic:

c1 \= Counter(a=3, b=2); c2 \= Counter(a=1, b=4)

c1 \+ c2   \# Counter(a=4, b=6)

c1 \- c2   \# Counter(a=2)  (negative counts dropped)

c1 & c2   \# Counter(a=1,b=2) (min of each)

c1 | c2   \# Counter(a=3,b=4) (max of each)

\# Anagram check:

Counter('listen') \== Counter('silent')  \# → True

### **deque (Double-Ended Queue)**

O(1) append and pop from BOTH ends. The go-to data structure for BFS, sliding windows, and implementing queues efficiently.

from collections import deque

dq \= deque(\[1,2,3\])

dq.appendleft(0)   \# \[0,1,2,3\]   O(1)

dq.append(4)       \# \[0,1,2,3,4\] O(1)

dq.popleft()       \# → 0         O(1)

dq.pop()           \# → 4         O(1)

dq.rotate(1)       \# \[3,1,2\]     rotate right by 1

dq.rotate(-1)      \# \[1,2,3\]     rotate left by 1

\# Bounded deque — auto-drops old items:

recent \= deque(maxlen=3)  \# sliding window

for x in range(6): recent.append(x)

\# deque(\[3,4,5\], maxlen=3)

\# BFS template:

from collections import deque

def bfs(graph, start):

    visited, queue \= set(), deque(\[start\])

    while queue:

        node \= queue.popleft()

        if node not in visited:

            visited.add(node)

            queue.extend(graph\[node\])

### **OrderedDict**

A dict subclass that remembers insertion order. In Python 3.7+ regular dicts also maintain order, so OrderedDict is mainly used for its move\_to\_end() and popitem() behavior.

from collections import OrderedDict

\# LRU Cache implementation pattern:

class LRUCache:

    def \_\_init\_\_(self, cap):

        self.cache \= OrderedDict()

        self.cap \= cap

    def get(self, key):

        if key not in self.cache: return \-1

        self.cache.move\_to\_end(key)   \# mark as recently used

        return self.cache\[key\]

    def put(self, key, val):

        if key in self.cache:

            self.cache.move\_to\_end(key)

        self.cache\[key\] \= val

        if len(self.cache) \> self.cap:

            self.cache.popitem(last=False)  \# remove LRU

### **namedtuple**

Creates immutable tuple subclasses with named fields. Better than plain tuples for readability, and better than dicts for immutable records.

from collections import namedtuple

Point \= namedtuple('Point', \['x','y'\])

p \= Point(3, 4\)

p.x, p.y   \# 3, 4

p\[0\], p\[1\] \# 3, 4  (still works as tuple)

p.\_asdict()  \# OrderedDict(\[('x',3),('y',4)\])

p.\_replace(x=10)  \# Point(x=10,y=4)  new object

### **ChainMap**

Groups multiple dicts into a single view. Lookups search through the maps in order. Original dicts are not merged.

from collections import ChainMap

defaults \= {'color':'red','size':10}

user\_prefs \= {'color':'blue'}

config \= ChainMap(user\_prefs, defaults)

config\['color'\]  \# → 'blue'  (user\_prefs wins)

config\['size'\]   \# → 10     (falls back to defaults)

## **6.2  itertools**

The itertools module provides memory-efficient iterators for combinatorics and iterator algebra.

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| chain(\*iters) | Concatenate multiple iterables lazily | chain(\[1,2\],\[3,4\]) → 1,2,3,4 |
| chain.from\_iterable | Flatten one level of nesting | chain.from\_iterable(\[\[1,2\],\[3\]\]) |
| combinations(it,r) | r-length combos, no repeats, sorted order | C(4,2)=6 combos |
| combinations\_with\_replacement | r-length combos, WITH repeats allowed | ('a',3) → aaa,aab,... |
| permutations(it,r) | r-length permutations; default r=length | P(3,2)=6 perms |
| product(\*iters,repeat) | Cartesian product of iterables | product('AB','12') → A1,A2,B1,B2 |
| accumulate(it,func) | Running total (or other accumulation function) | accumulate(\[1,2,3\]) → 1,3,6 |
| groupby(it,key) | Groups consecutive elements by key func | group sorted data |
| islice(it,start,stop) | Slice an iterator lazily (no negative indexing) | islice(range(100),5,15) |
| compress(data,selectors) | Filter by boolean selector sequence | compress('ABCD',\[1,0,1,1\])→A,C,D |
| dropwhile(pred,it) | Drop elements while predicate is True, then yield all | dropwhile(lambda x:x\<5,\[1,4,6,4\])→6,4 |
| takewhile(pred,it) | Yield elements while predicate is True, then stop | takewhile(lambda x:x\<5,\[1,3,6,2\])→1,3 |
| cycle(it) | Cycle through iterable indefinitely | cycle('AB') → A,B,A,B,... |
| repeat(x,n) | Repeat x n times (or forever if n omitted) | repeat(0,3) → 0,0,0 |
| starmap(func,it) | Apply func to each tuple in iterable | starmap(pow,\[(2,3),(3,2)\])→8,9 |
| zip\_longest(\*its) | Zip filling short iterables with fillvalue | zip\_longest(\[1,2\],\[3\],fillvalue=0) |
| count(start,step) | Infinite counter | count(0,2) → 0,2,4,6,... |
| pairwise(it) | Consecutive pairs (Python 3.10+) | pairwise('ABCD')→AB,BC,CD |

from itertools import \*

\# Flatten a 2D list:

flat \= list(chain.from\_iterable(\[\[1,2\],\[3,4\],\[5\]\]))

\# → \[1,2,3,4,5\]

\# All pairs from a list:

list(combinations(\[1,2,3,4\], 2))

\# → \[(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)\]

\# Running prefix sum:

list(accumulate(\[1,2,3,4,5\]))   \# → \[1,3,6,10,15\]

list(accumulate(\[1,2,3,4,5\], lambda a,b: a\*b))  \# running product

\# Group anagrams:

words \= \['eat','tea','tan','ate','nat','bat'\]

from itertools import groupby

for k, g in groupby(sorted(words, key=sorted), key=sorted):

    print(list(g))

## **6.3  functools**

Higher-order functions that work on or return other functions.

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| reduce(func,it,init) | Left-fold: apply func cumulatively | reduce(op.add,\[1,2,3\]) → 6 |
| partial(func,\*args) | Create new function with some args pre-filled | partial(pow,2) → powers of 2 |
| lru\_cache(maxsize) | @decorator: memoize function calls | @lru\_cache(maxsize=None) |
| cache | @decorator: unbounded lru\_cache (Python 3.9+) | @cache |
| cached\_property | @decorator: compute once, cache on instance | @cached\_property |
| wraps(func) | Preserve metadata when writing decorators | @wraps(func) |
| total\_ordering | Fill in comparison methods from \_\_eq\_\_+one more | @total\_ordering |
| cmp\_to\_key(func) | Convert old-style cmp function to key function | sorted(lst,key=cmp\_to\_key(cmp)) |
| singledispatch | Function overloading based on first arg type | @singledispatch |

from functools import lru\_cache, reduce, partial

\# Memoized Fibonacci — O(n) instead of O(2^n):

@lru\_cache(maxsize=None)

def fib(n):

    if n \< 2: return n

    return fib(n-1) \+ fib(n-2)

\# partial — create specialized functions:

double \= partial(lambda x,y: x\*y, 2\)

double(5)   \# → 10

\# Flatten arbitrarily nested list using reduce:

from functools import reduce

import operator

reduce(operator.add, \[\[1,2\],\[3,4\],\[5\]\])  \# → \[1,2,3,4,5\]

## **6.4  heapq**

Implements a min-heap (priority queue) on top of a Python list. All operations maintain the heap invariant.

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| heappush(h,x) | Push x onto heap — O(log n) | heappush(h, (priority, item)) |
| heappop(h) | Pop and return smallest item — O(log n) | val \= heappop(h) |
| heappushpop(h,x) | Push then pop — more efficient than two calls | heappushpop(h, x) |
| heapreplace(h,x) | Pop smallest then push x — O(log n) | heapreplace(h, x) |
| heapify(lst) | Transform list into heap in-place — O(n) | heapify(lst) |
| nlargest(k,it,key) | k largest items — O(n log k) | nlargest(3,nums) |
| nsmallest(k,it,key) | k smallest items — O(n log k) | nsmallest(3,nums) |

*💡 heapq is a MIN-heap. For a MAX-heap, negate values: push \-x, pop and negate result.*

import heapq

\# Top-K largest elements:

nums \= \[3,1,4,1,5,9,2,6\]

heapq.nlargest(3, nums)   \# → \[9,6,5\]  O(n log k)

\# Min-heap priority queue:

h \= \[\]

heapq.heappush(h, (1, 'low priority'))

heapq.heappush(h, (0, 'urgent'))

pri, task \= heapq.heappop(h)  \# → (0,'urgent')

\# Max-heap workaround (negate values):

max\_heap \= \[\]

for n in \[3,1,4,1,5\]: heapq.heappush(max\_heap, \-n)

max\_val \= \-heapq.heappop(max\_heap)  \# → 5

\# Merge k sorted lists (classic interview problem):

import heapq

def merge\_k\_sorted(lists):

    h \= \[(lst\[0\],i,0) for i,lst in enumerate(lists) if lst\]

    heapq.heapify(h)

    result \= \[\]

    while h:

        val, li, idx \= heapq.heappop(h)

        result.append(val)

        if idx+1 \< len(lists\[li\]):

            heapq.heappush(h, (lists\[li\]\[idx+1\], li, idx+1))

    return result

## **6.5  bisect**

Binary search on a SORTED list. All operations are O(log n).

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| bisect\_left(a,x) | Index to insert x keeping a sorted; leftmost pos if x exists | bisect\_left(\[1,3,5\],3) → 1 |
| bisect\_right(a,x) | Index to insert x keeping a sorted; rightmost pos if x exists | bisect\_right(\[1,3,5\],3) → 2 |
| insort\_left(a,x) | Insert x into sorted a maintaining sort order (leftmost) | insort\_left(a,x) |
| insort\_right(a,x) | Insert x into sorted a maintaining sort order (rightmost) | insort\_right(a,x) |

import bisect

\# Search in sorted array:

a \= \[1,3,3,5,7,9\]

bisect.bisect\_left(a, 3\)    \# → 1 (first 3\)

bisect.bisect\_right(a, 3\)   \# → 3 (after last 3\)

\# Count occurrences in sorted array O(log n):

def count(a, x):

    return bisect.bisect\_right(a,x) \- bisect.bisect\_left(a,x)

\# Grade lookup:

breakpoints \= \[60,70,80,90\]

grades \= 'FDCBA'

def grade(score):

    return grades\[bisect.bisect(breakpoints, score)\]

## **6.6  math**

Mathematical functions operating on real numbers (floats). For complex numbers use cmath.

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| math.floor(x) | Largest integer ≤ x | math.floor(3.7) → 3 |
| math.ceil(x) | Smallest integer ≥ x | math.ceil(3.2) → 4 |
| math.sqrt(x) | Square root — returns float | math.sqrt(16) → 4.0 |
| math.isqrt(x) | Integer square root (floor) — no float error | math.isqrt(17) → 4 |
| math.factorial(n) | n\! — exact integer result | math.factorial(10) → 3628800 |
| math.gcd(\*args) | Greatest common divisor | math.gcd(12,8) → 4 |
| math.lcm(\*args) | Least common multiple (Python 3.9+) | math.lcm(4,6) → 12 |
| math.log(x,base) | Logarithm; base defaults to e | math.log(100,10) → 2.0 |
| math.log2(x) | Base-2 logarithm (more precise than log(x,2)) | math.log2(8) → 3.0 |
| math.log10(x) | Base-10 logarithm | math.log10(1000) → 3.0 |
| math.comb(n,k) | Binomial coefficient C(n,k) — exact integer | math.comb(5,2) → 10 |
| math.perm(n,k) | Permutations P(n,k) | math.perm(5,2) → 20 |
| math.pow(x,y) | Float power — use \*\* or built-in pow() usually | math.pow(2,10) → 1024.0 |
| math.fabs(x) | Absolute value as float | math.fabs(-3) → 3.0 |
| math.inf / math.nan | Float infinity and NaN constants | math.inf \> 10\*\*308 |
| math.pi / math.e / math.tau | Mathematical constants | math.pi ≈ 3.14159... |
| math.trunc(x) | Truncate to integer toward zero | math.trunc(-3.9) → \-3 |
| math.copysign(x,y) | Magnitude of x with sign of y | math.copysign(3,-1)→-3.0 |
| math.hypot(\*coords) | Euclidean distance / hypotenuse | math.hypot(3,4) → 5.0 |
| math.degrees(r) | Radians to degrees | math.degrees(math.pi) → 180.0 |
| math.radians(d) | Degrees to radians | math.radians(180) → π |

## **6.7  os**

Operating system interface — file system operations, environment variables, process management.

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| os.getcwd() | Current working directory path | os.getcwd() |
| os.chdir(path) | Change working directory | os.chdir('/tmp') |
| os.listdir(path) | List directory contents | os.listdir('.') |
| os.path.join(\*paths) | Join path components portably | os.path.join('a','b','c.txt') |
| os.path.exists(p) | True if path exists | os.path.exists('file.txt') |
| os.path.isfile(p) | True if path is a regular file | os.path.isfile(p) |
| os.path.isdir(p) | True if path is a directory | os.path.isdir(p) |
| os.path.basename(p) | Last component of path | os.path.basename('/a/b.txt')→'b.txt' |
| os.path.dirname(p) | Directory part of path | os.path.dirname('/a/b.txt')→'/a' |
| os.path.splitext(p) | Split name and extension | os.path.splitext('f.txt')→('f','.txt') |
| os.path.getsize(p) | File size in bytes | os.path.getsize('f.txt') |
| os.makedirs(p,exist\_ok) | Create directory tree | os.makedirs('a/b',exist\_ok=True) |
| os.remove(p) | Delete a file | os.remove('tmp.txt') |
| os.rename(src,dst) | Rename/move a file | os.rename('old','new') |
| os.environ | Dict-like environment variables | os.environ.get('PATH') |
| os.walk(top) | Yields (dirpath, dirnames, filenames) recursively | for root,dirs,files in os.walk('.') |
| os.getpid() | Current process ID | os.getpid() |
| os.cpu\_count() | Number of CPUs available | os.cpu\_count() |

## **6.8  sys**

Python runtime environment access.

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| sys.argv | Command-line arguments list (argv\[0\] is script name) | sys.argv\[1:\] |
| sys.stdin/stdout/stderr | Standard I/O streams | sys.stdout.write('hi') |
| sys.exit(code) | Exit interpreter; 0=success, nonzero=error | sys.exit(1) |
| sys.path | Module search path list (modify to add dirs) | sys.path.append('.') |
| sys.version | Python version string | sys.version |
| sys.maxsize | Max value of int (platform-dependent) | sys.maxsize → 9223372036854775807 |
| sys.getrecursionlimit() | Current max recursion depth (default 1000\) | sys.getrecursionlimit() |
| sys.setrecursionlimit(n) | Change max recursion depth — CAREFUL | sys.setrecursionlimit(10\*\*6) |
| sys.getsizeof(obj) | Memory size of object in bytes | sys.getsizeof(\[1,2,3\]) |
| sys.intern(s) | Intern a string for fast equality comparisons | sys.intern('frequent\_key') |

## **6.9  re (Regular Expressions)**

Pattern matching using regular expressions. Compile patterns for reuse with re.compile().

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| re.match(p,s) | Match pattern at START of string only | re.match(r'\\d+','123abc') |
| re.search(p,s) | Search ANYWHERE in string — returns first match | re.search(r'\\d+','abc123') |
| re.findall(p,s) | All non-overlapping matches as list | re.findall(r'\\d+','a1b22c3')→\['1','22','3'\] |
| re.finditer(p,s) | Iterator of match objects — lazy | for m in re.finditer(p,s) |
| re.sub(p,r,s,n) | Replace n matches of p with r in s | re.sub(r'\\s+',' ','a  b c')→'a b c' |
| re.subn(p,r,s) | Like sub() but returns (new\_string, count) | re.subn(r'a','x','banana') |
| re.split(p,s,n) | Split s by pattern p | re.split(r'\[,;\]','a,b;c')→\['a','b','c'\] |
| re.fullmatch(p,s) | Match ENTIRE string against pattern | re.fullmatch(r'\\d+','123') |
| re.compile(p,flags) | Compile pattern to reusable regex object | pat=re.compile(r'\\d+') |
| re.escape(s) | Escape special regex chars in s | re.escape('a.b') → 'a\\.b' |
| re.IGNORECASE / re.I | Case-insensitive flag | re.search(p,s,re.I) |
| re.MULTILINE / re.M | ^ and $ match line boundaries | re.findall(r'^\\w+',s,re.M) |
| re.DOTALL / re.S | . matches \\n too | re.search(r'.+',s,re.S) |

import re

\# Extract all emails from text:

emails \= re.findall(r'\[\\w.+-\]+@\[\\w-\]+\\.\[a-zA-Z\]{2,}', text)

\# Named groups:

m \= re.search(r'(?P\<year\>\\d{4})-(?P\<month\>\\d{2})', '2024-03')

m.group('year')   \# → '2024'

\# Non-greedy match (? makes \* or \+ lazy):

re.findall(r'\<.\*?\>', '\<a\>text\</a\>')  \# → \['\<a\>','\</a\>'\]

re.findall(r'\<.\*\>',  '\<a\>text\</a\>')  \# → \['\<a\>text\</a\>'\]

## **6.10  datetime**

Date and time handling. Key classes: datetime, date, time, timedelta, timezone.

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| datetime.now(tz) | Current local datetime (with optional timezone) | datetime.now() |
| datetime.utcnow() | Current UTC datetime (naive) | datetime.utcnow() |
| datetime.today() | Current local datetime (same as now() without tz) | datetime.today() |
| datetime.fromisoformat(s) | Parse ISO 8601 string | datetime.fromisoformat('2024-01-15') |
| datetime.strptime(s,fmt) | Parse string with custom format | strptime('2024-01-15','%Y-%m-%d') |
| dt.strftime(fmt) | Format datetime to string | dt.strftime('%d/%m/%Y') |
| dt.timestamp() | Unix timestamp (seconds since epoch) | dt.timestamp() |
| datetime.fromtimestamp(t) | Datetime from Unix timestamp | datetime.fromtimestamp(ts) |
| timedelta(days,secs,etc) | Duration arithmetic | timedelta(days=7) |
| date.today() | Current local date | date.today() |
| dt.date() / dt.time() | Extract date or time component | dt.date() |
| dt.replace(\*\*kw) | Return new datetime with specified fields changed | dt.replace(year=2025) |
| dt.weekday() | Day of week 0=Mon ... 6=Sun | datetime.now().weekday() |

## **6.11  json**

Serialize Python objects to JSON strings and back.

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| json.dumps(obj,\*\*kw) | Python object → JSON string | json.dumps({'a':1}) → '{"a":1}' |
| json.loads(s) | JSON string → Python object | json.loads('{"a":1}') → {'a':1} |
| json.dump(obj,f) | Serialize directly to file object | json.dump(obj, open('f.json','w')) |
| json.load(f) | Deserialize from file object | json.load(open('f.json')) |

import json

\# Pretty print:

print(json.dumps(data, indent=2, sort\_keys=True))

\# Custom serialization:

json.dumps(data, default=str)  \# convert unsupported types to str

\# Sort and minimize:

json.dumps(data, separators=(',',':'))  \# compact

## **6.12  random**

Pseudo-random number generation. NOT cryptographically secure — use secrets module for security-sensitive code.

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| random.random() | Random float in \[0.0, 1.0) | random.random() |
| random.randint(a,b) | Random integer in \[a,b\] inclusive | random.randint(1,6) |
| random.randrange(s,e,step) | Random element from range(s,e,step) | random.randrange(0,100,2) |
| random.choice(seq) | Random element from non-empty sequence | random.choice(\[1,2,3\]) |
| random.choices(pop,k,weights) | k random elements WITH replacement, optional weights | random.choices('abc',k=5) |
| random.sample(pop,k) | k random elements WITHOUT replacement | random.sample(range(100),10) |
| random.shuffle(lst) | Shuffle list in-place | random.shuffle(lst) |
| random.uniform(a,b) | Random float in \[a,b\] | random.uniform(1.0,5.0) |
| random.gauss(mu,sigma) | Gaussian distribution sample | random.gauss(0,1) |
| random.seed(n) | Set seed for reproducibility | random.seed(42) |

## **6.13  pathlib (Modern File System)**

Object-oriented file system paths. Preferred over os.path in modern Python (3.4+).

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| Path('file.txt') | Create a Path object | p \= Path('/home/user/file.txt') |
| p / 'subdir' | Join paths with / operator | p \= base / 'data' / 'file.txt' |
| p.read\_text() | Read file contents as string | p.read\_text(encoding='utf-8') |
| p.write\_text(s) | Write string to file | p.write\_text('hello') |
| p.read\_bytes() | Read file contents as bytes | p.read\_bytes() |
| p.exists() | True if path exists | p.exists() |
| p.is\_file() | True if regular file | p.is\_file() |
| p.is\_dir() | True if directory | p.is\_dir() |
| p.stem / p.suffix | Filename without extension / extension | Path('f.txt').stem → 'f' |
| p.parent | Parent directory as Path | Path('/a/b/c').parent → Path('/a/b') |
| p.name | Final path component | Path('/a/b.txt').name → 'b.txt' |
| p.glob('\*.py') | Find files matching glob pattern | list(p.glob('\*\*/\*.py')) |
| p.mkdir(parents=True) | Create directory (and parents) | p.mkdir(parents=True,exist\_ok=True) |
| p.unlink() | Delete file | p.unlink(missing\_ok=True) |
| p.rename(target) | Rename/move path | p.rename('new\_name.txt') |
| p.stat().st\_size | File stats (size, mtime, etc.) | p.stat().st\_mtime |

## **6.14  typing**

Type hints for Python code. Used for documentation and static analysis tools like mypy and pyright. No runtime performance impact.

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| List\[T\] | List of items of type T | def f(lst: List\[int\]) \-\> None |
| Dict\[K,V\] | Dict with key type K, value type V | Dict\[str, int\] |
| Tuple\[T,...\] | Tuple; ... means variable-length same type | Tuple\[int,str,float\] |
| Set\[T\] | Set of items of type T | Set\[str\] |
| Optional\[T\] | T or None — equivalent to Union\[T,None\] | Optional\[str\] |
| Union\[A,B\] | A or B | Union\[int,str\] |
| Any | Disables type checking for this value | x: Any |
| Callable\[\[A,B\],R\] | Callable accepting args A,B and returning R | Callable\[\[int\],str\] |
| Generator\[Y,S,R\] | Generator with yield/send/return types | Generator\[int,None,None\] |
| TypeVar('T') | Generic type variable | T \= TypeVar('T') |
| Protocol | Structural subtyping (duck typing formalized) | class Sized(Protocol) |
| dataclass (decorator) | Auto-generate \_\_init\_\_,\_\_repr\_\_,\_\_eq\_\_ etc. | @dataclass |
| ClassVar\[T\] | Class variable (not instance variable) | ClassVar\[int\] |
| Final\[T\] | Value should not be reassigned | MAX: Final\[int\] \= 100 |

*💡 In Python 3.10+ you can write X | Y instead of Union\[X,Y\], and list\[int\] instead of List\[int\] (lowercase built-ins).*

from typing import Optional, Union, List, Dict, Callable

def greet(name: str) \-\> str:

    return f'Hello, {name}'

def find(lst: List\[int\], x: int) \-\> Optional\[int\]:

    try: return lst.index(x)

    except ValueError: return None

\# Python 3.10+ shorthand:

def func(x: int | str | None) \-\> list\[int\]: ...

# **PART 7 — Interview Questions: Brute Force vs Optimized**

*The following covers the most commonly asked Python interview problems. Each problem shows a brute-force solution with its complexity, followed by an optimized solution.*

## **7.1  Nested Lists**

### **Problem: Flatten Arbitrarily Nested List**

Given a nested list of any depth, return a flat list of all elements.

**🐢 Brute Force — Recursive  |  O(n) time, O(d) space (d \= depth)**

def flatten\_brute(lst):

    result \= \[\]

    for item in lst:

        if isinstance(item, list):

            result.extend(flatten\_brute(item))  \# recursive call

        else:

            result.append(item)

    return result

flatten\_brute(\[1,\[2,\[3,4\]\],\[5,6\]\])  \# → \[1,2,3,4,5,6\]

**🚀 Optimized — Iterative Stack  |  O(n) time, O(n) space, no recursion limit**

def flatten(lst):

    result, stack \= \[\], lst\[::-1\]  \# reverse so we pop from front

    while stack:

        item \= stack.pop()

        if isinstance(item, list):

            stack.extend(item\[::-1\])  \# push sub-items reversed

        else:

            result.append(item)

    return result

\# Bonus — generator (memory efficient for huge lists):

def flatten\_gen(lst):

    for item in lst:

        if isinstance(item, list): yield from flatten\_gen(item)

        else: yield item

### **Problem: Deep Sum of Nested List of Integers**

Sum all integers at any depth level, where deeper elements have higher weight proportional to depth.

**🐢 Brute Force — Recursive**

def depth\_sum\_brute(lst, depth=1):

    total \= 0

    for item in lst:

        if isinstance(item, list):

            total \+= depth\_sum\_brute(item, depth+1)

        else:

            total \+= item \* depth

    return total

depth\_sum\_brute(\[\[1,1\],2,\[1,1\]\])  \# → 10

**🚀 Optimized — BFS (level by level)**

from collections import deque

def depth\_sum\_bfs(lst):

    total, depth \= 0, 1

    queue \= deque(lst)

    while queue:

        for \_ in range(len(queue)):  \# process one level at a time

            item \= queue.popleft()

            if isinstance(item, list):

                queue.extend(item)

            else:

                total \+= item \* depth

        depth \+= 1

    return total

### **Problem: Find Maximum Depth of Nested List**

**🐢 Brute Force — Recursive**

def max\_depth\_brute(lst):

    if not isinstance(lst, list): return 0

    if not lst: return 1

    return 1 \+ max(max\_depth\_brute(item) for item in lst)

**🚀 Optimized — Iterative DFS with stack**

def max\_depth(lst):

    if not isinstance(lst, list): return 0

    max\_d \= 1

    stack \= \[(lst, 1)\]

    while stack:

        node, d \= stack.pop()

        if isinstance(node, list):

            max\_d \= max(max\_d, d)

            for item in node:

                stack.append((item, d+1))

    return max\_d

## **7.2  Nested Dictionaries**

### **Problem: Flatten Nested Dict (dot notation keys)**

Convert {'a':{'b':{'c':1},'d':2}} to {'a.b.c':1, 'a.d':2}.

**🐢 Brute Force — Recursive**

def flatten\_dict\_brute(d, parent='', sep='.'):

    result \= {}

    for k, v in d.items():

        new\_key \= f'{parent}{sep}{k}' if parent else k

        if isinstance(v, dict):

            result.update(flatten\_dict\_brute(v, new\_key, sep))

        else:

            result\[new\_key\] \= v

    return result

**🚀 Optimized — Iterative Stack (avoids recursion limit on deep dicts)**

def flatten\_dict(d, sep='.'):

    result \= {}

    stack \= \[('', d)\]

    while stack:

        prefix, curr \= stack.pop()

        for k, v in curr.items():

            key \= f'{prefix}{sep}{k}' if prefix else k

            if isinstance(v, dict):

                stack.append((key, v))

            else:

                result\[key\] \= v

    return result

### **Problem: Deep Get / Safe Access Nested Dict**

Safely access nested\['a'\]\['b'\]\['c'\] without chained .get() calls.

**🐢 Brute Force — Chained get()**

\# Works but ugly and breaks with deep paths:

val \= d.get('a',{}).get('b',{}).get('c', None)

**🚀 Optimized — reduce or loop**

from functools import reduce

def deep\_get(d, keys, default=None):

    try:

        return reduce(lambda obj, k: obj\[k\], keys, d)

    except (KeyError, TypeError):

        return default

deep\_get({'a':{'b':{'c':42}}}, \['a','b','c'\])  \# → 42

deep\_get({'a':1}, \['a','b','c'\], default=0)    \# → 0

### **Problem: Deep Merge Two Dicts (recursive)**

**🐢 Brute Force — dict.update (SHALLOW only)**

\# BUG: nested dicts get replaced not merged

d1 \= {'a':{'x':1}}; d2 \= {'a':{'y':2}}

d1.update(d2)  \# → {'a':{'y':2}}  WRONG\! 'x' is lost

**🚀 Optimized — Recursive deep merge**

def deep\_merge(d1, d2):

    result \= dict(d1)   \# shallow copy

    for k, v in d2.items():

        if k in result and isinstance(result\[k\], dict) and isinstance(v, dict):

            result\[k\] \= deep\_merge(result\[k\], v)  \# recurse on dicts

        else:

            result\[k\] \= v   \# d2 overrides d1

    return result

d1 \= {'a':{'x':1,'y':2}, 'b':3}

d2 \= {'a':{'y':99,'z':4}, 'c':5}

deep\_merge(d1,d2)  \# {'a':{'x':1,'y':99,'z':4},'b':3,'c':5}

### **Problem: Count Frequency in Nested Structure**

Count occurrences of a value anywhere in an arbitrarily nested dict/list structure.

**🚀 Optimized — Generic DFS using isinstance checks**

def count\_val(obj, target):

    count \= 0

    stack \= \[obj\]

    while stack:

        curr \= stack.pop()

        if curr \== target:

            count \+= 1

        elif isinstance(curr, dict):

            stack.extend(curr.values())

        elif isinstance(curr, (list,tuple)):

            stack.extend(curr)

    return count

## **7.3  Classic String Problems**

### **Problem: Longest Substring Without Repeating Characters**

Given string s, find the length of the longest substring without repeating characters.

**🐢 Brute Force  |  O(n³) time, O(min(n,m)) space**

def length\_brute(s):

    n, max\_len \= len(s), 0

    for i in range(n):

        for j in range(i+1, n+1):

            if len(set(s\[i:j\])) \== j-i:  \# all unique?

                max\_len \= max(max\_len, j-i)

    return max\_len

**🚀 Optimized — Sliding Window with dict  |  O(n) time, O(min(n,m)) space**

def length\_optimal(s):

    seen \= {}   \# char → last seen index

    left \= max\_len \= 0

    for right, ch in enumerate(s):

        if ch in seen and seen\[ch\] \>= left:

            left \= seen\[ch\] \+ 1   \# shrink window

        seen\[ch\] \= right

        max\_len \= max(max\_len, right \- left \+ 1\)

    return max\_len

length\_optimal('abcabcbb')  \# → 3 (abc)

### **Problem: Group Anagrams**

Given a list of strings, group the anagrams together.

**🐢 Brute Force  |  O(n² · k) time**

def group\_anagrams\_brute(words):

    groups, used \= \[\], set()

    for i, w in enumerate(words):

        if i in used: continue

        group \= \[w\]

        for j, w2 in enumerate(words\[i+1:\], i+1):

            if j not in used and sorted(w) \== sorted(w2):

                group.append(w2); used.add(j)

        groups.append(group)

    return groups

**🚀 Optimized — Hash by sorted key  |  O(n·k log k) time, O(n·k) space**

from collections import defaultdict

def group\_anagrams(words):

    groups \= defaultdict(list)

    for w in words:

        key \= tuple(sorted(w))   \# canonical form

        groups\[key\].append(w)

    return list(groups.values())

\# Even faster key using character counts (O(k) hashing):

def group\_anagrams\_v2(words):

    groups \= defaultdict(list)

    for w in words:

        count \= \[0\]\*26

        for c in w: count\[ord(c)-ord('a')\] \+= 1

        groups\[tuple(count)\].append(w)   \# O(26) \= O(1) key

    return list(groups.values())

### **Problem: Valid Parentheses / Brackets**

**🚀 Stack Solution  |  O(n) time, O(n) space**

def is\_valid(s):

    stack \= \[\]

    close\_to\_open \= {')':'(', '\]':'\[', '}':'{'}

    for ch in s:

        if ch in close\_to\_open:

            if not stack or stack\[-1\] \!= close\_to\_open\[ch\]:

                return False

            stack.pop()

        else:

            stack.append(ch)  \# opening bracket

    return len(stack) \== 0

is\_valid('({\[\]})')  \# → True

is\_valid('(\[)\]')    \# → False

## **7.4  Sorting & Searching Problems**

### **Problem: Top K Frequent Elements**

Return the k most frequent elements in nums.

**🐢 Brute Force — Sort by count  |  O(n log n)**

def top\_k\_brute(nums, k):

    count \= {}

    for n in nums: count\[n\] \= count.get(n,0) \+ 1

    return sorted(count, key=count.get, reverse=True)\[:k\]

**🚀 Optimized — Min-Heap  |  O(n log k) time, O(n) space**

import heapq

from collections import Counter

def top\_k\_heap(nums, k):

    count \= Counter(nums)

    return heapq.nlargest(k, count, key=count.get)  \# O(n log k)

\# Or bucket sort: O(n) time\!

def top\_k\_bucket(nums, k):

    count \= Counter(nums)

    buckets \= \[\[\] for \_ in range(len(nums)+1)\]

    for num, freq in count.items():

        buckets\[freq\].append(num)   \# index \= frequency

    result \= \[\]

    for i in range(len(buckets)-1, \-1, \-1):

        result.extend(buckets\[i\])

        if len(result) \>= k: return result\[:k\]

### **Problem: Two Sum**

Return indices of two numbers that add to target.

**🐢 Brute Force  |  O(n²) time, O(1) space**

def two\_sum\_brute(nums, target):

    for i in range(len(nums)):

        for j in range(i+1, len(nums)):

            if nums\[i\]+nums\[j\] \== target:

                return \[i, j\]

**🚀 Optimized — Hash Map  |  O(n) time, O(n) space**

def two\_sum(nums, target):

    seen \= {}   \# value → index

    for i, n in enumerate(nums):

        complement \= target \- n

        if complement in seen:

            return \[seen\[complement\], i\]

        seen\[n\] \= i

### **Problem: Binary Search**

**🚀 Binary Search Template  |  O(log n)**

def binary\_search(nums, target):

    left, right \= 0, len(nums) \- 1

    while left \<= right:

        mid \= left \+ (right \- left) // 2  \# avoid overflow

        if nums\[mid\] \== target: return mid

        elif nums\[mid\] \< target: left \= mid \+ 1

        else: right \= mid \- 1

    return \-1

\# Or use bisect module:

import bisect

def binary\_search\_v2(nums, target):

    i \= bisect.bisect\_left(nums, target)

    return i if i \< len(nums) and nums\[i\] \== target else \-1

## **7.5  Dynamic Programming**

### **Problem: Climbing Stairs / Fibonacci**

How many ways to climb n stairs taking 1 or 2 steps at a time?

**🐢 Brute Force — Naive Recursion  |  O(2ⁿ) time**

def climb\_brute(n):

    if n \<= 1: return 1

    return climb\_brute(n-1) \+ climb\_brute(n-2)  \# exponential\!

**🚀 Optimized — Constant Space DP  |  O(n) time, O(1) space**

def climb(n):

    a, b \= 1, 1

    for \_ in range(n-1):

        a, b \= b, a+b   \# sliding window DP

    return b

\# Alternative: lru\_cache memoization (O(n) space):

from functools import lru\_cache

@lru\_cache(None)

def climb\_memo(n):

    if n \<= 1: return 1

    return climb\_memo(n-1) \+ climb\_memo(n-2)

### **Problem: Longest Common Subsequence (LCS)**

Given two strings, find the length of their longest common subsequence.

**🐢 Brute Force — Recursive  |  O(2ⁿ) time**

def lcs\_brute(s1, s2, i=0, j=0):

    if i \== len(s1) or j \== len(s2): return 0

    if s1\[i\] \== s2\[j\]:

        return 1 \+ lcs\_brute(s1, s2, i+1, j+1)

    return max(lcs\_brute(s1,s2,i+1,j), lcs\_brute(s1,s2,i,j+1))

**🚀 Optimized — Bottom-up DP  |  O(m·n) time, O(m·n) space**

def lcs(s1, s2):

    m, n \= len(s1), len(s2)

    dp \= \[\[0\]\*(n+1) for \_ in range(m+1)\]

    for i in range(1, m+1):

        for j in range(1, n+1):

            if s1\[i-1\] \== s2\[j-1\]:

                dp\[i\]\[j\] \= dp\[i-1\]\[j-1\] \+ 1

            else:

                dp\[i\]\[j\] \= max(dp\[i-1\]\[j\], dp\[i\]\[j-1\])

    return dp\[m\]\[n\]

\# Space-optimized: O(min(m,n)) space using two rows

def lcs\_space(s1, s2):

    if len(s1) \< len(s2): s1, s2 \= s2, s1

    prev \= \[0\]\*(len(s2)+1)

    for c1 in s1:

        curr \= \[0\]\*(len(s2)+1)

        for j, c2 in enumerate(s2, 1):

            curr\[j\] \= (prev\[j-1\]+1) if c1==c2 else max(prev\[j\],curr\[j-1\])

        prev \= curr

    return prev\[-1\]

## **7.6  Graph & Tree Patterns**

### **BFS Template — Level-Order Traversal**

**🚀 BFS with Level Tracking**

from collections import deque

def bfs\_levels(root):

    if not root: return \[\]

    result, queue \= \[\], deque(\[root\])

    while queue:

        level \= \[\]

        for \_ in range(len(queue)):   \# process entire level

            node \= queue.popleft()

            level.append(node.val)

            if node.left:  queue.append(node.left)

            if node.right: queue.append(node.right)

        result.append(level)

    return result

### **DFS Template — Tree**

**🚀 Iterative DFS (avoids recursion limit)**

def dfs\_iterative(root):

    if not root: return \[\]

    result, stack \= \[\], \[root\]

    while stack:

        node \= stack.pop()

        result.append(node.val)

        if node.right: stack.append(node.right)  \# right first

        if node.left:  stack.append(node.left)   \# left processed first

    return result  \# preorder: root, left, right

### **Problem: Number of Islands (Graph BFS/DFS)**

Count connected components of '1's in a 2D grid.

**🚀 BFS — O(m·n) time and space**

from collections import deque

def num\_islands(grid):

    if not grid: return 0

    rows, cols \= len(grid), len(grid\[0\])

    count \= 0

    for r in range(rows):

        for c in range(cols):

            if grid\[r\]\[c\] \== '1':

                count \+= 1

                queue \= deque(\[(r,c)\])

                grid\[r\]\[c\] \= '0'   \# mark visited

                while queue:

                    row,col \= queue.popleft()

                    for dr,dc in \[(1,0),(-1,0),(0,1),(0,-1)\]:

                        nr,nc \= row+dr, col+dc

                        if 0\<=nr\<rows and 0\<=nc\<cols and grid\[nr\]\[nc\]=='1':

                            grid\[nr\]\[nc\]='0'

                            queue.append((nr,nc))

    return count

## **7.7  Sliding Window Patterns**

### **Problem: Maximum Sum Subarray of Size K**

**🐢 Brute Force  |  O(n·k)**

def max\_sum\_brute(nums, k):

    max\_s \= float('-inf')

    for i in range(len(nums)-k+1):

        max\_s \= max(max\_s, sum(nums\[i:i+k\]))

    return max\_s

**🚀 Sliding Window  |  O(n) time, O(1) space**

def max\_sum\_window(nums, k):

    window \= sum(nums\[:k\])

    max\_s \= window

    for i in range(k, len(nums)):

        window \+= nums\[i\] \- nums\[i-k\]  \# slide: add right, remove left

        max\_s \= max(max\_s, window)

    return max\_s

### **Problem: Variable-Size Window — Minimum Window Substring**

Find smallest window in s containing all chars of t.

**🚀 Two-Pointer \+ Counter  |  O(n+m) time, O(m) space**

from collections import Counter

def min\_window(s, t):

    need \= Counter(t)

    have, required \= 0, len(need)  \# unique chars required

    window \= {}

    result \= (-1,-1); res\_len \= float('inf')

    left \= 0

    for right, ch in enumerate(s):

        window\[ch\] \= window.get(ch, 0\) \+ 1

        if ch in need and window\[ch\] \== need\[ch\]:

            have \+= 1

        while have \== required:   \# valid window — try to shrink

            if (right-left+1) \< res\_len:

                res\_len \= right-left+1

                result \= (left, right)

            window\[s\[left\]\] \-= 1

            if s\[left\] in need and window\[s\[left\]\] \< need\[s\[left\]\]:

                have \-= 1

            left \+= 1

    l, r \= result

    return s\[l:r+1\] if res\_len \!= float('inf') else ''

## **7.8  Common Pythonic Patterns (Interview Shortcuts)**

### **Frequency Counter — Counter vs defaultdict**

from collections import Counter, defaultdict

\# Counter is most concise:

Counter('aabbcc')          \# Counter({'a':2,'b':2,'c':2})

Counter(\[1,2,2,3,3,3\])    \# Counter({3:3,2:2,1:1})

\# defaultdict(int) when you need to increment manually:

freq \= defaultdict(int)

for ch in s: freq\[ch\] \+= 1

### **Transpose a Matrix**

matrix \= \[\[1,2,3\],\[4,5,6\],\[7,8,9\]\]

\# Using zip:

transposed \= list(map(list, zip(\*matrix)))

\# \[\[1,4,7\],\[2,5,8\],\[3,6,9\]\]

\# Using list comprehension:

transposed \= \[\[row\[i\] for row in matrix\] for i in range(len(matrix\[0\]))\]

### **Find All Duplicates / Unique Elements**

nums \= \[1,2,2,3,4,4,5\]

\# Duplicates:

\[x for x, cnt in Counter(nums).items() if cnt \> 1\]  \# \[2,4\]

\# First duplicate (O(n) time, O(n) space):

def first\_dup(lst):

    seen \= set()

    for x in lst:

        if x in seen: return x

        seen.add(x)

    return None

\# Unique elements (maintain order Python 3.7+):

list(dict.fromkeys(nums))  \# \[1,2,3,4,5\]

### **Sort Dict by Value**

d \= {'b':3,'a':1,'c':2}

\# Sort ascending by value:

sorted(d.items(), key=lambda x: x\[1\])  \# \[('a',1),('c',2),('b',3)\]

\# Get sorted dict:

dict(sorted(d.items(), key=lambda x: x\[1\]))

\# Top 2 by value:

dict(sorted(d.items(), key=lambda x: x\[1\], reverse=True)\[:2\])

### **Merge Intervals**

**🚀 Sort \+ Greedy  |  O(n log n)**

def merge\_intervals(intervals):

    intervals.sort(key=lambda x: x\[0\])   \# sort by start

    merged \= \[intervals\[0\]\]

    for start, end in intervals\[1:\]:

        if start \<= merged\[-1\]\[1\]:   \# overlaps

            merged\[-1\]\[1\] \= max(merged\[-1\]\[1\], end)

        else:

            merged.append(\[start, end\])

    return merged

merge\_intervals(\[\[1,3\],\[2,6\],\[8,10\],\[15,18\]\])

\# → \[\[1,6\],\[8,10\],\[15,18\]\]

### **Rotate a List / Array**

nums \= \[1,2,3,4,5,6,7\]

k \= 3  \# rotate right by k

\# One-liner (uses extra space):

rotated \= nums\[-k:\] \+ nums\[:-k\]  \# \[5,6,7,1,2,3,4\]

\# In-place O(1) space (triple reverse):

def rotate(nums, k):

    k %= len(nums)

    nums.reverse()         \# \[7,6,5,4,3,2,1\]

    nums\[:k\] \= nums\[:k\]\[::-1\]   \# \[5,6,7,4,3,2,1\]

    nums\[k:\] \= nums\[k:\]\[::-1\]   \# \[5,6,7,1,2,3,4\]

### **Power Set / All Subsets**

from itertools import combinations

def all\_subsets(lst):

    result \= \[\]

    for r in range(len(lst)+1):

        result.extend(combinations(lst, r))

    return result

\# Without itertools (bit masking):

def all\_subsets\_bitmask(lst):

    n \= len(lst)

    return \[\[lst\[j\] for j in range(n) if mask & (1\<\<j)\]

            for mask in range(1\<\<n)\]

### **Detect Cycle in Linked List — Floyd's Algorithm**

**🚀 Fast & Slow Pointer  |  O(n) time, O(1) space**

def has\_cycle(head):

    slow \= fast \= head

    while fast and fast.next:

        slow \= slow.next

        fast \= fast.next.next

        if slow is fast: return True

    return False

\# Find cycle start:

def detect\_cycle(head):

    slow \= fast \= head

    while fast and fast.next:

        slow, fast \= slow.next, fast.next.next

        if slow is fast:

            slow2 \= head

            while slow2 is not slow:

                slow, slow2 \= slow.next, slow2.next

            return slow  \# cycle start node

    return None

# **PART 8 — Complexity Quick Reference**

## **Time Complexity Cheat Sheet**

| Method / Function | Description | Example |
| :---- | :---- | :---- |
| list.append(x) | O(1) amortized | use freely |
| list.insert(0,x) | O(n) — shifts all | use deque.appendleft instead |
| list.pop() | O(1) from end | use freely |
| list.pop(0) | O(n) — shifts all | use deque.popleft() instead |
| x in list | O(n) linear scan | use set for O(1) |
| x in set | O(1) average | always prefer over list lookup |
| dict\[key\] | O(1) average | O(n) worst case (hash collision) |
| sorted(lst) | O(n log n) | Timsort, stable |
| list.sort() | O(n log n) | in-place Timsort, stable |
| heappush / heappop | O(log n) | priority queue operations |
| heapify(lst) | O(n) | faster than n heappush calls |
| bisect.bisect(a,x) | O(log n) | binary search on sorted list |
| Counter(iterable) | O(n) | single pass |
| set(lst) | O(n) avg | dedup with O(1) lookup |
| str.join(lst) | O(n) | MUCH faster than \+= in loop |
| ''.join vs \+= | O(n) vs O(n²) | ALWAYS use join for string building |

## **Common Gotchas Summary**

\# 1\. Mutable default arguments — BUG:

def f(lst=\[\]):  lst.append(1); return lst  \# same list every call\!

def f(lst=None): lst \= lst or \[\]; ...      \# CORRECT

\# 2\. List multiplication — shallow copy only:

grid \= \[\[0\]\*3\]\*3   \# BUG: all rows share same object

grid \= \[\[0\]\*3 for \_ in range(3)\]  \# CORRECT

\# 3\. String \+= in loop is O(n²) — use join:

result \= ''; \[result := result+c for c in chars\]  \# O(n²) BAD

result \= ''.join(chars)   \# O(n) GOOD

\# 4\. dict iteration while modifying:

\# BAD: for k in d: del d\[k\]  \# RuntimeError

for k in list(d.keys()): del d\[k\]  \# iterate copy

\# 5\. Chained comparison is fine in Python:

1 \< x \< 10   \# valid Python, equivalent to (1\<x) and (x\<10)

\# 6\. Integer caching (-5 to 256):

a \= b \= 256; a is b  \# True (cached)

a \= b \= 257; a is b  \# False (not cached) — use \== not is

\# 7\. NaN \!= NaN in Python:

import math

math.nan \== math.nan   \# → False  (use math.isnan())

*Python Complete Reference Guide — Interview Ready Edition*  
Built-in Functions  |  Collections  |  itertools  |  functools  |  heapq  |  bisect  |  math  |  os  |  re  |  datetime  |  json  |  random  |  pathlib  |  typing