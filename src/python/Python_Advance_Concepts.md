  
**🐍  Python Mastery Guide**  
*Decorators · Generators · Itertools · Functools · Magic Methods*  
*Metaclasses · Context Managers · Recursion · Stacks & More*

**🎨  1\. DECORATORS**

A decorator is a function that wraps another function (or class) to extend or modify its behavior without changing its source code. Use the @ syntax.

## **1.1 Basic Function Decorator**

def my\_decorator(func):  
    def wrapper(\*args, \*\*kwargs):  
        print("Before the function")  
        result \= func(\*args, \*\*kwargs)  
        print("After the function")  
        return result  
    return wrapper  
   
@my\_decorator  
def greet(name):  
    print(f"Hello, {name}\!")  
   
greet("Alice")

**\# Output:**  
\# Before the function  
\# Hello, Alice\!  
\# After the function

## **1.2 Decorator with Arguments**

def repeat(n):  
    def decorator(func):  
        def wrapper(\*args, \*\*kwargs):  
            for \_ in range(n):  
                func(\*args, \*\*kwargs)  
        return wrapper  
    return decorator  
   
@repeat(3)  
def say\_hi():  
    print("Hi\!")  
   
say\_hi()

**\# Output:**  
\# Hi\!  
\# Hi\!  
\# Hi\!

## **1.3 Practical Decorators**

### **Timer Decorator**

import time  
import functools  
   
def timer(func):  
    @functools.wraps(func)   \# preserves original func metadata  
    def wrapper(\*args, \*\*kwargs):  
        start \= time.perf\_counter()  
        result \= func(\*args, \*\*kwargs)  
        end \= time.perf\_counter()  
        print(f"{func.\_\_name\_\_} took {end-start:.4f}s")  
        return result  
    return wrapper  
   
@timer  
def compute():  
    return sum(range(1\_000\_000))  
   
compute()

**\# Output:**  
\# compute took 0.0312s

### **Memoize / Cache Decorator**

def memoize(func):  
    cache \= {}  
    def wrapper(\*args):  
        if args not in cache:  
            cache\[args\] \= func(\*args)  
        return cache\[args\]  
    return wrapper  
   
@memoize  
def fib(n):  
    if n \<= 1: return n  
    return fib(n-1) \+ fib(n-2)  
   
print(fib(10))   \# 55  (fast with cache)

## **1.4 Class Decorators**

def add\_repr(cls):  
    """Adds \_\_repr\_\_ to any class"""  
    def \_\_repr\_\_(self):  
        attrs \= ", ".join(f"{k}={v}" for k,v in vars(self).items())  
        return f"{cls.\_\_name\_\_}({attrs})"  
    cls.\_\_repr\_\_ \= \_\_repr\_\_  
    return cls  
   
@add\_repr  
class Point:  
    def \_\_init\_\_(self, x, y):  
        self.x \= x  
        self.y \= y  
   
p \= Point(3, 4\)  
print(p)   \# Point(x=3, y=4)

## **1.5 Using @property, @staticmethod, @classmethod**

class Circle:  
    def \_\_init\_\_(self, radius):  
        self.\_radius \= radius  
   
    @property  
    def radius(self):          \# getter  
        return self.\_radius  
   
    @radius.setter  
    def radius(self, value):   \# setter  
        if value \< 0: raise ValueError('Negative radius\!')  
        self.\_radius \= value  
   
    @property  
    def area(self):  
        import math  
        return math.pi \* self.\_radius \*\* 2  
   
    @staticmethod  
    def unit\_circle():         \# no self / cls  
        return Circle(1)  
   
    @classmethod  
    def from\_diameter(cls, d): \# receives class  
        return cls(d / 2\)  
   
c \= Circle(5)  
print(c.area)            \# 78.54  
print(Circle.unit\_circle().radius)  \# 1  
print(Circle.from\_diameter(10).radius)  \# 5.0

*💡 Use @functools.wraps(func) inside decorators to preserve the original function's \_\_name\_\_ and \_\_doc\_\_.*

**⚡  2\. GENERATORS**

Generators are functions that use yield to lazily produce values one at a time — great for large data and infinite sequences. They pause execution at each yield.

## **2.1 Basic Generator Function**

def countdown(n):  
    while n \> 0:  
        yield n  
        n \-= 1  
   
gen \= countdown(3)  
print(next(gen))  \# 3  
print(next(gen))  \# 2  
print(next(gen))  \# 1  
   
\# Or iterate:  
for val in countdown(5):  
    print(val, end=' ')  \# 5 4 3 2 1

## **2.2 Generator Expression**

squares \= (x\*\*2 for x in range(10))  \# lazy – no list created  
print(next(squares))  \# 0  
print(next(squares))  \# 1  
   
\# Sum without building a full list:  
total \= sum(x\*\*2 for x in range(1000))  
print(total)  \# 332833500

## **2.3 Infinite Generator**

