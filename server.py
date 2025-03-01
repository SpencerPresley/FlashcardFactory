from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# USE THIS
from src.backend.models.user_form import UserForm


"""
class UserForm(BaseModel):
    course_name: str
    difficulty: str
    school_level: str
    subject: str
    subject_material: List[UploadFile]
    num_flash_cards: int | None = None
"""

"""
class FlashCard(BaseModel):
    question: str
    answer: str
"""


class FlashCards(BaseModel):
    # flashCards: List[FlashCard]
    file_name: str


app = FastAPI()

templates = Jinja2Templates(directory="src/frontend/templates")


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def get_form(request: Request):
    return templates.TemplateResponse(request=request, name="form.html")


@app.post("/build")
def make_cards(
    request: Request,
    courseName: str = Form(...),
    difficulty: str = Form(...),
    schoolLevel: str = Form(...),
    subject: str = Form(...),
    subjectMaterial: List[UploadFile] = File(),
    numberFlashCard: Optional[int] = None,
):
    data = UserForm(
        course_name=courseName,
        difficulty=difficulty,
        school_level=schoolLevel,
        subject=subject,
        subject_material=subjectMaterial,
        num_flash_cards=numberFlashCard,
    )

    # flashCards = run(data)
    flash_cards = FlashCards(file_name="sample.txt")

    return templates.TemplateResponse(
        request=request,
        name="flashcards.html",
        context={"Settings": data, "Test": flash_cards},
    )
