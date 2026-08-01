from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """Generate vector embeddings for text chunks."""

    def __init__(self, model_name="BAAI/bge-small-en-v1.5"):
        """
        Initialize the embedding generator.

        Args:
            model_name (str): Hugging Face model identifier.
        """
        self.model_name = model_name
        self.model = self.load_model()

    def load_model(self):
        """
        Load the embedding model.

        Returns:
            SentenceTransformer: Loaded embedding model.
        """

        print(f"Loading embedding model: {self.model_name}")

        model = SentenceTransformer(self.model_name)

        print("Model loaded successfully")

        return model

    def embed(self, chunks):
        """Generate embeddings for all chunks.

        Args:
            chunks (list): list of chunks dictionaries

        Return:
            list: chunks with embeddings attached
        """
        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(
            texts, batch_size=32, show_progress_bar=True, normalize_embeddings=True
        )

        embedded_chunks = []

        for chunk, embedding in zip(chunks, embeddings):
            chunk_with_embedding = self.create_embedding_records(
                chunk, embedding.tolist()
            )

            embedded_chunks.append(chunk_with_embedding)

        return embedded_chunks

    def embed_text(self, text):
        """
        Generate embedding for a single text.

        Args:
            text (str): Input text.

        Returns:
            list: Embedding vector.
        """
        embedding = self.model.encode(text, normalize_embeddings=True)

        return embedding.tolist()

    def create_embedding_records(self, chunk, embedding):
        """
        Combine chunk information with its embedding.

        Args:
            chunk (dict): Chunk metadata and text.
            embedding (list): Vector representation.

        Returns:
            dict: Chunk with embedding attached.
        """

        record = chunk.copy()

        record["embedding"] = embedding

        return record
