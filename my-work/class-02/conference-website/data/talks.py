"""
Conference Data Store for 1-Day Google Cloud Technologies Technical Conference
"""

CONFERENCE_INFO = {
    "name": "Google Cloud Tech Summit 2026",
    "subtitle": "Building Next-Gen Infrastructure & Intelligent AI Systems",
    "date": "October 24, 2026",
    "location": "Google Developer Hub, 345 Spear St, San Francisco, CA & Online",
    "time_zone": "PST (UTC-8)",
    "description": "Join leading industry experts, cloud architects, and AI researchers for an intensive 1-day deep dive into Google Cloud technologies, distributed architecture, and enterprise AI."
}

CATEGORIES = [
    {
        "id": "cat-1",
        "name": "Category 1",
        "label": "Cloud & DevOps Infrastructure",
        "color": "#4285F4"  # Google Blue
    },
    {
        "id": "cat-2",
        "name": "Category 2",
        "label": "AI & Data Engineering",
        "color": "#34A853"  # Google Green
    }
]

TALKS = [
    {
        "id": "talk-1",
        "title": "Architecting Resilient Multi-Region Applications on Google Kubernetes Engine",
        "time": "09:00 AM - 09:45 AM",
        "category_id": "cat-1",
        "category_name": "Category 1: Cloud & DevOps Infrastructure",
        "description": "Learn production-proven patterns for active-active multi-region deployments on GKE Enterprise. This session covers automated failover using Anthos Service Mesh, multi-cluster ingress routing, cross-region state management, and declarative GitOps workflows with Config Sync.",
        "speakers": [
            {
                "first_name": "Maya",
                "last_name": "Lin",
                "role": "Senior Cloud Architect",
                "company": "Google Cloud",
                "linkedin_url": "https://www.linkedin.com/in/mayalin-gcp"
            },
            {
                "first_name": "Alex",
                "last_name": "Rivera",
                "role": "Principal DevOps Engineer",
                "company": "CloudScale Systems",
                "linkedin_url": "https://www.linkedin.com/in/alexrivera-devops"
            }
        ]
    },
    {
        "id": "talk-2",
        "title": "Productionizing Generative AI with Vertex AI Agent Builder & Gemini 1.5 Pro",
        "time": "09:50 AM - 10:35 AM",
        "category_id": "cat-2",
        "category_name": "Category 2: AI & Data Engineering",
        "description": "A comprehensive walkthrough on building production-grade autonomous agent systems using Vertex AI Agent Builder and Gemini 1.5 Pro. Explore enterprise retrieval-augmented generation (RAG), groundings, custom tool integration, dynamic context windows, and real-time evaluation frameworks.",
        "speakers": [
            {
                "first_name": "Aris",
                "last_name": "Thorne",
                "role": "Lead AI Researcher",
                "company": "DeepMind Solutions",
                "linkedin_url": "https://www.linkedin.com/in/aris-thorne-ai"
            }
        ]
    },
    {
        "id": "talk-3",
        "title": "Zero-Trust Security & Enterprise Cloud IAM Strategy",
        "time": "10:40 AM - 11:25 AM",
        "category_id": "cat-1",
        "category_name": "Category 1: Cloud & DevOps Infrastructure",
        "description": "Explore practical strategies for implementing BeyondCorp zero-trust architecture in Google Cloud. Learn how to leverage Workload Identity Federation, IAM Recommender, Assured Workloads, and automated security posture management across complex multi-cloud organizations.",
        "speakers": [
            {
                "first_name": "Elena",
                "last_name": "Rostova",
                "role": "Head of Cloud Security",
                "company": "CyberGuard Inc.",
                "linkedin_url": "https://www.linkedin.com/in/elena-rostova-sec"
            },
            {
                "first_name": "David",
                "last_name": "Chen",
                "role": "Security Solutions Architect",
                "company": "Google Cloud",
                "linkedin_url": "https://www.linkedin.com/in/davidchen-gcpsec"
            }
        ]
    },
    {
        "id": "talk-4",
        "title": "Real-Time Streaming Analytics with Apache Beam and Cloud Dataflow",
        "time": "11:30 AM - 12:15 PM",
        "category_id": "cat-2",
        "category_name": "Category 2: AI & Data Engineering",
        "description": "Discover high-throughput streaming architecture with Apache Beam running on Cloud Dataflow Prime. Learn advanced windowing algorithms, stateful processing, late data handling, and dynamic resource allocation for processing millions of events per second with sub-second latency.",
        "speakers": [
            {
                "first_name": "Marcus",
                "last_name": "Vance",
                "role": "Principal Data Engineer",
                "company": "StreamLine Analytics",
                "linkedin_url": "https://www.linkedin.com/in/marcus-vance-data"
            }
        ]
    },
    {
        "id": "lunch-break",
        "is_break": True,
        "title": "Networking Lunch Break & Cloud Expo",
        "time": "12:15 PM - 01:15 PM",
        "duration": "60 Minutes",
        "description": "Enjoy a complimentary catered lunch, network with fellow engineers, and explore live technical demonstrations at the Google Cloud Partner Expo hall."
    },
    {
        "id": "talk-5",
        "title": "Global Database Operations with Cloud Spanner: Consistency Without Compromise",
        "time": "01:15 PM - 02:00 PM",
        "category_id": "cat-1",
        "category_name": "Category 1: Cloud & DevOps Infrastructure",
        "description": "Examine the inner workings of Cloud Spanner's TrueTime atomic clock synchronization and distributed consensus algorithm. Learn how to design global multi-region database schemas, handle zero-downtime online migrations, and optimize queries for high-throughput transactional applications.",
        "speakers": [
            {
                "first_name": "Sarah",
                "last_name": "Jenkins",
                "role": "Database Solutions Lead",
                "company": "DataGlobe Corp",
                "linkedin_url": "https://www.linkedin.com/in/sarah-jenkins-db"
            },
            {
                "first_name": "Kenji",
                "last_name": "Sato",
                "role": "Principal Staff Engineer",
                "company": "Spanner Core Team",
                "linkedin_url": "https://www.linkedin.com/in/kenjisato-spanner"
            }
        ]
    },
    {
        "id": "talk-6",
        "title": "High-Performance Data Warehousing & LLM Queries in BigQuery",
        "time": "02:05 PM - 02:50 PM",
        "category_id": "cat-2",
        "category_name": "Category 2: AI & Data Engineering",
        "description": "Unravel the convergence of data analytics and generative AI in BigQuery. Master BigQuery ML, vector embeddings, Remote Functions powered by Cloud Run, and partition clustering strategies to query structured data alongside multimodal AI models directly in SQL.",
        "speakers": [
            {
                "first_name": "Priya",
                "last_name": "Patel",
                "role": "Chief Data Officer",
                "company": "Analytics Engine",
                "linkedin_url": "https://www.linkedin.com/in/priya-patel-data"
            }
        ]
    },
    {
        "id": "talk-7",
        "title": "Serverless Microservices with Cloud Run, Eventarc, and Pub/Sub",
        "time": "02:55 PM - 03:40 PM",
        "category_id": "cat-1",
        "category_name": "Category 1: Cloud & DevOps Infrastructure",
        "description": "Build resilient, event-driven microservice architectures using Cloud Run and Eventarc. Learn how to implement scale-to-zero compute services, manage asynchronous event streams via Cloud Pub/Sub, integrate Direct VPC egress, and establish observability with Cloud Operations suite.",
        "speakers": [
            {
                "first_name": "Carlos",
                "last_name": "Gomez",
                "role": "Staff Serverless Architect",
                "company": "AppCloud Solutions",
                "linkedin_url": "https://www.linkedin.com/in/carlosgomez-serverless"
            }
        ]
    },
    {
        "id": "talk-8",
        "title": "Fine-Tuning Open Models on Cloud TPU v5p Pod Clusters",
        "time": "03:45 PM - 04:30 PM",
        "category_id": "cat-2",
        "category_name": "Category 2: AI & Data Engineering",
        "description": "Dive deep into hardware-accelerated model training on Google Cloud TPU v5p clusters. Learn efficient parallelization strategies (Tensor, Pipeline, Data parallelism), JAX/Flax optimization patterns, checkpoint management on Cloud Storage, and low-precision (bfloat16/FP8) model quantization.",
        "speakers": [
            {
                "first_name": "Hassan",
                "last_name": "Malik",
                "role": "Principal AI Compute Specialist",
                "company": "Compute Labs",
                "linkedin_url": "https://www.linkedin.com/in/hassan-malik-tpu"
            },
            {
                "first_name": "Emily",
                "last_name": "Zhang",
                "role": "ML Operations Lead",
                "company": "AI Scale Infrastructure",
                "linkedin_url": "https://www.linkedin.com/in/emilyzhang-mloops"
            }
        ]
    }
]
