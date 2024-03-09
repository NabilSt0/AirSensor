import streamlit as st
from streamlit_option_menu import option_menu  # Assurez-vous d'installer ce module

# Assurez-vous d'inclure ou d'importer les fonctions page_calcul_qualite_air et page_donnees_temps_reel ici
from Calcul import page_calcul_qualite_air
from Data import page_donnees_temps_reel



# Définir la fonction pour afficher la page de description
def page_description():
    st.title("🌍 Description du Projet 🚀")
    st.markdown("""
    ### Bienvenue sur la page de description de notre projet! 🎉
    Ce projet vise à révolutionner la manière dont nous interagissons avec les données environnementales. 🌱💨
    - **Objectif Principal**: Notre mission est d'offrir une plateforme dynamique et interactive pour visualiser et analyser les données environnementales en temps réel. Nous souhaitons sensibiliser à l'importance de surveiller la qualité de l'air et les conditions environnementales pour un futur plus durable. 🌟
    - **Fonctionnalités Clés**:
        - **Visualisation des Données**: Graphiques en temps réel pour une compréhension immédiate de l'état de l'environnement. 📊📈
        - **Calcul de la Qualité de l'Air**: Utilisez nos outils analytiques pour évaluer la qualité de l'air autour de vous, basée sur des mesures précises et des algorithmes avancés. 🌬️💨
        - **Engagement Utilisateur**: Une interface conviviale et des fonctionnalités interactives pour encourager la participation et l'éducation environnementale. 🌐👥
    Nous sommes déterminés à faire la différence, un byte à la fois. Rejoignez-nous dans cette aventure et contribuons ensemble à un monde plus propre et plus vert. 🌿🌎
    """, unsafe_allow_html=True)

# Créer la barre latérale avec les options de navigation
with st.sidebar:
    selected = option_menu("Menu ", ["Description", "Afficher les valeurs en temps réel", "Calculer la qualité de l'air"],
                           icons=['house', 'graph-up', 'calculator'], menu_icon="gear", default_index=0)

# Logique de navigation
if selected == "Description":
    page_description()
elif selected == "Afficher les valeurs en temps réel":
    page_donnees_temps_reel()  # Remplacez par l'appel à la fonction qui gère cette page
elif selected == "Calculer la qualité de l'air":
    page_calcul_qualite_air()  # Remplacez par l'appel à la fonction qui gère cette page
