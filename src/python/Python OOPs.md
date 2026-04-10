**Python OOP**

Object-Oriented Programming Guide

*Basic to Advanced — Complete Reference*

# **1\. Introduction to OOP**

Object-Oriented Programming (OOP) is a programming paradigm that organises software design around data (objects) rather than logic and functions. Python is a multi-paradigm language with first-class support for OOP. 

OOP is a programming paradigm in which software is structured around objects, which are instances of classes. 

A **class** defines the **data (attributes)** and **behaviour (methods)**, and **objects** are the actual entities created from the class.

**Key Idea:**  
 OOP organises code around **objects and their interactions**, improving:

* Modularity  
* Reusability  
* Maintainability  
* Scalability

## **▸ Core OOP Pillars**

* Encapsulation — It restricts direct access to data and allows controlled access through methods**.**

* Abstraction — It hides complex implementation details and exposes 	 only what is necessary

* Inheritance — It allows one class to inherit attributes and methods from another class.

* Polymorphism — It allows the same method name to behave differently depending on the object.

| 💡 Why OOP? OOP improves code reusability, makes large codebases manageable, and models real-world entities naturally — making software easier to reason about and maintain. |
| :---- |

# **2\. Classes and Objects**

A class is a blueprint for creating objects. An object is an instance of a class that holds state (attributes) and behaviour (methods).

## **▸ Defining a Class**

| `class Dog:` |
| :---- |
|     `"""Represents a dog."""` |
|  |
|     `# Class attribute — shared by all instances` |
|     `species = "Canis lupus familiaris"` |
|  |
|     `# Constructor / initialiser` |
|     `def __init__(self, name: str, age: int):` |
|         `self.name = name    # Instance attribute` |
|         `self.age  = age     # Instance attribute` |
|  |
|     `# Instance method` |
|     `def bark(self) -> str:` |
|         `return f"{self.name} says: Woof!"` |
|  |
|     `# String representation` |
|     `def __repr__(self) -> str:` |
|         `return f"Dog(name={self.name!r}, age={self.age})"` |
|  |
|  |
| `# Creating objects (instances)` |
| `rex   = Dog("Rex", 3)` |
| `buddy = Dog("Buddy", 5)` |
|  |
| `print(rex.bark())          # Rex says: Woof!` |
| `print(buddy.species)       # Canis lupus familiaris` |
| `print(Dog.species)         # Canis lupus familiaris` |

## **▸ Class vs Instance Attributes**

Class attributes belong to the class and are shared across all instances. Instance attributes are unique to each object.

| `class Counter:` |
| :---- |
|     `count = 0              # Class attribute` |
|  |
|     `def __init__(self):` |
|         `Counter.count += 1` |
|         `self.id = Counter.count    # Instance attribute` |
|  |
| `a = Counter()   # count = 1` |
| `b = Counter()   # count = 2` |
| `print(Counter.count)   # 2` |
| `print(a.id, b.id)      # 1  2` |

# **3\. Constructors and Destructors**

Python provides special (dunder) methods to initialise and clean up objects.

## **▸ \_\_init\_\_ and \_\_del\_\_**

| `class FileHandler:` |
| :---- |
|     `def __init__(self, filename: str):` |
|         `self.filename = filename` |
|         `self.file = open(filename, 'w')` |
|         `print(f"Opened {filename}")` |
|  |
|     `def write(self, text: str):` |
|         `self.file.write(text)` |
|  |
|     `def __del__(self):` |
|         `"""Called when the object is garbage-collected."""` |
|         `self.file.close()` |
|         `print(f"Closed {self.filename}")` |
|  |
|     `# Preferred pattern: context manager` |
|     `def __enter__(self):` |
|         `return self` |
|  |
|     `def __exit__(self, *args):` |
|         `self.file.close()` |
|  |
| `# Context manager usage (recommended over __del__)` |
| `with FileHandler('log.txt') as fh:` |
|     `fh.write('Hello!')` |

# **4\. Encapsulation**

Encapsulation restricts direct access to an object's internal state. Python uses naming conventions and properties to achieve this.

## **▸ Access Modifiers**

* public      — no underscore prefix; accessible anywhere

* \_protected  — single underscore; convention says 'internal use'

* \_\_private   — double underscore; name-mangled by Python

