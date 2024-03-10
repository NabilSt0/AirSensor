import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px
import time

def page_donnees_temps_reel():
    # Vos informations de connexion Snowflake
    USER = 'ELJAINABIL01'
    PASSWORD = 'Nabilox123@'
    ACCOUNT = 'py05488.ca-central-1.aws'
    WAREHOUSE = 'MY_SENSOR_DATA_WAREHOUSE'
    DATABASE = 'EnvironmentalData'
    SCHEMA = 'PUBLIC'

    def create_snowflake_connection():
        # Connexion à Snowflake
        conn = snowflake.connector.connect(
            user=USER,
            password=PASSWORD,
            account=ACCOUNT,
            warehouse=WAREHOUSE,
            database=DATABASE,
            schema=SCHEMA
        )
        return conn

    def get_latest_data(conn):
        # Modifier ici pour récupérer toutes les données plutôt que de limiter à 100
        query = """
        SELECT TIMESTAMP, AIRQUALITYINDEX, TVOC_PPB, ECO2_PPM, RELATIVEHUMIDITY_PERCENT, PRESSURE_PA, ALTITUDE_METERS, ALTITUDE_FEET, TEMPERATURE_C, TEMPERATURE_F
        FROM ENVIRONMENTALDATA.PUBLIC.SENSORREADINGS
        ORDER BY TIMESTAMP DESC
        """
        df = pd.read_sql(query, conn)
        return df

    # Initialiser l'application Streamlit
    st.title('Tableau de Bord des Données des Capteurs en Temps Réel')

    # Placeholder pour les tableaux de données
    data_placeholder = st.empty()

    # Créer des placeholders pour chaque graphe
    graph_placeholders = {column: st.empty() for column in ['AIRQUALITYINDEX', 'TVOC_PPB', 'ECO2_PPM', 'RELATIVEHUMIDITY_PERCENT', 'PRESSURE_PA', 'ALTITUDE_METERS', 'ALTITUDE_FEET', 'TEMPERATURE_C', 'TEMPERATURE_F']}

    # Gérer le démarrage/arrêt de la mise à jour des données
    if 'updating' not in st.session_state:
        st.session_state.updating = False

    if st.button('Afficher les données en temps réel'):
        st.session_state.updating = True

    if st.button('Arrêter laffichage  des données'):
        st.session_state.updating = False

    while st.session_state.updating:
        with create_snowflake_connection() as conn:
            df = get_latest_data(conn)
            
        # S'assurer que TIMESTAMP est de type datetime
        df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])

        # Afficher les données sous forme de tableau
        data_placeholder.write(df)
        
        # Mettre à jour les graphiques pour chaque métrique
        for column in graph_placeholders.keys():
            fig = px.line(df.sort_values('TIMESTAMP'), x='TIMESTAMP', y=column, title=f'Évolution de {column}')
            graph_placeholders[column].plotly_chart(fig)

        time.sleep(1)  # Mise à jour toutes les 1 secondes pour réduire la charge
        if not st.session_state.updating:
            break
