FROM python:3.11

WORKDIR /api_betano

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Instala dependências do Chrome e Chromedriver
RUN apt-get update && apt-get install -y \
    wget unzip xvfb \
    fonts-liberation libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libatspi2.0-0 libcups2 libdbus-1-3 \
    libdrm2 libgbm1 libgtk-3-0 libnspr4 libnss3 \
    libxcomposite1 libxdamage1 libxfixes3 libxkbcommon0 \
    libxrandr2 libvulkan1 xdg-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Instala Chrome (versão estável mais recente)
RUN wget -q -O /tmp/chrome.deb \
    "https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json | grep -oP '"version": "\K[^"]+')-1_amd64.deb" \
    && apt-get install -y /tmp/chrome.deb \
    && rm /tmp/chrome.deb

# Instala Chromedriver automaticamente (via webdriver-manager)
ENV CHROMEDRIVER_AUTO_INSTALL=true

# Copia requirements e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da API
COPY . /api_betano/

EXPOSE 3000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]