"""DOCX parsing strategy implementation using the strategy pattern.
"""

import io
import tempfile
import os
from fastapi import UploadFile
from pathlib import Path
from typing import Optional, Union

from langchain_community.document_loaders import Docx2txtLoader

from .base_parser import BaseDocumentParser, parser_for

@parser_for('docx')
class DOCXParser(BaseDocumentParser):
    """
    Parser strategy for DOCX documents.
    """

    def __init__(self):
        """Initialize the DOCX parser."""
        self.documents = None
        self.temp_path = None
        self._loader = None

    @classmethod
    def from_path(cls, file_path: Union[str, Path]) -> "DOCXParser":
        """Create a DOCXParser instance from a file path."""
        parser = cls()
        parser._load_from_path(file_path)
        return parser
        
    @classmethod
    def from_bytes(cls, file_bytes: bytes, file_name: Optional[str] = None) -> "DOCXParser":
        """Create a DOCXParser instance from bytes."""
        parser = cls()
        parser._load_from_bytes(file_bytes)
        return parser
        
    @classmethod
    def from_upload_file(cls, upload_file: UploadFile) -> "DOCXParser":
        """Create a DOCXParser instance from an UploadFile."""
        parser = cls()
        parser._load_from_upload_file(upload_file)
        return parser

    def _load_from_path(self, file_path: Union[str, Path]):
        """Load DOCX from a file path."""
        self._loader = Docx2txtLoader(file_path)
        self.documents = self._loader.load()

    def _load_from_bytes(self, file_bytes: bytes):
        """Load DOCX from bytes by creating a temporary file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_file:
            temp_file.write(file_bytes)
            self.temp_path = temp_file.name

        # Load the document
        self._loader = Docx2txtLoader(self.temp_path)
        self.documents = self._loader.load()

    def _load_from_upload_file(self, upload_file: UploadFile):
        """Load DOCX from a FastAPI UploadFile."""
        # Read content
        content = upload_file.file.read()

        # Load from bytes
        self._load_from_bytes(content)

        # Reset file pointer for future reads
        upload_file.file.seek(0)

    def parse(self) -> str:
        """
        Parse the DOCX document and return the extracted text.
        
        Returns:
            Full text content of the DOCX
        """
        if not self.documents:
            return ""

        return "\n".join([doc.page_content for doc in self.documents])

    def __del__(self):
        """Clean up temporary files when the object is destroyed."""
        if self.temp_path and os.path.exists(self.temp_path):
            try:
                os.unlink(self.temp_path)
            except:
                pass