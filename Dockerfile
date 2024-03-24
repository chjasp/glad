# Build stage for React frontend
FROM node:14 AS react-build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Final stage for Flask backend and React frontend
FROM python:3.9-slim

WORKDIR /app

# Install Flask dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask backend code
COPY backend/ .

# Copy built React frontend
COPY --from=react-build /app/build ./frontend/build

CMD ["python", "app.py"]
