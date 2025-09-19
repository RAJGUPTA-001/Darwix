🎭 Enhanced Emotion-Aware Text-to-Speech System
An advanced AI-powered text-to-speech application that generates emotionally expressive audio by analyzing text sentiment and creating dynamic SSML markup without requiring LLM dependencies for SSML generation, plus emotion-aware gTTS with audio effects.

🆕 What's New in This Version
🚀 Major Enhancements
🤖 LLM-Free SSML Generation: Direct rule-based SSML generation without requiring Gemini API calls

🎵 Emotion-Aware gTTS: Free alternative using Google Text-to-Speech with emotion-based audio effects

🔊 Audio Post-Processing: Real-time speed, pitch, and volume adjustments using PyDub

🌍 Multi-Accent Support: Different English accents for different emotions

⚡ Improved Performance: Faster processing without API dependencies for SSML

🎯 Enhanced Emotion Mapping
11 Emotions Supported: Joy, Love, Happiness, Excitement, Sadness, Fear, Anger, Disgust, Surprise, Optimism, Neutral

Intensity-Based Scaling: Voice parameters adjust based on emotion confidence scores

Smart Text Processing: Automatic emphasis detection and strategic break placement

🌟 Features
🧠 Emotion Detection: Uses Hugging Face's boltuix/bert-emotion model to classify text into 13+ emotional categories

🎪 Direct SSML Generation: Rule-based SSML creation without LLM dependencies (replaces Gemini API requirement)

🎤 Premium Voice Synthesis: Google Cloud Text-to-Speech with multiple voice options including premium neural voices

🎵 Free Alternative: Emotion-aware gTTS with audio effects for cost-effective synthesis

📊 Multiple Output Formats: Basic text, SSML-enhanced, premium voice, and gTTS with effects

⚖️ Intensity-Based Modulation: Adjusts speech parameters based on emotion confidence scores

🚀 Quick Start
Prerequisites
Python 3.13.5

Google Cloud Project with Text-to-Speech API enabled (optional for gTTS mode)

Hugging Face account and API token

Google Gemini API access (No longer required!)

Installation
Clone the repository:

bash
git clone https://github.com/RAJGUPTA-001/Darwix
cd Darwix



pip install -r requirements_enhanced.txt
Set up authentication:

Google Cloud: Configure Application Default Credentials (ADC) - Optional for gTTS mode

Hugging Face: Set your API token

Create a .env file:

text
HUGGINGFACE_KEY=your_hf_token_here
# Optional (only needed for Google Cloud TTS):
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
🔧 Configuration
Enhanced Dependencies
The new version requires additional packages for audio processing:



Install Google Cloud CLI:

bash
# Windows PowerShell
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
Configure authentication:

bash
gcloud auth application-default login
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
💻 Usage
New Enhanced Usage
Run the interactive CLI:

bash
python main_enhanced.py
Menu Options:

Basic Google Cloud TTS

Premium Google Cloud TTS (Chirp3-HD)

🆕 SSML-Enhanced TTS (Direct Generation - No LLM)

🆕 Emotion-Aware gTTS with Audio Effects

Generate All Methods

Test SSML Generation

Show Emotion Analysis

Programmatic Usage
1. LLM-Free SSML Generation
python
from utils_enhanced import generateaudio_basic_ssml

# Direct SSML generation without LLM
generateaudio_basic_ssml("I am absolutely thrilled about this amazing opportunity!")
# Creates: output_basic_ssml.mp3 with emotion-aware SSML
2. Emotion-Aware gTTS (Free Alternative)
python
from utils_enhanced import generateaudio_gtts_emotion

# Free TTS with emotion effects
generateaudio_gtts_emotion("This is really disappointing and makes me sad.")
# Creates: output_gtts_emotion.mp3 with audio effects
3. Compare All Methods
python
from utils_enhanced import generateaudio_all_methods

# Generate using all 4 methods
generateaudio_all_methods("This is the best news ever!")
4. Direct SSML Generation
python
from utils_enhanced import generate_ssml_direct, getemotion

text = "I'm so excited about this!"
emotions = getemotion(text)
ssml = generate_ssml_direct(text, emotions)
print(ssml)
# Output: <speak><google:style name="lively"><prosody rate="fast" pitch="+2st" volume="loud">...</prosody></google:style></speak>
🎯 How It Works
1. Enhanced Emotion Analysis Pipeline
text
Text Input → BERT Emotion Model → Rule-Based SSML Generation → Audio Synthesis + Effects
2. Direct SSML Generation (No LLM Required)
Emotion	SSML Style	Rate	Pitch	Volume	Audio Effects
Joy/Happiness	lively	fast	+2st	loud	1.2x speed, normalized
Love	lively	medium	+1st	loud	UK accent, gentle tone
Sadness	empathetic	slow	-2st	soft	0.8x speed, -5dB volume
Fear	empathetic	fast	+1st	soft	Canadian accent, nervous
Anger	firm	medium	+1st	loud	Normalized, emphasis
Surprise	None	x-fast	+3st	medium	Australian accent
3. gTTS Emotion Enhancement
The new gTTS implementation includes:

