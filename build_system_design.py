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
<div class="mermaid">
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

<h3>Cache Invalidation: The "Hard" Problem</h3>
<p>How do we keep the cache in sync with the DB? "There are only two hard things in Computer Science: cache invalidation and naming things."</p>
<ul>
    <li><strong>Purge:</strong> Remove a specific key manually on update.</li>
    <li><strong>Refresh:</strong> Update the cache value manually on DB update.</li>
    <li><strong>Short TTL:</strong> Let the data expire frequently (acceptable for non-critical data).</li>
</ul>
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

<h3>Handling Backpressure</h3>
<p>What happens when the producer is faster than the consumer?</p>
<ul>
    <li><strong>Pull Model:</strong> Consumer asks for data only when ready (e.g., Kafka).</li>
    <li><strong>Drop:</strong> Discard messages once buffer is full.</li>
    <li><strong>DLQ (Dead Letter Queue):</strong> Send failed messages to a separate queue for manual inspection.</li>
</ul>
        """
    },
    {
        "id": "api-design",
        "title": "7. API Design",
        "icon": "code",
        "description": "REST principles, Versioning, and Performance patterns.",
        "content": """
<h2>Building Usable Service Contracts</h2>
<p>APIs are the interface of your system. A well-designed API is easy to use, hard to misuse, and scales predictably.</p>

<h3>The 3 Main Styles</h3>
<div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-6 not-prose">
    <div class="p-4 border border-slate-200 dark:border-slate-800 rounded-xl bg-white dark:bg-slate-900/50">
        <h4 class="font-bold text-sm text-blue-600 mb-2">REST</h4>
        <p class="text-xs">Resource-based (nouns, not verbs). Uses HTTP methods (GET, POST). Stateless.</p>
    </div>
    <div class="p-4 border border-slate-200 dark:border-slate-800 rounded-xl bg-white dark:bg-slate-900/50">
        <h4 class="font-bold text-sm text-purple-600 mb-2">GraphQL</h4>
        <p class="text-xs">Client asks for exactly what it needs. Prevents over-fetching and under-fetching.</p>
    </div>
    <div class="p-4 border border-slate-200 dark:border-slate-800 rounded-xl bg-white dark:bg-slate-900/50">
        <h4 class="font-bold text-sm text-emerald-600 mb-2">gRPC</h4>
        <p class="text-xs">Binary protocol (Protobuf). Extremely fast, strongly typed, and supports streaming.</p>
    </div>
</div>

<h3>Pagination: Handling Large Lists</h3>
<p>When returning thousands of records, we must split them:</p>
<ul>
    <li><strong>Offset Pagination:</strong> <code>LIMIT 10 OFFSET 20</code>. Easy but slow for deep pages (DB has to scan and discard).</li>
    <li><strong>Cursor Pagination:</strong> <code>WHERE ID > last_seen_id LIMIT 10</code>. Stable and fast. Preferred for real-time streams.</li>
</ul>

<div class="my-10 p-6 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl">
    <h3 class="mt-0">Rate Limiting Algorithms</h3>
    <p class="text-sm opacity-80">How systems defend themselves from being overwhelmed:</p>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 mt-4">
        <div class="space-y-2">
            <h4 class="font-bold text-sm italic underline">Token Bucket</h4>
            <p class="text-xs">A bucket holds tokens. Each request takes one. Tokens refill at a set rate. Allows for "bursts" of traffic.</p>
        </div>
        <div class="space-y-2">
            <h4 class="font-bold text-sm italic underline">Leaky Bucket</h4>
            <p class="text-xs">Requests enter a bucket and "leak" out at a constant rate. Smooths out traffic, preventing bursts.</p>
        </div>
    </div>
</div>

<h3>Idempotency Keys</h3>
<p>A unique ID sent in a request header. If the server sees the same key again, it returns the cached response instead of performing the action again. Essential for handling network retries in payment systems.</p>
        """
    },
    {
        "id": "storage",
        "title": "8. Storage",
        "icon": "hard-drive",
        "description": "Block, Object, and File Storage. S3 and RAID.",
        "content": """
<h2>Data Persistence Layers</h2>
<p>Different workloads require different storage physical properties. In Data Engineering, object storage is king.</p>

