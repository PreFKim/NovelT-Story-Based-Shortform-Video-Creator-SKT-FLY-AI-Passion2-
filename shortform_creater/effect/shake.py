from .effect import Effect
from ..video import Video

import cv2
import numpy as np

class Shake(Effect):
    def __init__(self, start_frame:int=0, end_frame:int=None, xywh:list=None, exp=2):
        super(Shake,self).__init__(start_frame=start_frame,end_frame=end_frame)
        self.xywh = xywh
        self.exp = exp
        
    def effect(self,video:Video,start_frame:int,end_frame:int):
        h,w = video.shape

        
        rh,rw = h*self.exp, w*self.exp

        if self.xywh is None:
            xywh = np.array([0.1,0.1,0.8,0.8])
        else : 
            xywh = np.array(self.xywh) / [w,h,w,h]

        
        lst = [xywh]
        for i in range(end_frame-start_frame-1):

            diff = np.array([
                np.random.uniform((-lst[-1][0])/30,(1-(lst[-1][0]+lst[-1][2]))/30),
                np.random.uniform((-lst[-1][1])/30,(1-(lst[-1][1]+lst[-1][3]))/30),
                0,
                0
            ])
            lst.append(lst[-1]+diff)
        lst = np.array(lst)

        lst[:,[0,2]] = lst[:,[0,2]] * rw
        lst[:,[1,3]] = lst[:,[1,3]] * rh
        lst = np.round(lst,0).astype(np.int32)

        for i in range(start_frame):
            resized = cv2.resize(video.video[i],(rw,rh))
            crop = resized[lst[0][1]:lst[0][1]+lst[0][3],lst[0][0]:lst[0][0]+lst[0][2]]
            video.video[i] = cv2.resize(crop,(w,h))


        for i in range(start_frame, end_frame):
            resized = cv2.resize(video.video[i],(rw,rh))
            crop = resized[lst[i-start_frame][1]:lst[i-start_frame][1]+lst[i-start_frame][3],lst[i-start_frame][0]:lst[i-start_frame][0]+lst[i-start_frame][2]]
            video.video[i] = cv2.resize(crop,(w,h))

        for i in range(end_frame,len(video)):
            video.video[i] = video.video[end_frame-1].copy()
        
        return video


