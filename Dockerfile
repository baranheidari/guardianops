FROM python:3.11-slim

# System deps (optional but good practice)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Environment
ENV FLASK_ENV=production \
    FLASK_APP=app.py

EXPOSE 5000

# Use a production WSGI server instead of Flask dev server
# Make sure app.py exposes "app = Flask(__name__)"
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
