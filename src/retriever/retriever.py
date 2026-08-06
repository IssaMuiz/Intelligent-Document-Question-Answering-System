class Retriever:
    def __init__(self, embedder, vector_store):
        """
        Initialize the Retriever.

        Args:
            embedder: EmbeddingGenerator instance.
            vector_store: VectorStore instance.
        """
        self.embedder = embedder
        self.vector_store = vector_store

    def embed_query(self, query):
        """
        Convert a user query into an embedding vector.

        Args:
            query (str): User question.

        Returns:
            list: Query embedding vector.
        """

        return self.embedder.embed_text(query)

    def retrieve(self, query, k_top=5):
        """
        Retrieve the most relevant document chunks.

        Args:
            query (str): User question.
            top_k (int): Number of results to retrieve.

        Returns:
            list: Retrieved document chunks.
        """

        query_embedding = self.embed_query(query)

        results = self.vector_store.search(query_embedding=query_embedding, k_top=k_top)

        return results

    def format_context(self, results):
        """
        Format retrieved chunks into a single context string.

        Args:
            results (list): Retrieved document chunks.

        Returns:
            str: Formatted context.
        """

        separator = "\n\n" + ("-" * 60) + "\n\n"

        context_parts = []

        for result in results:
            context_parts.append(f"page: {result['page_number']}\n" f"{result['text']}")

        return separator.join(context_parts)
