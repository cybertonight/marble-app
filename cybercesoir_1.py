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

# Interface Streamlit
st.title("Simulation de course de billes")

# Sélection du nombre de billes
num_billes = st.slider("Nombre de billes", min_value=4, max_value=16, value=8)

# Initialisation de session_state pour conserver les noms des billes
if "Liste_billes" not in st.session_state:
    st.session_state.Liste_billes = [f"Bille {i+1}" for i in range(16)]

# Options de présélection
liga_villes = ["Madrid", "Barcelone", "Séville", "Valence", "Bilbao", "San Sebastián", "Vigo", "Grenade", "Malaga", "Saragosse", "Majorque", "La Corogne", "Gijón", "Cadix", "Murcie", "Alicante"]
ligue1_villes = ["Paris", "Marseille", "Lyon", "Lille", "Nice", "Rennes", "Strasbourg", "Nantes", "Toulouse", "Montpellier", "Reims", "Brest", "Metz", "Le Havre", "Clermont", "Lens"]
sfera_serie_a_villes = ["Rome", "Milan", "Turin", "Naples", "Florence", "Gênes", "Bologne", "Vérone", "Venise", "Palermo", "Cagliari", "Parme", "Bari", "Bergame", "Udine", "Sassuolo"]
meistriliiga_villes = ["Tallinn", "Tartu", "Narva", "Parnu", "Viljandi", "Rakvere", "Kuressaare", "Voru", "Haapsalu", "Johvi", "Maardu", "Rapla", "Paide", "Keila", "Kohtla-Järve", "Sillamäe"]
blackpink_k_league_villes = ["Séoul", "Busan", "Incheon", "Daegu", "Gwangju", "Daejeon", "Suwon", "Ulsan", "Jeonju", "Changwon", "Goyang", "Pohang", "Jeju", "Seongnam", "Ansan", "Anyang"]

cols_buttons = st.columns(5)
leagues = [liga_villes, ligue1_villes, sfera_serie_a_villes, meistriliiga_villes, blackpink_k_league_villes]
labels = ["LIGA", "LIGUE 1", "SFERA SERIE A", "MEISTRILIIGA", "BLACKPINK K LEAGUE"]

for i, (label, league) in enumerate(zip(labels, leagues)):
    with cols_buttons[i]:
        if st.button(label):
            st.session_state.Liste_billes[:num_billes] = league[:num_billes]

# Saisie des noms des billes sous forme de colonnes compactes
cols = st.columns(4)
for i in range(num_billes):
    with cols[i % 4]:
        st.session_state.Liste_billes[i] = st.text_input(f"Bille {i+1}", st.session_state.Liste_billes[i], key=f"bille_{i}", placeholder="Nom de la bille")

def simuler_course():
    Bilan = pd.DataFrame()
    Bilan["Bille"] = st.session_state.Liste_billes[:num_billes]
    Bilan["Total"] = 0
    
    # Paramètres de la course
    temps_borne_min = 25
    temps_borne_max = 35
    total_tronçons = 4
    tronçons = np.random.uniform(temps_borne_min, temps_borne_max, total_tronçons)
    
    def accident(temps):
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
        Bilan["Total"] += [accident(np.random.uniform(0.9, 1.1) * tronçons[i]) for _ in range(num_billes)]
    
    Bilan = Bilan.sort_values("Total", ascending=True, na_position="last").reset_index(drop=True)
    Bilan.insert(0, "POSITION", Bilan.index + 1)
    Bilan["Total"] = Bilan["Total"].apply(lambda x: "DNF" if pd.isna(x) else f"{x:.2f}")
    
    return Bilan

if st.button("Lancer la course"):
    result = simuler_course()
    st.markdown("""
    <style>
        .dataframe { margin-left: auto; margin-right: auto; width: 80%; }
    </style>
    """, unsafe_allow_html=True)
    st.dataframe(result)
