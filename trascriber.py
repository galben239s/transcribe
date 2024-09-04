import streamlit as st
import openai
from io import BytesIO
import tempfile
import os
x="sk-proj-TQeHH4twl6VyJ_EM22tIF0Tn71mSvS50PlpkZX5"
y="nYMCGKLqq5j8aKz1"
z="fuRT3BlbkFJbXbgPooWnwY8gnDoPYcnFohJSJNVk_Z4Kd_bR-EZf3cf_oQj9gMIlpQIIA"

# Hardcoded API key (not recommended for production use)
API_KEY = x+y+z # Replace with your actual API key

# Initialize OpenAI client
client = openai.OpenAI(api_key=API_KEY)


def transcribe_audio(audio_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(audio_file.getvalue())
        tmp_file_path = tmp_file.name

    with open(tmp_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    os.unlink(tmp_file_path)
    return transcription.text


# Page config
st.set_page_config(page_title="Audio Transcription App", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .st-emotion-cache-16idsys p {
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# App title
st.title("🎙️ Audio Transcription App")
with st.expander("ℹ️ About this app"):
    st.markdown("""
    This app allows you to transcribe your MP3 audio files using OpenAI's powerful Whisper model.

    **How to use:**
    1. Upload your MP3 file
    2. Click the 'Transcribe' button
    3. View your transcript and download if needed

    **Note:** This app is for demonstration purposes and uses a hardcoded API key. 
    In a production environment, it's recommended to use secure methods for API key management.
    """)
# Main container
main_container = st.container()

with main_container:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Upload your audio file")
        uploaded_file = st.file_uploader("Choose an MP3 file", type="mp3")

        if uploaded_file is not None:
            st.audio(uploaded_file, format='audio/mp3')

            if st.button("🚀 Transcribe"):
                with st.spinner("🎭 Magic in progress... Transcribing your audio!"):
                    transcript = transcribe_audio(uploaded_file)
                st.session_state['transcript'] = transcript
                st.success("✨ Transcription complete!")

    with col2:
        if 'transcript' in st.session_state:
            st.markdown("### Transcript")
            with st.expander("📜 View full transcript", expanded=True):
                st.text_area("", st.session_state['transcript'], height=300)

            st.download_button(
                label="📥 Download Transcript",
                data=st.session_state['transcript'],
                file_name="transcript.txt",
                mime="text/plain"
            )

# Info section
