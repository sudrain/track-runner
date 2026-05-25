#!/usr/bin/env bash
# Track-Runner deploy script (backend + frontend)
# Требует: uv sync --no-dev уже выполнен от пользователя
# Usage: cd /opt/track-runner && sudo bash deploy/setup.sh
set -euo pipefail

APP_NAME="track-runner"
APP_DIR=$(pwd)

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root: sudo bash deploy/setup.sh"
    exit 1
fi

SERVICE_USER=$(stat -c '%U' "$APP_DIR")
VPS_IP=$(curl -s ifconfig.me)

echo "[*] Installing system packages..."
apt update
apt install -y nginx postgresql postgresql-client curl lsof apparmor-utils

echo "[*] Cleaning up any previous uvicorn on port 8000..."
fuser -k 8000/tcp 2>/dev/null || true

echo "[*] Setting up PostgreSQL..."
DB_USER="track_runner"
DB_PASS=$(openssl rand -hex 16)
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';" 2>/dev/null || echo "  user already exists"
sudo -u postgres psql -c "CREATE DATABASE \"$APP_NAME\" OWNER $DB_USER;" 2>/dev/null || echo "  database already exists"
echo "DB_PASSWORD=$DB_PASS" >> /root/.deploy-secrets
chmod 600 /root/.deploy-secrets

echo "[*] Configuring .env..."
cp deploy/.env.template .env
SECRET_KEY=$(openssl rand -hex 32)
sed -i "s/change-me-in-production/$SECRET_KEY/" .env
sed -i "s|sqlite+aiosqlite:///./dev.db|postgresql+asyncpg://$DB_USER:$DB_PASS@localhost:5432/$APP_NAME|" .env
sed -i "s/<IP-АДРЕС-ВАШЕЙ-VPS>/$VPS_IP/" .env
sed -i "s/TRUSTED_PROXY=false/TRUSTED_PROXY=true/" .env

echo "[*] Installing Node.js via nvm (user $SERVICE_USER)..."
if ! sudo -u "$SERVICE_USER" command -v node &>/dev/null; then
    sudo -u "$SERVICE_USER" bash -c '
        export NVM_DIR="$HOME/.nvm"
        if [ ! -d "$NVM_DIR" ]; then
            curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash
        fi
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
        nvm install 24
    '
fi

echo "[*] Building frontend..."
sudo -u "$SERVICE_USER" bash -c "
    export NVM_DIR=\"\$HOME/.nvm\"
    [ -s \"\$NVM_DIR/nvm.sh\" ] && \. \"\$NVM_DIR/nvm.sh\"
    cd \"$APP_DIR/frontend\"
    npm ci
    npm run build
"

echo "[*] Installing systemd service..."
systemctl stop $APP_NAME 2>/dev/null || true
sed -e "s|__APP_DIR__|$APP_DIR|g" \
    -e "s|__APP_USER__|$SERVICE_USER|g" \
    deploy/$APP_NAME.service > /etc/systemd/system/$APP_NAME.service
systemctl daemon-reload
systemctl enable --now $APP_NAME

echo "[*] Configuring nginx..."
rm -f /etc/nginx/sites-enabled/default
cp deploy/nginx.conf /etc/nginx/sites-available/$APP_NAME
ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
if command -v aa-complain &>/dev/null; then
    aa-complain /etc/apparmor.d/usr.sbin.nginx 2>/dev/null || true
fi

echo "[*] Running initial migrations..."
cd "$APP_DIR"
sudo -u "$SERVICE_USER" "$APP_DIR/.venv/bin/python" -m alembic upgrade head

echo "[v] Deploy complete!"
echo "  App:   http://$VPS_IP/"
echo "  API:   http://$VPS_IP/health"
echo "  Logs:  journalctl -u $APP_NAME -f"
echo "  DB:    $APP_NAME@localhost"

