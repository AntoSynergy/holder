from azure.storage.blob import BlobServiceClient
import streamlit as st
from azure.storage.blob import BlobServiceClient
# Paramètres de connexion Azure Blob Storage
AZURE_CONNECTION_STRING = 'votre_chaine_de_connexion'
AZURE_CONTAINER_NAME = 'votre_nom_de_conteneur'

# Fonction pour établir une connexion à Azure Blob Storage
def get_azure_blob_client():
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    return blob_service_client

# Paramètres de connexion Azure Blob Storage
# (à remplir avec vos propres informations de connexion)

# Titre de l'application
st.title("Téléversement de fichiers dans le Lakehouse Microsoft Fabric")

# Widget de téléversement de fichier
uploaded_file = st.file_uploader("Sélectionnez un fichier CSV", type=["csv","xlsx","json"])

# Vérifier si un fichier a été téléversé
if uploaded_file is not None:

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
    st.success("Le fichier a été téléversé avec succès dans le Lakehouse Microsoft Fabric.")
