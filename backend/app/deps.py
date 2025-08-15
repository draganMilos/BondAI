from fastapi import Header, HTTPException

async def get_user_id(x_user_id: str | None = Header(default=None)) -> str:
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing X-User-Id header (stub auth)")
    return x_user_id
