import os
import difflib
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Load environment variables once at the module level
load_dotenv()

class TextRewriter:
    """Handles LLM connections and text transformation logic."""
    
    def __init__(self):
        # Initialize the LLM once so it doesn't reconnect on every button click
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.4,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.prompt = PromptTemplate(
            input_variables=["text", "tone", "length", "audience", "style"],
            template="""
            You are an expert copywriter. Rewrite the following text strictly adhering to these parameters:
            - Tone: {tone}
            - Length: Make it {length} than the original
            - Target Audience: {audience}
            - Language Style: {style}
            
            CRITICAL RULES:
            1. Preserve the original core meaning and facts.
            2. Output ONLY the rewritten text. Do not include introductory phrases.
            
            Original Text:
            {text}
            """
        )
        self.chain = self.prompt | self.llm

    def compute_diff(self, original: str, rewritten: str) -> list[tuple[str, str]]:
        """Calculates word-by-word differences for UI highlighting."""
        matcher = difflib.SequenceMatcher(None, original.split(), rewritten.split())
        diff_output = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                diff_output.append((" ".join(original.split()[i1:i2]) + " ", None))
            elif tag == 'replace':
                diff_output.append((" ".join(original.split()[i1:i2]) + " ", "-"))
                diff_output.append((" ".join(rewritten.split()[j1:j2]) + " ", "+"))
            elif tag == 'delete':
                diff_output.append((" ".join(original.split()[i1:i2]) + " ", "-"))
            elif tag == 'insert':
                diff_output.append((" ".join(rewritten.split()[j1:j2]) + " ", "+"))
                
        return diff_output

    def process_text(self, text: str, tone: str, length: str, audience: str, style: str) -> tuple[str, list]:
        """Main execution function to be called by the UI."""
        if not text.strip():
            return "Error: Please provide source text.", []
            
        try:
            response = self.chain.invoke({
                "text": text,
                "tone": tone,
                "length": length,
                "audience": audience,
                "style": style
            })
            rewritten_text = response.content.strip()
            diffs = self.compute_diff(text, rewritten_text)
            return rewritten_text, diffs
            
        except Exception as e:
            return f"An error occurred during generation: {str(e)}", []
