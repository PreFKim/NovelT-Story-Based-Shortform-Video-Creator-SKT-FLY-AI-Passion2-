from .effect import Effect
from ..video import Video
import numpy as np

def gaussian(x, y, x0, y0, sigma_x, sigma_y, eps=1e-6):
    return np.exp(-((x-x0)**2 / (2*sigma_x**2+eps) + (y-y0)**2 / (2*sigma_y**2+eps)),dtype=np.float32)

class Fade_in(Effect):
    def __init__(self, start_frame:int=0, end_frame:int=None):
        super(Fade_in,self).__init__(start_frame=start_frame,end_frame=end_frame)

    def effect(self,video:Video,start_frame:int,end_frame:int):
        h,w = video.shape

        x = np.linspace(-3, 3, w)
        y = np.linspace(-3, 3, h)
        X, Y = np.meshgrid(x, y)

        ratio = (3/(end_frame-start_frame))*2

        for i in range(start_frame):
            video.video[i] = (video.video[i]*np.reshape(gaussian(X, Y, 0, 0, 0, 0),(h,w,1))).astype(np.uint8)
            
        for i in range(start_frame,end_frame):
            video.video[i] = (video.video[i]*np.reshape(gaussian(X, Y, 0, 0, (i-start_frame)*ratio, (i-start_frame)*ratio),(h,w,1))).astype(np.uint8)


        return video

class Fade_out(Effect):
    def __init__(self, start_frame:int=0, end_frame:int=None):
        super(Fade_out,self).__init__(start_frame=start_frame,end_frame=end_frame)

    def effect(self,video:Video,start_frame:int,end_frame:int):
        h,w = video.shape

        x = np.linspace(-3, 3, w)
        y = np.linspace(-3, 3, h)
        X, Y = np.meshgrid(x, y)

        ratio = (3/(end_frame-start_frame))*2

        for i in reversed(range(start_frame,end_frame)):
            video.video[start_frame+end_frame-(i+1)] = (video.video[i]*np.reshape(gaussian(X, Y, 0, 0, (i-start_frame)*ratio, (i-start_frame)*ratio),(h,w,1))).astype(np.uint8)

        for i in range(end_frame,len(video)):
            video.video[i] = video.video[end_frame-1].copy()
        
        return video


    