def natural\_numbers():  
    n \= 1  
    while True:  
        yield n  
        n \+= 1  
   
import itertools  
first\_10 \= list(itertools.islice(natural\_numbers(), 10))  
print(first\_10)  \# \[1, 2, 3, 4, 5, 6, 7, 8, 9, 10\]

## **2.4 yield from (Delegating Generator)**

def flatten(nested):  
    for item in nested:  
        if isinstance(item, list):  
            yield from flatten(item)  \# delegate to sub-generator  
        else:  
            yield item  
   
data \= \[1, \[2, \[3, 4\]\], \[5, 6\]\]  
print(list(flatten(data)))  \# \[1, 2, 3, 4, 5, 6\]

## **2.5 Generator as Pipeline**

def read\_numbers():  
    for n in \[1, 2, 3, 4, 5, 6, 7, 8, 9, 10\]:  
        yield n  
   
def filter\_even(nums):  
    for n in nums:  
        if n % 2 \== 0: yield n  
   
def square(nums):  
    for n in nums: yield n \*\* 2  
   
pipeline \= square(filter\_even(read\_numbers()))  
print(list(pipeline))  \# \[4, 16, 36, 64, 100\]

*💡 Generators use O(1) memory regardless of the sequence size — perfect for processing huge files line by line.*

**📝  3\. STRING METHODS**

## **3.1 Case & Searching**

s \= "Hello, World\!"  
   
\# Case  
print(s.upper())         \# HELLO, WORLD\!  
print(s.lower())         \# hello, world\!  
print(s.title())         \# Hello, World\!  
print(s.swapcase())      \# hELLO, wORLD\!  
print(s.capitalize())    \# Hello, world\!  
   
\# Searching  
print(s.find('World'))   \# 7  (-1 if not found)  
print(s.index('World'))  \# 7  (raises ValueError if absent)  
print(s.count('l'))      \# 3  
print(s.startswith('He'))\# True  
print(s.endswith('\!'))   \# True  
print('World' in s)      \# True

## **3.2 Strip, Replace & Split**

s \= "  hello world  "  
print(s.strip())          \# 'hello world'  
print(s.lstrip())         \# 'hello world  '  
print(s.rstrip())         \# '  hello world'  
   
print("a-b-c".split("-"))  \# \["a", "b", "c"\]  
print("a-b-c".split("-", 1))  \# \["a", "b-c"\]  
print("-".join(\["a","b","c"\]))  \# "a-b-c"  
   
print("hello".replace("l","L"))  \# heLLo  
print("hello".replace("l","L",1))\# heLlo

## **3.3 Formatting**

\# f-strings (Python 3.6+)  
name, age \= "Alice", 30  
print(f"Name: {name}, Age: {age}")  \# Name: Alice, Age: 30  
print(f"{3.14159:.2f}")             \# 3.14  
print(f"{"hi":^10}")               \# "    hi    "  
print(f"{1000000:,}")              \# 1,000,000  
   
\# format()  
print("{0} loves {1}".format("Alice","Python"))  \# Alice loves Python  
print("{x:.2f}".format(x=3.14159))  \# 3.14  
   
\# zfill, ljust, rjust, center  
print("42".zfill(5))   \# 00042  
print("hi".ljust(10,"\*"))   \# hi\*\*\*\*\*\*\*\*  
print("hi".center(10,"-"))  \# \----hi----

## **3.4 Checking Methods**

print("hello123".isalnum())  \# True  
print("hello".isalpha())     \# True  
print("123".isdigit())       \# True  
print("   ".isspace())       \# True  
print("HELLO".isupper())     \# True  
print("hello".islower())     \# True  
print("Hello World".istitle())  \# True

**🔢  4\. NUMERIC METHODS & OPERATIONS**

## **4.1 Built-in Math Functions**

print(abs(-5))         \# 5  
print(round(3.14159, 2))  \# 3.14  
print(pow(2, 10))      \# 1024  
print(divmod(17, 5))   \# (3, 2\)  → quotient, remainder  
print(max(1,5,3,2,4))  \# 5  
print(min(1,5,3,2,4))  \# 1  
print(sum(\[1,2,3,4\]))  \# 10  
print(int(3.9))        \# 3  
print(float('3.14'))   \# 3.14  
print(bin(10))         \# 0b1010  
print(hex(255))        \# 0xff  
print(oct(8))          \# 0o10

## **4.2 math Module**

import math  
   
print(math.sqrt(16))    \# 4.0  
print(math.ceil(4.1))   \# 5  
print(math.floor(4.9))  \# 4  
print(math.factorial(5))\# 120  
print(math.log(100,10)) \# 2.0  
print(math.pi)          \# 3.141592...  
print(math.e)           \# 2.718281...  
print(math.gcd(12,8))   \# 4  
print(math.lcm(4,6))    \# 12  
print(math.isclose(0.1+0.2, 0.3, rel\_tol=1e-9))  \# True

