import sqlite3
import pandas as pd
import numpy as np
from . import recipe_db, ingredient_db

db_file = "database/recipes.db"

# 테이블이 없다면 생성 해주는 함수
def create_reci_ingred_table():
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    # 레시피에 포함된 재료 테이블 생성
    cur.execute('''
    CREATE TABLE IF NOT EXISTS recipe_ingredients (
        recipe_id TEXT NOT NULL,
        ingredient_id TEXT NOT NULL,
        quantity TEXT,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
        PRIMARY KEY (recipe_id, ingredient_id)
    )
    ''')

    con.commit()
    con.close()

# lst에 [레시피 이름, 재료, 갯수]를 넣으면 테이블에 삽입해주는 함수 
def insert_reci_ingred_ingredient(lst):
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    # Get recipe_id and ingredient_id
    recipe_id = recipe_db.recipeName_2_recipeID(lst[0])
    if recipe_id is None:
        raise ValueError(f"Recipe {lst[0]} not found in the database.")

    ingredient_id = ingredient_db.ingredName_2_ingredID(lst[1])
    if ingredient_id is None:
        raise ValueError(f"Ingredient {lst[1]} not found in the database.")

    ingredient_id = np.array(ingredient_id)
    kernel = f'SELECT * FROM recipe_ingredients WHERE recipe_id = {recipe_id} AND ingredient_id = {ingredient_id[0]}'
    ingredient_id = ingredient_id[0]

    # recipe_id와 ingredient_id의 조합이 이미 존재하는지 확인
    cur.execute(kernel)
    existing_row = cur.fetchone()

    if existing_row:
        # 이미 존재하면 quantity를 업데이트
        kernel = f'UPDATE recipe_ingredients SET quantity = "{lst[2]}" WHERE recipe_id = {recipe_id} AND ingredient_id = {ingredient_id}'
        cur.execute(kernel)
    else:
        # 존재하지 않으면 삽입
        kernel = f'INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES ({recipe_id}, {ingredient_id}, "{lst[2]}")'
        cur.execute(kernel)

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

    recipe_id = recipe_db.recipeName_2_recipeID(name)

    if recipe_id is None:
        print(f"Recipe '{name}' not found in the database.")
        return pd.DataFrame(columns=['recipe_name', 'ingredient_name', 'quantity'])

    query = f'SELECT r.name as recipe_name, i.name as ingredient_name, ri.quantity \
                FROM recipe_ingredients ri \
                JOIN recipes r ON ri.recipe_id = r.id \
                JOIN ingredients i ON ri.ingredient_id = i.id \
                WHERE r.id = {recipe_id}'
    cur.execute(query)

    rows = cur.fetchall()  # Fetch all rows from the executed query
    if not rows:
        print(f"No ingredients found for recipe '{name}'.")

    # Create a DataFrame directly from the fetched rows
    df = pd.DataFrame(rows, columns=['recipe_name', 'ingredient_name', 'quantity'])

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
