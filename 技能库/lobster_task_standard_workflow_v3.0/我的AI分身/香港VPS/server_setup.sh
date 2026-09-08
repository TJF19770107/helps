#!/bin/bash
# 香港 VPS 一键部署（模板）· 需要在服务器上以 root 运行
# 用法：bash server_setup.sh YOUR_DOMAIN_OR_IP
# 说明：先填真实域名/IP，再运行。以下为 sing-box Hysteria2 示例，请按实际 sing-box 版本核对配置语法。
set -e
SRV="${1:-YOUR_SERVER_DOMAIN_OR_IP}"
PORT=8443
PASSWORD="$(head -c 24 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 20)"
echo "==> 安装 sing-box (Debian/Ubuntu)"
mkdir -p /opt/sing-box && cd /opt/sing-box
# 到 https://github.com/SagerNet/sing-box/releases 下载对应 linux-amd64 版本替换下面 URL
ARCH="amd64"
VER="1.10.0"
curl -L -o sing-box.tar.gz "https://github.com/SagerNet/sing-box/releases/download/v${VER}/sing-box-${VER}-linux-${ARCH}.tar.gz"
tar -xzf sing-box.tar.gz
cp sing-box-${VER}-linux-${ARCH}/sing-box /usr/local/bin/sing-box || true
chmod +x /usr/local/bin/sing-box || true

echo "==> 生成配置"
cat > /opt/sing-box/config.json <<EOF
{
  "log": {"level": "info"},
  "inbounds": [{
    "type": "hysteria2",
    "listen": "::",
    "listen_port": ${PORT},
    "users": [{"password": "${PASSWORD}"}],
    "ignore_client_bandwidth": false
  }],
  "outbounds": [{"type": "direct"}]
}
EOF

echo "==> 启动"
systemctl stop sing-box 2>/dev/null || true
cat > /etc/systemd/system/sing-box.service <<EOF
[Unit]
Description=sing-box
After=network.target
[Service]
ExecStart=/usr/local/bin/sing-box run -c /opt/sing-box/config.json
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable sing-box
systemctl start sing-box

echo "=============================================="
echo "部署完成。请在本地 client_singbox.yaml 填入："
echo "  服务器: ${SRV}"
echo "  端口: ${PORT}"
echo "  密码: ${PASSWORD}"
echo "=============================================="