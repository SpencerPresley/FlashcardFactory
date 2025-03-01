from pydantic import BaseModel

class FlashcarderOutput(BaseModel):
    flashcards: str