| `class BankAccount:` |
| :---- |
|     `def __init__(self, owner: str, balance: float = 0.0):` |
|         `self.owner     = owner       # public` |
|         `self._bank     = 'PyBank'    # protected` |
|         `self.__balance = balance     # private (name-mangled)` |
|  |
|     `@property` |
|     `def balance(self) -> float:` |
|         `"""Read-only access to balance."""` |
|         `return self.__balance` |
|  |
|     `@balance.setter` |
|     `def balance(self, amount: float):` |
|         `if amount < 0:` |
|             `raise ValueError("Balance cannot be negative")` |
|         `self.__balance = amount` |
|  |
|     `def deposit(self, amount: float):` |
|         `if amount <= 0:` |
|             `raise ValueError("Deposit must be positive")` |
|         `self.__balance += amount` |
|  |
|     `def __repr__(self) -> str:` |
|         `return f"BankAccount({self.owner!r}, balance={self.__balance:.2f})"` |
|  |
|  |
| `acc = BankAccount("Alice", 1000)` |
| `acc.deposit(500)` |
| `print(acc.balance)          # 1500.0` |
| `# acc.__balance             # AttributeError!` |
| `# acc._BankAccount__balance # works (name mangling)` |

## **▸ Properties with @property**

The @property decorator lets you define getter, setter, and deleter methods on an attribute, enforcing validation without changing the public API.

| `class Temperature:` |
| :---- |
|     `def __init__(self, celsius: float = 0):` |
|         `self.celsius = celsius    # triggers setter` |
|  |
|     `@property` |
|     `def celsius(self) -> float:` |
|         `return self._celsius` |
|  |
|     `@celsius.setter` |
|     `def celsius(self, value: float):` |
|         `if value < -273.15:` |
|             `raise ValueError("Below absolute zero!")` |
|         `self._celsius = value` |
|  |
|     `@property` |
|     `def fahrenheit(self) -> float:` |
|         `return self._celsius * 9 / 5 + 32` |
|  |
|  |
| `t = Temperature(100)` |
| `print(t.fahrenheit)    # 212.0` |
| `t.celsius = -300       # ValueError!` |

# **5\. Inheritance**

Inheritance allows a class (child) to acquire attributes and methods of another class (parent), enabling code reuse and specialisation.

## **▸ Single Inheritance**

| `class Animal:` |
| :---- |
|     `def __init__(self, name: str):` |
|         `self.name = name` |
|  |
|     `def speak(self) -> str:` |
|         `raise NotImplementedError("Subclass must implement speak()")` |
|  |
|     `def __repr__(self) -> str:` |
|         `return f"{type(self).__name__}({self.name!r})"` |
|  |
|  |
| `class Cat(Animal):` |
|     `def speak(self) -> str:` |
|         `return f"{self.name} says: Meow!"` |
|  |
|  |
| `class Dog(Animal):` |
|     `def speak(self) -> str:` |
|         `return f"{self.name} says: Woof!"` |
|  |
|  |
| `print(Cat("Whiskers").speak())` |
| `print(Dog("Rex").speak())` |

## **▸ super() and Method Resolution** 

| `class Vehicle:` |
| :---- |
|     `def __init__(self, make: str, model: str, year: int):` |
|         `self.make  = make` |
|         `self.model = model` |
|         `self.year  = year` |
|  |
|     `def description(self) -> str:` |
|         `return f"{self.year} {self.make} {self.model}"` |
|  |
|  |
| `class ElectricVehicle(Vehicle):` |
|     `def __init__(self, make, model, year, battery_kwh: float):` |
|         `super().__init__(make, model, year)   # call parent __init__` |
|         `self.battery_kwh = battery_kwh` |
|  |
|     `def description(self) -> str:` |
|         `base = super().description()` |
|         `return f"{base} [EV {self.battery_kwh}kWh]"` |
|  |
|  |
| `ev = ElectricVehicle("Tesla", "Model 3", 2024, 75)` |
| `print(ev.description())` |
| `# 2024 Tesla Model 3 [EV 75kWh]` |

## **▸ Multiple Inheritance and MRO**

Python supports multiple inheritance. The Method Resolution Order (MRO) uses the C3 linearisation algorithm to determine the order in which base classes are searched.

| `class Flyable:` |
| :---- |
|     `def move(self) -> str:` |
|         `return "Flying"` |
|  |
| `class Swimmable:` |
|     `def move(self) -> str:` |
|         `return "Swimming"` |
|  |
| `class Duck(Flyable, Swimmable):` |
|     `pass` |
|  |
| `d = Duck()` |
| `print(d.move())         # Flying  (Flyable is first in MRO)` |
| `print(Duck.__mro__)` |
| `# (<class 'Duck'>, <class 'Flyable'>, <class 'Swimmable'>, ...)` |

# **6\. Polymorphism**

Polymorphism lets you write code that works with objects of different types through a common interface.

## **▸ Method Overriding**

