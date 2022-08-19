import gdown
import os
from pathlib import Path
 
def get_model_planerecnet():
    google_path = 'https://drive.google.com/uc?id='
    file_id = '1s4B-TSii7Qho-7J7_boZdHuIzt4Fx-nv'
    model_name = 'PlaneRecNet_101_9_125000.pth'
    # print(os.getcwd())
    output_name = Path(os.getcwd()).as_posix() + '/' + 'model' + '/' + model_name
    if not os.path.exists(output_name):
        gdown.download(google_path+file_id,output_name,quiet=False)
        
def get_model_planerecnet_classification():
    google_path = 'https://drive.google.com/uc?id='
    file_id = '1QA6ibzhJ_-1pjunxzU6_ZOoXm5QQFiZy'
    model_name = 'model_custom_100000.pt'
    # print(os.getcwd())
    output_name = Path(os.getcwd()).as_posix() + '/' + 'model' + '/' + model_name
    # print(output_name)
    if not os.path.exists(output_name):
        gdown.download(google_path+file_id,output_name,quiet=False)
        
    return str(output_name)