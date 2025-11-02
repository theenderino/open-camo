# Basisimage für Python 3.11 und VS Code Dev Container
FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Installiere nützliche Tools
RUN apt-get update && \
    apt-get install -y \
        procps \          # ps, pkill, top
        net-tools \       # netstat
        curl \            # HTTP Requests testen
        vim \ nano \      # Editoren
        htop \            # Prozessmonitor
        git \             # Versionskontrolle
        tree \            # Projektstruktur anzeigen
        unzip zip \       # Archive
        jq \              # JSON aufbereiten
        netcat \          # Ports testen
        && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis im Container
WORKDIR /workspace

# Installiere Python-Pakete für Django-Projekt
RUN pip install --no-cache-dir \
    django \
    djangorestframework \
    psycopg2-binary \
    gunicorn

# Expose Port für Django / API
EXPOSE 8000
