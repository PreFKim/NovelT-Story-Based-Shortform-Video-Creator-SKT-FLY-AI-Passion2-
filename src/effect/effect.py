from ..video import Video

class Effect:
    def __init__(self,start_frame:int=0,end_frame:int=None):
        self.start_frame = start_frame
        self.end_frame = end_frame

    def __call__(self,video:Video):

        start_frame = 0 if self.start_frame is None else self.start_frame
        end_frame = len(video) if self.end_frame is None else self.end_frame
        
        if start_frame<0: 
            start_frame = max(start_frame + len(video),0)
        if end_frame<0: 
            end_frame = max(end_frame + len(video),0)

        start_frame = min(len(video),start_frame)
        end_frame = min(len(video),end_frame)

        video = video.copy()
        ret = self.effect(video,start_frame,end_frame)
        del video
        return ret