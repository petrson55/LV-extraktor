import streamlit as st
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import tempfile

st.set_page_config(page_title="Extraktor údajů z výpisu z KN")
st.title("Extraktor údajů z výpisu z KN")

uploaded_file = st.file_uploader("Nahraj výpis z KN ve formátu PDF", type="pdf")

text_output = ""

if uploaded_file is not None:
    # Nejprve se pokusíme použít pdfplumber
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text_output += extracted + "\n"
    except:
        st.warning("Chyba při zpracování přes pdfplumber.")

    # Pokud selže nebo nic neextrahujeme, použijeme OCR
    if len(text_output.strip()) < 10:
        st.info("PDF neobsahuje extrahovatelný text, provádím OCR…")
        images = convert_from_bytes(uploaded_file.read())
        for image in images:
            text_output += pytesseract.image_to_string(image, lang='ces') + "\n"

    if text_output.strip():
        st.subheader("Extrahovaný text z PDF:")
        st.text_area("Zde je celý text výpisu z KN:", text_output, height=300)

        # Prompt pro GPT
        prompt = f"""
Zde je text výpisu z katastru nemovitostí:

{full_text}

Z něj prosím vytvoř následující tabulky v přehledném formátu:

---

**Topografie**

| Název údaje         | Hodnota                   |
|---------------------|---------------------------|
| Kraj                | [ ]                       |
| Okres               | [ ]                       |
| Obec                | [ ]                       |
| Počet obyvatel      | [ ]                       |(tento údaj najdi na internetu)
| Katastrální území   | [ ]                       |
| Část obce           | [ ]                       |
| LV č.               | [ ]                       |

---

**Výpis pozemků**

| Parc.č.   | Výměra m2 | Druh pozemku                | Způsob využití             |
|----------|-----------|-----------------------------|----------------------------|
| ...      | ...       | ...                         | ...                        |

---

**Stavby**

| č.budovy  | na p. č. | Poznámka                      | Způsob využití            |
|----------|----------|-------------------------------|---------------------------|
| ...      | ...      | ...                           | ...                       |
Do poznámky uveď buď "stavba je součástí pozemku" nebo "na pozemku stojí stavba" podle výpisu

---

Uveď pouze údaje z textu výpisu a dodrž formát. Pokud některé pole chybí, nech je prázdné.

- Všechna věcná břemena a jiná práva ve formátu:

Název práva: [např. Zástavní právo smluvní]  
Popis: [např. Pohledávka ve výši... nebo text z výpisu]  
Oprávnění pro: [z výpisu]  
Povinnost k: [z výpisu]  

Výstup uveď v nečíslovaných bodech pro každé právo zvlášť.
"""

  st.subheader("Prompt pro GPT:")
        st.code(prompt)
        st.success("Zkopíruj výše uvedený prompt a vlož ho do ChatGPT pro automatické zpracování dat.")
    else:
        st.error("Nepodařilo se extrahovat žádný text z PDF.")
