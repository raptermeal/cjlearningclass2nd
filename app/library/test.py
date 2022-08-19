import os
import random
# image1_path = Path("Upload/image/220803105932_color_seg.png")
img_folfer = 'C:/Users/CJ/fastapi-web-starter/Upload/image'
# image1_path = "Upload/image/220803105932_color_seg.png"
# image2_path = "Upload/image/example_nyu_seg.jpg"
# os.walk(img_folfer)

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
    
    
img_path_list = uu(img_folfer)
print(img_path_list)

