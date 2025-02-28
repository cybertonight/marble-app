import streamlit as st

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

import numpy as np
import pandas as pd

# Dictionnaire associant chaque ligue à son emoji drapeau
league_flags = {
    "LIGA": "🇪🇸",
    "LIGUE 1": "🇫🇷",
    "SFERA SERIE A": "🇮🇹",
    "MEISTRILIIGA": "🇪🇪",
    "BLACKPINK K LEAGUE": "🇰🇷"
}

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

def simuler_course():
    Bilan = pd.DataFrame()
    Bilan["Bille"] = st.session_state.Liste_billes[:num_billes]
    Bilan["Statut"] = "OK"
    Bilan["Total"] = 0
    
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

    # Récupération de l'emoji associé à la ligue sélectionnée
    league = st.session_state.get("current_league", None)
    flag = league_flags.get(league, "")

    # Création du tableau final avec Position, Nom, Emoji et Temps total
    ranking = pd.DataFrame({
        "Position": range(1, len(Bilan) + 1),
        "Nom": Bilan["Bille"],
        "Emoji": flag,
        "Temps total": Bilan["Total"]
    })
    
    # Résultats
    result_text = ""
    rang = 0
    best_time = Bilan.iloc[rang]["Total"]
    result_text += (f"{rang+1}. {Bilan.iloc[rang]['Bille']} | "
                    f"{Bilan.iloc[rang]['Total']:.2f}".replace(".", "''") + "\n").replace("+nan", "DNF")
    
    for rang in range(1, len(Bilan["Bille"])):
        result_text += (f"{rang+1}. {Bilan.iloc[rang]['Bille']} | +"
                        f"{(Bilan.iloc[rang]['Total'] - best_time):.2f}".replace(".", "''") + "\n").replace("+nan", "DNF")
    
    return ranking, result_text

if st.button("Lancer la course"):
    ranking_df, result_text = simuler_course()
    st.table(ranking_df)  # Affichage du tableau avec position, nom, emoji et temps total
    st.text_area("Résultats de la course (texte)", result_text, height=300)
