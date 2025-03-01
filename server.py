from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


class UserForm(BaseModel):
    courseWork: str
    difficulty: str
    schoolLevel: str
    subject: str
    subject_material: List[UploadFile]
    numberFlashCard: int
    numberMC: int
    numberSA: int


class FlashCard(BaseModel):
    question: str
    answer: str


class CardDeck(BaseModel):
    flashCards: List[FlashCard]
    downloadLink: str


app = FastAPI()


@app.mount("/public", StaticFiles(directory="public"), name="public")
@app.get("/")
def get_form(request: Request):
    return templates.TemplateResponse(request=request, name="form.html")
