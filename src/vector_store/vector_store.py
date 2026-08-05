import numpy as np
import pickle
from pathlib import Path


class VectorStore:
    """Store and search document embeddings."""

    def __init__(self):
        """
        Initialize an empty vector store.
        """

        self.records = []

    def add(self, record):
        """
        Add a single embedding record to the vector store.

        Args:
            record (dict): Embedding record.

        Returns:
            None
        """

        self.records.append(record)

    def add_many(self, records):
        """
        Add multiple embedding records to the vector store.

        Args:
            records (list): List of embedding records.

        Returns:
            None
        """

        for record in records:
            self.add(record)

    def search(self, query_embedding, k_top=5):
        """
        Search for the most similar records.

        Args:
            query_embedding (list): Query embedding vector.
            top_k (int): Number of results to return.

        Returns:
            list: Top matching records.
        """

        results = []

        for record in self.records:

            similarity = self.cosine_similarity(query_embedding, record["embedding"])

            result = record.copy()

            result["similarity"] = float(similarity)

            results.append(result)

        results.sort(key=lambda x: x["similarity"], reverse=True)

        return results[:k_top]

    def save(self, file_path):
        """
        Save the vector store to disk.

        Args:
            file_path (str | Path): Output file path.

        Returns:
            None
        """
        file_path = Path(file_path)

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "wb") as file:
            pickle.dump(self.records, file)

        print(f"vector store save to {file_path}")

    def load(self, file_path):
        """
        Load a vector store from disk.

        Args:
            file_path (str | Path): Path to the saved vector store.

        Returns:
            None
        """

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Vector store file not found {file_path}")

        with open(file_path, "rb") as file:
            self.records = pickle.load(file)

        print(f"Loaded {len(self.records)} records from {file_path}")

    def cosine_similarity(self, vector1, vector2):
        """
        Compute cosine similarity between two vectors.

        Args:
            vector1 (list | np.ndarray): First embedding vector.
            vector2 (list | np.ndarray): Second embedding vector.

        Returns:
            float: Cosine similarity score.
        """

        vector1 = np.array(vector1)
        vector2 = np.array(vector2)

        return np.dot(vector1, vector2)
