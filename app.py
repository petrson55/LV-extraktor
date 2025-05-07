import streamlit as st
import pdfplumber
import io

st.set_page_config(page_title="Extraktor údajů z výpisu z KN")
st.title("Extraktor údajů z výpisu z KN")

uploaded_file = st.file_uploader("Nahraj výpis z KN ve formátu PDF", type="pdf")

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"

    st.subheader("Extrahovaný text z PDF:")
    st.text_area("Zde je celý text výpisu z KN:", full_text, height=300)

    # Prompt pro GPT (pro ruční zkopírování do ChatGPT Free)
    prompt = f"""
Zde je text výpisu z katastru nemovitostí:

{full_text}

Z něj prosím extrahuj následující informace:
- Parcelní číslo a druh pozemku/stavby
- Výměru (v m²)
- Katastrální území
- Název/názvy vlastníků a jejich podíly
- Případná věcná břemena nebo omezení vlastnického práva

Výstup uveď v přehledných bodech.
"""

    st.subheader("Prompt pro GPT:")
    st.code(prompt)
    st.success("Zkopíruj výše uvedený prompt a vlož ho do ChatGPT pro automatické zpracování dat.")
