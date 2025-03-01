from pydantic import BaseModel

class CleanerOutput(BaseModel):
    cleaned_text: str