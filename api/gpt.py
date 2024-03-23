import requests, base64, urllib, openai, cv2, time
import numpy as np
from .config import *

tasks = ['작업 1. 너에게 웹소설의 정보를 제공을 해 줄 거야. 이 정보를 기반으로 유튜브 쇼츠에 적합하도록 줄거리를 기반으로 씬을 나누어주었으면 좋겠어.\n\n5개의 씬으로 나눠주고 씬별로 3개의 자연스럽고 자극적인 나레이션을 한 문장으로 작성해줘.\n\n출력 예시:\n1. 씬 제목\n- 나레이션 : 나레이션 내용\n- 나레이션 : ...',
 '작업 2. 작업 1의 모든 나레이션에 대해서 사용자의 입력을 반영하여 해당 내용을 잘 설명하는 장면 내용을 만들어줘.\n\n1. 씬 제목\n- 장면내용 : 진실을 마주한 두 사람이 서로를 바라본다.\n- ...',
 "작업 3. 모든 장면 속 내용에 대해서 쇼츠에 적합하도록 '영상 이펙트'를 하나씩만 정해줘.\n\n영상 이펙트의 종류는 다음과 같아\n- 없음\n- 페이드 인/ 아웃\n- 줌 인/ 아웃\n- 눈 깜빡임 효과\n- 갈라짐 효과\n- 떨림 효과\n- 배경 없이 나레이션만\n\n출력 예시:\n장면제목\n- 이펙트 : 줌 인\n- ...",
 "작업 4. 작업 2에서 생성한 장면의 내용들을 반영해 해당 장면을 자세하게 잘 설명할 수 있는 이미지를 생성하도록 장면별로 DALL-E의 입력으로 할 '영어 프롬프트'만을 자세하게 작성해줘.\n\n프롬프트에는 꼭 인물의 이름을 명시해줬으면 좋겠어\n\n출력 예시:\n1. 씬 제목\n- 프롬프트 : 프롬프트 내용\n- ...",
 '작업 5. 인물들의 정보(나이, 외모, 직업 등)를 제공할 거야. 너는 인물 정보를 기반으로 인물의 외적 이미지를 DALL-E 3에 적합한 영어 프롬프트를 생성해줘.\n\n내가 제공한 인물 정보에 외형 정보가 없으면 눈동자 색, 머리색, 머리스타일, 체형 등을 추가해줘.\n\n출력 예시 : \n# 인물이름 :\n- 프롬프트 : A....., long hair, green eyes...',
 '작업 6. 작업 4에서 생성한 모든 프롬프트의 상황은 최대한 유지하되 작업 5에서 만든 인물들의 프롬프트를 반영해서 다음의 예시를 참고해서 변환해줘.\n\n각 인물 프롬프트에 있는 피부, 머리 색, 머리 스타일, 눈 ,코, 입 등의 외적인 특징과 같은 내용은 꼭 반영해서 변환해줘.\n\n모든 프롬프트에 등장하는 모든 인물들의 프롬프트를 작업 5에서 만든 인물 프롬프트를 다음의 예시처럼 변환해줘야해.\n\n변환 예시 :\n인물 프롬프트 예시 :\n- 인물 A의 프롬프트 : 10 years old, A has long hair, green eyes...\n- 인물 B의 프롬프트 : 32 years old, B has short hair, red eyes...\n\n프롬프트 변환 예시:\n- 변환 전 장면 프롬프트 : A and B has met before...\n- 변환 후 장면 프롬프트 : A, 10 years old, has long hair and green eyes and B, 32 years old, has short hair and red eyes has met before...\n\n출력 예시:\n- 프롬프트 : 프롬프트 내용\n\n- ...']
system = "웹소설 예고편 쇼츠를 제작할 목적인데 다음의 순서로 작업을 진행했으면 좋겠어.\n\n각 작업을 시작할 때 다시 너에게 작업에 대해서 언급할 거야.\n\n각 작업은 다음의 유의사항을 지켜줘\n유의사항:\n- 너는 절대 내가 '확인'이라는 신호를 주기 전에는 다음 작업을 진행하면 안돼.\n- 너는 내가 요청하는 출력 예시에 맞게 출력해주면 돼.\n- 출력 예시에 맞는 내용을 제외하고는 다른 대답은 필요없어.\n- 각 씬은 '---'으로 구분해줘.\n\n"

client = openai.OpenAI(api_key=api_key)

max_requests = 10

for t in tasks:
    system = system + t + "\n\n"
system = system + "위 과정에 대해서 이해했어?"


