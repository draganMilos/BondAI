from typing import List, Optional
from pydantic import BaseModel, Field

class PersonaCreate(BaseModel):
    display_name: str
    tone: str = Field("warm", description="warm | witty | direct | playful | respectful")
    cadence: str = Field("short", description="short | medium | long")
    emoji_policy: str = Field("light", description="none | light | moderate | expressive")
    boundaries: List[str] = []  # e.g., ["no explicit sexual content", "no politics"]
    goals: List[str] = ["build rapport", "plan a coffee date"]
    disclosure: bool = False  # attach `drafted-with-ai` label

class PersonaOut(PersonaCreate):
    id: str

class DraftRequest(BaseModel):
    user_id: str
    persona_id: str
    incoming_text: str
    context_snippets: List[str] = []
    num_options: int = 3
    tone_bias: float = 0.0  # -1 cautious, 0 neutral, +1 bold

class DraftOption(BaseModel):
    text: str
    rationale: str
    risk_flags: List[str] = []
    disclosure: Optional[str] = None

class DraftResponse(BaseModel):
    options: List[DraftOption]

class FeedbackIn(BaseModel):
    user_id: str
    draft_text: str
    action: str  # approved | edited | rejected
    edit_distance: Optional[int] = None
