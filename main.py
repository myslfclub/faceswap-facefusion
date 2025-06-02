# interface.py (corrected Streamlit UI)

import streamlit as st
import requests
import os
import tempfile

st.set_page_config(page_title="FaceSwap Cloud", layout="centered")

st.title("🪄 Face Swap Cloud")
st.markdown("Upload a video and a face image to apply face swap.")

backend_url = os.getenv("BACKEND_URL", "https://faceswap-facefusion.streamlit.app/faceswap")
api_key = os.getenv("API_KEY", "demo-key")

MAX_SIZE = 100 * 1024 * 1024  # 100MB

# Upload : Vidéo d'abord, image ensuite
video_file = st.file_uploader("🎥 Upload Video File (mp4, mov)", type=["mp4", "mov"])
image_file = st.file_uploader("🖼️ Upload Face Image (jpg, png)", type=["jpg", "jpeg", "png"])
resolution = st.selectbox("Output Resolution", ["720", "1080"], index=0)

# Vérification poids
too_large = False
if video_file and video_file.size > MAX_SIZE:
    st.error("❌ Fichier trop volumineux pour le serveur. Veuillez compresser la vidéo.")
    too_large = True
if image_file and image_file.size > MAX_SIZE:
    st.error("❌ L'image est trop lourde. Essayez une plus légère.")
    too_large = True

if st.button("🚀 Launch FaceSwap"):
    if not video_file or not image_file:
        st.warning("📂 Veuillez importer une vidéo ET une image.")
    elif too_large:
        st.warning("⚠️ Réduisez la taille des fichiers avant de relancer.")
    else:
        with st.spinner("Processing face swap..."):
            files = {
                "image": (image_file.name, image_file, image_file.type),
                "video": (video_file.name, video_file, video_file.type),
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
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"🚫 Connection failed: {e}")
