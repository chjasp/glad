import sys
import logging
from google.cloud import storage
from youtube_transcript_api import YouTubeTranscriptApi

logging.basicConfig(level=logging.INFO, format="%(funcName)s - %(message)s")

def upload_transcript_to_gcs(video_id, transcript_text, bucket_name):
    """Uploads the transcript text to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"{video_id}.txt")
    blob.upload_from_string(transcript_text)
    logging.info(f"Transcript from video {video_id} uploaded as {blob.name} to {bucket_name}.")

def get_and_upload_transcript(video_id, bucket_name):
    """Fetches transcript using YouTubeTranscriptApi and uploads it to GCS."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([item["text"] for item in transcript_list])
        logging.info("Transcript excerpt: " + transcript_text[:100])
        upload_transcript_to_gcs(video_id, transcript_text, bucket_name)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example for video_id: qTogNUV3CAI&t
    video_id = sys.argv[1]
    bucket_name = "legalm-staging"
    get_and_upload_transcript(video_id, bucket_name)
