import os

subpages = [
    {
        "id": "complexity-analysis",
        "title": "1. Complexity Analysis",
        "icon": "bar-chart",
        "description": "Big O Notation (Time & Space), how to analyze loops & recursion.",
        "content": """
<h2>Understanding Complexity</h2>
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
</code></pre>
        """
    },
    {
        "id": "arrays",
        "title": "2. Arrays",
        "icon": "layout-grid",
        "description": "Traversal, Two Pointers, Sliding Window, Prefix Sum.",
        "content": """
<h2>Understanding Arrays</h2>
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
</code></pre>
        """
    },
    {
        "id": "strings",
        "title": "3. Strings",
        "icon": "type",
        "description": "String Manipulation, Palindromes, Anagrams.",
        "content": """
<h2>String Manipulation</h2>
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
</code></pre>
        """
    },
    {
        "id": "hashing",
        "title": "4. Hashing",
        "icon": "hash",
        "description": "HashMap, HashSet, Frequency Count, Two-Sum Pattern.",
        "content": """
<h2>HashMap & HashSet</h2>
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
</code></pre>
        """
    }
]

hub_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>DSA for Data Engineering — Data Sheets</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>
<div class="fixed top-0 left-0 w-96 h-96 bg-violet-600/10 rounded-full blur-3xl pointer-events-none z-0"></div>

<main class="relative z-10 pt-28 pb-20 px-6 max-w-5xl mx-auto">
    <a href="../learn.html" class="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm mb-8 no-underline transition-colors duration-200">
        <i data-lucide="arrow-left" class="w-4 h-4"></i>
        Back to Learn
    </a>

    <div class="flex items-start gap-5 mb-10">
        <div class="w-16 h-16 rounded-xl flex items-center justify-center bg-violet-100 dark:bg-violet-500/20 text-violet-600 dark:text-violet-400">
            <i data-lucide="braces" class="w-8 h-8"></i>
        </div>
        <div>
            <span class="inline-block px-3 py-1 rounded-full text-xs font-semibold mb-2 bg-violet-100 dark:bg-violet-500/20 text-violet-700 dark:text-violet-300">Concepts</span>
            <h1 class="font-display font-bold text-4xl text-slate-900 dark:text-white leading-tight">DSA for Data Engineering</h1>
            <p class="text-slate-600 dark:text-slate-400 mt-2 text-lg">Algorithms and data structures commonly used in data engineering systems and interviews.</p>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {cards_html}
    </div>
</main>
</body>
</html>'''

subpage_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>{title} — Data Sheets</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
    <script src="https://unpkg.com/lucide@latest"></script>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        const isDark = document.documentElement.classList.contains('dark');
        mermaid.initialize({{ startOnLoad: true, theme: isDark ? 'dark' : 'default', themeVariables: {{ fontFamily: 'Inter' }} }});
    </script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>

<main class="relative z-10 pt-28 pb-32 px-6 max-w-3xl mx-auto">
    <a href="../dsa-de.html" class="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm mb-10 no-underline transition-colors duration-200">
        <i data-lucide="arrow-left" class="w-4 h-4"></i>
        Back to DSA
    </a>

    <h1 class="font-display font-bold text-4xl md:text-5xl text-slate-900 dark:text-white mb-4 leading-tight">{title}</h1>
    <p class="text-xl text-slate-600 dark:text-slate-400 mb-12">{description}</p>
    
    <div class="prose prose-slate dark:prose-invert prose-lg max-w-none">
        {content}
    </div>
    
    <div class="mt-20 pt-8 border-t border-slate-200 dark:border-slate-800 flex justify-between">
        <a href="../dsa-de.html" class="inline-flex items-center gap-2 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white no-underline font-medium">
            <i data-lucide="list" class="w-4 h-4"></i> Table of Contents
        </a>
    </div>
</main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
</body>
</html>'''

# 1. Build Hub Page
cards_html = ""
for page in subpages:
    card = f'''
    <a href="dsa-de/{page['id']}.html" class="topic-card block p-6 bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-2xl no-underline group shadow-sm dark:shadow-none hover:border-violet-300 dark:hover:border-violet-500/50">
        <div class="flex items-center justify-between mb-4">
            <div class="w-10 h-10 rounded-lg bg-violet-50 dark:bg-violet-500/10 text-violet-600 dark:text-violet-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                <i data-lucide="{page['icon']}" class="w-5 h-5"></i>
            </div>
            <i data-lucide="arrow-right" class="w-4 h-4 text-slate-300 dark:text-slate-600 group-hover:text-violet-500 group-hover:-translate-x-1 transition-all"></i>
        </div>
        <h3 class="font-display font-semibold text-lg text-slate-900 dark:text-white mb-2">{page["title"]}</h3>
        <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">{page["description"]}</p>
    </a>
    '''
    cards_html += card

hub_content = hub_template.format(cards_html=cards_html)
os.makedirs("pages/learn", exist_ok=True)
with open("pages/learn/dsa-de.html", "w", encoding="utf-8") as f:
    f.write(hub_content)

# 2. Build Subpages
os.makedirs("pages/learn/dsa-de", exist_ok=True)
for page in subpages:
    content = subpage_template.format(
        title=page["title"],
        description=page["description"],
        content=page["content"]
    )
    path = os.path.join("pages", "learn", "dsa-de", f"{page['id']}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Successfully generated all DSA subpages!")
