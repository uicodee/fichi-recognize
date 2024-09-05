from typing import Optional

from pydantic import BaseModel, Field


class Alternative(BaseModel):
    text: str


class Chunk(BaseModel):
    alternatives: list[Alternative]


class Response(BaseModel):
    response_type: str = Field(alias="@type")
    chunks: list[Chunk]


class SpeechKit(BaseModel):

    id: str
    done: bool
    createdAt: str
    createdBy: str
    modifiedAt: str
    response: Optional[Response] = Field(default=None)
