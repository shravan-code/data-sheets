import os

subpages = [
    {
        "id": "fundamentals",
        "title": "1. Fundamentals",
        "icon": "box",
        "description": "The foundation of architecture: FR, NFR, Estimation, and Metrics.",
        "content": """
<h2>Core Architecture Concepts</h2>
<p>Before diving into specific technologies, we must understand the "why" behind system design. Every architectural decision is a trade-off between competing goals.</p>

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-8 not-prose">
    <div class="p-6 bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800 rounded-xl">
        <h3 class="font-bold text-blue-800 dark:text-blue-400">Functional Requirements (FR)</h3>
        <p class="text-sm text-slate-600 dark:text-slate-400 mt-2">The specific behaviors of the system. "What the system does."</p>
        <ul class="text-xs mt-3 space-y-1 text-slate-500">
            <li>• User can search for products</li>
            <li>• System sends email notification</li>
            <li>• User can process a payment</li>
        </ul>
    </div>
    <div class="p-6 bg-purple-50 dark:bg-purple-900/20 border border-purple-100 dark:border-purple-800 rounded-xl">
        <h3 class="font-bold text-purple-800 dark:text-purple-400">Non-Functional Requirements (NFR)</h3>
        <p class="text-sm text-slate-600 dark:text-slate-400 mt-2">The constraints or quality attributes. "How the system performs."</p>
        <ul class="text-xs mt-3 space-y-1 text-slate-500">
            <li>• Scalability: Handle 100k concurrent users</li>
            <li>• Availability: 99.99% uptime</li>
            <li>• Latency: Search results in < 200ms</li>
        </ul>
    </div>
</div>

<h3>Back of the Envelope Estimation</h3>
<p>System designers use quick calculations to estimate resource needs. Key constants to remember:</p>
<div class="overflow-x-auto my-6 not-prose">
    <table class="min-w-full text-sm text-left text-slate-600 dark:text-slate-300">
        <thead class="bg-slate-100 dark:bg-slate-800 uppercase text-xs">
            <tr>
                <th class="px-4 py-2">Operation</th>
                <th class="px-4 py-2">Approx. Time</th>
            </tr>
        </thead>
        <tbody>
            <tr><td class="px-4 py-2">L1 Cache Reference</td><td class="px-4 py-2">0.5 ns</td></tr>
            <tr><td class="px-4 py-2">Main Memory Reference</td><td class="px-4 py-2">100 ns</td></tr>
            <tr><td class="px-4 py-2">SSD Random Read</td><td class="px-4 py-2">16,000 ns (16 µs)</td></tr>
            <tr><td class="px-4 py-2">Round trip in same datacenter</td><td class="px-4 py-2">500,000 ns (0.5 ms)</td></tr>
        </tbody>
    </table>
</div>

<h3>Service Level Agreements (SLA)</h3>
<p>How we measure and guarantee system performance:</p>
<ul>
    <li><strong>SLI (Indicator):</strong> The actual metric being measured (e.g., Latency).</li>
    <li><strong>SLO (Objective):</strong> The target value for the indicator (e.g., Latency < 100ms).</li>
    <li><strong>SLA (Agreement):</strong> The contract with the customer (e.g., "If SLO is missed, we pay you back").</li>
</ul>

<div class="my-8 p-6 border border-slate-200 dark:border-slate-700 rounded-xl not-prose bg-white dark:bg-slate-900/50">
<div class="mermaid text-center">
graph LR
    U[User] -- "Latency (SLI)" --> S[System]
    S -- "Target: 99.9% (SLO)" --> B[Business Goal]
    B -- "Contract" --> C[SLA]
</div>
</div>
        """
    },
    {
        "id": "scalability",
        "title": "2. Scalability",
        "icon": "trending-up",
        "description": "How systems handle growth: Scaling, Load Balancing, and Sharding.",
        "content": """
<h2>Handling System Growth</h2>
<p>Scalability is the ability of a system to handle increased load by adding resources.</p>

<div class="space-y-8">
    <section>
        <h3 class="flex items-center gap-2">Vertical vs Horizontal Scaling</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
            <div class="p-5 border border-slate-200 dark:border-slate-800 rounded-xl bg-slate-50/50 dark:bg-slate-900/50">
                <h4 class="font-bold text-blue-600 mb-2">Vertical (Scaling Up)</h4>
                <p class="text-sm mb-3">Increasing the capacity of a single machine (e.g., more CPU, RAM).</p>
                <ul class="text-xs space-y-1 opacity-70">
                    <li>✅ Simpler to manage (no distributed complexity)</li>
                    <li>✅ No network latency between components</li>
                    <li>❌ Hard limit (hardware maximum)</li>
                    <li>❌ Single point of failure</li>
                    <li>❌ Extremely expensive at high ends</li>
                </ul>
            </div>
            <div class="p-5 border border-slate-200 dark:border-slate-800 rounded-xl bg-slate-50/50 dark:bg-slate-900/50">
                <h4 class="font-bold text-emerald-600 mb-2">Horizontal (Scaling Out)</h4>
                <p class="text-sm mb-3">Adding more machines to the system pool.</p>
                <ul class="text-xs space-y-1 opacity-70">
                    <li>✅ Theoretically infinite scale</li>
                    <li>✅ High availability (one node down doesn't kill system)</li>
                    <li>✅ Cost-effective (use commodity hardware)</li>
                    <li>❌ Complex management (Load Balancers, Service Discovery)</li>
                    <li>❌ Distributed data consistency issues</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h3>Load Balancing (Traffic Management)</h3>
        <p>A Load Balancer (LB) sits between the user and the servers, distributing incoming requests to prevent any single server from becoming a bottleneck.</p>
        
        <div class="my-6 p-6 border border-slate-200 dark:border-slate-800 rounded-xl bg-white dark:bg-slate-900/50">
            <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">Common Algorithms</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div class="text-sm">
                    <span class="font-bold">1. Round Robin:</span> Cycles through servers in order. Best when all servers have equal power.
                </div>
                <div class="text-sm">
                    <span class="font-bold">2. Least Connections:</span> Sends traffic to the server with the fewest active requests.
                </div>
                <div class="text-sm">
                    <span class="font-bold">3. IP Hash:</span> Uses the client's IP to map them to a specific server (Sticky Sessions).
                </div>
                <div class="text-sm">
                    <span class="font-bold">4. Weighted WRR:</span> Servers with higher capacity get a larger percentage of traffic.
                </div>
            </div>
        </div>
    </section>

    <section>
        <h3>Data Sharding & Partitioning</h3>
        <p>When a single database is too large or too slow, we split it. This is critical for Data Engineering pipelines.</p>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
            <div class="p-4 border-l-4 border-amber-500 bg-amber-50 dark:bg-amber-950/20">
                <h4 class="font-bold text-sm">Horizontal Partitioning (Sharding)</h4>
                <p class="text-xs mt-1">Splitting rows into different tables. E.g., Users 1-1000 in DB A, 1001-2000 in DB B.</p>
            </div>
            <div class="p-4 border-l-4 border-blue-500 bg-blue-50 dark:bg-blue-950/20">
                <h4 class="font-bold text-sm">Vertical Partitioning</h4>
                <p class="text-xs mt-1">Splitting columns into different tables. E.g., User Profile in DB A, User Metadata in DB B.</p>
            </div>
        </div>

        <div class="mt-6">
            <h4 class="font-bold mb-2">Sharding Strategies:</h4>
            <ul class="text-sm space-y-2">
                <li><strong>Key-Based (Hash):</strong> Apply a hash function to the user ID to determine the shard.</li>
                <li><strong>Range-Based:</strong> Shard based on a range (e.g., Dates or Alphabetical). Risk of "Hotspots" (e.g., all traffic on the current month).</li>
                <li><strong>Directory-Based:</strong> A lookup service tracks which data lives in which shard. Most flexible but adds a dependency.</li>
            </ul>
        </div>
    </section>
</div>
        """
    },
    {
        "id": "networking",
        "title": "3. Networking Basics",
        "icon": "globe",
        "description": "Protocols, Proxies, and Content Delivery.",
        "content": """
<h2>The Internet Protocol Suite</h2>
<p>Networking is the communication layer that enables distributed systems to talk to each other.</p>

<h3>HTTP Evolution</h3>
<div class="overflow-x-auto my-6 not-prose">
    <table class="min-w-full text-xs text-left">
        <thead class="bg-slate-100 dark:bg-slate-800 uppercase">
            <tr>
                <th class="px-4 py-2">Version</th>
                <th class="px-4 py-2">Mechanism</th>
                <th class="px-4 py-2">Key Benefit</th>
            </tr>
        </thead>
        <tbody>
            <tr class="border-b dark:border-slate-800">
                <td class="px-4 py-2 font-bold">HTTP/1.1</td>
                <td class="px-4 py-2">Sequential requests</td>
                <td class="px-4 py-2">Persistent connections.</td>
            </tr>
            <tr class="border-b dark:border-slate-800">
                <td class="px-4 py-2 font-bold">HTTP/2</td>
                <td class="px-4 py-2">Binary, Multiplexing</td>
                <td class="px-4 py-2">Send multiple requests over 1 connection. Header compression (HPACK).</td>
            </tr>
            <tr class="border-b dark:border-slate-800">
                <td class="px-4 py-2 font-bold">HTTP/3</td>
                <td class="px-4 py-2">QUIC (UDP based)</td>
                <td class="px-4 py-2">Solves Head-of-line blocking. Faster handshakes.</td>
            </tr>
        </tbody>
    </table>
</div>

<div class="grid grid-cols-1 md:grid-cols-2 gap-8 my-10">
    <div>
        <h3 class="mb-3">Proxies: The Gatekeepers</h3>
        <div class="space-y-4">
            <div class="p-4 bg-slate-100 dark:bg-slate-900 rounded-lg">
                <h4 class="font-bold text-sm">Forward Proxy</h4>
                <p class="text-xs mt-1">Sits in front of <strong>clients</strong>. Used to hide client IP, bypass firewalls, or cache client requests (e.g., VPNs).</p>
            </div>
            <div class="p-4 bg-slate-100 dark:bg-slate-900 rounded-lg">
                <h4 class="font-bold text-sm">Reverse Proxy</h4>
                <p class="text-xs mt-1">Sits in front of <strong>servers</strong>. Used for Load Balancing, SSL Termination, and Caching (e.g., Nginx, HAProxy).</p>
            </div>
        </div>
    </div>
    <div>
        <h3 class="mb-3">API Gateways</h3>
        <p class="text-sm">An advanced reverse proxy that acts as the single entry point for microservices.</p>
        <ul class="text-xs mt-3 space-y-2">
            <li class="flex items-start gap-2">✅ <strong>Authentication:</strong> Centralized login check.</li>
            <li class="flex items-start gap-2">✅ <strong>Rate Limiting:</strong> Prevent API abuse.</li>
            <li class="flex items-start gap-2">✅ <strong>Request Routing:</strong> Sending traffic to the right microservice.</li>
            <li class="flex items-start gap-2">✅ <strong>Protocol Translation:</strong> Converting REST to gRPC internally.</li>
        </ul>
    </div>
</div>

<h3>CDN (Content Delivery Network)</h3>
<p>Geographically distributed servers that cache content at the "edge" (close to users).</p>
<div class="my-6 p-6 bg-white dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-xl not-prose">
<div class="mermaid text-center">
graph LR
    User[User in London] -- Request --> Edge[CDN Edge Server: London]
    Edge -- Cache Hit --> User
    Edge -- Cache Miss --> Origin[Origin Server: NYC]
    Origin -- Content --> Edge
    Edge -- Cache & Deliver --> User
</div>
</div>
        """
    },
    {
        "id": "databases",
        "title": "4. Databases",
        "icon": "database",
        "description": "SQL, NoSQL, ACID, BASE, and the CAP Theorem.",
        "content": """
<h2>Modern Data Persistence</h2>
<p>Choosing a database is not about finding the "best" one, but the one whose trade-offs fit your data model.</p>

<div class="grid grid-cols-1 md:grid-cols-2 gap-8 my-8">
    <section>
        <h3 class="text-blue-600 dark:text-blue-400">SQL (Relational)</h3>
        <p class="text-sm">Structured data with strict schemas. Great for complex joins and financial data.</p>
        <div class="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-100 dark:border-blue-800">
            <h4 class="font-bold text-xs uppercase mb-2">ACID Properties</h4>
            <ul class="text-xs space-y-1">
                <li><strong>A: Atomicity</strong> - All or nothing transactions.</li>
                <li><strong>C: Consistency</strong> - Data follows rules (FKs, Constraints).</li>
                <li><strong>I: Isolation</strong> - Transactions don't interfere.</li>
                <li><strong>D: Durability</strong> - Data persists even if system crashes.</li>
            </ul>
        </div>
    </section>
    <section>
        <h3 class="text-purple-600 dark:text-purple-400">NoSQL (Non-Relational)</h3>
        <p class="text-sm">Flexible data models. Optimized for high volume and horizontal scaling.</p>
        <div class="mt-4 p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-100 dark:border-purple-800">
            <h4 class="font-bold text-xs uppercase mb-2">BASE Properties</h4>
            <ul class="text-xs space-y-1">
                <li><strong>BA: Basically Available</strong> - Guaranteed availability.</li>
                <li><strong>S: Soft state</strong> - State can change without input.</li>
                <li><strong>E: Eventual Consistency</strong> - Data will match across replicas... eventually.</li>
            </ul>
        </div>
    </section>
</div>

<h3>Indexing: Speeding up Reads</h3>
<p>An index is a data structure that improves the speed of data retrieval operations at the cost of additional storage and slower writes.</p>
<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 my-6">
    <div class="p-4 bg-slate-100 dark:bg-slate-800 rounded-lg">
        <h4 class="font-bold text-sm">B-Tree Index</h4>
        <p class="text-xs mt-1">Default for most SQL DBs. Great for range queries (e.g., <code>Price BETWEEN 10 AND 50</code>).</p>
    </div>
    <div class="p-4 bg-slate-100 dark:bg-slate-800 rounded-lg">
        <h4 class="font-bold text-sm">Hash Index</h4>
        <p class="text-xs mt-1">O(1) lookups. Only works for exact matches (e.g., <code>ID = 'abc'</code>).</p>
    </div>
</div>

<h3>Consistent Hashing</h3>
<p>A technique used to minimize re-mapping of keys when the number of shards changes. Essential for large-scale distributed caches (like Memcached) and NoSQL DBs (like Cassandra).</p>
<div class="my-8">
<div class="mermaid text-center">
graph LR
    subgraph Hash Ring
    A[Node 1] --- B[Node 2] --- C[Node 3] --- A
    end
    K1[Key 1] --> A
    K2[Key 2] --> B
</div>
<p class="text-center text-xs opacity-50 mt-2">When Node 3 is added, only some keys move from Node 1 to Node 3.</p>
</div>
        """
    },
    {
        "id": "caching",
        "title": "5. Caching",
        "icon": "zap",
        "description": "Improving speed with Memory storage and Eviction patterns.",
        "content": """
<h2>Why Cache?</h2>
<p>Memory access is <strong>100,000x faster</strong> than disk access. Caching is the process of storing copies of data in a high-speed layer.</p>

<h3>Cache Strategies (Patterns)</h3>
<div class="space-y-6 my-8">
    <div class="flex gap-4 items-start">
        <div class="w-24 shrink-0 font-bold text-xs uppercase text-blue-500 py-1">Cache Aside</div>
        <div class="text-sm">The most common. App checks cache; if miss, it reads from DB and updates cache. Simple and handles cache failures gracefully.</div>
    </div>
    <div class="flex gap-4 items-start">
        <div class="w-24 shrink-0 font-bold text-xs uppercase text-emerald-500 py-1">Read Through</div>
        <div class="text-sm">The library or framework handles the DB lookup. The app only talks to the cache. Consistent data but complex to implement.</div>
    </div>
    <div class="flex gap-4 items-start">
        <div class="w-24 shrink-0 font-bold text-xs uppercase text-amber-500 py-1">Write Through</div>
        <div class="text-sm">Data is written to cache and DB simultaneously. Ensures data consistency but adds write latency.</div>
    </div>
    <div class="flex gap-4 items-start">
        <div class="w-24 shrink-0 font-bold text-xs uppercase text-rose-500 py-1">Write Back</div>
        <div class="text-sm">Data is written ONLY to cache. DB is updated in batches later. Highest write performance but risk of data loss on cache crash.</div>
    </div>
</div>

<h3>Cache Eviction: Making Room</h3>
<p>When the cache is full, we must decide what to delete. This is handled by **Eviction Policies**:</p>
<div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-6">
    <div class="p-4 border border-slate-200 dark:border-slate-800 rounded-xl bg-white dark:bg-slate-900/50">
        <h4 class="font-bold text-sm mb-2">LRU</h4>
        <p class="text-xs"><strong>Least Recently Used:</strong> Discards items that haven't been accessed for the longest time. Best for general use.</p>
    </div>
    <div class="p-4 border border-slate-200 dark:border-slate-800 rounded-xl bg-white dark:bg-slate-900/50">
        <h4 class="font-bold text-sm mb-2">LFU</h4>
        <p class="text-xs"><strong>Least Frequently Used:</strong> Counts how often an item is used. Discards those with the lowest count.</p>
    </div>
    <div class="p-4 border border-slate-200 dark:border-slate-800 rounded-xl bg-white dark:bg-slate-900/50">
        <h4 class="font-bold text-sm mb-2">TTL</h4>
        <p class="text-xs"><strong>Time to Live:</strong> Automatically expires data after a set duration (e.g., 60 minutes).</p>
    </div>
</div>
        """
    },
    {
        "id": "messaging-queues",
        "title": "6. Messaging & Queues",
        "icon": "message-square",
        "description": "Kafka, RabbitMQ, Decoupling, and Delivery Guarantees.",
        "content": """
<h2>Asynchronous Communication</h2>
<p>Messaging systems allow services to communicate without waiting for a response, enabling high throughput and decoupling.</p>

<div class="grid grid-cols-1 md:grid-cols-2 gap-8 my-8">
    <section>
        <h3 class="text-orange-600">RabbitMQ (Message Queue)</h3>
        <p class="text-sm">Traditional message broker. Messages are deleted once consumed.</p>
        <div class="mt-4 p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
            <h4 class="font-bold text-xs mb-2">Routing Types</h4>
            <ul class="text-xs space-y-1">
                <li><strong>Direct:</strong> Exact routing key match.</li>
                <li><strong>Fanout:</strong> Broadcast to all queues.</li>
                <li><strong>Topic:</strong> Partial match using wildcards (*, #).</li>
            </ul>
        </div>
    </section>
    <section>
        <h3 class="text-blue-600">Apache Kafka (Event Log)</h3>
        <p class="text-sm">A distributed append-only log. Messages persist even after consumption.</p>
        <div class="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <h4 class="font-bold text-xs mb-2">Architecture</h4>
            <ul class="text-xs space-y-1">
                <li><strong>Topic:</strong> Stream of messages.</li>
                <li><strong>Partition:</strong> Subsets of a topic (enables parallel processing).</li>
                <li><strong>Offset:</strong> Unique ID for each message in a partition.</li>
            </ul>
        </div>
    </section>
</div>

<h3>The Delivery Guarantee Spectrum</h3>
<p>Depending on the business logic, you must choose how messages are delivered:</p>
<div class="space-y-4 my-6">
    <div class="p-4 border-l-4 border-rose-500 bg-rose-50 dark:bg-rose-950/20">
        <h4 class="font-bold text-sm">At-Most-Once</h4>
        <p class="text-xs">Message is sent once. If it's lost, it's gone. Used for telemetry data where missing a point is okay.</p>
    </div>
    <div class="p-4 border-l-4 border-amber-500 bg-amber-50 dark:bg-amber-950/20">
        <h4 class="font-bold text-sm">At-Least-Once</h4>
        <p class="text-xs">Message is sent until an ACK is received. Prevents data loss but can cause duplicates. (Most common in DE pipelines).</p>
    </div>
    <div class="p-4 border-l-4 border-emerald-500 bg-emerald-50 dark:bg-emerald-950/20">
        <h4 class="font-bold text-sm">Exactly-Once</h4>
        <p class="text-xs">The holy grail. Requires transactional coordination between producer, broker, and consumer.</p>
    </div>
</div>
        """
    }
]

