import sqlite3
import pandas as pd
import logging as log

db_file = "ingredients.db"


# 테이블이 없다면 생성 해주는 함수 
def create_ingredients_table():
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS ingredients (name TEXT NOT NULL, num INTEGER NOT NULL);")

    con.commit()
    con.close()


# 테이블 전체를 덮어 쓰는 함수
def rewrite_table(df):
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    # Clear the existing table
    cur.execute("DELETE FROM ingredients")

    # Insert all rows from the DataFrame into the table
    for _, row in df.iterrows():
        cur.execute("INSERT INTO ingredients (name, num) VALUES (?, ?)", (row['name'], row['num']))
        
    df = read_ingredient_query(cur)

    con.commit()
    con.close()

    return df


# 테이블에 한 줄을 삽입해 주는 함수
def insert_oneline(lst):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    

    cur.execute("SELECT * FROM ingredients WHERE name = ?", (lst[0],))
    existing_row = cur.fetchone()

    if existing_row:
        cur.execute("UPDATE ingredients SET num = num + ? WHERE name = ?", (lst[1], lst[0]))
    else:
        cur.execute("INSERT INTO ingredients (name, num) VALUES (?, ?)", (lst[0], lst[1]))

    df = read_ingredient_query(cur)

    con.commit()
    con.close()
    return df


# 테이블 전체를 읽어와서 df로 돌려주는 함수
def read_ingredients_table():
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    # query = 'SELECT name, num as total_num FROM ingredients'
    query = 'SELECT name, SUM(num) as total_num FROM ingredients GROUP BY name'
    cur.execute(query)

    rows = cur.fetchall()  # Fetch all rows from the executed query

    # Create a DataFrame directly from the fetched rows
    df = pd.DataFrame(rows, columns=['name', 'num'])

    con.close()
    return df


# 테이블 전체의 내용을 읽어오는 함수 중 쿼리문의 내용만을 담은 함수 
def read_ingredient_query(cur):
    # query = 'SELECT name, num as total_num FROM ingredients'
    query = 'SELECT name, SUM(num) as num FROM ingredients GROUP BY name'
    cur.execute(query)

    rows = cur.fetchall()  # Fetch all rows from the executed query

    # Create a DataFrame directly from the fetched rows
    df = pd.DataFrame(rows, columns=['name', 'num'])

    return df
