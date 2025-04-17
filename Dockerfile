FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gfortran \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the application code
COPY . /app/

# Set environment variables for production
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

EXPOSE 5000

# Fix the Gunicorn command - this was the main issue
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]