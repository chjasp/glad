FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "job.py"]

# europe-west3-docker.pkg.dev/steam-378309/gulch/job:latest