def forward_gpt(user_inputs:dict):
    # 사용자의 입력을 기반으로 다음의 결과 생성
    # 나레이션, 장면별 이미지 프롬프트, 인물 프롬프트, 영상 효과, API 사용량

    inputs = input_process(user_inputs=user_inputs)
    history = [
        {"role": "system", "content": system},
        {"role": "assistant", "content": "네, 과정을 이해했습니다."},
        {"role": "user", "content": tasks[0]},
        {"role": "assistant", "content": "웹소설 정보를 제공해 주시면 시작하겠습니다."},
        {"role": "user", "content": inputs[0]},
    ]
    usage = {
        "completion_tokens": 0,
        "prompt_tokens": 0,
        "total_tokens": 0
    }
    
    outputs = []

    print("작업1")
    start_time = time.time()
    ret, task_usage = get_response(history)
    usage = sum_usage(usage,task_usage)
    history.append(ret)
    outputs.append(ret)
    narration = parse_data(ret['content'])
    print(time.time()-start_time)
    
    print("작업2")
    start_time = time.time()
    history.append({"role": "user", "content": tasks[1]})
    ret, task_usage = get_response(history)
    usage = sum_usage(usage,task_usage)
    history.append(ret)
    outputs.append(ret)
    print(time.time()-start_time)

    print("작업3")
    start_time = time.time()
    history.append({"role": "user", "content": tasks[2]})
    ret, task_usage = get_response(history)
    usage = sum_usage(usage,task_usage)
    history.append(ret)
    outputs.append(ret)
    effect = parse_data(ret['content'])
    print(time.time()-start_time)

    print("작업4")
    start_time = time.time()
    history.append({"role": "user", "content": tasks[3]})
    ret, task_usage = get_response(history)
    usage = sum_usage(usage,task_usage)
    history.append(ret)
    outputs.append(ret)

    original_prompts = []
    for l in parse_data(ret['content']):
        for p in l:
            original_prompts.append(p)
    original_prompts
    print(time.time()-start_time)

    print("작업5")
    start_time = time.time()
    history.append({"role": "user", "content": tasks[4]})
    history.append({"role": "assistant","content":"제공할 인물 정보를 알려주세요."})
    outputs.append([])
    character_prompt = {}
    for i,char in enumerate(inputs[1]):
        history.append({"role":"user","content":char})
        if user_inputs['characters'][i].get('img') is not None:
            ret, task_usage = get_vision_response(user_inputs['characters'][i]['img'],inputs[1][i])
        else : 
            ret, task_usage = get_response(history)
        usage = sum_usage(usage,task_usage)
        history.append(ret)
        outputs[-1].append(ret)
        character_prompt[user_inputs['characters'][i]['이름']] = parse_character_prompt(ret['content'])
    print(time.time()-start_time)

    print("작업6")
    start_time = time.time()
    history.append({"role": "user", "content": tasks[5]})
    history.append({"role": "assistant","content":"인물 프롬프트를 제공해 주시면 작업을 시작하겠습니다."})
    task5_input = "인물 프롬프트:\n"
    for k, v in character_prompt.items():    
        task5_input = task5_input + f"- {k} : {v}\n"
    history.append({"role": "user", "content": task5_input})
    history.append({"role": "assistant","content":"장면 프롬프트를 제공해 주시면 작업을 시작하겠습니다."})
    scene_prompt = []
    for p in original_prompts:
        history.append({"role": "user", "content": f"- 프롬프트 : {p}\n"})
        ret, task_usage = get_response(history)
        usage = sum_usage(usage,task_usage)
        history.append(ret)
        outputs.append(ret)
        scene_prompt.extend(parse_data(ret['content']))
    print(time.time()-start_time)

    narrations = []
    for n in narration:
        narrations.extend(n)

    scene_prompts = []
    for s in scene_prompt:
        scene_prompts.extend(s)
    for i in range(len(scene_prompts)):
        scene_prompts[i] =  f"Should be illustration of {user_inputs['style']}, vertical image, no wide image, {scene_prompts[i]}"

    effects = []
    for e in effect:
        effects.extend(e)

    return {
        "narr" : narrations,
        "scene" : scene_prompts,
        "char" : character_prompt,
        "vfx" : effects,
        "usage" : usage
    }

