#!/usr/bin/env bash
# Track-Runner deploy script (IP-based, no HTTPS)
# Usage: sudo bash deploy/setup.sh
set -euo pipefail

APP_NAME="track-runner"
APP_USER="trackrunner"
APP_DIR="/opt/$APP_NAME"
REPO_URL="https://github.com/your/repo.git"
BRANCH="main"

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root: sudo bash deploy/setup.sh"
    exit 1
fi

VPS_IP=$(curl -s ifconfig.me)

echo "[*] Installing system packages..."
apt update
apt install -y nginx postgresql postgresql-client curl

if ! id "$APP_USER" &>/dev/null; then
    echo "[*] Creating system user $APP_USER..."
    useradd -r -s /bin/false -m -d "$APP_DIR" "$APP_USER"
fi

echo "[*] Setting up PostgreSQL..."
DB_PASS=$(openssl rand -base64 24)
sudo -u postgres psql -c "CREATE USER $APP_USER WITH PASSWORD '$DB_PASS';" 2>/dev/null || echo "  user already exists"
sudo -u postgres psql -c "CREATE DATABASE $APP_NAME OWNER $APP_USER;" 2>/dev/null || echo "  database already exists"
echo "DB_PASSWORD=$DB_PASS" >> /root/.deploy-secrets
chmod 600 /root/.deploy-secrets

echo "[*] Cloning repository..."
if [ -d "$APP_DIR/.git" ]; then
    cd "$APP_DIR"
    git fetch origin "$BRANCH"
    git reset --hard "origin/$BRANCH"
else
    git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
fi
cd "$APP_DIR"

echo "[*] Configuring .env..."
cp deploy/.env.template .env
SECRET_KEY=$(openssl rand -hex 32)
sed -i "s/change-me-in-production/$SECRET_KEY/" .env
sed -i "s|sqlite+aiosqlite:///./dev.db|postgresql+asyncpg://$APP_USER:$DB_PASS@localhost:5432/$APP_NAME|" .env
sed -i "s/<IP-АДРЕС-ВАШЕЙ-VPS>/$VPS_IP/" .env
sed -i "s/TRUSTED_PROXY=false/TRUSTED_PROXY=true/" .env

echo "[*] Installing uv and Python dependencies..."
if ! command -v uv &>/dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"
uv sync --no-dev --directory "$APP_DIR"
chown -R "$APP_USER":"$APP_USER" "$APP_DIR"

echo "[*] Installing systemd service..."
cp deploy/$APP_NAME.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now $APP_NAME

echo "[*] Configuring nginx..."
rm -f /etc/nginx/sites-enabled/default
cp deploy/nginx.conf /etc/nginx/sites-available/$APP_NAME
ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

echo "[*] Running initial migrations..."
sudo -u "$APP_USER" "$APP_DIR/.venv/bin/uv" run alembic upgrade head

echo "[v] Deploy complete!"
echo "  API:   http://$VPS_IP/health"
echo "  Logs:  journalctl -u $APP_NAME -f"
echo "  DB:    $APP_NAME@localhost"
