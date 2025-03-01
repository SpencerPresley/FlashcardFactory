from __future__ import annotations

from typing import List, TYPE_CHECKING
import os

from backend.ai import CleanerChain, FlashcarderChain
from backend.models import UserFormReg

if TYPE_CHECKING:
    from backend.models import UserForm
    from fastapi import UploadFile


def run(
    user_form: UserForm,
    api_key: str,
    cleaner_model: str | None = "gemini-2.0-flash-thinking-exp-01-21",
    flashcarder_model: str | None = "gemini-2.0-pro-exp-02-05"
):
    subject_material = _run_parsing(user_form.subject_material)
    cleaned_text = _run_cleaner(
        subject_material,
        api_key,
        cleaner_model
    )
    flashcards = _run_flashcarder(
        cleaned_text,
        user_form,
        api_key,
        flashcarder_model
    )
    return flashcards

def _run_parsing(subject_material: List[UploadFile]) -> str:
    """Parse documents from uploaded files using the appropriate parser strategy.
    
    Args:
        subject_material: List of UploadFile objects containing documents
        
    Returns:
        Combined text extracted from all documents
    """
    if not subject_material:
        raise ValueError("No subject material provided")
    
    # Extract text from each file and combine
    combined_texts = []
    parsing_errors = []
    successful_files = []
    
    for upload_file in subject_material:
        try:
            # Reset file pointer first to ensure we can read from the beginning
            upload_file.file.seek(0)
            
            # Get appropriate parser for this file type and parse it
            from backend.parsers import parse_document
            extracted_text = parse_document(upload_file=upload_file)
            
            if extracted_text:
                combined_texts.append(extracted_text)
                successful_files.append(upload_file.filename)
                print(f"Successfully parsed {upload_file.filename}: {len(extracted_text)} chars extracted")
            else:
                parsing_errors.append(f"No text could be extracted from {upload_file.filename}")
            
            # Reset file pointer after reading
            upload_file.file.seek(0)
            
        except ValueError as e:
            # Unsupported file type or parsing error
            error_msg = f"Could not parse file {upload_file.filename}: {str(e)}"
            parsing_errors.append(error_msg)
            print(f"Warning: {error_msg}")
            continue
        
        except Exception as e:
            # Other unexpected errors
            error_msg = f"Error parsing file {upload_file.filename}: {str(e)}"
            parsing_errors.append(error_msg)
            print(f"Error: {error_msg}")
            continue
    
    if not combined_texts and parsing_errors:
        # If no text was extracted but errors occurred, raise an error
        raise ValueError(
            f"Failed to extract text from any files. Errors: {'; '.join(parsing_errors)}"
        )
    
    print(f"Successfully parsed {len(successful_files)} files: {', '.join(successful_files)}")
    print(f"Combined content length: {sum(len(text) for text in combined_texts)} chars")
    
    # Join all extracted text with double newlines to separate content from different files
    return "\n\n".join(combined_texts)

def _run_cleaner(
    subject_material: str,
    api_key: str,
    cleaner_model: str,
) -> str:
    cleaner = CleanerChain(
        api_key=api_key,
        model=cleaner_model
    )
    cleaned_text = cleaner.run(subject_material).get("cleaned_text").get("cleaned_text")
    return cleaned_text

def _run_flashcarder(
    subject_material: str,
    user_form: UserForm,
    api_key: str,
    flashcarder_model: str,
) -> str:
    user_form_reg = UserFormReg(
        course_name=user_form.course_name,
        difficulty=user_form.difficulty,
        school_level=user_form.school_level,
        subject=user_form.subject,
        rules=user_form.rules,
        subject_material=subject_material,
        num_flash_cards=user_form.num_flash_cards
    )
    
    flashcarder = FlashcarderChain(
        api_key=api_key,
        model=flashcarder_model
    )
    
    flashcards = flashcarder.run(user_form_reg).get("flashcards").get("flashcards")
    
    return flashcards
