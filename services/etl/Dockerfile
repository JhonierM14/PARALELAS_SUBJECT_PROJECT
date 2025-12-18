FROM python:3.11-slim

WORKDIR /app
COPY app/ /app/

VOLUME ["/data"]

CMD ["python", "etl.py"]
