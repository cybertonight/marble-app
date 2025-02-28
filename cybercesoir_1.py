import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title = "CYBERCESOIR.FR",
    page_icon = ":hundred_points",
    layout = "wide")

#HEADER
with st.container():
    st.subheader("Salut.")
    st.title("C'est Marc.")
    st.write("Le youtubeur multigaming.")
    st.write("Hop là.")

# Interface Streamlit
st.title("Simulation de course de billes")

# Sélection du nombre de billes
num_billes = st.slider("Nombre de billes", min_value=4, max_value=16, value=8)

# Initialisation de session_state pour conserver les noms des billes
if "Liste_billes" not in st.session_state:
    st.session_state.Liste_billes = [f"Bille {i+1}" for i in range(16)]

# Case à cocher pour verrouiller les noms
if "verrouillage_billes" not in st.session_state:
    st.session_state.verrouillage_billes = [False] * 16

# Options de présélection
liga_villes = ["Madrid", "Barcelone", "Séville", "Valence", "Bilbao", "San Sebastián", "Vigo", "Grenade", "Malaga", "Saragosse", "Majorque", "La Corogne", "Gijón", "Cadix", "Murcie", "Alicante"]
ligue1_villes = ["Paris", "Marseille", "Lyon", "Lille", "Nice", "Rennes", "Strasbourg", "Nantes", "Toulouse", "Montpellier", "Reims", "Brest", "Metz", "Le Havre", "Clermont", "Lens"]
sfera_serie_a_villes = ["Rome", "Milan", "Turin", "Naples", "Florence", "Gênes", "Bologne", "Vérone", "Venise", "Palermo", "Cagliari", "Parme", "Bari", "Bergame", "Udine", "Sassuolo"]
meistriliiga_villes = ["Tallinn", "Tartu", "Narva", "Parnu", "Viljandi", "Rakvere", "Kuressaare", "Voru", "Haapsalu", "Johvi", "Maardu", "Rapla", "Paide", "Keila", "Kohtla-Järve", "Sillamäe"]
blackpink_k_league_villes = ["Séoul", "Busan", "Incheon", "Daegu", "Gwangju", "Daejeon", "Suwon", "Ulsan", "Jeonju", "Changwon", "Goyang", "Pohang", "Jeju", "Seongnam", "Ansan", "Anyang"]

cols_buttons = st.columns(5)
with cols_buttons[0]:
    if st.button("LIGA"):
        for i in range(num_billes):
            if not st.session_state.verrouillage_billes[i]:
                st.session_state.Liste_billes[i] = liga_villes[i]
with cols_buttons[1]:
    if st.button("LIGUE 1"):
        for i in range(num_billes):
            if not st.session_state.verrouillage_billes[i]:
                st.session_state.Liste_billes[i] = ligue1_villes[i]
with cols_buttons[2]:
    if st.button("SFERA SERIE A"):
        for i in range(num_billes):
            if not st.session_state.verrouillage_billes[i]:
                st.session_state.Liste_billes[i] = sfera_serie_a_villes[i]
with cols_buttons[3]:
    if st.button("MEISTRILIIGA"):
        for i in range(num_billes):
            if not st.session_state.verrouillage_billes[i]:
                st.session_state.Liste_billes[i] = meistriliiga_villes[i]
with cols_buttons[4]:
    if st.button("BLACKPINK K LEAGUE"):
        for i in range(num_billes):
            if not st.session_state.verrouillage_billes[i]:
                st.session_state.Liste_billes[i] = blackpink_k_league_villes[i]

# Saisie des noms des billes sous forme de colonnes
cols = st.columns(4)
for i in range(num_billes):
    with cols[i % 4]:
        st.session_state.Liste_billes[i] = st.text_input(f"Bille {i+1}", st.session_state.Liste_billes[i], key=f"bille_{i}")
        st.session_state.verrouillage_billes[i] = st.checkbox("Verrouiller", st.session_state.verrouillage_billes[i], key=f"lock_{i}")

# Fonction pour ajouter l'emoji du drapeau en fonction de la ligue
def obtenir_emoji_drapeau(league):
    ligues_drapeaux = {
        "LIGA": "🇪🇸",
        "LIGUE 1": "🇫🇷",
        "SFERA SERIE A": "🇮🇹",
        "MEISTRILIIGA": "🇪🇪",
        "BLACKPINK K LEAGUE": "🇰🇷"
    }
    return ligues_drapeaux.get(league, "🏳️")

def simuler_course():
    Bilan = pd.DataFrame()
    Bilan["Bille"] = st.session_state.Liste_billes[:num_billes]
    Bilan["Statut"] = "OK"
    Bilan["Total"] = 0
    Bilan["Pays"] = [""] * num_billes  # Pour les pays (avec emoji)
    
    # Paramètres de la course
    temps_borne_min = 25
    temps_borne_max = 35
    total_tronçons = 4
    tronçons = np.random.uniform(temps_borne_min, temps_borne_max, total_tronçons)
    
    def accident(temps, bille):
        accident_types = ["None", "Light", "Heavy"]
        accident_prob = [0.94, 0.05, 0.01]
        accident_type = np.random.choice(accident_types, p=accident_prob)
        if accident_type == "None":
            return temps
        elif accident_type == "Light":
            delay = np.random.uniform(2.5, 3.5)
            return temps + delay
        elif accident_type == "Heavy":
            return np.nan
    
    # Simulation de la course
    for i in range(total_tronçons):
        lis_tro = []
        for bille in range(len(Bilan["Bille"])):
            hazard = np.random.uniform(0.9, 1.1)
            temps = hazard * tronçons[i]
            temps = accident(temps, bille)
            lis_tro.append(temps)
        Bilan[f'Tronçon_{i+1}'] = lis_tro
        Bilan["Total"] += lis_tro
        Bilan = Bilan.sort_values("Total")
    
    # Ajout des emojis de drapeau pour chaque bille selon sa ligue
    for i in range(num_billes):
        ligue = None
        if i < 4: ligue = "LIGA"
        elif i < 8: ligue = "LIGUE 1"
        elif i < 12: ligue = "SFERA SERIE A"
        elif i < 14: ligue = "MEISTRILIIGA"
        else: ligue = "BLACKPINK K LEAGUE"
        
        Bilan.at[i, "Pays"] = obtenir_emoji_drapeau(ligue)

    # Résultats sous forme de tableau
    Bilan["Position"] = Bilan["Total"].rank(method="min", ascending=True)
    Bilan["Temps Total"] = Bilan["Total"].apply(lambda x: f"{x:.2f}".replace(".", "''"))
    
    # Réorganiser les colonnes
    Bilan = Bilan[["Position", "Bille", "Pays", "Temps Total"]]
    
    # Affichage du tableau avec le style souhaité
    st.dataframe(Bilan.style.set_table_styles(
        [{'selector': 'thead th', 'props': [('text-align', 'center'), ('font-size', '20px')]},  # En-tête centré
         {'selector': 'tbody td', 'props': [('text-align', 'center'), ('font-size', '18px')]}],  # Corps centré
        hide_index=True))  # Masquer la colonne index

if st.button("Lancer la course"):
    result = simuler_course()
    st.text_area("Résultats de la course", result, height=300)
