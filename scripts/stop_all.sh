#!/bin/zsh

echo "🛑 Stopping ALL LatamBeauty Dev Servers..."

# FastAPI 종료
pkill -f "uvicorn app.main:app" || true

# frontend dev 종료
pkill -f "npm start" || true

echo "✔ All dev servers stopped."