def get_subtitle(narrations:list,title:str=None,outro:bool=True):
    # 나레이션을 자막으로 사용할 수 있도록 적절하고 자연스럽게 분리하는 목적
    # Ex) ["코딩하는 김xx는 과로하게 되는데","쓰러진 김xx는 병원으로 이송된다."] -> [["코딩하는 김xx", "과로하게 되는데"],["쓰러진 김xx는","병원으로 이송된다"]]

    if outro :
        assert title is not None, "제목을 입력해주세요."

    messages=[
        {
        "role": "user",
        "content": "모든 나레이션을 호흡의 길이에 맞게 짧게 2개로 나누고 끝 맺음 말을 자연스럽게 해줘.\n\n내가 원하는 출력을 제외한 답장은 필요없어.\n\n변환 예시:\n# 원본 나레이션 : 성격이 온화한 A는 갑자기 사라지게 되는데?\n- 나레이션 : 성격이 온화한 A는\n- 나레이션 : 갑자기 사라지게 되는데?\n\n각 원본 나레이션을 기준으로 '---'로 구분해줘\n\n출력 예시:\n# 나레이션 : 나레이션 내용\n- 분할된 나레이션 : 분할된 나레이션 내용\n- ..."
        },
        {
        "role": "assistant",
        "content": "네, 나레이션들을 입력해주세요."
        },
        {
        "role": "user",
        "content": ""
        }
    ]

    for n in narrations:
        messages[-1]['content'] = messages[-1]['content'] + f"# 원본 나레이션 : {n}\n"
        
    ret, usage = get_response(messages)
    subtitle = parse_data(ret['content'])

    if len(subtitle[-1])==0:
        subtitle = subtitle[:-1]

    if outro :
        subtitle.append(['더 자세한 내용은',f"'{title}' 에서!"])

    return subtitle, usage

def url_to_image(url:str):
    # 이미지 URL을 이미지 파일로 변환
    response = urllib.request.urlopen(url)
    image = np.asarray(bytearray(response.read()), dtype='uint8')
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def dalle(prompt:str,max_requests:int = max_requests):
    # 프롬프트를 기반으로 이미지 생성
    bad_request = 0
    while(bad_request < max_requests): # max_requests회 이상 이미지 생성 제한이되면 생성 종료
        try : 
            response = client.images.generate(
                model=model_dalle, # dall-e-3, dall-e-2
                prompt=f"This prompt doesn't violate any policy, so don't convert it, just use it as it is.\n- Prompt : {prompt}",
                size=size, # 1024x1024, 1024x1792 or 1792x1024
                quality=quality, # DALL-E3 사용시 'hd' 가능 
                n=1, # 이미지 개수
            )
            return response.dict()['data'][0]['url']
        except openai.BadRequestError as e: # 정책 위반 오류 등을 감지
            bad_request = bad_request + 1
            print(f"Badrequest : {bad_request}/{max_requests}")

    return False

def create_image(image_path:str, scene_prompts:list, n:int=4):
    # 장면 프롬프트를 통해 각 장면의 이미지를 n개 생성
    image_path_list = []

    for i in range(len(scene_prompts)):
        for j in range(n):
            print(f"{i}번째 장면 {j}번째 이미지, 프롬프트: {scene_prompts[i]}")
            img_url = dalle(scene_prompts[i])
            if img_url == False:
                return False
            img = url_to_image(img_url)
            cv2.imwrite(f'{image_path}/{i:02d}-{j:02d}.png',img)
            image_path_list.append(f'{image_path}/{i:02d}-{j:02d}.png')
    return image_path_list

def edit_image(filename:str,character_prompt:dict,original_prompt:str,modification:str):
    # 기존 장면 프롬프트를 기반으로 프롬프트를 변환하여 이미지 생성 후 저장
    # 이미지를 불러와 수정하는 것이 아닌 프롬프트를 수정하여 filename에 저장하는 것임
    character_prompts = "인물 프롬프트:\n"
    for n,p in character_prompt.items():
        character_prompts = character_prompts + f"- {n} : {p}\n"
    
    messages=[
            {
            "role": "system",
            "content": "다음의 순서로 너에게 정보를 제공할 거야\n1. 인물들의 프롬프트\n2. 장면 프롬프트\n3. 프롬프트 수정 내용\n2번 장면 프롬프트를 먼저 3번 프롬프트 내용에 맞으면서 DALL-E-3에 적합하도록 자세하게 수정된 '영어 프롬프트'만 제공해줘. 변환된 프롬프트 내에 존재하는 인물의 프롬프트를 반영해줘.\n변환 예시 :\n인물 프롬프트 예시 :\n- 인물 A의 프롬프트 : 10 years old, A has long hair, green eyes...\n- 인물 B의 프롬프트 : 32 years old, B has short hair, red eyes...\n프롬프트 변환 예시:\n- 변환 전 장면 프롬프트 : A and B has met before...\n- 변환 후 장면 프롬프트 : A, 10 years old, has long hair and green eyes and B, 32 years old, has short hair and red eyes has met before...\n이해됐어?"
            },
            {
            "role": "assistant",
            "content": "인물 프롬프트를 제공해주세요."
            },
            {
            "role": "user",
            "content": character_prompts
            },
            {
            "role": "assistant",
            "content": "장면 프롬프트를 제공해주세요."
            },
            {
            "role": "user",
            "content": original_prompt
            },
            {
            "role": "assistant",
            "content": "수정 내용에 대해 제공해주세요."
            },
            {
                "role": "user",
                "content": modification
            },
        ]
    response, usage = get_response(messages)
    edited_prompt = response['content']
    if (edited_prompt[0] == "\"" and edited_prompt[-1] == "\"" ) or (edited_prompt[0] == "\'" and edited_prompt[-1] == "\'" ):
        edited_prompt = edited_prompt[1:-1]

    img_url = dalle(edited_prompt)
    img = url_to_image(img_url)
    cv2.imwrite(f'{filename}',img)

    return edited_prompt, usage


