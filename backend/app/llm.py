from typing import List
from .schemas import DraftOption
from .config import settings
import os

# Placeholder: use OpenAI or compatible client
import openai
openai.api_key = settings.OPENAI_API_KEY

SYSTEM_PROMPT = (
    "You are a dating conversation co-pilot. You draft SHORT, respectful, playful replies "
    "that the human user will approve and send. Never auto-send. Stay within the user's persona style. "
    "Avoid generic pickup lines. Ask one sincere, specific question about the other person."
)

TEMPLATE = (
    """
    USER_PERSONA:\n
    - Display name: {display_name}
    - Tone: {tone}\n
    - Cadence: {cadence}\n
    - Emoji policy: {emoji_policy}\n
    - Boundaries: {boundaries}\n
    - Goals: {goals}\n
    CONTEXT:\n
    Incoming message: "{incoming}"
    Extra snippets: {snippets}

    DIRECTION:\n
    Generate {n} distinct options. Each option must include:\n
    - `text`: 1–3 sentences, {cadence} length, tone={tone} (emoji policy={emoji_policy}).\n
    - `rationale`: 1 sentence explaining the move (mirroring, callback, playful tease, etc.).\n
    - Keep it ethical, no manipulation, no explicit sexual content, no PII solicitation.\n
    """
)

async def get_drafts(persona: dict, incoming_text: str, snippets: List[str], n: int, tone_bias: float) -> List[DraftOption]:
    prompt = TEMPLATE.format(
        display_name=persona["display_name"],
        tone=persona["tone"],
        cadence=persona["cadence"],
        emoji_policy=persona["emoji_policy"],
        boundaries=", ".join(persona.get("boundaries", [])),
        goals=", ".join(persona.get("goals", [])),
        incoming=incoming_text,
        snippets=snippets,
        n=n,
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    resp = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",  # swap as needed
        messages=messages,
        temperature=0.8 + 0.2 * tone_bias,
        n=1
    )
    text = resp.choices[0].message["content"]

    # Cheap parse: expect model to output JSON‑like blocks; for MVP, split lines
    options = []
    for chunk in text.split("\n\n"):
        chunk = chunk.strip()
        if not chunk:
            continue
        # Heuristic split
        if "rationale:" in chunk.lower():
            parts = chunk.split("Rationale:") if "Rationale:" in chunk else chunk.split("rationale:")
            draft = parts[0].strip("- *\n ")
            rationale = parts[1].strip() if len(parts) > 1 else ""
            options.append(DraftOption(text=draft, rationale=rationale))
        else:
            options.append(DraftOption(text=chunk, rationale="contextual reply"))
    if len(options) > n:
        options = options[:n]
    return options
