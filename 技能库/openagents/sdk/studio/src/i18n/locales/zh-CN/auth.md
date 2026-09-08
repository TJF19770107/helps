# auth.json

原始格式: JSON

```json
{
    "login": {
        "title": "登录",
        "subtitle": "登录到您的账户",
        "emailLabel": "邮箱",
        "emailPlaceholder": "您的邮箱",
        "passwordLabel": "密码",
        "passwordPlaceholder": "您的密码",
        "nameLabel": "姓名",
        "namePlaceholder": "您的姓名",
        "submitButton": "登录",
        "forgotPassword": "忘记密码?",
        "noAccount": "还没有账户?",
        "signUp": "注册"
    },
    "networkSelection": {
        "title": "OpenAgents Studio",
        "subtitle": "连接到 OpenAgents 网络,开始与 AI 智能体协作"
    },
    "agentSetup": {
        "title": "加入 OpenAgents 网络",
        "subtitle": "选择您的智能体名称和组以连接到网络。",
        "adminSubtitle": "输入您的管理员密码以访问管理控制台。",
        "connectingTo": "正在连接到",
        "previousName": "之前使用的名称",
        "previousNameHint": "您可以使用之前的名称或创建一个新名称",
        "agentName": "智能体名称",
        "agentNamePlaceholder": "输入您的智能体名称...",
        "agentGroup": "智能体组",
        "loadingGroups": "加载组中...",
        "default": "默认",
        "defaultAgentGroup": "默认智能体组",
        "password": "密码",
        "passwordRequired": "需要密码",
        "passwordPlaceholder": "输入 '{{group}}' 组的密码...",
        "noPasswordRequired": "'{{group}}' 组不需要密码",
        "passwordRequiredHint": "用于 '{{group}}' 组",
        "nameSavedHint": "您的名称将自动保存到此网络。",
        "groupDescription": "{{group}} 组",
        "adminPassword": "管理员密码",
        "adminPasswordPlaceholder": "输入管理员密码...",
        "adminPasswordRequired": "需要管理员密码",
        "adminPasswordHint": "输入管理员组的密码以访问管理功能。",
        "backToRegularLogin": "返回普通登录",
        "or": "或",
        "buttons": {
            "randomName": "🎲 生成随机名称",
            "usePrevious": "↶ 使用之前的名称",
            "back": "← 返回",
            "connect": "以 {{name}} 连接",
            "connecting": "连接中...",
            "loginAsAdmin": "以管理员身份登录"
        },
        "errors": {
            "passwordRequired": "'{{group}}' 组需要密码",
            "invalidPassword": "'{{group}}' 组的密码无效",
            "invalidAdminPassword": "管理员密码无效。请重试。",
            "connectionFailed": "连接网络失败。请重试。",
            "adminConnectionFailed": "以管理员身份连接失败。请检查您的密码并重试。",
            "adminPasswordRequired": "需要管理员密码"
        }
    },
    "profile": {
        "title": "个人资料",
        "editProfile": "编辑资料",
        "nameLabel": "姓名",
        "namePlaceholder": "您的姓名",
        "avatarLabel": "头像链接",
        "avatarPlaceholder": "头像链接(可选)",
        "saveButton": "保存更改",
        "cancelButton": "取消"
    },
    "password": {
        "title": "输入密码",
        "subtitle": "此网络需要密码",
        "passwordLabel": "密码",
        "passwordPlaceholder": "输入您的密码...",
        "submitButton": "连接",
        "cancelButton": "取消",
        "incorrectPassword": "密码错误",
        "pleaseTryAgain": "请重试"
    },
    "localNetwork": {
        "title": "本地网络",
        "detecting": "检测本地网络中...",
        "notFound": "未检测到本地 OpenAgents 网络",
        "found": "本地 OpenAgents 网络",
        "runningOn": "运行于 {{host}}:{{port}}",
        "connect": "连接",
        "manageNetwork": "管理网络"
    },
    "manualNetwork": {
        "title": "手动连接",
        "tabs": {
            "quickConnect": "快速连接 主机 + 端口",
            "networkId": "网络 ID",
            "hostPort": "主机 + 端口"
        },
        "lastConnected": "上次连接的服务器",
        "lastUsedAs": "上次使用: <strong>{{name}}</strong>",
        "cached": "来自上次成功连接的缓存",
        "clearSaved": "清除已保存",
        "hostLabel": "主机",
        "hostPlaceholder": "localhost 或 IP 地址",
        "portLabel": "端口",
        "networkIdLabel": "网络 ID",
        "networkIdPlaceholder": "network-id-123 或 openagents://network-id",
        "hostPortHint": "输入主机地址和端口号以直接连接",
        "networkIdHint": "输入网络 ID 通过 OpenAgents 目录服务连接",
        "useHttps": "使用 SSL 连接",
        "connect": "连接",
        "connecting": "连接中...",
        "savedHint": "成功的连接将自动保存以便快速访问"
    }
}
```
