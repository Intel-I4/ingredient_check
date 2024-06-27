import sqlite3
import pandas as pd

db_file = "recipes.db"


# 재료 테이블이 없다면 생성 해주는 함수 
def create_ingred_table():
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    # 재료 테이블 생성
    cur.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    con.commit()
    con.close()


# 재료 테이블에 한 줄을 삽입해 주는 함수
def insert_ingred(lst):
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    cur.execute('''SELECT * FROM ingredients WHERE name = ?''', (lst[0],))
    existing_row = cur.fetchone()

    if existing_row:
        pass
    else:
        # 재료가 존재하지 않으면 삽입
        cur.execute('''INSERT INTO ingredients (name) VALUES (?)''', (lst[0],))

    df = read_ingred_query(cur)

    con.commit()
    con.close()
    return df


# 재료 테이블 전체를 읽어와서 df로 돌려주는 함수
def read_ingred_table():
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    query = 'SELECT * FROM ingredients'
    cur.execute(query)

    rows = cur.fetchall()  # Fetch all rows from the executed query

    # Create a DataFrame directly from the fetched rows
    df = pd.DataFrame(rows, columns=['id', 'name'])

    con.close()
    return df


# 재료 테이블 전체의 내용을 읽어오는 함수 중 쿼리문의 내용만을 담은 함수
def read_ingred_query(cur):
    query = 'SELECT * FROM ingredients'
    cur.execute(query)

    rows = cur.fetchall()  # Fetch all rows from the executed query

    # Create a DataFrame directly from the fetched rows
    df = pd.DataFrame(rows, columns=['id', 'name'])

    return df


# 재료 테이블 전체의 내용을 읽어오는 함수
def read_ingred_table():
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    query = 'SELECT * FROM ingredients'
    cur.execute(query)

    rows = cur.fetchall()  # Fetch all rows from the executed query

    # Create a DataFrame directly from the fetched rows
    df = pd.DataFrame(rows, columns=['id', 'name'])

    con.close()
    return df


# 재료 이름을 입력받아 id를 돌려주는 함수
def ingredName_2_ingredID(name):
    df = read_ingred_table()
    ingred_id = df.loc[df["name"] == name, "id"]
    return ingred_id


# 재료 id를 입력받아 이름을 돌려주는 함수
def ingredID_2_ingredName(id):
    df = read_ingred_table()
    ingred_name = df.loc[df["id"] == id, "name"]
    ingred_name = str(ingred_name).split(" ")[4].split("\n")[0]
    return ingred_name