<div class="overflow-x-auto my-8 not-prose">
    <table class="min-w-full text-sm text-left">
        <thead class="bg-slate-100 dark:bg-slate-800 uppercase">
            <tr>
                <th class="px-4 py-2">Type</th>
                <th class="px-4 py-2">Latency</th>
                <th class="px-4 py-2">Typical Usage</th>
            </tr>
        </thead>
        <tbody>
            <tr class="border-b dark:border-slate-800">
                <td class="px-4 py-2 font-bold">Block (EBS)</td>
                <td class="px-4 py-2">Very Low</td>
                <td class="px-4 py-2">Databases, Transactional logs.</td>
            </tr>
            <tr class="border-b dark:border-slate-800">
                <td class="px-4 py-2 font-bold">Object (S3)</td>
                <td class="px-4 py-2">High</td>
                <td class="px-4 py-2">Data Lakes, Media files, Backups.</td>
            </tr>
            <tr class="border-b dark:border-slate-800">
                <td class="px-4 py-2 font-bold">File (EFS)</td>
                <td class="px-4 py-2">Medium</td>
                <td class="px-4 py-2">Shared config, CMS uploads.</td>
            </tr>
        </tbody>
    </table>
</div>

<h3>S3 Storage Tiers: Cost Optimization</h3>
<p>Cloud providers offer different "temperatures" for data storage:</p>
<ul>
    <li><strong>Standard:</strong> Active data. High cost, high performance.</li>
    <li><strong>Infrequent Access (IA):</strong> Lower storage cost, but retrieval fee. Best for month-old logs.</li>
    <li><strong>Glacier:</strong> Extremely cheap. Retrieval takes minutes to hours. Best for compliance archives.</li>
</ul>

<h3>RAID (Redundant Array of Independent Disks)</h3>
<p>Combining multiple disks to improve performance or redundancy:</p>
<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 my-6 text-xs">
    <div class="p-3 border border-slate-200 dark:border-slate-800 rounded-lg">
        <span class="font-bold">RAID 0 (Striping):</span> Speed. Splits data across disks. If one dies, all data is lost.
    </div>
    <div class="p-3 border border-slate-200 dark:border-slate-800 rounded-lg">
        <span class="font-bold">RAID 1 (Mirroring):</span> Redundancy. Writes data to two disks. 50% storage efficiency.
    </div>
    <div class="p-3 border border-slate-200 dark:border-slate-800 rounded-lg">
        <span class="font-bold">RAID 5:</span> Balance. Uses parity for redundancy. Can survive one disk failure.
    </div>
    <div class="p-3 border border-slate-200 dark:border-slate-800 rounded-lg">
        <span class="font-bold">RAID 10 (1+0):</span> The best of both. Mirroring + Striping. High perf and high reliability.
    </div>
</div>
        """
    },
    {
        "id": "high-availability",
        "title": "9. High Availability",
        "icon": "shield-check",
        "description": "Building fault-tolerant systems and handling failures.",
        "content": """
<h2>Reliability as a Feature</h2>
<p>System failures are inevitable. High Availability (HA) is the design pattern that ensures the system continues to function even when components fail.</p>

<h3>The Circuit Breaker Deep Dive</h3>
<p>Like an electrical fuse, it stops requests to a failing service to prevent a total system crash.</p>
<div class="my-8 p-6 bg-slate-900 rounded-xl">
<div class="mermaid text-center">
stateDiagram-v2
    [*] --> Closed: Healthy
    Closed --> Open: Error Threshold Reached
    Open --> HalfOpen: Wait for Timeout
    HalfOpen --> Closed: Success (Reset)
    HalfOpen --> Open: Failure (Re-Open)
</div>
</div>

<h3>Retry Strategies: Exponential Backoff</h3>
<p>When a request fails, don't immediately retry at full speed (you'll DDoS your own server). Instead, use exponential wait times.</p>
<div class="p-4 bg-slate-100 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 my-4 font-mono text-xs">
    retry_time = base * (2 ^ attempt) + random_jitter()
</div>
<p class="text-sm">Adding <strong>Jitter</strong> (randomness) ensures that thousands of retrying clients don't all hit the server at the exact same millisecond.</p>

<h3>Recovery Metrics: RTO vs RPO</h3>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-8">
    <div class="p-5 bg-rose-50 dark:bg-rose-900/20 border border-rose-100 rounded-xl">
        <h4 class="font-bold text-rose-700">RPO (Recovery Point Objective)</h4>
        <p class="text-xs mt-2">Maximum amount of data you can lose. E.g., RPO of 1 hour means you need backups every 60 minutes.</p>
    </div>
    <div class="p-5 bg-amber-50 dark:bg-amber-900/20 border border-amber-100 rounded-xl">
        <h4 class="font-bold text-amber-700">RTO (Recovery Time Objective)</h4>
        <p class="text-xs mt-2">Maximum time the system can be down before the business is in trouble.</p>
    </div>
