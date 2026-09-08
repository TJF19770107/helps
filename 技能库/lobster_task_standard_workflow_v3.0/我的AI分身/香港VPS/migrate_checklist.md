# 不续费前 · 数据迁移/备份清单

## 1. 拉回数据（在本地执行）
rsync -avz --progress root@SERVER_IP:/opt /path/to/local/backup/
# 或打包下载
ssh root@SERVER_IP "tar -czf /tmp/backup.tar.gz -C / opt"
scp root@SERVER_IP:/tmp/backup.tar.gz ./

## 2. 关键配置清单（务必备份）
- /opt/sing-box/（代理配置）
- 任何 webhook/机器人/量化脚本
- 域名 DNS 记录（A 记录指向的 IP）

## 3. 迁移到新服务器
- 装好 sing-box，改 DNS A 记录 → 新 IP
- 重新部署服务（复用 server_setup.sh）

## 4. 下线
- 验证本地/新服务器运行正常后
- 取消自动续费，到期释放