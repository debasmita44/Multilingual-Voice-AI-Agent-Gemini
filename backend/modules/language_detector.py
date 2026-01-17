from langdetect import detect, LangDetectException

def detect_language(text):
    """
    Detect the language of input text
    
    Args:
        text (str): Input text to detect language
        
    Returns:
        str: Detected language name
    """
    try:
        # Detect language code
        lang_code = detect(text)
        
        # Map language codes to full names
        language_names = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'nl': 'Dutch',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh-cn': 'Chinese',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'tr': 'Turkish',
            'pl': 'Polish',
            'sv': 'Swedish',
            'da': 'Danish',
            'no': 'Norwegian',
            'fi': 'Finnish'
        }
        
        return language_names.get(lang_code, 'English')
        
    except LangDetectException:
        return 'English'  # Default to English if detection fails
    except Exception as e:
        print(f"Error detecting language: {e}")
        return 'English'