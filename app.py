import streamlit as st
import requests
from PIL import Image
import io

# URL de l'API FastAPI
API_URL = "http://13.53.133.161:8000/segment"

# Titre de l'application
st.title("Segmentation d'image avec U-Net")

# Ajout d'un menu déroulant dans la barre latérale
st.sidebar.title("Options")
option = st.sidebar.selectbox(
    "Choisissez une option:",
    ("Segmentation d'image", "Autre fonctionalité")
)

# Interface pour télécharger une image si l'option est "Segmentation d'image"
if option == "Segmentation d'image":
    st.write("Téléchargez une image pour obtenir une segmentation basée sur le modèle U-Net.")

    # Interface pour télécharger une image
    uploaded_file = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Afficher l'image téléchargée
        image = Image.open(uploaded_file)
        width, height = image.size  # Obtenir la taille de l'image originale

        # Créer deux colonnes pour afficher les images côte à côte
        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Image téléchargée", use_column_width=True)

        # Bouton pour lancer la segmentation
        if st.button("Segmenter l'image"):
            st.write("Segmentation en cours...")

            try:
                with st.spinner("Segmentation en cours..."):
                    # Envoyer l'image à l'API FastAPI
                    files = {'file': uploaded_file.getvalue()}  # Utiliser getvalue pour lire le contenu
                    response = requests.post(API_URL, files=files)

                    # Vérifier si la réponse est OK (status 200)
                    if response.status_code == 200:
                        # Lire la réponse sous forme d'image
                        segmented_image = Image.open(io.BytesIO(response.content))

                        # Redimensionner l'image segmentée pour correspondre à l'image d'origine
                        segmented_image = segmented_image.resize((width, height))

                        # Afficher l'image segmentée dans la deuxième colonne
                        with col2:
                            st.image(segmented_image, caption="Masque segmenté", use_column_width=True)

                        # Ajout du bouton de téléchargement pour l'image segmentée
                        img_byte_arr = io.BytesIO()
                        segmented_image.save(img_byte_arr, format='PNG')
                        img_byte_arr.seek(0)

                        st.download_button(
                            label="Télécharger l'image segmentée",
                            data=img_byte_arr,
                            file_name="segmented_image.png",
                            mime="image/png"
                        )
                    else:
                        st.error(f"Erreur lors de la segmentation. Statut: {response.status_code}")
                        st.json(response.json())  # Voir le message d'erreur complet
            except Exception as e:
                st.error(f"Une erreur est survenue: {e}")

elif option == "Autre fonctionalité":
    st.write("Autre fonctionnalité sera bientôt disponible.")
