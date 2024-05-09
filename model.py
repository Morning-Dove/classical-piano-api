from pydantic import BaseModel

class Music(BaseModel):
    name: str
    alt_name: str | None
    difficulty: int
    composer_id: int


class Composer(BaseModel):
    name: str
    composer_id: int
    home_country: str

