"""
PDF parsing strategy implementation using the strategy pattern.
"""

import io
import tempfile
import os
from fastapi import UploadFile
from pathlib import Path
from typing import List, Dict, Optional, Union

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document

from .base_parser import BaseDocumentParser, parser_for

@parser_for('pdf')
class PDFParser(BaseDocumentParser):
    """Parser strategy for PDF documents.
    """

    def __init__(self):
        """Initialize the PDF parser."""
        self.documents = None
        self.temp_path = None
        self._loader = None

    @classmethod
    def from_path(cls, file_path: Union[str, Path]) -> "PDFParser":
        """Create a PDFParser instance from a file path."""
        parser = cls()
        parser._load_from_path(file_path)
        return parser
        
    @classmethod
    def from_bytes(cls, file_bytes: bytes, file_name: Optional[str] = None) -> "PDFParser":
        """Create a PDFParser instance from bytes."""
        parser = cls()
        parser._load_from_bytes(file_bytes)
        return parser
        
    @classmethod
    def from_upload_file(cls, upload_file: UploadFile) -> "PDFParser":
        """Create a PDFParser instance from an UploadFile."""
        parser = cls()
        parser._load_from_upload_file(upload_file)
        return parser

    def _load_from_path(self, file_path: Union[str, Path]):
        """Load PDF from a file path."""
        self._loader = PyMuPDFLoader(str(file_path))
        self.documents = self._loader.load()

    def _load_from_bytes(self, file_bytes: bytes):
        """Load PDF from bytes by creating a temporary file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file.write(file_bytes)
            self.temp_path = temp_file.name

        # Load the document
        self._loader = PyMuPDFLoader(self.temp_path)
        self.documents = self._loader.load()

    def _load_from_upload_file(self, upload_file: UploadFile):
        """Load PDF from a FastAPI UploadFile."""
        # Read content
        content = upload_file.file.read()

        # Load from bytes
        self._load_from_bytes(content)

        # Reset file pointer for future reads
        upload_file.file.seek(0)

    def parse(self) -> str:
        """Parse the PDF document and return the extracted text.
        
        Returns:
            Full text content of the PDF
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