from .schemas import PersonaCreate, PersonaOut
import uuid
from sqlalchemy import text
from .storage import get_engine


def create_persona(user_id: str, p: PersonaCreate) -> PersonaOut:
    pid = str(uuid.uuid4())
    eng = get_engine()
    with eng.begin() as conn:
        conn.execute(text("""
            insert into personas(id, user_id, display_name, tone, cadence, emoji_policy, boundaries, goals, disclosure)
            values (:id, :user_id, :display_name, :tone, :cadence, :emoji_policy, :boundaries, :goals, :disclosure)
        """), {
            "id": pid,
            "user_id": user_id,
            "display_name": p.display_name,
            "tone": p.tone,
            "cadence": p.cadence,
            "emoji_policy": p.emoji_policy,
            "boundaries": ",".join(p.boundaries),
            "goals": ",".join(p.goals),
            "disclosure": p.disclosure,
        })
    return PersonaOut(id=pid, **p.dict())


def get_persona(pid: str) -> PersonaOut | None:
    eng = get_engine()
    with eng.connect() as conn:
        row = conn.execute(text("select * from personas where id=:id"), {"id": pid}).fetchone()
        if not row:
            return None
        return PersonaOut(
            id=row.id,
            display_name=row.display_name,
            tone=row.tone,
            cadence=row.cadence,
            emoji_policy=row.emoji_policy,
            boundaries=row.boundaries.split(",") if row.boundaries else [],
            goals=row.goals.split(",") if row.goals else [],
            disclosure=bool(row.disclosure),
        )
