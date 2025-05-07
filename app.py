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
