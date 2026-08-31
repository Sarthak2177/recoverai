"""
RecoverAI — LLM Abstraction Layer (Gemini Only)
"""
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ GEMINI_API_KEY not found. Agent will use rule-based fallbacks.")
        return None
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.2,
            request_timeout=10,
        )
    except Exception as e:
        print(f"⚠️ Error initializing LLM: {e}. Agent will use rule-based fallbacks.")
        return None
