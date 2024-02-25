from .effect import Effect
from ..video import Video

import cv2
import numpy as np
import random

def crack_effect(img,from_x,from_y):
    h,w,_ = img.shape

    if (from_y<h):

        if from_y > 0.5:
            n = random.choices([1,2],[0.8,0.2])[0] 
        else : 
            n = random.choices([1,2],[0.9,0.1])[0] 

        for _ in range(n):
            to_x = from_x + int(np.random.uniform(-w*0.15,w*0.15))
            to_y = from_y + int(np.random.uniform(h*0.1,h*0.15))

            cv2.line(img,(from_x,from_y),(to_x,to_y),(0.0,0.0,0.0),int(w*0.025))
            crack_effect(img,to_x,to_y)
    return img

class Crack(Effect):
    def __init__(self, start_frame:int=0, x_ratio:tuple=(0.4,0.6)):
        super(Crack,self).__init__(start_frame=start_frame)
        self.x_ratio = x_ratio
        
    def effect(self,video:Video,start_frame:int,end_frame:int):
        l, r = self.x_ratio

        h,w = video.shape
        from_x = int(w*random.uniform(l,r))
        
        ret = crack_effect(np.ones((h,w,3))*0.75,from_x,0)

        for i in range(start_frame,start_frame+video.fps//10):
            video.video[i] = np.ones((h,w,3),dtype=np.uint8)*255

        for i in range(start_frame+video.fps//10,start_frame+2*(video.fps//10)):
            video.video[i] = (video.video[i]*ret).astype(np.uint8)

        for i in range(start_frame+2*(video.fps//10),start_frame+3*(video.fps//10)):
            video.video[i] = np.ones((h,w,3),dtype=np.uint8)*255

        for i in range(start_frame+3*(video.fps//10),len(video)):
            video.video[i] = (video.video[i]*ret).astype(np.uint8)
        
        return video