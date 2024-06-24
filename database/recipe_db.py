import sqlite3
import pandas as pd

db_file = "recipes.db"


# 테이블이 없다면 생성 해주는 함수
def create_recipes_table():
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    # 레시피 테이블 생성
    cur.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        steps TEXT NOT NULL
    )
    ''')

    con.commit()
    con.close()


# 레시피 테이블에 한 줄을 삽입해 주는 함수
def insert_recipe(lst):
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    cur.execute('''SELECT * FROM recipes WHERE name = ?''', (lst[0],))
    existing_row = cur.fetchone()
    recipe_steps = "\n".join(lst[1])

    if existing_row:
        cur.execute('UPDATE recipes SET steps = ? WHERE name = ?', (recipe_steps, lst[0],))
    else:
        # 레시피가 존재하지 않으면 삽입
        # 리스트를 문자열로 변환하여 저장
        recipe_steps = "\n".join(lst[1])
        cur.execute('''INSERT INTO recipes (name, steps) VALUES (?, ?)''', (lst[0], recipe_steps,))    

    df = read_recipe_query(cur)

    con.commit()
    con.close()
    return df


# 레시피 테이블 전체를 읽어와서 df로 돌려주는 함수
def read_recipes_table():
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    query = 'SELECT * FROM recipes'
    cur.execute(query)

    rows = cur.fetchall()  # Fetch all rows from the executed query

    # Create a DataFrame directly from the fetched rows
    df = pd.DataFrame(rows, columns=['id', 'name', 'steps'])

    con.close()
    return df


# 테이블 전체의 내용을 읽어오는 함수 중 쿼리문의 내용만을 담은 함수
def read_recipe_query(cur):
    query = 'SELECT * FROM recipes'
    cur.execute(query)

    rows = cur.fetchall()  # Fetch all rows from the executed query

    # Create a DataFrame directly from the fetched rows
    df = pd.DataFrame(rows, columns=['id', 'name', 'steps'])

    return df


# 레시피 이름을 입력받아 id를 돌려주는 함수
def recipeName_2_recipeID(name):
    df = read_recipes_table()
    recipe_id_series = df.loc[df["name"] == name, "id"]
    if not recipe_id_series.empty:
        return recipe_id_series.iloc[0]
    else:
        return None


# 입력 받은 레시피의 만드는 'steps'만 돌려주는 함수
def read_steps_recipe(name):
    df = read_recipes_table()

    if name in df["name"].values:
        return df.loc[df["name"] == name, "steps"].iloc[0]
    else:
        return f"Recipe named '{name}' not found."
