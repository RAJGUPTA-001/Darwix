from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import os
import re

load_dotenv()

# --- Configuration ---
try:
    HF_TOKEN = os.getenv("HUGGINGFACE_KEY")
    if not HF_TOKEN:
        raise ValueError("Hugging Face token not found in environment variables.")
except (KeyError, ValueError) as e:
    print(e)
    exit()

client = InferenceClient(token=HF_TOKEN)
model_id = "boltuix/bert-emotion"

def getemotion(text):
    """Get emotion analysis from text using Hugging Face model"""
    try:
        result = client.text_classification(
            text=text,
            model=model_id,
            top_k=13
        )
        detected_emotions = [emotion for emotion in result if emotion['score'] > 0.05]
        return detected_emotions
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

class EmotionSSMLGenerator:
    """Generate SSML markup based on detected emotions without using LLMs"""

    def __init__(self):
        # Emotion to prosody mapping
        self.emotion_mappings = {
            # High-energy positive emotions
            'joy': {
                'style': 'lively',
                'rate': 'fast',
                'pitch': '+2st',
                'volume': 'loud',
                'emphasis_level': 'strong'
            },
            'love': {
                'style': 'lively',
                'rate': 'medium',
                'pitch': '+1st',
                'volume': 'loud',
                'emphasis_level': 'moderate'
            },
            'happiness': {
                'style': 'lively',
                'rate': 'fast',
                'pitch': '+2st',
                'volume': 'loud',
                'emphasis_level': 'strong'
            },
            'excitement': {
                'style': 'lively',
                'rate': 'x-fast',
                'pitch': '+3st',
                'volume': 'loud',
                'emphasis_level': 'strong'
            },
            'surprise': {
                'style': None,
                'rate': 'x-fast',
                'pitch': '+3st',
                'volume': 'medium',
                'emphasis_level': 'strong'
            },
            'optimism': {
                'style': 'lively',
                'rate': 'medium',
                'pitch': '+1st',
                'volume': 'medium',
                'emphasis_level': 'moderate'
            },

            # Negative emotions
            'sadness': {
                'style': 'empathetic',
                'rate': 'slow',
                'pitch': '-2st',
                'volume': 'soft',
                'emphasis_level': 'reduced'
            },
            'fear': {
                'style': 'empathetic',
                'rate': 'fast',
                'pitch': '+1st',
                'volume': 'soft',
                'emphasis_level': 'moderate'
            },
            'anger': {
                'style': 'firm',
                'rate': 'medium',
                'pitch': '+1st',
                'volume': 'loud',
                'emphasis_level': 'strong'
            },
            'disgust': {
                'style': 'firm',
                'rate': 'slow',
                'pitch': '-1st',
                'volume': 'medium',
                'emphasis_level': 'moderate'
            },

            # Neutral emotions
            'neutral': {
                'style': None,
                'rate': 'medium',
                'pitch': 'medium',
                'volume': 'medium',
                'emphasis_level': 'none'
            }
        }

        # Keywords that should get emphasis
        self.emphasis_keywords = {
            'strong': ['best', 'amazing', 'incredible', 'fantastic', 'wonderful', 'terrible', 'worst', 'awful'],
            'moderate': ['very', 'really', 'quite', 'pretty', 'so', 'absolutely', 'totally', 'completely']
        }

    def get_dominant_emotion(self, emotions):
        """Get the dominant emotion from the emotion list"""
        if not emotions:
            return 'neutral', 0.5

        # Sort by score and get the highest
        sorted_emotions = sorted(emotions, key=lambda x: x['score'], reverse=True)
        dominant = sorted_emotions[0]

        # Map emotion labels to our mapping keys
        emotion_label = dominant['label'].lower()

        # Handle variations in emotion labels
        if emotion_label in ['happy', 'happiness']:
            emotion_label = 'happiness'
        elif emotion_label in ['joyful']:
            emotion_label = 'joy'
        elif emotion_label in ['excited']:
            emotion_label = 'excitement'
        elif emotion_label in ['sad']:
            emotion_label = 'sadness'
        elif emotion_label in ['angry']:
            emotion_label = 'anger'

        return emotion_label, dominant['score']

    def add_emphasis_to_text(self, text, emotion_config, intensity):
        """Add emphasis tags to important words in the text"""
        words = text.split()
        processed_words = []

        for word in words:
            word_lower = word.lower().strip('.,!?;:')

            # Check for strong emphasis words
            if word_lower in self.emphasis_keywords['strong']:
                if intensity > 0.7:
                    processed_words.append(f'<emphasis level="strong"><mark name="emotion_peak"/>{word}</emphasis>')
                elif intensity > 0.4:
                    processed_words.append(f'<emphasis level="moderate">{word}</emphasis>')
                else:
                    processed_words.append(word)

            # Check for moderate emphasis words
            elif word_lower in self.emphasis_keywords['moderate']:
                if intensity > 0.5:
                    processed_words.append(f'<emphasis level="moderate">{word}</emphasis>')
                else:
                    processed_words.append(word)

            else:
                processed_words.append(word)

        return ' '.join(processed_words)

    def add_breaks(self, text, emotion, intensity):
        """Add strategic breaks to the text"""
        # Add break before emotional peaks
        if intensity > 0.7:
            # Find superlatives and add dramatic pause before them
            for keyword in self.emphasis_keywords['strong']:
                pattern = r'\b(the|a)\s+(' + keyword + r')\b'
                replacement = r'\1 <break time="200ms"/> \2'
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        return text

    def generate_ssml(self, text, emotions):
        """Generate SSML markup based on emotions"""
        emotion_type, intensity = self.get_dominant_emotion(emotions)

        # Get emotion configuration
        if emotion_type in self.emotion_mappings:
            emotion_config = self.emotion_mappings[emotion_type]
        else:
            emotion_config = self.emotion_mappings['neutral']

        # Process text with emphasis
        enhanced_text = self.add_emphasis_to_text(text, emotion_config, intensity)

        # Add strategic breaks
        enhanced_text = self.add_breaks(enhanced_text, emotion_type, intensity)

        # Build SSML
        ssml_parts = ['<speak>']

        # Add Google style if available
        if emotion_config['style'] and intensity > 0.6:
            ssml_parts.append(f'<google:style name="{emotion_config["style"]}">')

        # Add prosody
        prosody_attrs = []
        if emotion_config['rate'] != 'medium':
            prosody_attrs.append(f'rate="{emotion_config["rate"]}"')
        if emotion_config['pitch'] != 'medium':
            prosody_attrs.append(f'pitch="{emotion_config["pitch"]}"')
        if emotion_config['volume'] != 'medium':
            prosody_attrs.append(f'volume="{emotion_config["volume"]}"')

        if prosody_attrs:
            ssml_parts.append(f'<prosody {" ".join(prosody_attrs)}>')

        # Add the processed text
        ssml_parts.append(enhanced_text)

        # Close prosody
        if prosody_attrs:
            ssml_parts.append('</prosody>')

        # Close Google style
        if emotion_config['style'] and intensity > 0.6:
            ssml_parts.append('</google:style>')

        ssml_parts.append('</speak>')

        return ' '.join(ssml_parts)