| `class Shape:` |
| :---- |
|     `def area(self) -> float:` |
|         `raise NotImplementedError` |
|  |
|     `def describe(self) -> str:` |
|         `return f"{type(self).__name__} with area={self.area():.2f}"` |
|  |
|  |
| `class Circle(Shape):` |
|     `def __init__(self, radius: float):` |
|         `self.radius = radius` |
|  |
|     `def area(self) -> float:` |
|         `import math` |
|         `return math.pi * self.radius ** 2` |
|  |
|  |
| `class Rectangle(Shape):` |
|     `def __init__(self, w: float, h: float):` |
|         `self.w, self.h = w, h` |
|  |
|     `def area(self) -> float:` |
|         `return self.w * self.h` |
|  |
|  |
| `shapes = [Circle(5), Rectangle(4, 6)]` |
| `for s in shapes:` |
|     `print(s.describe())` |
| `# Circle with area=78.54` |
| `# Rectangle with area=24.00` |

## **▸ Duck Typing**

Python is dynamically typed — if an object has the required attributes/methods, it can be used regardless of its class. This is 'duck typing'.

| `class PDF:` |
| :---- |
|     `def render(self): return 'Rendering PDF'` |
|  |
| `class Image:` |
|     `def render(self): return 'Rendering Image'` |
|  |
| `class Video:` |
|     `def render(self): return 'Rendering Video'` |
|  |
| `def display(content):` |
|     `print(content.render())   # works for any object with render()` |
|  |
| `for item in [PDF(), Image(), Video()]:` |
|     `display(item)` |

## **▸ Operator Overloading**

Python lets you define how operators (+, \-, \*, \==, etc.) behave for your custom classes using dunder methods.

| `class Vector:` |
| :---- |
|     `def __init__(self, x: float, y: float):` |
|         `self.x, self.y = x, y` |
|  |
|     `def __add__(self, other: 'Vector') -> 'Vector':` |
|         `return Vector(self.x + other.x, self.y + other.y)` |
|  |
|     `def __mul__(self, scalar: float) -> 'Vector':` |
|         `return Vector(self.x * scalar, self.y * scalar)` |
|  |
|     `def __eq__(self, other) -> bool:` |
|         `return self.x == other.x and self.y == other.y` |
|  |
|     `def __abs__(self) -> float:` |
|         `return (self.x**2 + self.y**2) ** 0.5` |
|  |
|     `def __repr__(self) -> str:` |
|         `return f"Vector({self.x}, {self.y})"` |
|  |
|  |
| `v1 = Vector(1, 2)` |
| `v2 = Vector(3, 4)` |
| `print(v1 + v2)     # Vector(4, 6)` |
| `print(v1 * 3)      # Vector(3, 6)` |
| `print(abs(v2))     # 5.0` |

# **7\. Abstraction**

Abstraction hides implementation details behind a clean interface. Python's abc module provides Abstract Base Classes (ABCs) for this purpose.

## **▸ Abstract Base Classes**

| `from abc import ABC, abstractmethod` |
| :---- |
|  |
| `class PaymentGateway(ABC):` |
|     `"""Abstract interface for payment gateways."""` |
|  |
|     `@abstractmethod` |
|     `def charge(self, amount: float) -> bool: ...` |
|  |
|     `@abstractmethod` |
|     `def refund(self, transaction_id: str) -> bool: ...` |
|  |
|     `def process(self, amount: float) -> str:` |
|         `"""Template method — uses abstract charge()."""` |
|         `if self.charge(amount):` |
|             `return f"Charged £{amount:.2f} via {type(self).__name__}"` |
|         `return "Payment failed"` |
|  |
|  |
| `class StripeGateway(PaymentGateway):` |
|     `def charge(self, amount: float) -> bool:` |
|         `# ... Stripe API call ...` |
|         `return True` |
|  |
|     `def refund(self, transaction_id: str) -> bool:` |
|         `return True` |
|  |
|  |
| `# PaymentGateway()       # TypeError: Can't instantiate abstract class` |
| `gw = StripeGateway()` |
| `print(gw.process(99.99))` |

# **8\. Special (Dunder) Methods**

Dunder (double-underscore) methods give your classes Pythonic behaviour — enabling them to work with built-in functions, operators, and language constructs.

## **▸ Common Dunder Methods**

| `class Book:` |
| :---- |
|     `def __init__(self, title: str, author: str, pages: int):` |
|         `self.title  = title` |
|         `self.author = author` |
|         `self.pages  = pages` |
|  |
|     `# str() and print()` |
|     `def __str__(self) -> str:` |
|         `return f'"{self.title}" by {self.author}'` |
|  |
|     `# repr() — developer-facing` |
|     `def __repr__(self) -> str:` |
|         `return f"Book({self.title!r}, {self.author!r}, {self.pages})"` |
|  |
|     `# len(book)` |
|     `def __len__(self) -> int:` |
|         `return self.pages` |
|  |
|     `# book1 < book2` |
|     `def __lt__(self, other: 'Book') -> bool:` |
|         `return self.pages < other.pages` |
|  |
|     `# book1 == book2` |
|     `def __eq__(self, other) -> bool:` |
|         `return self.title == other.title and self.author == other.author` |
|  |
|     `# book[idx] — slicing chapters, etc.` |
|     `def __getitem__(self, idx):` |
|         `return f"Chapter {idx}"` |
|  |
|     `# with Book(...) as b:` |
|     `def __enter__(self): return self` |
|     `def __exit__(self, *args): pass` |
|  |
|  |
| `b1 = Book("Dune", "Herbert", 412)` |
| `b2 = Book("Foundation", "Asimov", 244)` |
| `print(str(b1))     # "Dune" by Herbert` |
| `print(len(b1))     # 412` |
| `print(b1 > b2)     # True` |
| `print(sorted([b1, b2]))` |

