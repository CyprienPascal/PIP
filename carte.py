import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Résultats des Élections",
    layout="wide",
)
def apply_custom_design():
    """
    Applique un style CSS avancé pour l'application Streamlit.
    """
    st.markdown(
        """
        <style>
        /* Style général du corps */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f2f6;
            margin: 0;
            padding: 0;
        }

        /* Titres */
        h1, h2, h3 {
            color: #003366;
            font-weight: bold;
            margin-bottom: 20px;
        }

        h1 {
            text-align: center;
            font-size: 2.5em;
        }

        h2 {
            font-size: 2em;
            margin-top: 1em;
        }

        h3 {
            font-size: 1.5em;
        }

        /* Boutons */
        .stButton button {
            background-color: #00509e;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
            font-size: 16px;
            cursor: pointer;
        }

        .stButton button:hover {
            background-color: #003f7f;
        }

        /* Tableaux */
        .dataframe {
            border: 1px solid #ccc;
            border-radius: 10px;
            overflow: hidden;
        }

        table.dataframe {
            margin: 0 auto;
            font-size: 14px;
            color: #333;
        }

        table.dataframe th {
            background-color: #00509e;
            color: white;
            font-weight: bold;
            padding: 10px;
            text-align: center;
        }

        table.dataframe td {
            background-color: #f9f9f9;
            padding: 10px;
            text-align: center;
        }

        table.dataframe tr:nth-child(even) {
            background-color: #f0f4f7;
        }

        /* Graphiques */
        .main-svg {
            background-color: white !important;
            border-radius: 10px;
            padding: 10px;
        }

        /* Boîte latérale (sidebar) */
        .stSidebar {
            background-color: #e6effc;
        }

        .stSidebar h1, .stSidebar h2, .stSidebar h3 {
            color: #004080;
        }

        /* Entrées utilisateur */
        .stTextInput, .stSelectbox, .stNumberInput, .stDateInput {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
        }

        .stTextInput:hover, .stSelectbox:hover, .stNumberInput:hover, .stDateInput:hover {
            border-color: #00509e;
        }

        /* Amélioration des marges */
        .block-container {
            padding: 20px;
            max-width: 1200px;
        }

        /* Lien */
        a {
            color: #00509e;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


apply_custom_design()
def load_unemployment_data():
    try:
        return pd.read_csv('taux_chomage_par_departement.csv')
    except FileNotFoundError:
        st.error("Fichier 'taux_chomage_par_departement.csv' introuvable. Veuillez le placer dans le même répertoire que le script.")
        return pd.DataFrame()

# Charger les données démographiques
@st.cache_data
def load_demographic_data():
    try:
        return pd.read_csv('donnees_2017_2022.csv')
    except FileNotFoundError:
        st.error("Fichier 'donnees_2017_2022.csv' introuvable. Veuillez le placer dans le même répertoire que le script.")
        return pd.DataFrame()

# Charger les données principales
@st.cache_data
def load_data():
    try:
        return pd.read_csv('data_elections.csv', low_memory=False)
    except FileNotFoundError:
        st.error("Fichier 'data_elections.csv' introuvable. Assurez-vous qu'il est dans le même répertoire que le script.")
        return pd.DataFrame()

# Charger les données de pauvreté
@st.cache_data
def load_poverty_data():
    try:
        return pd.read_csv('moyenne_pauvrete_par_departement.csv')
    except FileNotFoundError:
        st.error("Fichier 'moyenne_pauvrete_par_departement.csv' introuvable. Veuillez le placer dans le même répertoire que le script.")
        return pd.DataFrame()

# Charger les données principales
df = load_data()

if df.empty:
    st.stop()

# Convertir les colonnes numériques si nécessaire
colonnes_a_convertir = ['Inscrits', 'Abstentions', '% Abs/Ins', 'Votants', '% Vot/Ins', 'Blancs', '% Blancs/Ins',
                        'Nuls', '% Nuls/Ins', '% Nuls/Vot', 'Exprimés', '% Exp/Ins', '% Exp/Vot']
for colonne in colonnes_a_convertir:
    if colonne in df.columns:
        df[colonne] = pd.to_numeric(df[colonne], errors='coerce')
# Gestion de la navigation entre les pages
page = st.sidebar.radio("", ["Présentation","Résultat des élections","Analyse globale de la population française","Analyse sur le chomage","Analyse sur le revenu","Cas de la Haute-Garonne","Analyse Générale de l'Abstention Électorale",
"Analyse Approfondie de l'Abstention et de ses Liens Socio-économiques","Résultat sur le vote et audiovisuel"], horizontal= False)

# Dictionnaire pour mapper les ID d'élections aux noms complets
id_to_name = {
    "2017_legi_t1": "Législative 2017 Tour 1",
    "2017_legi_t2": "Législative 2017 Tour 2",
    "2022_legi_t1": "Législative 2022 Tour 1",
    "2022_legi_t2": "Législative 2022 Tour 2",
    "2024_legi_t1": "Législative 2024 Tour 1",
    "2024_legi_t2": "Législative 2024 Tour 2"
}

if page == "Présentation":
    st.markdown(
    """
    <h1 style='font-size:24px; font-weight:bold;'>Présentation du Projet</h1>
    """,
    unsafe_allow_html=True
)

    st.markdown("Comment le paysage politique français a-t-il évolué depuis l'élection d'Emmanuel Macron, et quels facteurs socio-démographiques influencent les choix électoraux ou l'engagement politique des citoyens français ?")
    st.image("parti_politique.png",width=500)
    st.markdown("Ce dashboard présente les résultats d’un projet interpromotionnel réalisé dans le cadre du master SID à l’Université Paul Sabatier. Notre groupe s’est concentré sur l’analyse des élections françaises sous l’ère Macron. Ce projet porte sur les élections législatives de 2017, 2022 et 2024, en mettant en parallèle une analyse socio-démographique de la population française depuis 2017.")
    st.markdown("Ce dashboard vous sera présenté par :")
    st.markdown("""
<style>
  ul {
    list-style-type: none;
    padding: 0;          
    margin: 0;           
  }

  li {
    line-height: 1.2; 
  }
</style>
<ul>
  <li>Bougares Mazen</li>
  <li>Mailhes Alexia</li>
  <li>Niyazaliev Sardor</li>
  <li>Belhaj Mohamed-Taha</li>
  <li>Brun Morgan</li>
  <li>Konta Gaoussou Maouloud</li>
  <li>Pascal Cyprien</li>
</ul>
""", unsafe_allow_html=True)
if page == "Résultat des élections":
    # Titre principal
    st.title("Résultats des Élections")

    # Sélection du type d'élection
    election_type = st.radio("Type d'élection", ["Présidentielles", "Législatives"], horizontal=True)

    # Sélection des paramètres communs
    annee = st.selectbox("Année", ["2017", "2022"] + (["2024"] if election_type == "Législatives" else []))
    tour = st.selectbox("Tour", ["T1", "T2"])

    # Génération du nom de fichier en fonction du type d'élection
    if election_type == "Présidentielles":
        if annee == "2017":
            if tour== "T1":
                st.components.v1.html(open("resultats_electoraux_interactifs_2017_T1.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
            if tour == "T2":
                st.components.v1.html(open("resultats_electoraux_interactifs_2017_T2.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
        if annee == "2022":
            if tour== "T1":
                st.components.v1.html(open("resultats_electoraux_interactifs_2022_T1.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
            if tour == "T2":
                st.components.v1.html(open("resultats_electoraux_interactifs_2022_T2.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
    if election_type == "Législatives":
        niveau = st.selectbox("Niveau", ["Circonscription", "Département"])
        if niveau =="Circonscription":
            if annee == "2017":
                if tour== "T1":
                    st.components.v1.html(open("res_2017_T1_circo_circo.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
                if tour == "T2":
                    st.components.v1.html(open("res_2017_T2_circo_circo.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
            if annee == "2022":
                if tour== "T1":
                    st.components.v1.html(open("res_2022_T1_circo_circo.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
                if tour == "T2":
                    st.components.v1.html(open("res_2022_T2_circo_circo.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
            if annee == "2024":
                if tour== "T1":
                    st.components.v1.html(open("res_2024_T2_circo_circo.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
                if tour == "T2":
                    st.components.v1.html(open("res_2024_T2_circo_circo.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
        if niveau =="Département":
            if annee == "2017":
                if tour== "T1":
                    st.components.v1.html(open("res_2017_T1_dept.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
                if tour == "T2":
                    st.components.v1.html(open("res_2017_T2_dept.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
            if annee == "2022":
                if tour== "T1":
                    st.components.v1.html(open("res_2022_T1_dept.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
                if tour == "T2":
                    st.components.v1.html(open("res_2022_T2_dept.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
            if annee == "2024":
                if tour== "T1":
                    st.components.v1.html(open("res_2024_T1_dept.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
                if tour == "T2":
                    st.components.v1.html(open("res_2024_T2_dept.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
        # Ajout d'images pour les législatives
        st.image("voteevol.png", caption="Evolution du vote au fil des années",width=600)
        st.image("piechart.png", caption="répartition des votes pour le premier tour")
        if file_name:
            st.components.v1.html(open(file_name, "r", encoding="utf-8").read(), height=600, scrolling=True)
            # Affichage du texte contextuel basé sur l'année et le tour
        if election_type == "Législatives":
            st.markdown(f"**Analyse des résultats pour le {tour.lower().replace('t', 'tour ')} de l'année {annee} :**")
            st.markdown("Ces cartes montrent le résultat des élections législatives depuis l'élection de M.Macron en 2017.")
            if tour == "T2":
                st.markdown("De plus, si un département ou une circonscription manque sur le Tour 2 c'est qu'il a gagné au Tour 1.")
    
if page == "Analyse sur le chomage":
    st.title("Analyse sur le chomage")
    annee = st.selectbox("Année", ["2017", "2022","2024"])
    col1, col2 = st.columns(2)
    with col1:
        st.image("evolution_chomage.png", caption="")
    with col2:
        st.image("evolution_taux_chom_dep.png", caption="")
    if annee == "2017":
        with col1:
            st.image("Carte_classes_taux_chom.png", caption="")
            st.image("repartition_vote_classe_taux_chom.png", caption="")
        with col2:
            st.components.v1.html(open("res_2017_T1_dept.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
    if annee == "2022":
        with col1:
            st.image("Carte_classes_taux_chom_2022.png", caption="")
            st.image("repartition_vote_classe_taux_chom_2022.png", caption="")
        with col2:
            st.components.v1.html(open("res_2022_T1_dept.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
    if annee == "2024":
        with col1:
            st.image("Carte_classes_taux_chom_2024.png", caption="")
            st.image("repartition_vote_classe_taux_chom_2024.png", caption="")
        with col2:
            st.components.v1.html(open("res_2024_T1_dept.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
    

if page == "Analyse sur le revenu":
        # Liste permettant l'affichage des graphiques
    annees = ["2017", "2018", "2019", "2020", "2021"]
    deciles = ["1", "2", "3", "7", "8", "9"]
    
    # Fonction pour charger et afficher un fichier HTML (pour les maps interactives)
    def display_map_from_html(html_file):
        # Vérifier si le fichier existe
        if os.path.exists(html_file):
            # Charger le fichier HTML
            with open(html_file, "r",encoding="utf-8") as file:
                map_html = file.read()
            # Afficher le fichier HTML dans Streamlit
            st.components.v1.html(map_html, height=500, width=700)
        else:
            st.error("Le fichier HTML n'a pas été trouvé.")
    
    # Récupération du DataFrame permettant d'obtenir les graphiques
    df_data_departements = pd.read_csv("departements_pauvrete.csv")
    
    # Titre de la page
    st.title("Analyse de la pauvreté par département")
    
    
    ####################
    # LISTE DEROULANTE #
    ####################
    
    # Liste déroulante pour choisir un département
    dept_options = {
        row["dept"]: f"{row['dept']} - {row['lib_dept']}"
        for _, row in df_data_departements.iterrows()
    }
    
    # Liste déroulante affichant le nom complet, mais retournant uniquement le numéro du département
    selected_dept = st.selectbox(
        "Sélectionnez le département à analyser :",
        options=list(dept_options.keys()),  # Clés (numéros de département) pour la sélection
        format_func=lambda dept: dept_options[dept]  # Formattage pour afficher le nom complet
    )
    
    
    ###############
    # LES DONNEES #
    ###############
    
    # Filtrer les données pour le département sélectionné
    filtered_data = df_data_departements[df_data_departements['dept'] == selected_dept]
    
    # Récupérer le nombre de qpv pour ce département
    y_nbr_qpv = [filtered_data['nb_qpv_2017'].values[0], filtered_data['nb_qpv_2018'].values[0], filtered_data['nb_qpv_2019'].values[0],
        filtered_data['nb_qpv_2020'].values[0],
        filtered_data['nb_qpv_2021'].values[0]]
        
    # Les données pour les différents déciles
    # 1er décile
    y_decile_1 = [filtered_data['revenu_disp_d1_2017'].values[0], filtered_data['revenu_disp_d1_2018'].values[0], filtered_data['revenu_disp_d1_2019'].values[0],
        filtered_data['revenu_disp_d1_2020'].values[0],
        filtered_data['revenu_disp_d1_2021'].values[0]]
        
    # 2ème décile
    y_decile_2 = [filtered_data['revenu_disp_d2_2017'].values[0], filtered_data['revenu_disp_d2_2018'].values[0], filtered_data['revenu_disp_d2_2019'].values[0],
        filtered_data['revenu_disp_d2_2020'].values[0],
        filtered_data['revenu_disp_d2_2021'].values[0]]
    
    # 3ème décile
    y_decile_3 = [filtered_data['revenu_disp_d3_2017'].values[0], filtered_data['revenu_disp_d3_2018'].values[0], filtered_data['revenu_disp_d3_2019'].values[0],
        filtered_data['revenu_disp_d3_2020'].values[0],
        filtered_data['revenu_disp_d3_2021'].values[0]]
    
    # 7ème décile
    y_decile_7 = [filtered_data['revenu_disp_d7_2017'].values[0], filtered_data['revenu_disp_d7_2018'].values[0], filtered_data['revenu_disp_d7_2019'].values[0],
        filtered_data['revenu_disp_d7_2020'].values[0],
        filtered_data['revenu_disp_d7_2021'].values[0]]
    
    # 8ème décile
    y_decile_8 = [filtered_data['revenu_disp_d8_2017'].values[0], filtered_data['revenu_disp_d8_2018'].values[0], filtered_data['revenu_disp_d8_2019'].values[0],
        filtered_data['revenu_disp_d8_2020'].values[0],
        filtered_data['revenu_disp_d8_2021'].values[0]]
    
    # 9ème décile
    y_decile_9 = [filtered_data['revenu_disp_d9_2017'].values[0], filtered_data['revenu_disp_d9_2018'].values[0], filtered_data['revenu_disp_d9_2019'].values[0],
        filtered_data['revenu_disp_d9_2020'].values[0],
        filtered_data['revenu_disp_d9_2021'].values[0]]
        
        
    # Les pourcentages d'augmentation par décile au fur et à mesure des années
    x_pourcentage = [filtered_data['pourc_augm_d1'].values[0], filtered_data['pourc_augm_d2'].values[0], filtered_data['pourc_augm_d3'].values[0],
        filtered_data['pourc_augm_d7'].values[0],
        filtered_data['pourc_augm_d8'].values[0], filtered_data['pourc_augm_d9'].values[0]]
    
    
    
    #############
    # AFFICHAGE #
    #############
    
    # Graphique du haut
    with st.container():
        st.subheader(f"Diagramme montrant le nombre de QPV étudié pour le département {selected_dept}")
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        ax1.bar(annees, y_nbr_qpv)
        ax1.set_title(f"Nombre de QPV par année pour le département {selected_dept}")
        ax1.set_xlabel("Années")
        ax1.set_ylabel("Nombre de QPV")
        # Afficher le graphique
        st.pyplot(fig1)
    
    
    # Les deux graphiques du milieu
    st.subheader(f"Diagrammes mesurant les évolutions du revenu médian pour le dépt. {selected_dept}")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fig2, ax2 = plt.subplots(figsize=(12, 6))
            ax2.plot(annees, y_decile_1)
            ax2.plot(annees, y_decile_2)
            ax2.plot(annees, y_decile_3)
            ax2.plot(annees, y_decile_7)
            ax2.plot(annees, y_decile_8)
            ax2.plot(annees, y_decile_9)
            ax2.set_title(f"Évolution des révenus médians par unité de consommation pour le département {selected_dept}")
            ax2.set_xlabel("Années")
            ax2.set_ylabel("revenus disponibles (en euros)")
            # Afficher le graphique
            st.pyplot(fig2)
    
        with col2:
            fig3, ax3 = plt.subplots(figsize=(12, 6))
            ax3.barh(deciles, x_pourcentage)
            ax3.set_title(f"Évolution des revenus en pourcentage pour le département {selected_dept}")
            ax3.set_xlabel("déciles")
            ax3.set_ylabel("Augmentation (en %)")
            # Afficher le graphique
            st.pyplot(fig3)
    
    
    # Le graphique du bas
    with st.container():
        st.subheader("Carte représentant la pauvreté au sein des départements métropolitains")
        col_type, col_annee = st.columns(2)
        
        # Les boutons
        with col_type:
            # Créer des boutons pour le choix du type de carte (Taux de Pauvreté ou Revenu Médian)
            map_type = st.radio("Choisissez le type de carte :", ("Taux de Pauvreté", "Revenu Médian"))
    
        with col_annee:
            # Créer des boutons pour le choix de l'année (2017 ou 2021)
            year = st.radio("Choisissez l'année :", (2017, 2021))
    
        # Sélectionner la carte en fonction des choix
        if map_type == "Taux de Pauvreté":
            if year == 2017:
                map_to_display = "map_taux_pauv_departements_2017.html"  # Carte Taux de Pauvreté 2017
            else:
                map_to_display = "map_taux_pauv_departements_2021.html"  # Carte Taux de Pauvreté 2021
        elif map_type == "Revenu Médian":
            if year == 2017:
                map_to_display = "map_revenu_departements_2017.html"  # Carte Revenu Médian 2017
            else:
                map_to_display = "map_revenu_departements_2021.html"  # Carte Revenu Médian 2021
    
        # Afficher la carte sélectionnée
        display_map_from_html(map_to_display)

if page == "Résultat sur le vote et audiovisuel":
    df_all = pd.read_csv("df_all_export.csv", delimiter=';')
    df_all['Voix'] = pd.to_numeric(df_all['Voix'], errors='coerce')
    df_all['Elu'] = pd.to_numeric(df_all['Elu'], errors='coerce')
    
    # Options disponibles
    relevant_years = [2002, 2007, 2012, 2017, 2022, 2024]
    available_sexes = df_all['Sexe'].unique()
    
    # Interface utilisateur
    st.title("Analyse des Données Électorales")
    
    # Sélection de l'année
    selected_year = st.selectbox("Choisir l'Année", relevant_years, index=relevant_years.index(2022))
    
    # Filtrer par sexe
    selected_sexes = st.multiselect("Filtrer par sexe", available_sexes, default=list(available_sexes))
    
    # Graphique des élections
    st.subheader(f"Élections {selected_year} : Voix et Élus par Nuance")
    
    # Filtrer les données pour l'année et le sexe sélectionnés
    filtered = df_all[(df_all['Annee'] == selected_year) & (df_all['Sexe'].isin(selected_sexes))]
    
    # Vérifier si les données filtrées ne sont pas vides
    if filtered.empty:
        st.warning("Aucune donnée disponible pour les sélections actuelles.")
    else:
        # Regrouper les données par Nuance
        grouped = filtered.groupby("Nuance").agg({"Voix": "sum", "Elu": "sum"}).reset_index()
        grouped = grouped.sort_values("Voix", ascending=False)
        
        # Vérifier les données regroupées
        st.write("Aperçu des données utilisées pour le graphique :", grouped)
    
        # Créer le graphique
        fig_election = go.Figure()
        fig_election.add_trace(go.Bar(
            x=grouped["Nuance"],
            y=grouped["Voix"],
            name="Voix",
            marker_color='blue',
            text=grouped["Voix"],
            textposition='outside'  # Change la position du texte
        ))
        fig_election.add_trace(go.Bar(
            x=grouped["Nuance"],
            y=grouped["Elu"],
            name="Élus",
            marker_color='orange',
            text=grouped["Elu"],
            textposition='outside'  # Change la position du texte
        ))
    
        # Mise en page et affichage
        fig_election.update_layout(
            title="Voix et Élus par Nuance",
            xaxis_title="Nuance (Parti)",
            yaxis_title="Nombre total",
            barmode='group',
            bargap=0.15,
            plot_bgcolor="white",  # Fond blanc pour un meilleur contraste
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True),
            legend_title="Légende",
            font=dict(size=12),
            margin=dict(l=40, r=40, t=60, b=40),  # Marges ajustées
            width=800,  # Largeur fixe
            height=600  # Hauteur fixe
        )
    
        # Afficher le graphique
        st.plotly_chart(fig_election)
            
if page == "Cas de la Haute-Garonne":
    # Fonction pour charger et afficher un fichier HTML (pour les maps interactives)
    def display_map_from_html(html_file):
        # Vérifier si le fichier existe
        if os.path.exists(html_file):
            # Charger le fichier HTML
            with open(html_file, "r",encoding="utf-8") as file:
                map_html = file.read()
            # Afficher le fichier HTML dans Streamlit
            st.components.v1.html(map_html, height=500, width=700)
        else:
            st.error("Le fichier HTML n'a pas été trouvé.")
            
    def display_map_from_html2(html_file):
        # Vérifier si le fichier existe
        if os.path.exists(html_file):
            # Charger le fichier HTML
            with open(html_file, "r",encoding="utf-8") as file:
                map_html = file.read()
            # Afficher le fichier HTML dans Streamlit
            st.components.v1.html(map_html, height=400, width=400)
        else:
            st.error("Le fichier HTML n'a pas été trouvé.")
            
    df_circonscription = pd.read_csv('resultats_graphiques_partis.csv')

    # Titre de la page
    st.title("Cartes comparants la pauvreté par circonscription en Haute-Garonne aux résultats des votes durant les législatives 2022")


    #############
    # AFFICHAGE #
    #############

    # Les deux cartes du haut
    st.subheader("Résultats du 1er et 2nd tour des élections législatives de 2022 en Haute-Garonne")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            map_tour_1 = "res_2022_T1_circo_Haute_Garonne.html"
            display_map_from_html2(map_tour_1)
        with col2:
            map_tour_2 = "res_2022_T2_circo_Haute_Garonne.html"
            display_map_from_html2(map_tour_2)


    # La carte du bas
    with st.container():
        st.subheader("Visualisation de la pauvreté au sein des circonscriptions de la Haute-Garonne en 2022")

        # Créer des boutons pour le choix du type de carte (Taux de Pauvreté ou Revenu Médian)
        map_type = st.radio("Choisissez le type de carte :", ("Taux de Pauvreté", "Revenu Médian"))

        # Sélectionner la carte en fonction des choix
        if map_type == "Taux de Pauvreté":
            map_to_display = "map_circonscription_Haute_Garonne_taux.html"
        elif map_type == "Revenu Médian":
            map_to_display = "map_circonscription_Haute_Garonne_revenu.html"

        # Afficher la carte sélectionnée
        display_map_from_html(map_to_display)


    # Le graphique du bas
    with st.container():
        st.subheader("Graphique mettant en avant l'orientation des votes selon le taux de pauvreté présent dans la circonscription en Haute-Garonne")

        fig1, ax1 = plt.subplots(figsize=(10, 4))
        
        # Les données
        gauche = df_circonscription['gauche'].tolist()
        extr_gauche = df_circonscription['extr_gauche'].tolist()
        centre = df_circonscription['centre'].tolist()
        droite = df_circonscription['droite'].tolist()
        extr_droite = df_circonscription['extr_droite'].tolist()
        divers = df_circonscription['divers'].tolist()
        
        categories = ['< 10', '10-14', '14-18', '18-20', '> 20']

        # Positions des barres
        x = np.arange(len(categories))
        
        ax1.bar(x, extr_gauche, label='Extreme gauche', color='#8B0000')
        ax1.bar(x, gauche, bottom=extr_gauche, label='Gauche', color='red')
        ax1.bar(x, centre, bottom=np.array(extr_gauche) + np.array(gauche), label='Centre', color='yellow')
        ax1.bar(x, droite, bottom=np.array(extr_gauche) + np.array(gauche) + np.array(centre), label='Droite', color='blue')
        ax1.bar(x, extr_droite, bottom=np.array(extr_gauche) + np.array(gauche) + np.array(centre) + np.array(droite), label='Extreme droite', color='#00008B')
        ax1.bar(x, divers, bottom=np.array(extr_gauche) + np.array(gauche) + np.array(centre) + np.array(droite) + np.array(extr_droite), label='Divers', color='green')

        ax1.set_title("Représentation du pourcentage de votes selon le taux de pauvreté en Haute-Garonne")
        ax1.set_xlabel("taux de pauvreté")
        ax1.set_ylabel("pourcentage de vote")
        ax1.legend()
        ax1.set_xticks(x)
        ax1.set_xticklabels(categories)
        # Afficher le graphique
        st.pyplot(fig1)


if page ==     "Analyse Générale de l'Abstention Électorale":
    st.header("Tendances de l'abstention et statistiques globales ")

    # Calculer le taux moyen d'abstention par élection
    taux_abstention_par_election = df.groupby('id_election')['% Abs/Ins'].mean().reset_index()
    taux_abstention_par_election['Nom élection'] = taux_abstention_par_election['id_election'].map(id_to_name)
    # Graphique d'évolution
    st.subheader("Évolution du Taux d'Abstention par Élection")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        taux_abstention_par_election['Nom élection'],
        taux_abstention_par_election['% Abs/Ins'],
        marker='o',
        linestyle='-',
        color='skyblue',
        linewidth=2,
        label="Taux d'Abstention"
    )
    ax.set_title("Évolution du Taux d'Abstention", fontsize=18, fontweight='bold', color='darkblue')
    ax.set_xlabel("Élections (id_election)", fontsize=14, fontweight='bold', color='gray')
    ax.set_ylabel("Taux d'Abstention (%)", fontsize=14, fontweight='bold', color='gray')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.legend(fontsize=12, title="Indicateur", title_fontsize=14)
    ax.set_xticks(range(len(taux_abstention_par_election['Nom élection'])))
    ax.set_xticklabels(taux_abstention_par_election['Nom élection'], rotation=45, ha='right')
    ax.set_facecolor('#f7f9fc')
    st.pyplot(fig)

    # Calculer la variation entre les élections
    taux_abstention_par_election['Variation (%)'] = taux_abstention_par_election['% Abs/Ins'].diff()

    # Graphique de variations
    st.subheader("Variation du Taux d'Abstention entre Élections")
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(
        taux_abstention_par_election['Nom élection'],
        taux_abstention_par_election['Variation (%)'].fillna(0),
        color=['green' if val < 0 else 'red' for val in taux_abstention_par_election['Variation (%)'].fillna(0)],
        alpha=0.8,
        edgecolor='black'
    )
    ax.set_title("Variation du Taux d'Abstention Entre Chaque Élection", fontsize=18, fontweight='bold', color='darkblue')
    ax.set_xlabel("Élections (id_election)", fontsize=14, fontweight='bold', color='gray')
    ax.set_ylabel("Variation (%)", fontsize=14, fontweight='bold', color='gray')
    ax.axhline(0, color='black', linewidth=1.2, linestyle='--')
    ax.bar_label(bars, fmt="%.2f", fontsize=10, padding=3, label_type='edge', color='black')
    ax.set_xticks(range(len(taux_abstention_par_election['Nom élection'])))
    ax.set_xticklabels(taux_abstention_par_election['Nom élection'], rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.set_facecolor('#f7f9fc')
    st.pyplot(fig)

    # Informations supplémentaires
    st.subheader("Informations Clés")
    positive_variations = taux_abstention_par_election[taux_abstention_par_election['Variation (%)'] > 0]
    negative_variations = taux_abstention_par_election[taux_abstention_par_election['Variation (%)'] < 0]

    st.markdown(f"""
    - **Le taux d'abstention a augmenté**  {len(positive_variations)} fois (Tour 2 2017 & 2022).
    - **Le taux d'abstention a diminué**  {len(negative_variations)} fois (Tour 1 2022 & 2024, Tour 2 2024).
    - **Plus forte augmentation** : {positive_variations['Variation (%)'].max():.2f}% ({positive_variations.loc[positive_variations['Variation (%)'].idxmax(), 'Nom élection']}).
    - **Plus forte diminution** : {negative_variations['Variation (%)'].min():.2f}% ({negative_variations.loc[negative_variations['Variation (%)'].idxmin(), 'Nom élection']}).
    """)

    st.header(" Disparités des Taux d'Abstention entre les Départements par Élection")

    # Sidebar pour les filtres
    st.sidebar.header("Filtres")
    election = st.sidebar.selectbox("Sélectionnez une élection", df['id_election'].unique())
    departement = st.sidebar.multiselect("Sélectionnez un ou plusieurs départements", df['Libellé du département'].unique())
    commune = st.sidebar.text_input("Rechercher une commune (optionnel)")

    # Filtrer les données
    filtered_data = df[df['id_election'] == election]

    if departement:
        filtered_data = filtered_data[filtered_data['Libellé du département'].isin(departement)]

    if commune:
        filtered_data = filtered_data[filtered_data['Libellé de la commune'].str.contains(commune, case=False, na=False)]

    if filtered_data.empty:
        st.warning("Aucune donnée trouvée pour les filtres sélectionnés.")
        st.stop()

    # Statistiques globales
    st.subheader(f"Statistiques pour {election}")
    total_inscrits = filtered_data['Inscrits'].sum()
    total_abstentions = filtered_data['Abstentions'].sum()
    taux_abstention = (total_abstentions / total_inscrits) * 100 if total_inscrits > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total des inscrits", f"{total_inscrits:,}")
    col2.metric("Total des abstentions", f"{total_abstentions:,}")
    col3.metric("Taux moyen d'abstention", f"{taux_abstention:.2f}%")

    # Classement par taux d'abstention pour l'élection sélectionnée
    st.subheader("Visualisation des Taux d'Abstention par Département")
    departments_taux = (
        filtered_data.groupby('Libellé du département')['% Abs/Ins']
        .mean()
        .sort_values(ascending=False)
    )

    # Graphiques des départements avec les taux d'abstention les plus élevés et les plus faibles
    highest_abstention = departments_taux.head(5)
    lowest_abstention = departments_taux.tail(5)

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    highest_abstention.plot(kind='bar', color='red', alpha=0.7, ax=ax1)
    ax1.set_title("Top 5 - Départements avec les Taux d'Abstention les Plus Élevés")
    ax1.set_ylabel("Taux d'Abstention (%)")
    ax1.set_xlabel("Départements")
    ax1.set_xticklabels(highest_abstention.index, rotation=45, ha='right')
    ax1.bar_label(ax1.containers[0], fmt="%.2f%%")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(8, 5))
    lowest_abstention.plot(kind='bar', color='green', alpha=0.7, ax=ax2)
    ax2.set_title("Top 5 - Départements avec les Taux d'Abstention les Plus Faibles")
    ax2.set_ylabel("Taux d'Abstention (%)")
    ax2.set_xlabel("Départements")
    ax2.set_xticklabels(lowest_abstention.index, rotation=45, ha='right')
    ax2.bar_label(ax2.containers[0], fmt="%.2f%%")
    st.pyplot(fig2)

    # Analyse des départements sur plusieurs élections
    st.subheader("Fréquence des Départements dans les Meilleurs et Moins Bons Taux d'Abstention")
    st.write("Ce graphique montre les départements figurant fréquemment parmi les meilleurs ou les moins bons votants.")
    try:
        elections_analysis = df.groupby(['id_election', 'Libellé du département'])['% Abs/Ins'].mean().reset_index()

        # Identifier les départements dans le top 10 des taux d'abstention les plus faibles et les plus élevés
        top_departments = {}
        bottom_departments = {}

        for election_id in df['id_election'].unique():
            election_data = elections_analysis[elections_analysis['id_election'] == election_id]
            top_10 = election_data.nsmallest(10, '% Abs/Ins')['Libellé du département']
            bottom_10 = election_data.nlargest(10, '% Abs/Ins')['Libellé du département']

            for dept in top_10:
                top_departments[dept] = top_departments.get(dept, 0) + 1

            for dept in bottom_10:
                bottom_departments[dept] = bottom_departments.get(dept, 0) + 1

        # Convertir en DataFrame pour affichage
        top_departments_df = pd.DataFrame(list(top_departments.items()), columns=['Département', 'Apparitions'])
        top_departments_df['Classement'] = top_departments_df['Apparitions'].apply(lambda x: "Toujours Top 10" if x == len(df['id_election'].unique()) else "Parfois Top 10")
        top_departments_df = top_departments_df.sort_values(by='Apparitions', ascending=False)

        bottom_departments_df = pd.DataFrame(list(bottom_departments.items()), columns=['Département', 'Apparitions'])
        bottom_departments_df['Classement'] = bottom_departments_df['Apparitions'].apply(lambda x: "Toujours Top 10" if x == len(df['id_election'].unique()) else "Parfois Top 10")
        bottom_departments_df = bottom_departments_df.sort_values(by='Apparitions', ascending=False)

        fig3, ax3 = plt.subplots(figsize=(10, 6))
        ax3.bar(top_departments_df['Département'][:10], top_departments_df['Apparitions'][:10], color='blue', alpha=0.7)
        ax3.set_title("Départements votant le mieux (Top 10 des Taux les Plus Faibles)")
        ax3.set_ylabel("Nombre d'Apparitions")
        ax3.set_xlabel("Départements")
        ax3.set_xticklabels(top_departments_df['Département'][:10], rotation=90, ha='center')
        ax3.bar_label(ax3.containers[0], fmt="%d")
        st.pyplot(fig3)

        fig4, ax4 = plt.subplots(figsize=(10, 6))
        ax4.bar(bottom_departments_df['Département'][:10], bottom_departments_df['Apparitions'][:10], color='orange', alpha=0.7)
        ax4.set_title("Départements votant le moins (Top 10 des Taux les Plus Élevés)")
        ax4.set_ylabel("Nombre d'Apparitions")
        ax4.set_xlabel("Départements")
        ax4.set_xticklabels(bottom_departments_df['Département'][:10], rotation=90, ha='center')
        ax4.bar_label(ax4.containers[0], fmt="%d")
        st.pyplot(fig4)

        # Départements d'outre-mer présents dans le graphique
        outre_mer_departments = ['Guadeloupe', 'Martinique', 'Guyane', 'La Réunion', 'Saint-Martin/Saint-Barthélemy', 'Nouvelle-Calédonie']
        # Ajouter une explication après le graphique
        st.markdown(f"Les départements d'outre-mer représentés dans ce graphique sont : **{', '.join(outre_mer_departments)}**.")


    except Exception as e:
        st.error(f"Erreur lors de l'analyse des départements : {e}")




elif page == "Analyse Approfondie de l'Abstention et de ses Liens Socio-économiques":
    st.header("Analyse des Votes Blancs, Nuls et Abstentions")
    st.markdown("""
    Un **vote blanc** est exprimé lorsque l'enveloppe ou le bulletin est vide, tandis qu'un **vote nul** correspond à un bulletin non valide (rayé, annoté, etc.). Ces votes reflètent une expression particulière des électeurs vis-à-vis des options proposées.
    """)

    # Calculer les moyennes des pourcentages par élection
    grouped_data = df.groupby('id_election')[['% Abs/Ins', '% Blancs/Ins', '% Nuls/Ins']].mean().reset_index()

    if grouped_data.empty:
        st.warning("Aucune donnée disponible pour l'analyse.")
        st.stop()


    # Calculer les corrélations
    correlation_matrix = grouped_data[['% Abs/Ins', '% Blancs/Ins', '% Nuls/Ins']].corr()
    st.subheader("Corrélations entre Votes Blancs, Nuls et Abstentions")
    st.write(correlation_matrix)


    grouped_data['Nom élection'] = grouped_data['id_election'].map(id_to_name)


    # Comparer graphiquement les pourcentages par élection
    st.subheader("Comparaison des Votes Blancs, Nuls et Abstentions par Élection")
    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = 0.2
    x = range(len(grouped_data['Nom élection']))

    ax.bar(x, grouped_data['% Abs/Ins'], width=bar_width, label='% Abs/Ins', color='lightblue')
    ax.bar([p + bar_width for p in x], grouped_data['% Blancs/Ins'], width=bar_width, label='% Blancs/Ins', color='lightgreen')
    ax.bar([p + 2 * bar_width for p in x], grouped_data['% Nuls/Ins'], width=bar_width, label='% Nuls/Ins', color='lightcoral')

    ax.set_xticks([p + bar_width for p in x])
    ax.set_xticklabels(grouped_data['Nom élection'], rotation=45, ha='right')
    ax.set_title("Comparaison des Votes Blancs, Nuls et Abstentions par Élection", fontsize=16)
    ax.set_xlabel("Élections", fontsize=14)
    ax.set_ylabel("Pourcentage (%)", fontsize=14)
    ax.legend()
    st.pyplot(fig)

    # Analyse des tendances avec une visualisation linéaire
    st.subheader("Tendances des Votes Blancs, Nuls et Abstentions")
    fig = plt.figure(figsize=(12, 6))
    plt.plot(grouped_data['Nom élection'], grouped_data['% Abs/Ins'], marker='o', label='% Abs/Ins', color='lightblue')
    plt.plot(grouped_data['Nom élection'], grouped_data['% Blancs/Ins'], marker='o', label='% Blancs/Ins', color='lightgreen')
    plt.plot(grouped_data['Nom élection'], grouped_data['% Nuls/Ins'], marker='o', label='% Nuls/Ins', color='lightcoral')
    plt.title("Tendances des Votes Blancs, Nuls et Abstentions", fontsize=16)
    plt.xlabel("Élections", fontsize=14)
    plt.ylabel("Pourcentage (%)", fontsize=14)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    st.header("Analyse Croisée : Pauvreté et Abstention par Département")

    # Charger les données de pauvreté
    poverty_data = load_poverty_data()
    if poverty_data.empty:
        st.stop()
        


    # Sélection de l'année pour l'analyse
    selected_year = st.sidebar.selectbox("Choisissez une année pour l'analyse Abstention/Pauvreté  :", ['2017', '2021'])

    # Filtrer les données selon l'année sélectionnée
    if selected_year == '2017':
        poverty_column = 'tp60_a17'
        election_year = '2017'
        title_suffix = "(2017)"
    else:
        poverty_column = 'DISP_TP60_A21'
        election_year = '2022'
        title_suffix = "(2021/2022)"

    try:
        # Filtrer les données d'abstention pour l'année sélectionnée
        df_filtered = df[df['id_election'].str.contains(election_year, na=False)]
        df_filtered['Code du département'] = df_filtered['Code du département'].astype(str).str.zfill(3)
        poverty_data['departement'] = poverty_data['departement'].astype(str).str.zfill(3)

        # Fusionner les données d'abstention et de pauvreté
        merged_data = pd.merge(
            poverty_data, df_filtered, left_on='departement', right_on='Code du département', how='inner'
        )
    except Exception as e:
        st.error(f"Erreur lors de la préparation des données : {e}")
        st.stop()


    # Calculer les moyennes par département
    dept_analysis = merged_data.groupby('Libellé du département')[[poverty_column, '% Abs/Ins']].mean().reset_index()
    dept_analysis = dept_analysis.rename(columns={poverty_column: 'Taux de Pauvreté'})
    dept_analysis = dept_analysis.sort_values(by='% Abs/Ins', ascending=True)

    # Statistiques globales
    median_poverty = dept_analysis['Taux de Pauvreté'].median()
    median_absenteeism = dept_analysis['% Abs/Ins'].median()

    st.subheader(f"Statistiques Médianes {title_suffix}")
    col1, col2 = st.columns(2)
    col1.metric("Médiane du Taux de Pauvreté", f"{median_poverty:.2f}%")
    col2.metric("Médiane du Taux d'Abstention", f"{median_absenteeism:.2f}%")

    # Corrélation entre pauvreté et abstention
    correlation = dept_analysis[['Taux de Pauvreté', '% Abs/Ins']].corr().iloc[0, 1]
    st.metric("Corrélation Pauvreté-Abstention", f"{correlation:.2f}")

    # Obtenir les départements qui votent le mieux (taux d'abstention les plus faibles)
    best_voters = dept_analysis.head(10)
    # Obtenir les départements qui votent le moins bien (taux d'abstention les plus élevés)
    worst_voters = dept_analysis.tail(10)

    # Graphique pour les départements qui votent le mieux
    st.subheader(f"Départements avec le Taux d'Abstention le Plus Faible {title_suffix}")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    x1 = range(len(best_voters))
    bars1 = ax1.bar(x1, best_voters['Taux de Pauvreté'], width=0.4, label="Taux de Pauvreté (%)", color='lightblue', align='center')
    bars2 = ax1.bar(x1, best_voters['% Abs/Ins'], width=0.4, label="Taux d'Abstention (%)", color='orange', align='edge')
    ax1.set_xticks(range(len(best_voters)))
    ax1.set_xticklabels(best_voters['Libellé du département'], rotation=45)
    ax1.set_title(f"Taux de Pauvreté et Abstention (Meilleurs Votants) {title_suffix}", fontsize=16, fontweight='bold', color='darkblue')
    ax1.set_xlabel('Libellé du département', fontsize=14, fontweight='bold')
    ax1.set_ylabel("Pourcentage (%)", fontsize=14, fontweight='bold')
    ax1.legend(fontsize=12, title="Indicateur", title_fontsize=14)
    ax1.bar_label(bars1, fmt="%.2f%%")
    ax1.bar_label(bars2, fmt="%.2f%%")
    st.pyplot(fig1)

    # Graphique pour les départements qui votent le moins bien
    st.subheader(f"Départements avec le Taux d'Abstention le Plus Élevé {title_suffix}")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    x2 = range(len(worst_voters))
    bars3 = ax2.bar(x2, worst_voters['Taux de Pauvreté'], width=0.4, label="Taux de Pauvreté (%)", color='lightblue', align='center')
    bars4 = ax2.bar(x2, worst_voters['% Abs/Ins'], width=0.4, label="Taux d'Abstention (%)", color='orange', align='edge')
    ax2.set_xticks(range(len(worst_voters)))
    ax2.set_xticklabels(worst_voters['Libellé du département'], rotation=45)
    ax2.set_title(f"Taux de Pauvreté et Abstention (Moins Bons Votants) {title_suffix}", fontsize=16, fontweight='bold', color='darkblue')
    ax2.set_xlabel('Libellé du département', fontsize=14, fontweight='bold')
    ax2.set_ylabel("Pourcentage (%)", fontsize=14, fontweight='bold')
    ax2.legend(fontsize=12, title="Indicateur", title_fontsize=14)
    ax2.bar_label(bars3, fmt="%.2f%%")
    ax2.bar_label(bars4, fmt="%.2f%%")
    st.pyplot(fig2)

    # Informations supplémentaires
    st.subheader("Informations Importantes")
    st.markdown(f"""
    - **Corrélation entre Taux de Pauvreté et Abstention** : {correlation:.2f}.
    - **Médiane du Taux de Pauvreté** : {median_poverty:.2f}%.
    - **Médiane du Taux d'Abstention** : {median_absenteeism:.2f}%.
    - **Nombre total de départements analysés** : {len(dept_analysis)}.
    """)

    st.header("Analyse Croisée : Chômage et Absentéisme pour les Années 2017, 2022 et 2024")

    # Charger les données de chômage
    unemployment_data = load_unemployment_data()
    if unemployment_data.empty:
        st.stop()

    selected_years = st.sidebar.multiselect("Sélectionnez les années d'analyse Abstention/chômage:", ['2017', '2022', '2024'], default=['2017'])

    try:
        df['Code du département'] = df['Code du département'].astype(str).str.zfill(2)
        unemployment_data['DEP_CODE'] = unemployment_data['DEP_CODE'].astype(str).str.zfill(2)

        # Filtrer uniquement le premier tour avec un identifiant d'élection contenant '_t1'
        df_first_round = df[df['id_election'].str.contains("_t1", na=False)]

        merged_data = pd.merge(
            unemployment_data, 
            df_first_round.groupby(['Code du département', 'id_election'])['% Abs/Ins'].mean().reset_index(),
            left_on='DEP_CODE', 
            right_on='Code du département',
            how='inner'
        )
    except Exception as e:
        st.error(f"Erreur lors de la fusion des données : {e}")
        st.stop()

    for year in selected_years:
        st.subheader(f"Analyse pour l'Année {year}")
        if not any(merged_data['id_election'].str.contains(year, na=False)):
            st.warning(f"Aucune donnée disponible pour l'année {year}.")
            continue

        election_year = year
        year_data = merged_data[merged_data['id_election'].str.contains(election_year, na=False)]

        if year_data.empty:
            st.warning(f"Aucune donnée disponible pour l'année {year}.")
            continue

        mean_unemployment = year_data[year].mean()
        mean_absenteeism = year_data['% Abs/Ins'].mean()

        st.write(f"- **Taux de Chômage Moyen ({year})** : {mean_unemployment:.2f}%")
        st.write(f"- **Taux d'Absentéisme Moyen ({year})** : {mean_absenteeism:.2f}%")

        # Identifier les 10 départements avec les taux les plus élevés et les plus faibles
        top_10_highest = year_data.nlargest(10, year)
        top_10_lowest = year_data.nsmallest(10, year)

        # Graphique à barres pour les 10 taux de chômage et d'absentéisme les plus élevés
        st.subheader(f"10 Départements avec les Taux de Chômage les Plus Élevés ({year})")
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(top_10_highest['DEP_NOM']))
        bar_width = 0.4
        ax.bar(x, top_10_highest[year], bar_width, label="Taux de Chômage", color='red', alpha=0.7)
        ax.bar([p + bar_width for p in x], top_10_highest['% Abs/Ins'], bar_width, label="Taux d'Absentéisme", color='blue', alpha=0.7)
        ax.set_xticks([p + bar_width / 2 for p in x])
        ax.set_xticklabels(top_10_highest['DEP_NOM'], rotation=45, ha='right')
        ax.set_title(f"Top 10 Taux Élevés - Chômage et Absentéisme ({year})")
        ax.set_xlabel("Départements")
        ax.set_ylabel("Pourcentage (%)")
        ax.legend()
        st.pyplot(fig)

        # Graphique à barres pour les 10 taux de chômage et d'absentéisme les plus faibles
        st.subheader(f"10 Départements avec les Taux de Chômage les Plus Faibles ({year})")
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(top_10_lowest['DEP_NOM']))
        ax.bar(x, top_10_lowest[year], bar_width, label="Taux de Chômage", color='green', alpha=0.7)
        ax.bar([p + bar_width for p in x], top_10_lowest['% Abs/Ins'], bar_width, label="Taux d'Absentéisme", color='blue', alpha=0.7)
        ax.set_xticks([p + bar_width / 2 for p in x])
        ax.set_xticklabels(top_10_lowest['DEP_NOM'], rotation=45, ha='right')
        ax.set_title(f"Top 10 Taux Faibles - Chômage et Absentéisme ({year})")
        ax.set_xlabel("Départements")
        ax.set_ylabel("Pourcentage (%)")
        ax.legend()
        st.pyplot(fig)

        # Graphique de corrélation
        st.subheader(f"Corrélation entre Taux de Chômage et Absentéisme ({year})")
        correlation = year_data[[year, '% Abs/Ins']].corr().iloc[0, 1]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(year_data[year], year_data['% Abs/Ins'], color='orange', alpha=0.7)
        ax.set_title(f"Corrélation entre Chômage et Absentéisme ({year}) : {correlation:.2f}")
        ax.set_xlabel("Taux de Chômage (%)")
        ax.set_ylabel("Taux d'Absentéisme (%)")
        ax.grid(alpha=0.3)
        st.pyplot(fig)

    @st.cache_data
    def convert_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_to_csv(merged_data)
    st.download_button(
        label="Télécharger les données fusionnées",
        data=csv,
        file_name='chomage_absenteisme.csv',
        mime='text/csv'
    )

    st.header("Analyse de l'Absentéisme et des Proportions par Tranche d'Âge")

    st.markdown("""
    Cette analyse examine la relation entre les proportions de population par tranche d'âge et les taux d'absentéisme électoral. 
    Les graphiques identifient, pour chaque tranche d'âge, les 5 départements où cette tranche est la plus représentée **(majoritaire)** 
    et les 5 départements où elle est la moins représentée **(minoritaire)**. Ensuite, la relation entre la proportion de cette tranche 
    d'âge et le taux d'absentéisme est analysée pour mieux comprendre les dynamiques électorales liées aux caractéristiques démographiques.
    """)



    # Charger les données démographiques
    demographic_data = load_demographic_data()
    if demographic_data.empty:
        st.error("Les données démographiques sont introuvables.")
        st.stop()

    # Charger les données d'absentéisme
    absenteeism_data = load_data()
    if absenteeism_data.empty:
        st.error("Les données d'absentéisme sont introuvables.")
        st.stop()

    # Vérifier les proportions et les convertir en pourcentage si nécessaire
    for col in ['prop0142017', 'prop15392017', 'prop40592017', 'prop60p2017',
                'prop0142022', 'prop15392022', 'prop40592022', 'prop60p2022']:
        if demographic_data[col].max() <= 1:  # Si les proportions sont en décimales
            demographic_data[col] *= 100

    # Normaliser les codes département pour la jointure
    absenteeism_data['Code du département'] = absenteeism_data['Code du département'].astype(str).str.zfill(3)
    demographic_data['dep'] = demographic_data['dep'].astype(str).str.zfill(3)

    # Sélectionner l'année pour l'analyse
    selected_year = st.sidebar.selectbox("Choisissez une année pour l'analyse Abstention/Categorie d'age :", ['2017', '2022'])

    # Filtrer les données démographiques pour l'année sélectionnée
    cols_to_keep = ['dep', 'nomdep', f'prop014{selected_year}', f'prop1539{selected_year}', f'prop4059{selected_year}', f'prop60p{selected_year}']
    try:
        proportion_data = demographic_data[cols_to_keep]
    except KeyError:
        st.error(f"Colonnes pour l'année {selected_year} introuvables dans les données démographiques.")
        st.stop()

    # Renommer les colonnes pour simplifier l'affichage
    proportion_data = proportion_data.rename(columns={
        f'prop1539{selected_year}': '% Population 15-39 ans',
        f'prop4059{selected_year}': '% Population 40-59 ans',
        f'prop60p{selected_year}': '% Population 60+ ans'
    })

    # Filtrer les données d'absentéisme pour le premier tour
    absenteeism_data = absenteeism_data[absenteeism_data['id_election'].str.contains("_t1")]

    # Fusionner les données démographiques et d'absentéisme
    merged_data = pd.merge(proportion_data, absenteeism_data, left_on='dep', right_on='Code du département', how='inner')

    # Tranches d'âge
    age_columns = [ '% Population 15-39 ans', '% Population 40-59 ans', '% Population 60+ ans']

    # Analyse par tranche d'âge
    for age_column in age_columns:
        # Sélectionner les départements majoritaires et minoritaires
        majority_departments = merged_data.nlargest(5, age_column)
        minority_departments = merged_data.nsmallest(5, age_column)

        # Calculer les moyennes pour les groupes majoritaires et minoritaires
        majority_absenteeism = majority_departments['% Abs/Ins'].mean()
        minority_absenteeism = minority_departments['% Abs/Ins'].mean()

        majority_proportion = majority_departments[age_column].mean()
        minority_proportion = minority_departments[age_column].mean()

        # Créer les données pour le graphique
        graph_data = {
            'Groupe': ['Majoritaire', 'Minoritaire'],
            'Taux d\'Absentéisme (%)': [majority_absenteeism, minority_absenteeism],
            'Proportion Moyenne (%)': [majority_proportion, minority_proportion]
        }
        graph_df = pd.DataFrame(graph_data)

        # Afficher les résultats
        st.subheader(f"Tranche d'Âge : {age_column}")
        fig, ax = plt.subplots(figsize=(8, 6))
        bar_width = 0.35
        x = range(len(graph_df))

        bars1 = ax.bar(x, graph_df['Proportion Moyenne (%)'], bar_width, label='Proportion Moyenne (%)', color='skyblue')
        bars2 = ax.bar([i + bar_width for i in x], graph_df['Taux d\'Absentéisme (%)'], bar_width, label='Taux d\'Absentéisme (%)', color='orange')

        # Configuration des étiquettes et du graphique
        ax.set_xticks([i + bar_width / 2 for i in x])
        ax.set_xticklabels(graph_df['Groupe'])
        ax.set_title(f"Analyse : Proportions et Taux d'Absentéisme ({age_column})", fontsize=16, fontweight='bold')
        ax.set_ylabel("Pourcentage", fontsize=14, fontweight='bold')
        ax.legend(fontsize=12, title="Indicateur", title_fontsize=14)
        ax.bar_label(bars1, fmt="%.2f%%")
        ax.bar_label(bars2, fmt="%.2f%%")

        st.pyplot(fig)
        
if page == "Analyse globale de la population française":
        # Charger les données
    @st.cache_data
    def load_votes_data_2024():
        try:
            return pd.read_csv('df_jointure_2024.csv')
        except FileNotFoundError:
            st.error("Fichier 'df_jointure_2024.csv' introuvable. Assurez-vous qu'il est dans le même répertoire que le script.")
            return pd.DataFrame()
    
    @st.cache_data
    def load_votes_data_2022():
        try:
            return pd.read_csv('df_jointure_2022.csv')
        except FileNotFoundError:
            st.error("Fichier 'df_jointure_2022.csv' introuvable. Assurez-vous qu'il est dans le même répertoire que le script.")
            return pd.DataFrame()
    
    @st.cache_data
    def load_demographics_data():
        try:
            return pd.read_csv('df_age.csv')
        except FileNotFoundError:
            st.error("Fichier 'df_age.csv' introuvable. Assurez-vous qu'il est dans le même répertoire que le script.")
            return pd.DataFrame()
    
    
    df_jointure = load_votes_data_2024()
    df_jointure_2022 = load_votes_data_2022()
    df_age = load_demographics_data()
    #Ecrire un texte explicatif
    st.title("Analyse globale de la population française")
    st.write("Regardons à présent les caractéristiques socio-démographiques de la France. "
             "Il est utile de mentionner que les résultats que nous utilisons concernent la liste de tête.")
    # Afficher les quatre images
    st.header("La population française")
    col1, col2 = st.columns(2)
    with col1:
        st.image("image_page_21.png")
        st.image("image_page_22.png")
    with col2:
        st.image("image_page_23.png")
        st.image("image_page_24.png")
    
    # Carte des départements
    st.header("Répartition des classes d'âge majoritaires par département")
    st.write("Regardons à présent le facteur de l'âge.")
    st.write("En France, l'âge moyen pour les hommes est 41 ans et il est de 43 ans pour les femmes.")
    st.write("L'espérance de vie quant à elle est de 85 ans pour les femmes et 79 pour les hommes.")
    st.write("Regardons pour les tranches suivantes sur le territoire français : 15-39 ans (1539), 40-59 ans(4059) et 60 ans et plus(60p).")
    annees = [2017, 2018, 2019, 2020, 2021, 2022]
    annee_selectionnee = st.selectbox("Choisissez une année", annees)
    
    if annee_selectionnee==2017:
        st.image("age2017.png")
        st.components.v1.html(open("res_2017_T1_dept.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
    elif annee_selectionnee==2018:
        st.image("age2018.png")
    elif annee_selectionnee==2019:
        st.image("age2019.png")
    elif annee_selectionnee==2020:
        st.image("age2020.png")
    elif annee_selectionnee==2021:
        st.image("age2021.png")
    elif annee_selectionnee==2022:
        st.image("age2022.png")
        st.components.v1.html(open("res_2022_T1_dept.html", "r", encoding="utf-8").read(), height=600, scrolling=True)

    
    # Analyse des Partis Politiques
    st.header("Analyse des votes par parti selon le type de ville")
    
    st.write("A présent, nous différencions les différentes villes selon le nombre de leurs habitants. "
             "Moins de 200 habitants : Petite commune"
             "Entre 200 et 2000 habitants : Commune"
             "Entre 2000 et 100000 habitants : Petite ville"
             "Plus de 100000 habitants : Grande ville"
             "Au delà de 400000 habitants : Métropole")
    
    annee_selectionnee_graphe = st.selectbox("Choisissez l'année", [2022, 2024])
    
    if annee_selectionnee_graphe == 2022:
        st.image("image2022.png")
    elif annee_selectionnee_graphe == 2024:
         st.image("image2024.png")
