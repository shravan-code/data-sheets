import os

subpages = [
    {
        'id': 'arrays',
        'title': '2. Arrays',
        'icon': 'layout-grid',
        'description': 'Traversal, Two Pointers, Sliding Window, Prefix Sum.',
        'content': """<h2>Understanding Arrays</h2>
<p>An Array is the most fundamental data structure. It stores elements in <strong>contiguous memory locations</strong>, meaning they sit right next to each other in your computer's RAM.</p>

<div class="my-8 p-6 border border-slate-200 dark:border-slate-700 rounded-xl not-prose bg-white dark:bg-slate-900/50">
<div class="mermaid text-center">
graph LR
    subgraph Array
        direction LR
        A["10 (Index 0)"] --- B["20 (Index 1)"] --- C["30 (Index 2)"] --- D["40 (Index 3)"] --- E["50 (Index 4)"]
    end
</div>
</div>

<h3>Core Operations</h3>
<ul>
    <li><strong>Access:</strong> <code>O(1)</code>. Since items are contiguous, we can jump directly to any index.</li>
    <li><strong>Search:</strong> <code>O(N)</code>. In an unsorted array, we must check every element one by one.</li>
    <li><strong>Insertion/Deletion:</strong> <code>O(N)</code>. When you add or remove an item in the middle, you have to shift all subsequent items to make room or close the gap.</li>
</ul>

<h3>Advanced Techniques</h3>
<ul>
    <li><strong>Two Pointers:</strong> Using a <code>left</code> and <code>right</code> pointer that move towards each other. Great for reversing arrays.</li>
    <li><strong>Sliding Window:</strong> Maintaining a "window" of the array and sliding it forward. Perfect for subarray problems.</li>
    <li><strong>Prefix Sum:</strong> Pre-calculating the cumulative sum up to each index.</li>
</ul>

<h3>Python Example: Sliding Window</h3>
<pre><code class="language-python"># Problem: Find the maximum sum of a contiguous subarray of size K
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
        
    return max_sum

print(max_sum_subarray([2, 1, 5, 1, 3, 2], 3)) # Output: 9
</code></pre>"""
    },
    {
        'id': 'binary-search',
        'title': '8. Binary Search',
        'icon': 'search',
        'description': 'Search on sorted array, find first & last position.',
        'content': """<h2>Binary Search</h2>
<p>Binary Search is a remarkably efficient algorithm for finding an item from a <strong>sorted</strong> list of items. It works by repeatedly dividing in half the portion of the list that could contain the item.</p>

<div class="my-8 p-6 bg-slate-100 dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-700">
    <h3 class="font-bold mb-2">Requirement: Sorted Data</h3>
    <p class="text-sm">Binary Search ONLY works if your data is already sorted. If not, the "divide and conquer" logic fails.</p>
</div>

<h3>Core Concepts</h3>
<ul>
    <li><strong>Midpoint:</strong> Calculated as <code>(left + right) // 2</code>.</li>
    <li><strong>Divide & Conquer:</strong> Each step eliminates half of the remaining elements.</li>
    <li><strong>Time Complexity:</strong> O(log N). Incredibly fast for massive datasets.</li>
</ul>

<h3>Python Example: Binary Search</h3>
<pre><code class="language-python">def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: left = mid + 1
        else: right = mid - 1
    return -1
</code></pre>"""
    },
    {
        'id': 'complexity-analysis',
        'title': '1. Complexity Analysis',
        'icon': 'bar-chart',
        'description': 'Big O Notation (Time & Space), how to analyze loops & recursion.',
        'content': """<h2>Understanding Complexity</h2>
<p>Complexity analysis is the tool we use to measure how well an algorithm scales. As your data grows from 100 rows to 100 million rows, will your code still run in milliseconds, or will it take hours?</p>

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-8 not-prose">
    <div class="p-6 bg-amber-50 dark:bg-amber-900/20 border border-amber-100 dark:border-amber-800 rounded-xl">
        <h3 class="font-bold text-amber-800 dark:text-amber-400">Time Complexity</h3>
        <p class="text-sm text-slate-600 dark:text-slate-400 mt-2">How the number of <strong>operations</strong> increases as the input size (N) grows.</p>
    </div>
    <div class="p-6 bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800 rounded-xl">
        <h3 class="font-bold text-blue-800 dark:text-blue-400">Space Complexity</h3>
        <p class="text-sm text-slate-600 dark:text-slate-400 mt-2">How much <strong>extra memory</strong> the algorithm needs as the input size (N) grows.</p>
    </div>
</div>

<h3>Core Concepts</h3>
<ul>
    <li><strong>Worst Case (O):</strong> The maximum time an algorithm could take. We optimize for this to ensure reliability.</li>
    <li><strong>Average Case (Θ):</strong> The expected time taken over all possible inputs.</li>
    <li><strong>Big O Hierarchy:</strong> O(1) < O(log N) < O(N) < O(N log N) < O(N²).</li>
</ul>

<h3>Python Example: Linear vs Quadratic</h3>
<pre><code class="language-python"># O(N) Time: Linear scan (Efficiency)
def find_max(arr):
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val

# O(N^2) Time: Nested loops (Inefficiency)
def print_pairs(arr):
    for i in arr:
        for j in arr:
            print(i, j)
</code></pre>"""
    },
    {
        'id': 'graphs',
        'title': '12. Graphs',
        'icon': 'share-2',
        'description': 'What is a Graph, BFS, DFS, and Cycle Detection.',
        'content': """<h2>Understanding Graphs</h2>
<p>A Graph is a network of <strong>Nodes (Vertices)</strong> connected by <strong>Edges</strong>.</p>

<div class="my-8">
<div class="mermaid">
graph LR
    A((A)) --- B((B))
    B --- C((C))
    A --- C
    C --> D((D))
</div>
</div>

<h3>Core Anatomy</h3>
<ul>
    <li><strong>Vertex:</strong> A single node in the graph.</li>
    <li><strong>Edge:</strong> The connection between two vertices.</li>
    <li><strong>Directed vs Undirected:</strong> Does the edge have a direction (like a follow) or is it mutual (like a friend)?</li>
</ul>

<h3>Representation</h3>
<p>Graphs are usually stored as an <strong>Adjacency List</strong> (a dictionary where keys are nodes and values are lists of neighbors).</p>

<h3>Python Example: Simple DFS</h3>
<pre><code class="language-python">def dfs(graph, node, visited=set()):
    if node not in visited:
        print(node)
        visited.add(node)
        for neighbor in graph[node]:
            dfs(graph, neighbor, visited)
</code></pre>"""
    },
    {
        'id': 'hashing',
        'title': '4. Hashing',
        'icon': 'hash',
        'description': 'HashMap, HashSet, Frequency Count, Two-Sum Pattern.',
        'content': """<h2>HashMap & HashSet</h2>
<p>A <strong>HashMap</strong> stores Key-Value pairs. It uses a mathematical hashing function to turn a key into an index, allowing for instant <code>O(1)</code> lookups. A <strong>HashSet</strong> is like a HashMap but only stores unique keys.</p>

<div class="my-8">
<div class="mermaid text-center">
flowchart LR
    Key["Key: 'apple'"] --> HashFunction(Hash Function)
    HashFunction --> Index[Index: 3]
    Index --> Memory[Bucket 3: Value=50]
</div>
</div>

<h3>Core Concepts</h3>
<ul>
    <li><strong>Hashing:</strong> The process of converting a key into a fixed-size integer.</li>
    <li><strong>Collision:</strong> When two different keys result in the same hash. Modern dictionaries handle this automatically.</li>
    <li><strong>O(1) Lookups:</strong> Finding data in a hash map doesn't depend on how many items are in it.</li>
</ul>

<h3>The Two-Sum Pattern</h3>
<pre><code class="language-python"># Problem: Find indices of two numbers that add up to target
def two_sum(nums, target):
    seen = {} # Number: Index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

print(two_sum([2, 7, 11, 15], 9)) # Output: [0, 1]
</code></pre>"""
    },
    {
        'id': 'heap',
        'title': '13. Heap',
        'icon': 'pyramid',
        'description': 'Min Heap & Max Heap concept, Top-K Elements.',
        'content': """<h2>Understanding Heaps</h2>
<p>A Heap is a tree-based data structure that satisfies the <strong>Heap Property</strong>. It is primarily used for priority-based tasks.</p>

<div class="my-8">
<div class="mermaid">
graph TD
    A((Min: 1)) --> B((3))
    A --> C((6))
    B --> D((5))
    B --> E((9))
</div>
</div>

<h3>Core Concepts</h3>
<ul>
    <li><strong>Min Heap:</strong> Smallest element is at the Root.</li>
    <li><strong>Max Heap:</strong> Largest element is at the Root.</li>
    <li><strong>Heapify:</strong> The process of rearranging a tree to satisfy the heap property.</li>
    <li><strong>Extract Min/Max:</strong> Removing the root and "re-heapifying" the tree in O(log N).</li>
</ul>

<h3>Python Example: Finding Top-K Largest</h3>
<pre><code class="language-python">import heapq
def k_largest(nums, k):
    return heapq.nlargest(k, nums)

print(k_largest([3, 2, 1, 5, 6, 4], 2)) # [6, 5]
</code></pre>"""
    },
    {
        'id': 'linked-list',
        'title': '7. Linked List',
        'icon': 'link',
        'description': 'Traversal, Reversal, Detect Cycle, Merge Two Sorted Lists.',
        'content': """<h2>Understanding Linked Lists</h2>
<p>Unlike arrays where data is stored contiguously, a Linked List is made of independent <strong>Nodes</strong>. Each node is an object that contains data and a "link" (pointer) to the next object.</p>

<div class="my-8">
<div class="mermaid">
graph LR
    Head[Node: 10] --> Node2[Node: 20]
    Node2 --> Node3[Node: 30]
    Node3 --> Null[None]
</div>
</div>

<h3>Core Anatomy</h3>
<ul>
    <li><strong>Node:</strong> The basic building block containing <code>data</code> and <code>next</code>.</li>
    <li><strong>Head:</strong> The first node in the list. If you lose this, you lose the whole list!</li>
    <li><strong>Pointer:</strong> The memory address of the next node.</li>
</ul>

<h3>What problem does it solve?</h3>
<p>In arrays, inserting at the beginning is slow <code>O(N)</code>. In a Linked List, inserting at the beginning is instant <code>O(1)</code> because you just change a pointer.</p>

<h3>Python Example: Reversing a Linked List</h3>
<pre><code class="language-python">class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev, curr = None, head
    while curr:
        next_node = curr.next
        curr.next = prev # Reverse pointer
        prev, curr = curr, next_node
    return prev
</code></pre>"""
    },
    {
        'id': 'queues',
        'title': '6. Queues',
        'icon': 'list-ordered',
        'description': 'FIFO principle, enqueue, dequeue, and Breadth-First Search.',
        'content': """<h2>Understanding Queues</h2>
<p>A Queue is a collection of elements that follows the <strong>FIFO</strong> (First In, First Out) principle. Think of a line at a coffee shop: you join the back of the line and get served from the front.</p>

<div class="my-8 p-6 border border-slate-200 dark:border-slate-700 rounded-xl not-prose bg-white dark:bg-slate-900/50">
<div class="mermaid text-center">
flowchart LR
    subgraph Queue
        direction LR
        Enqueue["Enqueue (Add)"] --> Back["Back"]
        Back --> Front["Front"]
        Front --> Dequeue["Dequeue (Remove)"]
    end
</div>
</div>

<h3>Core Operations</h3>
<div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-6 not-prose">
    <div class="p-4 bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-100 dark:border-indigo-800 rounded-lg">
        <h4 class="font-bold text-indigo-800 dark:text-indigo-400 text-sm">ENQUEUE</h4>
        <p class="text-xs text-slate-600 dark:text-slate-400 mt-1">Adds an element to the <strong>Back</strong> of the queue.</p>
    </div>
    <div class="p-4 bg-orange-50 dark:bg-orange-900/20 border border-orange-100 dark:border-orange-800 rounded-lg">
        <h4 class="font-bold text-orange-800 dark:text-orange-400 text-sm">DEQUEUE</h4>
        <p class="text-xs text-slate-600 dark:text-slate-400 mt-1">Removes the <strong>Front</strong> element (the one that was there the longest).</p>
    </div>
</div>

<h3>What problem does it solve?</h3>
<p>Queues are used for scheduling and ordering tasks fairly. If multiple users want to print a document, the printer uses a queue. They are also heavily used in web server requests, task scheduling (like Celery/RabbitMQ), and algorithms like Breadth-First Search (BFS).</p>

<h3>Python Example: Basic Queue using Deque</h3>
<p>In Python, while you <em>could</em> use a list, removing from the front of a list is very slow <code>O(N)</code>. Instead, we use <code>collections.deque</code> which makes adding and removing from both ends instant <code>O(1)</code>.</p>
<pre><code class="language-python">from collections import deque

def simulate_printer_queue():
    # Initialize a queue
    printer_queue = deque()
    
    # Enqueue (Add to back)
    print("Adding jobs to queue...")
    printer_queue.append("Job 1: Resume.pdf")
    printer_queue.append("Job 2: Invoice.docx")
    printer_queue.append("Job 3: Photo.png")
    
    # Dequeue (Remove from front)
    print("
Processing jobs:")
    while printer_queue: # While queue is not empty
        current_job = printer_queue.popleft() # O(1) removal
        print(f"Printing -> {current_job}")

simulate_printer_queue()
# Output:
# Printing -> Job 1: Resume.pdf
# Printing -> Job 2: Invoice.docx
# Printing -> Job 3: Photo.png
</code></pre>"""
    },
    {
        'id': 'recursion',
        'title': '10. Recursion',
        'icon': 'repeat',
        'description': 'Base case, Recursive case, Divide & Conquer basics.',
        'content': """<h2>What is Recursion?</h2>
<p>Recursion is a technique where a function <strong>calls itself</strong> to solve smaller versions of the same problem.</p>

<div class="my-8 p-6 bg-slate-100 dark:bg-slate-800/50 rounded-xl not-prose border border-slate-200 dark:border-slate-700">
    <h3 class="font-bold text-slate-900 dark:text-white mb-2">The Two Essential Rules:</h3>
    <ol class="list-decimal pl-5 text-sm text-slate-600 dark:text-slate-400">
        <li><strong>Base Case:</strong> The condition that stops the recursion. Without it, you get a <strong>Stack Overflow</strong>.</li>
        <li><strong>Recursive Case:</strong> The part where the function calls itself with a smaller input.</li>
    </ol>
</div>

<h3>Related Concepts</h3>
<ul>
    <li><strong>Call Stack:</strong> The memory area where your computer tracks the nested function calls.</li>
    <li><strong>Recursive Tree:</strong> A visual map of all the function calls generated.</li>
</ul>

<h3>Python Example: Factorial</h3>
<pre><code class="language-python">def factorial(n):
    if n <= 1: return 1 # Base Case
    return n * factorial(n - 1) # Recursive Case
</code></pre>"""
    },
    {
        'id': 'sorting',
        'title': '9. Sorting',
        'icon': 'sort-asc',
        'description': 'Bubble, Merge, Quick Sort basics and built-in sort usage.',
        'content': """<h2>Sorting Algorithms</h2>
<p>Sorting is the process of arranging data in a specific order. While production code uses built-in sorts, understanding the concepts is vital.</p>

<div class="overflow-x-auto my-6 not-prose">
    <table class="min-w-full text-sm text-left text-slate-600 dark:text-slate-300">
        <thead class="text-xs uppercase bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200">
            <tr>
                <th class="px-6 py-3">Algorithm</th>
                <th class="px-6 py-3">Time</th>
                <th class="px-6 py-3">Stability</th>
            </tr>
        </thead>
        <tbody>
            <tr class="border-b dark:border-slate-800">
                <td class="px-6 py-4 font-bold">Merge Sort</td>
                <td class="px-6 py-4">O(N log N)</td>
                <td class="px-6 py-4">Stable (Preserves order of equal items)</td>
            </tr>
            <tr class="border-b dark:border-slate-800">
                <td class="px-6 py-4 font-bold">Quick Sort</td>
                <td class="px-6 py-4">O(N log N)</td>
                <td class="px-6 py-4">Unstable</td>
            </tr>
        </tbody>
    </table>
</div>

<h3>Core Concepts</h3>
<ul>
    <li><strong>Stability:</strong> Does the sort preserve the relative order of duplicate elements?</li>
    <li><strong>In-place:</strong> Does the sort require extra memory or does it sort within the original array?</li>
    <li><strong>Divide & Conquer:</strong> Breaking the array into single items and merging them back (Merge Sort).</li>
</ul>

<h3>Python Example: Timsort</h3>
<pre><code class="language-python"># Python's built-in sort is highly optimized
nums = [5, 2, 9, 1, 5, 6]
nums.sort() # In-place sort
print(nums) # [1, 2, 5, 5, 6, 9]
</code></pre>"""
    },
    {
        'id': 'stacks',
        'title': '5. Stacks',
        'icon': 'layers',
        'description': 'LIFO principle, push, pop, peek, and valid parentheses problems.',
        'content': """<h2>Understanding Stacks</h2>
<p>A Stack is a collection of elements that follows the <strong>LIFO</strong> (Last In, First Out) principle. Think of a stack of plates: you can only add a plate to the top and take a plate from the top.</p>

<div class="my-8 p-6 border border-slate-200 dark:border-slate-700 rounded-xl not-prose bg-white dark:bg-slate-900/50">
<div class="mermaid text-center">
flowchart TD
    subgraph Stack
        Push["Push (Add)"] --> Top["Top Element"]
        Top --> Pop["Pop (Remove)"]
        Top -.-> Peek["Peek (View)"]
    end
</div>
</div>

<h3>The Three Core Operations</h3>
<div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-6 not-prose">
    <div class="p-4 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-100 dark:border-emerald-800 rounded-lg">
        <h4 class="font-bold text-emerald-800 dark:text-emerald-400 text-sm">PUSH</h4>
        <p class="text-xs text-slate-600 dark:text-slate-400 mt-1">Adds an element to the <strong>Top</strong> of the stack.</p>
    </div>
    <div class="p-4 bg-rose-50 dark:bg-rose-900/20 border border-rose-100 dark:border-rose-800 rounded-lg">
        <h4 class="font-bold text-rose-800 dark:text-rose-400 text-sm">POP</h4>
        <p class="text-xs text-slate-600 dark:text-slate-400 mt-1">Removes the <strong>Top</strong> element and returns it.</p>
    </div>
    <div class="p-4 bg-sky-50 dark:bg-sky-900/20 border border-sky-100 dark:border-sky-800 rounded-lg">
        <h4 class="font-bold text-sky-800 dark:text-sky-400 text-sm">PEEK</h4>
        <p class="text-xs text-slate-600 dark:text-slate-400 mt-1">Looks at the <strong>Top</strong> element without removing it.</p>
    </div>
</div>

<h3>What problem does it solve?</h3>
<p>Stacks are perfect for tracking state that needs to be reversed or unwound. They are the core data structure behind the "Undo" button in text editors, browser history (back button), reversing strings, and verifying matching brackets in compilers.</p>

<h3>Python Example: Valid Parentheses</h3>
<p>In Python, you can just use a standard list <code>[]</code> as a stack using <code>append()</code> and <code>pop()</code>.</p>
<pre><code class="language-python"># Problem: Check if a string of brackets is valid
def is_valid_parentheses(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            # If stack is not empty, pop top element. Else use dummy '#'
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            # It's an opening bracket, push to stack
            stack.append(char)
            
    return not stack # True if stack is empty

print(is_valid_parentheses("{[()]}")) # Output: True
print(is_valid_parentheses("{[(])}")) # Output: False
</code></pre>"""
    },
    {
        'id': 'strings',
        'title': '3. Strings',
        'icon': 'type',
        'description': 'String Manipulation, Palindromes, Anagrams.',
        'content': """<h2>String Manipulation</h2>
<p>A string is essentially an <strong>array of characters</strong>. However, in many modern languages like Python, strings are <strong>immutable</strong>—meaning once they are created, they cannot be changed.</p>

<div class="my-8 p-6 bg-slate-50 dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-700">
    <h3 class="font-bold mb-2">Key Concepts</h3>
    <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
        <li><strong>Immutability:</strong> In Python, <code>s = "Hello"</code> followed by <code>s += "!"</code> actually creates a brand new string in memory.</li>
        <li><strong>Slicing:</strong> Extracting parts of a string (e.g., <code>s[1:4]</code>) is a core operation.</li>
        <li><strong>Character Frequency:</strong> Using HashMaps to count occurrences is the most common interview pattern.</li>
    </ul>
</div>

<h3>Common Patterns</h3>
<ul>
    <li><strong>Palindrome:</strong> A word that reads the same forwards and backwards.</li>
    <li><strong>Anagram:</strong> Two strings containing the exact same characters in any order.</li>
</ul>

<h3>Python Example: Palindrome & Anagram</h3>
<pre><code class="language-python"># Check if a string is a palindrome using Two Pointers
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]: return False
        left, right = left + 1, right - 1
    return True

# Check if two strings are anagrams using Counter
from collections import Counter
def is_anagram(s1, s2):
    return Counter(s1) == Counter(s2)
</code></pre>"""
    },
    {
        'id': 'trees',
        'title': '11. Trees',
        'icon': 'git-merge',
        'description': 'Binary Tree structure, Traversal, BFS and DFS.',
        'content': """<h2>Understanding Trees</h2>
<p>A Tree is a hierarchical data structure consisting of nodes. The topmost node is the <strong>Root</strong>.</p>

<div class="my-8">
<div class="mermaid">
graph TD
    A((Root: 10)) --> B((Child: 5))
    A --> C((Child: 15))
    B --> D((Leaf: 3))
    B --> E((Leaf: 7))
</div>
</div>

<h3>Core Anatomy</h3>
<ul>
    <li><strong>Parent/Child:</strong> A node that points to another is a Parent; the node pointed to is a Child.</li>
    <li><strong>Leaf:</strong> A node with no children (the "ends" of the tree).</li>
    <li><strong>Depth/Height:</strong> Measures of how "deep" or "tall" the tree is.</li>
</ul>

<h3>Tree Traversal</h3>
<ul>
    <li><strong>DFS (Inorder):</strong> Visit Left, Root, Right. Used in Binary Search Trees to get sorted data.</li>
    <li><strong>BFS:</strong> Visit level by level. Used for shortest path in hierarchical structures.</li>
</ul>

<h3>Python Example: Inorder DFS</h3>
<pre><code class="language-python">def inorder(root):
    if not root: return []
    return inorder(root.left) + [root.val] + inorder(root.right)
</code></pre>"""
    },

]

