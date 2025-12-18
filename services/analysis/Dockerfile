FROM python:3.11-slim

WORKDIR /app
COPY app/ /app/

RUN pip install pandas

VOLUME ["/data"]

CMD ["python", "analysis.py"]
