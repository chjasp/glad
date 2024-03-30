# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 8080

# Set the environment variables (if needed)
# ENV TG_TOKEN=your_telegram_bot_token
# ENV OPENAI_API_KEY=your_openai_api_key
# ENV GPT_MODEL_NAME=your_gpt_model_name

# Run the Flask application
CMD ["python", "-m", "app.main.py"]