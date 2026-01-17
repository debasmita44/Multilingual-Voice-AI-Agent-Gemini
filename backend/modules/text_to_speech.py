from gtts import gTTS
import os

def text_to_speech(text, language, output_path):
    """
    Convert text to speech and save as audio file
    
    Args:
        text (str): Text to convert
        language (str): Language code for TTS
        output_path (str): Path to save audio file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Map common language names to gTTS language codes
        language_map = {
            'english': 'en',
            'spanish': 'es',
            'french': 'fr',
            'german': 'de',
            'italian': 'it',
            'portuguese': 'pt',
            'dutch': 'nl',
            'russian': 'ru',
            'japanese': 'ja',
            'korean': 'ko',
            'chinese': 'zh-CN',
            'arabic': 'ar',
            'hindi': 'hi',
            'turkish': 'tr',
            'polish': 'pl',
            'swedish': 'sv',
            'danish': 'da',
            'norwegian': 'no',
            'finnish': 'fi'
        }
        
        # Get language code
        lang_code = language_map.get(language.lower(), 'en')
        
        # Generate speech
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(output_path)
        
        return True
        
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        # Fallback to English if language not supported
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)
            return True
        except:
            return False