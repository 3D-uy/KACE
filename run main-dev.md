DEV-MODE

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\run-dev.ps1

MAIN-MODE

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\run-prod.ps1

##########################################################################

docker-compose.dev.yml

services:
  kace:
    build: .
    container_name: kace-dev
    ports:
      - "3001:3000"
    volumes:
      - .:/app
    environment:
      - DEBUG=true
    stdin_open: true
    tty: true


docker-compose.yml  

services:
  kace:
    build: .
    container_name: kace
    stdin_open: true
    tty: true

##########################################################################   

🟢 run-dev.ps1

Write-Host "Running KACE in DEV mode 😈"

docker compose -f docker-compose.dev.yml build --no-cache
docker compose -f docker-compose.dev.yml run --rm kace


🔵 run-prod.ps1

Write-Host "Running KACE in PROD mode 🚀"

docker compose build --no-cache
docker compose run --rm kace

RUN;

.\run-dev.ps1

.\run-prod.ps1

##########################################################################   

Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "kace.py"]