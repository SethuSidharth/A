import streamlit as st
import requests

# Define available Languages
LANGUAGES = {"en": "English", "hi": "Hindi", "ta": "Tamil"}

# Custom CSS for styling
st.markdown(
    """
    <style>
        .stApp {
            background-color: #07183D; 
            color: white;
        }
        .title {
            background-color: #07183D;
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: white;
            margin-bottom: 50px;
        }
        .translate-btn {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown(
    "<div class='title'>Neural Machine Translation</div>", unsafe_allow_html=True
)

# Language selection
col3, col4 = st.columns(2)

with col3:
    source_lang = st.selectbox(
        "Select Input Language",
        options=list(LANGUAGES.keys()),
        index=0,
        format_func=lambda x: LANGUAGES[x],
        label_visibility="visible",
    )

with col4:
    target_lang = st.selectbox(
        "Select Output Language",
        options=list(LANGUAGES.keys()),
        index=1,
        format_func=lambda x: LANGUAGES[x],
        label_visibility="visible",
    )

# Layout Setup
col1, col2 = st.columns(2)

with col1:
    text = st.text_area("", placeholder="Type text to translate...")

with col2:
    translated_text = st.text_area(
        "",
        placeholder="Translation will appear here...",
        value=st.session_state.get("translated_text_area_value", ""),
    )
    st.markdown(
        """
        <style>
            .copy-icon {
                position: absolute;
                top: 5px;
                right: 5px;
                cursor: pointer;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="position: relative;">
            <span class="copy-icon" onclick="navigator.clipboard.writeText('{st.session_state.get("translated_text_display", "")}')">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16">
                    <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
                    <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3z"/>
                </svg>
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Add swap icon
    st.markdown(
        """
        <style>
            .swap-icon {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                cursor: pointer;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="position: relative; width: 100%; height: 0px;">
            <span class="swap-icon" onclick="swapLanguages()">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-arrow-left-right" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M1 11.5a.5.5 0 0 0 .5.5h11.793l-3.147 3.146a.5.5 0 0 0 .708.708l4-4a.5.5 0 0 0 0-.708l-4-4a.5.5 0 0 0-.708.708L13.293 11H1.5a.5.5 0 0 0-.5.5zM15 4.5a.5.5 0 0 0-.5-.5H3.207l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L3.207 5H14.5a.5.5 0 0 0 .5-.5z"/>
                </svg>
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # JavaScript function to swap languages
    st.markdown(
        """
        <script>
            function swapLanguages() {
                let sourceLang = document.getElementById('Select Input Language');
                let targetLang = document.getElementById('Select Output Language');
                let temp = sourceLang.value;
                sourceLang.value = targetLang.value;
                targetLang.value = temp;
            }
        </script>
        """,
        unsafe_allow_html=True,
    )


# Add swap icon
with st.container():
    col_swap = st.columns([4, 1, 4])
    with col_swap[1]:
        st.markdown(
            """
            <style>
                .swap-icon {
                    cursor: pointer;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <span class="swap-icon" onclick="swapLanguages()">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-arrow-left-right" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M1 11.5a.5.5 0 0 0 .5.5h11.793l-3.147 3.146a.5.5 0 0 0 .708.708l4-4a.5.5 0 0 0 0-.708l-4-4a.5.5 0 0 0-.708.708L13.293 11H1.5a.5.5 0 0 0-.5.5zM15 4.5a.5.5 0 0 0-.5-.5H3.207l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L3.207 5H14.5a.5.5 0 0 0 .5-.5z"/>
                </svg>
            </span>
            """,
            unsafe_allow_html=True,
        )

        # JavaScript function to swap languages
        st.markdown(
            """
            <script>
                function swapLanguages() {
                    let sourceLang = document.getElementById('Select Input Language');
                    let targetLang = document.getElementById('Select Output Language');
                    let temp = sourceLang.value;
                    sourceLang.value = targetLang.value;
                    targetLang.value = temp;
                }
            </script>
            """,
            unsafe_allow_html=True,
        )


# Translate button (using st.container for centering)
with st.container():
    col_center = st.columns([1, 1, 1])  # Create columns to center the button
    with col_center[1]:  # Place the button in the middle column
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
                            translated_result = response.json().get(
                                "translated_text", ""
                            )
                            st.session_state.translated_text = translated_result
                            st.session_state.translated_text_display = translated_result
                            st.success("Translation complete!")
                        else:
                            st.error(
                                f"Error: {response.json().get('error', 'Unknown error')}"
                            )
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error translating text: {e}")
            else:
                st.warning("Please enter text to translate.")
