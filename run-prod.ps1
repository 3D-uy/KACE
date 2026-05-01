Write-Host "Running KACE in PROD mode 🚀"

docker compose build --no-cache
docker compose run --rm kace