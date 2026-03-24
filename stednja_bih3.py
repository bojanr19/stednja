import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

# ═══════════════════════════════════════════════════════
#  KONFIGURACIJA STRANICE
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="ŠtednjaBiH Analytics",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════
#  DIZAJN SISTEM — "Midnight & Electric Blue"
# ═══════════════════════════════════════════════════════
PRIMARY = "#2563eb"   # Moderna plava
DARK_BG = "#0f172a"   # Tamna teget (Sidebar)
TEXT_MAIN = "#1e293b" # Skoro crna za tekst
ACCENT = "#38bdf8"    # Svijetlo plava
LIGHT_GREY = "#f8fafc"
WHITE = "#ffffff"
SUCCESS = "#10b981"
GOLD = "#fbbf24"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* GLOBALNI RESET */
html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: {LIGHT_GREY};
    color: {TEXT_MAIN};
}}

/* SIDEBAR RE-DESIGN */
section[data-testid="stSidebar"] {{
    background-color: {DARK_BG} !important;
    border-right: 1px solid rgba(255,255,255,0.1);
}}
section[data-testid="stSidebar"] .stMarkdown {{
    padding: 0 10px;
}}
section[data-testid="stSidebar"] label {{
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase;
}}

/* INPUT POLJA */
input[type="number"] {{
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 12px !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
}}

/* DUGME */
.stButton > button {{
    background: linear-gradient(135deg, {PRIMARY} 0%, {ACCENT} 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    width: 100% !important;
    box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3) !important;
    transition: all 0.3s ease !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.4) !important;
}}

/* METRIKE */
[data-testid="metric-container"] {{
    background: {WHITE} !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 20px !important;
    padding: 24px !important;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
}}
[data-testid="stMetricValue"] {{
    color: {PRIMARY} !important;
    font-weight: 800 !important;
    font-size: 1.8rem !important;
}}

/* TABOVI */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px !important;
    background-color: transparent !important;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: {WHITE} !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px 12px 12px 12px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    color: #64748b !important;
}}
.stTabs [aria-selected="true"] {{
    background-color: {PRIMARY} !important;
    color: white !important;
    border-color: {PRIMARY} !important;
}}

