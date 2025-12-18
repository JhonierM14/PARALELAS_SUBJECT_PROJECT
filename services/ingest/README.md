# ingest

- Descarga noticias (Common Crawl).
- Ejecuta paralelismo I/O.
- Produce datos crudos.
- En producción: Lambda / Jobs en K8s.

# Desde la raiz del proyecto

<!-- 
docker build -t ingest-service services/ingest
 -->

Ejecutar en powershell o cmd

 <!-- 
 docker run --rm -v ${PWD}\data:/data ingest-service
  -->

Con esto se espera

<!-- 
Datos guardados en /data/raw/index_sample.json
 -->