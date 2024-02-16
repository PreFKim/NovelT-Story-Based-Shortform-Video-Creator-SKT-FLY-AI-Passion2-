from .transition import Transition
from ..video import Video
from ..operation import full
import cv2

class Blending(Transition):
    def __init__(self,num_frames:int=60,gamma=0):
        super(Blending,self).__init__(num_frames=num_frames)
        self.gamma = gamma

    def effect(self,inputs:list):
        h, w = inputs[0].shape
        ret = inputs[0]
        d = 1/self.num_frames
        for i in range(1,len(inputs)):
            alpha = 0
            transition = full(inputs[0].shape,self.num_frames,fps=inputs[0].fps)
            for j in range(self.num_frames):
                transition.video[j] = cv2.addWeighted(inputs[i-1].video[-1],1-alpha,inputs[i].video[0],alpha,self.gamma)
                alpha = alpha + d
            ret = ret + transition + inputs[i]
            # 부드러운 연계
            # for j in range(self.num_frames):
            #     transition.video[j] = cv2.addWeighted(inputs[i-1].video[-(self.num_frames+j)],1-alpha,inputs[i].video[j],alpha,self.gamma)
            #     alpha = alpha + d
            # ret = ret[:-(self.num_frames)] + transition + inputs[i][self.num_frames:]

        return ret