/* HERO SECTION */
.hero-box {{
    background: linear-gradient(135deg, {DARK_BG} 0%, #1e293b 100%);
    border-radius: 24px;
    padding: 60px 40px;
    margin-bottom: 40px;
    color: white;
    position: relative;
    overflow: hidden;
}}
.hero-box::after {{
    content: "";
    position: absolute;
    top: -50%; right: -10%;
    width: 300px; height: 300px;
    background: {PRIMARY};
    filter: blur(120px);
    opacity: 0.2;
}}

</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  PODACI (ZADRŽANI ORIGINALNI)
# ═══════════════════════════════════════════════════════
RAZREDI = [
    {"naziv": "Mala štednja (<10k)", "max": 10000, "kljuc": "do_10000", "ikona": "🌱"},
    {"naziv": "Srednja štednja (10k-50k)", "max": 50000, "kljuc": "10000_50000", "ikona": "📈"},
    {"naziv": "Premium štednja (>50k)", "max": float('inf'), "kljuc": "preko_50000", "ikona": "💎"},
]

def odredi_razred(iznos):
    for r in RAZREDI:
        if iznos < r["max"]: return r
    return RAZREDI[-1]

BANKE = {
    "UniCredit Bank": {
        "boja": "#e31e24", "boja_sv": "#fef2f2",
        "orocene": {
            "3 mjeseca":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "6 mjeseci":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "12 mjeseci": {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "24 mjeseca": {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "36 mjeseci": {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
        "min_iznos": 0, "napomena": "Članica UniCredit Grupe."
    },
    "Raiffeisen Bank": {
        "boja": "#fee100", "boja_sv": "#fefce8",
        "orocene": {
            "3 mjeseca":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "6 mjeseci":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "12 mjeseci": {"do_10000": 0.05, "10000_50000": 0.05, "preko_50000": 0.05},
            "24 mjeseca": {"do_10000": 0.50, "10000_50000": 0.50, "preko_50000": 0.50},
            "36 mjeseci": {"do_10000": 0.70, "10000_50000": 0.70, "preko_50000": 0.70},
        },
        "tekuca": {"do_10000": 0.00, "10000_50000": 0.00, "preko_50000": 0.00},
        "min_iznos": 500, "napomena": "Fokus na digitalne usluge."
    },
    "NLB Banka": {
        "boja": "#0040ff", "boja_sv": "#eff6ff",
        "orocene": {
            "3 mjeseca":  {"do_10000": 0.00, "10000_50000": 0.00, "preko_50000": 0.00},
            "6 mjeseci":  {"do_10000": 0.60, "10000_50000": 0.60, "preko_50000": 0.60},
            "12 mjeseci": {"do_10000": 0.60, "10000_50000": 0.60, "preko_50000": 0.60},
            "24 mjeseca": {"do_10000": 2.00, "10000_50000": 2.00, "preko_50000": 2.00},
            "36 mjeseci": {"do_10000": 2.15, "10000_50000": 2.15, "preko_50000": 2.15},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.02, "preko_50000": 0.04},
        "min_iznos": 0, "napomena": "Regionalni lider u štednji."
    },
    "Sparkasse Bank": {
        "boja": "#e11d48", "boja_sv": "#fff1f2",
        "orocene": {
            "3 mjeseca":  {"do_10000": 0.25, "10000_50000": 0.25, "preko_50000": 0.25},
            "6 mjeseci":  {"do_10000": 0.45, "10000_50000": 0.45, "preko_50000": 0.45},
            "12 mjeseci": {"do_10000": 0.65, "10000_50000": 0.65, "preko_50000": 0.65},
            "24 mjeseca": {"do_10000": 0.85, "10000_50000": 0.85, "preko_50000": 0.85},
            "36 mjeseci": {"do_10000": 1.10, "10000_50000": 1.10, "preko_50000": 1.10},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.02, "preko_50000": 0.03},
        "min_iznos": 100, "napomena": "Stabilnost i povjerenje."
    },
    "ASA Banka": {
        "boja": "#2563eb", "boja_sv": "#eff6ff",
        "orocene": {
            "3 mjeseca":  {"do_10000": 0.35, "10000_50000": 0.50, "preko_50000": 0.65},
            "6 mjeseci":  {"do_10000": 0.55, "10000_50000": 0.70, "preko_50000": 0.90},
            "12 mjeseci": {"do_10000": 0.85, "10000_50000": 1.00, "preko_50000": 1.25},
            "24 mjeseca": {"do_10000": 1.05, "10000_50000": 1.20, "preko_50000": 1.50},
            "36 mjeseci": {"do_10000": 1.15, "10000_50000": 1.40, "preko_50000": 1.70},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.02, "preko_50000": 0.03},
        "min_iznos": 200, "napomena": "Domaća snaga BiH tržišta."
    },
    "Addiko Bank": {
        "boja": "#f97316", "boja_sv": "#fff7ed",
        "orocene": {
            "3 mjeseca":  {"do_10000": 0.01, "10000_50000": 0.01, "preko_50000": 0.01},
            "6 mjeseci":  {"do_10000": 0.60, "10000_50000": 0.60, "preko_50000": 0.60},
            "12 mjeseci": {"do_10000": 2.00, "10000_50000": 2.00, "preko_50000": 2.00},
            "24 mjeseca": {"do_10000": 2.30, "10000_50000": 2.30, "preko_50000": 2.30},
            "36 mjeseci": {"do_10000": 2.40, "10000_50000": 2.40, "preko_50000": 2.40},
        },
        "tekuca": {"do_10000": 0.01, "10000_50000": 0.02, "preko_50000": 0.03},
        "min_iznos": 500, "napomena": "Brza i direktna rješenja."
    },
}

PERIODI_MAPA = {"3 mjeseca": 0.25, "6 mjeseci": 0.5, "12 mjeseci": 1.0, "24 mjeseca": 2.0, "36 mjeseci": 3.0}

def fmt(iznos):
    return f"{iznos:,.2f} KM"

# ═══════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("<br><h2 style='color:white; margin-bottom:0;'>💎 ŠtednjaBiH</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:0.8rem;'>FINANSIJSKI SIMULATOR v2.0</p><br>", unsafe_allow_html=True)
    
    iznos = st.number_input("Iznos depozita (KM)", min_value=100, max_value=1000000, value=10000, step=1000)
    
    st.markdown("<br>", unsafe_allow_html=True)
    tip_stednje = st.radio("Tip štednje", ["Oročena štednja", "Štednja po viđenju"])
    
    period = "12 mjeseci"
    if tip_stednje == "Oročena štednja":
        period = st.selectbox("Trajanje ugovora", list(PERIODI_MAPA.keys()), index=2)
        
    porez_check = st.checkbox("Umanji za porez (10%)", value=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    btn_analiza = st.button("POKRENI ANALIZU")

# ═══════════════════════════════════════════════════════
#  GLAVNI SADRŽAJ
# ═══════════════════════════════════════════════════════
if not btn_analiza:
    # HERO SECTION
    st.markdown(f"""
    <div class="hero-box">
        <h1 style="margin:0; font-size:3rem; font-weight:800; letter-spacing:-0.03em;">
            Pametnija štednja,<br><span style="color:{ACCENT}">veća dobit.</span>
        </h1>
        <p style="font-size:1.1rem; opacity:0.8; margin-top:20px; max-width:600px;">
            Uporedite kamatne stope vodećih banaka u Bosni i Hercegovini. 
            Izračunajte precizan prinos koristeći složeni kamatni račun u par klikova.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🏦 Pregled tržišta (12 mjeseci)")
    
    # Brza tabela na početku
    cols = st.columns(len(BANKE))
    for i, (ime, info) in enumerate(BANKE.items()):
        stopa = info["orocene"]["12 mjeseci"]["10000_50000"]
        with cols[i]:
            st.markdown(f"""
            <div style="background:white; padding:20px; border-radius:16px; border:1px solid #e2e8f0; text-align:center;">
                <div style="width:12px; height:12px; background:{info['boja']}; border-radius:50%; margin: 0 auto 10px;"></div>
                <p style="margin:0; font-size:0.8rem; font-weight:700; color:#64748b;">{ime.split()[0]}</p>
                <h2 style="margin:0; color:{TEXT_MAIN};">{stopa}%</h2>
            </div>
            """, unsafe_allow_html=True)

else:
    # LOGIKA PRORAČUNA
    razred = odredi_razred(iznos)
    period_god = PERIODI_MAPA[period]
    
    rezultati = []
    for ime, info in BANKE.items():
        if tip_stednje == "Oročena štednja":
            stopa = info["orocene"][period][razred["kljuc"]]
            vrijednost = iznos * (1 + stopa/100)**period_god
        else:
            stopa = info["tekuca"][razred["kljuc"]]
            vrijednost = iznos * (1 + stopa/100 * period_god)
        
        zarada = vrijednost - iznos
        porez = zarada * 0.10 if porez_check else 0
        neto_zarada = zarada - porez
        
        rezultati.append({
            "banka": ime,
            "stopa": stopa,
            "ukupno": iznos + neto_zarada,
            "dobit": neto_zarada,
            "boja": info["boja"],
            "napomena": info["napomena"]
        })
    
    rezultati.sort(key=lambda x: x["ukupno"], reverse=True)
    top = rezultati[0]

    # REZULTATI HEADER
    st.markdown(f"## {razred['ikona']} Analiza za iznos {fmt(iznos)}")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Najbolja ponuda", f"{top['stopa']}%")
    m2.metric("Maks. neto dobit", fmt(top['dobit']))
    m3.metric("Ukupno nakon oročenja", fmt(top['ukupno']))
    m4.metric("Aktivni razred", razred['naziv'].split()[0])

    t1, t2, t3 = st.tabs(["🏆 Preporuka", "📊 Uporedni grafikon", "📋 Detaljna tabela"])
    
    with t1:
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns([1.5, 1])
        
        with c1:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg, {PRIMARY}, {DARK_BG}); padding:40px; border-radius:24px; color:white;">
                <p style="text-transform:uppercase; letter-spacing:0.1em; font-size:0.8rem; font-weight:700; opacity:0.7;">Pobjednik analize</p>
                <h1 style="margin:0; font-size:3.5rem;">{top['banka']}</h1>
                <div style="margin:20px 0; height:1px; background:rgba(255,255,255,0.1);"></div>
                <div style="display:flex; gap:40px;">
                    <div>
                        <p style="margin:0; opacity:0.6;">Kamatna stopa</p>
                        <h2 style="margin:0; color:{ACCENT};">{top['stopa']}% p.a.</h2>
                    </div>
                    <div>
                        <p style="margin:0; opacity:0.6;">Neto profit</p>
                        <h2 style="margin:0; color:{SUCCESS};">+{fmt(top['dobit'])}</h2>
                    </div>
                </div>
                <p style="margin-top:30px; font-style:italic; opacity:0.6; font-size:0.9rem;">
                    * {top['napomena']} Proračun uključuje {period} štednje.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown("#### Ostale banke")
            for r in rezultati[1:]:
                st.markdown(f"""
                <div style="background:white; padding:15px 25px; border-radius:16px; border:1px solid #e2e8f0; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <p style="margin:0; font-weight:700; color:{TEXT_MAIN};">{r['banka']}</p>
                        <p style="margin:0; font-size:0.8rem; color:#64748b;">Stopa: {r['stopa']}%</p>
                    </div>
                    <div style="text-align:right;">
                        <p style="margin:0; font-weight:700; color:{PRIMARY};">+{fmt(r['dobit'])}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with t2:
        st.markdown("<br>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(12, 5))
        names = [r["banka"].split()[0] for r in rezultati]
        profits = [r["dobit"] for r in rezultati]
        colors = [r["boja"] for r in rezultati]
        
        bars = ax.bar(names, profits, color=colors, alpha=0.8, edgecolor=DARK_BG, linewidth=0.5)
        ax.set_facecolor(LIGHT_GREY)
        fig.patch.set_facecolor(LIGHT_GREY)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_title("Neto dobit po bankama (KM)", pad=20, weight='bold', color=TEXT_MAIN)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{height:.2f}', ha='center', va='bottom', weight='bold')
            
        st.pyplot(fig)

    with t3:
        st.markdown("<br>", unsafe_allow_html=True)
        df_final = pd.DataFrame(rezultati)[["banka", "stopa", "dobit", "ukupno"]]
        df_final.columns = ["Banka", "Stopa (%)", "Neto Dobit (KM)", "Ukupno (KM)"]
        st.dataframe(df_final.style.highlight_max(axis=0, color='#dcfce7'), use_container_width=True)

# ═══════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════
st.markdown(f"""
<div style="margin-top:100px; padding:40px; text-align:center; border-top:1px solid #e2e8f0;">
    <p style="color:#64748b; font-size:0.85rem;">
        <b>Seminarski rad iz finansijske matematike</b><br>
        Podaci su informativnog karaktera i preuzeti su sa zvaničnih stranica banaka u BiH za 2024/25. godinu.
    </p>
</div>
""", unsafe_allow_html=True)