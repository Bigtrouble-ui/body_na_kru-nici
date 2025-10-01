import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import io

# ---------- Záložky ----------
tab1, tab2 = st.tabs(["Výpočty kružnice", "Informace o mně"])

# ---------- Záložka 1: Výpočty ----------
with tab1:
    st.header("Výpočty bodů na kružnici")

    # --- Vstupy ---
    jmeno = st.text_input("Jméno:", "Filip Boudný")
    kontakt = st.text_input("Kontakt:", "277690@vutbr.cz")
    stred_x = st.number_input("Střed X:", value=1.0)
    stred_y = st.number_input("Střed Y:", value=1.0)
    stred = (stred_x, stred_y)
    polomer = st.number_input("Poloměr (m):", value=3.0)
    pocet_bodu = st.number_input("Počet bodů:", value=20, step=1)
    barva = st.color_picker("Barva bodů:", "#00fff1")

    # --- Výpočet bodů ---
    theta = np.linspace(0, 2*np.pi, pocet_bodu, endpoint=False)
    x = stred[0] + polomer * np.cos(theta)
    y = stred[1] + polomer * np.sin(theta)

    # --- Graf ---
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.grid(True)
    ax.scatter(x, y, color=barva)
    for i, (xx, yy) in enumerate(zip(x, y), start=1):
        ax.text(xx, yy, str(i), fontsize=8, ha="center", va="center")
    kruh = plt.Circle(stred, polomer, fill=False)
    ax.add_artist(kruh)
    st.pyplot(fig)

    # --- PDF tlačítko ---
    if st.button("Vytvořit PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("arial", "", "arial.ttf", uni=True)
        pdf.set_font("arial", size=12)

        pdf.cell(200, 10, txt="Výpočty bodů na kružnici", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Jméno: {jmeno}", ln=True)
        pdf.cell(200, 10, txt=f"Kontakt: {kontakt}", ln=True)
        pdf.cell(200, 10, txt=f"Střed: {stred}", ln=True)
        pdf.cell(200, 10, txt=f"Poloměr: {polomer} m", ln=True)
        pdf.cell(200, 10, txt=f"Počet bodů: {pocet_bodu}", ln=True)
        pdf.cell(200, 10, txt=f"Barva: {barva}", ln=True)
        pdf.ln(10)

        # --- Graf do PDF ---
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        pdf.image(buf, x=10, y=None, w=pdf.w - 20)  # šířka stránky - okraje

        pdf_bytes = bytes(pdf.output(dest="S"))
        st.download_button("📥 Stáhnout PDF", pdf_bytes, file_name="vystup.pdf")

# ---------- Záložka 2: Informace o mně ----------
with tab2:
    st.header("Informace o mně a použitých technologiích")
    st.write("""
    **Jméno:** Filip Boudný 
    **Kontakt:** 277690@vutbr.cz  

    **Použité technologie:**  
    - Python 3  
    - Streamlit  
    - Matplotlib  
    - Numpy  
    - fpdf2
    """)