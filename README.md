# PARALELAS_SUBJECT_PROJECT

#### Estructura

PARALELAS_SUBJECT_PROJECT/
├── services/
│   ├── ingest/
│   │   ├── Dockerfile
│   │   └── app/
│   │       └── ingest.py
│   │
│   ├── etl/
│   │   ├── Dockerfile
│   │   └── app/
│   │       └── etl.py
│   │
│   ├── analysis/
│   │   ├── Dockerfile
│   │   └── app/
│   │       └── analysis.py
│   │
│   ├── api/
│   │   ├── Dockerfile
│   │   └── app/
│   │       └── api.py
│   │
│   └── frontend/
│       ├── Dockerfile
│       └── app/
│           └── index.html ...
│
├── infra/
│   ├── docker-compose.yml
│   └── k8s/
│       ├── ingest.yaml
│       ├── etl.yaml
│       ├── analysis.yaml
│       ├── api.yaml
│       └── fronted.yaml
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── results/
│
├── docs/
│   └── architecture.md
│
└── README.md
