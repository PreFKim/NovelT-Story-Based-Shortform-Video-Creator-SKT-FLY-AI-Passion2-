
def pad(video,shape,color=(0,0,0),xy=None):
    ret = video.copy()
    ret.pad(shape=shape,color=color,xy=xy)
    return ret

def resize(video,shape):
    ret = video.copy()
    ret.resize(shape=shape)
    return ret