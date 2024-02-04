import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
from google.cloud import bigquery
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

PROJECT = os.getenv("PROJECT")
BQ_DATASET = os.getenv("BQ_DATASET")
BQ_TABLE = os.getenv("BQ_TABLE")

app = Flask(__name__, template_folder="./static/templates/")
client = bigquery.Client()

CLIENT_ID = os.getenv("CLIENT_ID")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/verify_token", methods=["POST"])
def verify_token():
    data = request.get_json()
    token = data.get("token")
     
    if not token:
        return jsonify({"error": "No token provided"}), 400
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    except ValueError:
        return jsonify({"error": "Invalid token"}), 400
    user_email = id_info.get('email')
    if not user_email:
        return jsonify({"error": "No email in token"}), 400
    service = build('cloudresourcemanager', 'v1')
    policy = service.projects().getIamPolicy(resource=PROJECT, body={}).execute()
    print(policy)
    for binding in policy['bindings']:
        if binding['role'] in ['roles/run.invoker', 'roles/owner'] and f'user:{user_email}' in binding['members']:
            print("HAS ROLE")
            return render_template("admin.html")
            # return jsonify({"role": 'admin' if binding['role'] == 'roles/run.invoker' else 'regular'}), 200
    return render_template("regular.html")
    # return jsonify({"role": 'none'}), 200


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
            "index": row.index,
            "advice": row.advice,
            "video_id": row.video_id
        })

    return jsonify(advice_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
