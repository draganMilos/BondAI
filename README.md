# Dating Co‑Pilot (Human‑in‑the‑Loop) — MVP v0.1

A policy‑compliant dating chat co‑pilot that drafts replies, with user approval required before sending. No auto‑sending.

## Run locally

```bash
export OPENAI_API_KEY=sk-...
docker compose up --build
# Frontend at http://localhost:5173, Backend at http://localhost:8000
```

## Notes
- Minimal safety checks are included (PII redaction, risky phrase + length).
- Persona controls: tone, cadence, emoji, boundaries, goals, disclosure label.
- Known limitation: LLM output parsing is heuristic. Next step is JSON/function calling.
