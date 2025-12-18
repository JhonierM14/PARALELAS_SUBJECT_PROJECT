import json
import pandas as pd
from pathlib import Path

EVENTS = Path("/data/processed/events.json")
ICOLCAP = Path("/data/raw/icolcap.csv")
OUT = Path("/data/results")
OUT.mkdir(parents=True, exist_ok=True)

def main():
    # Cargar eventos
    events = json.loads(EVENTS.read_text())

    if len(events) == 0:
        events_df = pd.DataFrame(columns=["date", "event_count"])
    else:
        events_df = pd.DataFrame(events)
        events_df["date"] = pd.to_datetime(events_df["timestamp"]).dt.date
        events_df = (
            events_df.groupby("date")
            .size()
            .rename("event_count")
            .reset_index()
        )

    # Cargar ICOLCAP
    econ = pd.read_csv(ICOLCAP)
    econ["date"] = pd.to_datetime(econ["date"]).dt.date

    # Merge
    merged = econ.merge(events_df, on="date", how="left")
    merged["event_count"] = merged["event_count"].fillna(0)

    corr = merged["icolcap"].corr(merged["event_count"])

    merged["date"] = merged["date"].astype(str)

    result = {
        "correlation": None if pd.isna(corr) else float(corr),
        "data_points": merged.to_dict(orient="records")
    }

    out_file = OUT / "correlation.json"
    out_file.write_text(json.dumps(result, indent=2))
    print("Análisis completado correctamente")

if __name__ == "__main__":
    main()