# Initialize SSML generator
ssml_generator = EmotionSSMLGenerator()

def generate_ssml_direct(text, emotions):
    """Generate SSML directly without using LLM"""
    return ssml_generator.generate_ssml(text, emotions)

# ===== GOOGLE CLOUD TTS FUNCTIONS =====

def synthesize_top(input_text):
    """Synthesizes speech using premium voice"""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()
    input_text_obj = texttospeech.SynthesisInput(text=input_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Chirp3-HD-Achernar",
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text_obj, voice=voice, audio_config=audio_config
    )

    with open("output_top.mp3", "wb") as out:
        out.write(response.audio_content)
    print('Audio content written to file "output_top.mp3"')

def synthesize_basic_ssml(ssml_input):
    """Synthesizes speech from SSML input"""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(ssml=ssml_input)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-F",
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    with open("output_basic_ssml.mp3", "wb") as out:
        out.write(response.audio_content)
    print('Audio content written to file "output_basic_ssml.mp3"')

def synthesize_basic(input_text):
    """Basic text synthesis"""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()
    input_text_obj = texttospeech.SynthesisInput(text=input_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text_obj, voice=voice, audio_config=audio_config
    )

    with open("output_basic.mp3", "wb") as out:
        out.write(response.audio_content)
    print('Audio content written to file "output_basic.mp3"')

# ===== gTTS EMOTION-AWARE FUNCTIONS =====

