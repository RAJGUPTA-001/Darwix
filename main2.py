from google.cloud import texttospeech

def list_voices():
    """Lists the available voices."""
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices()

    print("Available Voices:")
    for voice in response.voices:
        # Each voice has a name, language codes, gender, and natural sample rate
        print(f"- Name: {voice.name}")
        print(f"  Supported Language Codes: {', '.join(voice.language_codes)}")
        print(f"  SSML Gender: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")
        print(f"  Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")

if __name__ == "__main__":
    list_voices()
