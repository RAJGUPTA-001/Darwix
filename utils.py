import os
from dotenv import load_dotenv

load_dotenv()

def synthesize_ssml(input):
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
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')


def generateaudio(input):
    synthesize_ssml(input)