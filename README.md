# 🕷️ Arachne MCP Server

**9 MCP tools** para web scraping, browser automation, visão computacional, transcrição de áudio e RAG — tudo via API.

Conecta no [Arachne](https://arachne.seu.pet) como backend. Funciona com **Claude Desktop**, **Cursor**, **Codex CLI**, e qualquer cliente MCP.

## ✨ Tools

| Tool | O que faz | Ideal para |
|------|-----------|------------|
| `arachne_search` | Busca na web via DuckDuckGo | Pesquisa, coleta de informações |
| `arachne_scrape` | Extrai markdown limpo de URLs | Páginas estáticas, blogs, docs |
| `arachne_extract` | Extrai QUALQUER formato (áudio, vídeo, PDF, YouTube) | **Canivete suíço** |
| `arachne_browser_extract` | Navegador real com evasão Cloudflare/CAPTCHA | Sites que bloqueiam scraper |
| `arachne_browser_run` | Executa ações em navegador (click, type, login) | Automação de formulários |
| `arachne_query` | Pergunta pra sua base de conhecimento RAG | Chatbot com seus dados |
| `arachne_vision` | Analisa imagens: OCR, cores, faces, descrição AI | Extrair texto de fotos |
| `arachne_transcribe` | Transcreve áudio/vídeo/YouTube com Whisper | Podcast, reunião, vídeo |
| `arachne_capabilities` | Auto-descoberta de capacidades | Saber o que o Arachne faz |

## 🚀 Quick Start

### 1. Pegue uma API Key

Crie em **[arachne.seu.pet/dev](https://arachne.seu.pet/dev)** (plano Free: 500 req/mês).

### 2. Configure no Claude Desktop

```json
{
  "mcpServers": {
    "arachne": {
      "command": "python3",
      "args": ["-m", "arachne_mcp"],
      "env": {
        "ARACHNE_API_KEY": "sua_chave_aqui"
      }
    }
  }
}
```

### 3. Ou teste direto

```bash
export ARACHNE_API_KEY="sua_chave"
python3 arachne_mcp.py
```

> Precisa de `httpx`: `pip install httpx`

## 📦 Como funciona

O MCP server é um **cliente HTTP** que chama a API pública do Arachne. Zero dependência de infra local — roda de qualquer lugar.

```
Seu agente AI → MCP stdio → arachne_mcp.py → HTTP → Arachne API → resultado
```

## 🔧 Exemplos

```python
# Via arachne-sdk (pip install arachne-sdk)
from arachne_sdk import Arachne
client = Arachne(api_key="sua_chave")

# Busca na web
results = client.search("preço iPhone 16 Brasil")
for r in results:
    print(f"{r.title}: {r.url}")

# Extrair página
content = client.scrape("https://exemplo.com")
print(content[:500])

# Analisar imagem
vision = client.vision("https://exemplo.com/foto.jpg")
print(vision.ocr.text)

# Perguntar ao RAG
answer = client.query("Qual a diferença do Arachne pro Firecrawl?")
print(answer)
```

## 📊 Planos

| Plano | Preço | Requests/mês | Features |
|-------|-------|-------------|----------|
| **Free** | R$ 0 | 500 | search, scrape, jobs |
| **Pro** | R$ 49/mês | 10.000 | + browser, vision, transcribe, MCP |
| **Enterprise** | R$ 199/mês | 100.000 | + admin, export, suporte dedicado |

## 🏗️ Stack

- **Backend:** FastAPI + Crawl4AI + Whisper + Tesseract + SQLite
- **Engines:** Trafilatura → Crawl4AI SDK → Sidecar Docker → Camoufox
- **MCP Transport:** stdio (compatível com Claude Desktop, Cursor, Codex)

## 🔗 Links

- [Arachne Platform](https://arachne.seu.pet)
- [Developer Portal](https://arachne.seu.pet/dev)
- [API Docs](https://arachne.seu.pet/dev)
- [Python SDK (PyPI)](https://pypi.org/project/arachne-sdk/)
- [GitHub](https://github.com/Samuelfmedeiros/arachne-mcp)

---

🕷️ Built with the Arachne engine. Open source MCP server.
