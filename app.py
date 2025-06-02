import streamlit as st
import subprocess
import os

st.title("🎭 FaceSwap FaceFusion")

# Upload des fichiers
uploaded_video = st.file_uploader("🎬 Vidéo source (MP4)", type=["mp4"])
uploaded_image = st.file_uploader("🖼️ Visage à insérer (JPG/PNG)", type=["jpg", "jpeg", "png"])
resolution = st.selectbox("📐 Résolution de sortie", ["480", "720", "1080"], index=1)

if st.button("Lancer le face swap"):
    if uploaded_video and uploaded_image:
        with open("target.mp4", "wb") as f:
            f.write(uploaded_video.read())
        with open("input.jpg", "wb") as f:
            f.write(uploaded_image.read())

        st.text("Traitement en cours...")
        subprocess.run(["python3", "scripts/cli.py", "run", "--target", "target.mp4", "--source", "input.jpg", "--output", "result.mp4", "--execution-provider", "cuda"])
        subprocess.run(["ffmpeg", "-i", "result.mp4", "-c", "copy", "-an", "result_no_audio.mp4"])
        subprocess.run(["ffmpeg", "-i", "result_no_audio.mp4", "-vf", f"scale=-2:{resolution}", "-c:a", "copy", "result_final.mp4"])

        st.video("result_final.mp4")
        with open("result_final.mp4", "rb") as f:
            st.download_button("📥 Télécharger la vidéo", data=f, file_name="face_swap_result.mp4")
    else:
        st.warning("Veuillez téléverser une vidéo et une image.")
