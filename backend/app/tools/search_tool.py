from retrieval.retriever import Retriever

class SearchTool:
    def __init__(self):
        # Initialize the retriever we built in Week 3
        self.retriever = Retriever()

    def search(self, query: str):
        """
        Searches the vector database for relevant context.
        """
        results = self.retriever.retrieve(query, k=4)
        
        if not results:
            return "No relevant information found in the documents."
        
        # Format results for the LLM
        context = ""
        for idx, res in enumerate(results):
            context += f"[Result {idx+1}] (Section: {res['metadata']['section']})\n"
            context += f"{res['text']}\n\n"
            
        return context