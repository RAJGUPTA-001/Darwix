from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import (
    getemotion,
    generate_ssml_direct,
    synthesize_basic,
    synthesize_top,
    generate_ssml_direct,
    generateaudio_gtts_emotion,
    synthesize_basic_ssml
)

app = FastAPI(
    title="Enhanced Emotion-Aware TTS API",
    description="FastAPI endpoints for emotion-aware TTS with SSML and gTTS",
    version="1.0.0"
)

class TextRequest(BaseModel):
    text: str

class EmotionResponse(BaseModel):
    emotion: str
    confidence: float

class SSMLRequest(BaseModel):
    text: str

class TTSRequest(BaseModel):
    text: str
    method: str  # one of: basic, premium, ssml, gtts

@app.post("/api/emotion", response_model=EmotionResponse)
def analyze_emotion(req: TextRequest):
    """Analyze and return dominant emotion"""
    emotions = getemotion(req.text)
    if not emotions:
        return {"emotion": "neutral", "confidence": 0.0}
    dominant = sorted(emotions, key=lambda x: x['score'], reverse=True)[0]
    return {"emotion": dominant['label'], "confidence": dominant['score']}

@app.post("/api/ssml", response_model=dict)
async def generate_ssml(req: SSMLRequest):
    """Generate SSML markup for the input text"""
    emotions = getemotion(req.text)
    ssml = generate_ssml_direct(req.text, emotions)
    return {"ssml": ssml}

@app.post("/api/synthesize")
async def synthesize(req: TTSRequest):
    """Synthesize audio via specified method"""
    text = req.text
    method = req.method.lower()
    try:
        if method == "basic":
            synthesize_basic(text)
            filename = "output_basic.mp3"
        elif method == "premium":
            synthesize_top(text)
            filename = "output_top.mp3"
        elif method == "ssml":
            emotions = getemotion(text)
            ssml = generate_ssml_direct(text, emotions)
            synthesize_basic_ssml(ssml)
            filename = "output_basic_ssml.mp3"
        elif method == "gtts":
            generateaudio_gtts_emotion(text)
            filename = "output_gtts_emotion.mp3"
        else:
            raise HTTPException(status_code=400, detail="Invalid method")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"audio_file": filename}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}