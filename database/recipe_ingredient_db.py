import sqlite3
import pandas as pd
import logging as log

import recipe_db, ingredient_db

db_file = "recipes.db"


# 테이블이 없다면 생성 해주는 함수 
def create_reci_ingred_table():
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    # 레시피에 포함된 재료 테이블 생성
    cur.execute('''
    CREATE TABLE IF NOT EXISTS recipe_ingredients (
        recipe_id INTEGER NOT NULL,
        ingredient_id INTEGER NOT NULL,
        quantity TEXT,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
        PRIMARY KEY (recipe_id, ingredient_id)
    )
    ''')

    con.commit()
    con.close()


def insert_reci_ingred_ingredient(lst):
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    set_lst = [recipe_db.recipeName_2_recipeID(lst[0]), ingredient_db.ingredName_2_ingredID(lst[1]), lst[2]]

    # recipe_id와 ingredient_id의 조합이 이미 존재하는지 확인
    cur.execute('''SELECT * FROM recipe_ingredients WHERE recipe_id = ? AND ingredient_id = ?''', 
                (set_lst[0], set_lst[1],))
    existing_row = cur.fetchone()

    if existing_row:
        # 이미 존재하면 quantity와 unit을 업데이트
        cur.execute('''UPDATE recipe_ingredients 
                    SET quantity = ? WHERE recipe_id = ? AND ingredient_id = ?''', 
                    (set_lst[2], set_lst[0], set_lst[1],))
    else:
        # 존재하지 않으면 삽입
        cur.execute('''INSERT INTO recipe_ingredients 
                    (recipe_id, ingredient_id, quantity) VALUES (?, ?, ?)''', 
                    (set_lst[0], set_lst[1], set_lst[2]))

    # 모든 레시피와 재료를 조회하는 read_recipe_query 호출
    df = read_reci_ingred_query(cur)

    # 데이터베이스 변경 사항 커밋 및 연결 종료
    con.commit()
    con.close()

    return df


# 테이블 전체의 내용을 읽어오는 함수 중 쿼리문의 내용만을 담은 함수 
def read_reci_ingred_query(cur):
    query = 'SELECT * FROM recipe_ingredients'
    cur.execute(query)

    rows = cur.fetchall()  # Fetch all rows from the executed query

    # Create a DataFrame directly from the fetched rows
    df = pd.DataFrame(rows, columns=["recipe_id", "ingredient_id", "quantity"])

    return df


# 입력받은 레시피의 재료 정보를 돌려주는 함수
def read_reci_2_ingred_table(name):
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    recipe_id = recipe_db.read_recipes_table()
    cur.execute('''
    SELECT r.name as recipe_name, i.name as ingredient_name, ri.quantity, ri.unit
    FROM recipe_ingredients ri
    JOIN recipes r ON ri.recipe_id = r.id
    JOIN ingredients i ON ri.ingredient_id = i.id
    WHERE r.id = ?
    ''', (recipe_id,))

    rows = cur.fetchall()  # Fetch all rows from the executed query

    # Create a DataFrame directly from the fetched rows
    df = pd.DataFrame(rows, columns=['recipe_name', 'ingredient_name', 'quantity', 'unit'])
    print(df)

    con.close()
    return df


# 테이블 전체의 내용을 읽어오는 함수
def read_reci_ingred_table():
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    query = 'SELECT * FROM recipe_ingredients'
    cur.execute(query)

    rows = cur.fetchall()  # Fetch all rows from the executed query

    # Create a DataFrame directly from the fetched rows
    df = pd.DataFrame(rows, columns=["recipe_id", "ingredient_id", "quantity"])

    con.close()
    return df


# 레시피 이름을 입력 받아 재료들의 이름을 돌려주는 함수
def find_ingred(name):
    ingredList = []

    recipeID = recipe_db.recipeName_2_recipeID(name)
    df = read_reci_ingred_table()
    ingredIDs = df.loc[df["recipe_id"] == recipeID, "ingredient_id"]

    for id in ingredIDs:
        ingredList.append(ingredient_db.ingredID_2_ingredName(id))

    return ingredList


# 레시피 이름을 입력 받아 재료들의 이름을 돌려주는 함수
def find_ingred(name):
    ingredList = []

    recipeID = recipe_db.recipeName_2_recipeID(name)
    df = read_reci_ingred_table()
    ingredIDs = df.loc[df["recipe_id"] == recipeID, "ingredient_id"]

    for id in ingredIDs:
        ingredList.append(ingredient_db.ingredID_2_ingredName(id))

    return ingredList
