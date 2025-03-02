from .base_parser import (
    parse_document,
    get_parser_for_file,
    get_parser_for_upload_file,
    BaseDocumentParser,
)
from .pdf_parser import PDFParser
from .docx_parser import DOCXParser
from .txt_parser import TXTParser
from .pptx_parser import PPTXParser

__all__ = [
    "parse_document",
    "get_parser_for_file",
    "get_parser_for_upload_file",
    "BaseDocumentParser",
    "PDFParser",
    "DOCXParser",
    "TXTParser",
    "PPTXParser",
]
