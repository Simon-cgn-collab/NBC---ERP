import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
import random

# ── Config page ───────────────────────────────────────────────────
st.set_page_config(
    page_title="NBC ERP",
    page_icon="🍹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS Custom NBC ────────────────────────────────────────────────
st.markdown("""
<style>
    /* Fond général */
    .stApp { background-color: #F8F9FA; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1F3864 0%, #152849 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stRadio label { color: #E0E0E0 !important; font-size: 15px; }

    /* Métriques */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    [data-testid="stMetricValue"] { color: #1F3864 !important; font-weight: 700; }

    /* Titres */
    h1 { color: #1F3864 !important; }
    h2 { color: #1F3864 !important; }
    h3 { color: #C9A84C !important; }

    /* Boutons */
    .stButton > button {
        background-color: #1F3864;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 20px;
        font-weight: 600;
    }
    .stButton > button:hover { background-color: #C9A84C; }

    /* Tags pipeline */
    .tag-contact   { background:#E8F5E9; color:#2E7D32; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
    .tag-prise     { background:#FFF3E0; color:#E65100; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
    .tag-pres      { background:#E3F2FD; color:#1565C0; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
    .tag-nego      { background:#F3E5F5; color:#6A1B9A; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; }
    .tag-client    { background:#E8F5E9; color:#1B5E20; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:600; font-style:italic; }

    /* Cards */
    .card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 12px;
    }

    /* Header badge */
    .badge-admin { background:#C9A84C; color:white; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; }
    .badge-com   { background:#1F3864; color:white; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; }

    /* Alerte stock */
    .stock-ok      { color: #27AE60; font-weight:700; }
    .stock-warning { color: #E67E22; font-weight:700; }
    .stock-alert   { color: #C0392B; font-weight:700; }

    /* Login */
    .login-box {
        max-width: 420px;
        margin: 80px auto;
        background: white;
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
</style>
""", unsafe_allow_html=True)

# ── Données fictives ───────────────────────────────────────────────
PROSPECTS = pd.DataFrame([
    {"Établissement": "NENI Paris",           "Type": "Restaurant",  "Produit": "Krush",    "Phase": "CONTACT ÉTABLI",    "Dernière action": "09/06/2026", "Email": "contact@neni.fr",              "Relance": "J+5"},
    {"Établissement": "Le Perchoir",          "Type": "Rooftop",     "Produit": "Krush",    "Phase": "CONTACT ÉTABLI",    "Dernière action": "09/06/2026", "Email": "menilmontant@leperchoir.fr",   "Relance": "J+5"},
    {"Établissement": "Terrass Hotel",        "Type": "Hôtel",       "Produit": "Krush",    "Phase": "PRÉSENTATION",      "Dernière action": "05/06/2026", "Email": "commercial@terrass-hotel.com", "Relance": "J+11"},
    {"Établissement": "Rosa Bonheur",         "Type": "Guinguette",  "Produit": "Krush",    "Phase": "CONTACT ÉTABLI",    "Dernière action": "09/06/2026", "Email": "info@rosabonheur.fr",          "Relance": "J+5"},
    {"Établissement": "Mama Shelter",         "Type": "Rooftop",     "Produit": "Krush",    "Phase": "NÉGOCIATION",       "Dernière action": "01/06/2026", "Email": "food.pariseast@mamashelter.com","Relance": "J+15"},
    {"Établissement": "La Bellevilloise",     "Type": "Rooftop Bar", "Produit": "Krush",    "Phase": "CONTACT ÉTABLI",    "Dernière action": "09/06/2026", "Email": "contact@labellevilloise.com",  "Relance": "J+5"},
    {"Établissement": "Holiday Inn Elysées", "Type": "Hôtel",       "Produit": "Krush",    "Phase": "PRÉSENTATION",      "Dernière action": "03/06/2026", "Email": "fnb@hiparisely.com",           "Relance": "J+9"},
    {"Établissement": "Café Odessa",          "Type": "Café",        "Produit": "Krush",    "Phase": "PRISE DE CONTACT",  "Dernière action": "09/06/2026", "Email": "contact@cafe-odessa.fr",       "Relance": "J+5"},
    {"Établissement": "Bar du Marché",        "Type": "Bar",         "Produit": "Krush",    "Phase": "CLIENT ✓",          "Dernière action": "20/05/2026", "Email": "contact@bardumarche.fr",       "Relance": "—"},
    {"Établissement": "Hotel Lutetia",        "Type": "Hôtel",       "Produit": "Samaï",    "Phase": "NÉGOCIATION",       "Dernière action": "28/05/2026", "Email": "fb@lutetia.com",               "Relance": "J+18"},
    {"Établissement": "Caviste du Temple",    "Type": "Caviste",     "Produit": "Kingdom",  "Phase": "PRISE DE CONTACT",  "Dernière action": "07/06/2026", "Email": "bonjour@caviste-temple.fr",    "Relance": "J+7"},
    {"Établissement": "Brasserie Lipp",       "Type": "Restaurant",  "Produit": "Indochine","Phase": "CLIENT ✓",          "Dernière action": "15/05/2026", "Email": "contact@brasserie-lipp.fr",    "Relance": "—"},
    {"Établissement": "Café des Marronniers", "Type": "Café",        "Produit": "Krush",    "Phase": "CONTACT ÉTABLI",    "Dernière action": "09/06/2026", "Email": "—",                            "Relance": "J+5"},
    {"Établissement": "Skyline Bar",          "Type": "Rooftop",     "Produit": "Krush",    "Phase": "PRISE DE CONTACT",  "Dernière action": "08/06/2026", "Email": "@skylinebarparis",             "Relance": "J+6"},
    {"Établissement": "L'Imprimerie Hotel",   "Type": "Hôtel",       "Produit": "Krush",    "Phase": "CONTACT ÉTABLI",    "Dernière action": "09/06/2026", "Email": "resa@limprimeriehotel.com",    "Relance": "J+5"},
])

STOCKS = pd.DataFrame([
    {"SKU": "Krush Lime Ginger 33cl",       "Stock (cartons)": 142, "Seuil alerte": 50,  "Entrée dernière": "02/06/2026", "Statut": "OK"},
    {"SKU": "Krush Yuzu Peach 33cl",        "Stock (cartons)": 38,  "Seuil alerte": 50,  "Entrée dernière": "02/06/2026", "Statut": "ALERTE"},
    {"SKU": "Krush Mango Passion 33cl",     "Stock (cartons)": 87,  "Seuil alerte": 50,  "Entrée dernière": "02/06/2026", "Statut": "OK"},
    {"SKU": "Krush Raspberry Jasmin 0%",    "Stock (cartons)": 54,  "Seuil alerte": 40,  "Entrée dernière": "02/06/2026", "Statut": "OK"},
    {"SKU": "Samaï Rum Original 70cl",      "Stock (cartons)": 21,  "Seuil alerte": 30,  "Entrée dernière": "28/05/2026", "Statut": "ALERTE"},
    {"SKU": "Kingdom Pilsner 33cl",         "Stock (cartons)": 210, "Seuil alerte": 80,  "Entrée dernière": "02/06/2026", "Statut": "OK"},
    {"SKU": "Kingdom IPA 33cl",             "Stock (cartons)": 178, "Seuil alerte": 80,  "Entrée dernière": "02/06/2026", "Statut": "OK"},
    {"SKU": "Kingdom IPA Mangue 33cl",      "Stock (cartons)": 44,  "Seuil alerte": 60,  "Entrée dernière": "02/06/2026", "Statut": "WARNING"},
    {"SKU": "Indochine Blanche Poivre 33cl","Stock (cartons)": 96,  "Seuil alerte": 60,  "Entrée dernière": "02/06/2026", "Statut": "OK"},
    {"SKU": "Wingman Lager 33cl",           "Stock (cartons)": 12,  "Seuil alerte": 40,  "Entrée dernière": "28/05/2026", "Statut": "ALERTE"},
])

FACTURES = pd.DataFrame([
    {"N°": "NBC-2026-0012", "Client": "Brasserie Lipp",    "Produit": "Indochine",  "Montant HT": "480 €",  "TVA": "96 €",  "Total TTC": "576 €",  "Date": "09/06/2026", "Statut": "✅ Payée"},
    {"N°": "NBC-2026-0011", "Client": "Bar du Marché",     "Produit": "Krush",      "Montant HT": "240 €",  "TVA": "48 €",  "Total TTC": "288 €",  "Date": "07/06/2026", "Statut": "⏳ En attente"},
    {"N°": "NBC-2026-0010", "Client": "Brasserie Lipp",    "Produit": "Indochine",  "Montant HT": "480 €",  "TVA": "96 €",  "Total TTC": "576 €",  "Date": "01/06/2026", "Statut": "✅ Payée"},
    {"N°": "NBC-2026-0009", "Client": "Cave Legrand",      "Produit": "Kingdom",    "Montant HT": "360 €",  "TVA": "72 €",  "Total TTC": "432 €",  "Date": "28/05/2026", "Statut": "✅ Payée"},
    {"N°": "NBC-2026-0008", "Client": "Bar du Marché",     "Produit": "Krush",      "Montant HT": "200 €",  "TVA": "40 €",  "Total TTC": "240 €",  "Date": "20/05/2026", "Statut": "🔴 En retard"},
])

EMAILS_LOG = pd.DataFrame([
    {"Date": "09/06/2026", "Destinataire": "NENI Paris",          "Type": "Premier contact", "Produit": "Krush",    "Statut": "✅ Envoyé"},
    {"Date": "09/06/2026", "Destinataire": "Le Perchoir",         "Type": "Premier contact", "Produit": "Krush",    "Statut": "✅ Envoyé"},
    {"Date": "09/06/2026", "Destinataire": "Rosa Bonheur",        "Type": "Premier contact", "Produit": "Krush",    "Statut": "✅ Envoyé"},
    {"Date": "05/06/2026", "Destinataire": "Terrass Hotel",       "Type": "Relance J+7",     "Produit": "Krush",    "Statut": "✅ Envoyé"},
    {"Date": "03/06/2026", "Destinataire": "Holiday Inn",         "Type": "Relance J+7",     "Produit": "Krush",    "Statut": "✅ Envoyé"},
    {"Date": "01/06/2026", "Destinataire": "Mama Shelter",        "Type": "Relance J+14",    "Produit": "Krush",    "Statut": "✅ Envoyé"},
    {"Date": "28/05/2026", "Destinataire": "Hotel Lutetia",       "Type": "Premier contact", "Produit": "Samaï",    "Statut": "✅ Envoyé"},
    {"Date": "07/06/2026", "Destinataire": "Rapport hebdo",       "Type": "Rapport auto",    "Produit": "—",        "Statut": "✅ Envoyé"},
])

# ── Session state ──────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""

# ══════════════════════════════════════════════════════════════════
#  LOGIN PAGE
# ══════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align:center; margin-bottom:30px;'>
            <div style='font-size:48px;'>🍹</div>
            <h1 style='color:#1F3864; margin:8px 0 4px 0;'>NBC ERP</h1>
            <p style='color:#888; font-size:14px;'>Natural Beverages Company</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Identifiant", placeholder="simon / admin")
            password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Se connecter", use_container_width=True)

            if submitted:
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

        st.markdown("""
        <div style='text-align:center; margin-top:20px; color:#AAA; font-size:12px;'>
            Demo : simon / krush2026 &nbsp;·&nbsp; admin / nbc2026
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px 0;'>
        <div style='font-size:36px;'>🍹</div>
        <div style='font-size:18px; font-weight:700; color:white;'>NBC ERP</div>
        <div style='font-size:11px; color:#C9A84C; margin-top:2px;'>Natural Beverages Company</div>
    </div>
    """, unsafe_allow_html=True)

    role = st.session_state.role
    badge = "badge-admin" if role == "admin" else "badge-com"
    label = "ADMIN" if role == "admin" else "COMMERCIAL"
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:20px;'>
        <span class='{badge}'>{label}</span>
        <div style='font-size:12px; color:#ccc; margin-top:6px;'>{st.session_state.username}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#ffffff30; margin:10px 0;'>", unsafe_allow_html=True)

    if role == "commercial":
        pages = ["🏠 Accueil", "🤝 CRM Pipeline", "📧 Emails", "📅 Mes relances"]
    else:
        pages = ["🏠 Accueil", "🤝 CRM Pipeline", "📧 Emails", "📦 Stocks", "🧾 Facturation", "💰 Compta", "📊 Rapport semaine", "⚙️ Paramètres"]

    page = st.radio("Navigation", pages, label_visibility="collapsed")

    st.markdown("<hr style='border-color:#ffffff30; margin:20px 0 10px 0;'>", unsafe_allow_html=True)
    if st.button("🚪 Déconnexion", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()

# ══════════════════════════════════════════════════════════════════
#  PAGE : ACCUEIL
# ══════════════════════════════════════════════════════════════════
if "Accueil" in page:
    st.markdown(f"## 🏠 Bonjour, {st.session_state.username} 👋")
    st.markdown(f"*{date.today().strftime('%A %d %B %Y')}*")
    st.markdown("---")

    if st.session_state.role == "commercial":
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Prospects actifs", "15", "+3 cette semaine")
        col2.metric("Relances dues", "6", "cette semaine")
        col3.metric("Emails envoyés", "23", "ce mois")
        col4.metric("Nouveaux clients", "2", "ce mois")

        st.markdown("---")
        st.markdown("### 📅 Mes relances cette semaine")
        relances = PROSPECTS[PROSPECTS["Relance"] != "—"][["Établissement", "Type", "Produit", "Phase", "Dernière action", "Relance"]]
        st.dataframe(relances, use_container_width=True, hide_index=True)

    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("CA du mois", "4 320 €", "+12% vs mai")
        col2.metric("Prospects actifs", "15", "+3 cette semaine")
        col3.metric("Factures en attente", "2", "528 €")
        col4.metric("SKUs en alerte stock", "3", "⚠️")

        st.markdown("---")
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("### 📦 Stocks critiques")
            alertes = STOCKS[STOCKS["Statut"] != "OK"][["SKU", "Stock (cartons)", "Seuil alerte", "Statut"]]
            st.dataframe(alertes, use_container_width=True, hide_index=True)

        with col_right:
            st.markdown("### 🧾 Dernières factures")
            st.dataframe(FACTURES[["N°", "Client", "Total TTC", "Statut"]].head(4),
                        use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 📈 CA par mois (2026)")
        ca_data = pd.DataFrame({
            "Mois": ["Févr.", "Mars", "Avr.", "Mai", "Juin"],
            "CA (€)": [1200, 2100, 2800, 3860, 4320],
        })
        fig = px.bar(ca_data, x="Mois", y="CA (€)",
                     color_discrete_sequence=["#1F3864"],
                     text="CA (€)")
        fig.update_traces(texttemplate="%{text} €", textposition="outside")
        fig.update_layout(showlegend=False, plot_bgcolor="white",
                          yaxis=dict(showgrid=True, gridcolor="#F0F0F0"),
                          margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : CRM PIPELINE
# ══════════════════════════════════════════════════════════════════
elif "CRM" in page:
    st.markdown("## 🤝 CRM Pipeline")
    st.markdown("---")

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        filtre_produit = st.selectbox("Filtrer par produit", ["Tous", "Krush", "Samaï", "Kingdom", "Indochine"])
    with col2:
        filtre_phase = st.selectbox("Filtrer par phase", ["Toutes", "PRISE DE CONTACT", "CONTACT ÉTABLI", "PRÉSENTATION", "NÉGOCIATION", "CLIENT ✓"])
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("➕ Nouveau prospect")

    df = PROSPECTS.copy()
    if filtre_produit != "Tous":
        df = df[df["Produit"] == filtre_produit]
    if filtre_phase != "Toutes":
        df = df[df["Phase"] == filtre_phase]

    st.markdown("---")

    phases = ["PRISE DE CONTACT", "CONTACT ÉTABLI", "PRÉSENTATION", "NÉGOCIATION", "CLIENT ✓"]
    colors_phase = {"PRISE DE CONTACT": "#FFF3E0", "CONTACT ÉTABLI": "#E3F2FD",
                    "PRÉSENTATION": "#F3E5F5", "NÉGOCIATION": "#EDE7F6", "CLIENT ✓": "#E8F5E9"}
    border_phase = {"PRISE DE CONTACT": "#E65100", "CONTACT ÉTABLI": "#1565C0",
                    "PRÉSENTATION": "#6A1B9A", "NÉGOCIATION": "#4A148C", "CLIENT ✓": "#1B5E20"}

    cols = st.columns(5)
    for i, phase in enumerate(phases):
        phase_df = df[df["Phase"] == phase]
        with cols[i]:
            st.markdown(f"""
            <div style='background:{colors_phase[phase]}; border-top:4px solid {border_phase[phase]};
                        border-radius:8px; padding:10px; margin-bottom:8px; text-align:center;'>
                <b style='color:{border_phase[phase]}; font-size:11px;'>{phase}</b><br>
                <span style='font-size:22px; font-weight:700; color:#1F3864;'>{len(phase_df)}</span>
            </div>
            """, unsafe_allow_html=True)
            for _, row in phase_df.iterrows():
                st.markdown(f"""
                <div style='background:white; border-radius:8px; padding:10px; margin-bottom:6px;
                             box-shadow:0 1px 4px rgba(0,0,0,0.1); border-left:3px solid {border_phase[phase]};'>
                    <div style='font-weight:700; font-size:12px; color:#1F3864;'>{row["Établissement"]}</div>
                    <div style='font-size:11px; color:#888;'>{row["Type"]}</div>
                    <div style='font-size:11px; color:#C9A84C; margin-top:2px;'>🍹 {row["Produit"]}</div>
                    <div style='font-size:10px; color:#AAA; margin-top:4px;'>📅 {row["Dernière action"]}</div>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : EMAILS
# ══════════════════════════════════════════════════════════════════
elif "Emails" in page:
    st.markdown("## 📧 Emails & Relances automatiques")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("Emails envoyés ce mois", "23")
    col2.metric("Taux de réponse estimé", "18%", "3 réponses")
    col3.metric("Prochaines relances auto", "6", "demain matin 9h")

    st.markdown("---")
    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        st.markdown("### 📋 Historique des envois")
        st.dataframe(EMAILS_LOG, use_container_width=True, hide_index=True)

    with col_right:
        st.markdown("### ⏰ Relances programmées")
        relances_prog = PROSPECTS[PROSPECTS["Relance"] != "—"][["Établissement", "Produit", "Relance"]].head(6)
        for _, row in relances_prog.iterrows():
            j = int(row["Relance"].replace("J+", ""))
            clr = "#E8F5E9" if j > 10 else "#FFF3E0" if j > 6 else "#FFEBEE"
            brd = "#27AE60" if j > 10 else "#E67E22" if j > 6 else "#C0392B"
            st.markdown(f"""
            <div style='background:{clr}; border-left:3px solid {brd};
                        border-radius:6px; padding:8px 12px; margin-bottom:6px;'>
                <b style='font-size:12px;'>{row["Établissement"]}</b>
                <span style='float:right; font-size:11px; color:{brd}; font-weight:700;'>{row["Relance"]}</span>
                <br><span style='font-size:11px; color:#888;'>{row["Produit"]}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ✏️ Composer un email")
    col1, col2 = st.columns(2)
    with col1:
        dest = st.selectbox("Destinataire", PROSPECTS["Établissement"].tolist())
        produit = st.selectbox("Produit", ["Krush", "Samaï", "Kingdom", "Indochine"])
    with col2:
        type_mail = st.selectbox("Type", ["Premier contact", "Relance J+7", "Relance J+14", "Offre dégus", "Confirmation commande"])
        objet = st.text_input("Objet", value=f"Krush — proposition pour {dest}")
    corps = st.text_area("Corps du mail", height=120,
        value=f"Bonjour,\n\nJe me permets de revenir vers vous au sujet de {produit}...\n\nBien à vous,\nSimon Cogné — Natural Beverages Company")
    col_btn1, col_btn2, _ = st.columns([1, 1, 3])
    col_btn1.button("📤 Envoyer")
    col_btn2.button("💾 Sauvegarder")

# ══════════════════════════════════════════════════════════════════
#  PAGE : MES RELANCES (commercial uniquement)
# ══════════════════════════════════════════════════════════════════
elif "relances" in page:
    st.markdown("## 📅 Mes relances")
    st.markdown("---")
    st.info("📬 6 relances sont programmées pour cette semaine — elles partiront automatiquement à 9h chaque matin.")
    relances = PROSPECTS[PROSPECTS["Relance"] != "—"]
    for _, row in relances.iterrows():
        j = int(row["Relance"].replace("J+", ""))
        clr = "#E8F5E9" if j > 10 else "#FFF3E0" if j > 6 else "#FFEBEE"
        brd = "#27AE60" if j > 10 else "#E67E22" if j > 6 else "#C0392B"
        with st.container():
            st.markdown(f"""
            <div style='background:{clr}; border-left:4px solid {brd}; border-radius:8px;
                        padding:14px 18px; margin-bottom:10px;'>
                <div style='display:flex; justify-content:space-between;'>
                    <b style='font-size:14px; color:#1F3864;'>{row["Établissement"]}</b>
                    <span style='color:{brd}; font-weight:700;'>{row["Relance"]}</span>
                </div>
                <div style='font-size:12px; color:#888; margin-top:4px;'>
                    {row["Type"]} · {row["Produit"]} · Dernier contact : {row["Dernière action"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : STOCKS (admin)
# ══════════════════════════════════════════════════════════════════
elif "Stocks" in page:
    st.markdown("## 📦 Gestion des Stocks")
    st.markdown("*Dernière mise à jour : 09/06/2026 à 03:47 (import entrepositaire automatique)*")
    st.markdown("---")

    alertes = STOCKS[STOCKS["Statut"] != "OK"]
    if len(alertes) > 0:
        st.error(f"⚠️ {len(alertes)} SKU(s) en alerte ou avertissement — vérifiez les niveaux ci-dessous")

    col1, col2, col3 = st.columns(3)
    col1.metric("SKUs en stock", len(STOCKS))
    col2.metric("SKUs en alerte", len(STOCKS[STOCKS["Statut"] == "ALERTE"]), delta_color="inverse")
    col3.metric("Prochaine sync", "Demain 03:30")

    st.markdown("---")
    st.markdown("### Niveaux par SKU")
    for _, row in STOCKS.iterrows():
        pct = min(int(row["Stock (cartons)"] / (row["Seuil alerte"] * 3) * 100), 100)
        clr = "#27AE60" if row["Statut"] == "OK" else "#E67E22" if row["Statut"] == "WARNING" else "#C0392B"
        bar_color = "#27AE60" if row["Statut"] == "OK" else "#E67E22" if row["Statut"] == "WARNING" else "#C0392B"
        st.markdown(f"""
        <div style='background:white; border-radius:8px; padding:12px 16px; margin-bottom:8px;
                    box-shadow:0 1px 4px rgba(0,0,0,0.08);'>
            <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
                <span style='font-weight:600; font-size:13px;'>{row["SKU"]}</span>
                <span style='color:{clr}; font-weight:700;'>{row["Stock (cartons)"]} cartons
                    {"✅" if row["Statut"]=="OK" else "⚠️" if row["Statut"]=="WARNING" else "🔴"}</span>
            </div>
            <div style='background:#F0F0F0; border-radius:4px; height:8px;'>
                <div style='background:{bar_color}; width:{pct}%; height:8px; border-radius:4px;'></div>
            </div>
            <div style='font-size:10px; color:#AAA; margin-top:4px;'>Seuil alerte : {row["Seuil alerte"]} cartons</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PAGE : FACTURATION (admin)
# ══════════════════════════════════════════════════════════════════
elif "Facturation" in page:
    st.markdown("## 🧾 Facturation & Devis")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CA du mois", "4 320 €")
    col2.metric("Factures payées", "3")
    col3.metric("En attente", "1", "288 €")
    col4.metric("En retard", "1", "240 €", delta_color="inverse")

    st.markdown("---")
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown("### 📋 Toutes les factures")
        st.dataframe(FACTURES, use_container_width=True, hide_index=True)

    with col_right:
        st.markdown("### ➕ Nouvelle facture")
        client = st.selectbox("Client", ["Brasserie Lipp", "Bar du Marché", "Cave Legrand", "Autre..."])
        produit = st.selectbox("Produit", ["Krush (12x33cl)", "Kingdom (12x33cl)", "Indochine (12x33cl)", "Samaï (6x70cl)"])
        qte = st.number_input("Quantité (cartons)", min_value=1, value=10)
        prix_u = st.number_input("Prix unitaire HT (€)", value=12.0, step=0.5)
        total_ht = qte * prix_u
        st.markdown(f"**Total HT : {total_ht:.0f} €** · TVA : {total_ht*0.2:.0f} € · **TTC : {total_ht*1.2:.0f} €**")
        st.button("📄 Générer la facture PDF")

# ══════════════════════════════════════════════════════════════════
#  PAGE : COMPTA (admin)
# ══════════════════════════════════════════════════════════════════
elif "Compta" in page:
    st.markdown("## 💰 Comptabilité & Export macompta.fr")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("CA cumulé 2026", "14 280 €")
    col2.metric("TVA collectée", "2 856 €")
    col3.metric("Droits d'accise", "342 €")

    st.markdown("---")
    st.markdown("### 📊 Répartition CA par marque")
    ca_marque = pd.DataFrame({
        "Marque": ["Krush", "Kingdom", "Indochine", "Samaï", "Wingman"],
        "CA HT (€)": [6800, 3200, 2400, 1400, 480],
    })
    fig = px.pie(ca_marque, values="CA HT (€)", names="Marque",
                 color_discrete_sequence=["#1F3864","#C9A84C","#2980B9","#27AE60","#E67E22"])
    fig.update_layout(margin=dict(t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📤 Export macompta.fr")
    col1, col2 = st.columns(2)
    with col1:
        mois = st.selectbox("Mois à exporter", ["Juin 2026", "Mai 2026", "Avril 2026"])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("📥 Générer CSV macompta.fr")
    st.info("📌 Le CSV est prêt à importer directement dans macompta.fr (format FEC compatible)")

# ══════════════════════════════════════════════════════════════════
#  PAGE : RAPPORT SEMAINE (admin)
# ══════════════════════════════════════════════════════════════════
elif "Rapport" in page:
    st.markdown("## 📊 Rapport de la semaine")
    st.markdown("*Semaine du 02/06/2026 au 09/06/2026 — généré automatiquement chaque lundi à 8h*")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nouveaux prospects", "7", "+7")
    col2.metric("Emails envoyés", "12", "cette semaine")
    col3.metric("CA facturé", "768 €", "+288 € vs sem. préc.")
    col4.metric("Relances effectuées", "4")

    st.markdown("---")
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 🤝 Activité commerciale")
        activite = pd.DataFrame({
            "Action": ["Premiers contacts", "Relances J+7", "Relances J+14", "Réponses reçues", "RDV obtenus"],
            "Nb": [7, 3, 1, 2, 1],
        })
        fig = px.bar(activite, x="Action", y="Nb", color_discrete_sequence=["#1F3864"])
        fig.update_layout(showlegend=False, plot_bgcolor="white",
                          yaxis=dict(showgrid=True, gridcolor="#F0F0F0"),
                          margin=dict(t=10, b=10), xaxis_tickangle=-20)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("### 📦 Mouvements stocks")
        mvt = pd.DataFrame({
            "SKU": ["Krush Lime", "Krush Yuzu", "Kingdom IPA", "Indochine", "Samaï"],
            "Variation": [-18, -24, -12, -8, -6],
        })
        fig = px.bar(mvt, x="SKU", y="Variation", color_discrete_sequence=["#C9A84C"])
        fig.update_layout(showlegend=False, plot_bgcolor="white",
                          yaxis=dict(showgrid=True, gridcolor="#F0F0F0"),
                          margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🔍 Points d'attention")
    st.warning("⚠️ **Krush Yuzu Peach** : stock à 38 cartons — sous le seuil. Commander avant le 15/06.")
    st.warning("⚠️ **Wingman Lager** : stock à 12 cartons — rupture imminente.")
    st.error("🔴 **Facture NBC-2026-0008** (Bar du Marché, 240 €) en retard de paiement — relancer le client.")
    st.success("✅ **Mama Shelter** en phase négociation — potentiel 500€/mois récurrent.")

    st.markdown("---")
    st.button("📤 Envoyer ce rapport par email à la direction")

# ══════════════════════════════════════════════════════════════════
#  PAGE : PARAMÈTRES (admin)
# ══════════════════════════════════════════════════════════════════
elif "Paramètres" in page:
    st.markdown("## ⚙️ Paramètres")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["👤 Comptes utilisateurs", "📧 Configuration email", "🔗 Intégrations"])

    with tab1:
        st.markdown("### Utilisateurs NBC")
        users = pd.DataFrame([
            {"Nom": "Simon Cogné",     "Login": "simon", "Rôle": "Commercial", "Accès": "CRM · Emails"},
            {"Nom": "Direction NBC",   "Login": "admin", "Rôle": "Admin",      "Accès": "Tout"},
        ])
        st.dataframe(users, use_container_width=True, hide_index=True)
        st.button("➕ Ajouter un utilisateur")

    with tab2:
        st.markdown("### Configuration SMTP Infomaniak")
        st.text_input("Serveur SMTP", value="mail.infomaniak.com", disabled=True)
        st.text_input("Port", value="587 (TLS)", disabled=True)
        st.text_input("Expéditeur", value="simon.cogne2004@gmail.com")
        st.text_input("Mot de passe", type="password", value="••••••••")
        col1, col2 = st.columns(2)
        col1.button("💾 Sauvegarder")
        col2.button("📤 Tester l'envoi")

    with tab3:
        st.markdown("### Connexions actives")
        integrations = [
            ("✅", "Notion API",       "Connecté — workspace NBC", "#E8F5E9"),
            ("✅", "Infomaniak SMTP",  "Connecté — simon.cogne2004@gmail.com", "#E8F5E9"),
            ("⏳", "macompta.fr",      "Non configuré — cliquer pour connecter", "#FFF3E0"),
            ("⏳", "Entrepositaire",   "Import auto actif — 03:30 chaque nuit", "#E8F5E9"),
        ]
        for icon, name, status, bg in integrations:
            st.markdown(f"""
            <div style='background:{bg}; border-radius:8px; padding:12px 16px; margin-bottom:8px;'>
                <b>{icon} {name}</b> — <span style='color:#555; font-size:13px;'>{status}</span>
            </div>
            """, unsafe_allow_html=True)
