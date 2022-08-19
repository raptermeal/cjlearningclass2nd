from gtts import gTTS
import os
from pathlib import Path
# __author__ = 'info-lab'
# imgpath = 'Upload/image.png'
# text = '오마이갓'


def makedirs(path): 
   try: 
        os.makedirs(path) 
   except OSError: 
       if not os.path.isdir(path): 
           raise
       
def save_sound(path_voice_root,file_path,text:str):
    tts = gTTS(
        text,
        lang='ko', slow=False
    )
    # root_path = 'Upload/sound'
    makedirs(path_voice_root)
    save_path = path_voice_root + '/' + os.path.basename(file_path).split('.')[0] + '.mp3'
    filename = os.path.basename(file_path).split('.')[0] + '.mp3'
    save_path1 = os.path.basename(file_path).split('.')[0] + '.mp3'
    tts.save(save_path)
    
    return filename
    # return str(Path(save_path))
    
# print(save_sound(imgpath,text))