import requests, json
from bs4 import BeautifulSoup

def food_info(name):
    '''
    This function gives you food information for the given input.

    PARAMETERS
        - name(str): name of Korean food in Korean ex) food_info("김치찌개")
    RETURN
        - res(list): list of dict that containing info for some Korean food related to 'name'
            - res['name'](str): name of food
            - res['ingredients'](str): ingredients to make the food
            - res['recipe'](list[str]): contain recipe in order
    '''
    url = f"https://www.10000recipe.com/recipe/list.html?q={name}"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
    else:
        print("HTTP response error :", response.status_code)
        return

    food_list = soup.find_all(attrs={'class':'common_sp_link'})
    food_id = food_list[0]['href'].split('/')[-1]
    new_url = f'https://www.10000recipe.com/recipe/{food_id}'
    new_response = requests.get(new_url)
    if new_response.status_code == 200:
        html = new_response.text
        soup = BeautifulSoup(html, 'html.parser')
    else:
        print("HTTP response error :", response.status_code)
        return

    food_info = soup.find(attrs={'type':'application/ld+json'})
    result = json.loads(food_info.text)
    ingredient = ','.join(result['recipeIngredient'])
    recipe = [result['recipeInstructions'][i]['text'] for i in range(len(result['recipeInstructions']))]
    for i in range(len(recipe)):
        recipe[i] = f'{i+1}. ' + recipe[i]

    res = {
        'name': name,
        'ingredients': ingredient,
        'recipe': recipe
    }

    return res

