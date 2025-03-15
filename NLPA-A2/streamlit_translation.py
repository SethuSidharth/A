import streamlit as st
import requests

# Define available Languages
LANGUAGES = {"en": "English", "hi": "Hindi", "ta": "Tamil"}

# Initialize session state variables if they don't exist
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "temp_source_lang" not in st.session_state:
    st.session_state.temp_source_lang = "en"
if "temp_target_lang" not in st.session_state:
    st.session_state.temp_target_lang = "hi"


# Function to swap languages (using callback pattern)
def swap_languages():
    # Store current values in temporary variables
    temp_source = st.session_state.source_lang_select
    temp_target = st.session_state.target_lang_select

    # Update session state with swapped values
    st.session_state.temp_source_lang = temp_target
    st.session_state.temp_target_lang = temp_source


# Custom CSS for styling - Enhanced with vibrant colors and soft edges
st.markdown(
    """
    <style>
        /* Main background with gradient */
        .stApp {
            background: linear-gradient(135deg, #0a1128 0%, #1e3a8a 100%);
            color: white;
        }
        
        /* Title styling with text shadow */
        .title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            color: white;
            margin-bottom: 50px;
            padding: 20px 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            background: linear-gradient(90deg, rgba(30, 58, 138, 0), rgba(30, 58, 138, 0.7), rgba(30, 58, 138, 0));
            border-radius: 10px;
        }
        
        /* Button styling */
        .stButton button {
            width: 100%;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        }
        
        /* Translate button specific styling */
        button[data-testid="baseButton-secondary"] {
            background: linear-gradient(90deg, #4338ca, #6366f1) !important;
            border: none !important;
            color: white !important;
            padding: 8px 16px !important;
        }
        
        /* Hover effect for buttons */
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            background-color: rgba(30, 41, 59, 0.8) !important;
            border: 1px solid #3b82f6 !important;
            border-radius: 12px !important;
            color: white !important;
        }
        
        /* Text area styling */
        .stTextArea textarea {
            background-color: rgba(30, 41, 59, 0.8) !important;
            border: 1px solid #3b82f6 !important;
            border-radius: 12px !important;
            color: white !important;
            padding: 15px !important;
            font-size: 16px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
            transition: all 0.3s ease !important;
        }
        
        /* Text area focus */
        .stTextArea textarea:focus {
            border: 1px solid #60a5fa !important;
            box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.3) !important;
        }
        
        /* Swap button styling */
        .swap-button button {
            background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
            color: white !important;
            border-radius: 50% !important;
            aspect-ratio: 1 !important;
            padding: 0px !important;
            width: 40px !important;
            height: 40px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border: none !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Copy button styling */
        .copy-btn button {
            background: linear-gradient(135deg, #3b82f6, #4f46e5) !important;
            border-radius: 50% !important;
            width: 40px !important;
            height: 40px !important;
            padding: 0px !important;
            position: absolute !important;
            top: 10px !important;
            right: 10px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border: none !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Success message styling */
        .stAlert {
            background-color: rgba(16, 185, 129, 0.2) !important;
            border: 1px solid #10b981 !important;
            border-radius: 12px !important;
        }
        
        /* Warning message styling */
        div[data-baseweb="notification"] {
            border-radius: 12px !important;
        }
        
        /* Custom container for language controls */
        .language-controls {
            margin-bottom: 20px;
            padding: 10px;
            background-color: rgba(30, 41, 59, 0.4);
            border-radius: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Custom container for text areas */
        .text-areas-container {
            padding: 10px;
            background-color: rgba(30, 41, 59, 0.4);
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Center elements in their columns */
        div[data-testid="column"] {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        /* Make selectbox containers full width */
        div.row-widget.stSelectbox {
            width: 100%;
        }
        
        /* Center the translate button */
        .center-translate-btn {
            display: flex;
            justify-content: center;
            margin-top: 20px;
            width: 100%;
        }
        
        .center-translate-btn > div {
            width: auto;
        }
        
        /* Main content padding */
        section[data-testid="stSidebar"] + div {
            padding-left: 5rem;
            padding-right: 5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title with enhanced styling
st.markdown(
    "<div class='title'>Neural Machine Translation</div>", unsafe_allow_html=True
)


# Filter out the selected source language from target options
def get_filtered_languages(source_lang):
    return {k: v for k, v in LANGUAGES.items() if k != source_lang}


# Language controls in a styled container
with st.container():
    st.markdown('<div class="language-controls">', unsafe_allow_html=True)

    # Language selection with better alignment
    col3, col_swap, col4 = st.columns([4, 1, 4])

    with col3:
        source_lang = st.selectbox(
            "Select Input Language",
            options=list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index(st.session_state.temp_source_lang),
            format_func=lambda x: LANGUAGES[x],
            key="source_lang_select",
        )

    # Update target language if it matches source language
    if source_lang == st.session_state.temp_target_lang:
        # Set to first available different language
        for lang in LANGUAGES.keys():
            if lang != source_lang:
                st.session_state.temp_target_lang = lang
                break

    with col_swap:
        st.write("")
        st.write("")
        st.markdown('<div class="swap-button">', unsafe_allow_html=True)
        if st.button("⇄", help="Swap languages"):
            swap_languages()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        # Get filtered languages
        filtered_languages = get_filtered_languages(source_lang)
        # Find the index of the target language in the filtered list
        target_options = list(filtered_languages.keys())

        # Default to first option if current target is same as source
        target_index = 0
        if st.session_state.temp_target_lang in target_options:
            target_index = target_options.index(st.session_state.temp_target_lang)

        target_lang = st.selectbox(
            "Select Output Language",
            options=target_options,
            index=target_index,
            format_func=lambda x: LANGUAGES[x],
            key="target_lang_select",
        )

    st.markdown("</div>", unsafe_allow_html=True)

# Text areas in a styled container
with st.container():
    st.markdown('<div class="text-areas-container">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        text = st.text_area("", placeholder="Type text to translate...", height=200)

    with col2:
        # Container for output with relative positioning
        output_container = st.container()
        with output_container:
            translated_text = st.text_area(
                "",
                placeholder="Translation will appear here...",
                value=st.session_state.translated_text,
                height=200,
            )

            # Add a copy button as an icon
            if st.session_state.translated_text:
                # Use columns to position the copy button
                copy_col1, copy_col2 = st.columns([9, 1])
                with copy_col2:
                    st.markdown('<div class="copy-btn">', unsafe_allow_html=True)
                    if st.button("📋", help="Copy to clipboard"):
                        st.code(st.session_state.translated_text, language="text")
                    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Translate button (centered properly with enhanced styling)
st.markdown('<div class="center-translate-btn">', unsafe_allow_html=True)
if st.button("Translate", key="translate", help="Click to translate the text"):
    if text.strip():
        with st.spinner("Translating..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/translate",
                    json={
                        "text": text,
                        "source_lang": source_lang,
                        "target_lang": target_lang,
                    },
                    timeout=30,
                )
                if response.status_code == 200:
                    translated_result = response.json().get("translated_text", "")
                    st.session_state.translated_text = translated_result
                    st.success("Translation complete!")
                    st.rerun()
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error translating text: {e}")
    else:
        st.warning("Please enter text to translate.")
st.markdown("</div>", unsafe_allow_html=True)
