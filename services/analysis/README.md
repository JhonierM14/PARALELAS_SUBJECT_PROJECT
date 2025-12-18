# analysis

- Carga ICOLCAP.
- Cruza con eventos.
- Calcula correlaciones, lags, ventanas.
- Produce métricas numéricas.

# Desde la raiz del proyecto

<!-- 
docker build -t analysis-service services/analysis
 -->

Ejecutar en powershell o cmd

<!-- 
 docker run --rm -v ${PWD}\data:/data analysis-service
 -->

Con esto se espera

<!-- 
Análisis completado
 -->

Y la generacion de un archivo <!-- data/results/correlation.json -->