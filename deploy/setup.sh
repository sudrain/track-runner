#!/usr/bin/env bash
# Track-Runner deploy script (IP-based, no HTTPS)
# Usage: cd /path/to/track-runner && sudo bash deploy/setup.sh
set -euo pipefail

APP_NAME="track-runner"
APP_DIR=$(pwd)
VPS_IP=$(curl -s ifconfig.me)

# --- Определяем пользователя сервиса ---
# Если проект в /home/ — запускаем от владельца директории
# Иначе создаём trackrunner
if echo "$APP_DIR" | grep -q "^/home/"; then
    SERVICE_USER=$(stat -c '%U' "$APP_DIR")
    echo "[*] Detected home directory — running as $SERVICE_USER"
else
    SERVICE_USER="trackrunner"
    if ! id "$SERVICE_USER" &>/dev/null; then
        echo "[*] Creating system user $SERVICE_USER..."
        useradd -r -s /bin/false "$SERVICE_USER"
    fi
fi

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root: sudo bash deploy/setup.sh"
    exit 1
fi

echo "[*] Installing system packages..."
apt update
apt install -y nginx postgresql postgresql-client curl lsof apparmor-utils

echo "[*] Cleaning up any previous uvicorn on port 8000..."
fuser -k 8000/tcp 2>/dev/null || true

echo "[*] Setting up PostgreSQL..."
DB_USER="track_runner"
DB_PASS=$(openssl rand -base64 24)
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';" 2>/dev/null || echo "  user already exists"
sudo -u postgres psql -c "CREATE DATABASE $APP_NAME OWNER $DB_USER;" 2>/dev/null || echo "  database already exists"
echo "DB_PASSWORD=$DB_PASS" >> /root/.deploy-secrets
chmod 600 /root/.deploy-secrets

echo "[*] Configuring .env..."
cp deploy/.env.template .env
SECRET_KEY=$(openssl rand -hex 32)
sed -i "s/change-me-in-production/$SECRET_KEY/" .env
sed -i "s|sqlite+aiosqlite:///./dev.db|postgresql+asyncpg://$DB_USER:$DB_PASS@localhost:5432/$APP_NAME|" .env
sed -i "s/<IP-АДРЕС-ВАШЕЙ-VPS>/$VPS_IP/" .env
sed -i "s/TRUSTED_PROXY=false/TRUSTED_PROXY=true/" .env

echo "[*] Installing uv and Python dependencies..."
if ! command -v uv &>/dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"
uv sync --no-dev --directory "$APP_DIR"
chown -R "$SERVICE_USER":"$SERVICE_USER" "$APP_DIR"

echo "[*] Installing systemd service..."
# Останавливаем старый запуск, если был
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
# AppArmor может блокировать proxy_pass — переводим nginx в complain mode
if command -v aa-complain &>/dev/null; then
    aa-complain /etc/apparmor.d/usr.sbin.nginx 2>/dev/null || true
fi

echo "[*] Running initial migrations..."
cd "$APP_DIR"
sudo -u "$SERVICE_USER" "$APP_DIR/.venv/bin/python" -m alembic upgrade head

echo "[v] Deploy complete!"
echo "  API:   http://$VPS_IP/health"
echo "  Logs:  journalctl -u $APP_NAME -f"
echo "  DB:    $APP_NAME@localhost"
