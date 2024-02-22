from .effect import Effect
from ..video import Video

import cv2
import numpy as np

class Zoom_in(Effect):
    def __init__(self, start_frame:int=0, end_frame:int=None, xywh:list=None, exp=2):
        super(Zoom_in,self).__init__(start_frame=start_frame,end_frame=end_frame)
        self.xywh = xywh
        self.exp = exp
        
    def effect(self,video:Video,start_frame:int,end_frame:int):
        h,w = video.shape

        
        rh,rw = h*self.exp, w*self.exp
        from_xywh = np.array([0,0,1,1]) # x, y ,w ,h

        if self.xywh is None:
            to_xywh = np.array([0.1,0.1,0.8,0.8])
        else : 
            to_xywh = np.array(self.xywh) / [w,h,w,h]

        dxy = (from_xywh-to_xywh)/(end_frame-start_frame)
        lst = [from_xywh]
        for i in range(end_frame-start_frame-1):
            lst.append(lst[-1]-dxy)
        lst = np.array(lst)
        lst[:,[0,2]] = lst[:,[0,2]] * rw
        lst[:,[1,3]] = lst[:,[1,3]] * rh
        lst = np.round(lst,0).astype(np.int32)
        for i in range(len(lst)):
            resized = cv2.resize(video.video[i],(rw,rh))
            crop = resized[lst[i][1]:lst[i][1]+lst[i][3],lst[i][0]:lst[i][0]+lst[i][2]]
            video.video[i] = cv2.resize(crop,(w,h))
        for i in range(end_frame,len(video)):
            video.video[i] = video.video[end_frame-1].copy()
        
        return video


class Zoom_out(Effect):
    def __init__(self, start_frame:int=0, end_frame:int=None, xywh:list=None, exp=2):
        super(Zoom_out,self).__init__(start_frame=start_frame,end_frame=end_frame)
        self.xywh = xywh
        self.exp = exp
        
    def effect(self,video:Video,start_frame:int,end_frame:int):
        h,w = video.shape

        
        rh,rw = h*self.exp, w*self.exp
        if self.xywh is None:
            from_xywh = np.array([0.1,0.1,0.8,0.8])
        else : 
            from_xywh = np.array(self.xywh) / [w,h,w,h]
        to_xywh = np.array([0,0,1,1]) # x, y ,w ,h

        dxy = (from_xywh-to_xywh)/(end_frame-start_frame)
        lst = [from_xywh]
        for i in range(end_frame-start_frame-1):
            lst.append(lst[-1]-dxy)
        lst = np.array(lst)
        lst[:,[0,2]] = lst[:,[0,2]] * rw
        lst[:,[1,3]] = lst[:,[1,3]] * rh
        lst = np.round(lst,0).astype(np.int32)
        for i in range(len(lst)):
            resized = cv2.resize(video.video[i],(rw,rh))
            crop = resized[lst[i][1]:lst[i][1]+lst[i][3],lst[i][0]:lst[i][0]+lst[i][2]]
            video.video[i] = cv2.resize(crop,(w,h))
        for i in range(end_frame,len(video)):
            video.video[i] = video.video[end_frame-1].copy()
        
        return video