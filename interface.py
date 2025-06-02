# interface.py (Streamlit)

import streamlit as st
import requests
import os

st.set_page_config(page_title="FaceSwap Cloud", layout="centered")

st.title("🪄 Face Swap Cloud")
st.markdown("Upload a face image and a video to apply face swap.")

# ✅ Utilise les variables d'environnement définies dans Streamlit Cloud
backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/faceswap")
api_key = os.getenv("API_KEY", "demo-key")

image_file = st.file_uploader("Upload Face Image (jpg, png)", type=["jpg", "jpeg", "png"])
video_file = st.file_uploader("Upload Video File (mp4, mov)", type=["mp4", "mov"])
resolution = st.selectbox("Output Resolution", ["720", "1080"], index=0)

if st.button("Launch FaceSwap"):
    if image_file and video_file:
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
                    st.video(response.content)
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"🚫 Connection failed: {e}")
    else:
        st.warning("📂 Please upload both an image and a video.")
