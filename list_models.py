import os
import google.generativeai as genai

try:
    api_key = open("gemini_apikey.txt", "r").read().strip()
    genai.configure(api_key=api_key)
    
    print("Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error: {e}")
