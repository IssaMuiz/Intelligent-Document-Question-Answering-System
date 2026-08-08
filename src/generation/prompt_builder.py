class PromptBuilder:
    """
    Builds prompts for the language model.
    """

    def __init__(self):
        """
        Initialize the Prompt Builder.
        """
        pass

    def build_prompt(self, question, context):
        """
        Build a prompt for the language model.

        Args:
            question (str): User question.
            context (str): Retrieved document context.

        Returns:
            str: Complete prompt.
        """

        prompt = f"""
            You are a helpful AI assistant.

            Answer the user's question using ONLY the information provided in
            the context.

            If the answer cannot be found in the context, say:

            "I couldn't find the answer in the provided documents."

            Do not make up information.

            Context:
            {context}
            Qusestion:
            {question}

            Answer:
            """

        return prompt.strip()
