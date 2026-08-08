class RAGPipeline:
    """
    Generate a response from the language model.

    Args:
        prompt (str): Complete prompt sent to the LLM.

    Returns:
        str: Generated response.
    """

    def __init__(self, retriever, prompt_builder, generator):
        """
        Initialize the RAG pipeline.

        Args:
            retriever: Retriever instance.
            prompt_builder: PromptBuilder instance.
            generator: Generator instance.
        """

        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.generator = generator

    def ask(self, question, k_top=5):
        """
        Answer a user question using retrieved document context.

        Args:
            question (str): User question.
            top_k (int): Number of chunks to retrieve.

        Returns:
            str: Generated answer.
        """
        results = self.retriever.retrieve(question, k_top=k_top)

        context = self.retriever.format_context(results)

        prompt = self.prompt_builder.build_prompt(question=question, context=context)

        answer = self.generator.generate(prompt)

        return answer