</div>
        """
    },
    {
        "id": "microservices",
        "title": "10. Microservices",
        "icon": "layers",
        "description": "Managing complexity in distributed application architectures.",
        "content": """
<h2>Distributed Systems Architecture</h2>
<p>Microservices break a monolith into small, independently deployable pieces. This improves developer velocity but adds massive networking complexity.</p>

<h3>Data Consistency: The Saga Pattern</h3>
<p>In microservices, you cannot have a distributed transaction (too slow). Instead, we use a sequence of local transactions called a Saga.</p>
<div class="space-y-4 my-6">
    <div class="p-4 border border-slate-200 dark:border-slate-800 rounded-xl">
        <h4 class="font-bold text-sm">1. Choreography</h4>
        <p class="text-xs">Each service produces an event. Other services listen and react. Decentralized and decoupled.</p>
    </div>
    <div class="p-4 border border-slate-200 dark:border-slate-800 rounded-xl">
        <h4 class="font-bold text-sm">2. Orchestration</h4>
        <p class="text-xs">A central "Orchestrator" service tells each service what to do. Easier to manage but adds a central dependency.</p>
    </div>
</div>

<h3>CQRS (Command Query Responsibility Segregation)</h3>
<p>Separating the model for writing data from the model for reading it.</p>
<ul>
    <li><strong>Command Side:</strong> Optimized for transactional writes (e.g., PostgreSQL).</li>
    <li><strong>Query Side:</strong> Optimized for fast reads/searches (e.g., Elasticsearch or a flattened View).</li>
</ul>

<h3>Service Discovery</h3>
<p>Because microservices scale up/down, their IPs change constantly. A **Service Registry** (like Consul or Kubernetes DNS) acts as a phone book, keeping track of active service instances.</p>

<div class="my-8 p-6 bg-white dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-xl not-prose">
<div class="mermaid text-center">
graph TD
    User --> Gateway[API Gateway]
    Gateway --> Discovery{Service Discovery}
    Discovery -- "Where is Order Service?" --> Registry[(Registry)]
    Registry -- "10.0.0.5" --> Discovery
    Discovery --> OrderService[Order Service at 10.0.0.5]
</div>
</div>
        """
    },
    {
        "id": "observability",
        "title": "11. Observability",
        "icon": "eye",
        "description": "Metrics, Logging, and Distributed Tracing.",
        "content": """
<h2>The Pulse of the System</h2>
<p>Observability allows teams to debug "unknown unknowns" by analyzing the external outputs of a system.</p>

<h3>The 3 Pillars of Observability</h3>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6 my-8 not-prose">
    <div class="p-6 bg-emerald-50 dark:bg-emerald-950/40 rounded-xl border border-emerald-100">
        <h4 class="font-bold text-emerald-700 mb-2">Metrics</h4>
        <p class="text-xs opacity-80">Numbers over time. CPU, RAM, Error Rates. Best for dashboards and alerting.</p>
        <span class="text-[10px] mt-4 block text-emerald-600">Tool: Prometheus, Grafana</span>
    </div>
    <div class="p-6 bg-blue-50 dark:bg-blue-950/40 rounded-xl border border-blue-100">
        <h4 class="font-bold text-blue-700 mb-2">Logging</h4>
        <p class="text-xs opacity-80">Textual records of specific events. Essential for root cause analysis.</p>
        <span class="text-[10px] mt-4 block text-blue-600">Tool: ELK Stack (Elastic, Logstash, Kibana)</span>
    </div>
    <div class="p-6 bg-violet-50 dark:bg-violet-950/40 rounded-xl border border-violet-100">
        <h4 class="font-bold text-violet-700 mb-2">Tracing</h4>
        <p class="text-xs opacity-80">Connecting logs across service boundaries using a Trace ID. Visualizes latency.</p>
        <span class="text-[10px] mt-4 block text-violet-600">Tool: Jaeger, Zipkin</span>
    </div>
</div>

<h3>Distributed Tracing Deep Dive</h3>
<p>When a user clicks "Order", the request flows through 5 services. Distributed tracing injects a header (TraceID) into the request. Every service logs with this ID, allowing you to reconstruct the entire journey.</p>

<div class="my-6 p-4 bg-slate-900 text-white rounded-lg font-mono text-xs">
    # Example Trace Header
    X-Trace-Id: 5d2b7e1-8f3a
    X-Span-Id: a1b2c3