## **4.3 int/float Methods**

x \= 3.14  
print(x.is\_integer())   \# False  
print((4.0).is\_integer())  \# True  
   
n \= 255  
print(n.bit\_length())   \# 8  
print(n.to\_bytes(2, 'big'))  \# b'\\x00\\xff'  
   
from decimal import Decimal  
d \= Decimal('1.1') \+ Decimal('2.2')  
print(d)  \# 3.3  (exact, no float errors)

**📋  5\. LIST METHODS**

## **5.1 Add / Remove**

lst \= \[3, 1, 4, 1, 5, 9\]  
   
lst.append(2)         \# adds to end: \[3,1,4,1,5,9,2\]  
lst.insert(0, 0\)      \# insert at index: \[0,3,1,4,1,5,9,2\]  
lst.extend(\[7, 8\])    \# extend: \[..., 7, 8\]  
   
lst.remove(1)         \# removes FIRST 1  
val \= lst.pop()       \# removes & returns last element  
val \= lst.pop(0)      \# removes & returns index 0  
lst.clear()           \# empty the list: \[\]

## **5.2 Search & Info**

lst \= \[3, 1, 4, 1, 5, 9, 2, 6\]  
   
print(lst.index(4))   \# 2  
print(lst.count(1))   \# 2  
print(len(lst))       \# 8  
print(min(lst))       \# 1  
print(max(lst))       \# 9  
print(sum(lst))       \# 31

## **5.3 Sort, Reverse, Copy**

lst \= \[3, 1, 4, 1, 5, 9\]  
   
lst.sort()            \# in-place: \[1,1,3,4,5,9\]  
lst.sort(reverse=True)\# descending: \[9,5,4,3,1,1\]  
lst.sort(key=abs)     \# by absolute value  
   
lst.reverse()         \# in-place reversal  
   
words \= \['banana','apple','cherry'\]  
words.sort(key=len)   \# \['apple','banana','cherry'\]  
   
\# sorted() returns NEW list:  
new \= sorted(lst, key=lambda x: \-x)  
   
copy1 \= lst.copy()    \# shallow copy  
copy2 \= lst\[:\]        \# also shallow copy

## **5.4 List Comprehensions**

\# \[expression for item in iterable if condition\]  
squares  \= \[x\*\*2 for x in range(10)\]  
evens    \= \[x for x in range(20) if x%2==0\]  
matrix   \= \[\[i\*j for j in range(1,4)\] for i in range(1,4)\]  
   
\# With multiple for:  
pairs \= \[(x,y) for x in \[1,2,3\] for y in \['a','b'\]\]  
\# \[(1,'a'),(1,'b'),(2,'a'),(2,'b'),(3,'a'),(3,'b')\]  
   
\# Nested comprehension to flatten:  
flat \= \[n for row in matrix for n in row\]

**🔁  6\. RECURSION**

Recursion is when a function calls itself. Every recursive function needs: (1) a base case to stop, (2) a recursive case that moves toward the base case.

## **6.1 Classic Examples**

\# Factorial  
def factorial(n):  
    if n \== 0: return 1        \# base case  
    return n \* factorial(n-1)  \# recursive case  
   
print(factorial(5))  \# 120  
   
\# Fibonacci  
def fib(n):  
    if n \<= 1: return n  
    return fib(n-1) \+ fib(n-2)  
   
print(fib(8))  \# 21  
   
\# Sum of list  
def sum\_list(lst):  
    if not lst: return 0  
    return lst\[0\] \+ sum\_list(lst\[1:\])  
   
print(sum\_list(\[1,2,3,4,5\]))  \# 15

## **6.2 Tree / Nested Structure Traversal**

\# Binary search tree traversal  
class Node:  
    def \_\_init\_\_(self, val, left=None, right=None):  
        self.val, self.left, self.right \= val, left, right  
   
def inorder(node):  
    if node is None: return \[\]  
    return inorder(node.left) \+ \[node.val\] \+ inorder(node.right)  
   
tree \= Node(4, Node(2, Node(1), Node(3)), Node(6, Node(5), Node(7)))  
print(inorder(tree))  \# \[1, 2, 3, 4, 5, 6, 7\]

## **6.3 Tail Recursion & sys.setrecursionlimit**

import sys  
sys.setrecursionlimit(5000)  \# default is 1000  
   
\# Tail-recursive style with accumulator (more efficient):  
def factorial\_tail(n, acc=1):  
    if n \== 0: return acc  
    return factorial\_tail(n-1, acc\*n)  \# accumulates result  
   
print(factorial\_tail(10))  \# 3628800

*💡 Python does NOT optimize tail recursion. For deep recursion, prefer iteration or use sys.setrecursionlimit carefully.*

**🗂️  7\. STACKS**

A stack is a Last-In First-Out (LIFO) data structure. Python has several ways to implement one.

## **7.1 Stack with list**

