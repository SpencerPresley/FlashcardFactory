"""
TXT parsing strategy implementation using the strategy pattern.
"""

import io
import tempfile
import os
from fastapi import UploadFile
from pathlib import Path
from typing import Optional, Union, List, Dict
from langchain_core.documents import Document

from .base_parser import BaseDocumentParser, parser_for


@parser_for("txt")
class TXTParser(BaseDocumentParser):
    """
    Parser strategy for plain text documents.
    """

    def __init__(self):
        """Initialize the TXT parser."""
        self.content = None
        self.temp_path = None

    @classmethod
    def from_path(cls, file_path: Union[str, Path]) -> "TXTParser":
        """Create a TXTParser instance from a file path."""
        parser = cls()
        parser._load_from_path(file_path)
        return parser

    @classmethod
    def from_bytes(
        cls, file_bytes: bytes, file_name: Optional[str] = None
    ) -> "TXTParser":
        """Create a TXTParser instance from bytes."""
        parser = cls()
        parser._load_from_bytes(file_bytes)
        return parser

    @classmethod
    def from_upload_file(cls, upload_file: UploadFile) -> "TXTParser":
        """Create a TXTParser instance from an UploadFile."""
        parser = cls()
        parser._load_from_upload_file(upload_file)
        return parser

    def _load_from_path(self, file_path: Union[str, Path]):
        """Load text from a file path."""
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            self.content = f.read()

    def _load_from_bytes(self, file_bytes: bytes):
        """Load text from bytes."""
        self.content = file_bytes.decode("utf-8", errors="replace")

    def _load_from_upload_file(self, upload_file: UploadFile):
        """Load text from a FastAPI UploadFile."""
        # Read content
        content = upload_file.file.read()

        # Decode bytes to string
        self.content = content.decode("utf-8", errors="replace")

        # Reset file pointer for future reads
        upload_file.file.seek(0)

    def parse(self) -> str:
        """
        Parse the text document and return the content.

        Returns:
            Full text content
        """
        return self.content if self.content else ""

    def get_documents(self) -> List[Document]:
        """
        Get the content as a LangChain Document object.

        Returns:
            List containing a single Document
        """
        if not self.content:
            return []

        return [Document(page_content=self.content, metadata={"source": "text"})]
