"""
PDF parsing utilities to extract text from PDF files using LangChain.
"""

import io
import tempfile
import os
from fastapi import UploadFile
from pathlib import Path
from typing import List, Dict, Union

from langchain_community.document_loaders import PyMuPDFLoader, PyPDFLoader
from langchain_core.documents import Document


class PDFParser:
    """
    A class for parsing PDF documents and extracting text.
    Can be initialized with a file path, bytes, or FastAPI UploadFile.
    """

    def __init__(
        self,
        file_path: str | Path | None = None,
        file_bytes: bytes | None = None,
        upload_file: UploadFile | None = None,
    ):
        """
        Initialize the PDF parser with either a file path, bytes, or an UploadFile.

        Args:
            file_path: Path to the PDF file
            file_bytes: PDF content as bytes
            upload_file: FastAPI UploadFile containing a PDF
        """
        self.documents = None
        self.temp_path = None

        if upload_file:
            self._load_from_upload_file(upload_file)
        elif file_bytes:
            self._load_from_bytes(file_bytes)
        elif file_path:
            self._load_from_path(file_path)

    def _load_from_path(self, file_path: str | Path):
        """Load PDF from a file path."""
        loader = PyMuPDFLoader(str(file_path))
        self.documents = loader.load()

    def _load_from_bytes(self, file_bytes: bytes):
        """Load PDF from bytes by creating a temporary file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file.write(file_bytes)
            self.temp_path = temp_file.name

        # Load the document
        loader = PyMuPDFLoader(self.temp_path)
        self.documents = loader.load()

    def _load_from_upload_file(self, upload_file: UploadFile):
        """Load PDF from a FastAPI UploadFile."""
        # Read content
        content = upload_file.file.read()

        # Load from bytes
        self._load_from_bytes(content)

        # Reset file pointer for future reads
        upload_file.file.seek(0)

    def get_full_text(self) -> str:
        """
        Get the full text content of the PDF.

        Returns:
            String containing all text from the PDF
        """
        if not self.documents:
            return ""

        return "\n".join([doc.page_content for doc in self.documents])

    def get_text_by_pages(self) -> List[str]:
        """
        Get text content as a list of pages.

        Returns:
            List of strings, one per page
        """
        if not self.documents:
            return []

        # Sort documents by page number
        sorted_docs = sorted(
            self.documents, key=lambda doc: doc.metadata.get("page", 0)
        )
        return [doc.page_content for doc in sorted_docs]

    def get_text_with_metadata(self) -> List[Dict]:
        """
        Get text content with page metadata.

        Returns:
            List of dictionaries containing page content and metadata
        """
        if not self.documents:
            return []

        # Sort documents by page number
        sorted_docs = sorted(
            self.documents, key=lambda doc: doc.metadata.get("page", 0)
        )

        return [
            {
                "page_number": doc.metadata.get("page", i + 1),
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
            for i, doc in enumerate(sorted_docs)
        ]

    def get_documents(self) -> List[Document]:
        """
        Get the raw LangChain Document objects.

        Returns:
            List of LangChain Document objects
        """
        return self.documents or []

    def __del__(self):
        """Clean up temporary files when the object is destroyed."""
        if self.temp_path and os.path.exists(self.temp_path):
            try:
                os.unlink(self.temp_path)
            except:
                pass


# Convenience functions that use the class internally


def extract_text_from_path(pdf_path: str | Path) -> str:
    """Convenience function to extract text from a PDF file path."""
    parser = PDFParser(file_path=pdf_path)
    return parser.get_full_text()


def extract_text_from_bytes(pdf_bytes: bytes) -> str:
    """Convenience function to extract text from PDF bytes."""
    parser = PDFParser(file_bytes=pdf_bytes)
    return parser.get_full_text()


def extract_text_from_upload_file(upload_file: UploadFile) -> str:
    """Convenience function to extract text from a FastAPI UploadFile."""
    parser = PDFParser(upload_file=upload_file)
    return parser.get_full_text()


def extract_text_by_pages(pdf_path: Union[str, Path]) -> List[str]:
    """
    Extract text from a PDF file and return as a list of pages using LangChain.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        List of strings, one per page
    """
    loader = PyMuPDFLoader(str(pdf_path))
    documents = loader.load()

    # Sort documents by page number and extract text
    documents.sort(key=lambda doc: doc.metadata.get("page", 0))
    return [doc.page_content for doc in documents]


def extract_text_with_metadata(pdf_path: Union[str, Path]) -> List[Dict]:
    """
    Extract text from a PDF file and return with page metadata using LangChain.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        List of dictionaries containing page content and metadata
    """
    loader = PyMuPDFLoader(str(pdf_path))
    documents = loader.load()

    # Sort documents by page number
    documents.sort(key=lambda doc: doc.metadata.get("page", 0))

    return [
        {
            "page_number": doc.metadata.get("page", i + 1),
            "content": doc.page_content,
            "metadata": doc.metadata,
        }
        for i, doc in enumerate(documents)
    ]


def get_documents(pdf_path: Union[str, Path]) -> List[Document]:
    """
    Get LangChain Document objects from a PDF.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        List of LangChain Document objects
    """
    loader = PyMuPDFLoader(str(pdf_path))
    return loader.load()
