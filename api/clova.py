from config import *
import urllib
import tqdm

from gpt import match_voice_actor

speaker_param = {
    "nyejin" : [0,-2,0,0],
    "nmovie" : [0,-2,0,-1],
    "nhajun" : [0,-1,0,0],
    "ndain" : [0,-3,0,0],
    "ndaeseong" : [0,-1,0,0],
    "nian" : [0,-3,0,0],
    "nnarae" : [0,-2,0,0],
    "nara" : [0,-2,0,0]
}

def create_voice(audio_path, subtitle, character_prompt):
    audio_path_list = []
    idx = 0
    speakers = match_voice_actor(subtitle,character_prompt)

    print(speakers)
    for i in tqdm.tqdm(range(len(subtitle))):
        for j in range(len(subtitle[i])):
            if (subtitle[i][j] != ""):
                volume,speed,pitch,alpha = speaker_param[speakers[idx]]
                data = f"speaker={speakers[idx]}&volume={volume}&speed={speed}&pitch={pitch}&alpha={alpha}&format=mp3&text={urllib.parse.quote(subtitle[i][j])}"
    
                request = urllib.request.Request("https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts")
                request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
                request.add_header("X-NCP-APIGW-API-KEY",client_secret)
                response = urllib.request.urlopen(request, data=data.encode('utf-8'))
                rescode = response.getcode()

                if(rescode==200):
                    response_body = response.read()
                    with open(f'{audio_path}/{i:02d}-{j:02d}.mp3', 'wb') as f:
                        f.write(response_body)
                    audio_path_list.append(f'{audio_path}/{i:02d}-{j:02d}.mp3')
                else:
                    return False
                idx += 1
                
    return audio_path_list