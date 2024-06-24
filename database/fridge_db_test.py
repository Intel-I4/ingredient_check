import sqlite3
import pandas as pd
import logging as log
import fridge_db as fred

db_file = "ingredients.db"

fred.create_ingredients_table()

fred.insert_oneline(["계란", 3])
fred.insert_oneline(["양파", 2])
fred.insert_oneline(["당근", 1])
fred.insert_oneline(["후추가루", 3])
fred.insert_oneline(["올리고당", 6])
fred.insert_oneline(["파", 4])
fred.insert_oneline(["매실액", 1])

df = fred.read_ingredients_table()
print(df)