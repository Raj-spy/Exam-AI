import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from src.llm.groq_client import get_groq_llm
    print("Successfully imported get_groq_llm")
    
    llm = get_groq_llm()
    print("Successfully created Groq LLM instance")
    
    # Check if key is set (ChatGroq stores it in groq_api_key which might be a SecretStr)
    if hasattr(llm, 'groq_api_key'):
        key = llm.groq_api_key
        # accessing SecretStr value requires .get_secret_value() usually, or just checking if it is not None
        if key:
             print("API Key appears to be set")
        else:
             print("API Key is None or empty")
    
except Exception as e:
    print(f"Error occurred: {e}")
