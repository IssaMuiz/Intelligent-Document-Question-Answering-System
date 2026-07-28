import fitz
from pathlib import Path


class PDFParser:
    """A parser for extracting text and metadata from pdf document"""

    def __init__(self):
        pass

    def parse(self, file_path):
        """Parse an entire document
        Args:
            file_path (str | Path): Path to the PDF file.

        Returns:
            dict: Structured document information.
        """

        file_path = Path(file_path)

        document = fitz.open(file_path)

        parsed_document = {
            "filename": file_path.name,
            "filepath": str(file_path),
            "page_count": len(document),
            "metadata": self.extract_metadata(document),
            "pages": self.extract_pages(document),
        }

        return parsed_document

    def extract_metadata(self, document):
        """
        Extract metadata from a PDF document.

        Args:
            document (fitz.Document): Open PDF document.

        Returns:
            dict: Cleaned metadata.
        """

        metadata = document.metadata

        return {
            "title": metadata.get("title"),
            "author": metadata.get("author"),
            "subject": metadata.get("subject"),
            "keywords": metadata.get("keywords"),
            "creator": metadata.get("creator"),
            "producer": metadata.get("producer"),
            "creation_date": metadata.get("creationDate"),
            "modified_date": metadata.get("modDate"),
            "pdf_format": metadata.get("format"),
        }

    def extract_pages(self, document):
        """
        Extract information from every page in a PDF.

        Args:
            document (fitz.Document): Open PDF document.

        Returns:
            list: List of page dictionaries.
        """

        pages = []

        for page_number, page in enumerate(document, start=1):
            text = self.extract_text(page)

            page_info = {
                "page_number": page_number,
                "text": text,
                "word_count": len(text.split()),
                "character_count": len(text),
                "has_text": bool(text.strip()),
            }

            pages.append(page_info)

        return pages

    def extract_text(self, page):
        """
        Extract text from a single PDF page.

        Args:
            page (fitz.Page): PDF page.

        Returns:
            str: Extracted page text.
        """

        return page.get_text("text")
