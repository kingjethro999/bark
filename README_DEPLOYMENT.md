# Bark TTS Service Deployment

## Deploy to Render

1. **Push to GitHub**: First, push this bark directory to a GitHub repository.

2. **Create Render Service**:
   - Go to [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the bark directory (or use root directory if this is the main repo)

3. **Configuration**:
   - **Name**: bark-tts-service
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Choose based on your needs (Starter plan works for testing)

4. **Environment Variables**:
   - `PORT`: 10000 (automatically set by Render)
   - `PYTHON_VERSION`: 3.9.18

## API Endpoints

Once deployed, your service will have these endpoints:

- `GET /health` - Health check
- `POST /generate` - Generate speech from text
- `GET /voices` - List available voices

### Example Usage

```bash
# Health check
curl https://your-service-url.onrender.com/health

# Generate speech
curl -X POST https://your-service-url.onrender.com/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, I am Buddy!", "voice": "v2/en_speaker_6"}' \
  --output speech.wav
```

## Testing Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
python app.py

# Test locally
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world!", "voice": "v2/en_speaker_6"}' \
  --output test.wav
```

## Voice Options

Available voices:
- `v2/en_speaker_0` through `v2/en_speaker_9`
- Default: `v2/en_speaker_6` (recommended female voice)

## Notes

- First request will be slow as models load
- Subsequent requests will be faster
- Max text length: 500 characters
- Returns WAV audio format 