import fridge_db, recipe_db, ingredient_db, recipe_ingredient_db
import logging as log
from recipe import recipe
import os


# 여기서부터 예제 전까지는 DB 셋팅을 위한 기본 값
ing_file = "./ingredients.db"
rec_file = "./recipes.db"

if __name__ == "__main__":
    fridge_db.db_file = ing_file
    recipe_db.db_file = rec_file
    ingredient_db.db_file = rec_file
    recipe_ingredient_db.db_file = rec_file

    if os.path.isfile(ing_file):
        log.info("DB ready")
    else:
        log.info("DB not exist")
        os.makedirs(os.path.dirname(ing_file), exist_ok=True)
        open(ing_file, 'w').close()
        log.info("DB ready")

    if os.path.isfile(rec_file):
        log.info("DB ready")
    else:
        log.info("DB not exist")
        os.makedirs(os.path.dirname(rec_file), exist_ok=True)
        open(rec_file, 'w').close()
        log.info("DB ready")

    fridge_db.create_ingredients_table()
    fridge_df = fridge_db.read_ingredients_table()
    print(fridge_df)

    recipe_db.create_recipes_table()
    recipe_df = recipe_db.read_recipes_table()
    print(recipe_df)


    ingredient_db.create_ingred_table()
    ingredient_df = ingredient_db.read_ingred_table()
    print(ingredient_df)

    recipe_ingredient_db.create_reci_ingred_table()
    recipe_ingredient_df = recipe_ingredient_db.read_reci_ingred_table()
    print(recipe_ingredient_df)

    # print(recipe_ingredient_db.find_ingred("오므라이스"))
