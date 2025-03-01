import os
import io
import json
from pathlib import Path
from typing import List
from fastapi import UploadFile
from fastapi.datastructures import UploadFile as FastAPIUploadFile
import dotenv

from backend.ai import run
from backend.models import UserForm

dotenv.load_dotenv()

def create_upload_file(file_path: str | Path, content_type: str = None) -> UploadFile:
    """Create a mock FastAPI UploadFile from a file path for testing.
    
    Args:
        file_path: Path to the file
        content_type: MIME type of the file (optional)
    
    Returns:
        A FastAPI UploadFile object
    """
    if content_type is None:
        # Guess content type based on extension
        ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.pdf': 'application/pdf',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.txt': 'text/plain',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        }
        content_type = content_types.get(ext, 'application/octet-stream')
    
    # Read the file content
    with open(file_path, "rb") as f:
        content = f.read()
    
    # Create a file-like object
    file_like = io.BytesIO(content)
    file_like.seek(0)
    
    # Create and return a FastAPI UploadFile
    return FastAPIUploadFile(
        file=file_like,
        size=len(content),
        filename=os.path.basename(file_path),
        headers={"content-type": content_type}
    )
    
def create_test_user_form(file_paths: List[str | Path]) -> UserForm:
    """Create a mock UserForm with the given files as subject material.
    
    Args:
        file_paths: List of paths to files to include as subject material
        
    Returns:
        A UserForm object with test data
    """
    # Create UploadFile objects from the file paths
    upload_files = [create_upload_file(path) for path in file_paths]
    
    # Create and return a UserForm with test data
    return UserForm(
        course_name="Computer Science 101",
        difficulty="Medium",
        school_level="University",
        subject="Computer Science",
        rules="Create flashcards with clear questions and answers",
        subject_material=upload_files,
        num_flash_cards=50
    )
    
def test_orchestrator_run():
    """Test the run() method of the AI orchestrator with sample files."""
    
    print("====== Testing AI Orchestrator ======")
    
    # Get API key from environment variable
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set")
        return
    
    # Define test file paths - update these to point to your test files
    project_root = Path(__file__).parents[3]  # Go up to project root
    test_files_dir = project_root / "test_files"  # Create this directory with test files
    
    # Test file paths - update these to match your actual test files
    pdf_path = test_files_dir / "sample.pdf"
    docx_path = test_files_dir / "sample.docx"
    txt_path = test_files_dir / "sample.txt"
    pptx_path = test_files_dir / "sample.pptx"
    
    # Create a list of existing file paths
    existing_files = []
    for path in [pdf_path, docx_path, txt_path, pptx_path]:
        if path.exists():
            existing_files.append(path)
    
    if not existing_files:
        print("Error: No test files found in the test_files directory")
        return
    
    # Print the files we'll be using
    print(f"Using {len(existing_files)} test files:")
    for path in existing_files:
        print(f"  - {path}")
    
    # Create a UserForm with the test files
    print("\nCreating test UserForm...")
    user_form = create_test_user_form(existing_files)
    
    # Run the orchestrator
    print("\nRunning AI orchestrator pipeline...")
    try:
        result = run(
            user_form=user_form,
            api_key=api_key,
        )
        
        # Print the results
        print("\n====== Flashcards Generated ======")
        
        # Check if result is a dictionary with expected keys
        if isinstance(result, dict) and "flashcards" in result:
            print(f"File saved to: {result.get('flashcards_file_path', 'Unknown location')}")
            
            # Extract flashcards from the result
            flashcards = result.get("flashcards", "")
            print(f"Flashcards string length: {len(flashcards)}")
            
            # Try to parse it as JSON
            try:
                parsed_flashcards = json.loads(flashcards)
                print("Successfully parsed as JSON")
                
                if isinstance(parsed_flashcards, dict) and "flashcards" in parsed_flashcards:
                    flashcards_str = parsed_flashcards["flashcards"]
                    print(f"Number of flashcard pairs: {flashcards_str.count(';')}")
                    
                    # Print a sample of the flashcards
                    print("\nSample flashcards:")
                    pairs = flashcards_str.split(";")
                    for i, pair in enumerate(pairs[:3]):
                        if pair.strip():  # Skip empty pairs
                            try:
                                question, answer = pair.split(",", 1)
                                print(f"\nFlashcard {i+1}:")
                                print(f"  Question: {question.strip()}")
                                print(f"  Answer: {answer.strip()}")
                            except ValueError:
                                print(f"  Invalid format: {pair}")
                
                elif isinstance(parsed_flashcards, list):
                    print(f"Number of flashcards: {len(parsed_flashcards)}")
                    # Print first 3 flashcards
                    for i, card in enumerate(parsed_flashcards[:3]):
                        print(f"\nFlashcard {i+1}:")
                        if isinstance(card, dict):
                            print(f"  Question: {card.get('question', 'No question')}")
                            print(f"  Answer: {card.get('answer', 'No answer')}")
                        else:
                            print(f"  {card}")
                else:
                    print("JSON result preview:")
                    print(str(parsed_flashcards)[:500] + "..." if len(str(parsed_flashcards)) > 500 else parsed_flashcards)
            
            except json.JSONDecodeError:
                # Not valid JSON, just print part of the string
                print("Flashcards text (first 500 chars):")
                print(flashcards[:500] + "..." if len(flashcards) > 500 else flashcards)
        
        else:
            print(f"Unexpected result type: {type(result)}")
            print(str(result)[:500] + "..." if len(str(result)) > 500 else result)
        
        # No need to save the output ourselves since it's already being saved by the run() function
        print(f"\nOutput has been saved by the orchestrator")
        print("\n====== Test Complete ======")
        
    except Exception as e:
        print(f"\nError running orchestrator: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """Run the test."""
    test_orchestrator_run()

if __name__ == "__main__":
    main()