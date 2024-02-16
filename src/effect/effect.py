from ..video import Video

class Effect:
    def __init__(self,start_frame:int=0,end_frame:int=None):
        self.start_frame = start_frame
        self.end_frame = end_frame

    def __call__(self,video:Video):

        self.start_frame = 0 if self.start_frame is None else self.start_frame
        self.end_frame = len(video) if self.end_frame is None else self.end_frame
        
        if self.start_frame<0: self.start_frame = max(self.start_frame + len(video),0)
        if self.end_frame<0: self.end_frame = max(self.end_frame + len(video),0)

        self.start_frame = min(len(video),self.start_frame)
        self.end_frame = min(len(video),self.end_frame)

        video = video.copy()
        return self.effect(video)