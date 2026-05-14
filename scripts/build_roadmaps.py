import os
import json

def build_roadmaps():
    roadmaps = [
        {
            "id": "data-engineering",
            "title": "Data Engineering",
            "subtitle": "Architecting the Future of Data",
            "description": "A comprehensive path to becoming a professional Data Engineer, covering everything from Linux foundations to advanced Data Mesh architectures.",
            "color": "indigo",
            "phases": [
                {"name": "Phase 1 — Programming Foundations", "items": ["Python", "SQL", "Bash", "Linux Fundamentals", "Networking Basics"]},
                {"name": "Phase 2 — CS Fundamentals", "items": ["DSA", "OOP Concepts", "Database Fundamentals"]},
                {"name": "Phase 3 — Data Libraries", "items": ["NumPy", "Pandas"]},
                {"name": "Phase 4 — Core DE Concepts", "items": ["DE Fundamentals", "Data Modeling", "Storage Formats", "Data Quality & Observability", "Data Governance"]},
                {"name": "Phase 5 — Databases & Storage", "items": ["PostgreSQL", "Redis", "Cassandra", "MongoDB", "DynamoDB"]},
                {"name": "Phase 6 — Big Data Processing", "items": ["Spark", "Kafka", "Flink"]},
                {"name": "Phase 7 — Transformation & Orchestration", "items": ["dbt", "Airflow", "Prefect / Dagster"]},
                {"name": "Phase 8 — Cloud Platforms", "items": ["AWS", "GCP / Azure", "Snowflake", "Databricks"]},
                {"name": "Phase 9 — Table Formats & Lakehouse", "items": ["Delta Lake", "Apache Iceberg", "Apache Hudi"]},
                {"name": "Phase 10 — Pipeline & System Design", "items": ["Pipeline Design", "System Design", "DE Architectures"]},
                {"name": "Phase 11 — DevOps & Infrastructure", "items": ["Docker", "Kubernetes", "Terraform", "GitHub Actions", "Ansible"]},
                {"name": "Phase 12 — Monitoring & Security", "items": ["Prometheus & Grafana", "OpenTelemetry", "Great Expectations", "IAM & Security", "Secret Management"]},
                {"name": "Phase 13 — Advanced Topics", "items": ["Data Mesh", "Data Contracts", "Reverse ETL", "PowerShell"]}
            ]
        },
        {
            "id": "ml-engineer",
            "title": "ML Engineer",
            "subtitle": "Bridging Science and Scale",
            "description": "Master the intersection of Software Engineering and Machine Learning to build and deploy production-grade models.",
            "color": "emerald",
            "phases": [
                {"name": "Phase 1 — Programming Foundations", "items": ["Python", "SQL", "Bash", "Linux Fundamentals", "Networking Basics"]},
                {"name": "Phase 2 — CS Fundamentals", "items": ["DSA", "OOP Concepts", "Probability & Statistics", "Linear Algebra", "Calculus"]},
                {"name": "Phase 3 — Data Libraries", "items": ["NumPy", "Pandas", "Matplotlib & Seaborn", "Scikit-learn"]},
                {"name": "Phase 4 — Machine Learning Fundamentals", "items": ["Supervised Learning", "Unsupervised Learning", "Model Evaluation & Metrics", "Feature Engineering", "Hyperparameter Tuning", "Cross Validation"]},
                {"name": "Phase 5 — Deep Learning", "items": ["Neural Networks", "TensorFlow / Keras", "PyTorch", "CNNs", "RNNs & LSTMs", "Transformers"]},
                {"name": "Phase 6 — Data Engineering for ML", "items": ["Data Pipelines", "Data Versioning (DVC)", "Feature Stores (Feast)", "Data Labeling"]},
                {"name": "Phase 7 — ML Frameworks & Tools", "items": ["XGBoost / LightGBM / CatBoost", "Hugging Face", "OpenCV", "NLTK / spaCy"]},
                {"name": "Phase 8 — MLOps", "items": ["MLflow", "Weights & Biases", "Kubeflow", "ZenML / Metaflow", "Model Registry", "Experiment Tracking"]},
                {"name": "Phase 9 — Model Deployment & Serving", "items": ["FastAPI / Flask", "Docker", "Kubernetes", "BentoML / Triton Inference Server", "REST & gRPC APIs"]},
                {"name": "Phase 10 — Cloud Platforms for ML", "items": ["AWS SageMaker", "GCP Vertex AI", "Azure ML", "Databricks"]},
                {"name": "Phase 11 — CI/CD for ML", "items": ["GitHub Actions", "Terraform", "Continuous Training Pipelines", "Model Monitoring & Drift Detection"]},
                {"name": "Phase 12 — Advanced Topics", "items": ["Distributed Training (Horovod, DeepSpeed)", "Quantization & Pruning", "Responsible AI & Fairness", "A/B Testing & Shadow Deployment", "LLM Fine-tuning"]}
            ]
        },
        {
            "id": "ai-engineer",
            "title": "AI Engineer",
            "subtitle": "The Generative Frontier",
            "description": "Focus on Large Language Models, AI Agents, and the modern Generative AI stack for building autonomous systems.",
            "color": "rose",
            "phases": [
                {"name": "Phase 1 — Programming Foundations", "items": ["Python", "SQL", "Bash", "Linux Fundamentals", "Networking & APIs"]},
                {"name": "Phase 2 — CS Fundamentals", "items": ["DSA", "OOP Concepts", "Probability & Statistics", "Linear Algebra"]},
                {"name": "Phase 3 — ML & Deep Learning Basics", "items": ["Machine Learning Fundamentals", "Neural Networks", "PyTorch / TensorFlow (basics)", "Scikit-learn"]},
                {"name": "Phase 4 — NLP & Language Models", "items": ["NLP Fundamentals", "Transformers Architecture", "Hugging Face Ecosystem", "Text Embeddings", "Tokenization", "Attention Mechanisms"]},
                {"name": "Phase 5 — Large Language Models", "items": ["LLM Architecture (GPT, BERT, T5, LLaMA)", "Prompt Engineering", "Few-shot & Zero-shot Learning", "Retrieval-Augmented Generation (RAG)", "Fine-tuning (LoRA, QLoRA, PEFT)", "LLM Evaluation"]},
                {"name": "Phase 6 — AI Frameworks & Tools", "items": ["LangChain", "LlamaIndex", "OpenAI API / Anthropic API", "Ollama", "vLLM"]},
                {"name": "Phase 7 — Vector Databases & Search", "items": ["Pinecone", "Weaviate", "Chroma", "Qdrant", "FAISS", "Semantic Search"]},
                {"name": "Phase 8 — AI Agents & Orchestration", "items": ["Agent Frameworks (LangGraph, AutoGen, CrewAI)", "Tool Use & Function Calling", "Memory Systems", "Multi-Agent Systems", "Agentic Pipelines"]},
                {"name": "Phase 9 — Multimodal AI", "items": ["Vision-Language Models (CLIP, LLaVA)", "Image Generation (Stable Diffusion, DALL\u00b7E)", "Speech & Audio (Whisper, TTS)", "Video Understanding"]},
                {"name": "Phase 10 — Deployment & Serving", "items": ["FastAPI", "Docker", "Kubernetes", "Triton Inference Server", "vLLM / TGI (Text Generation Inference)"]},
                {"name": "Phase 11 — Cloud Platforms for AI", "items": ["AWS Bedrock", "GCP Vertex AI", "Azure OpenAI Service", "Hugging Face Inference Endpoints"]},
                {"name": "Phase 12 — MLOps & AI Observability", "items": ["MLflow", "Weights & Biases", "LangSmith / LangFuse", "Prompt Versioning", "Model Monitoring & Drift Detection", "Guardrails & Safety"]},
                {"name": "Phase 13 — Advanced Topics", "items": ["RLHF & Constitutional AI", "Mixture of Experts (MoE)", "Speculative Decoding", "AI Safety & Alignment", "Responsible AI & Bias Mitigation", "Edge AI & On-device Inference"]}
            ]
        }
    ]

    os.makedirs(os.path.join('pages', 'roadmaps'), exist_ok=True)

    for rm in roadmaps:
        c = rm['color']
        phases_html = ""
        for i, phase in enumerate(rm['phases']):
            num = i + 1
            items_html = "".join([f"""
                <div class="flex items-center gap-3 p-3 bg-{c}-50/30 dark:bg-slate-900 border border-{c}-100/50 dark:border-slate-800 rounded-xl transition-all hover:bg-{c}-50 dark:hover:bg-{c}-900/20 hover:border-{c}-200 group/item">
                    <div class="w-2 h-2 rounded-full bg-{c}-400 group-hover/item:scale-125 transition-transform"></div>
                    <span class="text-sm font-semibold text-slate-700 dark:text-slate-300 group-hover/item:text-{c}-700 transition-colors">{item}</span>
                </div>""" for item in phase['items']])
            
            phases_html += f"""
            <div class="relative pl-12 pb-12 group last:pb-0">
                <!-- Timeline Line -->
                <div class="absolute left-[19px] top-0 bottom-0 w-0.5 bg-slate-200 dark:bg-slate-800 group-last:bottom-auto group-last:h-10"></div>
                
                <!-- Timeline Dot -->
                <div class="absolute left-0 top-0 w-10 h-10 rounded-full bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 flex items-center justify-center z-10 group-hover:border-{c}-500 transition-colors shadow-sm">
                    <span class="text-xs font-bold text-slate-500 group-hover:text-{c}-600">{num:02d}</span>
                </div>

                <div class="bg-white dark:bg-slate-900 border border-slate-200/60 dark:border-slate-800/60 p-6 rounded-3xl transition-all hover:shadow-xl hover:shadow-{c}-500/5">
                    <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-6 flex items-center gap-3">
                        {phase['name'].split(' \u2014 ')[1]}
                        <span class="text-[10px] uppercase tracking-widest px-2 py-1 bg-{c}-100 text-{c}-700 rounded-lg font-bold border border-{c}-200">Phase {num}</span>
                    </h3>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                        {items_html}
                    </div>
                </div>
            </div>"""

        template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>{rm['title']} Roadmap \u2014 Data Cake</title>
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
            <header class="roadmap-hero-bg mb-20 p-10 md:p-14 rounded-[48px] border-2 border-{c}-100 dark:border-slate-800 bg-white dark:bg-slate-900 relative overflow-hidden shadow-2xl shadow-{c}-500/10">
                <div class="absolute -top-24 -right-24 w-80 h-80 bg-{c}-500/10 blur-[100px] rounded-full"></div>
                <div class="absolute -bottom-24 -left-24 w-80 h-80 bg-blue-500/5 blur-[100px] rounded-full"></div>
                
                <div class="relative z-10">
                    <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-{c}-100 text-{c}-700 rounded-full text-xs font-black uppercase tracking-widest mb-8 border-2 border-{c}-200/50">
                        <i data-lucide="map" class="w-4 h-4"></i>
                        Ultimate Learning Path
                    </div>
                    <h1 class="font-display text-5xl md:text-7xl font-black text-slate-900 dark:text-white mb-6 tracking-tight leading-[1.1]">
                        {rm['title']} <span class="bg-gradient-to-r from-{c}-600 to-{c}-400 bg-clip-text text-transparent">Roadmap</span>
                    </h1>
                    <p class="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl leading-relaxed mb-0 font-medium italic">
                        "{rm['description']}"
                    </p>
                </div>
            </header>

            <!-- ROADMAP CONTENT -->
            <div class="max-w-4xl mx-auto">
                {phases_html}
            </div>

            <footer class="mt-20 py-10 border-t border-slate-200 dark:border-slate-800 text-center">
                <p class="text-slate-400 font-medium">\u00a9 2026 Data Cake \u2022 Path to Mastery</p>
            </footer>
        </main>
    </div>
</body>
</html>"""

        output_path = os.path.join('pages', 'roadmaps', f"{rm['id']}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"Built Roadmap: {output_path}")

if __name__ == "__main__":
    build_roadmaps()