</div>
        """
    },
    {
        "id": "security",
        "title": "12. Security",
        "icon": "lock",
        "description": "Protecting systems from edge to core.",
        "content": """
<h2>Defense in Depth</h2>
<p>Security must be implemented at every layer, from the network perimeter to the database columns.</p>

<div class="space-y-8">
    <section>
        <h3>Authentication vs Authorization</h3>
        <ul class="space-y-3">
            <li><strong>AuthN (Authentication):</strong> Verifying identity. "Who are you?" (Passwords, Biometrics, Multi-factor).</li>
            <li><strong>AuthZ (Authorization):</strong> Verifying permissions. "What are you allowed to do?" (Admin vs User).</li>
        </ul>
    </section>

    <section>
        <h3>Modern Auth: JWT & OAuth2</h3>
        <p class="text-sm"><strong>JWT (JSON Web Token):</strong> A stateless token that contains user data. Because it's digitally signed, the server doesn't need to look up the user in the DB for every request.</p>
        <p class="text-sm mt-3"><strong>OAuth2:</strong> The standard for delegated authorization. Allows a user to grant an app access to their data on another service (e.g., "Sign in with Google") without sharing passwords.</p>
    </section>

    <section>
        <h3>Role-Based Access Control (RBAC)</h3>
        <p class="text-sm italic">Assigning permissions to "Roles" rather than individual users. Makes management vastly simpler as organizations grow.</p>
    </section>
</div>

<h3>Top System Design Attacks</h3>
<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 my-8 text-xs">
    <div class="p-4 border border-rose-200 dark:border-rose-900/30 rounded-xl bg-rose-50/20">
        <h4 class="font-bold text-rose-600 mb-1">DDoS Attack</h4>
        <p>Overwhelming a system with traffic. <strong>Fix:</strong> API Gateway Rate Limiting, Cloudflare.</p>
    </div>
    <div class="p-4 border border-rose-200 dark:border-rose-900/30 rounded-xl bg-rose-50/20">
        <h4 class="font-bold text-rose-600 mb-1">Injection Attacks</h4>
        <p>Executing malicious code via input fields. <strong>Fix:</strong> Input validation, Parameterized queries.</p>
    </div>
</div>
        """
    },
    {
        "id": "infra-deployment",
        "title": "13. Infra & Deployment",
        "icon": "server",
        "description": "Containers, Orchestration, and Automated delivery.",
        "content": """
<h2>Modern Infrastructure Management</h2>
<p>Infrastructure as Code (IaC) and Containerization have revolutionized how systems are deployed.</p>

<div class="grid grid-cols-1 md:grid-cols-2 gap-8 my-8">
    <section>
        <h3>Docker: The Container</h3>
        <p class="text-sm">Packaging code, runtime, and system tools into a single immutable image. Solves the "it works on my machine" problem.</p>
    </section>
    <section>
        <h3>Kubernetes: The Orchestrator</h3>
        <p class="text-sm">Automating the deployment, scaling, and management of containers. It handles healing, rolling updates, and service discovery.</p>
    </section>
</div>

<h3>Deployment Strategies: The Zero-Downtime Goal</h3>
<div class="space-y-4 my-8">
    <div class="p-4 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl">
        <h4 class="font-bold text-sm text-blue-500">Blue-Green Deployment</h4>
        <p class="text-xs mt-1">You have two identical environments. You deploy to "Green". Once verified, you flip the switch (LB) to route traffic to Green. Instant rollback by switching back to Blue.</p>
    </div>
    <div class="p-4 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl">
        <h4 class="font-bold text-sm text-emerald-500">Canary Deployment</h4>
        <p class="text-xs mt-1">Slowly rolling out the new version to a subset of users (e.g., 5%). If metrics are healthy, you proceed to 100%.</p>
    </div>
</div>

<h3>Infrastructure as Code (IaC)</h3>
<p>Managing servers, networks, and databases via configuration files (e.g., Terraform, CloudFormation). This allows infrastructure to be version-controlled, reviewed, and audited just like application code.</p>
        """
    },
    {
        "id": "de-design",
        "title": "14. DE-Specific Design",
        "icon": "database",
        "description": "Architectures for Big Data: Lambda, Kappa, and CDC.",
        "content": """
<h2>Engineering the Data Lifecycle</h2>
<p>Data engineering systems differ from standard apps in their focus on massive state, consistency across hops, and analytical performance.</p>

