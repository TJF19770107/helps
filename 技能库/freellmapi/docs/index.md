FreeLLMAPI

Providers Quick start [GitHub](<https://github.com/tashfeenahmed/freellmapi>)

100+ free models · 16 providers · self-hosted

# One key.
1.7 billion free tokens.
Every month.

A self-hosted, OpenAI-compatible proxy that routes across every credible free-tier LLM provider. Bring your own keys; we just point requests at whichever provider still has budget left.

[View on GitHub →](<https://github.com/tashfeenahmed/freellmapi>) Quick start

Aggregate monthly free budget

1.7B

tokens · per month

Across 100+ free-tier models on 16 providers, plus any custom OpenAI-compatible endpoint. Mistral alone contributes ~1B; everything else is bonus.

The catalog

## Every free tier worth using

Only providers with **recurring** free quotas, no credit card required, and a self-serve API.

![](logos/google.svg)Google Gemini

~3M/moper model

Gemini 2.5 Flash · Flash-Lite · 3.1 Pro/Flash previews. **20 RPD per model**.

![](logos/openrouter.svg)OpenRouter

~6M/moper model

19 `:free` models — DeepSeek, Kimi, Qwen, Llama, Gemma, Nemotron, Tencent HY3 …

![](logos/cerebras.svg)Cerebras

~30M/moshared

Qwen3 235B · GPT-OSS 120B · Llama 3.1 8B. **1M TPD · 30 RPM**. Fastest tokens you'll ever see.

![](logos/groq.svg)Groq

~30M/moper model

Llama 3.3 70B · Llama 4 Scout · GPT-OSS 120B/20B · Qwen3 32B. **1000 RPD**.

![](logos/mistral.svg)Mistral La Plateforme

~1B/moshared

Mistral Large/Medium · Codestral · Devstral · Magistral. The biggest free pool of any provider.

![](logos/github.svg)GitHub Models

~18M/moest.

GPT-4.1 · GPT-4o. **50 RPD** on the free Copilot tier. Higher caps with paid Copilot.

OCOpenCode Zen

promorotating free models

DeepSeek V4 Flash · Nemotron 3 Super · MiMo V2.5 · Big Pickle. Free account key, no card.

![](logos/cloudflare.svg)Cloudflare Workers AI

~20M/moshared

Kimi K2.5/K2.6 · Qwen3 30B · GLM-4.7 Flash · Llama 4 Scout · IBM Granite 4.0. **10K Neurons/day**.

![](logos/zai.svg)Z.ai (Zhipu)

~30M/moshared

GLM-4.5 Flash · GLM-4.7 Flash. Both `:free` — perpetually, no card.

![](logos/cohere.svg)Cohere

~1-2M/moshared

Command R+. Trial key: **1000 calls/month** , 20 RPM.

![](logos/nvidia.svg)NVIDIA NIM

creditsdisabled

Llama 3.1 70B. Disabled by default — credit-based, not recurring.

HFHuggingFace

~3M/morouter credit

Inference Providers router → DeepSeek V4 · Kimi K2.6 · Qwen3. Recurring router credit, no card.

OLOllama Cloud

freeGPU-time

GLM-4.7 · Kimi K2 · gpt-oss · Qwen3. Free plan: 1 concurrent model, session/GPU-time caps.

KKilo Gateway

anon~200/hr

`:free` routes — anonymous access works per-IP; a key raises the limit.

PPollinations

anonfree tier

GPT-OSS 20B (`openai-fast`), tools supported. Anonymous tier, no key.

L7LLM7

anon~100/hr

GPT-OSS · Llama 3.1 Turbo · Codestral · GLM via one token. Anonymous access works.

+Custom endpoint

∞your server

Point at any OpenAI-compatible URL — llama.cpp, LM Studio, vLLM, a local Ollama, or a remote gateway.

Three minutes to first token

## Quick start

1

### Clone & install

Node 20+ required. `better-sqlite3` brings prebuilt binaries — no compile step.

2

### Drop in your keys

Sign up free at each provider, paste keys into the dashboard. No credit card needed for any of them.

3

### Point your SDK

Set `base_url` to your local proxy. Use any OpenAI-compatible client — Cursor, the SDK, curl, anything.

~/freellmapi · zsh


    # 1. clone, install, run
    $git clone https://github.com/tashfeenahmed/freellmapi.git
    $cd freellmapi
    $npm install && npm run dev

    # 2. open http://localhost:3001 — paste keys in the UI

    # 3. call it like OpenAI
    $curl http://localhost:3001/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{"messages":[{"role":"user","content":"hi"}]}'

FreeLLMAPI — open source, self-hosted, single-user. [github.com/tashfeenahmed/freellmapi](<https://github.com/tashfeenahmed/freellmapi>)

Built for personal use only. Each provider's ToS applies — don't expose this proxy publicly.
