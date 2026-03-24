import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ═══════════════════════════════════════════════════════
#  KONFIGURACIJA
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="ŠtednjaBiH Pro — Analitički Alat",
    page_icon="💹",
    layout="wide"
)

# ═══════════════════════════════════════════════════════
#  NAPREDNI CSS (FIX ZA VIDLJIVOST I DIZAJN)
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8FAFC;
    }

    /* FIX ZA INPUT POLJA - Osigurava da se broj vidi */
    input[type="number"], input[type="text"] {
        color: #1E293B !important; /* Tamno siva slova */
        background-color: #FFFFFF !important; /* Bijela pozadina */
        border: 2px solid #E2E8F0 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important; /* Tamno plava/crna */
        border-right: 1px solid #1E293B;
    }
    [data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }
    
    /* KARTICE */
    .metric-card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }

    /* FORMULA BOX */
    .formula-box {
        background: #F1F5F9;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #10B981;
        margin: 15px 0;
        font-family: 'Courier New', monospace;
    }

    /* GLAVNI DUGME */
    .stButton > button {
        background: #10B981 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 15px 25px !important;
        font-weight: 700 !important;
        width: 100% !important;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background: #059669 !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  PODACI I LOGIKA (NEPROMIJENJENO)
# ═══════════════════════════════════════════════════════
RAZREDI = [
    {"naziv": "Standard (do 10k KM)", "max": 10000, "kljuc": "do_10000", "ikona": "🥉"},
    {"naziv": "Srebrni (10k-50k KM)", "max": 50000, "kljuc": "10000_50000", "ikona": "🥈"},
    {"naziv": "Zlatni (preko 50k KM)", "max": float('inf'), "kljuc": "preko_50000", "ikona": "🥇"},
]

BANKE = {
    "UniCredit Bank": {
        "boja": "#e31e24", "orocene": {
            "3 mjeseca":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "6 mjeseci":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "12 mjeseci": {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "24 mjeseca": {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "36 mjeseci": {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
        "min": 0, "link": "unicredit.ba"
    },
    "Raiffeisen Bank": {
        "boja": "#fee100", "orocene": {
            "3 mjeseca":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "6 mjeseci":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "12 mjeseci": {"do_10000": 0.05, "10000_50000": 0.05, "preko_50000": 0.05},
            "24 mjeseca": {"do_10000": 0.50, "10000_50000": 0.50, "preko_50000": 0.50},
            "36 mjeseci": {"do_10000": 0.70, "10000_50000": 0.70, "preko_50000": 0.70},
        },
        "tekuca": {"do_10000": 0.00, "10000_50000": 0.00, "preko_50000": 0.00},
        "min": 500, "link": "raiffeisenbank.ba"
    },
    "NLB Banka": {
        "boja": "#00843d", "orocene": {
            "3 mjeseca":  {"do_10000": 0.00, "10000_50000": 0.00, "preko_50000": 0.00},
            "6 mjeseci":  {"do_10000": 0.60, "10000_50000": 0.60, "preko_50000": 0.60},
            "12 mjeseci": {"do_10000": 0.60, "10000_50000": 0.60, "preko_50000": 0.60},
            "24 mjeseca": {"do_10000": 2.00, "10000_50000": 2.00, "preko_50000": 2.00},
            "36 mjeseci": {"do_10000": 2.15, "10000_50000": 2.15, "preko_50000": 2.15},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.02, "preko_50000": 0.04},
        "min": 0, "link": "nlb.ba"
    },
    "Sparkasse Bank": {
        "boja": "#e11d48", "orocene": {
            "3 mjeseca":  {"do_10000": 0.25, "10000_50000": 0.25, "preko_50000": 0.25},
            "6 mjeseci":  {"do_10000": 0.45, "10000_50000": 0.45, "preko_50000": 0.45},
            "12 mjeseci": {"do_10000": 0.65, "10000_50000": 0.65, "preko_50000": 0.65},
            "24 mjeseca": {"do_10000": 0.85, "10000_50000": 0.85, "preko_50000": 0.85},
            "36 mjeseci": {"do_10000": 1.10, "10000_50000": 1.10, "preko_50000": 1.10},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.02, "preko_50000": 0.03},
        "min": 100, "link": "sparkasse.ba"
    },
    "ASA Banka": {
        "boja": "#1e40af", "orocene": {
            "3 mjeseca":  {"do_10000": 0.35, "10000_50000": 0.50, "preko_50000": 0.65},
            "6 mjeseci":  {"do_10000": 0.55, "10000_50000": 0.70, "preko_50000": 0.90},
            "12 mjeseci": {"do_10000": 0.85, "10000_50000": 1.00, "preko_50000": 1.25},
            "24 mjeseca": {"do_10000": 1.05, "10000_50000": 1.20, "preko_50000": 1.50},
            "36 mjeseci": {"do_10000": 1.15, "10000_50000": 1.40, "preko_50000": 1.70},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.02, "preko_50000": 0.03},
        "min": 200, "link": "asabanka.ba"
    },
    "Addiko Bank": {
        "boja": "#f97316", "orocene": {
            "3 mjeseca":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "6 mjeseci":  {"do_10000": 0.60, "10000_50000": 0.60, "preko_50000": 0.60},
            "12 mjeseci": {"do_10000": 2.00, "10000_50000": 2.00, "preko_50000": 2.00},
            "24 mjeseca": {"do_10000": 2.30, "10000_50000": 2.30, "preko_50000": 2.30},
            "36 mjeseci": {"do_10000": 2.40, "10000_50000": 2.40, "preko_50000": 2.40},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.02, "preko_50000": 0.03},
        "min": 500, "link": "addiko.ba"
    },
}

PERIODI_MAPA = {"3 mjeseca": 0.25, "6 mjeseci": 0.5, "12 mjeseci": 1.0, "24 mjeseca": 2.0, "36 mjeseci": 3.0}

def fmt(br): return f"{br:,.2f} KM"

# ═══════════════════════════════════════════════════════
#  SIDEBAR - UNOS PODATAKA
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Parametri štednje")
    st.markdown("---")
    
    iznos = st.number_input("Iznos koji ulažete (KM)", min_value=100, value=10000, step=500)
    
    tip = st.radio("Metoda štednje", ["Oročena štednja", "Štednja po viđenju (Tekuća)"])
    
    period_naziv = "12 mjeseci"
    if tip == "Oročena štednja":
        period_naziv = st.selectbox("Vremenski period", list(PERIODI_MAPA.keys()), index=2)
    
    porez_ukljucen = st.checkbox("Obračunaj porez na dobit (10%)", value=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    izracunaj = st.button("ANALIZIRAJ TRŽIŠTE")

# ═══════════════════════════════════════════════════════
#  MAIN UI
# ═══════════════════════════════════════════════════════
st.markdown("<h1 style='color: #0F172A;'>📊 Analiza Štednih Proizvoda BiH</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B;'>Finansijska matematika • Seminarski rad • Analiza kamatnih stopa 2024/25</p>", unsafe_allow_html=True)

if not izracunaj:
    # Početni ekran sa brzim pregledom
    st.info("Unesite željeni iznos i period u bočnom meniju kako biste dobili detaljnu matematičku analizu.")
    
    cols = st.columns(3)
    for i, r in enumerate(RAZREDI):
        with cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <span style="font-size: 2rem;">{r['ikona']}</span>
                <h3 style="margin: 10px 0;">{r['naziv']}</h3>
                <p style="color: #64748B; font-size: 0.85rem;">Sistem automatski prepoznaje nivo pogodnosti na osnovu uloga.</p>
            </div>
            """, unsafe_allow_html=True)
else:
    # KALKULACIJE
    razred = next((r for r in RAZREDI if iznos < r["max"]), RAZREDI[-1])
    n = PERIODI_MAPA[period_naziv]
    
    rezultati = []
    for banka, info in BANKE.items():
        if tip == "Oročena štednja":
            r_stopa = info["orocene"][period_naziv][razred["kljuc"]]
            # Složeni kamatni račun
            vrijednost = iznos * (1 + r_stopa/100)**n
            metoda = "Složeni kamatni račun"
        else:
            r_stopa = info["tekuca"][razred["kljuc"]]
            # Prosta kamata
            vrijednost = iznos * (1 + (r_stopa/100) * n)
            metoda = "Prosta kamata"
            
        dobit = vrijednost - iznos
        porez = dobit * 0.10 if porez_ukljucen else 0
        neto_dobit = dobit - porez
        
        rezultati.append({
            "Banka": banka,
            "Stopa": r_stopa,
            "Neto Dobit": neto_dobit,
            "Ukupno": iznos + neto_dobit,
            "Metoda": metoda,
            "Boja": info["boja"]
        })
    
    rezultati.sort(key=lambda x: x["Ukupno"], reverse=True)
    top = rezultati[0]

    # PRIKAZ REZULTATA
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏆 Najbolja Banka", top["Banka"])
    with col2:
        st.metric("📈 Neto Prinos", fmt(top["Neto Dobit"]))
    with col3:
        st.metric("💰 Ukupna Isplata", fmt(top["Ukupno"]))

    tabs = st.tabs(["🎯 Najbolja Ponuda", "📈 Matematički Model", "📊 Poređenje svih banaka"])

    with tabs[0]:
        st.markdown(f"""
        <div style="background: white; border-radius: 20px; padding: 30px; border: 1px solid #10B981; margin-top: 20px;">
            <h2 style="color: #10B981; margin-top: 0;">Pobjednik analize: {top['Banka']}</h2>
            <div style="display: flex; gap: 50px; margin-top: 20px;">
                <div>
                    <p style="color: #64748B; margin-bottom: 5px;">Godišnja kamatna stopa</p>
                    <h1 style="margin: 0; color: #1E293B;">{top['Stopa']}%</h1>
                </div>
                <div>
                    <p style="color: #64748B; margin-bottom: 5px;">Vaš čisti profit (Neto)</p>
                    <h1 style="margin: 0; color: #10B981;">{fmt(top['Neto Dobit'])}</h1>
                </div>
            </div>
            <p style="margin-top: 25px; color: #94A3B8; font-size: 0.9rem;">
                *Obračun urađen na osnovu <b>{top['Metoda'].lower()}a</b> za period od <b>{period_naziv}</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("### 🧮 Primijenjeni matematički modeli")
        
        if tip == "Oročena štednja":
            st.latex(r"V = P \cdot (1 + i)^n")
            st.markdown(f"""
            <div class="formula-box">
                <b>Objašnjenje parametara:</b><br>
                P (Glavnica) = {fmt(iznos)}<br>
                i (Kamatna stopa) = {top['Stopa']/100}<br>
                n (Broj perioda u godinama) = {n}<br><br>
                <b>Izračun:</b><br>
                V = {iznos:,.2f} * (1 + {top['Stopa']/100})^{n} = {top['Ukupno'] + (top['Neto Dobit']*0.11 if porez_ukljucen else 0):,.2f} KM
            </div>
            """, unsafe_allow_html=True)
        else:
            st.latex(r"V = P \cdot (1 + i \cdot n)")
            st.markdown(f"""
            <div class="formula-box">
                <b>Objašnjenje parametara:</b><br>
                P (Glavnica) = {fmt(iznos)}<br>
                i (Kamatna stopa) = {top['Stopa']/100}<br>
                n (Vrijeme u godinama) = {n}<br><br>
                <b>Izračun:</b><br>
                V = {iznos:,.2f} * (1 + {top['Stopa']/100} * {n})
            </div>
            """, unsafe_allow_html=True)
            
        if porez_ukljucen:
            st.markdown("**Porez na dobit (BiH):**")
            st.latex(r"Dobit_{neto} = (V - P) \cdot 0.90")

    with tabs[2]:
        st.markdown("### 📊 Rang lista banaka")
        
        # Grafik
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.set_facecolor('#F8FAFC')
        fig.patch.set_facecolor('#F8FAFC')
        
        imena = [r["Banka"] for r in rezultati]
        dobiti = [r["Neto Dobit"] for r in rezultati]
        boje = [r["Boja"] for r in rezultati]
        
        bars = ax.bar(imena, dobiti, color=boje, edgecolor='#E2E8F0', linewidth=1)
        ax.set_ylabel("Neto zarada (KM)", fontsize=9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xticks(rotation=15, fontsize=8)
        
        st.pyplot(fig)
        
        # Tabela
        df = pd.DataFrame(rezultati)[["Banka", "Stopa", "Neto Dobit", "Ukupno"]]
        df.columns = ["Banka", "Stopa (%)", "Neto Zarada (KM)", "Ukupna Isplata (KM)"]
        st.table(df)

# ═══════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; color: #94A3B8; font-size: 0.8rem; padding: 20px; border-top: 1px solid #E2E8F0;">
    ŠtednjaBiH Pro • Model: {tip} • Razred: {razred['naziv']} • Podaci validni za 2024/2025 godinu
</div>
""", unsafe_allow_html=True)