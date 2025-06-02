import streamlit as st
import requests

st.title("Face Swap Cloud")
st.write("Remplacez un visage sur une vidéo (QuickTime, MP4)")

video_file = st.file_uploader("Upload vidéo", type=["mp4", "mov"])
face_file = st.file_uploader("Upload visage (image)", type=["jpg", "jpeg", "png"])
api_key = st.text_input("Clé API", value="demo-key", type="password")

if st.button("Lancer le swap") and video_file and face_file:
    files = {
        "video": (video_file.name, video_file, video_file.type),
        "image": (face_file.name, face_file, face_file.type)
    }
    data = {"resolution": "720"}
    headers = {"x-api-key": api_key}

    try:
        response = requests.post("http://127.0.0.1:8000/faceswap", files=files, data=data, headers=headers)
        if response.status_code == 200:
            st.video(response.content)
        else:
            st.error(f"Erreur: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Échec de connexion: {e}")
