from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.speech_to_text import transcribe_audio
from modules.language_detector import detect_language
from modules.llm_handler import generate_response
from modules.text_to_speech import text_to_speech

app = Flask(__name__)

# Enable CORS for all domains (GitHub Pages)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Multilingual Voice AI API is running',
        'version': '1.0',
        'endpoints': {
            'health': '/ (GET)',
            'process_voice': '/api/process-voice (POST)',
            'get_audio': '/api/get-audio (GET)'
        }
    }), 200

@app.route('/api/process-voice', methods=['POST', 'OPTIONS'])
def process_voice():
    """Process voice input and return transcription, language, and AI response"""
    
    # Handle preflight request
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        # Save uploaded audio temporarily
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audio.webm')
        audio_file.save(audio_path)
        
        # Step 1: Transcribe audio to text
        transcribed_text = transcribe_audio(audio_path)
        if not transcribed_text:
            return jsonify({'error': 'Failed to transcribe audio'}), 500
        
        # Step 2: Detect language
        detected_language = detect_language(transcribed_text)
        
        # Step 3: Generate response using Gemini
        ai_response = generate_response(transcribed_text, detected_language)
        
        # Step 4: Convert response to speech
        output_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'response_audio.mp3')
        text_to_speech(ai_response, detected_language, output_audio_path)
        
        # Clean up input audio
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        # Get the base URL for audio
        base_url = request.host_url.rstrip('/')
        
        return jsonify({
            'success': True,
            'transcribed_text': transcribed_text,
            'detected_language': detected_language,
            'ai_response': ai_response,
            'audio_url': f'{base_url}/api/get-audio'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-audio', methods=['GET'])
def get_audio():
    """Serve the generated audio file"""
    try:
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'response_audio.mp3')
        if os.path.exists(audio_path):
            return send_file(audio_path, mimetype='audio/mpeg')
        else:
            return jsonify({'error': 'Audio file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
