from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.library.helpers import openfile
from app.routers import twoforms, unsplash, accordion, upload_re, video, image, yolov5
# import uvicorn

# https://stribny.name/blog/fastapi-video/

# from pathlib import Path
# from gtts import gTTS
# from typing import BinaryIO

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# CHUNK_SIZE = 1024*1024

# video_path = Path("videos/video.mp4")
# audio_path = Path("videos/video1.mp4")
# audio_path = Path("audio/test.mp4")

app.mount("/videos", StaticFiles(directory="videos"), name="videos")
app.mount("/app", StaticFiles(directory="app"), name="app")
# app.mount("/audio", StaticFiles(directory="audio"), name="audio")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/Upload", StaticFiles(directory="Upload"), name="Upload")
app.mount("/model", StaticFiles(directory="model"), name="model")
app.mount("/yolov5_result_image", StaticFiles(directory="yolov5_result_image"), name="yolov5_result_image")

app.include_router(upload_re.router)
# app.include_router(upload.router)
app.include_router(unsplash.router)
app.include_router(twoforms.router)
app.include_router(accordion.router)

app.include_router(video.router)
# app.include_router(audio.router)
app.include_router(image.router)
app.include_router(yolov5.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home_custom.md")
    # data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})

# @app.get("/video")
# async def read_root(request: Request):  
#     return templates.TemplateResponse("index_video.html", context={"request": request})

# @app.get("/audio")
# async def read_root(request: Request):
#     return templates.TemplateResponse("index_audio.html", context={"request": request})


# @app.get("/video/video")
# async def video_endpoint(range: str = Header(None)):
#     start, end = range.replace("bytes=", "").split("-")
#     start = int(start)
#     end = int(end) if end else start + CHUNK_SIZE
#     with open(video_path, "rb") as video:
#         video.seek(start)
#         data = video.read(end - start)
#         filesize = str(video_path.stat().st_size)
#         headers = {
#             'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
#             'Accept-Ranges': 'bytes'
#         }
#         return Response(data, status_code=206, headers=headers, media_type="video/mp4")

# @app.get("/audio")
# async def read_root_audio(request: Request):
#     return templates.TemplateResponse("index_audio.html", context={"request": request})

# @app.get("/audio/audio")
# async def audio_endpoint(range: str = Header(None)):
#     start, end = range.replace("bytes=", "").split("-")
#     start = int(start)
#     end = int(end) if end else start + CHUNK_SIZE
#     with open(audio_path, "rb") as audio:
#         audio.seek(start)
#         data = audio.read(end - start)
#         filesize = str(audio_path.stat().st_size)
#         headers = {
#             'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
#             'Accept-Ranges': 'bytes'
#         }
#         return Response(data, status_code=206, headers=headers, media_type="video/mp4")


# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=8000)
