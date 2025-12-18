#!/bin/zsh
set -e

APP_DIR="$HOME/latambeauty-app"
TMP_DIR="$APP_DIR/tmp"
TAR_DIR="$TMP_DIR/tar"

DATE=$(date +"%Y%m%d_%H%M%S")
EXPORT_NAME="latambeauty_code_${DATE}.tar"
EXPORT_PATH="$TAR_DIR/$EXPORT_NAME"

echo "🔍 LATAMBEAUTY Code Export 시작"
echo "📁 포함 대상:"
echo "   - backend/app"
echo "   - frontend/src"
echo "📦 생성 파일: $EXPORT_PATH"
echo ""

# ===== 디렉토리 검증 =====
if [[ ! -d "$APP_DIR/backend/app" ]]; then
  echo "❌ backend/app 디렉토리가 존재하지 않습니다"
  exit 1
fi

if [[ ! -d "$APP_DIR/frontend/src" ]]; then
  echo "❌ frontend/src 디렉토리가 존재하지 않습니다"
  exit 1
fi

if [[ ! -d "$TAR_DIR" ]]; then
  echo "❌ TAR 디렉토리가 존재하지 않습니다: $TAR_DIR"
  exit 1
fi

cd "$APP_DIR" || {
  echo "❌ 프로젝트 디렉토리 이동 실패"
  exit 1
}

# ===== 개발 코드만 tar로 묶기 =====
tar cvf "$EXPORT_PATH" \
  backend/app \
  frontend/src \
  --exclude="*/node_modules" \
  --exclude="*.pyc" \
  --exclude="__pycache__" \
  --exclude="*.log" \
  --exclude="*.DS_Store"

echo ""
echo "✅ Code Export 완료"
echo "➡️ 파일 위치: $EXPORT_PATH"
ls -lh "$EXPORT_PATH"