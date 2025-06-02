from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil, uuid, subprocess, os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.post("/faceswap")
async def faceswap(video: UploadFile, image: UploadFile, resolution: str = Form(...)):
    job_id = str(uuid.uuid4())
    os.makedirs(f"tmp/{job_id}", exist_ok=True)
    video_path = f"tmp/{job_id}/video.mov" if video.filename.endswith(".mov") else f"tmp/{job_id}/video.mp4"
    image_path = f"tmp/{job_id}/input.jpg"
    result_path = f"tmp/{job_id}/result_final.mp4"

    with open(video_path, "wb") as f: shutil.copyfileobj(video.file, f)
    with open(image_path, "wb") as f: shutil.copyfileobj(image.file, f)

    subprocess.run(["python3", "scripts/cli.py", "run", "--target", video_path, "--source", image_path, "--output", f"tmp/{job_id}/result.mp4", "--execution-provider", "cuda"])
    subprocess.run(["ffmpeg", "-i", f"tmp/{job_id}/result.mp4", "-c", "copy", "-an", f"tmp/{job_id}/result_no_audio.mp4"])
    subprocess.run(["ffmpeg", "-i", f"tmp/{job_id}/result_no_audio.mp4", "-vf", f"scale=-2:{resolution}", "-c:a", "copy", result_path])

    return FileResponse(result_path, media_type="video/mp4", filename="face_swap_result.mp4")
