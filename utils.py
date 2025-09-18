from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import os


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

# 2. Define the model and the text
model_id = "boltuix/bert-emotion"
def getemotion(text):
    try:
        # 3. Call the API with top_k=13 to get all emotion scores
        result = client.text_classification(
            text=text,
            model=model_id,
            top_k=13 
        )
        detected_emotions = [emotion for emotion in result if emotion['score'] > 0.05]
        return(detected_emotions)
        # sorted_emotions = sorted(detected_emotions, key=lambda x: x['score'], reverse=True)

        # print("\n--- Detected Emotions (Score > 0.05) ---")
        # if sorted_emotions:
        #     for emotion in sorted_emotions:
        #         print(f"- {emotion['label'].capitalize()}: {emotion['score']:.4f}")
        # else:
        #     print("No dominant emotions detected above the threshold.")

    except Exception as e:
        print(f"An error occurred: {e}")

def synthesize_top(input):
    """Synthesizes speech from the input string of ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/

    """
    from google.cloud import texttospeech

    ssml = f"""
   
    {input}

    """
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=ssml)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Chirp3-HD-Achernar",  # A premium, natural-sounding female voice
)

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("output_top.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')





def synthesize_basic_ssml(input):
    """Synthesizes speech from the input string of ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/

    """
    from google.cloud import texttospeech

    ssml = f"""{input}"""
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(ssml=ssml)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
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

    # The response's audio_content is binary.
    with open("output_basic_ssml.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

def mark_ssml(input,emotion):
    from google import genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
                     You are an expert in Speech Synthesis Markup Language (SSML) and emotion-aware text-to-speech optimization. Your task is to transform a given sentence into enhanced SSML markup based on its emotion analysis scores.
                     
                     **INPUT:**
                     - Sentence: "{input}"
                     - Emotion Analysis: {emotion}
                     
                     **SSML ENHANCEMENT RULES:**
                     
                     **1. Prosody Mapping (based on dominant emotions):**
                     - **Love/Happiness/Joy (>0.5)**: `<prosody rate="fast" pitch="+2st" volume="loud">`
                     - **Excitement/Surprise (>0.3)**: `<prosody rate="x-fast" pitch="+3st">`
                     - **Sadness/Fear (>0.3)**: `<prosody rate="slow" pitch="-2st" volume="soft">`
                     - **Anger/Disgust (>0.3)**: `<prosody rate="medium" pitch="+1st" volume="loud">`
                     - **Neutral/Calm (>0.5)**: `<prosody rate="medium" pitch="medium">`
                     
                     **2. Emphasis Rules:**
                     - Apply `<emphasis level="strong">` to superlatives (best, amazing, terrible, worst)
                     - Apply `<emphasis level="moderate">` to emotional intensifiers (so, very, really, absolutely)
                     - Use `<emphasis level="strong">` for exclamatory words and phrases
                     
                     **3. Break and Pacing:**
                     - Add `<break time="200ms"/>` before/after emotional peaks for dramatic effect
                     - Use `<break strength="weak"/>` for natural speech rhythm
                     - Add longer breaks (`<break time="500ms"/>`) before climactic words in high-emotion contexts
                     
                     **4. Style Application (when applicable):**
                     - Use `<google:style name="lively">` for happiness/excitement scores >0.6
                     - Use `<google:style name="empathetic">` for sadness/concern scores >0.4
                     - Use `<google:style name="firm">` for anger/determination scores >0.5
                     
                     **5. Intensity Scaling:**
                     - **High confidence (>0.7)**: Apply multiple enhancements (prosody + emphasis + style)
                     - **Medium confidence (0.3-0.7)**: Apply moderate enhancements (prosody + selective emphasis)
                     - **Low confidence (<0.3)**: Apply minimal enhancements (subtle prosody changes only)
                     
                     **6. Special Considerations:**
                     - Wrap complete sentences with appropriate tags
                     - Use `<say-as interpret-as="expletive">` for strong negative emotions if censoring is needed
                     - Add `<mark name="emotion_peak"/>` at the most emotionally intense word
                     - Consider using `<phoneme>` tags for emphasis on key emotional words if pronunciation needs adjustment
                     
                     **OUTPUT FORMAT:**
                     Provide the enhanced SSML markup wrapped in `<speak>` tags.only return the tags and content within
                     
                     **EXAMPLE:**
                     For the sentence "This is the best news ever!" with Love: 0.8928, Happiness: 0.0936:

                     return only 

                     <speak> <google:style name="lively"> <prosody rate="fast" pitch="+2st" volume="loud"> This is <break time="200ms"/> 
                     the <emphasis level="strong"><mark name="emotion_peak"/>best</emphasis> news <emphasis level="moderate">ever</emphasis>! </prosody> </google:style> </speak> 
                     """)
    
    
    print(response.text)   
    return  response.text           
    







def synthesize_basic(input):
    """Synthesizes speech from the input string of ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/

    """
    from google.cloud import texttospeech

    ssml = f"""
   
    {input}

    """
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=ssml)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", 
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("output_basic.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

def generateaudio_top(input):
    synthesize_top(input)
def generateaudio_basic(input):
    synthesize_basic(input)
def generateaudio_basic_ssml(input):
    emotion=getemotion(input)
    input_ssml=mark_ssml(input,emotion)
    synthesize_basic_ssml(input_ssml)