# Proxy de cobrança por chamada — Arachne + SettleGrid

Cobra por uso da API do Arachne **sem tocar no Arachne**: o proxy fica na frente, valida a chave
do consumidor e o saldo no SettleGrid, e só então chama a API.

## Por que aqui
O SDK do SettleGrid é Node (`@settlegrid/mcp`) e o Arachne é Python — o acoplamento é este proxy,
não o serviço. Se o SettleGrid não der certo, apagar esta pasta não afeta o Arachne.

## Rodar
```bash
npm install
SG_TOOL_SLUG=<slug-da-tool-no-painel> ARACHNE_API_KEY=<chave-do-arachne> npm start
```

## Config (env — nenhum valor no código)
| Variável | Default | Para que serve |
|---|---|---|
| `SG_TOOL_SLUG` | — (obrigatório) | slug da tool registrada em settlegrid.ai |
| `SG_COST_CENTS` | `5` | custo por chamada, em centavos |
| `SG_METHOD_COSTS` | `{}` | JSON com custo por rota, ex. `{"scrape":10}` |
| `ARACHNE_API_URL` | `http://127.0.0.1:9000` | base da API do Arachne |
| `ARACHNE_API_KEY` | — | chave usada pelo proxy ao chamar o Arachne |
| `PROXY_PORT` | `8787` | porta local |
| `PROXY_ROUTES` | `scrape,search,extract` | rotas expostas como `POST /v1/<rota>` |

## Comportamento verificado (18/10/2026)
- `GET /health` → 200 com tool, rotas e base do Arachne.
- `POST /v1/scrape` sem chave de consumidor → **401 `INVALID_KEY`** e o handler **não roda** (cobrança antes da execução).
- Sem `SG_TOOL_SLUG` → sai com código 2 e mensagem explícita (fail-fast, não sobe cobrando errado).

## Pitfall medido
`settlegridMiddleware` espera um **`Request` da Fetch API** (usa `request.headers.forEach`) —
passar o `req` do Express estoura `TypeError: request.headers.forEach is not a function` (HTTP 500).
Por isso existe o `toFetchRequest()` no `server.mjs`.

## Passos que dependem do painel (não são código)
1. Registrar a tool em settlegrid.ai e copiar o **slug** → `SG_TOOL_SLUG`.
2. Conectar a conta Stripe em *Settings > Payouts* (é para onde o dinheiro vai).
3. Gerar uma chave de consumidor (`sg_live_...`) para o teste ponta a ponta com cobrança real.