Voice Selection: Different English accents per emotion

Text Preprocessing: Emotion-based punctuation adjustment

Audio Effects: Post-synthesis speed/volume modification

Smart Emphasis: Automatic keyword detection and enhancement

4. Intensity-Based Scaling
High Confidence (>0.7):

Multiple SSML enhancements (prosody + emphasis + Google styles)

Significant audio effects (±20% speed, ±10dB volume)

Strategic breaks and emphasis markers

Medium Confidence (0.3-0.7):

Moderate prosody adjustments

Subtle audio effects (±10% speed, ±5dB volume)

Selective emphasis on key words

Low Confidence (<0.3):

Minimal parameter changes

Standard voice settings with slight accent variation

📁 Enhanced Project Structure
text
emotion-tts-system/
├── main_enhanced.py           # 🆕 Interactive CLI with all methods
├── utils_enhanced.py          # 🆕 Enhanced utilities with direct SSML
├── requirements_enhanced.txt  # 🆕 Updated dependencies
├── main.py                   # Original implementation
├── utils.py                  # Original utilities
├── requirements.txt          # Original dependencies
├── README.md                 # This documentation
├── .env                      # Environment variables
└── outputs/                  # Generated audio files
    ├── output_basic.mp3
    ├── output_top.mp3
    ├── output_basic_ssml.mp3
    └── output_gtts_emotion.mp3  # 🆕 gTTS with effects
🔍 Technical Implementation
Direct SSML Generation Logic
python
class EmotionSSMLGenerator:
    def __init__(self):
        self.emotion_mappings = {
            'joy': {
                'style': 'lively',
                'rate': 'fast', 
                'pitch': '+2st',
                'volume': 'loud',
                'emphasis_level': 'strong'
            }
            # ... 10 more emotions
        }
    
    def generate_ssml(self, text, emotions):
        emotion_type, intensity = self.get_dominant_emotion(emotions)
        enhanced_text = self.add_emphasis_to_text(text, intensity)
        enhanced_text = self.add_breaks(enhanced_text, intensity)
        return self.build_ssml_markup(enhanced_text, emotion_type, intensity)
gTTS Audio Effects Pipeline
python
class EmotionAwaregTTS:
    def synthesize_with_emotion(self, text, emotions):
        # 1. Select accent based on emotion
        voice_params = self.emotion_voice_mapping[emotion_type]
        
        # 2. Generate base audio with gTTS
        tts = gTTS(text=processed_text, **voice_params)
        
        # 3. Apply audio effects using PyDub
        if emotion_type in ['joy', 'happiness']:
            audio = speedup(audio, playback_speed=1.2)
            audio = normalize(audio, headroom=0.1)
        elif emotion_type == 'sadness':
            audio = speedup(audio, playback_speed=0.8)
            audio = audio - 5  # Reduce volume by 5dB
🎛️ Advanced Features
Smart Text Processing
Keyword Detection: Automatically identifies emotional keywords for emphasis

Strategic Breaks: Adds pauses before dramatic words based on intensity

Punctuation Enhancement: Adjusts punctuation for emotional effect

Superlative Highlighting: Emphasizes words like "best", "amazing", "terrible"

Multi-Method Comparison
Method	Cost	Quality	Emotion Features	Speed	Dependencies
Google Cloud Basic	Paid	High	SSML support	Fast	Cloud APIs
Google Cloud Premium	Higher	Highest	Natural voice	Fast	Cloud APIs
SSML Enhanced	Paid	Highest	Advanced markup	Fast	Cloud APIs
gTTS Emotion	Free	Good	Audio effects	Medium	None
Error Handling & Fallbacks
python
# Automatic fallback system
def generateaudio_with_fallback(text):
    try:
        # Try premium Google Cloud first
        generateaudio_top(text)
    except Exception as e1:
        try:
            # Fallback to basic Google Cloud
            generateaudio_basic(text)
        except Exception as e2:
            # Final fallback to free gTTS
            generateaudio_gtts_emotion(text)
🚦 Migration Guide
From Previous Version
Old Usage (LLM-dependent):

python
from utils import generateaudio_basic_ssml
generateaudio_basic_ssml(text)  # Required Gemini API
New Usage (LLM-free):

python
from utils_enhanced import generateaudio_basic_ssml
generateaudio_basic_ssml(text)  # No LLM required!
New Methods Available
python
# Free alternative with emotion effects
from utils_enhanced import generateaudio_gtts_emotion
generateaudio_gtts_emotion("I'm so happy!")

# Compare all methods
from utils_enhanced import generateaudio_all_methods  
generateaudio_all_methods("Test all synthesis methods!")


