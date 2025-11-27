import google.generativeai as genai
import os

try:
    # Key is in env var now thanks to docker-compose
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not set in environment")
        exit(1)
        
    genai.configure(api_key=api_key)
    
    print(f"Checking models for key: {api_key[:5]}...")
    
    models = list(genai.list_models())
    print(f"Found {len(models)} models.")
    
    for m in models:
        print(f"- {m.name} (methods: {m.supported_generation_methods})")
        
except Exception as e:
    print(f"Error: {e}")
