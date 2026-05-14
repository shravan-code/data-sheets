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

roadmap_phases = [
    {
        "name": "Phase 1 — Design Fundamentals",
        "items": [
            {"name": "Architecture Basics", "id": "fundamentals"},
            {"name": "Requirement Analysis", "id": "fundamentals"},
            {"name": "Estimation (Back-of-Envelope)", "id": "fundamentals"},
            {"name": "SLA, SLO, and SLI", "id": "fundamentals"}
        ]
    },
    {
        "name": "Phase 2 — Scalability Patterns",
        "items": [
            {"name": "Vertical vs Horizontal Scaling", "id": "scalability"},
            {"name": "Load Balancing Algorithms", "id": "scalability"},
            {"name": "Database Sharding", "id": "scalability"},
            {"name": "Consistent Hashing", "id": "databases"}
        ]
    },
    {
        "name": "Phase 3 — Networking & Communication",
        "items": [
            {"name": "HTTP 1.1 / 2 / 3", "id": "networking"},
            {"name": "Proxies & Reverse Proxies", "id": "networking"},
            {"name": "API Gateways", "id": "networking"},
            {"name": "CDN & Edge Computing", "id": "networking"}
        ]
    },
    {
        "name": "Phase 4 — Data Persistence",
        "items": [
            {"name": "SQL vs NoSQL", "id": "databases"},
            {"name": "ACID vs BASE", "id": "databases"},
            {"name": "CAP Theorem", "id": "databases"},
            {"name": "Indexing & Partitioning", "id": "databases"}
        ]
    },
    {
        "name": "Phase 5 — High-Performance Caching",
        "items": [
            {"name": "Cache Aside / Write-Through", "id": "caching"},
            {"name": "Eviction (LRU, LFU, TTL)", "id": "caching"},
            {"name": "Distributed Caching (Redis)", "id": "caching"}
        ]
    },
    {
        "name": "Phase 6 — Async Messaging",
        "items": [
            {"name": "Message Queues (RabbitMQ)", "id": "messaging-queues"},
            {"name": "Event Streaming (Kafka)", "id": "messaging-queues"},
            {"name": "Delivery Guarantees", "id": "messaging-queues"}
        ]
    },
    {
        "name": "Phase 7 — Microservices & API Design",
        "items": [
            {"name": "RESTful API Best Practices", "id": "networking"},
            {"name": "gRPC & Protocol Buffers", "id": "networking"},
            {"name": "GraphQL Fundamentals", "id": "networking"},
            {"name": "Service Discovery", "id": "scalability"}
        ]
    },
    {
        "name": "Phase 8 — Security & Identity",
        "items": [
            {"name": "OAuth2 & OpenID Connect", "id": "networking"},
            {"name": "JWT Authentication", "id": "networking"},
            {"name": "TLS/SSL Encryption", "id": "networking"},
            {"name": "Role-Based Access Control", "id": "networking"}
        ]
    },
    {
        "name": "Phase 9 — Reliability & Monitoring",
        "items": [
            {"name": "Circuit Breakers & Retries", "id": "fundamentals"},
            {"name": "Rate Limiting Patterns", "id": "networking"},
            {"name": "Distributed Tracing", "id": "fundamentals"},
            {"name": "Log Aggregation", "id": "fundamentals"}
        ]
    },
    {
        "name": "Phase 10 — Cloud Native & Infra",
        "items": [
            {"name": "Docker & Containerization", "id": "scalability"},
            {"name": "Kubernetes Orchestration", "id": "scalability"},
            {"name": "Serverless Architectures", "id": "scalability"},
            {"name": "Infrastructure as Code", "id": "fundamentals"}
        ]
    },
    {
        "name": "Phase 11 — Design Interviews & Cases",
        "items": [
            {"name": "Twitter/X Timeline Design", "id": "messaging-queues"},
            {"name": "Uber/Lyft Proximity Design", "id": "databases"},
            {"name": "Netflix Content Delivery", "id": "networking"},
            {"name": "Standard Interview Template", "id": "fundamentals"}
        ]
    }
]

