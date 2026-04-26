import os
import json

def build_roadmaps():
    roadmaps = [
        {
            "id": "data-engineering",
            "title": "Data Engineering Roadmap",
            "description": "A comprehensive path to becoming a professional Data Engineer.",
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
            "title": "ML Engineer Roadmap",
            "description": "Master the intersection of Software Engineering and Machine Learning.",
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
            "title": "AI Engineer Roadmap",
            "description": "Focus on Large Language Models, Agents, and Generative AI applications.",
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
        phases_html = ""
        for phase in rm['phases']:
            items_html = "".join([f'<li>{item}</li>' for item in phase['items']])
            phases_html += f"""
            <div class="roadmap-phase mb-10 relative pl-8 border-l-2 border-slate-200">
                <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-blue-500 border-4 border-white shadow-sm"></div>
                <h3 class="text-xl font-bold text-slate-800 mb-4">{phase['name']}</h3>
                <ul class="grid grid-cols-1 sm:grid-cols-2 gap-3 list-none p-0">
                    {"".join([f'<li class="flex items-center gap-2 text-slate-600 bg-white border border-slate-100 p-3 rounded-xl shadow-sm"><i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-500 flex-shrink-0"></i>{item}</li>' for item in phase['items']])}
                </ul>
            </div>"""

        template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>{rm['title']} \u2014 Data Cake</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{darkMode:'class',theme:{{extend:{{fontFamily:{{sans:['Inter','system-ui'],display:['Outfit','system-ui']}}}}}}}}</script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@0.395.0"></script>
    <style>
        .roadmap-phase:last-child {{ border-l-color: transparent; }}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen">
    <main class="relative z-10 pt-28 pb-20 px-6 max-w-4xl mx-auto">
        <header class="mb-16">
            <div class="flex items-center gap-4 mb-4">
                <div class="w-12 h-12 rounded-xl flex items-center justify-center bg-amber-100 text-amber-600">
                    <i data-lucide="map" class="w-7 h-7"></i>
                </div>
                <h1 class="text-4xl md:text-5xl font-bold text-slate-900 leading-tight tracking-tight">{rm['title']}</h1>
            </div>
            <p class="text-xl text-slate-600 max-w-3xl leading-relaxed">{rm['description']}</p>
        </header>

        <div class="roadmap-container">
            {phases_html}
        </div>
    </main>
</body>
</html>"""

        output_path = os.path.join('pages', 'roadmaps', f"{rm['id']}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"Built Roadmap: {output_path}")

if __name__ == "__main__":
    build_roadmaps()
