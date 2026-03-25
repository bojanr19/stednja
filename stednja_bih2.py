import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Finansijska Matematika – Kalkulator Depozita",
    page_icon="💰",
    layout="wide",
)

# ── Bank data (rates you provided) ───────────────────────────────────────────
BANKE = [
    {"naziv": "NLB Banka Banja Luka",         "1g": 3.10, "2g": 3.75, "3g": 4.25, "5g": 4.50},
    {"naziv": "UniCredit Bank Banja Luka",     "1g": 3.00, "2g": 3.60, "3g": 4.10, "5g": 4.35},
    {"naziv": "Komercijalna Banka Banja Luka", "1g": 2.90, "2g": 3.50, "3g": 3.95, "5g": 4.20},
    {"naziv": "Nova Banka",                    "1g": 2.85, "2g": 3.40, "3g": 3.85, "5g": 4.10},
    {"naziv": "Addiko Bank",                   "1g": 2.75, "2g": 3.30, "3g": 3.75, "5g": 4.00},
    {"naziv": "Sparkasse Bank",                "1g": 2.70, "2g": 3.20, "3g": 3.70, "5g": 3.95},
    {"naziv": "Raiffeisen Bank",               "1g": 2.65, "2g": 3.10, "3g": 3.60, "5g": 3.85},
    {"naziv": "Intesa Sanpaolo Banka",         "1g": 2.60, "2g": 3.00, "3g": 3.50, "5g": 3.75},
]

ROK_MAP = {"1 Godina": ("1g", 1), "2 Godine": ("2g", 2), "3 Godine": ("3g", 3), "5 Godina": ("5g", 5)}

def kamata_kljuc(rok_str):
    return ROK_MAP[rok_str][0]

def rok_godine(rok_str):
    return ROK_MAP[rok_str][1]

def izracunaj(iznos, godisnja_stopa, godine):
    finalni = iznos * (1 + godisnja_stopa / 100) ** godine
    zarada  = finalni - iznos
    prinos  = (zarada / iznos) * 100
    return finalni, zarada, prinos

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Source Serif 4', Georgia, serif;
    background: #fafaf8;
    color: #1a1a1a;
}
.stApp { background: #fafaf8; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── NAV ── */
.nav-bar {
    background: #fff;
    border-bottom: 2px solid #1a1a1a;
    padding: 14px 56px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0;
}
.nav-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    font-weight: 900;
    letter-spacing: -0.5px;
    color: #1a1a1a;
}
.nav-links { display: flex; gap: 32px; }
.nav-link {
    font-family: 'Source Serif 4', serif;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    color: #1a1a1a;
    text-decoration: none;
    font-weight: 400;
}

/* ── HERO ── */
.hero-wrap {
    padding: 52px 56px 40px;
    border-bottom: 1px solid #e0ddd8;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 40px;
    background: #fff;
}
.hero-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    color: #c0392b;
    text-transform: uppercase;
    margin-bottom: 14px;
    font-family: 'IBM Plex Mono', monospace;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -1.5px;
    color: #1a1a1a;
    margin: 0 0 18px 0;
}
.hero-divider {
    width: 56px; height: 3px;
    background: #c0392b;
    margin-bottom: 18px;
}
.hero-sub {
    font-style: italic;
    font-size: 1.05rem;
    color: #444;
    max-width: 540px;
    line-height: 1.6;
}

/* ── AT A GLANCE card ── */
.glance-card {
    border: 1.5px solid #e0ddd8;
    padding: 28px 32px;
    min-width: 230px;
    flex-shrink: 0;
    background: #fafaf8;
}
.glance-label {
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #888;
    font-family: 'IBM Plex Mono', monospace;
    margin-bottom: 16px;
}
.glance-divider { width: 32px; height: 2px; background: #c0392b; margin-bottom: 20px; }
.glance-item { margin-bottom: 18px; }
.glance-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 500;
    color: #c0392b;
    line-height: 1;
}
.glance-desc {
    font-size: 0.7rem;
    color: #888;
    letter-spacing: 0.06em;
    font-family: 'IBM Plex Mono', monospace;
    margin-top: 3px;
}

/* ── SECTIONS ── */
.section-wrap {
    padding: 44px 56px;
    border-bottom: 1px solid #e0ddd8;
    background: #fff;
    margin-top: 2px;
}
.section-header {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 10px;
}
.section-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.9rem;
    font-weight: 900;
    color: #c0392b;
    line-height: 1;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    text-decoration: underline;
    text-underline-offset: 5px;
    color: #1a1a1a;
}
.section-desc {
    font-size: 0.88rem;
    color: #555;
    margin: 10px 0 28px 0;
    line-height: 1.6;
}