def match_voice_actor(subtitles:list, character_prompts:dict):
    # 순서
    # 1. 웹 소설 속 등장하는 등장인물과 성우를 매칭 (등장인물의 특징을 반영)
    # 2. 각 나레이션별로 적절한 등장인물 매칭 (나레이션의 문맥과 특징을 통해 등장인물 매칭)
    # 3. 등장인물을 기반으로 나레이션과 성우 매칭
    script = ""
    for s in subtitles:
        for t in s:
            script = f"{script}- 대사 : {t}\n"

    characters = ""
    for k,v in character_prompts.items():
        characters = f"{characters}- {k} : {v}\n"

    usage = {
        "completion_tokens": 0,
        "prompt_tokens": 0,
        "total_tokens": 0
    }

    msg1 = [
        {
          "role": "system",
          "content": "대사의 성우를 지정하는 작업을 진행하고자 해.\n\n다음의 주의 사항을 지켜줘\n\n- 2번과 3번 작업에서는 다른 대답 없이 출력 예시에 맞게만 대답 해줘.\n\n- 2번 작업에서 각 인물들은 서로 다른 성우를 배정해줘.\n\n1. 너에게 8명의 성우에 대해서 성별, 특성, 분위기와 같은 정보를 제공할 거야 . 이 정보를 다음 작업에 활용해줘.\n\n2. 소설에 등장하는 등장인물을 제공할 거야. 이때 각 등장인물에 맞는 성우를 매칭해줘. 나레이션에 대한 성우도 매칭해줘.\n\n출력 예시 : \n- 인물 이름 : 성우 이름\n- 인물 이름 : ...\n- 나레이션 : 성우 이름\n\n이해했어?"
        },
        {
          "role": "assistant",
          "content": "네, 이해했습니다!"
        },
        {
          "role": "user",
          "content": "성우 목록:\n\n1. nyejin : 여성, 청년, 새침, 열정적, 밝은 나레이션에 적합\n\n2. nmovie : 남성, 청년, 진중함, 진지한 나레이션에 적합\n\n3. nhajun : 남성, 어린이, 친근한, 호기심 많은, 활기\n\n4. ndain : 여성, 어린이, 사랑스러운, 호기심 많은, 활기찬\n\n5. ndaeseong : 남성, 청년, 로맨틱한 배우, 저음\n\n6. nian : 남성, 청년, 친근한 오빠,  열정적인,풍부한, 활기찬\n\n7. nnarae : 여성, 청년,  털털한, 친근한 ,싹싹한, 열정적인, 차분한\n\n8. nara : 여성, 청년, 사랑스러운, 차분한, 친절한, 활기찬\n"
        },
        {
          "role": "assistant",
          "content": "다음으로 등장인물 정보를 제공해주세요."
        },
        {
          "role": "user",
          "content": characters
        }
    ]

    msg2 = [
        {
          "role": "system",
          "content": "대사의 성우를 지정하는 작업을 진행하고자 해.\n\n다음의 주의 사항을 지켜줘\n\n- 다른 대답 없이 출력 예시에 맞게만 대답 해줘.\n\n1. 인물의 정보를 먼저 제공할 거야.\n\n2. 대사를 제공할테니 모든 대사에 맞는 인물 혹은 나레이션을 적절하게 한명씩 매칭해줘.\n\n한 대사도 빠짐 없이 매칭해줘.\n\n출력 예시:\n# 대사 : 대사 내용\n- 이름\n\n이해했어?"
        },
        {
          "role": "assistant",
          "content": "네, 알겠습니다. 계속 진행해주세요."
        },
        {
          "role": "user",
          "content": characters
        },
        {
          "role": "assistant",
          "content": "대사를 제공해주세요"
        },
        {
          "role": "user",
          "content": script
        }
    ]

    voice_actor, task_usage = get_response(msg1)
    usage = sum_usage(usage,task_usage)
    script_char, task_usage = get_response(msg2)
    usage = sum_usage(usage,task_usage)

    pair = {}
    ret = []
    
    for l in voice_actor['content'].split('\n'):
        key_value = l.split(":")
        if len(key_value[0])>0 and key_value[0][0]=='-':
            key_value[0] = key_value[0][1:]
            key_value[0] = key_value[0].replace(" ","")
            key_value[1] = key_value[1].replace(" ","")
            pair[key_value[0]] = key_value[1]

    for script in script_char['content'].split('#'):
        for l in script.split('\n'):
          if len(l)>0 and l[0] == "-":
              l = l[1:]
              l = l.replace(" ","")
              ret.append(pair[l])
    
    return ret, usage


