from .transition import Transition
from ..video import Video
from ..operation import full
import cv2

class Blending(Transition):
    def __init__(self,num_frames:int=60,gamma=0):
        super(Blending,self).__init__(num_frames=num_frames)
        self.gamma = gamma

    def effect(self,x1:Video,x2:Video):
        d = 1/self.num_frames
        
        alpha = 0
        transition = full(x1.shape,self.num_frames,fps=x1.fps)
        for i in range(self.num_frames):
            transition.video[i] = cv2.addWeighted(x1.video[-1],1-alpha,x2.video[0],alpha,self.gamma)
            alpha = alpha + d

        return transition