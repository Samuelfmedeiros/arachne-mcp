"""
Arachne MCP Server — 49 tools for web scraping + AI + RAG + VRT + Social Research.

Connects to the Arachne API at https://arachne.seu.pet.
Requires an API key (get one at https://arachne.seu.pet/dev).
"""

import os
import json
import sys
import httpx

API_URL = os.environ.get("ARACHNE_API_URL", "https://arachne.seu.pet")
API_KEY = os.environ.get("ARACHNE_API_KEY", "")

if not API_KEY:
    print("X ARACHNE_API_KEY not set. Get one at https://arachne.seu.pet/dev", file=sys.stderr)
    sys.exit(1)

HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

TOOLS = [
    {
        "name": "arachne_ping",
        "description": "🏓 HEALTH CHECK (~0.001s). Quick connectivity test — returns server status, version, and uptime.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "arachne_plan",
        "description": "🔮 THE MAESTRO (~0.5-2s). Analyses goals, classifies tasks, suggests optimal tool chains.",
        "inputSchema": {"type": "object", "properties": {"goal": {"type": "string"}, "context": {"type": "string"}}, "required": ["goal"]}
    },
    {
        "name": "arachne_capabilities",
        "description": "🚀 SELF-DISCOVERY — returns ALL Arachne capabilities with engines, timings, and recommendations. No arguments needed.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "arachne_search",
        "description": "🔍 WEB SEARCH (~0.8s). Searches the web via DuckDuckGo. Returns URLs, titles, and snippets.",
        "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "default": 10}}, "required": ["query"]}
    },
    {
        "name": "arachne_scrape",
        "description": "📄 MARKDOWN EXTRACTION (~1.5-4s). Extracts URL content as clean markdown via Crawl4AI. Auto-indexes into RAG/SearchIndex.",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "kb_id": {"type": "string"}}, "required": ["url"]}
    },
    {
        "name": "arachne_query",
        "description": "🧠 RAG (~1-3s). Queries Arachne's knowledge base (FTS5 + vector search). kb_id=1 = Obsidian Vault.",
        "inputSchema": {"type": "object", "properties": {"question": {"type": "string"}, "kb_id": {"type": "string"}}, "required": ["question"]}
    },
    {
        "name": "arachne_browser_extract",
        "description": "🌐 REAL BROWSER WITH EVASION (~4-12s). Uses Playwright with 4 evasion layers to extract content from blocked/protected sites.",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "wait_ms": {"type": "integer", "default": 3000}, "screenshot": {"type": "boolean", "default": False}, "evasion_enabled": {"type": "boolean", "default": True}}, "required": ["url"]}
    },
    {
        "name": "arachne_browser_run",
        "description": "🎮 BROWSER AUTOMATION (~3-20s). Executes sequenced actions (click, type, navigate, extract, screenshot).",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "actions": {"type": "array"}, "screenshot": {"type": "boolean", "default": True}, "evasion_enabled": {"type": "boolean", "default": True}, "continue_on_error": {"type": "boolean", "default": False}}, "required": ["url"]}
    },
    {
        "name": "arachne_vision",
        "description": "👁️ IMAGE ANALYSIS (~1-8s). Runs 8-stage analysis pipeline (OCR, colors, quality, faces, edges) + optional VLM.",
        "inputSchema": {"type": "object", "properties": {"image_url": {"type": "string"}, "stages": {"type": "string"}, "fallback_ai": {"type": "boolean", "default": False}, "question": {"type": "string", "default": ""}}, "required": ["image_url"]}
    },
    {
        "name": "arachne_transcribe",
        "description": "🎤 AUDIO/VIDEO TRANSCRIPTION (~3-15s). Transcribes audio/video/YouTube via Whisper (tiny to large models).",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "model": {"type": "string", "default": "base"}, "language": {"type": "string", "default": ""}}, "required": ["url"]}
    },
    {
        "name": "arachne_extract",
        "description": "🦎 SWISS ARMY KNIFE. Smart dispatch for ANY URL/format: YouTube, audio, video, PDF, DOCX, images.",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "skip_cache": {"type": "boolean", "default": False}, "cache_max_age": {"type": "integer", "default": 24}, "format": {"type": "string"}, "kb_id": {"type": "string"}}, "required": ["url"]}
    },
    {
        "name": "arachne_screenshot",
        "description": "📸 SCREENSHOT (~3-8s). Captures a full-page or viewport screenshot of a URL via Playwright.",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "wait_ms": {"type": "integer", "default": 3000}, "full_page": {"type": "boolean", "default": True}, "width": {"type": "integer", "default": 1280}, "height": {"type": "integer", "default": 720}}, "required": ["url"]}
    },
    {
        "name": "arachne_screenshot_vision",
        "description": "📸+👁️ SCREENSHOT + VISION (~8-20s). Screenshots a URL then runs the full vision pipeline on the capture.",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "stages": {"type": "string"}, "fallback_ai": {"type": "boolean", "default": True}, "question": {"type": "string", "default": ""}, "wait_ms": {"type": "integer", "default": 3000}}, "required": ["url"]}
    },
    {
        "name": "arachne_record",
        "description": "🎬 SCREEN RECORDING (~5-65s). Records a screencast of a web page as .webm video.",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "duration_ms": {"type": "integer", "default": 10000}, "wait_ms": {"type": "integer", "default": 2000}, "scroll": {"type": "boolean", "default": False}, "width": {"type": "integer", "default": 1280}, "height": {"type": "integer", "default": 720}}, "required": ["url"]}
    },
    {
        "name": "arachne_record_vision",
        "description": "🎬👁️ RECORD + VISION (~15-90s). Records a screencast, extracts frames, and analyzes with vision + VLM.",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "duration_ms": {"type": "integer", "default": 10000}, "max_frames": {"type": "integer", "default": 5}, "fallback_ai": {"type": "boolean", "default": False}}, "required": ["url"]}
    },
    {
        "name": "arachne_pdf_vision",
        "description": "📄👁️ PDF VISION (~3-60s). Extracts images from a PDF and analyzes each with 8-stage vision + optional VLM.",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "stages": {"type": "string"}, "fallback_ai": {"type": "boolean", "default": False}, "question": {"type": "string", "default": ""}}, "required": ["url"]}
    },
    {
        "name": "arachne_calc",
        "description": "🧮 SAFE MATH CALCULATOR (~0.001s). AST-sandboxed math evaluator. Never uses eval().",
        "inputSchema": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}
    },
    {
        "name": "arachne_sandbox_status",
        "description": "🔒 SANDBOX STATUS — checks if ai-jail sandbox is available and active.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "arachne_metrics",
        "description": "📊 SERVER METRICS (~0.05s). Returns CPU %, RAM, disk, browser processes, safe_for_heavy_tasks.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "arachne_format_converter",
        "description": "🔄 UNIVERSAL CONVERTER (65+ FORMATS, ~0.001-2s). Zero AI cost. Converts data, documents, academic formats.",
        "inputSchema": {"type": "object", "properties": {"content": {"type": "string", "default": ""}, "source_format": {"type": "string", "default": "auto"}, "target_format": {"type": "string", "default": "json"}}}
    },
    {
        "name": "code_graph",
        "description": "📊 CODE KNOWLEDGE GRAPH. Explores Arachne's code structure: stats, search, routes, files, deps.",
        "inputSchema": {"type": "object", "properties": {"action": {"type": "string"}, "query": {"type": "string", "default": ""}, "node_id": {"type": "string", "default": ""}, "paths": {"type": "string"}}, "required": ["action"]}
    },
    {
        "name": "kg_context",
        "description": "📋 EFFICIENT CODE CONTEXT (~2K tokens). Ranked BFS extraction centered on a node or query.",
        "inputSchema": {"type": "object", "properties": {"action": {"type": "string"}, "q": {"type": "string", "default": ""}, "max_tokens": {"type": "integer", "default": 2048}}, "required": ["action"]}
    },
    {
        "name": "kg_communities",
        "description": "🏘️ CODE COMMUNITIES. Community detection (Leiden/greedy) over the code knowledge graph.",
        "inputSchema": {"type": "object", "properties": {"action": {"type": "string", "default": "detect"}, "algorithm": {"type": "string", "default": "auto"}}}
    },
    {
        "name": "kg_god_nodes",
        "description": "👑 GOD NODES. Most architecturally influential code entities (PageRank + betweenness + degree).",
        "inputSchema": {"type": "object", "properties": {"action": {"type": "string", "default": "nodes"}, "top_n": {"type": "integer", "default": 20}}}
    },
    {
        "name": "kg_watch",
        "description": "🔄 GIT WATCHER. Incremental code change detection via git diff.",
        "inputSchema": {"type": "object", "properties": {"action": {"type": "string", "default": "state"}, "repo_path": {"type": "string", "default": "."}, "since": {"type": "string", "default": ""}}}
    },
    {
        "name": "arachne_torrent_extract",
        "description": "🎯 TORRENT MAGNET EXTRACTOR (~5-60s). Extracts magnet links from Brazilian torrent sites (bludvfilmes, nerdtorrents, comandotorrenthd, torrentdosfilmes, dozitos, filmesbd, hinatasoul, ext.to). Handles systemads1 link protection — clicks ads, waits timers, intercepts magnet redirects.",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string", "default": ""}, "search_query": {"type": "string", "default": ""}, "use_browser": {"type": "boolean", "default": True}}}
    },
    {
        "name": "arachne_analyze_video",
        "description": "Analisa video e retorna metadados estruturados (cores, OCR, geometria, VQA, audio). Use quando precisar entender conteudo visual de videos: erros em terminal, mudancas de cena, textos na tela, cores dominantes.",
        "inputSchema": {"type": "object", "properties": {"video_url": {"type": "string"}, "audio_url": {"type": "string", "default": ""}, "use_scene_detection": {"type": "boolean", "default": True}, "frame_interval_sec": {"type": "number", "default": 5.0}, "max_frames": {"type": "integer", "default": 60}, "language": {"type": "string", "default": ""}, "enable_ocr": {"type": "boolean", "default": True}, "enable_color_extraction": {"type": "boolean", "default": True}, "enable_geometry": {"type": "boolean", "default": True}, "enable_vqa": {"type": "boolean", "default": True}, "output_format": {"type": "string", "default": "json"}}, "required": ["video_url"]}
    },
    {
        "name": "arachne_repo_download",
        "description": "📦 BAIXA REPOSITÓRIO (~2-60s). Download de repo GitHub (zipball/tarball) por URL ou owner/repo. Suporta branch específica e repo privado (token). Salva em app/static/acquired/. SSRF-safe.",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string", "default": ""}, "owner": {"type": "string", "default": ""}, "repo": {"type": "string", "default": ""}, "branch": {"type": "string", "default": ""}, "token": {"type": "string", "default": ""}}}
    },
    {
        "name": "arachne_repo_fork",
        "description": "🍴 FAZ FORK (~2-10s). Fork de repositório GitHub pra conta do token. Requer GITHUB_TOKEN ou token explícito.",
        "inputSchema": {"type": "object", "properties": {"owner": {"type": "string"}, "repo": {"type": "string"}, "token": {"type": "string", "default": ""}}, "required": ["owner", "repo"]}
    },
    {
        "name": "arachne_repo_forks",
        "description": "🍴 LISTA FORKS (~1-3s). Lista forks de um repositório GitHub, ordenados por estrelas.",
        "inputSchema": {"type": "object", "properties": {"owner": {"type": "string"}, "repo": {"type": "string"}, "limit": {"type": "integer", "default": 20}}, "required": ["owner", "repo"]}
    },
    {
        "name": "arachne_download",
        "description": "⬇️ DOWNLOAD UNIVERSAL (~1-60s). Baixa qualquer arquivo de URL (HTTP/HTTPS), repo GitHub/GitLab, pacote PyPI/npm. Detecta a fonte automaticamente. SSRF-safe. Salva em app/static/acquired/.",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "token": {"type": "string", "default": ""}}, "required": ["url"]}
    },
    {
        "name": "arachne_pypi_download",
        "description": "🐍 BAIXA PACOTE PyPI (~1-5s). Download de pacote Python (sdist/wheel) via JSON API. Ex: arachne_pypi_download('flask') ou ('flask', '3.0.0').",
        "inputSchema": {"type": "object", "properties": {"package": {"type": "string"}, "version": {"type": "string", "default": ""}}, "required": ["package"]}
    },
    {
        "name": "arachne_npm_download",
        "description": "📦 BAIXA PACOTE npm (~1-5s). Download de pacote npm (tarball) via registry. Ex: arachne_npm_download('react').",
        "inputSchema": {"type": "object", "properties": {"package": {"type": "string"}}, "required": ["package"]}
    },
    {
        "name": "arachne_gitlab_download",
        "description": "🦊 BAIXA PROJETO GitLab (~2-30s). Download de projeto GitLab (archive zip) por URL. Suporta repo privado (token).",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "token": {"type": "string", "default": ""}}, "required": ["url"]}
    },
    {
        "name": "arachne_releases",
        "description": "🏷️ LISTA RELEASES (~1-3s). Lista releases de um repo GitHub com assets disponíveis. Ex: arachne_releases('rust-lang', 'rust').",
        "inputSchema": {"type": "object", "properties": {"owner": {"type": "string"}, "repo": {"type": "string"}, "limit": {"type": "integer", "default": 10}}, "required": ["owner", "repo"]}
    },
    {
        "name": "arachne_release_download",
        "description": "📥 BAIXA ASSET DE RELEASE (~2-60s). Baixa um arquivo binário de release GitHub. Ex: arachne_release_download('rust-lang', 'rust', 'rust-1.80.0-x86_64-pc-windows-msvc.msi').",
        "inputSchema": {"type": "object", "properties": {"owner": {"type": "string"}, "repo": {"type": "string"}, "asset_name": {"type": "string"}, "tag": {"type": "string", "default": ""}, "token": {"type": "string", "default": ""}}, "required": ["owner", "repo", "asset_name"]}
    },
    {
        "name": "arachne_repo_index",
        "description": "🧠 BAIXA + INDEXA REPO NO RAG (~5-60s). Baixa um repo GitHub e indexa automaticamente no SearchIndex pra busca semântica. Ex: arachne_repo_index('psf', 'requests').",
        "inputSchema": {"type": "object", "properties": {"owner": {"type": "string"}, "repo": {"type": "string"}, "token": {"type": "string", "default": ""}}, "required": ["owner", "repo"]}
    },
    {
        "name": "arachne_desktop",
        "description": "🖥️ DESKTOP CONTROL (~0.5-3s). Controla o desktop X11 via wmctrl/xdotool — listar janelas, focar app, digitar texto, enviar teclas, clicar. Ex: arachne_desktop('windows'), arachne_desktop('activate', window='Firefox'), arachne_desktop('type', text='olá'), arachne_desktop('key', key='ctrl+s'). Requer ferramentas instaladas + DISPLAY.",
        "inputSchema": {"type": "object", "properties": {"action": {"type": "string"}, "window": {"type": "string", "default": ""}, "text": {"type": "string", "default": ""}, "key": {"type": "string", "default": ""}, "x": {"type": "integer", "default": 0}, "y": {"type": "integer", "default": 0}, "button": {"type": "integer", "default": 1}}, "required": ["action"]}
    },
    {
        "name": "arachne_observe",
        "description": "👁️ OITO OLHOS (~2-5s). Captura screenshot do navegador remoto com bounding boxes numerados em elementos clicáveis. Retorna imagem base64 + lista de elementos (tag, texto, coordenadas). A IA e o humano compartilham o mesmo nervo óptico.",
        "inputSchema": {"type": "object", "properties": {"session_id": {"type": "string", "default": ""}, "mode": {"type": "string", "default": "annotated"}}}
    },
    {
        "name": "arachne_visual_snapshot",
        "description": "🕷️ VISUAL SNAPSHOT (~8-30s). Captura screenshot de uma URL e cria baseline (1ª vez) ou compara com a existente. Combina pixel diff + DOM pareado + veredito VLM local (Douglas primário, Samuel fallback — mesmo modelo).",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "name": {"type": "string", "default": ""}, "full_page": {"type": "boolean", "default": True}, "width": {"type": "integer", "default": 1280}, "height": {"type": "integer", "default": 720}, "wait_ms": {"type": "integer", "default": 2500}, "threshold": {"type": "number", "default": 0.01}, "with_verdict": {"type": "boolean", "default": True}, "auth": {"type": "boolean", "default": False}}, "required": ["url"]}
    },
    {
        "name": "arachne_visual_diff",
        "description": "🕷️ VISUAL DIFF (~10-35s). Compara a URL atual com o baseline existente (nome obrigatório): diff_ratio, bounding boxes das regiões alteradas, noise hint (DOM pareado) e veredito VLM local (regression/expected/noise).",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "name": {"type": "string", "default": ""}, "threshold": {"type": "number", "default": 0.01}, "full_page": {"type": "boolean", "default": True}, "width": {"type": "integer", "default": 1280}, "height": {"type": "integer", "default": 720}, "wait_ms": {"type": "integer", "default": 2500}, "auth": {"type": "boolean", "default": False}}, "required": ["url"]}
    },
    {
        "name": "arachne_visual_gates",
        "description": "🕷️ VISUAL GATES (~10-30s). Gates determinísticos key-free numa URL: overflow-x, colisão de texto, JS errors, recursos quebrados — em 3 viewports. Retorna verdict CLEAN/DEFECTS com lista machine-parsable do que corrigir.",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "viewports": {"type": "array"}}, "required": ["url"]}
    },
    {
        "name": "arachne_visual_report",
        "description": "🕷️ VISUAL REPORT (~30-120s). Roda uma suíte de testes visuais (lista de {url, name}) e gera report HTML side-by-side (before/after/diff) + JSON machine-readable. Para aprovar mudanças, use arachne_visual_approve.",
        "inputSchema": {"type": "object", "properties": {"tests": {"type": "array"}, "title": {"type": "string", "default": "Oito Olhos — Relatório Visual"}}}
    },
    {
        "name": "arachne_visual_approve",
        "description": "🕷️ VISUAL APPROVE (~1s). Promove a captura atual (current.png) a baseline do teste — aprova a mudança visual como intencional. O contrário de arachne_visual_diff.",
        "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}
    },
    {
        "name": "arachne_visual_list",
        "description": "🕷️ VISUAL LIST (~1s). Lista todos os testes/baselines de VRT existentes + status do último diff.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "arachne_visual_video",
        "description": "🎬 VISUAL VIDEO (~15-90s). Grava screencast webm da URL (via arachne_record) e compara com o baseline de vídeo: dHash por frame detecta mudanças em ANIMAÇÕES, transições, hover, carrosséis — com heatmap temporal + janelas de mudança. 1ª chamada = baseline de vídeo.",
        "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "name": {"type": "string", "default": ""}, "duration_ms": {"type": "integer", "default": 5000}, "width": {"type": "integer", "default": 1280}, "height": {"type": "integer", "default": 720}, "wait_ms": {"type": "integer", "default": 2000}, "auth": {"type": "boolean", "default": False}}, "required": ["url"]}
    },
    {
        "name": "arachne_visual_video_report",
        "description": "🎬 VIDEO REPORT (~1-5min). Roda uma suíte de testes de vídeo (lista de {url, name, duration_ms}) e gera HTML interativo com vídeos side-by-side (antes/depois), heatmap temporal e veredito VLM da animação.",
        "inputSchema": {"type": "object", "properties": {"tests": {"type": "array"}, "title": {"type": "string", "default": "Oito Olhos — Relatório de Vídeo"}}}
    },
    {
        "name": "arachne_desktop_os",
        "description": "🖥️ DESKTOP OS AGENTIC (~1-15s). Controle do desktop (X11/WSLg) com olho de VLM: windows, activate, type, key, click, screenshot, e ask_vlm=true (screenshot + VLM local descreve a tela). O 'olho' permite ao agente ver antes de agir — base do Controle Remoto.",
        "inputSchema": {"type": "object", "properties": {"action": {"type": "string", "default": "windows"}, "window": {"type": "string", "default": ""}, "text": {"type": "string", "default": ""}, "key": {"type": "string", "default": ""}, "x": {"type": "integer", "default": 0}, "y": {"type": "integer", "default": 0}, "button": {"type": "integer", "default": 1}, "ask_vlm": {"type": "boolean", "default": False}}}
    },
    {
        "name": "arachne_social_research",
        "description": "🔍 SOCIAL SENTIMENT RESEARCH (~3-20s). Pesquisa o que as pessoas REALMENTE estão dizendo sobre um tema nas redes sociais (Hacker News, Reddit, YouTube) nos últimos 30 dias — sentimento, hype vs realidade, reclamações e top fontes com link. Sem API keys de terceiros.",
        "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "days": {"type": "integer", "default": 30}, "platforms": {"type": "string", "default": "hackernews,reddit,youtube"}, "limit_per_platform": {"type": "integer", "default": 25}, "include_items": {"type": "boolean", "default": True}}, "required": ["query"]}
    }
]