hub_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>System Design — Data Sheets</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>
<div class="fixed top-0 left-0 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none z-0"></div>

<main class="relative z-10 pt-28 pb-20 px-6 max-w-5xl mx-auto">
    <a href="../learn.html" class="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm mb-8 no-underline transition-colors duration-200">
        <i data-lucide="arrow-left" class="w-4 h-4"></i>
        Back to Learn
    </a>

    <div class="flex items-start gap-5 mb-10">
        <div class="w-16 h-16 rounded-xl flex items-center justify-center bg-blue-100 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400">
            <i data-lucide="layout" class="w-8 h-8"></i>
        </div>
        <div>
            <span class="inline-block px-3 py-1 rounded-full text-xs font-semibold mb-2 bg-blue-100 dark:bg-blue-500/20 text-blue-700 dark:text-blue-300">Architecture</span>
            <h1 class="font-display font-bold text-4xl text-slate-900 dark:text-white leading-tight">System Design</h1>
            <p class="text-slate-600 dark:text-slate-400 mt-2 text-lg">Foundation of scalable architectures: Load Balancing, Databases, Caching, and Microservices.</p>
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
    <title>{title} — System Design</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        const isDark = document.documentElement.classList.contains('dark');
        mermaid.initialize({{ 
            startOnLoad: true, 
            theme: isDark ? 'dark' : 'default',
            fontFamily: 'Inter',
            themeVariables: {{ fontFamily: 'Inter', fontSize: '13px' }}
        }});
    </script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>

