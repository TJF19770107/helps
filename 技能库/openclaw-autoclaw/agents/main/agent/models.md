# models.json

原始格式: JSON

```json
{
  "providers": {
    "zai": {
      "baseUrl": "https://autoglm-api.zhipuai.cn/autoclaw-proxy/proxy/autoclaw",
      "apiKey": "ZAI_API_KEY",
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
            "X-Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MTgyNjcsImRldmljZV9pZCI6ImY3OThmZmU4LTg1YWMtNDg1Ni1iN2U5LTIyMDJlMThlODU0ZCIsInNvdXJjZV9pZCI6ImF1dG9jbGF3YWNjZXNzX3Rva2VuIiwiZ3VpZCI6IiIsImlzX2d1ZXN0IjpmYWxzZSwicG93ZXIiOjAsImV4cCI6MTc3NzEyNzg0NSwiaWF0IjoxNzc3MDQxNDQ1LCJqdGkiOiIxMzM4MTA4NjM4MCJ9.DmRSrM6iTwJsUYiARPWPYGq71Hr88eEIuHc_Muc8c3Y",
            "X-Tm": "win",
            "X-Version": "0.2.26",
            "X-Product": "autoclaw",
            "X-Channel": "official",
            "X-Lang": "zh-CN"
          },
          "reasoning": false,
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "api": "openai-completions"
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
            "X-Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MTgyNjcsImRldmljZV9pZCI6ImY3OThmZmU4LTg1YWMtNDg1Ni1iN2U5LTIyMDJlMThlODU0ZCIsInNvdXJjZV9pZCI6ImF1dG9jbGF3YWNjZXNzX3Rva2VuIiwiZ3VpZCI6IiIsImlzX2d1ZXN0IjpmYWxzZSwicG93ZXIiOjAsImV4cCI6MTc3NzEyNzg0NSwiaWF0IjoxNzc3MDQxNDQ1LCJqdGkiOiIxMzM4MTA4NjM4MCJ9.DmRSrM6iTwJsUYiARPWPYGq71Hr88eEIuHc_Muc8c3Y",
            "X-Tm": "win",
            "X-Version": "0.2.26",
            "X-Product": "autoclaw",
            "X-Channel": "official",
            "X-Lang": "zh-CN"
          },
          "reasoning": false,
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "api": "openai-completions"
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
            "X-Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MTgyNjcsImRldmljZV9pZCI6ImY3OThmZmU4LTg1YWMtNDg1Ni1iN2U5LTIyMDJlMThlODU0ZCIsInNvdXJjZV9pZCI6ImF1dG9jbGF3YWNjZXNzX3Rva2VuIiwiZ3VpZCI6IiIsImlzX2d1ZXN0IjpmYWxzZSwicG93ZXIiOjAsImV4cCI6MTc3NzEyNzg0NSwiaWF0IjoxNzc3MDQxNDQ1LCJqdGkiOiIxMzM4MTA4NjM4MCJ9.DmRSrM6iTwJsUYiARPWPYGq71Hr88eEIuHc_Muc8c3Y",
            "X-Tm": "win",
            "X-Version": "0.2.26",
            "X-Product": "autoclaw",
            "X-Channel": "official",
            "X-Lang": "zh-CN"
          },
          "reasoning": false,
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "api": "openai-completions"
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
            "X-Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2MTgyNjcsImRldmljZV9pZCI6ImY3OThmZmU4LTg1YWMtNDg1Ni1iN2U5LTIyMDJlMThlODU0ZCIsInNvdXJjZV9pZCI6ImF1dG9jbGF3YWNjZXNzX3Rva2VuIiwiZ3VpZCI6IiIsImlzX2d1ZXN0IjpmYWxzZSwicG93ZXIiOjAsImV4cCI6MTc3NzEyNzg0NSwiaWF0IjoxNzc3MDQxNDQ1LCJqdGkiOiIxMzM4MTA4NjM4MCJ9.DmRSrM6iTwJsUYiARPWPYGq71Hr88eEIuHc_Muc8c3Y",
            "X-Tm": "win",
            "X-Version": "0.2.26",
            "X-Product": "autoclaw",
            "X-Channel": "official",
            "X-Lang": "zh-CN"
          },
          "reasoning": false,
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "api": "openai-completions"
        }
      ]
    },
    "zhipu": {
      "baseUrl": "https://open.bigmodel.cn/api/paas/v4/",
      "apiKey": "ZHIPUAI_API_KEY",
      "api": "openai-completions",
      "models": [
        {
          "id": "glm-4-flash",
          "name": "GLM-4-Flash",
          "api": "openai-completions",
          "reasoning": false,
          "input": [
            "text"
          ],
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "contextWindow": 128000,
          "maxTokens": 4096
        }
      ]
    },
    "ollama": {
      "baseUrl": "http://127.0.0.1:11434",
      "api": "ollama",
      "models": [
        {
          "id": "qwen3:8b",
          "name": "qwen3:8b",
          "reasoning": false,
          "input": [
            "text"
          ],
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "contextWindow": 40960,
          "maxTokens": 8192
        },
        {
          "id": "qwen2.5:7b-instruct",
          "name": "qwen2.5:7b-instruct",
          "reasoning": false,
          "input": [
            "text"
          ],
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "contextWindow": 32768,
          "maxTokens": 8192
        },
        {
          "id": "qwen3.5:2b",
          "name": "qwen3.5:2b",
          "reasoning": false,
          "input": [
            "text"
          ],
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "contextWindow": 262144,
          "maxTokens": 8192
        },
        {
          "id": "deepseek-r1:7b",
          "name": "deepseek-r1:7b",
          "reasoning": true,
          "input": [
            "text"
          ],
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "contextWindow": 131072,
          "maxTokens": 8192
        },
        {
          "id": "deepseek-r1:1.5b",
          "name": "deepseek-r1:1.5b",
          "reasoning": true,
          "input": [
            "text"
          ],
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "contextWindow": 131072,
          "maxTokens": 8192
        }
      ],
      "apiKey": "ollama-local"
    }
  }
}

```
