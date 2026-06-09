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

# ── Design System NBC ─────────────────────────────────────────────
# Dark premium palette inspired by Krush neon + NBC Art Deco
# Navy dark: #0D1B2A  Cards: #162032  Gold: #C9A84C  Orange accent: #E8834A

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

* {{ box-sizing: border-box; }}

/* ── Global ── */
.stApp {{
    background-color: #0D1B2A;
    font-family: 'Inter', sans-serif;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0A1520 0%, #0D1B2A 100%);
    border-right: 1px solid #1E3148;
}}
[data-testid="stSidebar"] * {{ color: #E8EDF2 !important; font-family: 'Inter', sans-serif !important; }}
[data-testid="stSidebarContent"] {{ padding: 0 !important; }}

/* ── Radio nav ── */
[data-testid="stSidebar"] .stRadio > div {{ gap: 2px !important; }}
[data-testid="stSidebar"] .stRadio label {{
    background: transparent;
    border-radius: 8px;
    padding: 10px 14px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #8FA3B8 !important;
    transition: all 0.2s;
    cursor: pointer;
    border: none !important;
}}
[data-testid="stSidebar"] .stRadio label:hover {{
    background: #162032 !important;
    color: #C9A84C !important;
}}
[data-testid="stSidebar"] [aria-checked="true"] + label,
[data-testid="stSidebar"] .stRadio label[data-selected="true"] {{
    background: linear-gradient(90deg, #162032, #1A2840) !important;
    color: #C9A84C !important;
    border-left: 3px solid #C9A84C !important;
}}

/* ── Metrics ── */
[data-testid="metric-container"] {{
    background: #162032 !important;
    border: 1px solid #1E3148 !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
}}
[data-testid="stMetricLabel"] {{ color: #7A90A4 !important; font-size: 12px !important; font-weight: 500 !important; text-transform: uppercase; letter-spacing: 0.5px; }}
[data-testid="stMetricValue"] {{ color: #F0F4F8 !important; font-size: 28px !important; font-weight: 700 !important; font-family: 'Inter', sans-serif !important; }}
[data-testid="stMetricDelta"] {{ font-size: 12px !important; }}

/* ── Titles ── */
h1, h2, h3 {{ font-family: 'Inter', sans-serif !important; }}
h1 {{ color: #F0F4F8 !important; font-weight: 700 !important; font-size: 24px !important; }}
h2 {{ color: #C9A84C !important; font-weight: 600 !important; font-size: 18px !important; }}
h3 {{ color: #8FA3B8 !important; font-weight: 500 !important; font-size: 14px !important; text-transform: uppercase; letter-spacing: 1px; }}

/* ── Buttons ── */
.stButton > button {{
    background: linear-gradient(135deg, #C9A84C, #E8B84C) !important;
    color: #0D1B2A !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 10px rgba(201,168,76,0.3) !important;
}}
.stButton > button:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(201,168,76,0.5) !important;
}}

/* ── Dataframes ── */
.stDataFrame {{
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid #1E3148 !important;
}}
[data-testid="stDataFrameResizable"] {{
    background: #162032 !important;
}}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {{
    background: #162032 !important;
    border: 1px solid #1E3148 !important;
    border-radius: 8px !important;
    color: #E8EDF2 !important;
    font-family: 'Inter', sans-serif !important;
}}
.stSelectbox > div > div {{ color: #E8EDF2 !important; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: #162032;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1E3148;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent;
    color: #7A90A4;
    border-radius: 7px;
    font-weight: 500;
    font-size: 13px;
    padding: 8px 16px;
}}
.stTabs [aria-selected="true"] {{
    background: #C9A84C !important;
    color: #0D1B2A !important;
    font-weight: 700 !important;
}}

/* ── Alerts ── */
.stAlert {{ border-radius: 10px !important; border: none !important; }}

/* ── Divider ── */
hr {{ border-color: #1E3148 !important; margin: 16px 0 !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: #0D1B2A; }}
::-webkit-scrollbar-thumb {{ background: #1E3148; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: #C9A84C; }}

/* ── Custom cards ── */
.nbc-card {{
    background: #162032;
    border: 1px solid #1E3148;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    transition: all 0.2s;
}}
.nbc-card:hover {{ border-color: #C9A84C44; box-shadow: 0 6px 24px rgba(201,168,76,0.1); }}

.nbc-card-header {{
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #C9A84C;
    margin-bottom: 12px;
}}

/* ── Pipeline kanban cards ── */
.phase-col {{
    background: #111D2B;
    border-radius: 10px;
    padding: 12px;
    border: 1px solid #1A2D42;
    min-height: 200px;
}}
.prospect-card {{
    background: #162032;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 8px;
    border-left: 3px solid #C9A84C;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    transition: transform 0.15s;
}}
.prospect-card:hover {{ transform: translateX(2px); }}

/* ── Badge rôle ── */
.badge-admin {{
    background: linear-gradient(135deg, #C9A84C, #E8B84C);
    color: #0D1B2A;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}}
.badge-com {{
    background: linear-gradient(135deg, #2A4A6B, #1E3A5F);
    color: #C9A84C;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    border: 1px solid #C9A84C44;
}}

/* ── Stock bars ── */
.stock-bar-wrap {{
    background: #0D1B2A;
    border-radius: 4px;
    height: 6px;
    margin-top: 6px;
}}
.stock-bar-fill {{ height: 6px; border-radius: 4px; transition: width 0.5s; }}

/* ── KPI top band ── */
.kpi-band {{
    background: linear-gradient(135deg, #162032 0%, #1A2840 100%);
    border: 1px solid #1E3148;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 20px;
}}

/* ── Section label ── */
.section-label {{
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #C9A84C;
    margin-bottom: 16px;
    padding-left: 2px;
}}

/* ── Login page ── */
.login-wrap {{
    max-width: 440px;
    margin: 60px auto;
}}
.login-card {{
    background: #162032;
    border: 1px solid #1E3148;
    border-radius: 16px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
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
    "PRISE DE CONTACT": ("#E8834A", "#2A1A0F"),
    "CONTACT ÉTABLI":   ("#3A9BD5", "#0F1E2A"),
    "PRÉSENTATION":     ("#9B59B6", "#1A0F24"),
    "NÉGOCIATION":      ("#C9A84C", "#1F1500"),
    "CLIENT ✓":         ("#27AE60", "#0A1F0F"),
}

def sidebar_logo():
    st.markdown(f"""
    <div style='padding:24px 20px 12px 20px; text-align:center;'>
        <img src='data:image/png;base64,{LOGO_B64}'
             style='width:90px; filter:brightness(0) invert(1); margin-bottom:8px;'/>
        <div style='font-size:10px; color:#4A6A8A; letter-spacing:2px; text-transform:uppercase;
                    font-weight:600; margin-top:4px;'>Internal Platform</div>
    </div>
    <div style='height:1px; background:linear-gradient(90deg,transparent,#C9A84C44,transparent); margin:0 20px 16px 20px;'></div>
    """, unsafe_allow_html=True)

def user_badge(role, name):
    badge = "badge-admin" if role == "admin" else "badge-com"
    label = "ADMIN" if role == "admin" else "COMMERCIAL"
    st.markdown(f"""
    <div style='padding:0 20px 16px 20px; text-align:center;'>
        <div class='{badge}'>{label}</div>
        <div style='font-size:12px; color:#4A6A8A; margin-top:8px; font-weight:500;'>{name}</div>
    </div>
    <div style='height:1px; background:#1E3148; margin:0 20px 16px 20px;'></div>
    """, unsafe_allow_html=True)

def page_header(title, subtitle=""):
    st.markdown(f"""
    <div style='margin-bottom:24px;'>
        <h1 style='margin:0; font-size:26px !important; font-weight:700 !important; color:#F0F4F8 !important;'>{title}</h1>
        {"<p style='margin:4px 0 0 0; color:#4A6A8A; font-size:13px;'>"+subtitle+"</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)

def card(content, title=""):
    header = f"<div class='nbc-card-header'>{title}</div>" if title else ""
    st.markdown(f"<div class='nbc-card'>{header}{content}</div>", unsafe_allow_html=True)

def metric_card(label, value, delta="", delta_good=True):
    delta_color = "#27AE60" if delta_good else "#E74C3C"
    delta_html = f"<div style='font-size:12px;color:{delta_color};margin-top:4px;'>{delta}</div>" if delta else ""
    return f"""
    <div class='nbc-card' style='text-align:center; padding:16px;'>
        <div style='font-size:10px;color:#4A6A8A;text-transform:uppercase;letter-spacing:1.5px;font-weight:600;'>{label}</div>
        <div style='font-size:30px;font-weight:700;color:#F0F4F8;margin:8px 0 2px 0;'>{value}</div>
        {delta_html}
    </div>"""

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
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='text-align:center; margin-bottom:32px;'>
            <img src='data:image/png;base64,{LOGO_B64}'
                 style='width:110px; filter:brightness(0) invert(1); margin-bottom:16px;'/>
            <div style='height:1px; background:linear-gradient(90deg,transparent,#C9A84C,transparent); margin:0 40px 20px 40px;'></div>
            <p style='color:#4A6A8A; font-size:13px; letter-spacing:1px; text-transform:uppercase; font-weight:500;'>
                Plateforme de gestion interne
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        with st.form("login"):
            st.markdown("<p style='color:#7A90A4;font-size:12px;text-transform:uppercase;letter-spacing:1px;font-weight:600;margin-bottom:16px;'>Connexion</p>", unsafe_allow_html=True)
            username = st.text_input("", placeholder="Identifiant", label_visibility="collapsed")
            password = st.text_input("", placeholder="Mot de passe", type="password", label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Se connecter →", use_container_width=True)
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
        <div style='text-align:center;margin-top:24px;'>
            <img src='data:image/jpeg;base64,{KRUSH_B64}'
                 style='width:100%;border-radius:12px;opacity:0.4;object-fit:cover;max-height:120px;'/>
        </div>
        <p style='text-align:center;color:#1E3148;font-size:11px;margin-top:12px;'>
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

    st.markdown("<div style='padding:0 10px;'>", unsafe_allow_html=True)
    page = st.radio("", pages, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='position:absolute;bottom:20px;left:0;right:0;padding:0 16px;'>", unsafe_allow_html=True)
    if st.button("Déconnexion", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : ACCUEIL
# ══════════════════════════════════════════════════════════════════
if "Accueil" in page:
    # Hero banner avec Krush
    st.markdown(f"""
    <div style='position:relative;border-radius:16px;overflow:hidden;margin-bottom:28px;height:160px;'>
        <img src='data:image/jpeg;base64,{KRUSH_B64}'
             style='width:100%;height:160px;object-fit:cover;object-position:center 30%;'/>
        <div style='position:absolute;inset:0;background:linear-gradient(90deg,rgba(13,27,42,0.95) 0%,rgba(13,27,42,0.6) 60%,rgba(13,27,42,0.1) 100%);'></div>
        <div style='position:absolute;top:50%;left:28px;transform:translateY(-50%);'>
            <p style='margin:0;color:#C9A84C;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:2px;'>
                {date.today().strftime("%A %d %B %Y")}
            </p>
            <h1 style='margin:6px 0 4px 0;color:#F0F4F8 !important;font-size:28px !important;font-weight:700 !important;'>
                Bonjour, {st.session_state.username.split()[0]} 👋
            </h1>
            <p style='margin:0;color:#7A90A4;font-size:13px;'>Natural Beverages Company · Tableau de bord</p>
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

        st.markdown("<div class='section-label' style='margin-top:24px;'>📅 Relances cette semaine</div>", unsafe_allow_html=True)
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
            st.markdown("<div class='section-label'>📦 Stocks critiques</div>", unsafe_allow_html=True)
            alertes = STOCKS[STOCKS["Statut"] != "OK"][["SKU","Stock","Seuil","Statut"]]
            st.dataframe(alertes, use_container_width=True, hide_index=True)

            st.markdown("<div class='section-label' style='margin-top:20px;'>📈 CA mensuel 2026</div>", unsafe_allow_html=True)
            ca = pd.DataFrame({"Mois":["Fév","Mar","Avr","Mai","Juin"],"CA":[ 1200,2100,2800,3860,4320]})
            fig = px.bar(ca, x="Mois", y="CA", color_discrete_sequence=["#C9A84C"], text="CA")
            fig.update_traces(texttemplate="%{text:,} €", textposition="outside", marker_line_width=0)
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              font=dict(color="#8FA3B8"), showlegend=False,
                              yaxis=dict(showgrid=True, gridcolor="#1E3148", tickfont=dict(color="#4A6A8A")),
                              xaxis=dict(tickfont=dict(color="#4A6A8A")), margin=dict(t=24,b=0,l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            st.markdown("<div class='section-label'>🧾 Dernières factures</div>", unsafe_allow_html=True)
            st.dataframe(FACTURES[["N°","Client","TTC","Statut"]].head(4), use_container_width=True, hide_index=True)

            st.markdown("<div class='section-label' style='margin-top:20px;'>🍹 Répartition CA par marque</div>", unsafe_allow_html=True)
            ca_m = pd.DataFrame({"Marque":["Krush","Kingdom","Indochine","Samaï","Wingman"],"CA":[6800,3200,2400,1400,480]})
            fig2 = px.pie(ca_m, values="CA", names="Marque",
                          color_discrete_sequence=["#C9A84C","#3A9BD5","#9B59B6","#27AE60","#E8834A"],
                          hole=0.5)
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font=dict(color="#8FA3B8"), showlegend=True,
                               legend=dict(font=dict(color="#8FA3B8",size=11)),
                               margin=dict(t=10,b=10,l=0,r=0))
            fig2.update_traces(textinfo="percent", textfont=dict(color="white"))
            st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : CRM PIPELINE
# ══════════════════════════════════════════════════════════════════
elif "CRM" in page:
    page_header("🤝 CRM Pipeline", f"{len(PROSPECTS)} prospects · mis à jour le {date.today().strftime('%d/%m/%Y')}")

    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        fp = st.selectbox("Produit", ["Tous","Krush","Samaï","Kingdom","Indochine"], label_visibility="collapsed")
    with col2:
        fph = st.selectbox("Phase", ["Toutes","PRISE DE CONTACT","CONTACT ÉTABLI","PRÉSENTATION","NÉGOCIATION","CLIENT ✓"], label_visibility="collapsed")
    with col3:
        st.button("➕ Nouveau prospect")

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
            <div style='background:{bg};border-radius:10px;padding:12px;border:1px solid {accent}33;min-height:80px;'>
                <div style='font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:{accent};margin-bottom:8px;'>{phase}</div>
                <div style='font-size:26px;font-weight:700;color:#F0F4F8;'>{len(pdata)}</div>
                <div style='font-size:10px;color:#4A6A8A;'>prospect{"s" if len(pdata)>1 else ""}</div>
            </div>
            <div style='margin-top:8px;'>
            """, unsafe_allow_html=True)
            for _, row in pdata.iterrows():
                st.markdown(f"""
                <div class='prospect-card' style='border-left-color:{accent};'>
                    <div style='font-weight:600;font-size:12px;color:#F0F4F8;'>{row["Établissement"]}</div>
                    <div style='font-size:11px;color:#4A6A8A;margin-top:2px;'>{row["Type"]}</div>
                    <div style='display:flex;justify-content:space-between;margin-top:6px;align-items:center;'>
                        <span style='font-size:10px;background:{accent}22;color:{accent};padding:2px 8px;border-radius:10px;font-weight:600;'>{row["Produit"]}</span>
                        <span style='font-size:10px;color:#2A4A6B;'>{row["Date"]}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : EMAILS
# ══════════════════════════════════════════════════════════════════
elif "Emails" in page:
    page_header("📧 Emails & Relances", "Automatisation SMTP · Infomaniak")

    cols = st.columns(3)
    with cols[0]: st.markdown(metric_card("Envoyés ce mois","23",""), unsafe_allow_html=True)
    with cols[1]: st.markdown(metric_card("Taux de réponse","18%","3 réponses",True), unsafe_allow_html=True)
    with cols[2]: st.markdown(metric_card("Relances demain","6","Auto 9h00",True), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3,2])

    with col_l:
        st.markdown("<div class='section-label'>Historique des envois</div>", unsafe_allow_html=True)
        st.dataframe(EMAILS, use_container_width=True, hide_index=True)

        st.markdown("<div class='section-label' style='margin-top:20px;'>✏️ Composer un email</div>", unsafe_allow_html=True)
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
        c1b.button("📤 Envoyer")
        c2b.button("💾 Sauver")

    with col_r:
        st.markdown("<div class='section-label'>⏰ Relances programmées</div>", unsafe_allow_html=True)
        for _, row in PROSPECTS[PROSPECTS["Relance"] != "—"].iterrows():
            j = int(row["Relance"].replace("J+",""))
            accent = "#27AE60" if j > 10 else "#C9A84C" if j > 6 else "#E74C3C"
            st.markdown(f"""
            <div class='nbc-card' style='padding:12px 16px;border-left:3px solid {accent};'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <span style='font-weight:600;font-size:13px;color:#F0F4F8;'>{row["Établissement"]}</span>
                    <span style='font-size:11px;font-weight:700;color:{accent};'>{row["Relance"]}</span>
                </div>
                <div style='font-size:11px;color:#4A6A8A;margin-top:4px;'>{row["Produit"]} · {row["Date"]}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : MES RELANCES
# ══════════════════════════════════════════════════════════════════
elif "relances" in page:
    page_header("📅 Mes relances", "Programmées automatiquement · envoi à 9h00")
    st.info("📬 6 relances programmées cette semaine — elles partent automatiquement, tu n'as rien à faire.")
    for _, row in PROSPECTS[PROSPECTS["Relance"] != "—"].iterrows():
        j = int(row["Relance"].replace("J+",""))
        accent = "#27AE60" if j > 10 else "#C9A84C" if j > 6 else "#E74C3C"
        st.markdown(f"""
        <div class='nbc-card' style='border-left:3px solid {accent};'>
            <div style='display:flex;justify-content:space-between;'>
                <div>
                    <div style='font-weight:600;font-size:14px;color:#F0F4F8;'>{row["Établissement"]}</div>
                    <div style='font-size:12px;color:#4A6A8A;margin-top:4px;'>{row["Type"]} · {row["Produit"]} · {row["Date"]}</div>
                </div>
                <div style='text-align:right;'>
                    <span style='font-size:16px;font-weight:700;color:{accent};'>{row["Relance"]}</span>
                    <div style='font-size:10px;color:#4A6A8A;'>avant relance</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : STOCKS
# ══════════════════════════════════════════════════════════════════
elif "Stocks" in page:
    page_header("📦 Stocks", "Import automatique · entrepositaire · 03:30 chaque nuit")
    alertes_n = len(STOCKS[STOCKS["Statut"]=="ALERTE"])
    if alertes_n: st.error(f"⚠️  {alertes_n} SKU(s) sous le seuil d'alerte — réapprovisionnement recommandé")

    cols = st.columns(4)
    with cols[0]: st.markdown(metric_card("Total SKUs",len(STOCKS),""), unsafe_allow_html=True)
    with cols[1]: st.markdown(metric_card("En alerte",alertes_n,"","" ), unsafe_allow_html=True)
    with cols[2]: st.markdown(metric_card("Dernière sync","03:47","09/06/2026",True), unsafe_allow_html=True)
    with cols[3]: st.markdown(metric_card("Prochaine sync","03:30","Demain",True), unsafe_allow_html=True)

    st.markdown("<div class='section-label' style='margin-top:24px;'>Niveaux de stock par SKU</div>", unsafe_allow_html=True)
    for _, row in STOCKS.iterrows():
        pct = min(int(row["Stock"] / (row["Seuil"] * 3) * 100), 100)
        accent = "#27AE60" if row["Statut"]=="OK" else "#C9A84C" if row["Statut"]=="WARNING" else "#E74C3C"
        icon = "✅" if row["Statut"]=="OK" else "⚠️" if row["Statut"]=="WARNING" else "🔴"
        st.markdown(f"""
        <div class='nbc-card' style='padding:14px 18px;'>
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>
                <span style='font-weight:600;font-size:13px;color:#F0F4F8;'>{row["SKU"]}</span>
                <span style='color:{accent};font-weight:700;font-size:13px;'>{row["Stock"]} cartons {icon}</span>
            </div>
            <div class='stock-bar-wrap'>
                <div class='stock-bar-fill' style='background:{accent};width:{pct}%;'></div>
            </div>
            <div style='font-size:10px;color:#2A4A6B;margin-top:5px;'>Seuil alerte : {row["Seuil"]} cartons</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : FACTURATION
# ══════════════════════════════════════════════════════════════════
elif "Facturation" in page:
    page_header("🧾 Facturation & Devis", "Génération PDF automatique · SMTP Infomaniak")

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
        st.markdown("<div class='section-label'>➕ Nouvelle facture</div>", unsafe_allow_html=True)
        client = st.selectbox("Client", ["Brasserie Lipp","Bar du Marché","Cave Legrand","Autre..."])
        produit = st.selectbox("Produit", ["Krush 12x33cl","Kingdom 12x33cl","Indochine 12x33cl","Samaï 6x70cl"])
        qte = st.number_input("Quantité (cartons)", min_value=1, value=10)
        prix = st.number_input("Prix unitaire HT (€)", value=12.0, step=0.5)
        ht = qte * prix
        st.markdown(f"""
        <div class='nbc-card' style='padding:14px;text-align:center;'>
            <div style='font-size:11px;color:#4A6A8A;text-transform:uppercase;letter-spacing:1px;'>Total</div>
            <div style='font-size:22px;font-weight:700;color:#C9A84C;margin:6px 0;'>{ht*1.2:.0f} € TTC</div>
            <div style='font-size:11px;color:#4A6A8A;'>HT : {ht:.0f} € · TVA : {ht*0.2:.0f} €</div>
        </div>
        """, unsafe_allow_html=True)
        st.button("📄 Générer & Envoyer la facture", use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : COMPTA
# ══════════════════════════════════════════════════════════════════
elif "Compta" in page:
    page_header("💰 Comptabilité", "Export macompta.fr · FEC · droits d'accise")

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
                     color_discrete_sequence=["#C9A84C","#3A9BD5","#9B59B6","#27AE60","#E8834A"])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                          font=dict(color="#8FA3B8"),legend=dict(font=dict(color="#8FA3B8")),
                          margin=dict(t=10,b=10))
        fig.update_traces(textinfo="percent",textfont=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)
    with col_r:
        st.markdown("<div class='section-label'>Export macompta.fr</div>", unsafe_allow_html=True)
        mois = st.selectbox("Mois", ["Juin 2026","Mai 2026","Avril 2026"])
        st.markdown(f"""
        <div class='nbc-card' style='margin-top:12px;'>
            <div style='font-size:12px;color:#4A6A8A;margin-bottom:12px;'>
                Le fichier CSV généré est directement compatible avec l'import macompta.fr (format FEC).
                Il inclut toutes les écritures de ventes, TVA et droits d'accise du mois sélectionné.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("📥 Générer CSV macompta.fr", use_container_width=True)
        st.button("📊 Exporter bilan du mois PDF", use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : RAPPORT SEMAINE
# ══════════════════════════════════════════════════════════════════
elif "Rapport" in page:
    page_header("📊 Rapport de la semaine", "02/06/2026 → 09/06/2026 · Généré automatiquement chaque lundi 8h")

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
        fig = px.bar(act, x="Action", y="Nb", color_discrete_sequence=["#C9A84C"], text="Nb")
        fig.update_traces(textposition="outside",marker_line_width=0)
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                          font=dict(color="#8FA3B8"),showlegend=False,
                          yaxis=dict(showgrid=True,gridcolor="#1E3148",tickfont=dict(color="#4A6A8A")),
                          xaxis=dict(tickfont=dict(color="#4A6A8A")),margin=dict(t=24,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)
    with col_r:
        st.markdown("<div class='section-label'>Mouvements stock</div>", unsafe_allow_html=True)
        mvt = pd.DataFrame({"SKU":["Krush Lime","Krush Yuzu","Kingdom IPA","Indochine","Samaï"],"Sorties":[18,24,12,8,6]})
        fig2 = px.bar(mvt, x="SKU", y="Sorties", color_discrete_sequence=["#3A9BD5"], text="Sorties")
        fig2.update_traces(textposition="outside",marker_line_width=0)
        fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#8FA3B8"),showlegend=False,
                           yaxis=dict(showgrid=True,gridcolor="#1E3148",tickfont=dict(color="#4A6A8A")),
                           xaxis=dict(tickangle=-20, tickfont=dict(color="#4A6A8A")),margin=dict(t=24,b=0,l=0,r=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='section-label'>Points d'attention</div>", unsafe_allow_html=True)
    st.error("🔴  **Wingman Lager** — 12 cartons restants, rupture imminente")
    st.warning("⚠️  **Krush Yuzu Peach** — 38 cartons, sous le seuil. Commander avant le 15/06")
    st.warning("⚠️  **Facture NBC-2026-0008** — Bar du Marché, 240 € en retard. Relancer le client")
    st.success("✅  **Mama Shelter** — en phase négociation, potentiel 500 €/mois récurrent")

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("📤 Envoyer ce rapport par email", use_container_width=False)

# ══════════════════════════════════════════════════════════════════
#  PAGE : PARAMÈTRES
# ══════════════════════════════════════════════════════════════════
elif "Paramètres" in page:
    page_header("⚙️ Paramètres", "Configuration de la plateforme NBC")
    tab1, tab2, tab3 = st.tabs(["👤  Utilisateurs","📧  Email SMTP","🔗  Intégrations"])

    with tab1:
        st.markdown("<div class='section-label'>Comptes actifs</div>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame([
            {"Nom":"Simon Cogné","Login":"simon","Rôle":"Commercial","Accès":"CRM · Emails · Relances"},
            {"Nom":"Direction NBC","Login":"admin","Rôle":"Admin","Accès":"Accès complet"},
        ]), use_container_width=True, hide_index=True)
        st.button("➕ Ajouter un utilisateur")

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
        c1b.button("💾 Sauvegarder")
        c2b.button("📤 Tester")

    with tab3:
        st.markdown("<div class='section-label'>Connexions</div>", unsafe_allow_html=True)
        integrations = [
            ("✅","Notion API","Connecté — workspace Natural Beverages Company","#27AE60"),
            ("✅","Infomaniak SMTP","Connecté — simon.cogne2004@gmail.com","#27AE60"),
            ("✅","Entrepositaire","Import auto actif — 03:30 chaque nuit","#27AE60"),
            ("⚙️","macompta.fr","Non configuré — cliquer pour connecter","#C9A84C"),
        ]
        for icon, name, status, clr in integrations:
            st.markdown(f"""
            <div class='nbc-card' style='display:flex;align-items:center;gap:14px;padding:14px 18px;border-left:3px solid {clr};'>
                <span style='font-size:20px;'>{icon}</span>
                <div>
                    <div style='font-weight:600;font-size:13px;color:#F0F4F8;'>{name}</div>
                    <div style='font-size:11px;color:#4A6A8A;margin-top:2px;'>{status}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
