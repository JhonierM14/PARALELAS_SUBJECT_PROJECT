# etl

- Limpia HTML.
- Extrae texto.
- Identifica keywords / eventos.
- Produce series temporales de eventos.

# Desde la raiz del proyecto

<!-- 
docker build -t etl-service services/etl
 -->

Ejecutar en powershell o cmd

<!-- 
 docker run --rm -v ${PWD}\data:/data etl-service
 -->

Con esto se espera

<!-- 
X eventos detectados
 -->

Y la generacion de un archivo <!-- data/processed/events.json -->