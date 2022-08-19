import torch
from torch import nn
# import torch.nn.functional as F
# from pathlib import Path
# import os
from app.library import model_download
import numpy as np
# https://velog.io/@dldydrhkd/AttributeError-Cant-get-attribute-BERTClassifier-on-module-main-from-path

def classification(save_list_add):

    class CustomModel(nn.Module):
        def __init__(self):
            super(CustomModel, self).__init__()

            self.layer = nn.Sequential(
                # nn.Linear(3, 3)
                nn.Linear(15, 3)
            )

        def forward(self, x):
            x = self.layer(x)
            return x

    device = "cuda" if torch.cuda.is_available() else "cpu"
        

    load_model_path = model_download.get_model_planerecnet_classification()
    # path_parents = Path(os.getcwd()).as_posix()
    # load_model_path = path_parents + '/' + 'model' + '/' + 'model_custom_100000.pt'

    # model = CustomModel().to(device)  
    # model = torch.load(load_model_path)
    model = CustomModel().to(device)
    model.load_state_dict(torch.load(load_model_path, map_location='cpu'))
    model.eval()

    # save_list_add =         [0.669,	0.873,	3.205,
    #         0.65,	0.117,	3.949,
    #         0.158,	0.098,	1.557,
    #         0.205,	0.594,	1.301,
    #         0.878,	0.685,	3.583] # 1 | attention



    with torch.no_grad():
        model.eval()
        classes = {0: "Safe", 1: "Attention", 2: "Warning"}
        # np.array(save_list_add, ndmin = 2)
        # inputs = np.array(save_list_add, ndmin = 2)
        inputs = torch.FloatTensor(np.array(save_list_add, ndmin = 2)).to(device)
        # inputs = torch.FloatTensor([save_list_add]).to(device)
        outputs = model(inputs)
        
        # print('---------')
        # print(outputs)
        # print(torch.round(F.softmax(outputs, dim=1)))
        # print(outputs.argmax(1))
        # result = list(map(classes.get, outputs.argmax(1).tolist()))[0]
        # print(list(map(classes.get, outputs.argmax(1).tolist())))
    
    return list(map(classes.get, outputs.argmax(1).tolist()))