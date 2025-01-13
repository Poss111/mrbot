from pydantic import BaseModel

class LoggerDetails(BaseModel):
    user_id: int
    guild_id: int
    command: str
    id: int