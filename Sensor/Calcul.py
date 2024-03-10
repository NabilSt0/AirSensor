import streamlit as st
import pandas as pd
import snowflake.connector
import os
import pickle
import openai

openai.api_key = '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'

# Fonction principale pour la page de calcul de la qualité de l'air
def page_calcul_qualite_air():
    # Initialisation des variables de session pour contrôler le flux
    if 'data_fetched' not in st.session_state:
        st.session_state.data_fetched = False
    if 'model_predictions' not in st.session_state:
        st.session_state.model_predictions = {}
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()

    # Fonction pour créer ou remplacer le fichier CSV avec les données actuelles, sans le TIMESTAMP
    def create_or_replace_csv(df, file_path='sensor_readings.csv'):
        df_copy = df.drop(columns=['TIMESTAMP'], errors='ignore')
        if os.path.exists(file_path):
            os.remove(file_path)
        df_copy.to_csv(file_path, index=False)

    # Fonction pour se connecter à Snowflake et récupérer les données
    def fetch_data():
        # Paramètres de connexion (remplacer par vos propres paramètres)
        USER = 'ELJAINABIL01'
        PASSWORD = 'Nabilox123@'
        ACCOUNT = 'py05488.ca-central-1.aws'
        WAREHOUSE = 'MY_SENSOR_DATA_WAREHOUSE'
        DATABASE = 'EnvironmentalData'
        SCHEMA = 'public'
        
        conn = snowflake.connector.connect(
            user=USER,
            password=PASSWORD,
            account=ACCOUNT,
            warehouse=WAREHOUSE,
            database=DATABASE,
            schema=SCHEMA
        )
        cur = conn.cursor()
        query = """
        SELECT
            TIMESTAMP,
            AIRQUALITYINDEX,
            TVOC_PPB,
            ECO2_PPM,
            RELATIVEHUMIDITY_PERCENT,
            PRESSURE_PA,
            TEMPERATURE_C      
        FROM SENSORREADINGS
        ORDER BY TIMESTAMP DESC
        LIMIT 180
        """
        cur.execute(query)
        df = pd.DataFrame(cur.fetchall(), columns=[x[0] for x in cur.description])
        cur.close()
        conn.close()
        return df

    # Fonction pour effectuer les prédictions
    def make_predictions():
        df = pd.read_csv("sensor_readings.csv")
        model_linear = pickle.load(open('linear_regression_model.pkl', 'rb'))
        model_ridge = pickle.load(open('ridge_regression_model.pkl', 'rb'))
        model_lasso = pickle.load(open('lasso_regression_model.pkl', 'rb'))
        input_data = df[['TVOC_PPB', 'ECO2_PPM', 'RELATIVEHUMIDITY_PERCENT', 'PRESSURE_PA', 'TEMPERATURE_C']].mean().to_frame().transpose()
        prediction_linear = model_linear.predict(input_data)[0]
        prediction_ridge = model_ridge.predict(input_data)[0]
        prediction_lasso = model_lasso.predict(input_data)[0]
        return {
            'linear': prediction_linear,
            'ridge': prediction_ridge,
            'lasso': prediction_lasso
        }

    def interaction_chatsensor():
        moyennes = calculer_moyennes(st.session_state.df)
        texte_explicatif = generer_texte_explicatif(*moyennes)
        return texte_explicatif

    def calculer_moyennes(df):
        tvoc_moyenne = df['TVOC_PPB'].mean()
        eco2_moyenne = df['ECO2_PPM'].mean()
        humidity_moyenne = df['RELATIVEHUMIDITY_PERCENT'].mean()
        pressure_moyenne = df['PRESSURE_PA'].mean()
        temperature_moyenne = df['TEMPERATURE_C'].mean()
        return tvoc_moyenne, eco2_moyenne, humidity_moyenne, pressure_moyenne, temperature_moyenne

    def generer_texte_explicatif(tvoc_moyenne, eco2_moyenne, humidity_moyenne, pressure_moyenne, temperature_moyenne):
        prompt = f"""
        TVOC (Total Volatile Organic Compounds) en PPB : {tvoc_moyenne},
        eCO2 (Equivalent CO2) en PPM : {eco2_moyenne},
        Humidité Relative en Pourcentage : {humidity_moyenne},
        Pression en PA : {pressure_moyenne},
        Température en °C : {temperature_moyenne}.
        dis la valeure moyenne de chaque metrique et en quoi chaque métrique inflence la qualite de l air et proposez un indice de qualité de l'air (entre 1 et 5) pour chaque valeur et enfin donne moi une vue global de la qualite de lair.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Vous êtes un assistant intelligent qui fournit la qualité de l'air intérieur basées sur des données spécifiques."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        if response['choices']:
            return response['choices'][0]['message']['content']
        else:
            return "Désolé, je ne peux pas générer de réponse en ce moment."

    # Interface Streamlit pour la page de calcul de la qualité de l'air
    st.title('Visualisation et prédiction de la qualité de l’air')

    if st.button('Commencer Test'):
        st.session_state.df = fetch_data()
        create_or_replace_csv(st.session_state.df)
        st.session_state.data_fetched = True
        st.success('Les dernières données de capteurs, y compris les timestamps, ont été récupérées et le fichier CSV a été mis à jour.')

    if st.session_state.data_fetched:
        st.write(st.session_state.df)
        air_quality_index_mean = st.session_state.df['AIRQUALITYINDEX'].mean()
        st.write(f"La moyenne de l'index de qualité de l'air calculée depuis la base de données est : {air_quality_index_mean:.2f}")

    if st.session_state.data_fetched and st.button('Prédire'):
        st.session_state.model_predictions = make_predictions()
        st.write("## Prédictions de la qualité de l'air (AIRQUALITYINDEX) :")
        st.write(f"Régression Linéaire: {st.session_state.model_predictions['linear']:.2f}")
        st.write(f"Régression Ridge: {st.session_state.model_predictions['ridge']:.2f}")
        st.write(f"Régression Lasso: {st.session_state.model_predictions['lasso']:.2f}")

        # Ajout de l'appel à la fonction interaction_chatsensor ici
        texte_explicatif = interaction_chatsensor()
        st.markdown(f"### Explication sur la Qualité de l'Air\n{texte_explicatif}", unsafe_allow_html=True)

    if st.button('Retest'):
        st.session_state.data_fetched = False
        st.session_state.model_predictions = {}
        st.session_state.df = pd.DataFrame()
        st.experimental_rerun()

