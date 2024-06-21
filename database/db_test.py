import fridge_db
import logging as log
import pandas as pd
import time 
import os


# 여기서부터 예제 전까지는 DB 셋팅을 위한 기본 값
db_file = "./database/ingredients.db"

if __name__ == "__main__":
    fridge_db.db_file = db_file

    if os.path.isfile(db_file):
        log.info("DB ready")
    else:
        log.info("DB not exist")
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        open(db_file, 'w').close()
        log.info("DB ready")

    fridge_db.create_ingredients_table()
    db_df = fridge_db.read_ingredients_table()


    # 당근의 수를 5개 늘려주는 함수
    # (DB에 이미 당근이 있었다면 여러 개로 나타날 수 있음)
    list = ["onion", 5]
    db_df = fridge_db.insert_oneline(list)
    print(db_df)


    # 데이터를 수정할 때, 예제 함수
    # 저장되어 있는 당근의 수를 1로 변경
    # db_df.loc[db_df["name"] == "onion", 'num'] = 1
    # db_df = fridge_db.rewrite_table(db_df)
    # print(db_df)
