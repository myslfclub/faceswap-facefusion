
# interface.py (Streamlit)

import streamlit as st
import requests
import os
import tempfile

st.set_page_config(page_title="FaceSwap Cloud", layout="centered")

st.title("🪄 Face Swap Cloud")
st.markdown("Upload a video and a face image to apply face swap.")

# ✅ Utilise les variables d'environnement définies dans Streamlit Cloud
backend_url = os.getenv("BACKEND_URL", "https://faceswap-facefusion.streamlit.app/faceswap")
api_key = os.getenv("API_KEY", "demo-key")

# ⚠️ Limite de taille de fichier : 100 Mo (en bytes)
MAX_SIZE = 100 * 1024 * 1024

# Ordre inversé : vidéo d'abord, puis image
video_file = st.file_uploader("Upload Video File (mp4, mov)", type=["mp4", "mov"])
image_file = st.file_uploader("Upload Face Image (jpg, png)", type=["jpg", "jpeg", "png"])
resolution = st.selectbox("Output Resolution", ["720", "1080"], index=0)

# Avertissements de taille
if video_file and video_file.size > MAX_SIZE:
    st.warning("⚠️ La vidéo dépasse 100 Mo. Merci d'en choisir une plus légère.")
if image_file and image_file.size > MAX_SIZE:
    st.warning("⚠️ L'image dépasse 100 Mo. Merci d'en choisir une plus légère.")

if st.button("Launch FaceSwap"):
    if image_file and video_file and image_file.size <= MAX_SIZE and video_file.size <= MAX_SIZE:
        with st.spinner("Processing face swap..."):
            files = {
                "image": (image_file.name, image_file, image_file.type),
                "video": (video_file.name, video_file, video_file.type)
            }
            data = {"resolution": resolution}
            headers = {"x-api-key": api_key}

            try:
                response = requests.post(backend_url, files=files, data=data, headers=headers)
                if response.status_code == 200:
                    st.success("✅ Done! Download your video below.")
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                        tmp_file.write(response.content)
                        tmp_path = tmp_file.name
                    st.video(tmp_path)
                    with open(tmp_path, "rb") as file:
                        st.download_button("Download result", file, file_name="result.mp4")
                elif response.status_code == 413:
                    st.error("❌ Fichier trop volumineux pour le serveur. Veuillez compresser la vidéo.")
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"🚫 Connection failed: {e}")
    else:
        st.warning("📂 Please upload both a video and an image within 100MB size limit.")
