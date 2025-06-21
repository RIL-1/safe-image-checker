FROM python:3.9-slim

RUN apt-get update && apt-get install -y git && \
    pip install --no-cache-dir nudenet flask pillow

WORKDIR /app
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