stack \= \[\]  
stack.append(1)    \# push  
stack.append(2)  
stack.append(3)  
print(stack)       \# \[1, 2, 3\]  
   
top \= stack.pop()  \# pop (removes 3\)  
print(top)         \# 3  
print(stack\[-1\])   \# peek: 2  (no removal)  
print(bool(stack)) \# True (not empty)

## **7.2 Stack Class Implementation**

class Stack:  
    def \_\_init\_\_(self):  
        self.\_data \= \[\]  
   
    def push(self, val):  self.\_data.append(val)  
    def pop(self):        return self.\_data.pop()  
    def peek(self):       return self.\_data\[-1\]  
    def is\_empty(self):   return len(self.\_data) \== 0  
    def size(self):       return len(self.\_data)  
    def \_\_repr\_\_(self):   return f'Stack({self.\_data})'  
   
s \= Stack()  
s.push(10); s.push(20); s.push(30)  
print(s)          \# Stack(\[10, 20, 30\])  
print(s.peek())   \# 30  
print(s.pop())    \# 30  
print(s.size())   \# 2

## **7.3 Stack Application – Balanced Parentheses**

def is\_balanced(expr):  
    stack \= \[\]  
    pairs \= {')':'(', '\]':'\[', '}':'{'}  
    for ch in expr:  
        if ch in '(\[{':  
            stack.append(ch)  
        elif ch in ')\]}':  
            if not stack or stack\[-1\] \!= pairs\[ch\]:  
                return False  
            stack.pop()  
    return len(stack) \== 0  
   
print(is\_balanced("({\[\]})"))  \# True  
print(is\_balanced("({\[})"))   \# False

## 

## 

## 

## **7.4 collections.deque as Stack**

from collections import deque  
   
stack \= deque()  
stack.append(1)  
stack.append(2)  
stack.append(3)  
print(stack.pop())  \# 3  (O(1) unlike list.pop(0))

**🔗  8\. ITERTOOLS METHODS**

## **8.1 Infinite Iterators**

import itertools  
   
\# count(start, step) – counts forever  
for n in itertools.islice(itertools.count(10, 2), 5):  
    print(n, end=' ')   \# 10 12 14 16 18  
   
\# cycle(iterable) – repeats forever  
colors \= itertools.cycle(\['red','green','blue'\])  
for \_ in range(6):  
    print(next(colors), end=' ')  \# red green blue red green blue  
   
\# repeat(value, times)  
print(list(itertools.repeat(7, 4)))  \# \[7, 7, 7, 7\]

## **8.2 Combinatorics**

\# permutations – ordered arrangements  
p \= list(itertools.permutations('ABC', 2))  
print(p)  \# \[('A','B'),('A','C'),('B','A'),('B','C'),('C','A'),('C','B')\]  
   
\# combinations – unordered, no repeats  
c \= list(itertools.combinations(\[1,2,3\], 2))  
print(c)  \# \[(1,2),(1,3),(2,3)\]  
   
\# combinations\_with\_replacement – unordered, with repeats  
cr \= list(itertools.combinations\_with\_replacement('AB', 2))  
print(cr)  \# \[('A','A'),('A','B'),('B','B')\]  
   
\# product – Cartesian product  
prod \= list(itertools.product(\[1,2\],\[3,4\]))  
print(prod)  \# \[(1,3),(1,4),(2,3),(2,4)\]

## **8.3 Chaining & Slicing**

\# chain – connect iterables  
merged \= list(itertools.chain(\[1,2\],\[3,4\],\[5,6\]))  
print(merged)   \# \[1, 2, 3, 4, 5, 6\]  
   
\# islice – lazy slice  
sliced \= list(itertools.islice(range(100), 5, 15, 2))  
print(sliced)   \# \[5, 7, 9, 11, 13\]  
   
\# zip\_longest – zip with fill value  
zl \= list(itertools.zip\_longest(\[1,2,3\],\[4,5\], fillvalue=0))  
print(zl)       \# \[(1,4),(2,5),(3,0)\]  
   
\# starmap – apply func to each tuple  
sm \= list(itertools.starmap(pow, \[(2,3),(3,2),(10,2)\]))  
print(sm)       \# \[8, 9, 100\]

## **8.4 Filtering & Grouping**

\# groupby – group consecutive identical keys  
data \= \[('a',1),('a',2),('b',3),('b',4),('a',5)\]  
for key, group in itertools.groupby(data, key=lambda x: x\[0\]):  
    print(key, list(group))  
\# a \[('a',1),('a',2)\]  
\# b \[('b',3),('b',4)\]  
\# a \[('a',5)\]  
   
\# takewhile / dropwhile  
tw \= list(itertools.takewhile(lambda x: x\<5, \[1,2,3,4,5,1\]))  
print(tw)   \# \[1, 2, 3, 4\]  
   
