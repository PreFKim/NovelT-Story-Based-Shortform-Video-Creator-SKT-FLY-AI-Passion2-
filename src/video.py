
import cv2
import numpy as np
import matplotlib.pyplot as plt


class Video:
    def __init__(self,video,fps):
        self.fps = fps
        self.video = video
        self.shape = (video[0].shape[:2])
        self.check_shape()
    
    def __str__(self):
        return f"Frame shape(h,w):{self.shape}, Num_frames:{len(self)}, FPS:{self.fps}, Duration:{len(self)/self.fps} Sec"
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.video)
    
    def __setitem__(self,idx,value):
        target_idx = []
        if isinstance(idx,list):
            for i in idx:
                target_idx.append(i)
        elif isinstance(idx,slice):
            start = 0 if idx.start is None else idx.start
            stop = len(self) if idx.stop is None else idx.stop
            step = 1 if idx.step is None else idx.step

            if start<0: start = max(start + len(self),0)
            if stop<0: stop = max(stop + len(self),0)

            start = min(len(self),start)
            stop = min(len(self),stop)

            target_idx.extend(list(range(start,stop,step)))
        else:
            target_idx = [idx]
        
        assert isinstance(value,Video), "Video 클래스가 아닙니다."
        assert len(target_idx) == len(value), "크기가 다릅니다."

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
            while(idx<len(other)):
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
        self.shape = self.video[0].shape[:2]
        return self
    
    def pad(self,shape,color=(0,0,0),xy=None):
        h, w = shape
        ret = [np.full((h,w,3),color,dtype=np.uint8)]*len(self)

        if xy is None:
            x1,y1 = int((w-self.shape[1])/2), int((h-self.shape[0])/2)
        else:
            x1,y1 = xy

        for i,frame in enumerate(self.video):
            ret[i][y1:y1+self.shape[0],x1:x1+self.shape[1]] = frame
        self.video = ret
        self.shape = shape

        return self
    
    def show(self):
        global playing
        playing = True 
        title = self.__str__()
        def on_trackbar(pos):
            cv2.imshow(title, self.video[pos])
        
        def on_space_press():
            global playing
            if cv2.getTrackbarPos('Frame', title) == len(self)-1:
                cv2.setTrackbarPos('Frame', title, 0)
            playing = not playing              

        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(title,450,800)
        cv2.createTrackbar('Frame', title, 0, len(self) - 1, on_trackbar)
        
        cv2.imshow(title, self.video[0])
        
        while True:

            key = cv2.waitKey(30)
            if key == 32:  # 스페이스바를 누르면 재생/일시정지
                on_space_press()
            elif key == 27:  # ESC를 누르면 종료
                break

            if playing:        
                if cv2.getTrackbarPos('Frame', title) < len(self)-1:
                    cv2.setTrackbarPos('Frame', title, cv2.getTrackbarPos('Frame', title)+1)
                else : 
                    playing = False

        cv2.destroyAllWindows()
        return True
    
    def save(self,path):
        self.check_shape()
        out = cv2.VideoWriter(path,cv2.VideoWriter_fourcc(*'DIVX'), self.fps, (self.shape[1],self.shape[0]))
        for i in range(len(self)):
            out.write(self.video[i])
        out.release()