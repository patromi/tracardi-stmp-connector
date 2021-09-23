from pydantic import BaseModel
from typing import Optional


class Smtp(BaseModel):
    smtp: str
    port: int
    username: str
    password: str
    timeout: int = 15


class Message(BaseModel):
    send_to: str
    send_from: str
    title: Optional[str] = ''
    reply_to: Optional[str] = None
    message: Optional[str] = ''


class Configuration(BaseModel):
    server: Smtp
    message: Message