# **9\. Class Methods, Static Methods & Properties**

## **▸ Method Types Compared**

| `class Pizza:` |
| :---- |
|     `_tax_rate = 0.1` |
|  |
|     `def __init__(self, toppings: list, price: float):` |
|         `self.toppings = toppings` |
|         `self.price    = price` |
|  |
|     `# ---------- Instance method (access self) ----------` |
|     `def total(self) -> float:` |
|         `return self.price * (1 + Pizza._tax_rate)` |
|  |
|     `# ---------- Class method (access cls) ----------` |
|     `@classmethod` |
|     `def margherita(cls) -> 'Pizza':` |
|         `"""Alternative constructor / factory."""` |
|         `return cls(['tomato', 'mozzarella'], 8.00)` |
|  |
|     `@classmethod` |
|     `def set_tax(cls, rate: float):` |
|         `cls._tax_rate = rate` |
|  |
|     `# ---------- Static method (no self or cls) ----------` |
|     `@staticmethod` |
|     `def is_valid_topping(topping: str) -> bool:` |
|         `allowed = {'cheese', 'tomato', 'mushroom', 'pepperoni', 'mozzarella'}` |
|         `return topping in allowed` |
|  |
|  |
| `p = Pizza.margherita()` |
| `print(p.total())                  # 8.8` |
| `print(Pizza.is_valid_topping('ham'))  # False` |

# **10\. Dataclasses**

The @dataclass decorator (Python 3.7+) auto-generates \_\_init\_\_, \_\_repr\_\_, \_\_eq\_\_, and more, reducing boilerplate for data-holding classes.

## **▸ Basic and Advanced Dataclasses**

| `from dataclasses import dataclass, field, KW_ONLY` |
| :---- |
| `from typing import ClassVar` |
|  |
| `@dataclass(order=True, frozen=True)` |
| `class Point:` |
|     `x: float` |
|     `y: float` |
|  |
|     `def distance_from_origin(self) -> float:` |
|         `return (self.x**2 + self.y**2) ** 0.5` |
|  |
|  |
| `@dataclass` |
| `class Student:` |
|     `name: str` |
|     `grade: int` |
|     `scores: list = field(default_factory=list)  # mutable default` |
|     `_: KW_ONLY                                  # all below are keyword-only` |
|     `scholarship: bool = False` |
|     `_student_count: ClassVar[int] = 0           # class var, not instance field` |
|  |
|     `def __post_init__(self):` |
|         `Student._student_count += 1` |
|         `if not (1 <= self.grade <= 12):` |
|             `raise ValueError("Grade must be 1-12")` |
|  |
|  |
| `p1 = Point(3, 4)` |
| `print(p1.distance_from_origin())   # 5.0` |
|  |
| `alice = Student("Alice", 11, scholarship=True)` |
| `alice.scores.extend([95, 88, 92])` |
| `print(alice)` |

# **11\. Design Patterns in Python**

Design patterns are reusable solutions to common software design problems. The following covers the most widely used patterns.

## **▸ Singleton Pattern**

Ensures a class has only one instance throughout the application lifecycle.

| `class Singleton:` |
| :---- |
|     `_instance = None` |
|  |
|     `def __new__(cls, *args, **kwargs):` |
|         `if cls._instance is None:` |
|             `cls._instance = super().__new__(cls)` |
|         `return cls._instance` |
|  |
|     `def __init__(self, value: int = 0):` |
|         `if not hasattr(self, '_initialised'):` |
|             `self.value = value` |
|             `self._initialised = True` |
|  |
|  |
| `a = Singleton(42)` |
| `b = Singleton(99)` |
| `print(a is b)        # True` |
| `print(a.value)       # 42 (not overwritten)` |

## **▸ Factory Pattern**

Creates objects without specifying the exact class at instantiation time, delegating that decision to a factory method.

