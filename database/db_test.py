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
    ingredient_df = ingredient_db.read_insert_ingred_table()
    print(ingredient_df)

    recipe_ingredient_db.create_reci_ingred_table()
    recipe_ingredient_df = recipe_ingredient_db.insert_reci_ingred_ingredient([
        '오므라이스', '햄', '100g'
    ])
    recipe_ingredient_df = recipe_ingredient_db.insert_reci_ingred_ingredient([
        '오므라이스', '양파', '(대) 1/2개'
    ])
    recipe_ingredient_df = recipe_ingredient_db.insert_reci_ingred_ingredient([
        '오므라이스', '당근', '1줌'
    ])
    recipe_ingredient_df = recipe_ingredient_db.insert_reci_ingred_ingredient([
        '오므라이스', '감자', '(중) 1/2개'
    ])
    recipe_ingredient_df = recipe_ingredient_db.insert_reci_ingred_ingredient([
        '오므라이스', '파', '(잎위주) 1/2대'
    ])
    recipe_ingredient_df = recipe_ingredient_db.insert_reci_ingred_ingredient([
        '오므라이스', '밥', '2인분'
    ])
    recipe_ingredient_df = recipe_ingredient_db.insert_reci_ingred_ingredient([
        '오므라이스', '케챱', '4T'
    ])
    recipe_ingredient_df = recipe_ingredient_db.insert_reci_ingred_ingredient([
        '오므라이스', '소금', '1/2T'
    ])
    recipe_ingredient_df = recipe_ingredient_db.insert_reci_ingred_ingredient([
        '오므라이스', '후추', '약간'
    ])
    recipe_ingredient_df = recipe_ingredient_db.insert_reci_ingred_ingredient([
        '오므라이스', '계란', '4개'
    ])
    recipe_ingredient_df = recipe_ingredient_db.insert_reci_ingred_ingredient([
        '오므라이스', '돈가스소스', '6T'
    ])
    recipe_ingredient_df = recipe_ingredient_db.insert_reci_ingred_ingredient([
        '오므라이스', '올리고당', '3T'
    ])
    recipe_ingredient_df = recipe_ingredient_db.insert_reci_ingred_ingredient([
        '오므라이스', '굴소스', '1T'
    ])

    print(recipe_ingredient_db.read_reci_2_ingred_table("오므라이스"))
    # print(recipe_ingredient_db.find_ingred("오므라이스"))
