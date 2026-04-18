Write-Host "Running KACE in DEV mode 😈"

docker compose -f docker-compose.dev.yml build --no-cache
docker compose -f docker-compose.dev.yml run --rm kace
