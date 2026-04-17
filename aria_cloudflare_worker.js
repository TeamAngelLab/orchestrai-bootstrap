/**
 * ORCHESTRAI™ Aria — Cloudflare Worker Proxy
 * API key stored as Cloudflare secret — never in public code
 * Deploy: wrangler deploy
 * Set secret: wrangler secret put ANTHROPIC_API_KEY
 */

const RATE_LIMIT = new Map();
const MAX_REQUESTS_PER_HOUR = 20;

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders(origin), status: 204 });
    }

    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    const now = Date.now();
    const limit = RATE_LIMIT.get(ip);
    if (limit && now < limit.reset) {
      if (limit.count >= MAX_REQUESTS_PER_HOUR) {
        return new Response(JSON.stringify({ error: 'Rate limit exceeded.' }), {
          status: 429, headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) }
        });
      }
      limit.count++;
    } else {
      RATE_LIMIT.set(ip, { count: 1, reset: now + 3600000 });
    }

    let body;
    try { body = await request.json(); }
    catch { return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400, headers: corsHeaders(origin) }); }

    if (!body.messages || !Array.isArray(body.messages)) {
      return new Response(JSON.stringify({ error: 'messages array required' }), { status: 400, headers: corsHeaders(origin) });
    }

    const anthropicResponse = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-6',
        max_tokens: 1000,
        system: body.system || '',
        messages: body.messages.slice(-10)
      })
    });

    const data = await anthropicResponse.json();
    return new Response(JSON.stringify(data), {
      status: anthropicResponse.status,
      headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) }
    });
  }
};

function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin': origin || '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400'
  };
}