<div class="flex justify-center max-w-[1440px] mx-auto">
    <main class="relative z-10 pt-28 pb-32 px-6 w-full max-w-3xl">
        <a href="../system-design.html" class="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm mb-10 no-underline transition-colors duration-200">
            <i data-lucide="arrow-left" class="w-4 h-4"></i>
            Back to System Design
        </a>

        <h1 class="font-display font-bold text-4xl md:text-5xl text-slate-900 dark:text-white mb-4 leading-tight">{title}</h1>
        <p class="text-xl text-slate-600 dark:text-slate-400 mb-12">{description}</p>
        
        <div class="prose prose-slate dark:prose-invert prose-lg max-w-none">
            {content}
        </div>
    </main>

    <aside class="toc-container">
        <div class="toc-title">On this page</div>
        <ul class="toc-list"></ul>
        {topics_list_html}
    </aside>
</div>
</body>
</html>'''

# 1. Build Hub Page
cards_html = ""
for page in subpages:
    card = f'''
    <a href="system-design/{page['id']}.html" class="topic-card block p-6 bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-2xl no-underline group shadow-sm dark:shadow-none hover:border-blue-300 dark:hover:border-blue-500/50">
        <div class="flex items-center justify-between mb-4">
            <div class="w-10 h-10 rounded-lg bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                <i data-lucide="{page['icon']}" class="w-5 h-5"></i>
            </div>
            <i data-lucide="arrow-right" class="w-4 h-4 text-slate-300 dark:text-slate-600 group-hover:text-blue-500 group-hover:-translate-x-1 transition-all"></i>
        </div>
        <h3 class="font-display font-semibold text-lg text-slate-900 dark:text-white mb-2">{page["title"]}</h3>
        <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">{page["description"]}</p>
    </a>
    '''
    cards_html += card

hub_content = hub_template.format(cards_html=cards_html)
os.makedirs("pages/learn", exist_ok=True)
with open("pages/learn/system-design.html", "w", encoding="utf-8") as f:
    f.write(hub_content)

# 2. Build Subpages
os.makedirs("pages/learn/system-design", exist_ok=True)
for page in subpages:
    # Build list of all topics for the sidebar
    topics_html = '<div class="toc-title mt-8">System Design</div><ul class="toc-list">'
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
    path = os.path.join("pages", "learn", "system-design", f"{page['id']}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Successfully generated System Design pages!")
