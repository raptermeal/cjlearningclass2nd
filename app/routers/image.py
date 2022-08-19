from fastapi import Request, Form, APIRouter, File, UploadFile, Header,Response
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from app.library.helpers import *
import base64
import io
from PIL import Image
import requests
import os
import random

from pathlib import Path

router = APIRouter()    
templates = Jinja2Templates(directory="templates/")

# image1_path = Path("Upload/image/220803105932_color_seg.png")
img_folfer = 'Upload/image'
# image1_path = "Upload/image/220803105932_color_seg.png"
# image2_path = "Upload/image/example_nyu_seg.jpg"


def get_random_img_path(img_folfer):
     
    img_path_list = []
    possible_img_extension = ['.jpg', '.jpeg', '.JPG', '.bmp', '.png'] # 이미지 확장자들
    
    for (root, dirs, files) in os.walk(img_folfer):
        if len(files) > 0:
            for file_name in files:
                if os.path.splitext(file_name)[1] in possible_img_extension:
                    img_path = root + '/' + file_name
                    
                    # 경로에서 \를 모두 /로 바꿔줘야함
                    img_path = img_path.replace('\\', '/') # \는 \\로 나타내야함         
                    img_path_list.append(img_path)
    img_path_final = random.choice(img_path_list)
    return img_path_final

@router.get("/image",response_class=HTMLResponse)
async def read_root(request: Request):  
    return templates.TemplateResponse("index_image.html", context={"request": request})

@router.get("/image/image")
async def image_endpoint():
    return FileResponse(get_random_img_path(img_folfer))
    # return FileResponse(image2_path)



# with open(video_path, "rb") as video:
#     video.seek(start)
#     data = video.read(end - start)
#     filesize = str(video_path.stat().st_size)
#     headers = {
#         'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
#         'Accept-Ranges': 'bytes'
#     }
#     return Response(data, status_code=206, headers=headers, media_type="video/mp4")