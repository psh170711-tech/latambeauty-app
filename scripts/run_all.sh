#!/bin/zsh

echo "🚀 Starting Backend + Frontend Together..."

# -------------------------
# Backend 실행 (백그라운드)
# -------------------------
cd ~/latambeauty-app/backend
source .venv/bin/activate

echo "✔ Backend starting..."
uvicorn app.main:app --reload > ~/latambeauty-app/logs/backend.log 2>&1 &

BACKEND_PID=$!
echo "✔ Backend running (PID: $BACKEND_PID)"

# -------------------------
# Frontend (Foreground)
# -------------------------
cd ~/latambeauty-app/frontend
echo "✔ Frontend starting..."

npm start

# -------------------------
# Frontend 종료 시 Backend도 종료
# -------------------------
echo "🛑 Stopping backend (PID: $BACKEND_PID)"
kill $BACKEND_PID 2>/dev/null || true

echo "✔ All processes stopped"