hub_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DSA Roadmap — Data Cake</title>
    <meta name="description" content="Master Data Structures and Algorithms with our 11-phase structured roadmap.">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <style>
        .roadmap-hero-bg {{
            background-image: radial-gradient(circle at 2px 2px, rgba(0,0,0,0.03) 1px, transparent 0);
            background-size: 24px 24px;
        }}
        .dark .roadmap-hero-bg {{
            background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.03) 1px, transparent 0);
        }}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <div id="ds-main-content">
        <main class="relative z-10 pt-24 pb-20 px-6 max-w-5xl mx-auto">
            <!-- HERO -->
            <header class="roadmap-hero-bg mb-20 p-10 md:p-14 rounded-[48px] border-2 border-emerald-100 dark:border-slate-800 bg-white dark:bg-slate-900 relative overflow-hidden shadow-2xl shadow-emerald-500/10">
                <div class="absolute -top-24 -right-24 w-80 h-80 bg-emerald-500/10 blur-[100px] rounded-full"></div>
                <div class="absolute -bottom-24 -left-24 w-80 h-80 bg-emerald-500/5 blur-[100px] rounded-full"></div>
                
                <div class="relative z-10">
                    <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-emerald-100 text-emerald-700 rounded-full text-xs font-black uppercase tracking-widest mb-8 border-2 border-emerald-200/50">
                        <i data-lucide="git-branch-plus" class="w-4 h-4"></i>
                        DSA for Data Engineering
                    </div>
                    <h1 class="font-display text-5xl md:text-7xl font-black text-slate-900 dark:text-white mb-6 tracking-tight leading-[1.1]">
                        DSA <span class="bg-gradient-to-r from-emerald-600 to-emerald-400 bg-clip-text text-transparent">Roadmap</span>
                    </h1>
                    <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl leading-relaxed mb-0 font-medium italic">
                        "Master the algorithms and data structures that power modern data platforms. From complexity analysis to graph algorithms and dynamic programming."
                    </p>
                </div>
            </header>

            <!-- ROADMAP TIMELINE -->
            <div class="max-w-4xl mx-auto">
                {phases_html}
            </div>
        </main>
    </div>
