FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gfortran \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app

# Copy requirements file and upgrade pip tools.
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel

# Ensure your requirements.txt pins a numpy version that supports Python 3.10.
# For example, your file might have:
#    numpy>=1.25.0
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code.
COPY . /app/

EXPOSE 5000
CMD ["python", "app.py"]