| `class Logger:` |
| :---- |
|     `def log(self, msg: str): ...` |
|  |
| `class FileLogger(Logger):` |
|     `def log(self, msg): print(f"[FILE] {msg}")` |
|  |
| `class ConsoleLogger(Logger):` |
|     `def log(self, msg): print(f"[CONSOLE] {msg}")` |
|  |
| `class CloudLogger(Logger):` |
|     `def log(self, msg): print(f"[CLOUD] {msg}")` |
|  |
|  |
| `class LoggerFactory:` |
|     `_registry = {` |
|         `'file':    FileLogger,` |
|         `'console': ConsoleLogger,` |
|         `'cloud':   CloudLogger,` |
|     `}` |
|  |
|     `@classmethod` |
|     `def create(cls, kind: str) -> Logger:` |
|         `if kind not in cls._registry:` |
|             `raise ValueError(f"Unknown logger: {kind}")` |
|         `return cls._registry[kind]()` |
|  |
|  |
| `logger = LoggerFactory.create('cloud')` |
| `logger.log('Deployed!')     # [CLOUD] Deployed!` |

## **▸ Observer Pattern**

Defines a one-to-many dependency so that when one object changes state, all its dependents are notified automatically.

| `from typing import Callable` |
| :---- |
|  |
| `class EventEmitter:` |
|     `def __init__(self):` |
|         `self._listeners: dict[str, list[Callable]] = {}` |
|  |
|     `def on(self, event: str, callback: Callable):` |
|         `self._listeners.setdefault(event, []).append(callback)` |
|  |
|     `def emit(self, event: str, *args, **kwargs):` |
|         `for cb in self._listeners.get(event, []):` |
|             `cb(*args, **kwargs)` |
|  |
|  |
| `class StockMarket(EventEmitter):` |
|     `def __init__(self):` |
|         `super().__init__()` |
|         `self._prices: dict[str, float] = {}` |
|  |
|     `def update(self, ticker: str, price: float):` |
|         `self._prices[ticker] = price` |
|         `self.emit('price_change', ticker, price)` |
|  |
|  |
| `market = StockMarket()` |
| `market.on("price_change", lambda t, p: print(f"{t}: £{p:.2f}"))` |
| `market.update("AAPL", 189.45)` |
| `market.update("TSLA", 245.00)` |

## **▸ Decorator Pattern**

Adds behaviour to objects dynamically without altering their class.

| `import time` |
| :---- |
| `import functools` |
|  |
| `def timer(func):` |
|     `""" Decorator that measures execution time. """` |
|     `@functools.wraps(func)` |
|     `def wrapper(*args, **kwargs):` |
|         `start = time.perf_counter()` |
|         `result = func(*args, **kwargs)` |
|         `elapsed = time.perf_counter() - start` |
|         `print(f"{func.__name__} took {elapsed:.4f}s")` |
|         `return result` |
|     `return wrapper` |
|  |
| `def retry(times: int = 3):` |
|     `"""Decorator factory with configurable retries."""` |
|     `def decorator(func):` |
|         `@functools.wraps(func)` |
|         `def wrapper(*args, **kwargs):` |
|             `for attempt in range(1, times + 1):` |
|                 `try:` |
|                     `return func(*args, **kwargs)` |
|                 `except Exception as e:` |
|                     `print(f"Attempt {attempt} failed: {e}")` |
|             `raise RuntimeError('All attempts failed')` |
|         `return wrapper` |
|     `return decorator` |
|  |
|  |
| `@timer` |
| `@retry(times=3)` |
| `def fetch_data(url: str):` |
|     `import urllib.request` |
|     `return urllib.request.urlopen(url).read()` |

# **12\. Metaclasses**

Metaclasses are the 'classes of classes' — they define how a class itself is created and can modify class definitions at creation time.

## **▸ Custom Metaclass**

| `class ValidatedMeta(type):` |
| :---- |
|     `"""Metaclass that enforces required class attributes."""` |
|  |
|     `REQUIRED = ('name', 'version')` |
|  |
|     `def __new__(mcs, cls_name, bases, namespace):` |
|         `for attr in mcs.REQUIRED:` |
|             `if attr not in namespace:` |
|                 `raise TypeError(` |
|                     `f"Class {cls_name!r} must define {attr!r}"` |
|                 `)` |
|         `return super().__new__(mcs, cls_name, bases, namespace)` |
|  |
|  |
| `class Plugin(metaclass=ValidatedMeta):` |
|     `name    = "base_plugin"` |
|     `version = "1.0"` |
|  |
|     `def run(self): ...` |
|  |
|  |
| `class MyPlugin(Plugin):` |
|     `name    = "my_plugin"` |
|     `version = "2.1"` |
|  |
|     `def run(self):` |
|         `print(f"Running {self.name} v{self.version}")` |
|  |
|  |
| `MyPlugin().run()` |
| `# Running my_plugin v2.1` |

# **13\. Descriptors**

