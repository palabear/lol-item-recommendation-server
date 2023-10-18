import requests
import json
import time


import pandas as pd

# for문 진행률 확인 라이브러리
from tqdm import tqdm


api_key = 'RGAPI-c0aeb4d9-be49-4009-9b04-3d04154edb7f'
request_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-c0aeb4d9-be49-4009-9b04-3d04154edb7f"
}

game_data = pd.read_csv('clean_gameid.csv',encoding='utf-8')



for i in tqdm(game_data['game_id']):
    print(i)
    url2 = 'https://asia.api.riotgames.com/lol/match/v5/matches/'+ i + '?api_key=' + api_key
    r = requests.get(url2)

    if r.status_code == 200:
        pass

    elif r.status_code == 429:
        start_time = time.time()

        while True:
            if r.status_code == 429:
                print('10 second wait time')
                time.sleep(10)

                r = requests.get(url2)
                print(r.status_code)

            elif r.status_code == 200:
                print('total wait time : ', time.time() - start_time)
                break

    r = r.json()
    print(r)
    with open('gameinfo/game_info'+ i +'.json','w',encoding='utf-8') as file :
        json.dump(r,file)


