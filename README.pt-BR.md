<!-- mcp-name: io.github.Samuelfmedeiros/arachne-mcp -->

# 🕷️ Arachne MCP Server

> 🇧🇷 **Português** · [🌐 English](README.md)

**15 MCP tools** para web scraping, browser automation, visão computacional, transcrição de áudio, RAG e **Visual Regression Testing (VRT) — o Oito Olhos da Aranha** — tudo via API.

Conecta no [Arachne](https://arachne.seu.pet) como backend. Funciona com **Claude Desktop**, **Cursor**, **Codex CLI**, **Hermes** e qualquer cliente MCP.

## ✨ Tools

### 🔍 Web & Dados
| Tool | O que faz | Ideal para |
|------|-----------|------------|
| `arachne_search` | Busca na web via DuckDuckGo | Pesquisa, coleta de informações |
| `arachne_scrape` | Extrai markdown limpo de URLs | Páginas estáticas, blogs, docs |
| `arachne_extract` | Extrai QUALQUER formato (áudio, vídeo, PDF, YouTube) | **Canivete suíço** |
| `arachne_browser_extract` | Navegador real com evasão Cloudflare/CAPTCHA | Sites que bloqueiam scraper |
| `arachne_browser_run` | Executa ações em navegador (click, type, login) | Automação de formulários |
| `arachne_query` | Pergunta pra sua base de conhecimento RAG | Chatbot com seus dados |

### 👁️ Visão & Áudio
| Tool | O que faz | Ideal para |
|------|-----------|------------|
| `arachne_vision` | Analisa imagens: OCR, cores, faces, descrição AI | Extrair texto de fotos |
| `arachne_transcribe` | Transcreve áudio/vídeo/YouTube com Whisper | Podcast, reunião, vídeo |

### 🕷️ Oito Olhos — Visual Regression Testing (VRT)
| Tool | O que faz | Ideal para |
|------|-----------|------------|
| `arachne_visual_snapshot` | Captura URL e cria baseline (1ª vez) ou compara | Testes visuais idempotentes |
| `arachne_visual_diff` | Compara com baseline → diff + veredito semântico | Verificação pós-deploy |
| `arachne_visual_gates` | Auditoria determinística: overflow, colisão de texto, JS errors | **Key-free, sem baseline** |
| `arachne_visual_report` | Suíte de testes → HTML side-by-side | Revisão consolidada |
| `arachne_visual_approve` | Aprova current → novo baseline | Aceitar mudança esperada |
| `arachne_visual_list` | Lista baselines + status | Monitorar o que existe |

### 🧭 Utilidades
| Tool | O que faz |
|------|-----------|
| `arachne_capabilities` | Auto-descoberta de capacidades |

> **VRT com LLM local:** o Oito Olhos usa pixel diff + DOM pareado + **CLIP semântico** + **VLM local** (Qwen2.5-VL via Douglas, fallback Samuel) — classificando mudanças como `regression | expected | noise`, com sugestão de correção (`CORRECAO:`) quando detecta bug. **Sem API key de terceiros para o veredito.**

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
        "ARACHNE_API_KEY": "sua_chave_aqui",
        "ARACHNE_BASE_URL": "https://arachne.seu.pet"
      }
    }
  }
}
```

### 3. Ou teste direto

```bash
export ARACHNE_API_KEY="sua_chave"
python3 -m arachne_mcp
```

> Precisa de `httpx`: `pip install httpx`

## 📦 Como funciona

O MCP server é um **cliente HTTP** que chama a API pública do Arachne. Zero dependência de infra local — roda de qualquer lugar.

```
Seu agente AI → MCP stdio → arachne_mcp.py → HTTP → Arachne API → resultado
```

## 🕷️ Exemplos — Oito Olhos (VRT)

```python
# 1. Cria baseline de uma página (1ª vez)
arachne_visual_snapshot(url="https://meusite.com/", name="home")

# 2. Após um deploy: compara e recebe veredito
arachne_visual_diff(url="https://meusite.com/", name="home")
# → { diff_ratio: 0.023, classification: "regression",
#     description: "Botão CTA mudou de cor. CLASSIFICACAO: regression
#     CORRECAO: verificar CSS de .cta — cor deve ser var(--primary)" }

# 3. Mudança esperada? Aprova como novo baseline
arachne_visual_approve(name="home")

# 4. Auditoria sem baseline (gates determinísticos)
arachne_visual_gates(url="https://meusite.com/")
# → verdict: CLEAN | DEFECTS com lista machine-parsable

# 5. Suíte completa → report HTML
arachne_visual_report(tests=[{"url": "https://meusite.com/", "name": "home"},
                             {"url": "https://meusite.com/pricing", "name": "pricing"}])
```

**Dicas:**
- Páginas autenticadas: use `auth: true` — o motor faz login e injeta o token.
- Áreas dinâmicas (stats, relógio): use `mask: [{"selector": ".stats"}]`.
- Diferenças de cor/tema que não são bugs: o **CLIP semântico** classifica como `expected` sem acionar o VLM 7B.

## 📊 Planos

| Plano | Preço | Requests/mês | Features |
|-------|-------|-------------|----------|
| **Free** | R$ 0 | 500 | search, scrape, jobs |
| **Pro** | R$ 49/mês | 10.000 | + browser, vision, transcribe, MCP, **VRT visual** |
| **Enterprise** | R$ 199/mês | 100.000 | + admin, export, suporte dedicado |

## 🏗️ Stack

- **Backend:** FastAPI + Crawl4AI + Whisper + Tesseract + PostgreSQL
- **VRT:** Playwright + ffmpeg (vídeo) + CLIP ViT-B-32 + Qwen2.5-VL (VLM local)
- **Engines:** Trafilatura → Crawl4AI SDK → Sidecar Docker → Camoufox
- **MCP Transport:** stdio (compatível com Claude Desktop, Cursor, Codex, Hermes)

## 🔗 Links

- [Arachne Platform](https://arachne.seu.pet)
- [Developer Portal](https://arachne.seu.pet/dev)
- [Python SDK (PyPI)](https://pypi.org/project/arachne-sdk/)
- [GitHub](https://github.com/Samuelfmedeiros/arachne-mcp)

---

🕷️ Built with the Arachne engine. Open source MCP server.