dw \= list(itertools.dropwhile(lambda x: x\<5, \[1,2,3,4,5,6\]))  
print(dw)   \# \[5, 6\]  
   
\# filterfalse  
ff \= list(itertools.filterfalse(lambda x: x%2, range(8)))  
print(ff)   \# \[0, 2, 4, 6\]

**⚙️  9\. FUNCTOOLS METHODS**

## **9.1 functools.lru\_cache**

from functools import lru\_cache  
   
@lru\_cache(maxsize=128)  \# caches up to 128 results  
def fib(n):  
    if n \< 2: return n  
    return fib(n-1) \+ fib(n-2)  
   
print(fib(50))         \# 12586269025 (fast\!)  
print(fib.cache\_info())\# CacheInfo(hits=48, misses=51,...)  
   
\# @cache  (Python 3.9+) – unbounded cache  
from functools import cache  
@cache  
def expensive(n): return n \*\* n

## **9.2 functools.partial**

from functools import partial  
   
def power(base, exp):  
    return base \*\* exp  
   
square \= partial(power, exp=2)  
cube   \= partial(power, exp=3)  
   
print(square(5))  \# 25  
print(cube(3))    \# 27  
   
\# Real use case:  
from functools import partial  
add\_tax \= partial(round, ndigits=2)  
price \= add\_tax(99.999)  
print(price)  \# 100.0

## **9.3 functools.reduce**

from functools import reduce  
   
\# reduce(func, iterable\[, initial\])  
product \= reduce(lambda a, b: a \* b, \[1,2,3,4,5\])  
print(product)  \# 120  
   
\# Flatten nested list  
nested \= \[\[1,2\],\[3,4\],\[5,6\]\]  
flat \= reduce(lambda a,b: a+b, nested)  
print(flat)  \# \[1, 2, 3, 4, 5, 6\]  
   
\# Max of a list  
mx \= reduce(lambda a,b: a if a\>b else b, \[3,1,4,1,5,9\])  
print(mx)  \# 9

## **9.4 functools.wraps & total\_ordering**

from functools import wraps, total\_ordering  
   
\# wraps – preserve metadata in decorators  
def decorator(func):  
    @wraps(func)  
    def wrapper(\*args, \*\*kwargs):  
        return func(\*args, \*\*kwargs)  
    return wrapper  
   
@decorator  
def hello(): 'Says hello'  
print(hello.\_\_name\_\_)  \# "hello" (not "wrapper")  
   
\# total\_ordering – fill in comparison methods  
@total\_ordering  
class Student:  
    def \_\_init\_\_(self, name, gpa):  
        self.name, self.gpa \= name, gpa  
    def \_\_eq\_\_(self, other): return self.gpa \== other.gpa  
    def \_\_lt\_\_(self, other): return self.gpa \< other.gpa  
    \# \_\_le\_\_, \_\_gt\_\_, \_\_ge\_\_ auto-generated\!  
   
a, b \= Student('Alice',3.8), Student('Bob',3.5)  
print(a \> b)  \# True

**🔒  10\. CONTEXT MANAGERS**

Context managers manage resources (files, DB connections, locks) via the 'with' statement, guaranteeing setup and teardown even if exceptions occur.

## **10.1 Using with Statement**

\# File handling – the classic context manager  
with open('example.txt', 'w') as f:  
    f.write('Hello, World\!')   \# file auto-closes after block  
   
\# Multiple context managers  
with open('in.txt') as fin, open('out.txt','w') as fout:  
    fout.write(fin.read())

## **10.2 Custom Context Manager (Class)**

class DBConnection:  
    def \_\_init\_\_(self, host):  
        self.host \= host  
        self.conn \= None  
   
    def \_\_enter\_\_(self):       \# called on entering 'with'  
        print(f"Connecting to {self.host}")  
        self.conn \= f'conn:{self.host}'  
        return self.conn  
   
    def \_\_exit\_\_(self, exc\_type, exc\_val, exc\_tb):  
        print('Connection closed')  
        self.conn \= None  
        return False  \# don't suppress exceptions  
   
with DBConnection('localhost') as conn:  
    print(f'Using {conn}')

**\# Output:**  
\# Connecting to localhost  
\# Using conn:localhost  
\# Connection closed

## **10.3 Custom Context Manager (contextlib)**

from contextlib import contextmanager  
   
@contextmanager  
def managed\_resource(name):  
    print(f"Acquiring {name}")  
    try:  
        yield name          \# value returned by 'as'  
    finally:  
        print(f"Releasing {name}")  
   
with managed\_resource('DB lock') as res:  
    print(f"Working with {res}")

## **10.4 contextlib Utilities**

from contextlib import suppress, redirect\_stdout  
import io  
   
\# suppress – silently ignore specific exceptions  
with suppress(FileNotFoundError):  
    open('missing.txt')  
   
\# redirect\_stdout – capture output  
buf \= io.StringIO()  
with redirect\_stdout(buf):  
    print("captured\!")  
