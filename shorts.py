import glob, cv2, random, tqdm, src_video, moviepy, os
import numpy as np
from moviepy.editor import AudioFileClip, concatenate_videoclips, ImageSequenceClip, concatenate_audioclips, CompositeAudioClip


def identity(video:src_video.Video):
    return video

vfx_name = [
    "없음",
    "페이드 인",
    "페이드 아웃",
    "줌 인",
    "줌 아웃",
    "눈 깜빡임 효과",
    "갈라짐 효과",
    "떨림 효과",
    "배경 없이 나레이션만"
]

narr_idx = 8

vfx = [
    identity,
    src_video.effect.Fade_in(0,60),
    src_video.effect.Fade_out(-60),
    src_video.effect.Zoom_in(0),
    src_video.effect.Zoom_out(0),
    src_video.effect.Blink(0,60),
    src_video.effect.Crack(60),
    src_video.effect.Shake(60,120),
    identity
]

def apply_subtitle(video:src_video.Video, vfx:int, subtitle:list,audio_frames:list):
    start_frame = 0
    ret = video
    
    for i in range(len(subtitle)):
        if subtitle[i] != "":
            if vfx == narr_idx:
                ret = src_video.effect.Narration(subtitle[i],start_frame=start_frame,end_frame=start_frame+audio_frames[i])(ret)
            else:
                ret = src_video.effect.Subtitle(subtitle[i],start_frame=start_frame,end_frame=start_frame+audio_frames[i],color=(255,255,255),bg_color=(0,0,0))(ret)
        start_frame = start_frame + audio_frames[i]
    return ret

def floor(lst:list):
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            lst[i][j] = int(lst[i][j])
    return lst


def create_video(images,audio,subtitle,effects,bgm_path,save_path,last_narr=True,bgm_volume=1.0):
    fps = 60 # 영상 프레임

    imgs = [] # 이미지 모음
    audios = [] # 오디오 클립

    audio_frames = [] # 오디오별 프레임 길이

    for p in images:
        imgs.append(cv2.cvtColor(cv2.imread(p),cv2.COLOR_BGR2RGB))
    bgm = AudioFileClip(bgm_path)

    
    for img in imgs:
        print(img.shape)
    # 오디오 길이 추출
    idx = 0 
    for i in range(len(subtitle)):
        audios.append([])
        audio_frames.append([])
        for j in range(len(subtitle[i])):
            audios[i].append(AudioFileClip(audio[idx]))
            audio_frames[i].append(audios[i][j].duration*fps)
            idx = idx + 1
    audio_frames = floor(audio_frames)


    # 장면 전환
    transition_frames = [20,20]
    transition_lst = [src_video.transition.Slide,src_video.transition.Blending]
    transition = []
    for i in range(1,len(imgs)):
        idx = random.randint(0,len(transition_lst)-1)
        transition.append(transition_lst[idx](transition_frames[idx]))

    # 장면 효과
    vfx_idx = []
    for j,e in enumerate(effects):
        for i in range(len(vfx_name)):
            if e.find(vfx_name[i]) != -1:
                vfx_idx.append(i)
                break
            elif i == len(vfx_name)-1:
                vfx_idx.append(random.randint(1,4))

    # 마지막 나레이션 영상 효과 (더 자세한 내용은 '~~' 에서!)
    if last_narr:
        imgs.append(np.zeros_like(imgs[-1],dtype=np.uint8))
        transition.append(transition_lst[1](transition_frames[1]))
        vfx_idx.append(narr_idx)

    print("이미지 수 :",len(imgs),", 나레이션 수 :",len(audios)," 효과 수 :",len(vfx_idx))

    # 장면별 영상 효과, 자막 적용
    videos = [apply_subtitle(vfx[vfx_idx[0]](src_video.im2vid(imgs[0],sum(audio_frames[0]))),vfx_idx[0],subtitle[0],audio_frames[0])]
    for i in tqdm.tqdm(range(1,len(imgs))):
        x1 = videos[-1]
        x2 = apply_subtitle(vfx[vfx_idx[i]](src_video.im2vid(imgs[i],sum(audio_frames[i]))),vfx_idx[i],subtitle[i],audio_frames[i])
        videos.append(transition[i-1](x1,x2))
        videos.append(x2)

    # 영상에 오디오 입히기
    video_lst = []
    for i in tqdm.tqdm(range(len(videos))):
        vid = ImageSequenceClip(videos[i].video, fps=fps)

        if i%2 == 0:
            video_lst.append(vid.set_audio(concatenate_audioclips(audios[i//2])))
        else :
            video_lst.append(vid)
        
    video_clip = concatenate_videoclips(video_lst)
    new_audio = CompositeAudioClip([video_clip.audio,bgm.audio_loop(duration=video_clip.duration).volumex(bgm_volume)])
    video_clip.audio = new_audio


    # 비디오를 저장합니다.
    video_clip.write_videofile(save_path)