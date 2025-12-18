import asyncio
import aiohttp
import json
import re
import boto3
import os
from datetime import datetime
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from io import BytesIO

def parse_boolean_query(query):
    """
    Convierte una consulta booleana en una expresión evaluable.
    Soporta: palabras, "frases exactas", y (AND), o (OR), paréntesis.
    """
    query = query.lower()
    query = re.sub(r'\by\b', 'and', query)
    query = re.sub(r'\bo\b', 'or', query)
    def replace_phrase(match):
        phrase = match.group(1).replace(' ', '_')
        return f'("{phrase}" in text)'
    query = re.sub(r'"([^"]+)"', replace_phrase, query)
    query = re.sub(r'(\b\w+\b)', r'("\1" in text)', query)
    query = query.replace('_', ' ')
    return query

def evaluate_query(text, query_expr):
    """
    Evalúa la expresión booleana en el contexto del texto (minúsculas).
    """
    text = text.lower()
    try:
        return eval(query_expr, {"__builtins__": {}}, {"text": text})
    except:
        return False

async def extract_text_from_warc_record(record):
    """
    Extrae el texto visible y el HTML crudo de un registro WARC.
    Retorna una tupla (texto_visible, html_crudo).
    """
    try:
        if record.rec_type == 'response' and 'html' in record.http_headers.get('Content-Type', '').lower():
            html_content = record.content_stream().read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html_content, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text(separator=' ', strip=True)
            return text, html_content
        return "", ""
    except Exception as e:
        print(f"Error al procesar WARC record: {e}")
        return "", ""

async def fetch_index_records(session, domain, crawl_id="CC-MAIN-2025-26"):
    """
    Consulta el índice de Common Crawl de forma asíncrona.
    """
    index_url = f"https://index.commoncrawl.org/{crawl_id}-index?url={domain}/*&output=json"
    try:
        async with session.get(index_url) as response:
            response.raise_for_status()
            records = []
            async for line in response.content:
                if line:
                    records.append(json.loads(line.decode('utf-8')))
            return records
    except Exception as e:
        print(f"Error al consultar índice de Common Crawl: {e}")
        return []

async def fetch_warc_content(session, warc_filename, offset, length):
    """
    Descarga un fragmento de un archivo WARC desde AWS S3 de forma asíncrona.
    """
    s3_url = f"https://data.commoncrawl.org/{warc_filename}"
    headers = {'Range': f'bytes={offset}-{offset+length-1}'}
    try:
        async with session.get(s3_url, headers=headers) as response:
            response.raise_for_status()
            return await response.read()
    except Exception as e:
        print(f"Error al descargar WARC: {e}")
        return None

def create_s3_prefix(domain, criterion):
    """
    Crea un prefijo para S3 con el formato dominio_criterio_fecha_hora.
    """
    safe_criterion = re.sub(r'[^\w\s-]', '', criterion.replace(' ', '-').lower())
    safe_criterion = re.sub(r'-+', '-', safe_criterion).strip('-')
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{domain}/{safe_criterion}/{timestamp}"

async def save_html_to_s3(url, html_content, s3_client, bucket, prefix, index):
    """
    Sube el contenido HTML a S3.
    """
    parsed_url = urlparse(url)
    path = parsed_url.path.strip('/').replace('/', '_')
    filename = path if path else f"page_{index}"
    filename = re.sub(r'[^\w\-]', '', filename) + '.html'
    s3_key = f"{prefix}/{filename}"
    
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=s3_key,
            Body=html_content.encode('utf-8'),
            ContentType='text/html'
        )
        print(f"Guardado en S3: s3://{bucket}/{s3_key}")
        return s3_key
    except Exception as e:
        print(f"Error al guardar en S3 {s3_key}: {e}")
        return None