</body>
</html>'''

subpage_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <script>(function(){{
        const s=localStorage.getItem('ds-theme');
        const isL = s==='light';
        if(isL) document.documentElement.classList.remove('dark');
        else document.documentElement.classList.add('dark');
        
        // Immediate Prism theme sync
        window.addEventListener('DOMContentLoaded', () => {{
            const l = document.getElementById('prism-theme-light');
            const d = document.getElementById('prism-theme-dark');
            if(l && d) {{
                l.disabled = !isL;
                d.disabled = isL;
            }}
        }});
    }})();</script>
    <title>{title} — Data Sheets</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        const isDark = document.documentElement.classList.contains('dark');
        mermaid.initialize({{ startOnLoad: true, theme: isDark ? 'dark' : 'default', themeVariables: {{ fontFamily: 'Inter' }} }});
    </script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>

<div class="flex justify-center max-w-[1440px] mx-auto">
    <main class="relative z-10 pt-28 pb-32 px-6 w-full max-w-3xl">
        <a href="../dsa-de.html" class="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm mb-10 no-underline transition-colors duration-200">
            <i data-lucide="arrow-left" class="w-4 h-4"></i>
            Back to DSA
        </a>

        <h1 class="font-display font-bold text-4xl md:text-5xl text-slate-900 dark:text-white mb-4 leading-tight">{title}</h1>
        <p class="text-xl text-slate-600 dark:text-slate-400 mb-12">{description}</p>
        
        <div class="prose prose-slate dark:prose-invert prose-lg max-w-none">
            {content}
        </div>
        
        <div class="mt-20"></div>
    </main>

    <aside class="toc-container">
        <div class="toc-title">On this page</div>
        <ul class="toc-list"></ul>
        {topics_list_html}
    </aside>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
</body>
</html>'''

