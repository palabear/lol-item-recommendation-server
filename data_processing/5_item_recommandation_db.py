import pandas as pd
import numpy as np
import xgboost
import tqdm
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import explained_variance_score
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from sqlalchemy import create_engine
pd.set_option('mode.chained_assignment',  None) # 경고 off
df = pd.read_csv("game_data.csv")

cnt = 0
for i in df.Champ_ID.unique():
    for j in df.vs.unique():
        if i == j :#챔피언이 같을때
            continue
        print("ij",i,j)
        mask = (df.Champ_ID == i) & (df.vs == j)
        df_sub = df[mask]
        if len(df_sub) < 10 :# 경기데이터가 너무적을때
            continue

        cnt += 1
        #del mask
        dff = df_sub
        #del df_sub
        dfff = dff[['item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6']]
        temp_arr = np.array([])
        for k in dfff.columns:
            temp_arr = np.append(temp_arr, dfff[k])
        temp_arr = temp_arr.tolist()

        new_col = np.unique(temp_arr)

        dff["win"] = dff["win"].astype(int)
        dff = dff.reset_index(drop=True)
        data_set = pd.DataFrame(columns=new_col)  # sparse matrix 로 변환
        for k in range(dff.shape[0]):
            for l in dfff.columns.tolist():
                data_set.loc[k, dff.iloc[k][l]] = 1
        data_set = data_set.fillna(0)
        data_set['win'] = dff['win']
        match_data = data_set.drop([0], axis=1,errors='ignore')
        my_champ = dff['Champ_ID'][0]
        vs_champ = dff['vs'][0]

        if len(match_data) < 10 :
            continue
        X_train, X_test, y_train, y_test = train_test_split(match_data.iloc[:, 0:(len(match_data.columns) - 1)],
                                                            match_data.iloc[:, len(match_data.columns) - 1],
                                                            test_size=0.2)  # , 승패 여부



        xgb_model = xgboost.XGBRegressor(n_estimators=10, learning_rate=0.06, gamma=0, subsample=0.5,
                                         colsample_bytree=1, max_depth=4)
        xgb_model.fit(X_train, y_train)

        recommand_dict = dict(
            sorted(xgb_model.get_booster().get_score(importance_type='weight').items(), key=lambda item: item[1],
                   reverse=True))
        recommand_craft_item = []
        recommand_value_item = []
        for key, value in recommand_dict.items():
            if float(key) < 2000:
                if len(recommand_craft_item) < 3:
                    recommand_craft_item.append(key)
            elif float(key) > 3000:
                if len(recommand_value_item) < 3:
                    recommand_value_item.append(key)
        while len(recommand_value_item) < 3:
            recommand_value_item.append(0)
        while len(recommand_craft_item) < 3:
            recommand_craft_item.append(0)

        USER = "root"
        PW = "1q2w3e4r!"
        URL = "127.0.0.1"
        PORT = "3306"
        DB = "lol_item"
        engine = create_engine(
            "mysql+pymysql://root:1q2w3e4r!@127.0.0.1:3306/lol_item")  #DB연결

        query = "INSERT INTO `lol_item`.`item_recommand`(`my_champ`,`vs_champ`,`recommand_craft_1`,`recommand_craft_2`,`recommand_craft_3`,`recommand_value_1`,`recommand_value_2`,`recommand_value_3`)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        my_data = (
        my_champ, vs_champ,recommand_craft_item[0], recommand_craft_item[1], recommand_craft_item[2],
        recommand_value_item[0], recommand_value_item[1], recommand_value_item[2])
        id = engine.execute(query, my_data) # DB저장


