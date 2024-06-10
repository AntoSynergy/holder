import streamlit as st
from azure.storage.blob import BlobServiceClient
import pandas as pd
import os

st.markdown(
    """
    <style>
    .main {

    }
    .css-18e3th9 {
        padding: 1rem 1rem 10rem 1rem;
    }
    .css-1lcbmhc {
        padding: 0rem;
    }
    .centered-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 200px; /* Adjust the width as needed */
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Paramètres de connexion Azure Blob Storage
AZURE_CONNECTION_STRING = os.getenv('AZURESTORAGE')
AZURE_CONTAINER_NAME = 'antoinze'

# Fonction pour établir une connexion à Azure Blob Storage
def get_azure_blob_client():
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        return blob_service_client
    except Exception as e:
        st.error(f"Erreur lors de la connexion à Azure Blob Storage: {e}")
        return None

# Sidebar Menu
st.sidebar.title("Menu")
menu = st.sidebar.radio("Navigation", ["Accueil", "Dépôt"])

if menu == "Accueil":
    st.title("Accueil")
    st.write("Bienvenue sur l'application de téléversement de fichiers d'HOLDER.")
    image_url="https://th.bing.com/th/id/R.94d0294b4adf9af75b7c9374602d8c19?rik=53TxVxUvr86xxA&riu=http%3a%2f%2fwww.groupeholder.com%2f_files%2f_media%2fimages%2flogo_holder.png&ehk=tbMZniI%2fiLu%2bO6zUD8QZWGvweho0E61TvKrKmyfoFRk%3d&risl=&pid=ImgRaw&r=0&sres=1&sresct=1"
    st.markdown(f'<img src="{image_url}" class="centered-image">', unsafe_allow_html=True)
    
elif menu == "Dépôt":
    st.title("Téléversement de fichiers")
    
    # Widget de téléversement de fichier
    uploaded_file = st.file_uploader("Sélectionnez un fichier CSV ou XLSX", type=["csv", "xlsx"])
    
    # Option pour sélectionner le délimiteur
    
    format=st.selectbox("Choisissez le format du fichier",["CSV","XLSX"])
    if format =="CSV":
        delimiter = st.selectbox("Sélectionnez le délimiteur du fichier CSV", [",",";"])
    st.text("Le format du fichier se situe après son nom, ex: données.csv, '.csv' est le format.")
    # Vérifier si un fichier a été téléversé
    if uploaded_file is not None:
        validate = st.button("Valider")
        if validate:
            # Charger le fichier CSV dans un DataFrame Pandas
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file, sep=delimiter)
                elif uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)
                else:
                    st.error("Format de fichier non pris en charge.")
                    st.stop()
                
                # Afficher les premières lignes du DataFrame
                st.write("Aperçu des données :")
                st.write(df.head())
                
                # Établir une connexion à Azure Blob Storage
                blob_service_client = get_azure_blob_client()
                if blob_service_client:
                    # Téléverser le fichier dans Azure Blob Storage
                    blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=uploaded_file.name)
                    blob_client.upload_blob(uploaded_file.getvalue())
                    
                    # Afficher un message de succès
                    st.success("Le fichier a été téléversé avec succès")
            except Exception as e:
                st.error(f"Erreur lors du traitement du fichier : {e}")