<h3>The Lambda Architecture</h3>
<p>Addresses the problem of high-latency batch processing by adding a real-time "speed layer".</p>
<div class="my-8 p-6 bg-white dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-xl not-prose">
<div class="mermaid text-center">
graph TD
    Data[Incoming Data] --> Batch[Batch Layer: High Accuracy]
    Data --> Speed[Speed Layer: Low Latency]
    Batch --> View[Serving Layer]
    Speed --> View
    View --> User[User Query]
</div>
</div>

<h3>Kappa Architecture</h3>
<p>A simplification of Lambda. It treats EVERYTHING as a stream. If you need to re-run historical data, you simply "replay" the log from the beginning. (Enabled by tools like Apache Kafka).</p>

<h3>CDC: Change Data Capture</h3>
<p>Capturing the changes made to a source database in real-time. Instead of querying a DB every hour (expensive), CDC listens to the DB's **Transaction Log** (WAL) and streams every Insert/Update to the warehouse.</p>

<div class="p-5 bg-amber-50 dark:bg-amber-900/10 border border-amber-200 dark:border-amber-800 rounded-xl my-8">
    <h4 class="font-bold text-amber-700">The Medallion Architecture</h4>
    <p class="text-sm opacity-90 mt-2">A data design pattern used to organize data into layers of increasing quality:</p>
    <ul class="text-xs mt-3 space-y-2 list-none">
        <li>🟫 <strong>Bronze:</strong> Raw, unprocessed data. The "Source of Truth".</li>
        <li>⬜ <strong>Silver:</strong> Cleaned, filtered, and joined data. Validated schema.</li>
        <li>🟨 <strong>Gold:</strong> Aggregated and highly optimized data for business users and BI tools.</li>
    </ul>
</div>
        """
    },
    {
        "id": "classic-problems",
        "title": "15. Classic Problems",
        "icon": "layout",
        "description": "Deep dives into TinyURL, Rate Limiters, and Feed Designs.",
        "content": """
<h2>Applying the Theory</h2>
<p>The best way to master system design is to see how these blocks fit together to solve real-world problems.</p>