/* ── Input labels ── */
.input-label {
    font-size: 0.7rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace;
    color: #333;
    margin-bottom: 6px;
    font-weight: 500;
}
.input-hint {
    font-size: 0.73rem;
    color: #888;
    margin-top: 5px;
    font-family: 'IBM Plex Mono', monospace;
}

/* ── Stickers (quick amounts) ── */
.sticker-row { display: flex; gap: 10px; margin-top: 14px; flex-wrap: wrap; }
.sticker {
    border: 1.5px solid #ccc;
    background: #fff;
    padding: 5px 16px;
    font-size: 0.78rem;
    font-family: 'IBM Plex Mono', monospace;
    cursor: pointer;
    transition: all 0.15s;
}
.sticker:hover { border-color: #1a1a1a; background: #1a1a1a; color: #fff; }

/* ── Term pills ── */
.pill-group { display: flex; gap: 2px; }
.pill {
    padding: 10px 22px;
    border: 1.5px solid #ccc;
    background: #fff;
    font-size: 0.82rem;
    font-family: 'IBM Plex Mono', monospace;
    cursor: pointer;
    transition: all 0.15s;
}
.pill-active { border-color: #c0392b; border-width: 2px; color: #c0392b; font-weight: 600; }

/* ── Checkbox legend ── */
.legend-row { display: flex; align-items: center; gap: 10px; margin-top: 14px; }
.legend-box { width: 14px; height: 14px; background: #c0392b; flex-shrink: 0; }
.legend-text { font-size: 0.78rem; color: #444; font-family: 'IBM Plex Mono', monospace; }

/* ── RECOMMENDED BANK ── */
.rec-wrap {
    border: 1.5px solid #e0ddd8;
    padding: 28px 36px;
    background: #fafaf8;
    display: flex;
    justify-content: space-between;
    align-items: stretch;
    gap: 40px;
    flex-wrap: wrap;
}
.rec-left { min-width: 220px; }
.rec-badge {
    font-size: 0.65rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #888;
    font-family: 'IBM Plex Mono', monospace;
    margin-bottom: 8px;
}
.rec-badge-divider { width: 32px; height: 2px; background: #c0392b; margin-bottom: 14px; }
.rec-bank {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #1a1a1a;
    line-height: 1.1;
    margin-bottom: 12px;
}
.rec-rate-row { display: flex; gap: 40px; }
.rec-rate {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    font-weight: 500;
    color: #c0392b;
}
.rec-rate-label { font-size: 0.7rem; color: #888; font-family: 'IBM Plex Mono', monospace; margin-top: 2px; }
.rec-right { flex: 1; min-width: 260px; }
.rec-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px 32px; }
.rec-stat-label {
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #888;
    font-family: 'IBM Plex Mono', monospace;
    margin-bottom: 4px;
}
.rec-stat-divider { width: 100%; height: 1px; background: #e0ddd8; margin-bottom: 8px; }
.rec-stat-val {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #1a1a1a;
}
.rec-stat-val-red {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #c0392b;
}
.rec-yield-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.5rem;
    font-weight: 500;
    color: #c0392b;
}

/* ── TABLE ── */
.comp-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 18px;
    font-size: 0.85rem;
}
.comp-table th {
    text-align: left;
    padding: 10px 14px;
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace;
    color: #555;
    border-top: 1.5px solid #1a1a1a;
    border-bottom: 1.5px solid #1a1a1a;
    background: #fafaf8;
}
.comp-table td {
    padding: 13px 14px;
    border-bottom: 1px solid #e0ddd8;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: #333;
}
.comp-table tr:first-child td { font-weight: 600; }
.rank-1 { color: #c0392b; font-weight: 700 !important; }
.highlight-red { color: #c0392b !important; font-weight: 600 !important; }
.highlight-rate { color: #c0392b !important; font-weight: 600 !important; }

/* ── FOOTER ── */
.footer-bar {
    padding: 16px 56px;
    border-top: 1px solid #e0ddd8;
    display: flex;
    justify-content: space-between;
    background: #fff;
    margin-top: 2px;
}
.footer-text { font-size: 0.72rem; color: #888; font-family: 'IBM Plex Mono', monospace; }

/* ── Streamlit widget overrides ── */
div[data-testid="stNumberInput"] input {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.15rem !important;
    border: 1.5px solid #ccc !important;
    border-radius: 0 !important;
    padding: 14px 16px !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: #1a1a1a !important;
    box-shadow: none !important;
}
.stRadio > div { flex-direction: row !important; gap: 0 !important; }
.stRadio label {
    border: 1.5px solid #ccc;
    padding: 9px 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    cursor: pointer;
    margin: 0 !important;
    background: #fff;
    transition: all 0.15s;
}
div[data-testid="stButton"] button {
    background: #c0392b !important;
    color: #fff !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'Source Serif 4', serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    padding: 16px 32px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: background 0.15s !important;
}
div[data-testid="stButton"] button:hover {
    background: #96281b !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "iznos" not in st.session_state:
    st.session_state.iznos = 10000.0
if "rok" not in st.session_state:
    st.session_state.rok = "3 Godine"

# ── NAV ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
  <div class="nav-logo">Finansijska Matematika</div>
  <div class="nav-links">
    <span class="nav-link">Pregled</span>
    <span class="nav-link">Kalkulator</span>
    <span class="nav-link">Metodologija</span>
    <span class="nav-link">Reference</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div>
    <div class="hero-label">Seminarski rad – Finansijska analiza</div>
    <h1 class="hero-title">Optimalni Štedni<br>Depoziti u Republici<br>Srpskoj</h1>
    <div class="hero-divider"></div>
    <p class="hero-sub">Interaktivni alat za izračunavanje složene kamate u regionalnim bankama,
    uz identifikaciju najpovoljnijih uslova depozita za vaš investicioni horizont.</p>
  </div>
  <div class="glance-card">
    <div class="glance-label">Na prvi pogled</div>
    <div class="glance-divider"></div>
    <div class="glance-item">
      <div class="glance-num">8</div>
      <div class="glance-desc">analiziranih banaka</div>
    </div>
    <div class="glance-item">
      <div class="glance-num">4,50%</div>
      <div class="glance-desc">najviša godišnja stopa</div>
    </div>
    <div class="glance-item">
      <div class="glance-num">2024</div>
      <div class="glance-desc">podaci ažurirani</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION I – Parameters
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-wrap">
  <div class="section-header">
    <span class="section-num">I</span>
    <span class="section-title">Unesite Parametre</span>
  </div>
  <p class="section-desc">
    Unesite iznos depozita u BAM (Konvertibilne marke) i odaberite željeni period štednje.
    Kalkulator primjenjuje složenu kamatu sa godišnjom kapitalizacijom.
  </p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div style="padding: 0 56px 32px; background:#fff; border-bottom:1px solid #e0ddd8;">', unsafe_allow_html=True)

    col_iznos, col_rok, col_btn = st.columns([3, 3, 2])

    with col_iznos:
        st.markdown('<div class="input-label">Iznos depozita (BAM)</div>', unsafe_allow_html=True)
        iznos = st.number_input(
            "", min_value=500.0, max_value=1_000_000.0,
            value=st.session_state.iznos, step=500.0,
            format="%.2f", label_visibility="collapsed", key="num_input"
        )
        st.session_state.iznos = iznos
        st.markdown('<div class="input-hint">Minimum: 500 BAM. Maksimum: 1.000.000 BAM</div>', unsafe_allow_html=True)

        # Quick amount buttons
        st.markdown('<div class="sticker-row">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        for col, val in zip([c1, c2, c3, c4], [1000, 5000, 10000, 50000]):
            if col.button(f"{val:,}".replace(",", "."), key=f"btn_{val}"):
                st.session_state.iznos = float(val)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_rok:
        st.markdown('<div class="input-label">Rok štednje</div>', unsafe_allow_html=True)
        rok = st.radio(
            "", list(ROK_MAP.keys()),
            index=list(ROK_MAP.keys()).index(st.session_state.rok),
            horizontal=True, label_visibility="collapsed", key="radio_rok"
        )
        st.session_state.rok = rok
        st.markdown('<div class="input-hint">Duži rokovi tipično nude više kamatne stope, ali manju likvidnost.</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="legend-row">
          <div class="legend-box"></div>
          <div class="legend-text">Složena kamata sa godišnjom kapitalizacijom</div>
        </div>""", unsafe_allow_html=True)

    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        izracunaj_btn = st.button("Izračunaj Optimalni Depozit", key="calc_btn")
        st.markdown('<div class="input-hint" style="text-align:center;margin-top:8px;">Rezultati se ažuriraju automatski na osnovu tekućih bankarskih stopa</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# Compute results
# ══════════════════════════════════════════════════════════════════════════════
kljuc = kamata_kljuc(st.session_state.rok)
godine = rok_godine(st.session_state.rok)
iznos_val = st.session_state.iznos

rezultati = []
for b in BANKE:
    stopa = b[kljuc]
    fin, zar, prinos = izracunaj(iznos_val, stopa, godine)
    rezultati.append({**b, "finalni": fin, "zarada": zar, "prinos": prinos, "stopa": stopa})
rezultati.sort(key=lambda x: x["finalni"], reverse=True)
best = rezultati[0]

# ══════════════════════════════════════════════════════════════════════════════
# SECTION II – Recommended Bank
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="section-wrap">
  <div class="section-header">
    <span class="section-num">II</span>
    <span class="section-title">Preporučena Banka</span>
  </div>
</div>
<div style="padding: 0 56px 32px; background:#fff; border-bottom:1px solid #e0ddd8;">
  <div class="rec-wrap">
    <div class="rec-left">
      <div class="rec-badge">Najviši prinos na vaš depozit</div>
      <div class="rec-badge-divider"></div>
      <div class="rec-bank">{best['naziv']}</div>
      <div class="rec-rate-row">
        <div>
          <div class="rec-rate">{best['stopa']:.2f}%</div>
          <div class="rec-rate-label">godišnja stopa</div>
        </div>
        <div>
          <div class="rec-rate">{best['zarada']:,.2f} BAM</div>
          <div class="rec-rate-label">ukupna kamata</div>
        </div>
      </div>
    </div>
    <div class="rec-right">
      <div class="rec-grid">
        <div>
          <div class="rec-stat-label">Vaš depozit</div>
          <div class="rec-stat-divider"></div>
          <div class="rec-stat-val">{iznos_val:,.0f} BAM</div>
        </div>
        <div>
          <div class="rec-stat-label">Odabrani rok</div>
          <div class="rec-stat-divider"></div>
          <div class="rec-stat-val">{st.session_state.rok}</div>
        </div>
        <div>
          <div class="rec-stat-label">Finalni saldo</div>
          <div class="rec-stat-divider"></div>
          <div class="rec-stat-val-red">{best['finalni']:,.2f} BAM</div>
        </div>
        <div>
          <div class="rec-stat-label">Efektivni prinos</div>
          <div class="rec-stat-divider"></div>
          <div class="rec-yield-val">+{best['prinos']:.2f}%</div>
        </div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION III – Bank Comparison Table
# ══════════════════════════════════════════════════════════════════════════════
rows_html = ""
for i, b in enumerate(rezultati):
    rank = i + 1
    rank_class = "rank-1" if rank == 1 else ""
    rate_class = "highlight-rate" if rank == 1 else ""
    int_class = "highlight-red" if rank == 1 else ""

    rows_html += f"""
    <tr>
      <td class="{rank_class}">{rank}</td>
      <td class="{rank_class}">{b['naziv']}</td>
      <td>{'<span class="highlight-rate">' if rank==1 else ''}{b['1g']:.2f}%{'</span>' if rank==1 else ''}</td>
      <td>{'<span class="highlight-rate">' if rank==1 else ''}{b['2g']:.2f}%{'</span>' if rank==1 else ''}</td>
      <td>{'<span class="highlight-rate">' if rank==1 else ''}{b['3g']:.2f}%{'</span>' if rank==1 else ''}</td>
      <td>{'<span class="highlight-rate">' if rank==1 else ''}{b['5g']:.2f}%{'</span>' if rank==1 else ''}</td>
      <td class="{int_class}">{b['zarada']:,.2f} BAM</td>
    </tr>"""

st.markdown(f"""
<div class="section-wrap">
  <div class="section-header">
    <span class="section-num">III</span>
    <span class="section-title">Poređenje Banaka</span>
  </div>
  <table class="comp-table">
    <thead>
      <tr>
        <th>Rang</th>
        <th>Naziv banke</th>
        <th>1 Godina</th>
        <th>2 Godine</th>
        <th>3 Godine</th>
        <th>5 Godina</th>
        <th>Kamata ({st.session_state.rok.lower()})</th>
      </tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-bar">
  <div class="footer-text">Seminarski rad – Finansijska matematika, Univerzitet u Banjoj Luci, 2024.</div>
  <div class="footer-text">Izvori podataka: Zvanične publikacije banaka o kamatnim stopama</div>
</div>
""", unsafe_allow_html=True)
