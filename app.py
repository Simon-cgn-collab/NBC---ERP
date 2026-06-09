import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import base64, os

st.set_page_config(
    page_title="NBC ERP",
    page_icon="🍹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load assets ───────────────────────────────────────────────────
def load_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

BASE = os.path.dirname(__file__)
LOGO_B64  = load_b64(os.path.join(BASE, "logo.png"))
KRUSH_B64 = load_b64(os.path.join(BASE, "krush_hero.jpg"))

# ── Palette NBC minimaliste ───────────────────────────────────────
# Fond : #F7F7F5  Cards : #FFFFFF  Texte : #1A1A1A  Gris : #6B7280
# Bordures : #E5E5E3  Accent noir : #1A1A1A  Vert OK : #16A34A  Rouge : #DC2626

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {{ box-sizing: border-box; }}

/* ── Global ── */
.stApp {{
    background-color: #F7F7F5;
    font-family: 'Inter', sans-serif;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: #FFFFFF !important;
    border-right: 1px solid #E5E5E3 !important;
}}
[data-testid="stSidebar"] * {{ font-family: 'Inter', sans-serif !important; }}
[data-testid="stSidebarContent"] {{ padding: 0 !important; }}

/* ── Radio nav ── */
[data-testid="stSidebar"] .stRadio > div {{ gap: 2px !important; }}
[data-testid="stSidebar"] .stRadio label {{
    background: transparent !important;
    border-radius: 6px !important;
    padding: 9px 12px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #1A1A1A !important;
    transition: background 0.12s ease;
    cursor: pointer;
    border: none !important;
    margin: 1px 6px !important;
    width: calc(100% - 12px) !important;
    letter-spacing: 0.01em !important;
    opacity: 1 !important;
}}
[data-testid="stSidebar"] .stRadio label p,
[data-testid="stSidebar"] .stRadio label span,
[data-testid="stSidebar"] .stRadio label div {{
    color: #1A1A1A !important;
    opacity: 1 !important;
}}
[data-testid="stSidebar"] .stRadio label:hover {{
    background: #F1F0EF !important;
    color: #1A1A1A !important;
}}
[data-testid="stSidebar"] [aria-checked="true"] + label,
[data-testid="stSidebar"] .stRadio label[data-selected="true"] {{
    background: #E9E9E7 !important;
    color: #1A1A1A !important;
    font-weight: 600 !important;
    border-left: none !important;
}}
[data-testid="stSidebar"] .stRadio > div > label > div:first-child {{
    display: none !important;
}}

/* ── Metrics ── */
[data-testid="metric-container"] {{
    background: #FFFFFF !important;
    border: 1px solid #E5E5E3 !important;
    border-radius: 10px !important;
    padding: 18px !important;
    box-shadow: none !important;
}}
[data-testid="stMetricLabel"] {{ color: #6B7280 !important; font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.06em; }}
[data-testid="stMetricValue"] {{ color: #1A1A1A !important; font-size: 26px !important; font-weight: 700 !important; font-family: 'Inter', sans-serif !important; }}
[data-testid="stMetricDelta"] {{ font-size: 11px !important; }}

/* ── Titles ── */
h1, h2, h3 {{ font-family: 'Inter', sans-serif !important; }}
h1 {{ color: #1A1A1A !important; font-weight: 700 !important; font-size: 22px !important; }}
h2 {{ color: #374151 !important; font-weight: 600 !important; font-size: 16px !important; }}
h3 {{ color: #6B7280 !important; font-weight: 600 !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 0.08em; }}

/* ── Buttons ── */
.stButton > button {{
    background: #1A1A1A !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 7px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 9px 20px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.15s !important;
    box-shadow: none !important;
}}
.stButton > button:hover {{
    background: #374151 !important;
    transform: none !important;
}}

/* ── Dataframes ── */
.stDataFrame {{
    border-radius: 8px !important;
    overflow: hidden !important;
    border: 1px solid #E5E5E3 !important;
}}
[data-testid="stDataFrameResizable"] {{
    background: #FFFFFF !important;
}}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {{
    background: #FFFFFF !important;
    border: 1px solid #E5E5E3 !important;
    border-radius: 7px !important;
    color: #1A1A1A !important;
    font-family: 'Inter', sans-serif !important;
}}
.stSelectbox > div > div {{ color: #1A1A1A !important; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: #FFFFFF;
    border-radius: 8px;
    padding: 3px;
    gap: 2px;
    border: 1px solid #E5E5E3;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent;
    color: #6B7280;
    border-radius: 6px;
    font-weight: 500;
    font-size: 13px;
    padding: 7px 16px;
}}
.stTabs [aria-selected="true"] {{
    background: #1A1A1A !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
}}

/* ── Alerts ── */
.stAlert {{ border-radius: 8px !important; border: none !important; }}

/* ── Divider ── */
hr {{ border-color: #E5E5E3 !important; margin: 16px 0 !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: #F7F7F5; }}
::-webkit-scrollbar-thumb {{ background: #D1D5DB; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: #9CA3AF; }}

/* ── Cards ── */
.nbc-card {{
    background: #FFFFFF;
    border: 1px solid #E5E5E3;
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 10px;
    transition: border-color 0.15s;
}}
.nbc-card:hover {{ border-color: #9CA3AF; }}

.nbc-card-header {{
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6B7280;
    margin-bottom: 10px;
}}

/* ── Kanban cards ── */
.phase-col {{
    background: #F7F7F5;
    border-radius: 8px;
    padding: 10px;
    border: 1px solid #E5E5E3;
    min-height: 200px;
}}
.prospect-card {{
    background: #FFFFFF;
    border-radius: 7px;
    padding: 11px;
    margin-bottom: 7px;
    border-left: 2px solid #1A1A1A;
    border: 1px solid #E5E5E3;
    border-left: 2px solid #1A1A1A;
    transition: box-shadow 0.15s;
}}
.prospect-card:hover {{ box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}

/* ── Badges rôle ── */
.badge-admin {{
    background: #1A1A1A;
    color: #FFFFFF;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}}
.badge-com {{
    background: #F1F0EF;
    color: #374151;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border: 1px solid #E5E5E3;
}}

/* ── Stock bars ── */
.stock-bar-wrap {{
    background: #F1F0EF;
    border-radius: 3px;
    height: 5px;
    margin-top: 6px;
}}
.stock-bar-fill {{ height: 5px; border-radius: 3px; transition: width 0.4s; }}

/* ── Section label ── */
.section-label {{
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #9CA3AF;
    margin-bottom: 12px;
    padding-left: 1px;
}}

/* ── Login ── */
.login-wrap {{
    max-width: 420px;
    margin: 60px auto;
}}
.login-card {{
    background: #FFFFFF;
    border: 1px solid #E5E5E3;
    border-radius: 12px;
    padding: 36px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}}

/* ── Sidebar déconnexion ── */
[data-testid="stSidebar"] .stButton > button {{
    background: transparent !important;
    color: #9CA3AF !important;
    border: 1px solid #E5E5E3 !important;
    border-radius: 6px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    padding: 7px 14px !important;
    margin: 0 6px !important;
    width: calc(100% - 12px) !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: #F1F0EF !important;
    color: #374151 !important;
    transform: none !important;
}}

</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  DATA
# ══════════════════════════════════════════════════════════════════
PROSPECTS = pd.DataFrame([
    {"Établissement":"NENI Paris",           "Type":"Restaurant",  "Produit":"Krush",    "Phase":"CONTACT ÉTABLI",   "Date":"09/06/2026","Email":"contact@neni.fr",                "Relance":"J+5"},
    {"Établissement":"Le Perchoir",          "Type":"Rooftop",     "Produit":"Krush",    "Phase":"CONTACT ÉTABLI",   "Date":"09/06/2026","Email":"menilmontant@leperchoir.fr",     "Relance":"J+5"},
    {"Établissement":"Terrass Hotel",        "Type":"Hôtel",       "Produit":"Krush",    "Phase":"PRÉSENTATION",     "Date":"05/06/2026","Email":"commercial@terrass-hotel.com",   "Relance":"J+11"},
    {"Établissement":"Rosa Bonheur",         "Type":"Guinguette",  "Produit":"Krush",    "Phase":"CONTACT ÉTABLI",   "Date":"09/06/2026","Email":"info@rosabonheur.fr",            "Relance":"J+5"},
    {"Établissement":"Mama Shelter",         "Type":"Rooftop",     "Produit":"Krush",    "Phase":"NÉGOCIATION",      "Date":"01/06/2026","Email":"food.pariseast@mamashelter.com", "Relance":"J+15"},
    {"Établissement":"La Bellevilloise",     "Type":"Rooftop Bar", "Produit":"Krush",    "Phase":"CONTACT ÉTABLI",   "Date":"09/06/2026","Email":"contact@labellevilloise.com",   "Relance":"J+5"},
    {"Établissement":"Holiday Inn Elysées", "Type":"Hôtel",       "Produit":"Krush",    "Phase":"PRÉSENTATION",     "Date":"03/06/2026","Email":"fnb@hiparisely.com",             "Relance":"J+9"},
    {"Établissement":"Café Odessa",          "Type":"Café",        "Produit":"Krush",    "Phase":"PRISE DE CONTACT", "Date":"09/06/2026","Email":"contact@cafe-odessa.fr",         "Relance":"J+5"},
    {"Établissement":"Bar du Marché",        "Type":"Bar",         "Produit":"Krush",    "Phase":"CLIENT ✓",         "Date":"20/05/2026","Email":"contact@bardumarche.fr",         "Relance":"—"},
    {"Établissement":"Hotel Lutetia",        "Type":"Hôtel",       "Produit":"Samaï",    "Phase":"NÉGOCIATION",      "Date":"28/05/2026","Email":"fb@lutetia.com",                 "Relance":"J+18"},
    {"Établissement":"Caviste du Temple",    "Type":"Caviste",     "Produit":"Kingdom",  "Phase":"PRISE DE CONTACT", "Date":"07/06/2026","Email":"bonjour@caviste-temple.fr",      "Relance":"J+7"},
    {"Établissement":"Brasserie Lipp",       "Type":"Restaurant",  "Produit":"Indochine","Phase":"CLIENT ✓",         "Date":"15/05/2026","Email":"contact@brasserie-lipp.fr",      "Relance":"—"},
    {"Établissement":"Café des Marronniers", "Type":"Café",        "Produit":"Krush",    "Phase":"CONTACT ÉTABLI",   "Date":"09/06/2026","Email":"—",                             "Relance":"J+5"},
    {"Établissement":"Skyline Bar",          "Type":"Rooftop",     "Produit":"Krush",    "Phase":"PRISE DE CONTACT", "Date":"08/06/2026","Email":"@skylinebarparis",              "Relance":"J+6"},
    {"Établissement":"L'Imprimerie Hotel",   "Type":"Hôtel",       "Produit":"Krush",    "Phase":"CONTACT ÉTABLI",   "Date":"09/06/2026","Email":"resa@limprimeriehotel.com",      "Relance":"J+5"},
])

STOCKS = pd.DataFrame([
    {"SKU":"Krush Lime Ginger 33cl",        "Stock":142,"Seuil":50, "Statut":"OK"},
    {"SKU":"Krush Yuzu Peach 33cl",         "Stock":38, "Seuil":50, "Statut":"ALERTE"},
    {"SKU":"Krush Mango Passion 33cl",      "Stock":87, "Seuil":50, "Statut":"OK"},
    {"SKU":"Krush Raspberry Jasmin 0%",     "Stock":54, "Seuil":40, "Statut":"OK"},
    {"SKU":"Samaï Rum Original 70cl",       "Stock":21, "Seuil":30, "Statut":"ALERTE"},
    {"SKU":"Kingdom Pilsner 33cl",          "Stock":210,"Seuil":80, "Statut":"OK"},
    {"SKU":"Kingdom IPA 33cl",              "Stock":178,"Seuil":80, "Statut":"OK"},
    {"SKU":"Kingdom IPA Mangue 33cl",       "Stock":44, "Seuil":60, "Statut":"WARNING"},
    {"SKU":"Indochine Blanche Poivre 33cl", "Stock":96, "Seuil":60, "Statut":"OK"},
    {"SKU":"Wingman Lager 33cl",            "Stock":12, "Seuil":40, "Statut":"ALERTE"},
])

FACTURES = pd.DataFrame([
    {"N°":"NBC-2026-0012","Client":"Brasserie Lipp",  "Produit":"Indochine","HT":"480 €","TTC":"576 €","Date":"09/06/2026","Statut":"✅ Payée"},
    {"N°":"NBC-2026-0011","Client":"Bar du Marché",   "Produit":"Krush",    "HT":"240 €","TTC":"288 €","Date":"07/06/2026","Statut":"⏳ En attente"},
    {"N°":"NBC-2026-0010","Client":"Brasserie Lipp",  "Produit":"Indochine","HT":"480 €","TTC":"576 €","Date":"01/06/2026","Statut":"✅ Payée"},
    {"N°":"NBC-2026-0009","Client":"Cave Legrand",    "Produit":"Kingdom",  "HT":"360 €","TTC":"432 €","Date":"28/05/2026","Statut":"✅ Payée"},
    {"N°":"NBC-2026-0008","Client":"Bar du Marché",   "Produit":"Krush",    "HT":"200 €","TTC":"240 €","Date":"20/05/2026","Statut":"🔴 En retard"},
])

EMAILS = pd.DataFrame([
    {"Date":"09/06/2026","Destinataire":"NENI Paris",     "Type":"1er contact","Produit":"Krush",   "Statut":"✅ Envoyé"},
    {"Date":"09/06/2026","Destinataire":"Le Perchoir",    "Type":"1er contact","Produit":"Krush",   "Statut":"✅ Envoyé"},
    {"Date":"09/06/2026","Destinataire":"Rosa Bonheur",   "Type":"1er contact","Produit":"Krush",   "Statut":"✅ Envoyé"},
    {"Date":"05/06/2026","Destinataire":"Terrass Hotel",  "Type":"Relance J+7","Produit":"Krush",   "Statut":"✅ Envoyé"},
    {"Date":"03/06/2026","Destinataire":"Holiday Inn",    "Type":"Relance J+7","Produit":"Krush",   "Statut":"✅ Envoyé"},
    {"Date":"01/06/2026","Destinataire":"Mama Shelter",   "Type":"Relance J+14","Produit":"Krush",  "Statut":"✅ Envoyé"},
    {"Date":"28/05/2026","Destinataire":"Hotel Lutetia",  "Type":"1er contact","Produit":"Samaï",   "Statut":"✅ Envoyé"},
    {"Date":"07/06/2026","Destinataire":"Rapport hebdo",  "Type":"Rapport auto","Produit":"—",      "Statut":"✅ Envoyé"},
])

PHASE_COLORS = {
    "PRISE DE CONTACT": ("#9CA3AF", "#F9F9F8"),
    "CONTACT ÉTABLI":   ("#6B7280", "#F4F4F3"),
    "PRÉSENTATION":     ("#374151", "#EFEFED"),
    "NÉGOCIATION":      ("#1A1A1A", "#E9E9E7"),
    "CLIENT ✓":         ("#16A34A", "#F0FDF4"),
}

# ── Helpers ──────────────────────────────────────────────────────
def sidebar_logo():
    st.markdown(f"""
    <div style='padding:20px 18px 10px 18px;'>
        <div style='display:flex; align-items:center; gap:10px;'>
            <img src='data:image/png;base64,{LOGO_B64}'
                 style='width:34px; height:34px; object-fit:contain; border-radius:6px; background:#1A1A1A; padding:4px;'/>
            <div>
                <div style='font-size:13px; font-weight:700; color:#1A1A1A; letter-spacing:0.01em; line-height:1.2;'>NBC ERP</div>
                <div style='font-size:10px; color:#9CA3AF; font-weight:500; letter-spacing:0.05em; text-transform:uppercase;'>Internal platform</div>
            </div>
        </div>
    </div>
    <div style='height:1px; background:#E5E5E3; margin:10px 12px 4px 12px;'></div>
    """, unsafe_allow_html=True)

def user_badge(role, name):
    icon = "◆" if role == "admin" else "○"
    label = "Admin" if role == "admin" else "Commercial"
    st.markdown(f"""
    <div style='padding:8px 18px 12px 18px;'>
        <div style='display:flex; align-items:center; gap:9px;'>
            <div style='width:28px;height:28px;border-radius:50%;background:#1A1A1A;display:flex;align-items:center;justify-content:center;font-size:11px;color:#FFFFFF;font-weight:700;flex-shrink:0;'>{icon}</div>
            <div>
                <div style='font-size:13px;font-weight:600;color:#1A1A1A;line-height:1.2;'>{name.split()[0]}</div>
                <div style='font-size:11px;color:#9CA3AF;font-weight:400;'>{label}</div>
            </div>
        </div>
    </div>
    <div style='height:1px; background:#E5E5E3; margin:0 12px 8px 12px;'></div>
    """, unsafe_allow_html=True)

def page_header(title, subtitle=""):
    st.markdown(f"""
    <div style='margin-bottom:20px; padding-bottom:16px; border-bottom:1px solid #E5E5E3;'>
        <h1 style='margin:0; font-size:20px !important; font-weight:700 !important; color:#1A1A1A !important;'>{title}</h1>
        {"<p style='margin:4px 0 0 0; color:#9CA3AF; font-size:12px; font-weight:400;'>"+subtitle+"</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)

def card(content, title=""):
    header = f"<div class='nbc-card-header'>{title}</div>" if title else ""
    st.markdown(f"<div class='nbc-card'>{header}{content}</div>", unsafe_allow_html=True)

def metric_card(label, value, delta="", delta_good=True):
    delta_color = "#16A34A" if delta_good else "#DC2626"
    delta_html = f"<div style='font-size:11px;color:{delta_color};margin-top:3px;font-weight:500;'>{delta}</div>" if delta else ""
    return f"""
    <div class='nbc-card' style='text-align:center; padding:16px;'>
        <div style='font-size:10px;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.08em;font-weight:600;'>{label}</div>
        <div style='font-size:26px;font-weight:700;color:#1A1A1A;margin:8px 0 2px 0;'>{value}</div>
        {delta_html}
    </div>"""

# ── Plotly theme ─────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#6B7280", family="Inter"),
    showlegend=False,
    margin=dict(t=24, b=0, l=0, r=0),
    xaxis=dict(tickfont=dict(color="#9CA3AF"), gridcolor="#F1F0EF"),
    yaxis=dict(tickfont=dict(color="#9CA3AF"), showgrid=True, gridcolor="#F1F0EF"),
)

# ══════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""

# ══════════════════════════════════════════════════════════════════
#  LOGIN
# ══════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='text-align:center; margin-bottom:28px;'>
            <img src='data:image/png;base64,{LOGO_B64}'
                 style='width:80px; margin-bottom:14px; border-radius:8px; background:#1A1A1A; padding:8px;'/>
            <p style='color:#9CA3AF; font-size:12px; letter-spacing:0.08em; text-transform:uppercase; font-weight:500; margin:0;'>
                Natural Beverages Company
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        with st.form("login"):
            st.markdown("<p style='color:#9CA3AF;font-size:11px;text-transform:uppercase;letter-spacing:0.08em;font-weight:600;margin-bottom:14px;'>Connexion</p>", unsafe_allow_html=True)
            username = st.text_input("", placeholder="Identifiant", label_visibility="collapsed")
            password = st.text_input("", placeholder="Mot de passe", type="password", label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Connexion →", use_container_width=True)
            if submit:
                if username == "simon" and password == "krush2026":
                    st.session_state.logged_in = True
                    st.session_state.role = "commercial"
                    st.session_state.username = "Simon Cogné"
                    st.rerun()
                elif username == "admin" and password == "nbc2026":
                    st.session_state.logged_in = True
                    st.session_state.role = "admin"
                    st.session_state.username = "Direction NBC"
                    st.rerun()
                else:
                    st.error("Identifiants incorrects")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <p style='text-align:center;color:#D1D5DB;font-size:11px;margin-top:16px;'>
            demo · simon / krush2026 &nbsp;|&nbsp; admin / nbc2026
        </p>
        """, unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    sidebar_logo()
    user_badge(st.session_state.role, st.session_state.username)

    if st.session_state.role == "commercial":
        pages = ["🏠  Accueil", "🤝  CRM Pipeline", "📧  Emails", "📅  Mes relances"]
    else:
        pages = ["🏠  Accueil", "🤝  CRM Pipeline", "📧  Emails", "📦  Stocks",
                 "🧾  Facturation", "💰  Compta", "📊  Rapport semaine", "⚙️  Paramètres"]

    st.markdown("<div style='padding:0 6px; color:#9CA3AF; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin: 4px 12px 4px 12px;'>Navigation</div>", unsafe_allow_html=True)
    st.markdown("<div style='padding:0 6px;'>", unsafe_allow_html=True)
    page = st.radio("", pages, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1px;background:#E5E5E3;margin:12px 12px 8px 12px;'></div>", unsafe_allow_html=True)
    if st.button("← Déconnexion", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ══════════════════════════════════════════════════════════════════
#  PAGE : ACCUEIL
# ══════════════════════════════════════════════════════════════════
if "Accueil" in page:
    # Header sobre avec logo et date
    st.markdown(f"""
    <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;padding-bottom:16px;border-bottom:1px solid #E5E5E3;'>
        <div>
            <h1 style='margin:0;font-size:20px !important;font-weight:700 !important;color:#1A1A1A !important;'>
                Bonjour, {st.session_state.username.split()[0]}
            </h1>
            <p style='margin:4px 0 0 0;color:#9CA3AF;font-size:12px;'>Natural Beverages Company · Tableau de bord</p>
        </div>
        <div style='text-align:right;'>
            <div style='font-size:12px;font-weight:600;color:#374151;'>{date.today().strftime("%d %B %Y")}</div>
            <div style='font-size:11px;color:#9CA3AF;'>{date.today().strftime("%A")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.role == "commercial":
        cols = st.columns(4)
        metrics = [
            ("Prospects actifs","15","+3 cette semaine",True),
            ("Relances dues","6","cette semaine",True),
            ("Emails envoyés","23","ce mois",True),
            ("Nouveaux clients","2","ce mois",True),
        ]
        for col, (label, val, delta, good) in zip(cols, metrics):
            with col:
                st.markdown(metric_card(label, val, delta, good), unsafe_allow_html=True)

        st.markdown("<div class='section-label' style='margin-top:24px;'>Relances cette semaine</div>", unsafe_allow_html=True)
        rel = PROSPECTS[PROSPECTS["Relance"] != "—"][["Établissement","Type","Produit","Phase","Date","Relance"]]
        st.dataframe(rel, use_container_width=True, hide_index=True,
                     column_config={"Relance": st.column_config.TextColumn(width="small")})

    else:
        cols = st.columns(4)
        metrics = [
            ("CA du mois","4 320 €","+12% vs mai",True),
            ("Prospects actifs","15","+3 cette semaine",True),
            ("Factures en attente","2","528 €",None),
            ("Stocks en alerte","3","SKUs critiques",False),
        ]
        for col, (label, val, delta, good) in zip(cols, metrics):
            with col:
                ok = good if good is not None else True
                st.markdown(metric_card(label, val, delta, ok), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown("<div class='section-label'>Stocks critiques</div>", unsafe_allow_html=True)
            alertes = STOCKS[STOCKS["Statut"] != "OK"][["SKU","Stock","Seuil","Statut"]]
            st.dataframe(alertes, use_container_width=True, hide_index=True)

            st.markdown("<div class='section-label' style='margin-top:20px;'>CA mensuel 2026</div>", unsafe_allow_html=True)
            ca = pd.DataFrame({"Mois":["Fév","Mar","Avr","Mai","Juin"],"CA":[1200,2100,2800,3860,4320]})
            fig = px.bar(ca, x="Mois", y="CA", color_discrete_sequence=["#1A1A1A"], text="CA")
            fig.update_traces(texttemplate="%{text:,} €", textposition="outside", marker_line_width=0)
            fig.update_layout(**PLOT_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            st.markdown("<div class='section-label'>Dernières factures</div>", unsafe_allow_html=True)
            st.dataframe(FACTURES[["N°","Client","TTC","Statut"]].head(4), use_container_width=True, hide_index=True)

            st.markdown("<div class='section-label' style='margin-top:20px;'>Répartition CA par marque</div>", unsafe_allow_html=True)
            ca_m = pd.DataFrame({"Marque":["Krush","Kingdom","Indochine","Samaï","Wingman"],"CA":[6800,3200,2400,1400,480]})
            fig2 = px.pie(ca_m, values="CA", names="Marque",
                          color_discrete_sequence=["#1A1A1A","#374151","#6B7280","#9CA3AF","#D1D5DB"],
                          hole=0.5)
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font=dict(color="#6B7280", family="Inter"), showlegend=True,
                               legend=dict(font=dict(color="#374151", size=11)),
                               margin=dict(t=10,b=10,l=0,r=0))
            fig2.update_traces(textinfo="percent", textfont=dict(color="white"))
            st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : CRM PIPELINE
# ══════════════════════════════════════════════════════════════════
elif "CRM" in page:
    page_header("CRM Pipeline", f"{len(PROSPECTS)} prospects · mis à jour le {date.today().strftime('%d/%m/%Y')}")

    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        fp = st.selectbox("Produit", ["Tous","Krush","Samaï","Kingdom","Indochine"], label_visibility="collapsed")
    with col2:
        fph = st.selectbox("Phase", ["Toutes","PRISE DE CONTACT","CONTACT ÉTABLI","PRÉSENTATION","NÉGOCIATION","CLIENT ✓"], label_visibility="collapsed")
    with col3:
        st.button("+ Nouveau")

    df = PROSPECTS.copy()
    if fp != "Tous": df = df[df["Produit"] == fp]
    if fph != "Toutes": df = df[df["Phase"] == fph]

    st.markdown("<br>", unsafe_allow_html=True)
    phases = list(PHASE_COLORS.keys())
    cols = st.columns(5)
    for i, phase in enumerate(phases):
        accent, bg = PHASE_COLORS[phase]
        pdata = df[df["Phase"] == phase]
        with cols[i]:
            st.markdown(f"""
            <div style='background:{bg};border-radius:8px;padding:12px;border:1px solid #E5E5E3;min-height:80px;margin-bottom:8px;'>
                <div style='font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:{accent};margin-bottom:6px;'>{phase}</div>
                <div style='font-size:24px;font-weight:700;color:#1A1A1A;'>{len(pdata)}</div>
                <div style='font-size:10px;color:#9CA3AF;'>prospect{"s" if len(pdata)>1 else ""}</div>
            </div>
            """, unsafe_allow_html=True)
            for _, row in pdata.iterrows():
                st.markdown(f"""
                <div class='prospect-card' style='border-left:2px solid {accent};'>
                    <div style='font-weight:600;font-size:12px;color:#1A1A1A;'>{row["Établissement"]}</div>
                    <div style='font-size:11px;color:#9CA3AF;margin-top:2px;'>{row["Type"]}</div>
                    <div style='display:flex;justify-content:space-between;margin-top:6px;align-items:center;'>
                        <span style='font-size:10px;background:#F1F0EF;color:#374151;padding:2px 7px;border-radius:4px;font-weight:600;'>{row["Produit"]}</span>
                        <span style='font-size:10px;color:#D1D5DB;'>{row["Date"]}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : EMAILS
# ══════════════════════════════════════════════════════════════════
elif "Emails" in page:
    page_header("Emails & Relances", "Automatisation SMTP · Infomaniak")

    cols = st.columns(3)
    with cols[0]: st.markdown(metric_card("Envoyés ce mois","23",""), unsafe_allow_html=True)
    with cols[1]: st.markdown(metric_card("Taux de réponse","18%","3 réponses",True), unsafe_allow_html=True)
    with cols[2]: st.markdown(metric_card("Relances demain","6","Auto 9h00",True), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3,2])

    with col_l:
        st.markdown("<div class='section-label'>Historique des envois</div>", unsafe_allow_html=True)
        st.dataframe(EMAILS, use_container_width=True, hide_index=True)

        st.markdown("<div class='section-label' style='margin-top:20px;'>Composer un email</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            dest = st.selectbox("Destinataire", PROSPECTS["Établissement"].tolist())
            type_m = st.selectbox("Type", ["Premier contact","Relance J+7","Relance J+14","Offre dégustation"])
        with c2:
            prod = st.selectbox("Produit", ["Krush","Samaï","Kingdom","Indochine"])
            objet = st.text_input("Objet", value=f"{prod} — proposition pour {dest}")
        corps = st.text_area("Corps", height=100,
            value=f"Bonjour,\n\nJe me permets de revenir vers vous au sujet de {prod}...\n\nBien à vous,\nSimon Cogné — NBC")
        c1b, c2b, _ = st.columns([1,1,3])
        c1b.button("Envoyer")
        c2b.button("Sauver")

    with col_r:
        st.markdown("<div class='section-label'>Relances programmées</div>", unsafe_allow_html=True)
        for _, row in PROSPECTS[PROSPECTS["Relance"] != "—"].iterrows():
            j = int(row["Relance"].replace("J+",""))
            accent = "#16A34A" if j > 10 else "#D97706" if j > 6 else "#DC2626"
            st.markdown(f"""
            <div class='nbc-card' style='padding:12px 14px;border-left:2px solid {accent};'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <span style='font-weight:600;font-size:13px;color:#1A1A1A;'>{row["Établissement"]}</span>
                    <span style='font-size:11px;font-weight:700;color:{accent};'>{row["Relance"]}</span>
                </div>
                <div style='font-size:11px;color:#9CA3AF;margin-top:3px;'>{row["Produit"]} · {row["Date"]}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : MES RELANCES
# ══════════════════════════════════════════════════════════════════
elif "relances" in page:
    page_header("Mes relances", "Programmées automatiquement · envoi à 9h00")
    st.info("6 relances programmées cette semaine — elles partent automatiquement.")
    for _, row in PROSPECTS[PROSPECTS["Relance"] != "—"].iterrows():
        j = int(row["Relance"].replace("J+",""))
        accent = "#16A34A" if j > 10 else "#D97706" if j > 6 else "#DC2626"
        st.markdown(f"""
        <div class='nbc-card' style='border-left:2px solid {accent};'>
            <div style='display:flex;justify-content:space-between;'>
                <div>
                    <div style='font-weight:600;font-size:14px;color:#1A1A1A;'>{row["Établissement"]}</div>
                    <div style='font-size:12px;color:#9CA3AF;margin-top:3px;'>{row["Type"]} · {row["Produit"]} · {row["Date"]}</div>
                </div>
                <div style='text-align:right;'>
                    <span style='font-size:16px;font-weight:700;color:{accent};'>{row["Relance"]}</span>
                    <div style='font-size:10px;color:#9CA3AF;'>avant relance</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : STOCKS
# ══════════════════════════════════════════════════════════════════
elif "Stocks" in page:
    page_header("Stocks", "Import automatique · entrepositaire · 03:30 chaque nuit")
    alertes_n = len(STOCKS[STOCKS["Statut"]=="ALERTE"])
    if alertes_n: st.error(f"{alertes_n} SKU(s) sous le seuil d'alerte — réapprovisionnement recommandé")

    cols = st.columns(4)
    with cols[0]: st.markdown(metric_card("Total SKUs",len(STOCKS),""), unsafe_allow_html=True)
    with cols[1]: st.markdown(metric_card("En alerte",alertes_n,"",""), unsafe_allow_html=True)
    with cols[2]: st.markdown(metric_card("Dernière sync","03:47","09/06/2026",True), unsafe_allow_html=True)
    with cols[3]: st.markdown(metric_card("Prochaine sync","03:30","Demain",True), unsafe_allow_html=True)

    st.markdown("<div class='section-label' style='margin-top:24px;'>Niveaux de stock par SKU</div>", unsafe_allow_html=True)
    for _, row in STOCKS.iterrows():
        pct = min(int(row["Stock"] / (row["Seuil"] * 3) * 100), 100)
        accent = "#16A34A" if row["Statut"]=="OK" else "#D97706" if row["Statut"]=="WARNING" else "#DC2626"
        icon = "✓" if row["Statut"]=="OK" else "!" if row["Statut"]=="WARNING" else "✕"
        st.markdown(f"""
        <div class='nbc-card' style='padding:13px 16px;'>
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:7px;'>
                <span style='font-weight:600;font-size:13px;color:#1A1A1A;'>{row["SKU"]}</span>
                <span style='color:{accent};font-weight:700;font-size:12px;'>{row["Stock"]} cartons &nbsp;{icon}</span>
            </div>
            <div class='stock-bar-wrap'>
                <div class='stock-bar-fill' style='background:{accent};width:{pct}%;'></div>
            </div>
            <div style='font-size:10px;color:#9CA3AF;margin-top:5px;'>Seuil alerte : {row["Seuil"]} cartons</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : FACTURATION
# ══════════════════════════════════════════════════════════════════
elif "Facturation" in page:
    page_header("Facturation & Devis", "Génération PDF automatique · SMTP Infomaniak")

    cols = st.columns(4)
    with cols[0]: st.markdown(metric_card("CA du mois","4 320 €","+12% vs mai",True), unsafe_allow_html=True)
    with cols[1]: st.markdown(metric_card("Factures payées","3","1 728 €",True), unsafe_allow_html=True)
    with cols[2]: st.markdown(metric_card("En attente","1","288 €",None), unsafe_allow_html=True)
    with cols[3]: st.markdown(metric_card("En retard","1","240 €",False), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3,2])
    with col_l:
        st.markdown("<div class='section-label'>Toutes les factures</div>", unsafe_allow_html=True)
        st.dataframe(FACTURES, use_container_width=True, hide_index=True)
    with col_r:
        st.markdown("<div class='section-label'>Nouvelle facture</div>", unsafe_allow_html=True)
        client = st.selectbox("Client", ["Brasserie Lipp","Bar du Marché","Cave Legrand","Autre..."])
        produit = st.selectbox("Produit", ["Krush 12x33cl","Kingdom 12x33cl","Indochine 12x33cl","Samaï 6x70cl"])
        qte = st.number_input("Quantité (cartons)", min_value=1, value=10)
        prix = st.number_input("Prix unitaire HT (€)", value=12.0, step=0.5)
        ht = qte * prix
        st.markdown(f"""
        <div class='nbc-card' style='padding:14px;text-align:center;'>
            <div style='font-size:10px;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.08em;'>Total</div>
            <div style='font-size:22px;font-weight:700;color:#1A1A1A;margin:6px 0;'>{ht*1.2:.0f} € TTC</div>
            <div style='font-size:11px;color:#9CA3AF;'>HT : {ht:.0f} € · TVA : {ht*0.2:.0f} €</div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Générer & Envoyer la facture", use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : COMPTA
# ══════════════════════════════════════════════════════════════════
elif "Compta" in page:
    page_header("Comptabilité", "Export macompta.fr · FEC · droits d'accise")

    cols = st.columns(3)
    with cols[0]: st.markdown(metric_card("CA cumulé 2026","14 280 €",""), unsafe_allow_html=True)
    with cols[1]: st.markdown(metric_card("TVA collectée","2 856 €",""), unsafe_allow_html=True)
    with cols[2]: st.markdown(metric_card("Droits d'accise","342 €","2025"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("<div class='section-label'>CA par marque</div>", unsafe_allow_html=True)
        cam = pd.DataFrame({"Marque":["Krush","Kingdom","Indochine","Samaï","Wingman"],"CA":[6800,3200,2400,1400,480]})
        fig = px.pie(cam, values="CA", names="Marque", hole=0.55,
                     color_discrete_sequence=["#1A1A1A","#374151","#6B7280","#9CA3AF","#D1D5DB"])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          font=dict(color="#6B7280", family="Inter"),
                          legend=dict(font=dict(color="#374151")),
                          margin=dict(t=10,b=10))
        fig.update_traces(textinfo="percent", textfont=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)
    with col_r:
        st.markdown("<div class='section-label'>Export macompta.fr</div>", unsafe_allow_html=True)
        mois = st.selectbox("Mois", ["Juin 2026","Mai 2026","Avril 2026"])
        st.markdown(f"""
        <div class='nbc-card' style='margin-top:12px;'>
            <div style='font-size:12px;color:#6B7280;margin-bottom:12px;line-height:1.6;'>
                Le fichier CSV généré est directement compatible avec l'import macompta.fr (format FEC).
                Il inclut toutes les écritures de ventes, TVA et droits d'accise du mois sélectionné.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Générer CSV macompta.fr", use_container_width=True)
        st.button("Exporter bilan du mois PDF", use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : RAPPORT SEMAINE
# ══════════════════════════════════════════════════════════════════
elif "Rapport" in page:
    page_header("Rapport de la semaine", "02/06/2026 → 09/06/2026 · Généré automatiquement chaque lundi 8h")

    cols = st.columns(4)
    with cols[0]: st.markdown(metric_card("Nouveaux prospects","7","+7 vs sem. préc.",True), unsafe_allow_html=True)
    with cols[1]: st.markdown(metric_card("Emails envoyés","12","cette semaine",True), unsafe_allow_html=True)
    with cols[2]: st.markdown(metric_card("CA facturé","768 €","+288 € vs s-1",True), unsafe_allow_html=True)
    with cols[3]: st.markdown(metric_card("Relances faites","4","",True), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("<div class='section-label'>Activité commerciale</div>", unsafe_allow_html=True)
        act = pd.DataFrame({"Action":["1ers contacts","Relances J+7","Relances J+14","Réponses","RDV"],"Nb":[7,3,1,2,1]})
        fig = px.bar(act, x="Action", y="Nb", color_discrete_sequence=["#1A1A1A"], text="Nb")
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with col_r:
        st.markdown("<div class='section-label'>Mouvements stock</div>", unsafe_allow_html=True)
        mvt = pd.DataFrame({"SKU":["Krush Lime","Krush Yuzu","Kingdom IPA","Indochine","Samaï"],"Sorties":[18,24,12,8,6]})
        fig2 = px.bar(mvt, x="SKU", y="Sorties", color_discrete_sequence=["#6B7280"], text="Sorties")
        fig2.update_traces(textposition="outside", marker_line_width=0)
        layout2 = dict(PLOT_LAYOUT)
        layout2["xaxis"] = dict(tickfont=dict(color="#9CA3AF"), tickangle=-20, gridcolor="#F1F0EF")
        fig2.update_layout(**layout2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='section-label'>Points d'attention</div>", unsafe_allow_html=True)
    st.error("Wingman Lager — 12 cartons restants, rupture imminente")
    st.warning("Krush Yuzu Peach — 38 cartons, sous le seuil. Commander avant le 15/06")
    st.warning("Facture NBC-2026-0008 — Bar du Marché, 240 € en retard. Relancer le client")
    st.success("Mama Shelter — en phase négociation, potentiel 500 €/mois récurrent")

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Envoyer ce rapport par email")

# ══════════════════════════════════════════════════════════════════
#  PAGE : PARAMÈTRES
# ══════════════════════════════════════════════════════════════════
elif "Paramètres" in page:
    page_header("Paramètres", "Configuration de la plateforme NBC")
    tab1, tab2, tab3 = st.tabs(["Utilisateurs","Email SMTP","Intégrations"])

    with tab1:
        st.markdown("<div class='section-label'>Comptes actifs</div>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame([
            {"Nom":"Simon Cogné","Login":"simon","Rôle":"Commercial","Accès":"CRM · Emails · Relances"},
            {"Nom":"Direction NBC","Login":"admin","Rôle":"Admin","Accès":"Accès complet"},
        ]), use_container_width=True, hide_index=True)
        st.button("Ajouter un utilisateur")

    with tab2:
        st.markdown("<div class='section-label'>Configuration Infomaniak</div>", unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1:
            st.text_input("Serveur SMTP", value="mail.infomaniak.com", disabled=True)
            st.text_input("Expéditeur", value="simon.cogne2004@gmail.com")
        with c2:
            st.text_input("Port", value="587 (TLS)", disabled=True)
            st.text_input("Mot de passe", type="password", value="••••••••")
        c1b, c2b, _ = st.columns([1,1,3])
        c1b.button("Sauvegarder")
        c2b.button("Tester")

    with tab3:
        st.markdown("<div class='section-label'>Connexions</div>", unsafe_allow_html=True)
        integrations = [
            ("✓","Notion API","Connecté — workspace Natural Beverages Company","#16A34A"),
            ("✓","Infomaniak SMTP","Connecté — simon.cogne2004@gmail.com","#16A34A"),
            ("✓","Entrepositaire","Import auto actif — 03:30 chaque nuit","#16A34A"),
            ("○","macompta.fr","Non configuré — cliquer pour connecter","#9CA3AF"),
        ]
        for icon, name, status, clr in integrations:
            st.markdown(f"""
            <div class='nbc-card' style='display:flex;align-items:center;gap:14px;padding:14px 16px;border-left:2px solid {clr};'>
                <span style='font-size:16px;color:{clr};font-weight:700;'>{icon}</span>
                <div>
                    <div style='font-weight:600;font-size:13px;color:#1A1A1A;'>{name}</div>
                    <div style='font-size:11px;color:#9CA3AF;margin-top:2px;'>{status}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
