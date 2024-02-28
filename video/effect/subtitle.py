from .effect import Effect
from ..video import Video
from ..operation import put_text, full

class Subtitle(Effect):
    def __init__(self,text, start_frame:int=0, end_frame:int=None, fontsize:int=None, color=(0,0,0), h_ratio:float =0.7, bg_color=(255,255,255)):
        super(Subtitle,self).__init__(start_frame=start_frame,end_frame=end_frame)
        self.text = text
        self.h_ratio = h_ratio
        self.color = color
        self.bg_color = bg_color
        self.fontsize = fontsize
        
    def effect(self,video:Video,start_frame:int,end_frame:int):

        h, w = video.shape

        if self.fontsize is None:
            fontsize = w//22
        else :
            fontsize = self.fontsize
        
        return put_text(video,self.text,start_frame,end_frame,fontsize=fontsize,color=self.color,center_xy=(w/2,h*self.h_ratio),bg_color=self.bg_color)

class Narration(Effect):
    def __init__(self,text, start_frame:int=0, end_frame:int=None, fontsize:int=None, color=(255,255,255), bg_color=(0,0,0)):
        super(Narration,self).__init__(start_frame=start_frame,end_frame=end_frame)
        self.text = text
        self.color = color
        self.bg_color = bg_color
        self.fontsize = fontsize
        
    def effect(self,video:Video,start_frame:int,end_frame:int):

        h, w = video.shape

        if self.fontsize is None:
            fontsize = w//16
        else :
            fontsize = self.fontsize

        video[start_frame:end_frame] = put_text(full(video.shape,end_frame-start_frame,color=self.bg_color),self.text,fontsize=fontsize,color=self.color)
        
        return video