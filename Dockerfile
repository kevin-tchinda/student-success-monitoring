FROM python:3.12.1-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copier les requirements
COPY requirements.txt .

# Installer pip et mettre à jour
RUN python -m pip install --upgrade pip

# Installer les dépendances avec résolution flexible
RUN pip install --no-cache-dir -r requirements.txt

# Vérifier l'installation
RUN python -c "import sys; print(f'Python {sys.version}')"

# Copier le code
COPY api/ ./api/
COPY api/.env ./

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
