class TextChunker:
    """
    Split cleaned documents into retrieval-ready chunks.
    """

    def __init__(self, chunk_size=300, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, document):
        """
        Chunk an entire cleaned document.

        Args:
            document (dict): Cleaned document.

        Returns:
            list: List of chunk dictionaries.
        """

        chunk = []

        for page in document["pages"]:
            page_chunk = self.chunk_page(page)

            chunk.extend(page_chunk)

        return chunk

    def chunk_page(self, page):
        """
        Split one page into overlapping chunks.

        Args:
            page (dict): Cleaned page.

        Returns:
            list: Chunk dictionaries.
        """

        chunks = []
        words = page["text"].split()

        step = self.chunk_size - self.chunk_overlap

        for start in range(0, len(words), step):

            chunk_words = words[start : start + self.chunk_size]
            if not chunk_words:
                continue

            chunk_text = " ".join(chunk_words)

            chunk = self.create_chunk(
                page=page, chunk_text=chunk_text, chunk_index=len(chunks)
            )

            chunks.append(chunk)
        return chunks

    def create_chunk(self, page, chunk_text, chunk_index):
        """
        Create a chunk dictionary.

        Args:
            page (dict): Source page.
            chunk_text (str): Chunk text.
            chunk_index (int): Position of the chunk within the page.

        Returns:
            dict: Chunk dictionary.
        """

        return {
            "chunk_id": f"page_{page['page_number']}_chunk_{chunk_index}",
            "chunk_index": chunk_index,
            "page_number": page["page_number"],
            "text": chunk_text,
            "word_count": len(chunk_text.split()),
        }
