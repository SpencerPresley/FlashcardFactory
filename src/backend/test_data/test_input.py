from backend.models.user_form import UserForm
from fastapi import UploadFile
import io
import os
from pathlib import Path
from unittest.mock import Mock
from starlette.datastructures import UploadFile as StarletteUploadFile
from fastapi.datastructures import UploadFile as FastAPIUploadFile

project_root = Path(__file__).parents[3]  # Go up 3 levels from this file
pdf_path = project_root / "public" / "StrategyPatternInClassExercise.pdf"

# Create a FastAPI UploadFile compatible object
def create_upload_file_from_path(file_path, filename=None):
    if filename is None:
        filename = os.path.basename(file_path)
    
    with open(file_path, "rb") as f:
        content = f.read()
    
    file_like = io.BytesIO(content)
    
    # Create a SpooledTemporaryFile-like object (what FastAPI expects)
    spool = Mock()
    spool.read = lambda: content
    spool.seek = lambda *args: file_like.seek(*args)
    
    # Create a FastAPI UploadFile
    return FastAPIUploadFile(
        file=file_like,
        size=len(content),
        filename=filename,
        headers={"content-type": "application/pdf"}
    )

# Load PDF for parsing
from backend.parsers.pdf_parser import PDFParser, extract_text_from_path

# Create the FastAPI UploadFile with the actual PDF content
mock_file1 = create_upload_file_from_path(pdf_path)

# Method 1: Use the PDFParser class with a file path
parser1 = PDFParser(file_path=pdf_path)
pdf_text1 = parser1.get_full_text()
print(f"PDF content length (from file path): {len(pdf_text1)} chars")
print(f"First 100 chars: {pdf_text1[:100]}")

# Method 2: Use the PDFParser class with an UploadFile
# Reset the file pointer first
mock_file1.file.seek(0)
parser2 = PDFParser(upload_file=mock_file1)
pdf_text2 = parser2.get_full_text()
print(f"PDF content length (from UploadFile): {len(pdf_text2)} chars")

# Get page-by-page content
pages = parser1.get_text_by_pages()
print(f"Number of pages: {len(pages)}")

# Get content with metadata
pages_with_metadata = parser1.get_text_with_metadata()
if pages_with_metadata:
    print(f"First page number: {pages_with_metadata[0]['page_number']}")
    print(f"Metadata: {list(pages_with_metadata[0]['metadata'].keys())}")

# Or simply use the convenience function for quick extraction
quick_text = extract_text_from_path(pdf_path)
print(f"Quick extract length: {len(quick_text)} chars")

# Create test input with the correctly typed file
test_input = UserForm(
    course_name="Object-Oriented Programming and Design Patterns",
    difficulty="Medium",
    school_level="Undergraduate",
    subject="Computer Science",
    subject_material=[mock_file1],
    num_flash_cards=20,
)

# Print test_input details
print(f"Created test_input with course_name: {test_input.course_name}")
print(f"Number of files: {len(test_input.subject_material)}")

print(f'\n\nTEST INPUT:\n\n{test_input}')

# Write the extracted PDF text to a file
# Generate output filename based on the PDF name
pdf_name = os.path.basename(pdf_path)
txt_name = pdf_name.rsplit('.', 1)[0] + '.txt'  # Replace .pdf with .txt
output_path = project_root / "output" / txt_name

# Create output directory if it doesn't exist
output_dir = output_path.parent
output_dir.mkdir(exist_ok=True, parents=True)

# Write the text to the file
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(pdf_text1)

print(f"\nExtracted PDF text has been written to: {output_path}")

# Optionally, write each page to a separate file
pages_dir = output_dir / (pdf_name.rsplit('.', 1)[0] + "_pages")
pages_dir.mkdir(exist_ok=True)

for i, page_text in enumerate(pages):
    page_file = pages_dir / f"page_{i+1:03d}.txt"
    with open(page_file, 'w', encoding='utf-8') as f:
        f.write(page_text)

print(f"Individual pages have been written to: {pages_dir}")