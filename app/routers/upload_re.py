from fastapi import Request, APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.library.helpers import *
from app.library import inference_PRN,inference_classfication,findpath,tts
from pathlib import Path
import requests

router = APIRouter()    
templates = Jinja2Templates(directory="templates/")


@router.get("/upload/", response_class=HTMLResponse)
def get_upload(request: Request):
    result = "Hello from upload.py"
    return templates.TemplateResponse('upload.html', context={'request': request, 'result': result})


@router.post("/upload/new/")
async def post_upload(imgdata: tuple, file: UploadFile = File(...)):
    # print(file)
    # data_dict = eval(imgdata[0])
    # winWidth, imgWidth, imgHeight = data_dict["winWidth"], data_dict["imgWidth"], data_dict["imgHeight"]

    # create the full path
    # 불러온 파일을 저장할 위치
    path_root = 'Upload/image'
    workspace = create_workspace(path_root)
    # 저장할 파일명 get
    file_path = Path(file.filename).name
    file_path = ''.join(char for char in file_path if char.isalnum())
    # file_path = Path(file.filename)
    # 가져온 url이 확장자가 없는경우 확장자를 추가
    if not "." in file_path:
        file_path = file_path + '.png'
    # 파일 저장 풀 경로 지정
    img_full_path = Path(path_root +'/'+ file_path)
    # img_full_path = workspace / file_path
    # 지정한 경로에 이미지 저장
    with open(str(img_full_path), 'wb') as myfile:
        contents = await file.read()
        myfile.write(contents)
    # req1 = requests.get(str(file.filename))
    # with open(Path(file_path),mode="wb") as myfile:
    #     contents = await file.read()
    #     myfile.write(req1.content)
        
    # url = file.filename
    # req1 = requests.get(url)
    # if req1.headers['Content-Type'] == 'image/jpeg':
    #     ext = '.png'
    # file = open(Path(url).name+ext,mode="wb")
    # file.write(req1.content)
    # print(Path(url).name+ext)
    
    # req1 = requests.get(file.filename)
    # # print(req1.headers['Content-Type'])
    # # if req1.headers['Content-Type'] == 'image/jpeg':
    # #     ext = '.png'
    # myfile = open(str(img_full_path),mode="wb")
    # myfile.write(req1.content)
        
    # UPLOAD_DIRECTORY = "./"
    # with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as myfile:
    #     contents = await file.read()
    #     myfile.write(contents)
    # print(file.filename)
    # return {"filenames": [file.filename for file in files]}

    # img_thumb_path = thumb(img_full_path, winWidth, imgWidth, imgHeight)
    gray_path = img_processing(img_full_path)
    prn_path, depth_path1, depth_path2, save_list_add = inference_PRN.main(img_full_path, output_type = 0)
    # print(save_list_add)
    # print(img_full_path)
    # print(gray_path)
    # print(prn_path)
    
    
    # inference_classfication
    judgment_scence_result = inference_classfication.classification(save_list_add)
    xx,yy,zz = findpath.find_nav(save_list_add)
    str_keypoint = str(judgment_scence_result[0]) + ', You will need to be careful ' + zz + ' to the ' +xx+' and '+yy
    # print(judgment_scence_result[0])
    path_voice_root = 'Upload/sound'
    workspace_voice = create_workspace(path_voice_root)
    # sound_path = Path(path_voice_root +'/'+ file_path)
    sound_filename = tts.save_sound(path_voice_root,file_path,str(judgment_scence_result[0]) + '     ' + zz)
    sound_path = str(Path(workspace_voice / sound_filename))
    # sound_path = '22.mp3'
    # result_classfication = inference_classfication.classification(save_list_add)
    # print(result_classfication)
    
    
    # filepath, ext = os.path.splitext(img_full_path)
    # thumb_path = filepath + "_thumbnail"+ext
    # print(img_full_path,thumb_path)
    
        # save_list_add =         [0.669,	0.873,	3.205,
    #         0.65,	0.117,	3.949,
    #         0.158,	0.098,	1.557,
    #         0.205,	0.594,	1.301,
    #         0.878,	0.685,	3.583] # 1 | attention
    
    

    data = {
        "img_full_path": img_full_path,
        "gray_path": gray_path,
        "prn_path": prn_path,
        "depth1_path": depth_path1,
        "depth1_path": depth_path2,
        "judgment_scence_result": str(judgment_scence_result[0]),
        "sound_path": sound_path,
        "advice":str_keypoint,
    }
    print(data)
    return data