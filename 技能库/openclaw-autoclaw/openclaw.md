# openclaw.json

原始格式: JSON

```json
{
  "meta": {
    "lastTouchedVersion": "2026.3.11",
    "lastTouchedAt": "2026-04-24T14:37:29.053Z"
  },
  "update": {
    "checkOnStart": false
  },
  "models": {
    "providers": {
      "zai": {
        "baseUrl": "https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw",
        "apiKey": "autoclaw-internal-proxy",
        "api": "openai-completions",
        "headers": {
          "x_trace_id": "autoclaw-desktop"
        },
        "models": [
          {
            "id": "zai_pony-alpha-2",
            "name": "GLM-5-Turbo",
            "input": [
              "text"
            ],
            "contextWindow": 204800,
            "maxTokens": 131072,
            "headers": {
              "X-Request-Model": "zai_pony-alpha-2",
              "X-Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MTgyNjcsImRldmljZV9pZCI6ImY3OThmZmU4LTg1YWMtNDg1Ni1iN2U5LTIyMDJlMThlODU0ZCIsInNvdXJjZV9pZCI6ImF1dG9jbGF3YWNjZXNzX3Rva2VuIiwiZ3VpZCI6IiIsImlzX2d1ZXN0IjpmYWxzZSwicG93ZXIiOjAsImV4cCI6MTc3NzE3NTIyMSwiaWF0IjoxNzc3MDg4ODIxLCJqdGkiOiIxMzM4MTA4NjM4MCJ9.j7TcM0vZ8eMkzxInBjdJQzKvl1PCrvMw0HdUP-j249A",
              "X-Tm": "win",
              "X-Version": "0.2.26",
              "X-Product": "autoclaw",
              "X-Channel": "official",
              "X-Lang": "zh-CN"
            }
          },
          {
            "id": "huawei_glm-5",
            "name": "GLM-5",
            "input": [
              "text"
            ],
            "contextWindow": 204800,
            "maxTokens": 131072,
            "headers": {
              "X-Request-Model": "huawei_glm-5",
              "X-Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MTgyNjcsImRldmljZV9pZCI6ImY3OThmZmU4LTg1YWMtNDg1Ni1iN2U5LTIyMDJlMThlODU0ZCIsInNvdXJjZV9pZCI6ImF1dG9jbGF3YWNjZXNzX3Rva2VuIiwiZ3VpZCI6IiIsImlzX2d1ZXN0IjpmYWxzZSwicG93ZXIiOjAsImV4cCI6MTc3NzE3NTIyMSwiaWF0IjoxNzc3MDg4ODIxLCJqdGkiOiIxMzM4MTA4NjM4MCJ9.j7TcM0vZ8eMkzxInBjdJQzKvl1PCrvMw0HdUP-j249A",
              "X-Tm": "win",
              "X-Version": "0.2.26",
              "X-Product": "autoclaw",
              "X-Channel": "official",
              "X-Lang": "zh-CN"
            }
          },
          {
            "id": "zai_glm-5v-turbo",
            "name": "GLM-5V-Turbo",
            "input": [
              "text",
              "image"
            ],
            "contextWindow": 204800,
            "maxTokens": 131072,
            "headers": {
              "X-Request-Model": "zai_glm-5v-turbo",
              "X-Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MTgyNjcsImRldmljZV9pZCI6ImY3OThmZmU4LTg1YWMtNDg1Ni1iN2U5LTIyMDJlMThlODU0ZCIsInNvdXJjZV9pZCI6ImF1dG9jbGF3YWNjZXNzX3Rva2VuIiwiZ3VpZCI6IiIsImlzX2d1ZXN0IjpmYWxzZSwicG93ZXIiOjAsImV4cCI6MTc3NzE3NTIyMSwiaWF0IjoxNzc3MDg4ODIxLCJqdGkiOiIxMzM4MTA4NjM4MCJ9.j7TcM0vZ8eMkzxInBjdJQzKvl1PCrvMw0HdUP-j249A",
              "X-Tm": "win",
              "X-Version": "0.2.26",
              "X-Product": "autoclaw",
              "X-Channel": "official",
              "X-Lang": "zh-CN"
            }
          },
          {
            "id": "zai_glm-5.1",
            "name": "GLM-5.1",
            "input": [
              "text"
            ],
            "contextWindow": 204800,
            "maxTokens": 131072,
            "headers": {
              "X-Request-Model": "zai_glm-5.1",
              "X-Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MTgyNjcsImRldmljZV9pZCI6ImY3OThmZmU4LTg1YWMtNDg1Ni1iN2U5LTIyMDJlMThlODU0ZCIsInNvdXJjZV9pZCI6ImF1dG9jbGF3YWNjZXNzX3Rva2VuIiwiZ3VpZCI6IiIsImlzX2d1ZXN0IjpmYWxzZSwicG93ZXIiOjAsImV4cCI6MTc3NzE3NTIyMSwiaWF0IjoxNzc3MDg4ODIxLCJqdGkiOiIxMzM4MTA4NjM4MCJ9.j7TcM0vZ8eMkzxInBjdJQzKvl1PCrvMw0HdUP-j249A",
              "X-Tm": "win",
              "X-Version": "0.2.26",
              "X-Product": "autoclaw",
              "X-Channel": "official",
              "X-Lang": "zh-CN"
            }
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "zai/huawei_glm-5"
      },
      "imageModel": {
        "primary": "zai/zai_glm-5v-turbo"
      },
      "models": {
        "qwen-portal/coder-model": {
          "alias": "qwen"
        },
        "qwen-portal/vision-model": {}
      },
      "workspace": "C:\\Users\\Administrator/.openclaw-autoclaw/workspace",
      "compaction": {
        "mode": "safeguard",
        "reserveTokensFloor": 40000
      },
      "timeoutSeconds": 1800,
      "heartbeat": {
        "every": "2h"
      }
    }
  },
  "tools": {
    "web": {
      "search": {
        "enabled": false
      }
    },
    "fs": {
      "workspaceOnly": true
    }
  },
  "commands": {
    "native": "auto",
    "nativeSkills": "auto",
    "restart": true,
    "ownerDisplay": "raw"
  },
  "session": {
    "dmScope": "per-account-channel-peer"
  },
  "channels": {
    "openclaw-weixin": {
      "accounts": {
        "9af714449ec4-im-bot": {
          "enabled": true
        }
      },
      "defaultAccount": "9af714449ec4-im-bot",
      "enabled": true
    }
  },
  "skills": {
    "allowBundled": [
      "__none__"
    ]
  },
  "plugins": {
    "slots": {
      "memory": "none"
    },
    "entries": {
      "openclaw-lark": {
        "enabled": true
      },
      "openclaw-weixin": {
        "enabled": true
      },
      "wecom": {
        "enabled": true
      },
      "qwen-portal-auth": {
        "enabled": true
      }
    }
  }
}
```
