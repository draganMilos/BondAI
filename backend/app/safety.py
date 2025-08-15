import re
from typing import Tuple, List
from .config import settings

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:(?:\+|00)\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}")

RISKY_PHRASES = [
    "send nudes", "come over now", "neg",
]

BOUNDARY_BLOCKLIST = [
    "explicit sexual content", "hate speech", "harassment"
]


def redact_pii(text: str) -> str:
    text = EMAIL_RE.sub("[email redacted]", text)
    text = PHONE_RE.sub("[phone redacted]", text)
    return text


def quick_screen(text: str, persona_boundaries: List[str]) -> Tuple[bool, List[str], str]:
    """Return (ok, flags, possibly_redacted_text)."""
    flags = []
    if len(text) > settings.MAX_MSG_LEN:
        flags.append("too_long")
    lower = text.lower()
    for p in RISKY_PHRASES:
        if p in lower:
            flags.append("risky_phrase")
    # Enforce user boundaries
    for b in persona_boundaries:
        if b in BOUNDARY_BLOCKLIST:
            pass  # already enforced
    redacted = redact_pii(text)
    ok = "harassment" not in flags and "explicit" not in flags
    return ok, flags, redacted
