from typing import Optional

from pydantic import BaseModel, HttpUrl, Field


class Url(BaseModel):
    long_url: HttpUrl
    short_url: Optional[str] = Field(None, min_length=5, max_length=30)

    class Config:
        orm_mode = True
