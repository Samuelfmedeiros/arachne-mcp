<!-- mcp-name: io.github.Samuelfmedeiros/arachne-mcp -->

# 🕷️ Arachne MCP Server

> 🌐 **English** · [🇧🇷 Português](README.pt-BR.md)

**49 MCP tools** for web scraping, browser automation, computer vision, audio transcription, RAG, **Social Sentiment Research**, and **Visual Regression Testing (VRT) — the Oito Olhos (Spider's Eight Eyes)** — all through the Arachne API.

Backed by [Arachne](https://arachne.seu.pet). Works with **Claude Desktop**, **Cursor**, **Codex CLI**, **Hermes**, and any MCP client.

## ✨ Tools (49)

### 🔍 Web & Data
| Tool | What it does | Best for |
|------|-----------|------------|
| `arachne_search` | Web search via DuckDuckGo | Research, lead collection |
| `arachne_scrape` | Clean markdown from URLs | Static pages, blogs, docs |
| `arachne_extract` | Extracts ANY format (audio, video, PDF, YouTube) | **Swiss-army knife** |
| `arachne_browser_extract` | Real browser with Cloudflare/CAPTCHA evasion | Sites that block scrapers |
| `arachne_browser_run` | Browser actions (click, type, login) | Form automation |
| `arachne_screenshot` | Screenshot of a URL (full page or viewport) | Visual evidence |
| `arachne_record` | Records a screencast of a page (.webm) | Interactions, demos |
| `arachne_torrent_extract` | Extracts magnet links from BR torrent sites | Torrent acquisition |
| `arachne_download` | Universal download (URL, repo, PyPI, npm) | Fetch any artifact |
| `arachne_query` | Ask your RAG knowledge base | Chatbot with your data |

### 🔍 Social Sentiment Research
| Tool | What it does | Best for |
|------|-----------|------------|
| `arachne_social_research` | Searches what people REALLY say (HN/Reddit/YouTube, last N days) + AI judge via local VLM | **Hype vs reality, complaints, market sentiment** |

### 👁️ Vision & Audio
| Tool | What it does | Best for |
|------|-----------|------------|
| `arachne_vision` | Image analysis: OCR, colors, faces, AI description | Text extraction from photos |
| `arachne_screenshot_vision` | Screenshot + full vision pipeline | Visual page inspection |
| `arachne_pdf_vision` | Extracts images from PDF + vision analysis | Scanned PDFs |
| `arachne_analyze_video` | Video metadata: colors, OCR, geometry, VQA, audio | Video understanding |
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
| `arachne_visual_video` | Video VRT: records screencast + compares (animations) | Hover, carousels, transitions |
| `arachne_visual_video_report` | Video suite → interactive HTML report | Animation regression review |

### 🤖 Desktop & Agentic
| Tool | What it does | Best for |
|------|-----------|------------|
| `arachne_desktop` | Desktop control (windows, type, key, click) | OS automation |
| `arachne_desktop_os` | Desktop agentic with VLM "eye" (screenshot + describe) | See before acting |
| `arachne_observe` | Screenshot + numbered clickable bounding boxes | GUI agent navigation |

### 📦 GitHub / GitLab / Packages
| Tool | What it does |
|------|-----------|
| `arachne_repo_download` | Download GitHub repo as zip (branch/token) |
| `arachne_repo_fork` | Fork a GitHub repo |
| `arachne_repo_forks` | List forks by stars |
| `arachne_repo_index` | Download + index repo into RAG |
| `arachne_releases` | List GitHub releases with assets |
| `arachne_release_download` | Download a release asset |
| `arachne_pypi_download` | Download PyPI package (sdist/wheel) |
| `arachne_npm_download` | Download npm package tarball |
| `arachne_gitlab_download` | Download GitLab project archive |

### 🧠 Code Knowledge Graph
| Tool | What it does |
|------|-----------|
| `code_graph` | Explore code structure: stats, search, routes, files, deps |
| `kg_context` | Ranked BFS code context (~2K tokens) |
| `kg_communities` | Community detection (Leiden/greedy) |
| `kg_god_nodes` | Most influential code entities (PageRank) |
| `kg_watch` | Git watcher — incremental change detection |

### 🧭 Utilities
| Tool | What it does |
|------|-----------|
| `arachne_capabilities` | Auto-discover capabilities |
| `arachne_ping` | Health check |
| `arachne_metrics` | Server metrics (CPU, RAM, disk) |
| `arachne_plan` | Goal analysis → tool chain suggestion |
| `arachne_calc` | Safe math calculator (AST-sandboxed) |
| `arachne_format_converter` | Universal converter (65+ formats) |
| `arachne_sandbox_status` | Check ai-jail sandbox availability |

> **VRT with local LLM:** Oito Olhos uses pixel diff + DOM pairing + **CLIP semantic triage** + **local VLM** (Qwen2.5-VL via Douglas, Samuel mirror fallback) — classifying changes as `regression | expected | noise`, with a fix suggestion (`CORRECAO:`) when it detects a bug. **No third-party API key for the verdict.**

> **Social Research with local AI judge:** `arachne_social_research` searches Hacker News (Algolia), Reddit (JSON API + browser_agent/Camoufox fallback) and YouTube (yt-dlp) in the last N days, scores by real engagement (upvotes/points/views), and synthesizes a **hype vs reality** report with a local VLM (no third-party API keys).

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
        "ARACHNE_API_KEY": "arn_your_key_here",
        "ARACHNE_API_URL": "https://arachne.seu.pet"
      }
    }
  }
}
```

### 3. Or run directly

```bash
pip install arachne-mcp
export ARACHNE_API_KEY="arn_your_key_here"
python3 -m arachne_mcp
```

## 📡 Architecture

The MCP server is a **thin proxy**: it forwards each tool call to the Arachne API
(`POST /api/mcp/proxy`), which executes the tool server-side and returns the result.
This keeps the client light (only `httpx`), while all heavy work — browser, VLM,
vision, RAG — runs on the Arachne server.

```text
Claude Desktop / Cursor / Codex
        │  MCP (stdio)
        ▼
arachne-mcp (thin proxy, 49 tools)
        │  HTTP + X-API-Key
        ▼
Arachne API (arachne.seu.pet) → executes tool → returns JSON
```

## 🔐 Security

- **API key auth**: every request carries `X-API-Key` (create at `/dev`)
- **Rate limits** enforced server-side per plan
- No code runs client-side — the proxy only forwards arguments
