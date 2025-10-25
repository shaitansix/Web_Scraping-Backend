FROM python:3.13-alpine
RUN mkdir -p /home/api
WORKDIR /home/api

RUN apk update && apk add --no-cache \
    wget \
    gnupg \
    unzip \
    curl \
    chromium \
    chromium-chromedriver

COPY requirements.txt .
RUN pip install --no-cache-dir --verbose -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]