from fastapi import Request, Form, APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.library.helpers import *
# from ..library import inference_PRN
# from app.library import inference_PRN
from app.library import yolov5_detect
# from app.library import inference_classfication
from pathlib import Path
from app.library.tts import makedirs, save_sound
import yaml, copy, requests

router = APIRouter()    
templates = Jinja2Templates(directory="templates/")


@router.get("/yolov5", response_class=HTMLResponse)
def get_upload(request: Request):
    result = "Hello from upload.py"
    return templates.TemplateResponse('yolov5.html', context={'request': request, 'result': result})


@router.post("/yolov5/yolov5")
async def post_upload(imgdata: tuple, file: UploadFile = File(...)):
    path_root = 'yolov5_result_image'
    workspace = create_workspace(path_root)
    # file_path = Path(file.filename)
    
    
    file_path = Path(file.filename).name
    file_path = ''.join(char for char in file_path if char.isalnum())
    # file_path = Path(file.filename)
    # 가져온 url이 확장자가 없는경우 확장자를 추가
    if not "." in file_path:
        file_path = file_path + '.png'
    img_full_path = Path(workspace / file_path)
    with open(str(img_full_path), 'wb') as myfile:
        contents = await file.read()
        myfile.write(contents)
        
        
        
    # url = str(file.filename)
    # req1 = requests.get(url)
    # if req1.headers['Content-Type'] == 'image/jpeg':
    #     ext = '.png'
    # filename = Path(url).name
    # filename_new = ''.join(char for char in filename if char.isalnum())
    # img_full_path = str(workspace / filename_new+ext)
    # file = open(img_full_path,mode="wb")
    # file.write(req1.content)




    # classs, classs_n, rename_result = yolov5_detect.run(file)
    classs, classs_n, rename_result = yolov5_detect.run(img_full_path)
    path_parents, path_model, path_yaml = yolov5_detect.path_name()
    class_data = yolov5_detect.load_yaml(path_parents, path_model, path_yaml)
    price = yolov5_detect.get_price(classs,class_data)
    price_add=copy.deepcopy(price)
    # print(range(len(price)))
    # print(price[0])
    for i in range(len(price_add)):
        price_add[i] = str(price_add[i]) + '원'
    # print(price_add)
    final_price = 0
    # print('final',final_price)
    # print(price[0],classs_n[0])
    for j in range(len(price)):
        final_price = final_price + int(price[j]) * int(classs_n[j])

    
    
    if classs==int(1000):
        word = '라면을 찾지 못했어요. 다시한번 시도해주세요.'
    else:
        word = '라면을 찾았어요!'
        word = word + ' 거기에는 ' + str(' '.join(classs)) + ' 가 있고, 각 각  ' + str(' '.join(classs_n)) + ' 개 있어요. ' 
        # word = word + '거기에는' + str(classs[0]) + '가 있고 각 각' + str(classs_n) + '개 있다' 
        word = word + ' 그리고 각 라면의 가격은 ' + str(' '.join(price_add)) + ' 입니다. '
        word = word + ' 따라서 최종 가격은 ' + str(final_price) + ' 원 입니다. '
    # print(word)
    # sound_path = save_sound(img_full_path,str(word))
    
    # path_parents, path_model, path_yaml = yolov5_detect.path_name()
    # class_data = yolov5_detect.load_yaml(path_parents, path_model, path_yaml)
    # price = yolov5_detect.get_price(classs,class_data)
    # price = []
    # for yy in range(len(classs)):
    #     find_name = classs[yy]
    #     order = [i for i in range(len(class_data['names'])) if find_name in class_data['names'][i]][0]
    #     # order = class_data['names'].find(classs[yy])
    #     print(order)
    #     price = price + [class_data['price'][int(order)]]
        
    # print('price',price)
    
    
    
    

    data = {
        "img_path": rename_result,
        "detect_class": classs,
        "detect_class_number": classs_n,
        # "sound_path": sound_path,
        "advice_price": word,
    }

    print(data)
    return data