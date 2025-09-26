import streamlit as st
from deep_translator import GoogleTranslator


st.set_page_config(page_title="🌍 Translator (Google Style)", layout="centered")


SUPPORTED_LANGS = GoogleTranslator().get_supported_languages(as_dict=True)


name_to_code = {name.title(): code for name, code in SUPPORTED_LANGS.items()}
code_to_name = {code: name.title() for code, name in SUPPORTED_LANGS.items()}
sorted_langs = sorted(list(name_to_code.keys()))


source_options = ["Auto-detect"] + sorted_langs
target_options = sorted_langs   

if "source_lang" not in st.session_state:
    st.session_state.source_lang = "Auto-detect"
if "target_lang" not in st.session_state:
    st.session_state.target_lang = "Urdu" if "Urdu" in target_options else target_options[0]
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "text_input" not in st.session_state:
    st.session_state.text_input = ""


def get_source_code():
    return "auto" if st.session_state.source_lang == "Auto-detect" \
           else name_to_code[st.session_state.source_lang]


st.title("🌍 Translator (Google Style)")
st.caption("Instant translations using **Google Translate backend** (deep-translator).")

col1, col2, col3 = st.columns([4, 1, 4])

with col1:
    st.session_state.source_lang = st.selectbox(
        "Source Language",
        source_options,
        index=source_options.index(st.session_state.source_lang)
        if st.session_state.source_lang in source_options else 0,
        key="src_select"
    )

with col2:
    if st.button("🔄 Swap"):
        src = st.session_state.source_lang
        tgt = st.session_state.target_lang

        st.session_state.source_lang = tgt if tgt in source_options else "Auto-detect"
        st.session_state.target_lang = src

     
        if st.session_state.target_lang == "Auto-detect":
            st.session_state.target_lang = "English"

      
        st.session_state.text_input, st.session_state.translated_text = (
            st.session_state.translated_text,
            st.session_state.text_input,
        )

        st.rerun()

with col3:
    st.session_state.target_lang = st.selectbox(
        "Target Language",
        target_options,
        index=target_options.index(st.session_state.target_lang)
        if st.session_state.target_lang in target_options else 0,
        key="tgt_select"
    )

col1, col2 = st.columns(2)
with col1:
    st.session_state.text_input = st.text_area(
        "Enter text",
        height=200,
        placeholder="Type or paste text here…",
        key="input_area"
    )
with col2:
    output_box = st.empty()
    if st.session_state.translated_text:
        output_box.text_area(
            "Translation",
            st.session_state.translated_text,
            height=200,
            key="output_area"
        )

if st.button("🚀 Translate"):
    if not st.session_state.text_input.strip():
        st.warning("Please enter some text.")
    else:
        try:
            source_code = get_source_code()
            target_code = name_to_code[st.session_state.target_lang]

            with st.spinner(f"Translating into {st.session_state.target_lang}... ⏳"):
                st.session_state.translated_text = GoogleTranslator(
                    source=source_code, target=target_code
                ).translate(st.session_state.text_input)

            output_box.text_area(
                "Translation",
                st.session_state.translated_text,
                height=200,
                key="output_area_btn"
            )
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
