#!/usr/bin/env bash
# Rollback Track-Runner to a previous commit or tag
# Usage: sudo bash deploy/rollback.sh <commit-hash>
set -euo pipefail

APP_DIR="/opt/track-runner"
APP_NAME="track-runner"

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

if [ $# -lt 1 ]; then
    echo "Usage: $0 <commit-hash>"
    echo "Current commits:"
    git -C "$APP_DIR" log --oneline -10
    exit 1
fi

TARGET="$1"

if [ ! -d "$APP_DIR/.git" ]; then
    echo "No deployment found at $APP_DIR"
    exit 1
fi

cd "$APP_DIR"

echo "[*] Saving current state..."
git stash 2>/dev/null || true

echo "[*] Checking out $TARGET..."
git fetch origin
git checkout "$TARGET"

echo "[*] Updating dependencies..."
sudo -u trackrunner "$APP_DIR/.venv/bin/uv" sync --no-dev

echo "[*] Running migrations..."
sudo -u trackrunner "$APP_DIR/.venv/bin/uv" run alembic upgrade head

echo "[*] Restarting service..."
systemctl restart $APP_NAME

echo "[v] Rolled back to $TARGET"
journalctl -u $APP_NAME --since "30 seconds ago" --no-pager
