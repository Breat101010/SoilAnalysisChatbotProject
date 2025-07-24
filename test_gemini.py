import os
import google.generativeai as genai

# Configure the API key from environment variables
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please set it using: 'set GOOGLE_API_KEY=YOUR_KEY' (Windows)")
    exit()

genai.configure(api_key=api_key)

def test_gemini_connection():
    try:
        # Use the model: 'models/gemini-2.5-flash-lite'
        model = genai.GenerativeModel('models/gemini-2.5-flash-lite')
        response = model.generate_content("Hello, introduce yourself briefly and mention you are an AI assistant.")
        print("\nGemini's response:")
        print(response.text)
        print("\nGemini connection successful!")
    except Exception as e:
        print(f"\nError connecting to Gemini API: {e}")
        print("Please check your internet connection and API key.")

if __name__ == "__main__":
    test_gemini_connection()