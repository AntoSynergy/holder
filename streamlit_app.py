import streamlit as st
from azure.storage.blob import BlobServiceClient
import pandas as pd 


# Paramètres de connexion Azure Blob Storage
AZURE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=csb100320036fd16df4;AccountKey=ZXstKpygpdrTGBL0SISmIkZHOnWTZLMyt3OQ8TImph6sxdykKnWA8ByV+IHiv5EzAn6C5dvMTYDL+AStedoewg==;EndpointSuffix=core.windows.net'
AZURE_CONTAINER_NAME = 'antoinze'

# Fonction pour établir une connexion à Azure Blob Storage
def get_azure_blob_client():
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    return blob_service_client


# Titre de l'application
st.title("Téléversement de fichiers")

# Widget de téléversement de fichier
uploaded_file = st.file_uploader("Sélectionnez un fichier CSV", type=["csv","xlsx"])

# Vérifier si un fichier a été téléversé
if uploaded_file is not None:
    validate= st.button("Valider")
    if validate: 
    # Charger le fichier CSV dans un DataFrame Pandas
        df = pd.read_csv(uploaded_file)
        
        # Afficher les premières lignes du DataFrame
        st.write("Aperçu des données :")
        st.write(df.head())

        # Établir une connexion à Azure Blob Storage
        blob_service_client = get_azure_blob_client()

        # Téléverser le fichier dans Azure Blob Storage
        blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=uploaded_file.name)
        blob_client.upload_blob(uploaded_file.getvalue())

        # Afficher un message de succès
        st.success("Le fichier a été téléversé avec succès")
