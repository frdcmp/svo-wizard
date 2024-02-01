# documentation.py

import streamlit as st
import os

# URLs
url_supported_languages = "https://andovar3.sharepoint.com/:x:/g/Audio/EcgPANhWI1tOvO1Q89hhKWkBRxnfijBdrav5rU1DIsEBaw?e=9exw1e"
url_voice_samples = "https://andovar3.sharepoint.com/:f:/g/Audio/EkQaAz7Hv8FBoJtav-YDEK0BUiLiVpWahtuy-_f6UAwC1w?e=uoWzmj"
url_SVO_QC_costs = "https://andovar3.sharepoint.com/:x:/s/RMMeeting/EfrQkPECuqpPsjMq0Nt9ObsBbqgO1OM2oIiykjnD8tMZVQ?e=njLjfU"
url_adaptation_costs = "https://andovar3.sharepoint.com/:x:/s/RMMeeting/Eanx8uRReJVGggkcgcERLjQBe5Rb39ErygkE8bXRmXjlpA?e=ehcbQI"

# Emojis for buttons
emoji_supported_languages = "🌐"
emoji_voice_samples = "🎤"
emoji = "🔊"
emoji_SVO_QC_costs = "💵"
emoji_adaptation_costs = "🔄"

# Labels for buttons
label_supported_languages = "Supported Languages"
label_voice_samples = "Voice-Over Samples"
label_SVO_QC_costs = "SVO_QC_costs"
label_adaptation_costs = "adaptation_costs"

# Media Showcase Links
un_style = "./documentation/un-style.mp4"
video_sync = "./documentation/video-sync.mp4"


def rm_costs():
    st.markdown(f"[{emoji_SVO_QC_costs} {label_SVO_QC_costs}]({url_SVO_QC_costs})", unsafe_allow_html=True)
    st.markdown(f"[{emoji_adaptation_costs} {label_adaptation_costs}]({url_adaptation_costs})", unsafe_allow_html=True)

def rm_svo():
    st.markdown(f"[{emoji_supported_languages} {label_supported_languages}]({url_supported_languages})", unsafe_allow_html=True)
    st.markdown(f"[{emoji_voice_samples} {label_voice_samples}]({url_voice_samples})", unsafe_allow_html=True)

def audio_narration_info():
    link_label_an = "Audio Script for Audio Narration"
    link_url_an = "https://www.notion.so/andovar-studio/Audio-Scripts-850ea2b09003466db085e27c392bea78?pvs=4#30a6dbd362854a10aec035dd08525258"

    st.markdown(f"""
- Audio Specification: **Multiple** standalone audio files, each associated with distinct names, used for applications such as e-learning courses, audiobooks, and voice-over narrations.
- Key Characteristics:
    - No synchronization with video elements.
    - Primarily utilized for integration with a localized e-learning course.
- Information needed: **File names, Target Text, Source Text, Characters** (if more than one).

[{emoji} {link_label_an}]({link_url_an})

""")

    # Path to the directory containing audio files
    audio_dir = "./documentation/audio_narration"

    # Get a list of audio files in the directory and sort them alphabetically
    audio_files = sorted([f for f in os.listdir(audio_dir) if f.endswith(".mp3")])

    # Display a selectbox for audio file selection
    selected_audio_file = st.selectbox("Select Audio File", audio_files)

    # Check if an audio file is selected
    if selected_audio_file:
        # Get the file path
        audio_path = os.path.join(audio_dir, selected_audio_file)

        # Display the audio player
        st.audio(audio_path, format="audio/mp3")


def video_sync_info():
    link_label_vs = "Audio Script for Video Sync"
    link_url_vs = "https://www.notion.so/andovar-studio/Audio-Scripts-850ea2b09003466db085e27c392bea78?pvs=4#72a8bc2292e9472790e13a7dc3299cb0"
    st.markdown(f"""
- Audio Specification: **Single** audio files, each associated with distinct names, synchronized with video content. Commonly employed in e-learning animations and similar contexts.
- Key Characteristics:
    - Requires precise timing and alignment with on-screen visuals.
    - Primarily utilized for integration with a localized e-learning course.
- Information needed: **Source file name, Timecodes, Characters** (if more than one), **Source Text, Target Text.**
- Format: Excel Document.

[{emoji} {link_label_vs}]({link_url_vs})
""")
    # Embed the iframe code
    st.video(video_sync)


def dubbing_info():
    link_label_db = "Audio Script for Dubbing UN Style"
    link_url_db = "https://www.notion.so/andovar-studio/Audio-Scripts-850ea2b09003466db085e27c392bea78?pvs=4#33cf517d68994615a95e8406670a8909"
    st.markdown(f"""
- Audio Specification: **Single** audio file time-synced with video for dubbing purposes. Applied in media localization scenarios involving individuals speaking on video, such as documentaries, short marketing clips, and character animations.
- Key Characteristics:
    - Involves synchronization of audio with video for a realistic and culturally adapted viewing experience.
    - Accommodates various visual contexts, ensuring accurate alignment with on-screen dialogues.
- Information needed: **File names, Target Text, Source Text, Characters, Timecodes.**
- Format: Excel Document.

[{emoji} {link_label_db}]({link_url_db})
""")
    # Embed the iframe code
    st.video(un_style)