Descriptors are objects that define how attribute access is handled via \_\_get\_\_, \_\_set\_\_, and \_\_delete\_\_. Properties, classmethods, and staticmethods are all implemented as descriptors internally.

## **▸ Custom Descriptor**

| `class TypedAttribute:` |
| :---- |
|     `"""Descriptor that enforces type on assignment."""` |
|  |
|     `def __init__(self, expected_type: type):` |
|         `self.expected_type = expected_type` |
|         `self.attr_name     = None` |
|  |
|     `def __set_name__(self, owner, name):` |
|         `self.attr_name = f'_{name}'` |
|  |
|     `def __get__(self, obj, objtype=None):` |
|         `if obj is None: return self` |
|         `return getattr(obj, self.attr_name, None)` |
|  |
|     `def __set__(self, obj, value):` |
|         `if not isinstance(value, self.expected_type):` |
|             `raise TypeError(` |
|                 `f"{self.attr_name!r} expects {self.expected_type.__name__}, got {type(value).__name__}"` |
|             `)` |
|         `setattr(obj, self.attr_name, value)` |
|  |
|  |
| `class Person:` |
|     `name = TypedAttribute(str)` |
|     `age  = TypedAttribute(int)` |
|  |
|     `def __init__(self, name: str, age: int):` |
|         `self.name = name` |
|         `self.age  = age` |
|  |
|  |
| `p = Person("Alice", 30)` |
| `print(p.name, p.age)     # Alice 30` |
| `p.age = "old"            # TypeError!` |

# **14\. Mixins**

Mixins are small, focused classes that provide specific functionality to be mixed into other classes through multiple inheritance. They shouldn't stand alone as base classes.

| `import json` |
| :---- |
|  |
| `class JSONMixin:` |
|     `def to_json(self) -> str:` |
|         `return json.dumps(self.__dict__, default=str)` |
|  |
|     `@classmethod` |
|     `def from_json(cls, data: str):` |
|         `return cls(**json.loads(data))` |
|  |
|  |
| `class LogMixin:` |
|     `def log(self, msg: str):` |
|         `print(f"[{type(self).__name__}] {msg}")` |
|  |
|  |
| `class ComparableMixin:` |
|     `def __eq__(self, other) -> bool:` |
|         `return self.__dict__ == other.__dict__` |
|  |
|     `def __lt__(self, other) -> bool:` |
|         `return list(self.__dict__.values()) < list(other.__dict__.values())` |
|  |
|  |
| `class Product(JSONMixin, LogMixin, ComparableMixin):` |
|     `def __init__(self, name: str, price: float):` |
|         `self.name  = name` |
|         `self.price = price` |
|  |
|  |
| `p = Product("Widget", 9.99)` |
| `p.log('Created')              # [Product] Created` |
| `print(p.to_json())` |
| `# {"name": "Widget", "price": 9.99}` |
|  |
| `q = Product.from_json(p.to_json())` |
| `print(p == q)    # True` |

# **15\. Context Managers**

Context managers manage resources (files, connections, locks) cleanly via the with statement. Implement them using \_\_enter\_\_/\_\_exit\_\_ or contextlib.

## **▸ Class-Based Context Manager**

| `import threading` |
| :---- |
|  |
| `class ManagedConnection:` |
|     `def __init__(self, host: str, port: int):` |
|         `self.host = host` |
|         `self.port = port` |
|         `self.conn = None` |
|  |
|     `def __enter__(self):` |
|         `print(f"Connecting to {self.host}:{self.port}")` |
|         `# self.conn = create_connection(self.host, self.port)` |
|         `return self` |
|  |
|     `def __exit__(self, exc_type, exc_val, exc_tb):` |
|         `# if exc_type: handle exception` |
|         `print('Connection closed')` |
|         `return False   # don't suppress exceptions` |
|  |
|  |
| `with ManagedConnection('db.example.com', 5432) as conn:` |
|     `pass  # use conn here` |

## **▸ Generator-Based Context Manager**

| `from contextlib import contextmanager` |
| :---- |
| `import time` |
|  |
| `@contextmanager` |
| `def timed_block(label: str):` |
|     `start = time.perf_counter()` |
|     `try:` |
|         `yield` |
|     `finally:` |
|         `elapsed = time.perf_counter() - start` |
|         `print(f"{label}: {elapsed:.4f}s")` |
|  |
|  |
| `with timed_block('Data processing'):` |
|     `total = sum(range(1_000_000))` |
|     `print(total)` |

# **16\. Protocols and Structural Subtyping**

Python 3.8+ introduced typing. Protocol for structural subtyping — classes that implement certain methods satisfy a Protocol without explicit inheritance (similar to Go interfaces).