print(buf.getvalue())  \# 'captured\!\\n'  
   
\# ExitStack – dynamic context managers  
from contextlib import ExitStack  
files \= \['a.txt','b.txt'\]  
with ExitStack() as stack:  
    handles \= \[stack.enter\_context(open(f,'w')) for f in files\]

**✨  11\. MAGIC (DUNDER) METHODS**

Magic methods (also called dunder methods – double underscore) let you define how Python's built-in operators and functions behave on your custom objects.

## **11.1 Object Lifecycle**

class Dog:  
    def \_\_new\_\_(cls, \*args, \*\*kwargs):   \# called BEFORE \_\_init\_\_  
        print('Creating instance')  
        return super().\_\_new\_\_(cls)  
   
    def \_\_init\_\_(self, name, breed):  
        self.name  \= name  
        self.breed \= breed  
        print(f'{name} initialized')  
   
    def \_\_del\_\_(self):                   \# called on garbage collection  
        print(f'{self.name} deleted')  
   
d \= Dog('Rex', 'Labrador')  
del d

**\# Output:**  
\# Creating instance  
\# Rex initialized  
\# Rex deleted

## **11.2 String Representation**

class Book:  
    def \_\_init\_\_(self, title, pages):  
        self.title, self.pages \= title, pages  
   
    def \_\_str\_\_(self):   \# human-readable (used by print)  
        return f'Book: {self.title}'  
   
    def \_\_repr\_\_(self):  \# developer-repr (debugging)  
        return f'Book(title={self.title\!r}, pages={self.pages})'  
   
b \= Book('Python Tricks', 300\)  
print(b)        \# Book: Python Tricks  
print(repr(b))  \# Book(title='Python Tricks', pages=300)

## 

## **11.3 Arithmetic Operators**

class Vector:  
    def \_\_init\_\_(self, x, y):  
        self.x, self.y \= x, y  
   
    def \_\_add\_\_(self, other):  return Vector(self.x+other.x, self.y+other.y)  
    def \_\_sub\_\_(self, other):  return Vector(self.x-other.x, self.y-other.y)  
    def \_\_mul\_\_(self, scalar): return Vector(self.x\*scalar, self.y\*scalar)  
    def \_\_neg\_\_(self):         return Vector(-self.x, \-self.y)  
    def \_\_abs\_\_(self):         return (self.x\*\*2 \+ self.y\*\*2)\*\*0.5  
    def \_\_repr\_\_(self):        return f'Vector({self.x},{self.y})'  
   
v1 \= Vector(1, 2\)  
v2 \= Vector(3, 4\)  
print(v1 \+ v2)  \# Vector(4,6)  
print(v1 \* 3\)   \# Vector(3,6)  
print(abs(v2))  \# 5.0

## **11.4 Comparison Operators**

class Temperature:  
    def \_\_init\_\_(self, celsius):  
        self.celsius \= celsius  
   
    def \_\_eq\_\_(self, other): return self.celsius \== other.celsius  
    def \_\_lt\_\_(self, other): return self.celsius \< other.celsius  
    def \_\_le\_\_(self, other): return self.celsius \<= other.celsius  
    def \_\_gt\_\_(self, other): return self.celsius \> other.celsius  
    def \_\_ge\_\_(self, other): return self.celsius \>= other.celsius  
   
t1, t2 \= Temperature(100), Temperature(80)  
print(t1 \> t2)   \# True  
print(sorted(\[t1, t2\])\[-1\].celsius)  \# 100

## **11.5 Container Protocol**

class NumberBag:  
    def \_\_init\_\_(self, \*nums):  
        self.\_items \= list(nums)  
   
    def \_\_len\_\_(self):         return len(self.\_items)

    def \_\_getitem\_\_(self, i):  return self.\_items\[i\]

    def \_\_setitem\_\_(self, i, v): self.\_items\[i\] \= v

    def \_\_delitem\_\_(self, i):  del self.\_items\[i\]

    def \_\_contains\_\_(self, v): return v in self.\_items

    def \_\_iter\_\_(self):        return iter(self.\_items)  
   
bag \= NumberBag(10, 20, 30\)  
print(len(bag))    \# 3  
print(bag\[1\])      \# 20  
print(20 in bag)   \# True  
for n in bag: print(n, end=' ')  \# 10 20 30

## 

## 

## **11.6 Callable & Context Manager Magic**

\# \_\_call\_\_ – make instance callable  
class Multiplier:  
    def \_\_init\_\_(self, factor):  
        self.factor \= factor  
    def \_\_call\_\_(self, x):  
        return x \* self.factor  
   
double \= Multiplier(2)  
print(double(5))    \# 10  
print(double(100))  \# 200  
   
\# \_\_enter\_\_ and \_\_exit\_\_ for 'with' support  
class Timer:  
    def \_\_enter\_\_(self):  
        import time  
        self.start \= time.time()  
        return self

    def \_\_exit\_\_(self, \*args):  
        self.elapsed \= time.time() \- self.start  
   
