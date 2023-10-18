
from urllib import parse
import pprint
import requests
import json
import time
import csv

import pandas as pd

# for문 진행률 확인 라이브러리
from tqdm import tqdm
pp = pprint.PrettyPrinter(indent=4)

api_key = 'RGAPI-2479968b-99cf-44dd-9022-a96248266713'
request_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-2479968b-99cf-44dd-9022-a96248266713"
}

url = 'https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key=' + api_key

summonerId = {}

r = requests.get(url)
r = r.json()['entries'] #소환사의 고유 id

num = 0
for i in r:
    summonerId[i['summonerName']] = i['summonerId']

    num += 1
print(num)
accountId = {}

for i, j in zip(tqdm(summonerId.values()), summonerId.keys()):
    url2 = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/' + i + '?api_key=' + api_key
    r = requests.get(url2)

    if r.status_code == 200:  # response가 정상이면 바로 맨 밑으로 이동하여 정상적으로 코드 실행
        pass

    elif r.status_code == 429:
        print('api cost full : infinite loop start')
        print('loop location : ', i)
        start_time = time.time()

        while True:  # 429error가 끝날 때까지 무한 루프
            if r.status_code == 429:

                print('try 10 second wait time')
                time.sleep(10)

                r = requests.get(url2)
                print(r.status_code)

            elif r.status_code == 200:  # 다시 response 200이면 loop escape
                print('total wait time : ', time.time() - start_time)
                print('recovery api cost')
                break

    r = r.json()['accountId']
    print(r)
    accountId[j] = r



print(accountId)
puuid = []
for i in tqdm(accountId.values()):
    url3 = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-account/' + i + '?&api_key=' + api_key
    r = requests.get(url3)

    if r.status_code == 200:
        pass

    elif r.status_code == 429:
        print('api cost full : infinite loop start')
        print('loop location : ', i)
        start_time = time.time()

        while True:
            if r.status_code == 429:

                print('try 10 second wait time')
                time.sleep(10)

                r = requests.get(url2)
                print(r.status_code)

            elif r.status_code == 200:
                print('total wait time : ', time.time() - start_time)
                print('recovery api cost')
                break
    try:
        r = r.json()['puuid']
        puuid.append(r)
        print("accountID: " + i)
    except:
        print(r.text)
        print('matches 오류 확인불가')
print(puuid)

gameId=[]
for i in tqdm(puuid):
    #https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/9EixO7KWNYzL1wcUyCey7Lt7S565EJbw9FX-xdmTvjPBxABj26U-ivjR3lj209x-T7BYw5NJRgAHAw/ids?start=0&count=20
    url3 = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/' + i + '/ids?type=ranked&start=0&count=20&api_key=' + api_key
    r = requests.get(url3)

    if r.status_code == 200:
        pass

    elif r.status_code == 429:
        start_time = time.time()

        while True:
            if r.status_code == 429:
                print('10 second wait time')
                time.sleep(10)

                r = requests.get(url3)
                print(r.status_code)

            elif r.status_code == 200:
                print('total wait time : ', time.time() - start_time)
                print('recovery api cost')
                break
    try:
        r = r.json()
        for j in r:
            print(j)
            gameId.append(j)
    except:
        print('game id not found')

print(gameId)

with open("gameid.csv", 'w') as file:
  writer = csv.writer(file)
  writer.writerow(gameId)
