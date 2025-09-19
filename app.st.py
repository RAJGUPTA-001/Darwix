import streamlit as st
from utils import (
    getemotion,
    generate_ssml_direct,
    synthesize_basic,
    synthesize_top,
    generateaudio_basic_ssml,
    generateaudio_gtts_emotion
)

st.set_page_config(page_title="Emotion-Aware TTS", layout="centered")

st.title("🎭 Emotion-Aware Text-to-Speech Demo")

text = st.text_area("Enter text to synthesize:", height=150)
method = st.selectbox("Select synthesis method:", ["basic", "premium", "ssml", "gtts"] )

if st.button("Generate Audio"):
    if not text.strip():
        st.error("Please enter some text.")
    else:
        st.info(f"Using method: {method}")
        
        # Show emotion analysis
        emotions = getemotion(text)
        if emotions:
            dominant = sorted(emotions, key=lambda x: x['score'], reverse=True)[0]
            st.markdown(f"**Detected Emotion:** {dominant['label']} ({dominant['score']:.2%})")
        else:
            st.markdown("**Detected Emotion:** neutral")
        
        # Generate audio
        try:
            if method == "basic":
                synthesize_basic(text)
                filename = "output_basic.mp3"
            elif method == "premium":
                synthesize_top(text)
                filename = "output_top.mp3"
            elif method == "ssml":
                generateaudio_basic_ssml(text)
                filename = "output_basic_ssml.mp3"
            else:
                generateaudio_gtts_emotion(text)
                filename = "output_gtts_emotion.mp3"
            
            st.success(f"Audio generated: {filename}")
            audio_file = open(filename, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')

        except Exception as e:
            st.error(f"Error: {e}")