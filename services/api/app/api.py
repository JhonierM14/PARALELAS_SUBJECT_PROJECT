from flask import Flask, jsonify
from flask_cors import CORS
import json
from pathlib import Path

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

RESULTS_DIR = Path("/data/results")
DATA_PATH = RESULTS_DIR / "correlation.json"


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/correlation")
def correlation():
    if not DATA_PATH.exists():
        return jsonify({
            "error": "correlation.json not found",
            "hint": "Run analysis-service before querying this endpoint"
        }), 404

    with DATA_PATH.open() as f:
        data = json.load(f)

    return jsonify(data), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
