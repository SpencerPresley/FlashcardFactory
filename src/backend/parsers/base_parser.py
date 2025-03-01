"""Base parser interface and registry for document parsing strategies.
"""

from abc import ABC, abstractmethod
from typing import Dict, Type, List, Optional, Union
from fastapi import UploadFile
from pathlib import Path
import os

# Parser registry

PARSER_REGISTRY: Dict[str, Type["BaseDocumentParser"]] = {}

def parser_for(*extensions: str):
    """Decorator to register parser classes for specific file extensions.
    
    Args:
        *extensions: File extensions this parser supports (e.g., 'pdf', 'docx', 'pptx', etc.)
    """
    def decorator(cls):
        for ext in extensions:
            ext_lower = ext.lower().lstrip('.')
            PARSER_REGISTRY[ext_lower] = cls
        return cls
    return decorator

class BaseDocumentParser(ABC):
    """Base abstract class for all document parsers."""
    
    @abstractmethod
    def parse(self) -> str:
        """Parse the document and return the extracted text."""
        pass
    
    @classmethod
    def from_path(cls, file_path: Union[str, Path]) -> "BaseDocumentParser":
        """Create a parser instance from a file path."""
        pass
    
    @classmethod
    def from_bytes(cls, file_bytes: bytes, file_name: str | None = None) -> "BaseDocumentParser":
        """Create a parser instance from bytes."""
        pass
    
    @classmethod
    def from_upload_file(cls, upload_file: UploadFile) -> "BaseDocumentParser":
        """Create a parser instance from a FastAPI UploadFile."""
        
def get_parser_for_file(file_path: Union[str, Path]) -> Type[BaseDocumentParser]:
    """Get the appropriate parser class for a given file path.
    
    Args:
        file_path: Path to the file
    
    Returns:
        Parser class for the file type
    
    Raises:
        ValueError: If no parser is registered for the file extension
    """
    ext = os.path.splitext(str(file_path))[1].lower().lstrip('.')
    if ext not in PARSER_REGISTRY:
        raise ValueError(f"No parser registered for file extension: .{ext}")
    return PARSER_REGISTRY[ext]

def get_parser_for_upload_file(upload_file: UploadFile) -> Type[BaseDocumentParser]:
    """Get the appropriate parser class for an UploadFile.
    
    Args:
        upload_file: FastAPI UploadFile object
    
    Returns:
        Parser class for the file type
    
    Raises:
        ValueError: If no parser is registered for the file extension
    """
    ext = os.path.splitext(upload_file.filename)[1].lower().lstrip('.')
    if ext not in PARSER_REGISTRY:
        raise ValueError(f"No parser registered for file extension: .{ext}")
    return PARSER_REGISTRY[ext]

def parse_document(
    file_path: Union[str, Path, None] = None, 
    file_bytes: bytes | None = None,
    upload_file: UploadFile | None = None
) -> str:
    """Parse a document using the appropriate parser.
    
    Args:
        file_path: Path to the document file
        file_bytes: Document content as bytes
        upload_file: FastAPI UploadFile containing the document
    
    Returns:
        Extracted text content
    
    Raises:
        ValueError: If no input is provided or no parser is available
    """
    if upload_file:
        parser_cls = get_parser_for_upload_file(upload_file)
        parser = parser_cls.from_upload_file(upload_file)
    elif file_path:
        parser_cls = get_parser_for_file(file_path)
        parser = parser_cls.from_path(file_path)
    elif file_bytes and upload_file and upload_file.filename:
        # Use filename from upload_file to determine extension
        parser_cls = get_parser_for_upload_file(upload_file)
        parser = parser_cls.from_bytes(file_bytes, upload_file.filename)
    else:
        raise ValueError("Must provide file_path, file_bytes, or upload_file")
    
    return parser.parse()