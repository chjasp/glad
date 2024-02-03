import os
from flask import Flask, jsonify
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

PROJECT     = os.getenv("PROJECT")
BQ_DATASET  = os.getenv("BQ_DATASET")
BQ_TABLE    = os.getenv("BQ_TABLE")

app = Flask(__name__)
client = bigquery.Client()

@app.route("/")
def index():
    return "Welcome"

@app.route("/advice", methods=["GET"])
def get_advice():
    query = f"""
    SELECT * 
    FROM
    `{PROJECT}.{BQ_DATASET}.{BQ_TABLE}`
    WHERE video_id = 'CQlTmOFM4Qs' 
    """

    query_job = client.query(query)
    results = query_job.result()

    advice_list = []
    for row in results:
        advice_list.append({
            "topics": row.index,
            "advice": row.advice,
            "video_id": row.video_id
        })

    return jsonify(advice_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)