import streamlit as st
import pandas as pd
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from documentation.documentation import (
    audio_narration_info, video_sync_info, dubbing_info, rm_costs, rm_svo
)

st.set_page_config(layout="wide")
# Function to load settings and TTS service rates from the Excel file
def load_settings(excel_file_path):
    df = pd.read_excel(excel_file_path)
    settings = df.iloc[0].to_dict()
    
    # Find the column that contains the list of TTS services
    tts_service_column = None
    for col in df.columns:
        if 'ttsServiceList' in col:
            tts_service_column = col
            break
    
    tts_rates = {}
    
    if tts_service_column is not None:
        # Get the list of TTS services from the specified column
        tts_service_list = df[tts_service_column][0].split(', ')
        for service in tts_service_list:
            rate_col = f'{service.strip()} Rate'
            if rate_col in df:
                rate = df[rate_col][0]
                tts_rates[service.strip()] = rate
    
    return settings, tts_rates

# Create a Streamlit app
st.title("SVO Wizard")

with st.chat_message("assistant"):
    st.write("Supported languages and generic voice SVO samples:")
    # Using st.markdown to create emoji buttons as links
    rm_svo()

st.write("---")

col1, col2 = st.columns(2)
with col1:
    svo_service = st.selectbox("Select the SVO Type", [
        "Audio Narration",
        "Video Sync",
        "Dubbing (UN-Style)"
    ])

if svo_service == "Audio Narration":
    audio_narration_info()

elif svo_service == "Video Sync":
    video_sync_info()

elif svo_service == "Dubbing (UN-Style)":
    dubbing_info()

