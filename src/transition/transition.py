from ..operation import resize, set_fps

class Transition:
    def __init__(self,num_frames:int=60):
        self.num_frames = num_frames

    def __call__(self,inputs:list):

        for i in range(len(inputs)):

            if i >= 1:
                if (inputs[0].shape != inputs[i].shape):
                    inputs[i] = resize(inputs[i],inputs[0].shape)
                
                if (inputs[0].fps != inputs[i].fps):
                    inputs[i] = set_fps(inputs[i],inputs[0].fps)

        return self.effect(inputs)

