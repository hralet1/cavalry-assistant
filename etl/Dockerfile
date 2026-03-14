FROM python:3.11-slim

WORKDIR /app

COPY etl/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY etl/ ./

CMD ["python", "ingest.py", "--help"]
