from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from .config import settings

_engine: Engine | None = None

def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    return _engine

def insert_feedback(user_id: str, draft_text: str, action: str, edit_distance: int | None):
    eng = get_engine()
    with eng.begin() as conn:
        conn.execute(text(
            """
            insert into feedback(user_id, draft_text, action, edit_distance)
            values (:user_id, :draft_text, :action, :edit_distance)
            """
        ), {
            "user_id": user_id,
            "draft_text": draft_text,
            "action": action,
            "edit_distance": edit_distance
        })
