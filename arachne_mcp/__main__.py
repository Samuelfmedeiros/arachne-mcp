"""
🕷️ Arachne MCP Server — 9 tools for web scraping + AI + RAG.

Connects to the Arachne API at https://arachne.seu.pet.
Requires an API key (get one at https://arachne.seu.pet/dev).

## Tools

| Tool | Description |
|------|-------------|
| arachne_search | Search the web via DuckDuckGo |
| arachne_scrape | Extract clean markdown from any URL |
| arachne_extract | Universal extract — auto-detects format (web/audio/video/pdf/image) |
| arachne_browser_extract | Full browser extraction with Cloudflare/CAPTCHA evasion |
| arachne_browser_run | Execute browser actions (click, type, navigate, screenshot) |
| arachne_query | Ask questions to your RAG knowledge base |
| arachne_vision | Analyze images (OCR, colors, faces, textures, AI description) |
| arachne_transcribe | Transcribe audio/video/YouTube with Whisper |
| arachne_capabilities | Auto-discover all Arachne capabilities |

## Setup

### 1. Get an API key
Go to https://arachne.seu.pet/dev and create a key (or buy a plan).

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
pip install arachne-sdk
export ARACHNE_API_KEY="arn_your_key_here"
python3 -m arachne_mcp
```
"""

import os
import json
import sys
import httpx
from typing import Any

API_URL = os.environ.get("ARACHNE_API_URL", "https://arachne.seu.pet")
API_KEY = os.environ.get("ARACHNE_API_KEY", "")

if not API_KEY:
    print("❌ ARACHNE_API_KEY not set. Get one at https://arachne.seu.pet/dev", file=sys.stderr)
    sys.exit(1)

HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

TOOLS = [
    {
        "name": "arachne_search",
        "description": "Search the web via DuckDuckGo. Returns titles, URLs, and descriptions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "description": "Max results (1-20)", "default": 10}
            },
            "required": ["query"]
        }
    },
    {
        "name": "arachne_scrape",
        "description": "Extract clean markdown from any URL. Best for static pages, blogs, docs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to extract"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "arachne_extract",
        "description": "Universal extract — auto-detects format. Works with web pages, audio, video, PDFs, images, YouTube.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to extract (web, audio, video, PDF, image, YouTube)"},
                "format": {"type": "string", "description": "Output format: json (default), xlsx, csv, pptx, md", "default": "json"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "arachne_browser_extract",
        "description": "Extract content using a real browser with Cloudflare/CAPTCHA/WAF evasion. Use when arachne_scrape fails.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to extract"},
                "screenshot": {"type": "boolean", "description": "Include screenshot?", "default": False}
            },
            "required": ["url"]
        }
    },
    {
        "name": "arachne_browser_run",
        "description": "Execute actions in a real browser: click, type, navigate, screenshot. For login flows, multi-page forms.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Starting URL"},
                "actions": {
                    "type": "array",
                    "description": "Actions to execute",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "enum": ["navigate", "click", "type", "select", "wait", "scroll", "extract", "screenshot"]},
                            "selector": {"type": "string", "description": "CSS selector for click/type/wait"},
                            "value": {"type": "string", "description": "Text for type action"}
                        }
                    }
                },
                "screenshot": {"type": "boolean", "description": "Take final screenshot?", "default": True}
            },
            "required": ["url", "actions"]
        }
    },
    {
        "name": "arachne_query",
        "description": "Ask questions to a RAG knowledge base. Retrieves grounded answers with source citations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "Your question"},
                "kb_id": {"type": "integer", "description": "Knowledge base ID (default: 1)", "default": 1}
            },
            "required": ["question"]
        }
    },
    {
        "name": "arachne_vision",
        "description": "Analyze an image: OCR text extraction, color palette, face detection, quality metrics, AI description.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image_url": {"type": "string", "description": "Public URL of the image"},
                "question": {"type": "string", "description": "Optional question about the image (requires AI fallback)"}
            },
            "required": ["image_url"]
        }
    },
    {
        "name": "arachne_transcribe",
        "description": "Transcribe audio, video, or YouTube URL using Whisper. Supports MP3, WAV, MP4, WebM, YouTube.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Audio/video/YouTube URL"},
                "language": {"type": "string", "description": "Language code (pt, en, es, fr) or auto-detect"},
                "model": {"type": "string", "enum": ["tiny", "base", "small", "medium", "large"], "description": "Whisper model size", "default": "base"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "arachne_capabilities",
        "description": "Auto-discover all capabilities, engines, and recommended tools of the Arachne platform.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


async def call_api(endpoint: str, payload: dict) -> dict:
    """Call the Arachne API."""
    url = f"{API_URL.rstrip('/')}{endpoint}"
    async with httpx.AsyncClient(timeout=120.0) as client:
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
    """Execute a tool and return MCP-formatted content."""
    result = None

    if name == "arachne_search":
        result = await call_api("/api/v2/search", {
            "q": args["query"],
            "limit": args.get("limit", 10)
        })
    elif name == "arachne_scrape":
        result = await call_api("/api/v2/scrape", {
            "url": args["url"]
        })
    elif name == "arachne_extract":
        result = await call_api("/api/extract/universal", {
            "url": args["url"],
            "format": args.get("format", "json")
        })
    elif name == "arachne_browser_extract":
        result = await call_api("/api/browser/extract", {
            "url": args["url"],
            "screenshot": args.get("screenshot", False)
        })
    elif name == "arachne_browser_run":
        result = await call_api("/api/browser/run", {
            "url": args["url"],
            "actions": args["actions"],
            "screenshot": args.get("screenshot", True)
        })
    elif name == "arachne_query":
        result = await call_api("/api/v2/query", {
            "question": args["question"],
            "kb_id": args.get("kb_id", 1)
        })
    elif name == "arachne_vision":
        result = await call_api("/api/vision/analyze", {
            "image_url": args["image_url"],
            "question": args.get("question", ""),
            "stages": ["metadata", "colors", "quality", "edges", "shapes", "ocr", "faces", "texture"]
        })
    elif name == "arachne_transcribe":
        result = await call_api("/api/transcribe/url", {
            "url": args["url"],
            "language": args.get("language", ""),
            "model": args.get("model", "base")
        })
    elif name == "arachne_capabilities":
        result = await call_api("/api/capabilities", {})
    else:
        return [{"type": "text", "text": f"Unknown tool: {name}"}]

    if result is None:
        return [{"type": "text", "text": f"No result from {name}"}]

    return [{"type": "text", "text": json.dumps(result, indent=2, ensure_ascii=False)}]


# ── MCP stdio transport ─────────────────────────────────────────────

def main():
    """Run the MCP server over stdio (Claude Desktop / Cursor compatible)."""
    import asyncio

    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")

    async def _loop():
        # Send initialize response
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
                        "serverInfo": {"name": "arachne-mcp", "version": "1.0.0"}
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

                # Send tools list after initialized notification
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
                pass  # OK

    asyncio.run(_loop())


if __name__ == "__main__":
    main()
