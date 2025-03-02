from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional, Union
from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

# USE THIS
from src.backend.models.user_form import UserForm
from src.backend.ai import run

from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

templates = Jinja2Templates(directory="src/frontend/templates")


app.mount("/public", StaticFiles(directory="public"), name="public")
app.mount("/static", StaticFiles(directory="./src/frontend/static"), name="static")


@app.get("/")
def get_form(request: Request):
    return templates.TemplateResponse(request=request, name="form.html")


@app.post("/build")
def make_cards(
    request: Request,
    course_name: str = Form(...),
    difficulty: str = Form(...),
    school_level: str = Form(...),
    subject: str = Form(...),
    rules: str = Form(...),
    subject_material: List[UploadFile] = File(),
    num_flash_cards: Optional[str] = Form(None),
):
    num_flash_cards = (
        int(num_flash_cards)
        if num_flash_cards and num_flash_cards.strip().isdigit()
        else None
    )

    data = UserForm(
        course_name=course_name,
        difficulty=difficulty,
        school_level=school_level,
        subject=subject,
        rules=rules,
        subject_material=subject_material,
        num_flash_cards=num_flash_cards,
    )

    # flash_cards = "sample.txt"

    flash_cards = run(data, os.getenv("GOOGLE_API_KEY"))

    return templates.TemplateResponse(
        request=request,
        name="flashcards.html",
        context={"Settings": data, "flashcards": flash_cards},
    )
