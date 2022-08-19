from fastapi import Request, Form, APIRouter, File, UploadFile, Header,Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.library.helpers import *

from pathlib import Path

router = APIRouter()    
templates = Jinja2Templates(directory="templates/")

CHUNK_SIZE = 1024*1024
audio_path = Path("videos/video1.mp4")

# @router.get("/video")
# async def read_root(request: Request):  
#     return templates.TemplateResponse("index_video.html", context={"request": request})

@router.get("/audio")
async def read_root(request: Request):
    return templates.TemplateResponse("index_audio.html", context={"request": request})


@router.get("/audio/audio")
async def audio_endpoint(range: str = Header(None)):
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    with open(audio_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        filesize = str(audio_path.stat().st_size)
        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
            'Accept-Ranges': 'bytes'
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")