with Timer() as t:  
    sum(range(1\_000\_000))  
print(f"Elapsed: {t.elapsed:.4f}s")

## **11.7 Attribute Access Magic**

class Config:  
    def \_\_init\_\_(self):  
        self.\_data \= {}  
   
    def \_\_getattr\_\_(self, name):      \# called when attr not found  
        return self.\_data.get(name, 'N/A')  
   
    def \_\_setattr\_\_(self, name, val): \# called on every assignment  
        if name.startswith('\_'):  
            super().\_\_setattr\_\_(name, val)  
        else:  
            self.\_data\[name\] \= val  
   
cfg \= Config()  
cfg.host \= 'localhost'  
cfg.port \= 8080  
print(cfg.host)     \# localhost  
print(cfg.missing)  \# N/A

**🧠  12\. METACLASSES**

A metaclass is a 'class of a class'. Just as a class defines how instances behave, a metaclass defines how classes themselves behave. The default metaclass is 'type'.

## **12.1 type() – The Default Metaclass**

\# type(name, bases, dict) creates a class dynamically  
Dog \= type('Dog', (object,), {  
    'species': 'Canis lupus',  
    'bark': lambda self: 'Woof\!'  
})  
   
d \= Dog()  
print(d.bark())     \# Woof\!  
print(type(Dog))    \# \<class 'type'\>  
print(type(d))      \# \<class '\_\_main\_\_.Dog'\>

## **12.2 Custom Metaclass**

class SingletonMeta(type):  
    """Metaclass that enforces singleton pattern"""  
    \_instances \= {}  
   
    def \_\_call\_\_(cls, \*args, \*\*kwargs):  
        if cls not in cls.\_instances:  
            cls.\_instances\[cls\] \= super().\_\_call\_\_(\*args, \*\*kwargs)  
        return cls.\_instances\[cls\]  
   
class Database(metaclass=SingletonMeta):  
    def \_\_init\_\_(self):  
        self.connected \= True  
   
db1 \= Database()  
db2 \= Database()  
print(db1 is db2)   \# True – same instance\!

## **12.3 Metaclass for Validation**

class ValidateMeta(type):  
    def \_\_new\_\_(mcs, name, bases, namespace):  
        for key, val in namespace.items():  
            if callable(val) and not key.startswith('\_'):  
                if not val.\_\_doc\_\_:  
                    raise TypeError(  
                        f'{name}.{key} must have a docstring\!'  
                    )  
        return super().\_\_new\_\_(mcs, name, bases, namespace)  
   
class Service(metaclass=ValidateMeta):  
    def process(self):  
        """Process the request"""  
        pass  
   
\# This would raise TypeError:  
\# class BadService(metaclass=ValidateMeta):  
\#     def run(self): pass  \# no docstring\!

## **12.4 \_\_init\_subclass\_\_ (Modern Alternative)**

class Plugin:  
    \_registry \= {}  
   
    def \_\_init\_subclass\_\_(cls, plugin\_name=None, \*\*kwargs):  
        super().\_\_init\_subclass\_\_(\*\*kwargs)  
        if plugin\_name:  
            Plugin.\_registry\[plugin\_name\] \= cls  
   
class VideoPlugin(Plugin, plugin\_name='video'):  
    def run(self): print('Running video plugin')  
   
class AudioPlugin(Plugin, plugin\_name='audio'):  
    def run(self): print('Running audio plugin')  
   
print(Plugin.\_registry)  
\# {'video': \<class 'VideoPlugin'\>, 'audio': \<class 'AudioPlugin'\>}  
   
Plugin.\_registry\['video'\]().run()  \# Running video plugin

**🏗️  13\. WAYS TO CREATE A CLASS**

## **13.1 Standard class Statement**

class Animal:  
    kingdom \= 'Animalia'  \# class variable  
   
    def \_\_init\_\_(self, name):  
        self.name \= name   \# instance variable  
   
    def speak(self):  
        return f'{self.name} makes a sound'  
   
cat \= Animal('Cat')  
print(cat.speak())   \# Cat makes a sound

## **13.2 Using type() Dynamically**

\# type(name, bases, dict)  
Car \= type('Car', (object,), {  
    'wheels': 4,  
    '\_\_init\_\_': lambda self, brand: setattr(self, 'brand', brand),  
    '\_\_repr\_\_': lambda self: f'Car({self.brand})',  
})  
   
c \= Car('Toyota')  
print(c)          \# Car(Toyota)  
print(c.wheels)   \# 4

## **13.3 dataclass (Python 3.7+)**

from dataclasses import dataclass, field  
   
@dataclass  
class Point:  
    x: float  
    y: float  
    z: float \= 0.0   \# default value  
    tags: list \= field(default\_factory=list)  
   
