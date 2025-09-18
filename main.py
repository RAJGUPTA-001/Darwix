# """---------------------------------------------------------------------------------------------------------------------------------------------




# using  ADC  (application default credential)

# already stored and fetched if  generated using cli 
# or set the path of your application_default_credentials.json file  to GOOGLE_APPLICATION_CREDENTIALS either direclty from terminal using


# $Env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\your\keyfile.json"



#  or in .env file with 

#  GOOGLE_APPLICATION_CREDENTIALS = C:\path\to\your\keyfile.json

#  and then load the .env file 



# for  installing google cli visit    https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe
# Alternatively, open a PowerShell terminal and run the following PowerShell commands:   
# (New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")& $env:Temp\GoogleCloudSDKInstaller.exe
    
# now configure here accordingly  for your project (created on google )   (check your console @ google for more information   https://console.cloud.google.com/ )

# now run  gcloud auth application-default set-quota-project your_projet_id
# this  will generate an ADC file for you generally at   [C:\Users\mainuser\AppData\Roaming\gcloud\application_default_credentials.json]
 


# for information on  how to set ADC visit https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment#local-user-cred













# """---------------------------------------------------------------------------------------------------------------------------------------------



# import os
# from dotenv import load_dotenv

# load_dotenv()

# def synthesize_ssml():
#     """Synthesizes speech from the input string of ssml.

#     Note: ssml must be well-formed according to:
#         https://www.w3.org/TR/speech-synthesis/

#     """
#     from google.cloud import texttospeech

#     ssml = """
#     <speak>
#   <say-as interpret-as='currency' language='en-US'>$42.01</say-as>
#   <emphasis level="high"> This</emphasis> is an hhhhhhhhhhhhhhhhhhhhhhsrt hwrt announcement
# </speak>
    
#     """
#     client = texttospeech.TextToSpeechClient()

#     input_text = texttospeech.SynthesisInput(ssml=ssml)

#     # Note: the voice can also be specified by name.
#     # Names of voices can be retrieved with client.list_voices().
#     voice = texttospeech.VoiceSelectionParams(
#         language_code="en-US",
#         name="en-US-Standard-C",
#         ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
#     )

#     audio_config = texttospeech.AudioConfig(
#         audio_encoding=texttospeech.AudioEncoding.MP3
#     )

#     response = client.synthesize_speech(
#         input=input_text, voice=voice, audio_config=audio_config
#     )

#     # The response's audio_content is binary.
#     with open("output.mp3", "wb") as out:
#         out.write(response.audio_content)
#         print('Audio content written to file "output.mp3"')
# synthesize_ssml()


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#











# """----------------------------------------------------------------------------------------------------------------------------------------------

# using direct api keys and forminf the http request 


# get the apikey from https://console.cloud.google.com


# """---------------------------------------------------------------------------------------------------------------------------------------------

# from dotenv import load_dotenv
# load_dotenv()
# import requests
# import base64

# def synthesize_ssml_with_api_key():
#     """
#     Synthesizes speech from an SSML string by making a direct REST API call
#     with an API key.
#     """
    
#     # --- Configuration ---
#     # IMPORTANT: Replace with your actual API key
#     API_KEY = os.getenv("GOOGLE_API_KEY")
#     # The REST API endpoint
#     url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={API_KEY}"
    
#     # The SSML you want to synthesize.
#     # This must be well-formed according to the W3C SSML specification.
#     ssml_text = """
#     <speak>
#       <say-as interpret-as='currency' language='en-US'>$42.01</say-as>.
#       <emphasis level="strong">This</emphasis> is an  announcement.
#     </speak>
#     """

#     # --- Construct the Request Body ---
#     # The request body must be a JSON object matching the API's structure.
#     request_body = {
#         "input": {
#             "ssml": ssml_text
#         },
#         "voice": {
#             "languageCode": "en-US",
#             "name": "en-US-Standard-C",
#             "ssmlGender": "FEMALE"
#         },
#         "audioConfig": {
#             "audioEncoding": "MP3"
#         }
#     }

#     # --- Send the Request ---
#     response = requests.post(url, json=request_body)

#     # --- Handle the Response ---
#     if response.status_code == 200:
#         # The API returns a JSON object with the audio content encoded in base64.
#         response_json = response.json()
#         audio_content = base64.b64decode(response_json['audioContent'])

#         # Save the binary audio content to a file.
#         with open("output.mp3", "wb") as out:
#             out.write(audio_content)
#             print('Audio content written to file "output.mp3"')
#     else:
#         # Print the error if the request failed.
#         print(f"Error: {response.status_code}")
#         print(response.text)

# # Run the function
# synthesize_ssml_with_api_key()








from utils import generateaudio_top, generateaudio_basic , generateaudio_basic_ssml
import streamlit as st
import io
import asyncio
from concurrent.futures import ThreadPoolExecutor
# --- Streamlit UI Configuration ---
st.set_page_config(
    page_title="Text-to-Speech Generator",
    page_icon="🔊",
    layout="centered"
)
st.markdown("""
    <style>
    .full-width-title {
        width: 100vw;
        background-color: #333; /* Example background color */
        color: white; /* Example text color */
        padding: 1rem;
        text-align: center;
        font-size: 3rem;
        /* Positioning to break out of the centered layout */
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        
        /* A little top margin for spacing */
        margin-top: -1rem; 
        margin-bottom: 5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="full-width-title">The Empathy Engine: Giving AI a Human Voice 🎙️</div>', unsafe_allow_html=True)

# st.write("Enter some text below, and click the button to generate the corresponding audio.")

# --- UI Elements ---
# Text area for user input
input_text = st.text_area("Enter text to convert to speech:", height=200,width=1200, placeholder="e.g., Hello, Streamlit!")

# Button to trigger audio generation
if st.button("Generate Audio"):
    if input_text.strip():
        with st.spinner():
              # Check if the text input is not empty
            # generateaudio(text_input)
            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(generateaudio_top, input_text),
                    executor.submit(generateaudio_basic, input_text),
                    executor.submit(generateaudio_basic_ssml, input_text),
                ]
                for future in futures:
                    try:
                        future.result()  # will re-raise exception if one occurred
                    except Exception as e:
                        print(f"Error in one of the tasks: {e}")
            st.markdown("top ttsmodel")            
            st.audio(r"C:\Users\rajgu\programming\darwix\output_top.mp3", format='audio/mp3')
            st.markdown("basic ttsmodel")
            st.audio(r"C:\Users\rajgu\programming\darwix\output_basic.mp3", format='audio/mp3')
            st.markdown("basic ttsmodel with ssml")
            st.audio(r"C:\Users\rajgu\programming\darwix\output_basic_ssml.mp3", format='audio/mp3')
            
            

    else:
        st.warning("Please enter some text before generating audio.")

# --- Footer ---
st.markdown("---")