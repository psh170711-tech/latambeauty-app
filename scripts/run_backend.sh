#!/bin/zsh

echo "🚀 LatamBeauty Backend Starting..."

cd ~/latambeauty-app/backend

# 가상환경 활성화
source .venv/bin/activate

echo "✔ venv activated"
echo "✔ Running FastAPI at http://127.0.0.1:8000"

uvicorn app.main:app --reload
