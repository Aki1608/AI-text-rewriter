from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
import difflib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.4, # Low temperature keeps the rewrite focused on the original text
    api_key=os.getenv("GROQ_API_KEY")
)

# Define the prompt template that strictly constraints the LLM
rewrite_prompt = PromptTemplate(
    input_variables=["text", "tone", "length", "audience", "style"],
    template="""
    You are an expert copywriter. Rewrite the following text strictly adhering to these parameters:
    
    - Tone: {tone}
    - Length: Make it {length} than the original
    - Target Audience: {audience}
    - Language Style: {style}
    
    CRITICAL RULES:
    1. Preserve the original core meaning and facts.
    2. Output ONLY the rewritten text. Do not include introductory phrases, explanations, or quotes.
    
    Original Text:
    {text}
    """
)

def compute_diff(original, rewritten):
    """
    Compares two strings word-by-word and formats the output for Gradio's HighlightedText component.
    """
    matcher = difflib.SequenceMatcher(None, original.split(), rewritten.split())
    diff_output = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            diff_output.append((" ".join(original.split()[i1:i2]) + " ", None))
        elif tag == 'replace':
            diff_output.append((" ".join(original.split()[i1:i2]) + " ", "-")) # Removed
            diff_output.append((" ".join(rewritten.split()[j1:j2]) + " ", "+")) # Added
        elif tag == 'delete':
            diff_output.append((" ".join(original.split()[i1:i2]) + " ", "-"))
        elif tag == 'insert':
            diff_output.append((" ".join(rewritten.split()[j1:j2]) + " ", "+"))
            
    return diff_output

def rewrite_text(text, tone, length, audience, style):
    if not text.strip():
        return "Please enter text to rewrite.", []
        
    # Construct the chain and execute
    chain = rewrite_prompt | llm
    response = chain.invoke({
        "text": text,
        "tone": tone,
        "length": length,
        "audience": audience,
        "style": style
    })
    
    rewritten_text = response.content.strip()
    
    # Calculate the visual differences
    diff_highlights = compute_diff(text, rewritten_text)
    
    return rewritten_text, diff_highlights