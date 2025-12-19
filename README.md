# PARALELAS_SUBJECT_PROJECT

# Proyecto Final – Infraestructuras en Ingeniería de Sistemas

Autor: JHONIER MENDEZ BRAVO - 2372226
Curso: Infraestructuras en Ingeniería de Sistemas

## Descripción general

Este proyecto implementa un prototipo de software distribuido y escalable para el procesamiento y análisis de información noticiosa proveniente de fuentes abiertas (Common Crawl), con el fin de identificar correlaciones entre eventos mediáticos y un indicador económico nacional (ICOLCAP).

El sistema está basado en contenedores Docker y se despliega en un entorno orquestado con Kubernetes (Minikube), demostrando conceptos de:
- computación paralela y distribuida
- escalabilidad
- tolerancia a fallos
- orquestación de servicios

---

## Tecnologias utilizadas
Tecnologías utilizadas

- Python 3
- Docker
- Docker Compose
- Kubernetes (Minikube)
- Flask
- Pandas
- Common Crawl
- AWS (arquitectura preparada para migración)


## Arquitectura del sistema

El sistema se divide en tres servicios principales:

1. **Ingest Service**
   - Descarga y procesa datos de Common Crawl
   - Extrae eventos noticiosos relevantes
   - Genera `events.json`

2. **Analysis Service**
   - Agrega eventos por fecha
   - Integra datos económicos (ICOLCAP)
   - Calcula correlación evento–economía
   - Genera `correlation.json`

3. **API Service**
   - Expone resultados vía REST API
   - Endpoints:
     - `/health`
     - `/correlation`

Todos los servicios comparten un volumen persistente (`PVC`).

---

## Estructura del proyecto

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
