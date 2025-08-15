from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import PersonaCreate, PersonaOut, DraftRequest, DraftResponse, FeedbackIn
from .persona import create_persona, get_persona
from .safety import quick_screen
from .llm import get_drafts
from .deps import get_user_id
from .config import settings
from .telemetry import log_feedback
import asyncio

app = FastAPI(title="Dating Co‑Pilot API", version="0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

@app.post("/persona", response_model=PersonaOut)
async def create_persona_route(p: PersonaCreate, user_id: str = Depends(get_user_id)):
    return create_persona(user_id, p)

@app.post("/drafts", response_model=DraftResponse)
async def drafts(req: DraftRequest, user_id: str = Depends(get_user_id)):
    persona = get_persona(req.persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")

    ok, flags, redacted_incoming = quick_screen(req.incoming_text, persona.boundaries)
    if not ok:
        raise HTTPException(status_code=400, detail={"error": "safety_block", "flags": flags})

    options = await get_drafts(persona.dict(), redacted_incoming, req.context_snippets, req.num_options, req.tone_bias)

    # Attach disclosure if persona requests it
    if persona.disclosure or settings.DISCLOSURE_DEFAULT:
        for o in options:
            o.disclosure = "Drafted with AI — approved by me"

    return DraftResponse(options=options)

@app.post("/feedback")
async def feedback(fb: FeedbackIn, user_id: str = Depends(get_user_id)):
    log_feedback(user_id, fb.draft_text, fb.action, fb.edit_distance)
    return {"ok": True}

@app.get("/health")
async def health():
    return {"status": "ok"}