<div class="space-y-12">
    <section>
        <h3 class="text-blue-600">Problem 1: Design TinyURL</h3>
        <p class="text-sm italic mb-4">"How do we generate short, unique keys for 10 billion URLs?"</p>
        <ul class="text-sm space-y-2">
            <li><strong>Key Generation:</strong> Use Base62 encoding (a-z, A-Z, 0-9) to turn IDs into short strings.</li>
            <li><strong>Optimization:</strong> A **Key Generation Service (KGS)** pre-generates millions of keys and stores them in a separate DB to avoid runtime collisions.</li>
            <li><strong>Scaling:</strong> Use a write-back cache for new URLs and an aggressive LRU cache for popular ones.</li>
        </ul>
    </section>

    <section>
        <h3 class="text-emerald-600">Problem 2: Design a News Feed</h3>
        <p class="text-sm italic mb-4">"How do we show a user what their 500 friends just posted?"</p>
        <ul class="text-sm space-y-2">
            <li><strong>The Fan-out Problem:</strong> When a user posts, do we "Push" to all followers or let followers "Pull" on refresh?</li>
            <li><strong>Hybrid Approach:</strong> Push for regular users. Pull for celebrities (don't push a Taylor Swift post to 200M people instantly).</li>
            <li><strong>Storage:</strong> Use a Graph Database (like Neo4j) to track "Following" relationships.</li>
        </ul>
    </section>

    <section>
        <h3 class="text-rose-600">Problem 3: Design a Rate Limiter</h3>
        <p class="text-sm italic mb-4">"How do we prevent a user from calling an API more than 100 times/minute?"</p>
        <ul class="text-sm space-y-2">
            <li><strong>Algorithm:</strong> **Token Bucket** is standard. It allows for bursts of traffic while maintaining a strict average rate.</li>
            <li><strong>Distributed:</strong> Use **Redis** to store the counters. It's fast and supports atomic increments (INCR) to avoid race conditions.</li>
        </ul>
    </section>
</div>

<h3>How to Pass a System Design Interview</h3>
<ol class="text-sm space-y-3 mt-8">
    <li><strong>Step 1: Clarify Requirements.</strong> Ask about scale (DAU), read/write ratio, and data retention.</li>
    <li><strong>Step 2: Propose High-Level Design.</strong> Draw the 4-5 main boxes (LB, App, DB, Cache).</li>
    <li><strong>Step 3: Deep Dive into Components.</strong> Explain why you chose SQL over NoSQL or Kafka over RabbitMQ.</li>
    <li><strong>Step 4: Identify Bottlenecks.</strong> What happens if the DB fails? How do you scale the cache?</li>
</ol>
        """
    }
]

hub_template = '''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Design — Data Sheets</title>
    <script>(function(){{const s=localStorage.getItem('ds-theme');if(s==='light')document.documentElement.classList.remove('dark');else document.documentElement.classList.add('dark');}})();</script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body{{font-family:'Inter',sans-serif;}}
        .font-display,h1,h2,h3{{font-family:'Outfit',sans-serif;}}
        .grid-bg{{background-image:linear-gradient(rgba(0,0,0,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.05) 1px,transparent 1px);background-size:40px 40px;}}
        .dark .grid-bg{{background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);}}
        .topic-card{{transition:all 0.2s;}}
        .topic-card:hover{{transform:translateY(-2px);}}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen transition-colors duration-300">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>
<div class="fixed top-0 left-0 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none z-0"></div>

<!-- NAV -->
<nav class="fixed top-0 w-full z-50 bg-white/90 dark:bg-slate-950/90 backdrop-blur-xl border-b border-slate-200 dark:border-slate-800/60 transition-colors duration-300">
    <div class="max-w-7xl mx-auto px-4 md:px-6 py-3 md:py-4 flex items-center justify-between">
        <a href="../../index.html" class="no-underline"><span style="font-family:'Outfit',sans-serif;font-weight:700;letter-spacing:-.02em;" class="text-base md:text-xl text-slate-900 dark:text-slate-100 transition-colors duration-300">Data Sheets</span></a>
        <div class="flex items-center gap-1">
            <a href="../learn.html" class="px-3 md:px-5 py-2 rounded-lg text-sm font-medium text-slate-900 dark:text-white bg-slate-100 dark:bg-white/10 transition-colors no-underline">Learn</a>
            <a href="../practice.html" class="px-3 md:px-5 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-all no-underline">Practice</a>
        </div>
        <button id="theme-toggle" class="w-9 h-9 flex items-center justify-center rounded-lg text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-all">
            <i data-lucide="sun" class="w-5 h-5 hidden dark:block"></i>
            <i data-lucide="moon" class="w-5 h-5 block dark:hidden"></i>
        </button>
    </div>
</nav>

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
            <p class="text-slate-600 dark:text-slate-400 mt-2 text-lg">Master the art of building scalable, reliable, and maintainable distributed systems.</p>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {cards_html}
    </div>
</main>
<script>
lucide.createIcons();
document.getElementById('theme-toggle').addEventListener('click',()=>{{
    const d=document.documentElement.classList.toggle('dark');
    localStorage.setItem('ds-theme', d?'dark':'light');
}});
</script>
</body>
</html>'''

subpage_template = '''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — System Design</title>
    <script>(function(){{const s=localStorage.getItem('ds-theme');if(s==='light')document.documentElement.classList.remove('dark');else document.documentElement.classList.add('dark');}})();</script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ 
            startOnLoad: true, 
            theme: document.documentElement.classList.contains('dark') ? 'dark' : 'default',
            fontFamily: 'Inter',
            themeVariables: {{
                fontFamily: 'Inter',
                fontSize: '13px'
            }}
        }});
        window.mermaid = mermaid;
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    <style>
        body{{font-family:'Inter',sans-serif;}}
        .font-display,h1,h2,h3{{font-family:'Outfit',sans-serif;}}
        .prose h2{{margin-top:2.5rem;margin-bottom:1.25rem;font-weight:700;color:inherit;font-size:2.25rem;letter-spacing:-0.02em;}}
        .prose h3{{margin-top:2rem;margin-bottom:1rem;font-weight:600;color:inherit;font-size:1.6rem;letter-spacing:-0.01em;}}
        .prose p{{margin-bottom:1.25rem;line-height:1.8;opacity:0.9;}}
        .prose ul{{list-style-type:disc;padding-left:1.5rem;margin-bottom:1.25rem;}}
        .prose li{{margin-bottom:0.6rem;}}
        .prose code{{background:rgba(0,0,0,0.05);padding:0.2rem 0.4rem;border-radius:0.25rem;font-size:0.875em;font-weight:500;}}
        .dark .prose code{{background:rgba(255,255,255,0.1);}}
        .grid-bg{{background-image:linear-gradient(rgba(0,0,0,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.05) 1px,transparent 1px);background-size:40px 40px;}}
        .dark .grid-bg{{background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);}}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen transition-colors duration-300">
<div class="fixed inset-0 grid-bg pointer-events-none opacity-60 z-0"></div>

<!-- NAV -->
<nav class="fixed top-0 w-full z-50 bg-white/90 dark:bg-slate-950/90 backdrop-blur-xl border-b border-slate-200 dark:border-slate-800/60 transition-colors duration-300">
    <div class="max-w-7xl mx-auto px-4 md:px-6 py-3 md:py-4 flex items-center justify-between">
        <a href="../../../index.html" class="no-underline"><span style="font-family:'Outfit',sans-serif;font-weight:700;letter-spacing:-.02em;" class="text-base md:text-xl text-slate-900 dark:text-slate-100 transition-colors duration-300">Data Sheets</span></a>
        <div class="flex items-center gap-1">
            <a href="../../learn.html" class="px-3 md:px-5 py-2 rounded-lg text-sm font-medium text-slate-900 dark:text-white bg-slate-100 dark:bg-white/10 transition-colors no-underline">Learn</a>
            <a href="../../practice.html" class="px-3 md:px-5 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-all no-underline">Practice</a>
        </div>
        <button id="theme-toggle" class="w-9 h-9 flex items-center justify-center rounded-lg text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-all">
            <i data-lucide="sun" class="w-5 h-5 hidden dark:block"></i>
            <i data-lucide="moon" class="w-5 h-5 block dark:hidden"></i>
        </button>
    </div>
</nav>

<main class="relative z-10 pt-28 pb-20 px-6 max-w-4xl mx-auto">
    <a href="../system-design.html" class="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm mb-8 no-underline transition-colors duration-200">
        <i data-lucide="arrow-left" class="w-4 h-4"></i>
        Back to System Design
    </a>

    <header class="mb-12">
        <h1 class="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4 leading-tight tracking-tight">{title}</h1>
        <p class="text-xl text-slate-600 dark:text-slate-400 font-medium">{description}</p>
    </header>

    <article class="prose dark:prose-invert max-w-none pb-20">
        {content}
    </article>

    <div class="mt-16 pt-8 border-t border-slate-200 dark:border-slate-800 flex justify-between items-center">
        {prev_link}
        {next_link}
    </div>
</main>

<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script>
lucide.createIcons();
document.getElementById('theme-toggle').addEventListener('click',()=>{{
    const d=document.documentElement.classList.toggle('dark');
    localStorage.setItem('ds-theme', d?'dark':'light');
    location.reload();
}});
</script>
</body>
</html>'''

def build():
    os.makedirs('pages/learn/system-design', exist_ok=True)
    
    cards_html = ""
    for idx, page in enumerate(subpages):
        cards_html += f'''
        <a href="system-design/{page['id']}.html" class="topic-card group relative p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800/60 rounded-2xl no-underline transition-all hover:shadow-xl hover:shadow-blue-500/5 hover:border-blue-500/30 overflow-hidden">
            <div class="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <i data-lucide="{page['icon']}" class="w-16 h-16 text-blue-600"></i>
            </div>
            <div class="relative z-10">
                <div class="w-10 h-10 rounded-lg bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <i data-lucide="{page['icon']}" class="w-5 h-5"></i>
                </div>
                <h3 class="text-lg font-bold text-slate-900 dark:text-white mb-2">{page['title']}</h3>
                <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed mb-4">{page['description']}</p>
                <div class="flex items-center text-xs font-semibold text-blue-600 dark:text-blue-400 gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    Explore Module <i data-lucide="arrow-right" class="w-3 h-3"></i>
                </div>
            </div>
        </a>'''

    # Write Hub
    with open('pages/learn/system-design.html', 'w', encoding='utf-8') as f:
        f.write(hub_template.format(cards_html=cards_html))

    # Write Subpages
    for i, page in enumerate(subpages):
        prev_p = subpages[i-1] if i > 0 else None
        next_p = subpages[i+1] if i < len(subpages)-1 else None
        
        prev_link = f'''<a href="{prev_p['id']}.html" class="flex flex-col no-underline group">
            <span class="text-xs text-slate-500 mb-1 flex items-center gap-1"><i data-lucide="arrow-left" class="w-3 h-3"></i> Previous</span>
            <span class="text-sm font-bold text-slate-900 dark:text-white group-hover:text-blue-600 transition-colors">{prev_p['title']}</span>
        </a>''' if prev_p else '<div></div>'
        
        next_link = f'''<a href="{next_p['id']}.html" class="flex flex-col items-end no-underline group text-right">
            <span class="text-xs text-slate-500 mb-1 flex items-center gap-1">Next <i data-lucide="arrow-right" class="w-3 h-3"></i></span>
            <span class="text-sm font-bold text-slate-900 dark:text-white group-hover:text-blue-600 transition-colors">{next_p['title']}</span>
        </a>''' if next_p else '<div></div>'

        with open(f"pages/learn/system-design/{page['id']}.html", 'w', encoding='utf-8') as f:
            f.write(subpage_template.format(
                title=page['title'],
                description=page['description'],
                content=page['content'],
                prev_link=prev_link,
                next_link=next_link
            ))

    print("Successfully generated all System Design subpages!")

if __name__ == "__main__":
    build()


import glob
import os


def inject_sidebar_into_all_html():
    SIDEBAR_TEMPLATE = '''
<!-- SIDEBAR -->
<aside class="fixed top-16 left-0 h-[calc(100vh-4rem)] w-64 border-r border-slate-200 dark:border-slate-800/60 bg-white/50 dark:bg-slate-950/50 backdrop-blur-xl z-40 hidden lg:block overflow-y-auto py-8 px-6">
    <div class="mb-8">
        <a href="{prefix}learn.html" class="font-display font-bold text-slate-900 dark:text-white mb-4 text-sm uppercase tracking-wider block no-underline hover:text-blue-600 dark:hover:text-blue-400">Learn</a>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Programming</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/python.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Python</a></li>
                <li><a href="{prefix}learn/sql.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">SQL</a></li>
                <li><a href="{prefix}learn/bash.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Bash</a></li>
                <li><a href="{prefix}learn/powershell.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">PowerShell</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Concepts</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/de-fundamentals.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">DE Fundamentals</a></li>
                <li><a href="{prefix}learn/dsa-de.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">DSA for DE</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Tools</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/spark.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Spark</a></li>
                <li><a href="{prefix}learn/flink.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Flink</a></li>
                <li><a href="{prefix}learn/kafka.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Kafka</a></li>
                <li><a href="{prefix}learn/dbt.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">dbt</a></li>
                <li><a href="{prefix}learn/pandas.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Pandas</a></li>
                <li><a href="{prefix}learn/numpy.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">NumPy</a></li>
                <li><a href="{prefix}learn/airflow.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Airflow</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Cloud</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/aws.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">AWS</a></li>
                <li><a href="{prefix}learn/gcp.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">GCP</a></li>
                <li><a href="{prefix}learn/azure.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Azure</a></li>
                <li><a href="{prefix}learn/snowflake.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Snowflake</a></li>
                <li><a href="{prefix}learn/databricks.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Databricks</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">CI/CD</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/docker.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Docker</a></li>
                <li><a href="{prefix}learn/kubernetes.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Kubernetes</a></li>
                <li><a href="{prefix}learn/terraform.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Terraform</a></li>
                <li><a href="{prefix}learn/github.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">GitHub</a></li>
            </ul>
        </div>
        <div class="mb-6">
            <h5 class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase tracking-wider">Design</h5>
            <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
                <li><a href="{prefix}learn/system-design.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">System Design</a></li>
                <li><a href="{prefix}learn/pipeline-design.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Pipeline Design</a></li>
                <li><a href="{prefix}learn/de-architectures.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">DE Architectures</a></li>
            </ul>
        </div>
    </div>
    <div>
        <a href="{prefix}practice.html" class="font-display font-bold text-slate-900 dark:text-white mb-4 text-sm uppercase tracking-wider block no-underline hover:text-blue-600 dark:hover:text-blue-400">Practice</a>
        <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-400">
            <li><a href="{prefix}practice.html" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors no-underline">Coming Soon</a></li>
        </ul>
    </div>
</aside>
'''
    html_files = glob.glob('pages/**/*.html', recursive=True)
    for html_file in html_files:
        if html_file.replace(chr(92)*2, '/').replace(chr(92), '/') in ['pages/learn.html', 'pages/practice.html']:
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '<!-- SIDEBAR -->' in content:
            continue
            
        normalized = html_file.replace(chr(92)*2, '/').replace(chr(92), '/')
        depth = len(normalized.split('/')) - 1
        prefix = '../' * (depth - 1)
        
        sidebar_rendered = SIDEBAR_TEMPLATE.replace('{prefix}', prefix)
        
        if '</nav>' in content:
            content = content.replace('</nav>', '</nav>\n' + sidebar_rendered + '\n<div class="lg:pl-64 w-full">')
            content = content.replace('</body>', '</div>\n</body>')
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)

inject_sidebar_into_all_html()
