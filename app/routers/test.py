# from pathlib import Path
# import os
# url = 'https://static.hyundailivart.co.kr/upload_ctn/board/ME00000036/B000003365/B000003365_MnImgPath.jpg/dims/autorotate/on'

# img_full_path = Path(url).name
# print(img_full_path)

# import os
# from urllib.parse import urlparse

# url = 'http://www.plssomeotherurl.com/station.pls?id=111'
# path = urlparse(url).path
# ext = os.path.splitext(path)[1]
# print(ext)

import requests
from pathlib import Path

# req0 = requests.get('https://mall-image.tving.com/media/file/goods/2020/07/50a101706b3e69dec13b9ddb69aa9442.jpg')
# file = open("yes.jpg",mode="wb")
# file.write(req0.content)
# file.close()

# # 아래는 헤더 참고용 코드입니다.
# print(req0.headers)
url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSntroMb9pRv6LTpN_qr91ttN5t8s602LzJeQ&usqp=CAU'
req1 = requests.get(url)
if req1.headers['Content-Type'] == 'image/jpeg':
    ext = '.png'
filename = Path(url).name
filename_new = ''.join(char for char in filename if char.isalnum())
file = open(filename_new+ext,mode="wb")
file.write(req1.content)