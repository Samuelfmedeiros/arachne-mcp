// Proxy de cobrança por chamada na frente da API do Arachne (SettleGrid).
//
// Por que existe: o Arachne já tem API e MCP, mas nada cobra por uso de terceiros.
// O SDK do SettleGrid é Node — este proxy põe o billing na frente, SEM tocar no Arachne.
//
// Fluxo de uma chamada:
//   cliente -> POST /v1/<rota> (Authorization: Bearer sg_live_...) -> SettleGrid valida
//   saldo/chave -> handler roda -> resposta volta -> chamada é medida (cobrada).
//   Sem chave válida: 401/402 e o handler NÃO roda.
//
// Config (env, sem hardcode):
//   SG_TOOL_SLUG      slug da tool registrada em settlegrid.ai (obrigatório p/ cobrar)
//   SG_COST_CENTS     custo por chamada em centavos (default 5)
//   SG_METHOD_COSTS   JSON opcional: {"scrape":10,"search":5}
//   ARACHNE_API_URL   base da API do Arachne (default http://127.0.0.1:9000)
//   ARACHNE_API_KEY   chave da API do Arachne usada pelo proxy
//   PROXY_PORT        porta local (default 8787)
//   PROXY_ROUTES      CSV de rotas expostas (default: scrape,search,extract)
//
// PITFALL medido: `settlegridMiddleware` espera um Request da Fetch API (usa
// headers.forEach), NÃO o `req` do Express — por isso `toFetchRequest()`.
import express from 'express';
import { settlegridMiddleware } from '@settlegrid/mcp';

const PORT = Number(process.env.PROXY_PORT || 8787);
const TOOL = process.env.SG_TOOL_SLUG || '';
const COST = Number(process.env.SG_COST_CENTS || 5);
const ARACHNE = process.env.ARACHNE_API_URL || 'http://127.0.0.1:9000';
const AKEY = process.env.ARACHNE_API_KEY || '';
const ROUTES = (process.env.PROXY_ROUTES || 'scrape,search,extract').split(',').map((s) => s.trim()).filter(Boolean);

let METHOD_COSTS = {};
try {
  METHOD_COSTS = JSON.parse(process.env.SG_METHOD_COSTS || '{}');
} catch {
  console.error('[aviso] SG_METHOD_COSTS não é JSON válido — usando custo padrão');
}

if (!TOOL) {
  console.error('[erro] SG_TOOL_SLUG não definido — registre a tool em settlegrid.ai e exporte o slug.');
  process.exit(2);
}

const withBilling = settlegridMiddleware({ toolSlug: TOOL, costCents: COST });
const app = express();
app.use(express.json({ limit: '1mb' }));

function toFetchRequest(req) {
  const url = `${req.protocol}://${req.get('host')}${req.originalUrl}`;
  const headers = new Headers();
  for (const [k, v] of Object.entries(req.headers)) {
    if (typeof v === 'string') headers.set(k, v);
    else if (Array.isArray(v)) headers.set(k, v.join(','));
  }
  const hasBody = !['GET', 'HEAD'].includes(req.method);
  return new Request(url, {
    method: req.method,
    headers,
    body: hasBody ? JSON.stringify(req.body ?? {}) : undefined,
  });
}

for (const route of ROUTES) {
  app.post(`/v1/${route}`, async (req, res) => {
    const handler = async () => {
      const r = await fetch(`${ARACHNE}/${route}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...(AKEY ? { 'X-API-Key': AKEY } : {}) },
        body: JSON.stringify(req.body ?? {}),
      });
      return new Response(await r.text(), {
        status: r.status,
        headers: { 'Content-Type': r.headers.get('content-type') || 'application/json' },
      });
    };
    const out = await withBilling(toFetchRequest(req), handler);
    res.status(out.status).send(await out.text());
  });
}

app.get('/health', (_req, res) => res.json({ ok: true, tool: TOOL, routes: ROUTES, arachne: ARACHNE }));
app.get('/.well-known/mcp-server', (_req, res) => res.json({ name: 'Arachne', billing: { toolSlug: TOOL, costCents: COST } }));

app.listen(PORT, '127.0.0.1', () => {
  console.log(`proxy ouvindo em http://127.0.0.1:${PORT} | tool=${TOOL} | rotas=${ROUTES.join(',')}`);
});
