#!/bin/zsh

APP_DIR="$HOME/latambeauty-app"
EXPORT_NAME="latambeauty_export_$(date +%Y%m%d_%H%M%S).tar"
EXPORT_PATH="$APP_DIR/$EXPORT_NAME"

echo "🔍 LATAMBEAUTY Export 시작..."
echo "📁 대상 디렉토리: $APP_DIR"
echo "📦 생성 파일: $EXPORT_PATH"

cd "$APP_DIR" || { echo "❌ 디렉토리 이동 실패"; exit 1 }

# 🔥 불필요한 파일/폴더 제외 목록
EXCLUDES=(
  --exclude="node_modules"
  --exclude="*/node_modules"
  --exclude="db-data"
  --exclude="logs"
  --exclude=".git"
  --exclude="*.tar"
  --exclude="*.tar.gz"
  --exclude="*.zip"
  --exclude="*.DS_Store"
  --exclude="**/.DS_Store"
)

# tar 생성
tar cvf "$EXPORT_PATH" \
  "${EXCLUDES[@]}" \
  .

echo "✅ Export 완료!"
echo "➡️ 파일 위치: $EXPORT_PATH"
ls -lh "$EXPORT_PATH"