import asyncio
import aiohttp
import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("/data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

COMMON_CRAWL_INDEX = "https://index.commoncrawl.org/CC-MAIN-2025-26-index"

DOMAINS = [
    "eltiempo.com",
    "elespectador.com"
]

MAX_URLS = 5

async def fetch_index(session, domain):
    url = f"{COMMON_CRAWL_INDEX}?url={domain}/*&output=json"
    results = []
    async with session.get(url) as resp:
        async for line in resp.content:
            if line:
                results.append(json.loads(line))
                if len(results) >= MAX_URLS:
                    break
    return results

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_index(session, d) for d in DOMAINS]
        results = await asyncio.gather(*tasks)

    timestamp = datetime.utcnow().isoformat()
    output = {
        "timestamp": timestamp,
        "domains": DOMAINS,
        "results": results
    }

    out_file = DATA_DIR / "index_sample.json"
    out_file.write_text(json.dumps(output, indent=2))
    print(f"Datos guardados en {out_file}")

if __name__ == "__main__":
    asyncio.run(main())