class EmotionAwaregTTS:
    """gTTS wrapper with emotion-based parameter tweaking"""

    def __init__(self):
        self.emotion_voice_mapping = {
            'joy': {'lang': 'en', 'tld': 'com', 'slow': False},
            'happiness': {'lang': 'en', 'tld': 'com', 'slow': False},
            'love': {'lang': 'en', 'tld': 'co.uk', 'slow': False},
            'excitement': {'lang': 'en', 'tld': 'com.au', 'slow': False},
            'sadness': {'lang': 'en', 'tld': 'co.uk', 'slow': True},
            'fear': {'lang': 'en', 'tld': 'ca', 'slow': True},
            'anger': {'lang': 'en', 'tld': 'com', 'slow': False},
            'neutral': {'lang': 'en', 'tld': 'com', 'slow': False}
        }

    def preprocess_text_for_emotion(self, text, emotion, intensity):
        """Preprocess text to simulate emotional speech patterns"""

        if emotion in ['joy', 'happiness', 'excitement'] and intensity > 0.6:
            # Add exclamation for emphasis
            if not text.endswith('!'):
                text = text.rstrip('.') + '!'

            # Add emphasis through punctuation and repetition
            text = re.sub(r'\b(amazing|incredible|fantastic|wonderful|great)\b', 
                         r'\1!', text, flags=re.IGNORECASE)

        elif emotion in ['sadness', 'fear'] and intensity > 0.5:
            # Add ellipses for dramatic pauses
            text = re.sub(r'\b(but|however|unfortunately)\b', 
                         r'... \1', text, flags=re.IGNORECASE)

        elif emotion == 'anger' and intensity > 0.6:
            # Add emphasis through capitalization (sparingly)
            for word in ['never', 'always', 'terrible', 'awful']:
                text = re.sub(f'\\b{word}\\b', word.upper(), text, flags=re.IGNORECASE)

        return text

    # def synthesize_with_emotion(self, text, emotions, output_file="output_gtts_emotion.mp3"):
    #     """Synthesize speech using gTTS with emotion-based tweaks"""
    #     try:
    #         from gtts import gTTS
    #         import pygame
    #         from pydub import AudioSegment
    #         from pydub.effects import speedup, normalize
    #     except ImportError:
    #         print("Required packages not installed. Run: pip install gtts pygame pydub")
    #         return

    #     # Get dominant emotion
    #     emotion_type = 'neutral'
    #     intensity = 0.5

    #     if emotions:
    #         sorted_emotions = sorted(emotions, key=lambda x: x['score'], reverse=True)
    #         emotion_type = sorted_emotions[0]['label'].lower()
    #         intensity = sorted_emotions[0]['score']

    #     # Get voice parameters for emotion
    #     if emotion_type in self.emotion_voice_mapping:
    #         voice_params = self.emotion_voice_mapping[emotion_type]
    #     else:
    #         voice_params = self.emotion_voice_mapping['neutral']

    #     # Preprocess text for emotional effect
    #     processed_text = self.preprocess_text_for_emotion(text, emotion_type, intensity)

    #     # Generate base audio
    #     tts = gTTS(
    #         text=processed_text,
    #         lang=voice_params['lang'],
    #         tld=voice_params['tld'],
    #         slow=voice_params['slow']
    #     )

    #     # Save to temporary file
    #     temp_file = "temp_gtts.mp3"
    #     tts.save(temp_file)

    #     # Load and modify audio based on emotion
    #     audio = AudioSegment.from_mp3(temp_file)

    #     # Apply emotion-based audio effects
    #     if emotion_type in ['joy', 'happiness', 'excitement']:
    #         # Increase tempo and pitch for happy emotions
    #         if intensity > 0.7:
    #             audio = speedup(audio, playback_speed=1.2)
    #         elif intensity > 0.5:
    #             audio = speedup(audio, playback_speed=1.1)

    #         # Normalize volume (make it louder)
    #         audio = normalize(audio, headroom=0.1)

    #     elif emotion_type in ['sadness', 'fear']:
    #         # Decrease tempo for sad emotions
    #         if intensity > 0.6:
    #             audio = speedup(audio, playback_speed=0.8)
    #         elif intensity > 0.4:
    #             audio = speedup(audio, playback_speed=0.9)

    #         # Reduce volume
    #         audio = audio - 5  # Reduce by 5dB

    #     elif emotion_type == 'anger':
    #         # Keep normal speed but increase volume
    #         audio = normalize(audio, headroom=0.0)

    #     # Save final audio
    #     audio.export(output_file, format="mp3")

    #     # Clean up temporary file
    #     os.remove(temp_file)

    #     print(f'Emotion-aware gTTS audio saved to "{output_file}"')
    #     print(f'Detected emotion: {emotion_type} (intensity: {intensity:.2f})')

# Initialize emotion-aware gTTS
gtts_emotion = EmotionAwaregTTS()

# ===== PUBLIC API FUNCTIONS =====

def generateaudio_top(input_text):
    """Generate audio using premium Google Cloud voice"""
    synthesize_top(input_text)

def generateaudio_basic(input_text):
    """Generate basic audio using Google Cloud TTS"""
    synthesize_basic(input_text)

def generateaudio_basic_ssml(input_text):
    """Generate SSML-enhanced audio without using LLM"""
    emotions = getemotion(input_text)
    ssml_markup = generate_ssml_direct(input_text, emotions)
    print(f"Generated SSML: {ssml_markup}")
    synthesize_basic_ssml(ssml_markup)

def generateaudio_gtts_emotion(input_text):
    """Generate audio using emotion-aware gTTS"""
    emotions = getemotion(input_text)
    gtts_emotion.synthesize_with_emotion(input_text, emotions)

def generateaudio_all_methods(input_text):
    """Generate audio using all available methods"""
    print(f"Processing text: '{input_text}'")

    # Get emotions once
    emotions = getemotion(input_text)
    print(f"Detected emotions: {emotions}")

    # Method 1: Basic Google Cloud TTS
    print("\n1. Generating basic Google Cloud TTS...")
    generateaudio_basic(input_text)

    # Method 2: Premium Google Cloud TTS
    print("\n2. Generating premium Google Cloud TTS...")
    generateaudio_top(input_text)

    # Method 3: SSML-enhanced Google Cloud TTS (no LLM)
    print("\n3. Generating SSML-enhanced TTS (direct generation)...")
    generateaudio_basic_ssml(input_text)

    # Method 4: Emotion-aware gTTS
    print("\n4. Generating emotion-aware gTTS...")
    generateaudio_gtts_emotion(input_text)

    print("\nAll audio generation methods completed!")


