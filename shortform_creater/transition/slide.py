from .transition import Transition
from ..video import Video
from ..operation import full
import random


class Slide(Transition):
    def __init__(self,num_frames:int=60,mode:int=-1):
        super(Slide,self).__init__(num_frames=num_frames)
        self.mode = mode
        

    def effect(self,x1:Video,x2:Video):
        h, w = x1.shape
        
        mode = random.randint(0,3) if self.mode==-1 else self.mode
        transition = full(x1.shape,self.num_frames,fps=x1.fps)
        if mode == 0:
            d = -h/self.num_frames
            border = h-1
            for i in range(self.num_frames):
                transition.video[i][:int(border)] = x1.video[-1][-int(border):]
                transition.video[i][int(border):] = x2.video[0][:-int(border)]
                border = border + d
        elif mode == 1:
            d = h/self.num_frames
            border = 1
            for i in range(self.num_frames):
                transition.video[i][int(border):] = x1.video[-1][:-int(border)]
                transition.video[i][:int(border)] = x2.video[0][-int(border):]
                border = border + d
        elif mode == 2:
            d = -w/self.num_frames
            border = w-1
            for i in range(self.num_frames):
                transition.video[i][:,:int(border)] = x1.video[-1][:,-int(border):]
                transition.video[i][:,int(border):] = x2.video[0][:,:-int(border)]
                border = border + d
        elif mode == 3:
            d = w/self.num_frames
            border = 1
            for i in range(self.num_frames):
                transition.video[i][:,int(border):] = x1.video[-1][:,:-int(border)]
                transition.video[i][:,:int(border)] = x2.video[0][:,-int(border):]
                border = border + d
    

        return transition