from flask import Flask, request, jsonify
from google.cloud import run_v2

app = Flask(__name__)

@app.route("/api/transcribe", methods=["POST"])
def transcribe():
    video_id = request.json["video_id"]

    client = run_v2.JobsClient()
    job = client.create_job(
        parent = "projects/steam-378309/locations/europe-west3",
        job={
            "name": "transcription-job",
            "launch_stage": run_v2.Job.LaunchStage.BETA,
            "template": {
                "containers": [
                    {
                        "image": "gcr.io/steam-378309/transcription-job",
                        "args": [video_id]
                    }
                ]
            }
        }
    )

    return jsonify({"message": "Transcription job started sucessfully."})

if __name__ == "__main__":
    app.run()