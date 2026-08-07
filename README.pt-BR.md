<!-- mcp-name: io.github.Samuelfmedeiros/arachne-mcp -->

# 🕷️ Arachne MCP Server

> [🌐 English](README.md) · 🇧🇷 **Português**

**49 MCP tools** para scraping web, automação de browser, visão computacional, transcrição de áudio, RAG, **Pesquisa de Sentimento Social** e **Visual Regression Testing (VRT) — o Oito Olhos** — tudo através da API do Arachne.

Baseado no [Arachne](https://arachne.seu.pet). Funciona com **Claude Desktop**, **Cursor**, **Codex CLI**, **Hermes** e qualquer cliente MCP.

## ✨ Tools (49)

### 🔍 Web & Dados
| Tool | O que faz | Melhor para |
|------|-----------|------------|
| `arachne_search` | Busca web via DuckDuckGo | Pesquisa, coleta de leads |
| `arachne_scrape` | Markdown limpo de URLs | Páginas estáticas, blogs, docs |
| `arachne_extract` | Extrai QUALQUER formato (áudio, vídeo, PDF, YouTube) | **Canivete suíço** |
| `arachne_browser_extract` | Browser real com evasão Cloudflare/CAPTCHA | Sites que bloqueiam scrapers |
| `arachne_browser_run` | Ações de browser (click, type, login) | Automação de formulários |
| `arachne_screenshot` | Screenshot de URL (página inteira ou viewport) | Evidência visual |
| `arachne_record` | Grava screencast da página (.webm) | Interações, demos |
| `arachne_torrent_extract` | Extrai magnet links de sites BR de torrent | Aquisição de torrents |
| `arachne_download` | Download universal (URL, repo, PyPI, npm) | Baixar qualquer artefato |
| `arachne_query` | Pergunte à sua base RAG | Chatbot com seus dados |

### 🔍 Pesquisa de Sentimento Social
| Tool | O que faz | Melhor para |
|------|-----------|------------|
| `arachne_social_research` | Pesquisa o que as pessoas REALMENTE dizem (HN/Reddit/YouTube, últimos N dias) + AI judge via VLM local | **Hype vs realidade, reclamações, sentimento de mercado** |

### 👁️ Visão & Áudio
| Tool | O que faz | Melhor para |
|------|-----------|------------|
| `arachne_vision` | Análise de imagem: OCR, cores, rostos, descrição IA | Extração de texto de fotos |
| `arachne_screenshot_vision` | Screenshot + pipeline de visão completo | Inspeção visual de páginas |
| `arachne_pdf_vision` | Extrai imagens de PDF + análise de visão | PDFs escaneados |
| `arachne_analyze_video` | Metadados de vídeo: cores, OCR, geometria, VQA, áudio | Entendimento de vídeo |
| `arachne_transcribe` | Transcrição de áudio/vídeo/YouTube com Whisper | Podcast, reunião, vídeo |

### 🕷️ Oito Olhos — Visual Regression Testing (VRT)
| Tool | O que faz | Melhor para |
|------|-----------|------------|
| `arachne_visual_snapshot` | Captura URL → cria baseline (1ª vez) ou compara | Testes visuais idempotentes |
| `arachne_visual_diff` | Compara com baseline → diff + veredito semântico | Verificação pós-deploy |
| `arachne_visual_gates` | Auditoria determinística: overflow, colisão de texto, erros JS | **Sem key, sem baseline** |
| `arachne_visual_report` | Suíte de testes → HTML lado a lado | Revisão consolidada |
| `arachne_visual_approve` | Promove atual → novo baseline | Aceitar mudança esperada |
| `arachne_visual_list` | Lista baselines + status | Monitorar o que existe |
| `arachne_visual_video` | VRT de vídeo: grava screencast + compara (animações) | Hover, carrosséis, transições |
| `arachne_visual_video_report` | Suíte de vídeo → relatório HTML interativo | Revisão de regressão de animação |

### 🤖 Desktop & Agêntico
| Tool | O que faz | Melhor para |
|------|-----------|------------|
| `arachne_desktop` | Controle de desktop (janelas, type, key, click) | Automação de SO |
| `arachne_desktop_os` | Desktop agêntico com "olho" VLM (screenshot + descrição) | Ver antes de agir |
| `arachne_observe` | Screenshot + bounding boxes numerados clicáveis | Navegação de agente GUI |

### 📦 GitHub / GitLab / Pacotes
| Tool | O que faz |
|------|-----------|
| `arachne_repo_download` | Baixa repo GitHub como zip (branch/token) |
| `arachne_repo_fork` | Faz fork de repo GitHub |
| `arachne_repo_forks` | Lista forks por estrelas |
| `arachne_repo_index` | Baixa + indexa repo no RAG |
| `arachne_releases` | Lista releases GitHub com assets |
| `arachne_release_download` | Baixa asset de release |
| `arachne_pypi_download` | Baixa pacote PyPI (sdist/wheel) |
| `arachne_npm_download` | Baixa pacote npm (tarball) |
| `arachne_gitlab_download` | Baixa projeto GitLab (archive) |

### 🧠 Code Knowledge Graph
| Tool | O que faz |
|------|-----------|
| `code_graph` | Explora estrutura de código: stats, busca, rotas, arquivos, deps |
| `kg_context` | Contexto de código rankeado BFS (~2K tokens) |
| `kg_communities` | Detecção de comunidades (Leiden/greedy) |
| `kg_god_nodes` | Entidades de código mais influentes (PageRank) |
| `kg_watch` | Git watcher — detecção incremental de mudanças |

### 🧭 Utilitários
| Tool | O que faz |
|------|-----------|
| `arachne_capabilities` | Auto-descobre capacidades |
| `arachne_ping` | Health check |
| `arachne_metrics` | Métricas do servidor (CPU, RAM, disco) |
| `arachne_plan` | Análise de objetivo → sugestão de cadeia de tools |
| `arachne_calc` | Calculadora matemática segura (AST-sandbox) |
| `arachne_format_converter` | Conversor universal (65+ formatos) |
| `arachne_sandbox_status` | Verifica disponibilidade do sandbox ai-jail |

> **VRT com LLM local:** Oito Olhos usa pixel diff + pareamento DOM + **triagem semântica CLIP** + **VLM local** (Qwen2.5-VL via Douglas, espelho Samuel como fallback) — classificando mudanças como `regression | expected | noise`, com sugestão de correção (`CORRECAO:`) quando detecta bug. **Sem API key de terceiros para o veredito.**

> **Pesquisa Social com AI judge local:** `arachne_social_research` busca no Hacker News (Algolia), Reddit (JSON API + fallback browser_agent/Camoufox) e YouTube (yt-dlp) nos últimos N dias, pontua por engajamento real (upvotes/points/views) e sintetiza um relatório **hype vs realidade** com VLM local (sem API keys de terceiros).

## 🚀 Início Rápido

### 1. Obtenha uma API key

Crie em **[arachne.seu.pet/dev](https://arachne.seu.pet/dev)** (Plano Free: 500 req/mês).

### 2. Configure no Claude Desktop

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

### 3. Ou rode direto

```bash
pip install arachne-mcp
export ARACHNE_API_KEY="arn_your_key_here"
python3 -m arachne_mcp
```

## 📡 Arquitetura

O servidor MCP é um **proxy leve**: encaminha cada chamada de tool para a API do
Arachne (`POST /api/mcp/proxy`), que executa a tool no servidor e retorna o
resultado. Isso mantém o cliente leve (só `httpx`), enquanto todo o trabalho
pesado — browser, VLM, visão, RAG — roda no servidor Arachne.

```text
Claude Desktop / Cursor / Codex
        │  MCP (stdio)
        ▼
arachne-mcp (proxy leve, 49 tools)
        │  HTTP + X-API-Key
        ▼
API Arachne (arachne.seu.pet) → executa tool → retorna JSON
```

## 🔐 Segurança

- **Auth por API key**: toda requisição carrega `X-API-Key` (crie em `/dev`)
- **Rate limits** aplicados no servidor por plano
- Nenhum código roda no cliente — o proxy só encaminha argumentos
