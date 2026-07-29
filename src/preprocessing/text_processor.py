import re


class TextProcessor:
    """Clean and normalize parsed document"""

    def __init__(self):
        pass

    def process(self, document):
        """Process an entire parsed document.

            Args:
            document (dict): Parsed document.

        Returns:
            dict: Cleaned document.

        """

        pages = self.remove_empty_pages(document["pages"])

        cleaned_pages = [self.clean_page(page) for page in pages]

        cleaned_document = {
            **document,
            "pages": cleaned_pages,
            "page_count": len(cleaned_pages),
        }

        return cleaned_document

    def remove_empty_pages(self, pages):
        """Remove pages without text.

            Args:
            pages (list): List of page dictionaries.

        Returns:
            list: Pages containing text.

        """

        return [page for page in pages if page["has_text"]]

    def normalize_whitespace(self, text):
        """Normalize whitespace in text.

            Args:
            text (str): Raw text.

        Returns:
            str: Normalized text.
        """

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def clean_page(self, page):
        """Clean a single page.

            Args:
            page (dict): Page dictionary.

        Returns:
            dict: Cleaned page dictionary.
        """
        cleaned_text = self.normalize_whitespace(page["text"])

        cleaned_page = {
            **page,
            "text": cleaned_text,
            "word_count": len(cleaned_text.strip()),
            "character_count": len(cleaned_text),
            "has_text": bool(cleaned_text),
        }

        return cleaned_page
