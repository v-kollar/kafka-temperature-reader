FROM python:3.9-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r scripts/requirements.txt

ENTRYPOINT ["python", "scripts/kafka-reader.py"]

