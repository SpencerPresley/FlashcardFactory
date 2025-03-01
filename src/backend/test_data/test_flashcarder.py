from backend.ai import FlashcarderChain
from backend.models import UserFormReg
import os
from dotenv import load_dotenv

load_dotenv()

def load_cleaned_text():
    with open("../static/cleaned_text.txt", "r") as f:
        return f.read()

def test_flashcarder():
    subject_material = load_cleaned_text()
    user_form = UserFormReg(
        course_name="Object Oriented Programming and Design Patterns",
        difficulty="Medium",
        school_level="Undergraduate",
        subject="Computer Science",
        rules="",
        subject_material=subject_material,
        number_flash_cards=20
    )
    
    flashcarder = FlashcarderChain(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model="gemini-2.0-pro-exp-02-05"
    )
    
    flashcarder_output = flashcarder.run(user_form).get("flashcards").get("flashcards")
    
    print(flashcarder_output)
    
    with open("../static/flashcarder_output.txt", "w") as f:
        f.write(flashcarder_output)
    
if __name__ == "__main__":
    test_flashcarder()