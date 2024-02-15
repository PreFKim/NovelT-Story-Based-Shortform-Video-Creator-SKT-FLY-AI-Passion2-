import cv2
from PIL import Image, ImageFont, ImageDraw
import numpy as np
from .video import Video

def im2vid(img,num_frames:int,fps=60):
    if isinstance(img,str):
        img = cv2.imread(img)
    return Video([img for _ in range(num_frames)],fps=fps)

def read_video(path:str):
    video = []
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    while(True):
        ret,frame = cap.read()
        if ret == False: break
        video.append(frame)
    cap.release()
    return Video(video=video,fps=fps)
    

def put_text(video:Video,text:str,start_frame:int,end_frame:int,fontsize=12,color:tuple=(0,0,0),center_xy:tuple=None):
    ret = video.copy()
    h,w = video.shape

    if center_xy is None:
        x1, y1 = w/2,h/2
    else :
        x1, y1 = center_xy

    for i in range(start_frame,end_frame):
        img_pillow = Image.fromarray(ret.video[i]).convert('RGB')

        fontpath = "./fonts/gulim.ttc"
        font = ImageFont.truetype(fontpath, fontsize)
        draw = ImageDraw.Draw(img_pillow, 'RGB')
        draw.text([x1, y1],text=text, font=font, anchor='mm', fill=(color[2],color[1],color[0]))

        ret.video[i] = np.array(img_pillow,dtype=np.uint8)
    return ret

def set_fps(video:Video,fps:float=60):
    ret = video.copy()
    ret.set_fps(fps)
    return ret

def full(shape,num_frames:int,color:tuple=(0,0,0),fps:float=60):
    h,w = shape
    return Video(video=[np.full((h,w,3),color,dtype=np.uint8) for _ in range(num_frames)],fps=fps)

def pad(video:Video,shape,color:tuple=(0,0,0),xy:tuple=None):
    ret = video.copy()
    ret.pad(shape=shape,color=color,xy=xy)
    return ret

def resize(video:Video,shape):
    ret = video.copy()
    ret.resize(shape=shape)
    return ret