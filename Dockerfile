# Basisimage für Python 3.11 und VS Code Dev Container
FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Installiere nützliche Tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apt-utils \
        ca-certificates \
        procps \
        net-tools \
        curl \
        vim \
        nano \
        htop \
        git \
        tree \
        unzip \
        zip \
        jq \
        netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis im Container
WORKDIR /workspace

# Installiere Python-Pakete für Django-Projekt
RUN pip install --no-cache-dir \
    django \
    djangorestframework \
    psycopg2-binary \
    gunicorn \
    dj-database-url

# Expose Port für Django / API
EXPOSE 8000
