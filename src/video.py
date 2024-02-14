
import cv2
import numpy as np
import matplotlib.pyplot as plt


def im2vid(img,duration,fps=30):
    return Video([img]*duration*fps,fps=fps)

class Video:
    def __init__(self,video,fps):
        self.fps = fps
        self.video = video
        self.shape = (video[0].shape[:2])
        self.check_shape()
    
    def __str__(self):
        return f"Frame shape(h,w):{self.shape}, Num_frame:{len(self.video)}, FPS:{self.fps}, Duration:{len(self.video)/self.fps} Sec"
    
    def __repr__(self):
        return self.__str__()
    
    def __setitem__(self,idx,value):
        target_idx = []
        if isinstance(idx,list):
            for i in idx:
                target_idx.append(i)
        elif isinstance(idx,slice):
            start = 0 if idx.start is None else idx.start
            stop = len(self.video) if idx.stop is None else idx.stop
            step = 1 if idx.step is None else idx.step

            if start<0: start = max(start + len(self.video),0)
            if stop<0: stop = max(stop + len(self.video),0)

            start = min(len(self.video),start)
            stop = min(len(self.video),stop)

            target_idx.extend(list(range(start,stop,step)))
        else:
            target_idx = [idx]
        
        assert isinstance(value,Video), "Video 클래스가 아닙니다."
        assert len(target_idx) == len(value.video), "크기가 다릅니다."

        for i,v in zip(target_idx,value.resize(self.shape).video):
            self.video[i] = v
        
    def __getitem__(self,idx):
        if isinstance(idx,list):
            ret = []
            for i in idx:
                ret.append(self.video[i])
            return Video(video=ret,fps=self.fps)
        else:
            ret = self.video[idx]
            return Video(video=ret,fps=self.fps)

    def __add__(self,other):
        assert isinstance(other,Video), "Video 클래스가 아닙니다."
        
        other = other.copy()
        if (self.shape != other.shape):
            other.resize(self.shape)

        if (self.fps > other.fps):
            rest = self.fps % other.fps
            repeat = self.fps // other.fps
            ret = self.copy()

            for v in other.video:
                for _ in range(repeat+ int(rest>0)):
                    ret.video.append(v)
                rest = rest - 1 

        elif (self.fps < other.fps):
            step = other.fps / self.fps
            ret = self.copy()
            idx = 0.0
            while(idx<len(other.video)):
                ret.video.append(other.video[int(idx)])
                idx = idx + step
        else :
            ret = Video(video = self.video + other.video,fps=self.fps)

        return ret
            
    def copy(self):
        return Video(video=self.video.copy(),fps=self.fps)
    
    def check_shape(self):
        ret = True
        idx = []
        for i,v in enumerate(self.video):
            if (v.shape[:2]) != self.shape:
                idx.append(i)
                ret = False
        
        assert ret, f"일부 프레임의 크기가 다릅니다. idx:{idx}"
    
    def resize(self,shape):
        h, w = shape
        for i,frame in enumerate(self.video):
            self.video[i] = cv2.resize(frame,(w,h))
            #self.video[i] = cv2.resize(frame,tuple(reversed(shape))) # cv2는 (w,h) 형태이기 때문에 reversed후 reshape해야함
        self.shape = self.video[0].shape[:2]
        return self
    
    def pad(self,shape,color=(0,0,0),xy=None):
        h, w = shape
        ret = [np.full((h,w,3),color,dtype=np.uint8)]*len(self.video)

        if xy is None:
            x1,y1 = int((w-self.shape[1])/2), int((h-self.shape[0])/2)
        else:
            x1,y1 = xy

        for i,frame in enumerate(self.video):
            ret[i][y1:y1+self.shape[0],x1:x1+self.shape[1]] = frame
        self.video = ret
        self.shape = shape

        return self
    
    def show(self,idx1=0,idx2=None,step=None,figsize=(5,5)):
        ret = []
        if idx2 is None:
            if isinstance(idx1,list):
                for i in idx1:
                    ret.append(self.video[i])
            elif type(idx1)== int : 
                ret.append(self.video[idx1])
            else :
                assert False, "인덱스는 Integer, List 형식이 되어야 합니다."
        else :
            if idx2<0: idx2 = max(idx2 + len(self.video),0)

            idx2 = min(len(self.video)-1,idx2)
            step = 1 if step is None else step
                
            for i in range(idx1,idx2+1):
                ret.append(self.video[i])

        plt.figure(figsize=figsize)
        
        for i, v in enumerate(ret):
            plt.subplot(1,len(ret),i+1)
            plt.axis('off')
            plt.imshow(cv2.cvtColor(v,cv2.COLOR_BGR2RGB))
        plt.show()
        
        

    def save(self,path):
        self.check_shape()
        out = cv2.VideoWriter(path,cv2.VideoWriter_fourcc(*'DIVX'), self.fps, (self.shape[1],self.shape[0]))
        for i in range(len(self.video)):
            out.write(self.video[i])
        out.release()