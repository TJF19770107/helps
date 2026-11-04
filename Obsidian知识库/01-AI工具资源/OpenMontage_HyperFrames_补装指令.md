# OpenMontage + HyperFrames 补装指令

> 创建时间: 2026-06-27
> 标签: [补装指令] [待执行] [需外网] [视频工具]

## 前置条件

1. 网络环境: 切换至手机热点或其他可访问GitHub的网络
2. 端口验证: git clone 能正常连接 github.com:443
3. 磁盘空间: 至少预留 2GB

## 补装顺序: 先OpenMontage后HyperFrames

### Step 1: OpenMontage (全流程AI视频引擎)

    cd 'E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\video-tools'
    git clone https://github.com/calesthio/OpenMontage.git
    cd OpenMontage
    npm install
    node src/index.js --help

预期结果: 看到OpenMontage的CLI帮助信息，无报错

### Step 2: HyperFrames (HTML/CSS转视频)

    cd 'E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\video-tools'
    npx hyperframes init hyperframes
    cd hyperframes
    npm install
    npx hyperframes --version

预期结果: HyperFrames版本号输出，无报错

### Step 3: 全量验证

    Write-Host '--- 6大视频工具验证 ---'
    ffmpeg -version 2>&1 | Select-Object -First 1
    & 'C:\Users\Administrator\AppData\Local\Programs\Python\Python313\python.exe' -c 'import manim; print("Manim:", manim.__version__)'
    cd '...\remotion-project'; npx remotion --version
    cd '...\OpenMontage'; node src/index.js --version
    cd '...\hyperframes'; npx hyperframes --version
    Write-Host '--- 验证完成 ---'

## 常见问题

问题 -> 解决方案
git clone 超时 -> 切换手机热点/代理
npm install EPERM -> 检查D盘缓存权限,用 --cache 参数
npm init video 交互式卡住 -> 改用手动创建 package.json
磁盘空间不足 -> 降低安装规模或清理临时文件

## 关联索引

- 视频工具部署归档: ../01-视频工具/视频工具部署归档_20260627.md
- 卸载回滚脚本: ../02-工作规范/视频工具卸载回滚脚本.md
