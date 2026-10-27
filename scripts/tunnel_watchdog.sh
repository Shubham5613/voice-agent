#!/bin/bash
# Keeps the Cloudflare quick tunnel alive. If the public URL stops answering,
# restarts cloudflared, writes the new URL into .env and redeploys the agent
# so ElevenLabs tool URLs stay correct. Run: nohup scripts/tunnel_watchdog.sh &
cd "$(dirname "$0")/.."
LOG=${TUNNEL_LOG:-/tmp/karta_tunnel.log}
WLOG=${WATCHDOG_LOG:-/tmp/karta_watchdog.log}
start_tunnel() {
  pkill -f "cloudflared tunnel --url http://localhost:8000" 2>/dev/null
  sleep 1
  nohup cloudflared tunnel --url http://localhost:8000 > "$LOG" 2>&1 &
  for i in $(seq 1 20); do
    sleep 1
    URL=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' "$LOG" | head -1)
    [ -n "$URL" ] && break
  done
  [ -z "$URL" ] && { echo "$(date) could not get tunnel URL" >> "$WLOG"; return 1; }
  sed -i '' "s#^PUBLIC_BASE_URL=.*#PUBLIC_BASE_URL=$URL#" .env
  .venv/bin/python agent/deploy_agent.py >> "$WLOG" 2>&1
  echo "$(date) tunnel restarted: $URL  (set post-call webhook to $URL/webhooks/post-call)" >> "$WLOG"
}
while true; do
  URL=$(grep -o '^PUBLIC_BASE_URL=.*' .env | cut -d= -f2)
  code=$(curl -s -m 10 -o /dev/null -w '%{http_code}' "$URL/" 2>/dev/null)
  if [ "$code" != "200" ]; then
    echo "$(date) tunnel $URL returned '$code' -> restarting" >> "$WLOG"
    start_tunnel
  fi
  sleep 60
done
