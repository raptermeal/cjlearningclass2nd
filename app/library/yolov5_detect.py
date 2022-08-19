from .yolov5.detect_custom import custom_args, main
import yaml
from pathlib import Path
import os

def path_name():
    path_model = 'model' + '/' + 'ramen_220817.pt'
    path_yaml = 'model' + '/' + 'ramen_korea.yaml'
    path_parents = Path(os.getcwd()).as_posix()
    return path_parents, path_model, path_yaml

def load_yaml(path_parents, path_model, path_yaml):
    path_yamldata = path_parents + '/' + path_yaml
    with open(path_yamldata,encoding="UTF-8") as f:
        data = yaml.load(f, Loader=yaml.loader.SafeLoader)    
    return data

def get_price(classs,class_data):
    price = []
    for yy in range(len(classs)):
        find_name = classs[yy]
        order = [i for i in range(len(class_data['names'])) if find_name in class_data['names'][i]][0]
        # order = class_data['names'].find(classs[yy])
        # print(order)
        price = price + [class_data['price'][int(order)]]
        
    # print('price',price)
    return price
    


def run(img_path):
    # img_path = 'images' + '/' + 'bus.jpg'
    # path_model = 'model' + '/' + 'ramen_220817.pt'
    # path_yaml = 'model' + '/' + 'ramen.yaml'
    # path_yaml = 'model' + '/' + 'ramen_korea.yaml'
    path_parents, path_model, path_yaml = path_name()
    conf_thres = '0.3'
    # path_model = 'model' + '/' + 'yolov5s.pt'
    # path_yaml = 'app/library/yolov5/data/coco128.yaml'
    device = 'cpu' #'cpu'
    opt = custom_args(img_path, path_model, path_yaml, conf_thres,device )
    print_result, rename_result = main(opt)
    # print(print_result, rename_result)
    
    if str(print_result)=='nodetect':
        # print_result==str('nodetect'):
        return int(1000),int(1000),img_path
    else:
        # print(print_result)
        list_result = []
        for i in range(len(print_result)):
            tt = print_result[i]
            tt = tt.split()
            ttt = tt[0]
            list_result = list_result + [ttt]
            
        # path_parents = Path(os.getcwd()).as_posix()
        data = load_yaml(path_parents, path_model, path_yaml)
        # path_yamldata = path_parents + '/' + path_yaml
        # with open(path_yamldata,encoding="UTF-8") as f:
        #     data = yaml.load(f, Loader=yaml.loader.SafeLoader)
            
        classs = []
        classs_n = []
        for i in range(500):
            a = list_result.count(str(i))
            if not a == 0:
                classs = classs + [data['names'][i]]
                classs_n = classs_n + [str(a)]
                # print(data['names'][i],i,a)
                
        # print(classs,classs_n)   
            
        return classs, classs_n, rename_result

# classs, classs_n, rename_result = run()
# print(classs,classs_n, rename_result)  

# yy = []
# for i in range(len(list_result)):
#     tt = list_result[i]
#     tt = tt.split()
#     ttt = tt[0]
#     yy = yy + [ttt]
    
# print(yy)

# path_yaml = 'app/library/yolov5/data/coco128.yaml'
# path_parents = Path(os.getcwd()).as_posix()
# path_yamldata = path_parents + '/' + path_yaml
# with open(path_yamldata,encoding="UTF-8") as f:
#     data = yaml.load(f, Loader=yaml.loader.SafeLoader)

# print(data)
# classs = []
# classs_n = []
# for i in range(100):
#     a = yy.count(str(i))
#     if not a == 0:
#         classs = classs + [data['names'][i]]
#         classs_n = classs_n + [a]
#         print(data['names'][i],i,a)
        
# print(classs,classs_n)

