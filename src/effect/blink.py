from .effect import Effect
from ..video import Video
from .fade import gaussian
import numpy as np

class Blink(Effect):
    def __init__(self, start_frame:int=0, end_frame:int=None):
        super(Blink,self).__init__(start_frame=start_frame,end_frame=end_frame)

    def effect(self,video:Video):
        h,w = video.shape

        x = np.linspace(-3, 3, w)
        y = np.linspace(-3, 3, h)
        X, Y = np.meshgrid(x, y)

        duration = self.end_frame-self.start_frame
        ratio = (1/duration)*2
        for i in range(duration//3): # 눈뜨기
            video.video[i] = (video.video[i]*np.reshape(gaussian(X, Y, 0, 0, 3, i*ratio),(h,w,1))).astype(np.uint8)

        for i in range(duration//3,duration): # 감았다 뜨기
            video.video[i] = (video.video[i]*np.reshape(gaussian(X, Y, 0, 0, 3, duration//3 * ratio - 3 * (i-duration//3) * ratio),(h,w,1))).astype(np.uint8)
        
        return video