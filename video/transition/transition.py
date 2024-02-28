from ..operation import resize, set_fps

class Transition:
    def __init__(self,num_frames:int=60):
        self.num_frames = num_frames

    def __call__(self,x1,x2):

        if (x1.shape != x2.shape):
            x2 = resize(x2,x1.shape)
        
        if (x1.fps != x2.fps):
            x2 = set_fps(x2,x1.fps)

        ret = self.effect(x1,x2)
        return ret
        