# 1. Build Hub Page
subpages.sort(key=lambda x: int(x['title'].split('.')[0]))

phases_html = ""
for i, page in enumerate(subpages):
    num = i + 1
    items_html = f"""
    <a href="dsa-de/{page['id']}.html" class="flex items-center gap-3 p-3 bg-emerald-50/30 dark:bg-slate-900 border border-emerald-100/50 dark:border-slate-800 rounded-xl transition-all hover:bg-emerald-50 dark:hover:bg-emerald-900/20 hover:border-emerald-200 group/item no-underline">
        <div class="w-8 h-8 rounded-lg bg-emerald-100 dark:bg-emerald-900/50 flex items-center justify-center text-emerald-600 dark:text-emerald-400 group-hover/item:bg-emerald-600 group-hover/item:text-white transition-all">
            <i data-lucide="{page['icon']}" class="w-4 h-4"></i>
        </div>
        <span class="text-sm font-semibold text-slate-700 dark:text-slate-300 group-hover/item:text-emerald-700 transition-colors">{page['title']}</span>
    </a>"""

    phases_html += f"""
    <div class="relative pl-12 pb-12 group last:pb-0">
        <div class="absolute left-[19px] top-0 bottom-0 w-0.5 bg-slate-200 dark:bg-slate-800 group-last:bottom-auto group-last:h-10"></div>
        <div class="absolute left-0 top-0 w-10 h-10 rounded-full bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 flex items-center justify-center z-10 group-hover:border-emerald-500 transition-colors shadow-sm">
            <span class="text-xs font-bold text-slate-500 group-hover:text-emerald-600">{num:02d}</span>
        </div>

        <div class="bg-white dark:bg-slate-900 border border-slate-200/60 dark:border-slate-800/60 p-6 rounded-3xl transition-all hover:shadow-xl hover:shadow-emerald-500/5">
            <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-6 flex items-center gap-3 font-display">
                {page['title'].split('.', 1)[1].strip() if '.' in page['title'] else page['title']}
                <span class="text-[10px] uppercase tracking-widest px-2 py-1 bg-emerald-100 text-emerald-700 rounded-lg font-bold border border-emerald-200">Phase {num}</span>
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {items_html}
            </div>
        </div>
    </div>"""

