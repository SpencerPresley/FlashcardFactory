"""Test script for the document parser strategy pattern.
This demonstrates how to use the parsers with different file types,
including mocking upload files for testing.
"""

import io
import os
from pathlib import Path
from unittest.mock import Mock
from fastapi import UploadFile
from fastapi.datastructures import UploadFile as FastAPIUploadFile
from typing import List, Dict, Any

# Import our parsers
from backend.parsers import (
    parse_document,
    PDFParser,
    DOCXParser,
    TXTParser,
    PPTXParser,
    BaseDocumentParser,
)


# Helper function to create mock upload files
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
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".txt": "text/plain",
            ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        }
        content_type = content_types.get(ext, "application/octet-stream")

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
        headers={"content-type": content_type},
    )


def test_single_file_parsing():
    """Test parsing a single file of each supported type."""

    # Define test file paths - update these to point to your test files
    project_root = Path(__file__).parents[3]  # Go up to project root
    test_files_dir = (
        project_root / "test_files"
    )  # Create this directory with test files

    # Test file paths - update these to match your actual test files
    pdf_path = test_files_dir / "sample.pdf"
    docx_path = test_files_dir / "sample.docx"
    txt_path = test_files_dir / "sample.txt"
    pptx_path = test_files_dir / "sample.pptx"

    # Create test text file if it doesn't exist
    if not txt_path.exists():
        txt_path.parent.mkdir(exist_ok=True, parents=True)
        with open(txt_path, "w") as f:
            f.write(
                "This is a sample text file for testing the TXT parser.\nIt contains multiple lines."
            )

    # Test each file type if they exist
    results = {}

    if pdf_path.exists():
        print(f"\n--- Testing PDF parsing ---")
        # Test direct file path parsing
        pdf_text_direct = parse_document(file_path=pdf_path)
        print(f"PDF content length (direct): {len(pdf_text_direct)} chars")
        print(f"First 100 chars: {pdf_text_direct[:100]}")

        # Test upload file parsing
        pdf_upload = create_upload_file(pdf_path)
        pdf_text_upload = parse_document(upload_file=pdf_upload)
        print(f"PDF content length (upload): {len(pdf_text_upload)} chars")

        # Test specific parser class
        pdf_parser = PDFParser.from_path(pdf_path)
        pdf_text_class = pdf_parser.parse()
        print(f"PDF content length (class): {len(pdf_text_class)} chars")

        results["pdf"] = {
            "direct": len(pdf_text_direct),
            "upload": len(pdf_text_upload),
            "class": len(pdf_text_class),
        }

        # Verify that all methods produced the same content
        assert (
            pdf_text_direct == pdf_text_upload == pdf_text_class
        ), "PDF parsing methods produced different results"

    if docx_path.exists():
        print(f"\n--- Testing DOCX parsing ---")
        # Test direct file path parsing
        docx_text_direct = parse_document(file_path=docx_path)
        print(f"DOCX content length (direct): {len(docx_text_direct)} chars")
        print(f"First 100 chars: {docx_text_direct[:100]}")

        # Test upload file parsing
        docx_upload = create_upload_file(docx_path)
        docx_text_upload = parse_document(upload_file=docx_upload)
        print(f"DOCX content length (upload): {len(docx_text_upload)} chars")

        results["docx"] = {
            "direct": len(docx_text_direct),
            "upload": len(docx_text_upload),
        }

    if txt_path.exists():
        print(f"\n--- Testing TXT parsing ---")
        # Test direct file path parsing
        txt_text_direct = parse_document(file_path=txt_path)
        print(f"TXT content length (direct): {len(txt_text_direct)} chars")
        print(f"Full TXT content: {txt_text_direct}")

        # Test upload file parsing
        txt_upload = create_upload_file(txt_path)
        txt_text_upload = parse_document(upload_file=txt_upload)
        print(f"TXT content length (upload): {len(txt_text_upload)} chars")

        results["txt"] = {
            "direct": len(txt_text_direct),
            "upload": len(txt_text_upload),
        }

        # Verify that both methods produced the same content
        assert (
            txt_text_direct == txt_text_upload
        ), "TXT parsing methods produced different results"

    if pptx_path.exists():
        print(f"\n--- Testing PPTX parsing ---")
        # Test direct file path parsing
        pptx_text_direct = parse_document(file_path=pptx_path)
        print(f"PPTX content length (direct): {len(pptx_text_direct)} chars")
        print(f"First 100 chars: {pptx_text_direct[:100]}")

        # Test upload file parsing
        pptx_upload = create_upload_file(pptx_path)
        pptx_text_upload = parse_document(upload_file=pptx_upload)
        print(f"PPTX content length (upload): {len(pptx_text_upload)} chars")

        results["pptx"] = {
            "direct": len(pptx_text_direct),
            "upload": len(pptx_text_upload),
        }

    return results


def test_multiple_files():
    """Test parsing multiple files of different types."""

    project_root = Path(__file__).parents[3]  # Go up to project root
    test_files_dir = (
        project_root / "test_files"
    )  # Create this directory with test files

    # Test file paths - update these to match your actual test files
    pdf_path = test_files_dir / "sample.pdf"
    txt_path = test_files_dir / "sample.txt"
    docx_path = test_files_dir / "sample.docx"
    pptx_path = test_files_dir / "sample.pptx"

    # Create a list of upload files
    upload_files = []

    for path in [pdf_path, txt_path, docx_path, pptx_path]:
        if path.exists():
            upload_files.append(create_upload_file(path))

    if not upload_files:
        print("No test files found. Please add test files to the test_files directory.")
        return None

    print(f"\n--- Testing parsing multiple files ({len(upload_files)} files) ---")

    # This simulates what the AI orchestrator's _run_parsing function does
    combined_texts = []

    for upload_file in upload_files:
        try:
            print(f"Parsing {upload_file.filename}...")
            upload_file.file.seek(0)
            extracted_text = parse_document(upload_file=upload_file)

            if extracted_text:
                # Just take the first 50 chars for display
                print(
                    f"  Extracted {len(extracted_text)} chars: {extracted_text[:50]}..."
                )
                combined_texts.append(extracted_text)
            else:
                print(f"  No text extracted.")

            upload_file.file.seek(0)
        except Exception as e:
            print(f"  Error: {str(e)}")

    combined_content = "\n\n".join(combined_texts)
    print(f"Combined content length: {len(combined_content)} chars")

    return {
        "num_files": len(upload_files),
        "num_successful": len(combined_texts),
        "total_content_length": len(combined_content),
    }


def main():
    """Run all tests."""
    print("====== Document Parser Strategy Pattern Test ======")

    single_results = test_single_file_parsing()
    print(f"\nSingle file parsing results: {single_results}")

    multiple_results = test_multiple_files()
    print(f"\nMultiple file parsing results: {multiple_results}")

    print("\n====== Test Complete ======")


if __name__ == "__main__":
    main()
