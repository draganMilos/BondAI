from .storage import insert_feedback

def log_feedback(user_id: str, draft_text: str, action: str, edit_distance: int | None):
    insert_feedback(user_id, draft_text, action, edit_distance)