hub_content = hub_template.format(phases_html=phases_html)
os.makedirs("pages/learn", exist_ok=True)
with open("pages/learn/dsa-de.html", "w", encoding="utf-8") as f:
    f.write(hub_content)

print("Created Hub: pages/learn/dsa-de.html")

# 2. Build Subpages
os.makedirs("pages/learn/dsa-de", exist_ok=True)
for i, page in enumerate(subpages):
    # Navigation logic
    prev_page = subpages[i-1] if i > 0 else None
    next_page = subpages[i+1] if i < len(subpages)-1 else None

    prev_html = ""
    if prev_page:
        prev_html = f"""
        <a href="{prev_page['id']}.html" class="nav-card prev">
            <span class="nav-label"><i data-lucide="arrow-left"></i> Previous</span>
            <span class="nav-title">{prev_page["title"]}</span>
        </a>"""
        
    next_html = ""
    if next_page:
        next_html = f"""
        <a href="{next_page['id']}.html" class="nav-card next">
            <span class="nav-label">Next <i data-lucide="arrow-right"></i></span>
            <span class="nav-title">{next_page["title"]}</span>
        </a>"""

    # Build list of all topics for the sidebar
    topics_html = '<div class="toc-title mt-8">DSA Topics</div><ul class="toc-list">'
    for p in subpages:
        active_cls = "active" if p['id'] == page['id'] else ""
        topics_html += f'<li><a href="{p["id"]}.html" class="toc-link {active_cls}">{p["title"]}</a></li>'
    topics_html += '</ul>'

    content = subpage_template.format(
        title=page["title"],
        description=page["description"],
        content=page["content"],
        topics_list_html=topics_html
    )

    # Inject Navigation Cards
    nav_html = f"""
    <div class="nav-container">
        {prev_html if prev_html else "<div></div>"}
        {next_html if next_html else "<div></div>"}
    </div>
    """
    content = content.replace('</main>', nav_html + '</main>')

    path = os.path.join("pages", "learn", "dsa-de", f"{page['id']}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Successfully generated all DSA subpages!")
