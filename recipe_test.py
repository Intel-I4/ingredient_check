from recipe import recipe

if __name__ == "__main__":
    res = recipe.food_info("김치 찌개")

    print(res["name"])
    print(res["ingredients"])
    print(res["recipe"])