| `from typing import Protocol, runtime_checkable` |
| :---- |
|  |
| `@runtime_checkable` |
| `class Drawable(Protocol):` |
|     `def draw(self) -> None: ...` |
|     `def resize(self, factor: float) -> None: ...` |
|  |
|  |
| `class Circle:` |
|     `def __init__(self, r: float): self.r = r` |
|     `def draw(self): print(f"Drawing circle r={self.r}")` |
|     `def resize(self, f: float): self.r *= f` |
|  |
| `class Square:` |
|     `def __init__(self, s: float): self.s = s` |
|     `def draw(self): print(f"Drawing square s={self.s}")` |
|     `def resize(self, f: float): self.s *= f` |
|  |
|  |
| `def render(item: Drawable):` |
|     `item.draw()` |
|  |
| `render(Circle(5))     # works — structurally satisfies Drawable` |
| `render(Square(3))     # works — no inheritance needed` |
|  |
| `print(isinstance(Circle(1), Drawable))   # True` |

# **17\. \_\_slots\_\_ for Memory Optimisation**

By default, Python stores instance attributes in a \_\_dict\_\_. Using \_\_slots\_\_ replaces this with a fixed-size array, significantly reducing memory usage for classes with many instances.

| `class PointWithDict:` |
| :---- |
|     `def __init__(self, x, y):` |
|         `self.x, self.y = x, y` |
|  |
|  |
| `class PointWithSlots:` |
|     `__slots__ = ('x', 'y')` |
|  |
|     `def __init__(self, x, y):` |
|         `self.x, self.y = x, y` |
|  |
|  |
| `import sys` |
| `p1 = PointWithDict(1.0, 2.0)` |
| `p2 = PointWithSlots(1.0, 2.0)` |
|  |
| `print(sys.getsizeof(p1.__dict__))   # ~232 bytes` |
| `# p2.__dict__                       # AttributeError — no __dict__` |
|  |
| `# Memory for 1M points:` |
| `# PointWithDict:   ~350 MB` |
| `# PointWithSlots:  ~56 MB  (~6x savings)` |
|  |
| `# LIMITATION: cannot add arbitrary attributes` |
| `# p2.z = 3.0     # AttributeError` |

# **18\. SOLID Principles**

SOLID is a set of five design principles that guide writing maintainable, scalable OOP code.

## **▸ S — Single Responsibility Principle**

A class should have only one reason to change.

| `# BAD — UserManager does too much` |
| :---- |
| `class UserManager:` |
|     `def create_user(self, name): ...` |
|     `def send_email(self, user): ...   # email concern` |
|     `def save_to_db(self, user): ...   # persistence concern` |
|  |
| `# GOOD — each class has one responsibility` |
| `class UserService:` |
|     `def create_user(self, name): ...` |
|  |
| `class EmailService:` |
|     `def send_welcome(self, user): ...` |
|  |
| `class UserRepository:` |
|     `def save(self, user): ...` |

## **▸ O — Open/Closed Principle**

Open for extension, closed for modification.

| `from abc import ABC, abstractmethod` |
| :---- |
|  |
| `class Discount(ABC):` |
|     `@abstractmethod` |
|     `def apply(self, price: float) -> float: ...` |
|  |
| `class NoDiscount(Discount):` |
|     `def apply(self, price): return price` |
|  |
| `class PercentageDiscount(Discount):` |
|     `def __init__(self, pct): self.pct = pct` |
|     `def apply(self, price): return price * (1 - self.pct / 100)` |
|  |
| `class SeasonalDiscount(Discount):` |
|     `def apply(self, price): return price * 0.75` |
|  |
| `# Add new discount types without modifying existing code` |
| `def checkout(price: float, discount: Discount) -> float:` |
|     `return discount.apply(price)` |

## **▸ L — Liskov Substitution Principle**

Objects of a subclass should be replaceable for their parent class without breaking the programme.

| `class Rectangle:` |
| :---- |
|     `def __init__(self, w, h): self.w, self.h = w, h` |
|     `def area(self): return self.w * self.h` |
|  |
| `# BAD — Square violates LSP if it overrides setters inconsistently` |
| `# GOOD — use composition or separate hierarchy instead` |
| `class Square:` |
|     `def __init__(self, side): self.side = side` |
|     `def area(self): return self.side ** 2` |

## **▸ I — Interface Segregation Principle**

Clients should not be forced to depend on methods they don't use. Prefer small, focused interfaces.

| `# BAD — fat interface` |
| :---- |
| `class Worker(ABC):` |
|     `@abstractmethod` |
|     `def work(self): ...` |
|     `@abstractmethod` |
|     `def eat(self): ...    # robots don't eat!` |
|  |
| `# GOOD — segregated interfaces` |
| `class Workable(Protocol):` |
|     `def work(self) -> None: ...` |
|  |
| `class Eatable(Protocol):` |
|     `def eat(self) -> None: ...` |
|  |
| `class Human:` |
|     `def work(self): print("Working")` |
|     `def eat(self):  print("Eating")` |
|  |
| `class Robot:` |
|     `def work(self): print("Beep boop, working")` |
|     `# no eat() needed` |

