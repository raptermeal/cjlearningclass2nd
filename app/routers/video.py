from fastapi import Request, APIRouter
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from app.library.helpers import *

from pathlib import Path

router = APIRouter()    
templates = Jinja2Templates(directory="templates/")

# CHUNK_SIZE = 1024*1024
# CHUNK_SIZE = 100000
video_path = Path("videos/video.mp4")
# video_path = Path('https://media.w3.org/2010/05/sintel/trailer.mp4')


@router.get("/video")
async def read_root(request: Request):  
    return templates.TemplateResponse("index_video.html", context={"request": request})

@router.get("/audio")
async def read_root(request: Request):
    return templates.TemplateResponse("index_audio.html", context={"request": request})


# @router.get("/video/video")
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
    
    
@router.get("/video/video")
async def image_endpoint():
    return FileResponse(video_path)