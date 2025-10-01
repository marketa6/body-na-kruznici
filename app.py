import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages

st.set_page_config(page_title="Body na kružnici", layout="wide")

st.title("Body na kružnici – webová aplikace")

# --- 1. Vstupní parametry ---
st.sidebar.header("Parametry kružnice")
x_center = st.sidebar.number_input("X souřadnice středu [m]", value=0.0, format="%.2f")
y_center = st.sidebar.number_input("Y souřadnice středu [m]", value=0.0, format="%.2f")
radius = st.sidebar.number_input("Poloměr kružnice [m]", min_value=0.01, value=1.0, format="%.2f")
num_points = st.sidebar.number_input("Počet bodů na kružnici", min_value=1, max_value=100, value=8)
color = st.sidebar.color_picker("Barva bodů", "#FF0000")

# --- 2. Výpočet bodů na kružnici ---
angles = np.linspace(0, 2 * np.pi, int(num_points), endpoint=False)
x_points = x_center + radius * np.cos(angles)
y_points = y_center + radius * np.sin(angles)

# --- 3. Vykreslení ---
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.plot(x_center, y_center, 'ko', label="Střed")
ax.scatter(x_points, y_points, color=color, label="Body")
circle = plt.Circle((x_center, y_center), radius, fill=False, color='b', lw=2, label="Kružnice")
ax.add_artist(circle)
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.grid(True, which='both')
ax.set_title("Rozmístění bodů na kružnici")
ax.legend()
padding = radius * 1.2
ax.set_xlim(x_center - padding, x_center + padding)
ax.set_ylim(y_center - padding, y_center + padding)
for i, (x, y) in enumerate(zip(x_points, y_points)):
    ax.text(x, y, f"{i+1}", fontsize=10, ha='center', va='center', color='white', weight='bold')

st.pyplot(fig)

with st.expander("Informace o aplikaci"):
    st.markdown("""
    **Autor:** Markéta Coufalová  
    **Email:** 277723@vutbr.cz  
    **Použité technologie:** Streamlit, Python, Matplotlib  
    **Popis:**  
    Tato aplikace slouží k vizualizaci bodů na zadané kružnici, včetně možnosti exportu grafu do PDF.
    """)

def create_pdf_buffer(fig, params, author_info):
    buf = BytesIO()
    pdf = PdfPages(buf)
    fig_text = plt.figure(figsize=(8.27, 11.69))
    plt.axis('off')
    textstr = (
        f"Parametry úlohy:\n"
        f"Střed: [{x_center:.2f}, {y_center:.2f}] m\n"
        f"Poloměr: {radius:.2f} m\n"
        f"Počet bodů: {num_points}\n"
        f"Barva bodů: {color}\n\n"
        f"{author_info}"
    )
    plt.text(0.02, 0.98, textstr, fontsize=12, va='top')
    pdf.savefig(fig_text)
    plt.close(fig_text)
    pdf.savefig(fig)
    pdf.close()
    buf.seek(0)
    return buf

author_info = (
    "Autor: Markéta Coufalová\n"
    "Email: 277723@vutbr.cz\n"
)
params = {
    "Střed": f"[{x_center:.2f}, {y_center:.2f}]",
    "Poloměr": f"{radius:.2f}",
    "Počet bodů": num_points,
    "Barva bodů": color
}

if st.button("Exportovat do PDF"):
    pdf_buffer = create_pdf_buffer(fig, params, author_info)
    st.download_button(
        label="Stáhnout PDF",
        data=pdf_buffer,
        file_name="body_na_kruzici.pdf",
        mime="application/pdf"
    )