def sum_usage(usage1:dict,usage2:dict):
    # API 사용량 합
    for k,v in usage2.items():
        usage1[k] = usage1[k]+v
    return usage1

def get_response(message:str = None):   
    # Text를 입력으로 하여 결과 값, 사용량 리턴 
    response = client.chat.completions.create(
        model=model,
        messages= message,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=0,
        presence_penalty=0
    )
        
    ret = {
        "role" : response.dict()['choices'][0]['message']["role"],
        "content" : response.dict()['choices'][0]['message']["content"]
    }
    return ret, response.dict()['usage']

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_vision_response(image_path,char_input):
    # 등장인물의 사진이 주어지는 경우에 이미지를 반영한 특징 추출
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model":"gpt-4-vision-preview",
        "messages":[
            {
                "role": "user",
                "content": [{"type": "text", "text": "너에게 인물의 정보와 인물의 이미지를 제공할 거야. 제공된 정보와 인물 이미지를 기반으로 해당 인물의 피부, 머리 색, 머리 스타일, 눈 ,코, 입 등의 외모 특징을 담은 '영어 프롬프트'를 생성해줘.\n\n이미지 속 인물의 특징만 알려주면 돼.\n\n출력 예시에 맞는 대답만 해줘.\n\n출력 예시 : \n# 인물이름 :\n- 프롬프트 : A....., long hair, green eyes..."}]
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": "알겠습니다. 인물에 대한 정보와 이미지를 제공해 주세요. 그럼 제가 해당 정보를 바탕으로 인물의 특징을 담은 영어 프롬프트를 만들어 드리겠습니다."}]
            },

            {
                "role": "user",
                "content": [
                    {"type": "text", "text": char_input},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        "max_tokens":1024,
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json()
        
    return response['choices'][0]['message'], response['usage']
    

def parse_character_prompt(content:str):
    # GPT의 결과에서 캐릭터 프롬프트 추출
    for line in content.split('\n'):
        if len(line)>0 and line[0] == '-':
            ret = line.split(':')[-1]
            if (ret[0] == ' '):
                ret = ret[1:]
            if (ret[0] == '\"' and ret[-1] == '\"'):
                ret = ret[1:-1]
            if (ret[0] == '\'' and ret[-1] == '\''):
                ret = ret[1:-1]
            return ret
        
def parse_data(content:str, sep='---'):
    # GPT의 결과에서 원하는 내용 추출
    ret = []
    if (content.find(sep)== -1 ):
        sep = "\n\n"
    for i,scene in enumerate(content.split(sep)):
        ret.append([])
        for line in scene.split('\n'):
            if len(line) > 0 and line[0] == '-':
                line = line.split(':')[-1]
                if line[0] == ' ':
                    line = line[1:]
                if (line[0] == '\"' and line[-1] == '\"'):
                    line = line[1:-1]
                if (line[0] == '\'' and line[-1] == '\''):
                    line = line[1:-1]
                ret[i].append(line)

    return ret

def input_process(user_inputs:dict):
    # 웹 소설 정보 전처리
    ret = []

    ret.append("")
    for k,v in user_inputs["novel"].items():
        ret[0] = ret[0] + f"{k}:{v}\n"

    ret.append([])
    for i,char in enumerate(user_inputs["characters"]):
        ret[1].append("")
        for k,v in char.items():
            if k!= "img":
                ret[1][i] = ret[1][i] + f"{k}:{v}\n"
    return ret

    