async def process_warc_record(session, record, query_expr, s3_client, bucket, prefix, index, semaphore):
    """
    Procesa un registro WARC, verifica si cumple el criterio y guarda el HTML en S3 si es necesario.
    """
    async with semaphore:
        url = record.get('url', '')
        warc_filename = record.get('filename', '')
        offset = int(record.get('offset', 0))
        length = int(record.get('length', 0))

        warc_data = await fetch_warc_content(session, warc_filename, offset, length)
        if not warc_data:
            return None

        try:
            warc_stream = BytesIO(warc_data)
            for warc_record in ArchiveIterator(warc。第

System: It looks like the artifact content was cut off in the previous response. Below is the complete, corrected version of the script, continuing from where it was truncated, ensuring all functionality is included. The script is adapted for AWS Lambda, saves HTML content to S3, and includes the Lambda handler. I'll also provide the Dockerfile and detailed steps for deployment and invocation.

<xaiArtifact artifact_id="2b03c345-95e8-4399-80d1-0d87252a3336" artifact_version_id="a7f67787-eff1-4de9-9f6b-2062ee069232" title="cc_search_lambda.py" contentType="text/python">
import asyncio
import aiohttp
import json
import re
import boto3
import os
from datetime import datetime
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from io import BytesIO

def parse_boolean_query(query):
    """
    Convierte una consulta booleana en una expresión evaluable.
    Soporta: palabras, "frases exactas", y (AND), o (OR), paréntesis.
    """
    query = query.lower()
    query = re.sub(r'\by\b', 'and', query)
    query = re.sub(r'\bo\b', 'or', query)
    def replace_phrase(match):
        phrase = match.group(1).replace(' ', '_')
        return f'("{phrase}" in text)'
    query = re.sub(r'"([^"]+)"', replace_phrase, query)
    query = re.sub(r'(\b\w+\b)', r'("\1" in text)', query)
    query = query.replace('_', ' ')
    return query

def evaluate_query(text, query_expr):
    """
    Evalúa la expresión booleana en el contexto del texto (minúsculas).
    """
    text = text.lower()
    try:
        return eval(query_expr, {"__builtins__": {}}, {"text": text})
    except:
        return False

async def extract_text_from_warc_record(record):
    """
    Extrae el texto visible y el HTML crudo de un registro WARC.
    Retorna una tupla (texto_visible, html_crudo).
    """
    try:
        if record.rec_type == 'response' and 'html' in record.http_headers.get('Content-Type', '').lower():
            html_content = record.content_stream().read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html_content, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text(separator=' ', strip=True)
            return text, html_content
        return "", ""
    except Exception as e:
        print(f"Error al procesar WARC record: {e}")
        return "", ""

async def fetch_index_records(session, domain, crawl_id="CC-MAIN-2025-26"):
    """
    Consulta el índice de Common Crawl de forma asíncrona.
    """
    index_url = f"https://index.commoncrawl.org/{crawl_id}-index?url={domain}/*&output=json"
    try:
        async with session.get(index_url) as response:
            response.raise_for_status()
            records = []
            async for line in response.content:
                if line:
                    records.append(json.loads(line.decode('utf-8')))
            return records
    except Exception as e:
        print(f"Error al consultar índice de Common Crawl: {e}")
        return []

async def fetch_warc_content(session, warc_filename, offset, length):
    """
    Descarga un fragmento de un archivo WARC desde AWS S3 de forma asíncrona.
    """
    s3_url = f"https://data.commoncrawl.org/{warc_filename}"
    headers = {'Range': f'bytes={offset}-{offset+length-1}'}
    try:
        async with session.get(s3_url, headers=headers) as response:
            response.raise_for_status()
            return await response.read()
    except Exception as e:
        print(f"Error al descargar WARC: {e}")
        return None

def create_s3_prefix(domain, criterion):
    """
    Crea un prefijo para S3 con el formato dominio/criterio/fecha_hora.
    """
    safe_criterion = re.sub(r'[^\w\s-]', '', criterion.replace(' ', '-').lower())
    safe_criterion = re.sub(r'-+', '-', safe_criterion).strip('-')
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{domain}/{safe_criterion}/{timestamp}"

async def save_html_to_s3(url, html_content, s3_client, bucket, prefix, index):
    """
    Sube el contenido HTML a S3.
    """
    parsed_url = urlparse(url)
    path = parsed_url.path.strip('/').replace('/', '_')
    filename = path if path else f"page_{index}"
    filename = re.sub(r'[^\w\-]', '', filename) + '.html'
    s3_key = f"{prefix}/{filename}"
    
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=s3_key,
            Body=html_content.encode('utf-8'),
            ContentType='text/html'
        )
        print(f"Guardado en S3: s3://{bucket}/{s3_key}")
        return s3_key
    except Exception as e:
        print(f"Error al guardar en S3 {s3_key}: {e}")
        return None