st.write("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    mediaMinutes = st.number_input('Media Length (minutes)', min_value=0, value=60)
with col2:
    characters = st.number_input("How many characters (not specified = 1)", min_value=0, value=1)
with col3:
    LQARound = st.number_input('SVO Audio LQA Rounds', min_value=0, max_value=5, value=1)
with col4:
    samples_review = st.radio("Is the client reviewing the samples?", ["Review Required", "Review not Required"], index=0)


col1, col2, col3, col4 = st.columns(4)
with col1:
    transcription = st.radio("Transcription: Y/N", ["Yes", "No"])
with col2:
    translation = st.radio("Translation: Y/N", ["Yes", "No"])

# Create Audio Narration
if svo_service == "Audio Narration":

    with col3:
        dpIntegration = st.radio("DP Integration: Y/N", ["Yes", "No"], index=1)

    with col4:
        if (transcription == "No" or translation == "No"):
            scriptPreparation = st.radio("Script Preparation: Y/N", ["Yes", "No"])
        else:
            scriptPreparation = None
        audioEditing = "No"

# Create Video Sync
if svo_service == "Video Sync":

    with col2:
        if (transcription == "No" or translation == "No"):
            scriptPreparation = st.radio("Script Preparation: Y/N", ["Yes", "No"])
        else:
            scriptPreparation = None

    with col3:
        audioEditing = st.selectbox("Who is taking care of syncing the audio?", [
            "Audio Editing",
            "DP integration",
        ])
        if (audioEditing == "Audio Editing"):
            with col4:
                dpIntegration = st.radio("DP Integration: Y/N", ["Yes", "No"], index=1)
            audioEditing = "Yes"
            #dpIntegration = "No"
        else:

            audioEditing = "No"
            dpIntegration = "Yes"

# Create Dubbing (UN-Style)
if svo_service == "Dubbing (UN-Style)":

    with col3:
        if (transcription == "No" or translation == "No"):
            scriptPreparation = st.radio("Script Preparation: Y/N", ["Yes", "No"])
        else:
            scriptPreparation = None

    with col4:
        audioEditing = st.selectbox("Who is taking care of syncing the audio?", [
            "Audio Editing",
            "DP integration",
        ])
        if (audioEditing == "Audio Editing"):
            audioEditing = "Yes"
            dpIntegration = "No"
        else:
            audioEditing = "No"
            dpIntegration = "Yes"

# Display additional requirements based on selected options
warning = ("We accept transcriptions or translations in various formats such as .vtt, srt, Excel, or Word documents.\nHowever, it's important that the text is organized into coherent, continuous sentences and includes proper punctuation, as our Text-to-Speech system relies on it.\nIf there are multiple speakers, they must be identified and included in the transcription or translation received, with their contributions clearly marked in the text.\nIf any issues arise, we will promptly report them, but please note that we cannot be held responsible for delays or unexpected project complications.")
if scriptPreparation == "No":
    st.warning("Requirements for transcription and translation scripts:")
    st.info(f"{warning}", icon="ℹ️")


# Display additional requirements for multiple characters
ch_warning = ("We accept scripts for multiple characters only if the script has one file name per character.")
if (characters > 1) and (scriptPreparation == "No") and (audioEditing == "No"):
    st.warning("Requirements for multiple character without audio editing and script preparation:")
    st.info(f"{ch_warning}", icon="ℹ️")


with st.expander("Costs and Rates Adjustments (In Developement)"):

    with st.chat_message("assistant"):
        st.write("Consider using the most updated rates here:")
        rm_costs()
    
    # Calculate the total scope based on the selected options
    total_scope = {
        "SVO Service": svo_service,
        "Media Length": mediaMinutes,
        "Transcription": transcription,
        "Translation": translation,
        "Script Preparation": scriptPreparation,
        "SVO Audio LQA round": LQARound,
        "Samples review": samples_review,
        "Characters": characters,
        "Audio Editing": audioEditing,
        "DP Integration": dpIntegration
    }

    # Define units as a dictionary
    units = {
        "SVO Service": "",
        "Media Length": " minutes",
        "Transcription": "",
        "Translation": "",
        "Script Preparation": "",
        "SVO Audio LQA round": " Round",
        "Samples review": "",
        "Characters": " Character/s",
        "Audio Editing": "",
        "DP Integration": "",
    }

    # Display the selected options and the total scope in a dataframe
    df = pd.DataFrame([total_scope])

    # Define Excel file path
    excel_file_path = './temp/svoqg.xlsx'

    # Check if the Excel file exists, if not, create it with default values
    if not os.path.exists(excel_file_path):
        st.error('Excel file not found. Please create the Excel file with settings first.')
    else:
        # Load settings and TTS service rates from the Excel file
        settings, tts_rates = load_settings(excel_file_path)
        # Get the rate for the selected TTS service

# Input fields in the "SVO Calculator" tab
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ttsService = st.selectbox('TTS Service', list(tts_rates.keys()))
        selected_tts_rate = tts_rates.get(ttsService, 0) 
    with col2:
        ttsService = st.selectbox('TTS Service [Feedback]', list(tts_rates.keys()), index=0)
        selected_tts_fbk_rate = tts_rates.get(ttsService, 0) 
    with col3:
        lqaRate = st.number_input('LQA hourly Rate ($)', min_value=0, max_value=100, value=15)
    with col4:
        lqaratio = st.number_input('LQA time / Media Hour/s', min_value=0, max_value=4, value=3)

    col1, col2, col3, col4 = st.columns(4)
    with col1:    
        audioEditingRate = st.number_input('Audio Editing hourly Rate ($)', min_value=0, max_value=25, value=15)
    with col2:
        scriptPreparationRate = st.number_input('Script Preparation hourly Rate ($)', min_value=0, max_value=25, value=15)
    #with col3:    
        

    # Create an empty list to store cost components
    cost_components = []
    scriptPreparationUnit = math.ceil(mediaMinutes / 60.0)
    scriptPreparationCost = scriptPreparationUnit * scriptPreparationRate

    # Append all the variables to the dataframe
    if transcription == 'Yes':
        cost_components.append(('Transcription', "Included"))

    if translation == 'Yes':
        cost_components.append(('Translation', "Included"))

    if scriptPreparation == 'Yes':
        cost_components.append(('Script Preparation', str(scriptPreparationUnit) + " Hour/s", str(scriptPreparationRate) + " $", scriptPreparationCost))

    ttsGenerationCost = selected_tts_rate * mediaMinutes
    ttsFeedbackCost = selected_tts_fbk_rate * mediaMinutes / 2
    cost_components.append(('TTS Generation [Mass Production]', str(mediaMinutes) + " Minutes", str(selected_tts_rate) + " $/minute", ttsGenerationCost))
    cost_components.append(('TTS Generation [Feedback]', str(mediaMinutes/2) + " Minutes", str(selected_tts_fbk_rate) + " $/minute", ttsFeedbackCost))

    if LQARound > 0:    
        lqaRoundUnit = LQARound * math.ceil(mediaMinutes * lqaratio / 60.0)
        lqaRoundCost = lqaRate * lqaRoundUnit
        cost_components.append((str(LQARound) + ' x SVO Audio LQA Round\s', str(lqaRoundUnit) + " Hour/s", str(lqaRate) + " $/hour", lqaRoundCost))

    if audioEditing == 'Yes':
        audioEditingUnit = math.ceil(mediaMinutes / 20.0)
        audioEditingCost = audioEditingUnit * audioEditingRate
        cost_components.append(('Audio Editing', str(audioEditingUnit) + " Hour/s", str(audioEditingRate) + " $/hour", audioEditingCost))

    if dpIntegration == 'Yes':
        cost_components.append(('DP Integration', "Included"))


    # Create a DataFrame for the cost breakdown
    cost_breakdown_df = pd.DataFrame(cost_components, columns=['Cost Component', 'Units', 'Rate', 'Cost'])

    df_costs = cost_breakdown_df

    # Show Dataframe with Costs
    st.dataframe(df_costs, use_container_width=False, hide_index=True)

    # Set Selling Price per minute
    price_rate_per_minute = st.number_input('Price Rate per Minute ($/minute)', min_value=0.0, value=2.0)
    # Calculate revenue
    revenue = price_rate_per_minute * mediaMinutes
    # Calculate total cost
    total_cost = cost_breakdown_df['Cost'].sum()
    # Calculate margin
    margin = revenue - total_cost
    # Calculate margin percentage
    margin_percentage = (margin / revenue) * 100 if revenue != 0 else 0

    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("Cost:    ", f'<span style="color:red">{total_cost:.2f} $</span>', unsafe_allow_html=True)
    with col2:
        st.write("Revenue:    ", f'<span style="color:green">{revenue:.2f} $</span>', unsafe_allow_html=True)
    with col3:
        st.write("Margin:     ", f'<span style="color:blue">{margin_percentage:.2f} %</span>', unsafe_allow_html=True)


# Display the cost breakdown DataFrame and financial summary
st.subheader('SVO Process Breakdown')
df = cost_breakdown_df[['Cost Component', 'Units']]
st.dataframe(df, use_container_width=True, hide_index=True)

# Display the quote in a text input for copying
st.subheader("Scope:")

# Create a quote from the dataframe, excluding lines with "No" values
quote_lines = [f"{column}: {value}{units.get(column, '')}" for column, value in total_scope.items() if value is not None and value != "No"]
quote = "\n".join(quote_lines)

if samples_review == "Review Required":
    url2 = "https://andovar3.sharepoint.com/:f:/g/Audio/EkQaAz7Hv8FBoJtav-YDEK0BUiLiVpWahtuy-_f6UAwC1w?e=uoWzmj"
    quote += f"\n\nSVO Voice Samples:({url2})"

tot_cost = f"\n\nTotal cost for {mediaMinutes} minutes of SVO: {total_cost:.2f}$"
#quote += f"{tot_cost}"
if scriptPreparation == "No":
    quote += "\n\nRequirements for transcription and translation scripts:\n"
    quote += f"{warning}"

if (characters > 1) and (scriptPreparation == "No") and (audioEditing == "No"):
    quote += "\n\nRequirements for multiple character without audio editing and script preparation:\n"
    quote += f"{ch_warning}"

quote_input = st.code(f"{quote}")