FROM python:3.11

WORKDIR /api_betano

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxss1 libappindicator1 libasound2 libatk-bridge2.0-0 \
    libgtk-3-0 libx11-xcb1 libxcb-dri3-0 libdrm2 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux-signing-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

RUN pip install --upgrade pip setuptools wheel

ENV CHROMEDRIVER_AUTO_INSTALL=true

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /api_betano/

EXPOSE 3000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
