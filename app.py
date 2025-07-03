from flask import Flask, request, Response, jsonify
from bark import SAMPLE_RATE, generate_audio, preload_models
import numpy as np
import io
import scipy.io.wavfile as wavfile
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Global variables for models
models_loaded = False

def load_models():
    """Load Bark models on startup"""
    global models_loaded
    if not models_loaded:
        logging.info("Loading Bark models...")
        try:
            preload_models()
            models_loaded = True
            logging.info("Bark models loaded successfully!")
        except Exception as e:
            logging.error(f"Failed to load models: {e}")
            raise e

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "models_loaded": models_loaded})

@app.route('/generate', methods=['POST'])
def generate_speech():
    """Generate speech from text using Bark"""
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field in request"}), 400
        
        text = data['text']
        voice_preset = data.get('voice', 'v2/en_speaker_6')  # Default to a nice female voice
        
        if len(text.strip()) == 0:
            return jsonify({"error": "Text cannot be empty"}), 400
        
        if len(text) > 500:
            return jsonify({"error": "Text too long (max 500 characters)"}), 400
        
        logging.info(f"Generating audio for text: {text[:50]}...")
        
        # Generate audio
        audio_array = generate_audio(text, history_prompt=voice_preset)
        
        # Convert to wav format
        buffer = io.BytesIO()
        wavfile.write(buffer, SAMPLE_RATE, audio_array)
        buffer.seek(0)
        
        logging.info("Audio generation completed")
        
        return Response(
            buffer.getvalue(),
            mimetype='audio/wav',
            headers={
                'Content-Disposition': 'attachment; filename=speech.wav',
                'Content-Type': 'audio/wav'
            }
        )
        
    except Exception as e:
        logging.error(f"Error generating speech: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/voices', methods=['GET'])
def list_voices():
    """List available voice presets"""
    voices = [
        "v2/en_speaker_0", "v2/en_speaker_1", "v2/en_speaker_2", 
        "v2/en_speaker_3", "v2/en_speaker_4", "v2/en_speaker_5",
        "v2/en_speaker_6", "v2/en_speaker_7", "v2/en_speaker_8", "v2/en_speaker_9"
    ]
    return jsonify({"voices": voices})

@app.before_first_request
def startup():
    """Load models when the app starts"""
    load_models()

if __name__ == '__main__':
    # Load models on startup
    load_models()
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 