p \= Point(1.0, 2.0)  
print(p)           \# Point(x=1.0, y=2.0, z=0.0, tags=\[\])  
print(p.x)         \# 1.0  
   
@dataclass(frozen=True)   \# immutable like namedtuple  
class RGB:  
    r: int; g: int; b: int  
   
color \= RGB(255, 0, 128\)  
\# color.r \= 0  → FrozenInstanceError

## **13.4 namedtuple**

from collections import namedtuple  
   
\# Classic namedtuple  
Person \= namedtuple('Person', \['name', 'age', 'city'\])  
p \= Person('Alice', 30, 'Hyderabad')  
print(p.name)         \# Alice  
print(p\[1\])           \# 30  
print(p.\_asdict())    \# OrderedDict(name='Alice', ...)  
   
\# typing.NamedTuple – with types and defaults  
from typing import NamedTuple  
class Employee(NamedTuple):  
    name: str  
    dept: str  
    salary: float \= 0.0  
   
e \= Employee('Bob', 'Engineering', 95000\)  
print(e)  \# Employee(name='Bob', dept='Engineering', salary=95000)

## **13.5 attrs Library**

\# pip install attrs  
import attr  
   
@attr.s  
class Product:  
    name  \= attr.ib(validator=attr.validators.instance\_of(str))  
    price \= attr.ib(validator=attr.validators.gt(0))  
    qty   \= attr.ib(default=0)  
   
p \= Product('Widget', 9.99, qty=100)  
print(p)  \# Product(name='Widget', price=9.99, qty=100)

## **13.6 Class Factory Function**

def make\_animal(name, sound):  
    class Animal:  
        species \= name  
        def speak(self):  
            return sound  
        def \_\_repr\_\_(self):  
            return f'\<{name}\>',  
    Animal.\_\_name\_\_ \= name  
    return Animal  
   
Cat \= make\_animal('Cat', 'Meow')  
Dog \= make\_animal('Dog', 'Woof')  
   
print(Cat().speak())  \# Meow  
print(Dog().speak())  \# Woof

## **13.7 Abstract Base Class**

from abc import ABC, abstractmethod  
   
class Shape(ABC):  
    @abstractmethod  
    def area(self): ...  
   
    @abstractmethod  
    def perimeter(self): ...  
   
    def describe(self):  
        return f"Area={self.area():.2f}"  
   
class Rectangle(Shape):  
    def \_\_init\_\_(self, w, h): self.w, self.h \= w, h  
    def area(self):      return self.w \* self.h  
    def perimeter(self): return 2\*(self.w+self.h)  
   
r \= Rectangle(4, 5\)  
print(r.describe())   \# Area=20.00  
\# Shape()  → TypeError: Can't instantiate abstract class

## **13.8 Mixin Pattern**

class JSONMixin:  
    def to\_json(self):  
        import json  
        return json.dumps(self.\_\_dict\_\_)  
   
class LogMixin:  
    def log(self, msg):  
        print(f"\[{self.\_\_class\_\_.\_\_name\_\_}\] {msg}")  
   
class User(JSONMixin, LogMixin):  
    def \_\_init\_\_(self, name, email):  
        self.name  \= name  
        self.email \= email  
   
u \= User("Alice","alice@example.com")  
print(u.to\_json())  \# {"name": "Alice", "email": "alice@example.com"}  
u.log("Created")    \# \[User\] Created

## **13.9 \_\_slots\_\_ for Memory Optimization**

class Point:  
    \_\_slots\_\_ \= ('x', 'y')   \# no \_\_dict\_\_, faster \+ less memory  
    def \_\_init\_\_(self, x, y):  
        self.x, self.y \= x, y  
   
p \= Point(3, 4\)  
print(p.x, p.y)   \# 3 4  
\# p.z \= 5  → AttributeError: 'Point' has no attribute 'z'

# **📊 Quick Reference Summary**

| Concept | Key Syntax | Use Case |
| :---- | :---- | :---- |
| Decorator | @my\_dec / @wraps | Modify functions/classes |
| Generator | yield / yield from | Lazy sequences, pipelines |
| String Methods | .upper() .split() .format() | Text processing |
| Numeric Methods | math.sqrt() divmod() abs() | Math computations |
| List Methods | .sort() .append() .pop() | Collection manipulation |
| Recursion | def f(): return f() | Trees, divide-and-conquer |
| Stack | list.append/pop or deque | LIFO, undo, parsing |
| itertools | chain() product() groupby() | Combinatorics, iteration |
| functools | lru\_cache partial reduce | Caching, HOF |
| Context Manager | with / \_\_enter\_\_/\_\_exit\_\_ | Resource management |
| Magic Methods | \_\_add\_\_ \_\_len\_\_ \_\_call\_\_ | Operator overloading |
| Metaclass | class Meta(type): | Class creation control |
| dataclass | @dataclass | Data containers |

**Happy Coding\! 🐍**  *Master Python one concept at a time.*