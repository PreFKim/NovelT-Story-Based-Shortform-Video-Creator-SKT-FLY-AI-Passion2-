from .transition import Transition
from ..video import Video
from ..operation import full
import random


class Slide(Transition):
    def __init__(self,num_frames:int=60,mode:int=-1):
        super(Slide,self).__init__(num_frames=num_frames)
        self.mode = mode
        

    def effect(self,inputs:list):
        h, w = inputs[0].shape

        ret = inputs[0]


        for i in range(1,len(inputs)):
            mode = int(random.uniform(0,4)) if self.mode==-1 else self.mode
            transition = full(inputs[0].shape,self.num_frames,fps=inputs[0].fps)
            if mode == 0:
                d = -h/self.num_frames
                border = h-1
                for j in range(self.num_frames):
                    transition.video[j][:int(border)] = inputs[i-1].video[-(j+1)][-int(border):]
                    transition.video[j][int(border):] = inputs[i].video[j][:-int(border)]
                    border = border + d
            elif mode == 1:
                d = h/self.num_frames
                border = 1
                for j in range(self.num_frames):
                    transition.video[j][int(border):] = inputs[i-1].video[-(j+1)][:-int(border)]
                    transition.video[j][:int(border)] = inputs[i].video[j][-int(border):]
                    border = border + d
            elif mode == 2:
                d = -w/self.num_frames
                border = w-1
                for j in range(self.num_frames):

                    transition.video[j][:,:int(border)] = inputs[i-1].video[-(j+1)][:,-int(border):]
                    transition.video[j][:,int(border):] = inputs[i].video[j][:,:-int(border)]
                    border = border + d
            elif mode == 3:
                d = w/self.num_frames
                border = 1
                for j in range(self.num_frames):
                    transition.video[j][:,int(border):] = inputs[i-1].video[-(j+1)][:,:-int(border)]
                    transition.video[j][:,:int(border)] = inputs[i].video[j][:,-int(border):]
                    border = border + d
            ret = ret + transition + inputs[i]


        return ret