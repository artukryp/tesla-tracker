#!/bin/bash

VERSION=$(cat VERSION)

echo "🚀 [TeslaTracker] Instalador automático del bot Tesla tracker"

echo "----------------------------------------------"
echo "🚀 Instalando Tesla Tracker"
echo "🔖 Versión: $VERSION"
echo "----------------------------------------------"

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
USER="$(whoami)"

echo "1️⃣  Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

pip install --upgrade pip
pip install -r requirements.txt

echo "5️⃣  Generando archivo de servicio systemd..."
sudo tee /etc/systemd/system/tesla-tracker.service > /dev/null <<EOF
[Unit]
Description=Tesla Tracker
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/bin/python3 $PROJECT_DIR/tesla-tracker-scheduler.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo "6️⃣  Recargando demonio de systemd..."
sudo systemctl daemon-reload

echo "7️⃣  Habilitando servicio para inicio automático..."
sudo systemctl enable tesla-tracker.service

echo "8️⃣  Iniciando servicio..."
sudo systemctl start tesla-tracker.service

echo "----------------------------------------------"
echo "✅ Instalación completada."
echo "📡 Estado del bot:"
sudo systemctl status tesla-tracker.service