from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI  # example
from .config import LLM_PROVIDER, OPENAI_API_KEY, MAX_QUESTIONS, GEMINI_API_KEY
import os
# simple wrapper — swap provider logic here
def get_llm():
    if LLM_PROVIDER == "openai":
        return OpenAI(temperature=0.2, openai_api_key=OPENAI_API_KEY)
    elif LLM_PROVIDER == "gemini":
        # Placeholder: user must configure Gemini adapter in LangChain and auth
        # e.g., from langchain import GoogleGemini as Gemini ... (depends on LangChain version)
        raise NotImplementedError("Gemini provider adapter must be wired by the developer. Use OPENAI for testing.")
    else:
        raise ValueError("Unsupported provider")

# Load prompt templates from files
from pathlib import Path
BASE = Path(__file__).parent / "prompts"
quiz_template = (BASE / "quiz_prompt.txt").read_text()
related_template = (BASE / "related_prompt.txt").read_text()

def generate_quiz(scraped_text, title, max_questions=MAX_QUESTIONS):
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=["title","text","max_q"],
        template=quiz_template
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    out = chain.run({"title": title, "text": scraped_text, "max_q": str(max_questions)})
    # Expect JSON back. Try parse; if not, return raw string for debugging.
    import json
    try:
        result = json.loads(out)
    except Exception:
        # fallback: return raw text as one question list
        result = {"quiz": [], "raw": out}
    return result

def generate_related(scraped_text, title):
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=["title","text"],
        template=related_template
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    out = chain.run({"title": title, "text": scraped_text})
    # expect a JSON list
    import json
    try:
        topics = json.loads(out)
    except:
        topics = []
    return topics
