# Basisimage für Python 3.11 und VS Code Dev Container
FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Arbeitsverzeichnis
WORKDIR /workspace

# Nützliche Tools, Browser-Abhängigkeiten und Python-Pakete installieren
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
        netcat-openbsd \
        gnupg \
        lsb-release \
        wget \
        xvfb \
        fonts-liberation \
        libappindicator3-1 \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libcups2 \
        libdbus-1-3 \
        libgdk-pixbuf-xlib-2.0-0 \
        libnspr4 \
        libnss3 \
        libx11-xcb1 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        xdg-utils \
        unzip \
        chromium-driver && \
    rm -rf /var/lib/apt/lists/*

# Google Chrome installieren
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-linux-signing-key.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Python-Pakete für Django-Projekt
RUN pip install --no-cache-dir \
    django \
    djangorestframework \
    psycopg2-binary \
    gunicorn \
    dj-database-url \
    python-dotenv \
    requests \
    selenium

# Port für Django / API freigeben
EXPOSE 8000

# Standardbefehl (optional)
CMD ["bash"]
