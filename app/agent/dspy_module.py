import dspy
from pydantic import BaseModel, Field
from typing import List

class Citation(BaseModel):
    ref_id: int = Field(description="Reference number starting from 1")
    file_name: str = Field(description="The exact filename of the document used as a reference")
    page: str = Field(description="The exact page number where the information was found")
    quote: str = Field(description="A short, exact verbatim quote from the text that proves your answer.")

class SummaryWithCitations(BaseModel):
    summary: str = Field(description="A clear, professional summary answering the user's question in Thai. ALWAYS append reference numbers like [1], [2] at the end of sentences that use factual information.")
    references: List[Citation] = Field(description="List of all citations used. You MUST populate this list if you used the search_documents tool to answer.")

class RAGAnswerSignature(dspy.Signature):
    """You are a strict and professional AI assistant. 
    1. You MUST ALWAYS use the `search_documents` tool to find factual information before answering.
    2. Do NOT answer using your internal pre-trained knowledge. Only answer based on the search results.
    3. If you use information from the search results, you MUST populate the `references` list with the exact file_name, page, and a direct quote.
    4. Only return an empty reference list if the user is just saying a general greeting (e.g., 'Hello', 'Hi')."""
    
    question: str = dspy.InputField()
    output: SummaryWithCitations = dspy.OutputField()

class KnowledgeAgent(dspy.Module):
    def __init__(self, retriever):
        super().__init__()
        self.retriever = retriever
        def search_documents(query: str) -> str:
            retrieved_nodes = self.retriever.retrieve(query)
            formatted_context = ""
            for node in retrieved_nodes:
                file_name = node.metadata.get('filename', node.metadata.get('original_filename', 'Unknown_File'))
                page = node.metadata.get('page_number', 'N/A')
                text = node.get_content().strip()
                formatted_context += f"--- File: {file_name} | Page: {page} ---\n{text}\n\n"
            
            if not formatted_context.strip():
                return "No relevant documents found in the system."
            return formatted_context

        self.agent = dspy.ReAct(RAGAnswerSignature, tools=[search_documents], max_iters=3)

    def forward(self, question: str) -> SummaryWithCitations:
        result = self.agent(question=question)
        return result.output