async def call_api(endpoint: str, payload: dict) -> dict:
    """Call the Arachne API."""
    url = f"{API_URL.rstrip('/')}{endpoint}"
    async with httpx.AsyncClient(timeout=300.0) as client:
        resp = await client.post(url, json=payload, headers=HEADERS)
        if resp.status_code == 401:
            return {"error": "Invalid API key. Get one at https://arachne.seu.pet/dev"}
        if resp.status_code == 429:
            return {"error": "Rate limit exceeded. Check your plan at https://arachne.seu.pet/dev"}
        if resp.status_code != 200:
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                detail = resp.text[:500]
            return {"error": f"API error ({resp.status_code}): {detail}"}
        return resp.json()


async def handle_tool(name: str, args: dict) -> list:
    """Execute a tool via the Arachne MCP proxy endpoint (supports all 49 tools)."""
    result = await call_api("/api/mcp/proxy", {
        "name": name,
        "arguments": args,
    })

    if isinstance(result, dict) and result.get("error"):
        return [{"type": "text", "text": result["error"]}]

    if isinstance(result, dict) and result.get("success"):
        inner = result.get("result", "{}")
        return [{"type": "text", "text": inner if isinstance(inner, str) else json.dumps(inner, indent=2, ensure_ascii=False)}]

    return [{"type": "text", "text": json.dumps(result, indent=2, ensure_ascii=False)}]


def main():
    """Run the MCP server over stdio (Claude Desktop / Cursor compatible)."""
    import asyncio

    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")

    async def _loop():
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg_id = msg.get("id")
            method = msg.get("method")

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "arachne-mcp", "version": "1.2.0"}
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

                tools_notification = {
                    "jsonrpc": "2.0",
                    "method": "notifications/tools/list",
                    "params": {"tools": TOOLS}
                }
                sys.stdout.write(json.dumps(tools_notification) + "\n")
                sys.stdout.flush()

            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"tools": TOOLS}
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = msg["params"]["name"]
                tool_args = msg["params"].get("arguments", {})
                try:
                    content = await handle_tool(tool_name, tool_args)
                    resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": content}}
                except Exception as e:
                    resp = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "error": {"code": -32603, "message": str(e)}
                    }
                sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
                sys.stdout.flush()

            elif method == "notifications/initialized":
                pass

    asyncio.run(_loop())


if __name__ == "__main__":
    main()
