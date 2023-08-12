# Dockerfile
FROM python:3.10-slim

WORKDIR /app
RUN mkdir -p /app/files

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./run.py"]