hub_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>System Design Roadmap — Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
            <header class="roadmap-hero-bg mb-20 p-10 md:p-14 rounded-[48px] border-2 border-blue-100 dark:border-slate-800 bg-white dark:bg-slate-900 relative overflow-hidden shadow-2xl shadow-blue-500/10">
                <div class="absolute -top-24 -right-24 w-80 h-80 bg-blue-500/10 blur-[100px] rounded-full"></div>
                <div class="absolute -bottom-24 -left-24 w-80 h-80 bg-indigo-500/5 blur-[100px] rounded-full"></div>
                
                <div class="relative z-10">
                    <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-100 text-blue-700 rounded-full text-xs font-black uppercase tracking-widest mb-8 border-2 border-blue-200/50">
                        <i data-lucide="map" class="w-4 h-4"></i>
                        Ultimate Learning Path
                    </div>
                    <h1 class="font-display text-5xl md:text-7xl font-black text-slate-900 dark:text-white mb-6 tracking-tight leading-[1.1]">
                        System <span class="bg-gradient-to-r from-blue-600 to-indigo-400 bg-clip-text text-transparent">Design</span>
                    </h1>
                    <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl leading-relaxed mb-0 font-medium italic">
                        "Master the architecture, patterns, and best practices for building massive-scale distributed systems."
                    </p>
                </div>
            </header>

            <!-- ROADMAP CONTENT -->
            <div class="max-w-4xl mx-auto">
                {phases_html}
            </div>

            <footer class="mt-20 py-10 border-t border-slate-200 dark:border-slate-800 text-center">
                <p class="text-slate-400 font-medium">© 2026 Data Cake • Path to Mastery</p>
            </footer>
        </main>
    </div>
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
        <a href="../system-design.html" class="inline-flex items-center gap-2 text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors mb-6 group no-underline">
            <i data-lucide="arrow-left" class="w-4 h-4 transition-transform group-hover:-translate-x-1"></i>
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

# 1. Build Roadmap Index
phases_html = ""
for i, phase in enumerate(roadmap_phases):
    num = i + 1
    items_html = ""
    for item in phase['items']:
        items_html += f"""
        <a href="system-design/{item['id']}.html" class="flex items-center gap-3 p-3 bg-blue-50/30 dark:bg-slate-900 border border-blue-100/50 dark:border-slate-800 rounded-xl transition-all hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:border-blue-200 group/item no-underline">
            <div class="w-2 h-2 rounded-full bg-blue-400 group-hover/item:scale-125 transition-transform"></div>
            <span class="text-sm font-semibold text-slate-700 dark:text-slate-300 group-hover/item:text-blue-700 transition-colors">{item['name']}</span>
        </a>"""

    phases_html += f"""
    <section class="mb-12">
        <div class="flex items-center gap-4 mb-8">
            <div class="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center text-blue-600">
                <span class="text-sm font-black">{num}</span>
            </div>
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white font-display tracking-tight">{phase['name'].split(' — ')[1]}</h2>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {items_html}
        </div>
    </section>"""

hub_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>System Design Mastery — Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Master the architecture, patterns, and best practices for building massive-scale distributed systems.">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
</head>
<body class="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-200 min-h-screen">
    <div id="ds-main-content">
        <main class="relative z-10 pt-24 pb-20 px-6 max-w-5xl mx-auto">
            <!-- HERO -->
            <header class="mb-20 text-center">
                <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-100 text-blue-700 rounded-full text-[10px] font-black uppercase tracking-widest mb-8 border-2 border-blue-200/50">
                    <i data-lucide="map" class="w-3 h-3"></i> Architecture Guide
                </div>
                <h1 class="font-display text-5xl md:text-7xl font-black text-slate-900 dark:text-white mb-6 tracking-tight leading-tight">
                    System <span class="bg-gradient-to-r from-blue-600 to-indigo-400 bg-clip-text text-transparent">Design</span>
                </h1>
                <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed font-medium italic">
                    "Master the architecture, patterns, and best practices for building massive-scale distributed systems."
                </p>
            </header>

            <!-- CARD CONTENT -->
            <div class="space-y-16">
                {phases_html}
            </div>
            
            <footer class="mt-20 py-10 border-t border-slate-200 dark:border-slate-800 text-center">
                <p class="text-slate-400 font-medium text-xs tracking-widest uppercase text-[10px]">\u00a9 2026 Data Cake \u2022 System Mastery</p>
            </footer>
        </main>
    </div>
    <script>lucide.createIcons();</script>
</body>
</html>'''

hub_content = hub_template.format(phases_html=phases_html)
os.makedirs("pages/learn", exist_ok=True)
with open("pages/learn/system-design.html", "w", encoding="utf-8") as f:
    f.write(hub_content)

# 2. Build Subpages
os.makedirs("pages/learn/system-design", exist_ok=True)
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

    # Inject Navigation Cards
    nav_html = f"""
    <div class="nav-container">
        {prev_html if prev_html else "<div></div>"}
        {next_html if next_html else "<div></div>"}
    </div>
    """
    content = content.replace('</main>', nav_html + '</main>')

    path = os.path.join("pages", "learn", "system-design", f"{page['id']}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Successfully generated System Design Roadmap!")
