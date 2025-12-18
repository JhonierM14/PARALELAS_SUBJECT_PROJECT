import json
from pathlib import Path
from multiprocessing import Pool, cpu_count
from datetime import datetime
import re

RAW = Path("/data/raw/index_sample.json")
OUT = Path("/data/processed")
OUT.mkdir(parents=True, exist_ok=True)

KEYWORDS = [
    "protesta", "bloqueo", "paro",
    "manifestación", "huelga"
]

def process_record(record):
    url = record.get("url", "")
    text = json.dumps(record).lower()

    hits = [k for k in KEYWORDS if k in text]

    if hits:
        return {
            "url": url,
            "domain": record.get("url", "").split("/")[2],
            "keywords": hits,
            "timestamp": datetime.utcnow().isoformat()
        }
    return None

def main():
    data = json.loads(RAW.read_text())
    records = []

    for domain_data in data["results"]:
        records.extend(domain_data)

    with Pool(cpu_count()) as pool:
        results = pool.map(process_record, records)

    events = [r for r in results if r]

    out_file = OUT / "events.json"
    out_file.write_text(json.dumps(events, indent=2))
    print(f"{len(events)} eventos detectados")

if __name__ == "__main__":
    main()
