import gdown
import os
from pathlib import Path
 
def get_model_planerecnet():
    google_path = 'https://drive.google.com/uc?id='
    file_id = '1s4B-TSii7Qho-7J7_boZdHuIzt4Fx-nv'
    model_name = 'PlaneRecNet_101_9_125000.pth'
    print(os.getcwd())
    output_name = Path(os.getcwd()).as_posix() + '/' + 'model' + '/' + model_name
    # print(os.path.exists(output_name))

    if not os.path.exists(output_name):
        gdown.download(google_path+file_id,output_name,quiet=False)