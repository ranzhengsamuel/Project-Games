"# Week 4 - FastAPI backend goes here" 
from flask import Flask, jsonify

import datetime

app = Flask(__name__)

LOG_FILE = "/data/requests.log"

@app.get("/health")

def health():

    with open(LOG_FILE, "a") as f:

        f.write(f"{datetime.datetime.now()} — health check\n")

    return jsonify({"status": "ok"})

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8000)