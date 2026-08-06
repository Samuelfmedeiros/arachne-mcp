<!-- mcp-name: io.github.Samuelfmedeiros/arachne-mcp -->

# 🕷️ Arachne MCP Server

> 🌐 **English** · [🇧🇷 Português](README.pt-BR.md)

**15 MCP tools** for web scraping, browser automation, computer vision, audio transcription, RAG, and **Visual Regression Testing (VRT) — the Oito Olhos (Spider's Eight Eyes)** — all through the Arachne API.

Backed by [Arachne](https://arachne.seu.pet). Works with **Claude Desktop**, **Cursor**, **Codex CLI**, **Hermes**, and any MCP client.

## ✨ Tools

### 🔍 Web & Data
| Tool | What it does | Best for |
|------|-----------|------------|
| `arachne_search` | Web search via DuckDuckGo | Research, lead collection |
| `arachne_scrape` | Clean markdown from URLs | Static pages, blogs, docs |
| `arachne_extract` | Extracts ANY format (audio, video, PDF, YouTube) | **Swiss-army knife** |
| `arachne_browser_extract` | Real browser with Cloudflare/CAPTCHA evasion | Sites that block scrapers |
| `arachne_browser_run` | Browser actions (click, type, login) | Form automation |
| `arachne_query` | Ask your RAG knowledge base | Chatbot with your data |

### 👁️ Vision & Audio
| Tool | What it does | Best for |
|------|-----------|------------|
| `arachne_vision` | Image analysis: OCR, colors, faces, AI description | Text extraction from photos |
| `arachne_transcribe` | Audio/video/YouTube transcription with Whisper | Podcast, meeting, video |

### 🕷️ Oito Olhos — Visual Regression Testing (VRT)
| Tool | What it does | Best for |
|------|-----------|------------|
| `arachne_visual_snapshot` | Captures URL → creates baseline (1st time) or compares | Idempotent visual tests |
| `arachne_visual_diff` | Compares with baseline → diff + semantic verdict | Post-deploy verification |
| `arachne_visual_gates` | Deterministic audit: overflow, text collision, JS errors | **Key-free, no baseline** |
| `arachne_visual_report` | Test suite → HTML side-by-side | Consolidated review |
| `arachne_visual_approve` | Promotes current → new baseline | Accept an expected change |
| `arachne_visual_list` | Lists baselines + status | Monitor what exists |

### 🧭 Utilities
| Tool | What it does |
|------|-----------|
| `arachne_capabilities` | Auto-discover capabilities |

> **VRT with local LLM:** Oito Olhos uses pixel diff + DOM pairing + **CLIP semantic triage** + **local VLM** (Qwen2.5-VL via Douglas, Samuel mirror fallback) — classifying changes as `regression | expected | noise`, with a fix suggestion (`CORRECAO:`) when it detects a bug. **Zero API key for the verdict.**

## 🚀 Quick Start

### 1. Get an API key

Create one at **[arachne.seu.pet/dev](https://arachne.seu.pet/dev)** (Free plan: 500 req/month).

### 2. Configure in Claude Desktop

```json
{
  "mcpServers": {
    "arachne": {
      "command": "python3",
      "args": ["-m", "arachne_mcp"],
      "env": {
        "ARACHNE_API_KEY": "your_key_here",
        "ARACHNE_BASE_URL": "https://arachne.seu.pet"
      }
    }
  }
}
```

### 3. Or run directly

```bash
export ARACHNE_API_KEY="your_key"
python3 -m arachne_mcp
```

> Requires `httpx`: `pip install httpx`

## 📦 How it works

The MCP server is an **HTTP client** that calls the public Arachne API. Zero local infrastructure — runs anywhere.

```
Your AI agent → MCP stdio → arachne_mcp.py → HTTP → Arachne API → result
```

## 🕷️ Examples — Oito Olhos (VRT)

```python
# 1. Create a baseline for a page (first run)
arachne_visual_snapshot(url="https://mysite.com/", name="home")

# 2. After a deploy: compare and get a verdict
arachne_visual_diff(url="https://mysite.com/", name="home")
# → { diff_ratio: 0.023, classification: "regression",
#     description: "CTA button changed color. CLASSIFICACAO: regression
#     CORRECAO: check .cta CSS — color should be var(--primary)" }

# 3. Expected change? Approve as the new baseline
arachne_visual_approve(name="home")

# 4. Baseline-free audit (deterministic gates)
arachne_visual_gates(url="https://mysite.com/")
# → verdict: CLEAN | DEFECTS with machine-parsable fix list

# 5. Full suite → HTML report
arachne_visual_report(tests=[{"url": "https://mysite.com/", "name": "home"},
                             {"url": "https://mysite.com/pricing", "name": "pricing"}])
```

**Tips:**
- Authenticated pages: use `auth: true` — the engine logs in and injects the token.
- Dynamic areas (stats, clock): use `mask: [{"selector": ".stats"}]`.
- Color/theme differences that aren't bugs: **CLIP semantic triage** classifies them as `expected` without invoking the 7B VLM.

## 📊 Plans

| Plan | Price | Requests/month | Features |
|-------|-------|-------------|----------|
| **Free** | R$ 0 | 500 | search, scrape, jobs |
| **Pro** | R$ 49/month | 10.000 | + browser, vision, transcribe, MCP, **VRT visual** |
| **Enterprise** | R$ 199/month | 100.000 | + admin, export, dedicated support |

## 🏗️ Stack

- **Backend:** FastAPI + Crawl4AI + Whisper + Tesseract + PostgreSQL
- **VRT:** Playwright + ffmpeg (video) + CLIP ViT-B-32 + Qwen2.5-VL (local VLM)
- **Engines:** Trafilatura → Crawl4AI SDK → Sidecar Docker → Camoufox
- **MCP Transport:** stdio (compatible with Claude Desktop, Cursor, Codex, Hermes)

## 🔗 Links

- [Arachne Platform](https://arachne.seu.pet)
- [Developer Portal](https://arachne.seu.pet/dev)
- [Python SDK (PyPI)](https://pypi.org/project/arachne-sdk/)
- [GitHub](https://github.com/Samuelfmedeiros/arachne-mcp)

---

🕷️ Built with the Arachne engine. Open source MCP server.