async def process_warc_record(session, record, query_expr, s3_client, bucket, prefix, index, semaphore):
    """
    Procesa un registro WARC, verifica si cumple el criterio y guarda el HTML en S3 si es necesario.
    """
    async with semaphore:
        url = record.get('url', '')
        warc_filename = record.get('filename', '')
        offset = int(record.get('offset', 0))
        length = int(record.get('length', 0))

        warc_data = await fetch_warc_content(session, warc_filename, offset, length)
        if not warc_data:
            return None

        try:
            warc_stream = BytesIO(warc_data)
            for warc_record in ArchiveIterator(warc_stream):
                text, html_content = await extract_text_from_warc_record(warc_record)
                if text and evaluate_query(text, query_expr):
                    s3_key = await save_html_to_s3(url, html_content, s3_client, bucket, prefix, index)
                    if s3_key:
                        return {"url": url, "s3_path": f"s3://{bucket}/{s3_key}"}
        except Exception as e:
            print(f"Error procesando WARC para {url}: {e}")
        return None

async def search_common_crawl(domain, query, bucket, max_results=10, max_concurrent=10, crawl_id="CC-MAIN-2025-26"):
    """
    Busca páginas en Common Crawl de forma concurrente y guarda HTML en S3.
    """
    query_expr = parse_boolean_query(query)
    print(f"Expresión evaluable: {query_expr}")

    s3_client = boto3.client('s3')
    prefix = create_s3_prefix(domain, query)
    print(f"Guardando resultados en S3: s3://{bucket}/{prefix}")

    async with aiohttp.ClientSession() as session:
        index_records = await fetch_index_records(session, domain, crawl_id)
        if not index_records:
            print("No se encontraron registros en el índice para el dominio.")
            return []

        matching_pages = []
        processed_urls = set()
        semaphore = asyncio.Semaphore(max_concurrent)

        tasks = []
        for i, record in enumerate(index_records[:max_results], 1):
            url = record.get('url', '')
            if url in processed_urls:
                continue
            processed_urls.add(url)
            tasks.append(process_warc_record(session, record, query_expr, s3_client, bucket, prefix, i, semaphore))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, dict):
                matching_pages.append(result)

    return matching_pages

def lambda_handler(event, context):
    """
    Manejador de AWS Lambda.
    """
    try:
        domain = event.get('domain', '')
        criterion = event.get('criterion', '')
        bucket = event.get('bucket', '')
        max_results = event.get('max_results', 10)
        max_concurrent = event.get('max_concurrent', 10)
        crawl_id = event.get('crawl_id', 'CC-MAIN-2025-26')

        if not domain or not criterion or not bucket:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Faltan parámetros: domain, criterion, bucket'})
            }

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            search_common_crawl(domain, criterion, bucket, max_results, max_concurrent, crawl_id)
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'results': results,
                'message': f"Resultados guardados en s3://{bucket}/{create_s3_prefix(domain, criterion)}"
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# al final del archivo
if __name__ == "__main__":
    import argparse, asyncio
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True)
    parser.add_argument("--criterion", required=True)
    parser.add_argument("--bucket", default="local")
    parser.add_argument("--max_results", type=int, default=3)
    args = parser.parse_args()

    # si bucket == "local", usa cliente S3 local que escribe en ./data
    # (implementa una clase LocalS3Client con put_object que crea archivos locales)
    asyncio.run(search_common_crawl(args.domain, args.criterion, args.bucket, args.max_results))