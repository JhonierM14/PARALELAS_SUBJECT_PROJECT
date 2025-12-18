from flask import Flask, jsonify
import json
from pathlib import Path

app = Flask(__name__)

DATA_PATH = Path("/data/results/correlation.json")

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/correlation")
def correlation():
    if not DATA_PATH.exists():
        return jsonify({"error": "correlation.json not found"}), 404

    with open(DATA_PATH) as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
