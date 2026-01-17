import google.generativeai as genai
import os

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or os.environ.get('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in Railway environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

def generate_response(user_input, language):
    """
    Generate AI response using Google Gemini
    
    Args:
        user_input (str): User's transcribed text
        language (str): Detected language code
        
    Returns:
        str: AI generated response
    """
    try:
        # Initialize Gemini model - using gemini-1.5-flash
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Create language-aware prompt
        language_instruction = f"Please respond in {language} language."
        
        prompt = f"""{language_instruction}

User message: {user_input}

Provide a helpful, natural, and conversational response."""
        
        # Generate response
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        print(f"Error generating response: {e}")
        return f"I'm sorry, I encountered an error processing your request. Error: {str(e)}"