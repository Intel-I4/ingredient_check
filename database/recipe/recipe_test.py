import recipe

if __name__ == "__main__":
    res = recipe.food_info("오므라이스")

    print(res["name"])
    print(res["ingredients"])
    
    # for test in res["recipe"]:
    #     print(test)