## **▸ D — Dependency Inversion Principle**

High-level modules should not depend on low-level modules. Both should depend on abstractions.

| `class Database(Protocol):` |
| :---- |
|     `def save(self, data: dict) -> None: ...` |
|     `def find(self, id: int) -> dict: ...` |
|  |
| `class PostgresDB:` |
|     `def save(self, data): ...` |
|     `def find(self, id): ...` |
|  |
| `class MockDB:` |
|     `def __init__(self): self._store = {}` |
|     `def save(self, data): self._store[data['id']] = data` |
|     `def find(self, id): return self._store.get(id)` |
|  |
| `class UserService:` |
|     `def __init__(self, db: Database):   # depends on abstraction` |
|         `self._db = db` |
|  |
|     `def register(self, user: dict):` |
|         `self._db.save(user)` |
|  |
| `# Easily swap implementations` |
| `svc = UserService(MockDB())` |
| `svc.register({"id": 1, "name": "Alice"})` |

# **19\. Advanced Class Hooks**

## **▸ \_\_init\_subclass\_\_**

Called on the parent class when a subclass is created — useful for plugin registration and validation.

| `class Plugin:` |
| :---- |
|     `_registry: dict[str, type] = {}` |
|  |
|     `def __init_subclass__(cls, plugin_name: str, **kwargs):` |
|         `super().__init_subclass__(**kwargs)` |
|         `Plugin._registry[plugin_name] = cls` |
|         `print(f"Registered plugin: {plugin_name}")` |
|  |
|  |
| `class AudioPlugin(Plugin, plugin_name='audio'):` |
|     `def process(self): return "Processing audio"` |
|  |
| `class VideoPlugin(Plugin, plugin_name='video'):` |
|     `def process(self): return "Processing video"` |
|  |
|  |
| `print(Plugin._registry)` |
| `# {'audio': <AudioPlugin>, 'video': <VideoPlugin>}` |
|  |
| `plugin = Plugin._registry['audio']()` |
| `print(plugin.process())` |

## **▸ \_\_class\_getitem\_\_ and Generics**

| `from __future__ import annotations` |
| :---- |
| `from typing import Generic, TypeVar` |
|  |
| `T = TypeVar('T')` |
|  |
| `class Stack(Generic[T]):` |
|     `def __init__(self):` |
|         `self._items: list[T] = []` |
|  |
|     `def push(self, item: T) -> None:` |
|         `self._items.append(item)` |
|  |
|     `def pop(self) -> T:` |
|         `return self._items.pop()` |
|  |
|     `def peek(self) -> T:` |
|         `return self._items[-1]` |
|  |
|     `def __len__(self) -> int:` |
|         `return len(self._items)` |
|  |
|     `def __repr__(self) -> str:` |
|         `return f"Stack({self._items})"` |
|  |
|  |
| `s: Stack[int] = Stack()` |
| `s.push(1); s.push(2); s.push(3)` |
| `print(s.pop())    # 3` |
| `print(s.peek())   # 2` |

# **20\. Quick Reference Cheat Sheet**

## **▸ Dunder Method Summary**

| Method | Trigger | Example |
| :---- | :---- | :---- |
| `__init__` | obj \= MyClass() | Constructor |
| `__str__` | str(obj) / print(obj) | Human-readable string |
| `__repr__` | repr(obj) | Developer string |
| `__len__` | len(obj) | Length |
| `__getitem__` | obj\[key\] | Indexing |
| `__setitem__` | obj\[key\] \= val | Index assignment |
| `__contains__` | x in obj | Membership test |
| `__iter__` | for x in obj | Iteration |
| `__next__` | next(obj) | Iterator protocol |
| `__add__` | obj \+ other | Addition |
| `__eq__` | obj \== other | Equality |
| `__lt__` | obj \< other | Less-than |
| `__enter__` | with obj as x: | Context manager entry |
| `__exit__` | end of with block | Context manager exit |
| `__call__` | obj() | Callable instance |
| `__del__` | del obj | Cleanup/destructor |

## **▸ Decorator Quick Reference**

| `@property          # getter` |
| :---- |
| `@x.setter          # setter for property x` |
| `@classmethod       # receives cls; factory / alt constructors` |
| `@staticmethod      # no self or cls; utility function` |
| `@abstractmethod    # must be overridden (requires ABC)` |
| `@dataclass         # auto-generates __init__, __repr__, __eq__` |
| `@functools.wraps   # preserve wrapped function metadata` |
| `@runtime_checkable # allow isinstance() checks on Protocol` |

**End of Guide**

*Happy Coding with Python OOP\! 🐍*