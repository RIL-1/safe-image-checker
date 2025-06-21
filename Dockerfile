FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances système nécessaires pour OpenCV et NudeNet
RUN apt-get update && apt-get install -y \
    build-essential \
    libopenblas-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
RUN pip install --no-cache-dir nudenet==3.0.2 fastapi==0.115.0 uvicorn==0.32.0

# Copier les fichiers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

# Vérifier la présence de app.py
RUN ls -la /app && test -f /app/app.py || (echo "app.py not found" && exit 1)

# Configurer PYTHONPATH
ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]