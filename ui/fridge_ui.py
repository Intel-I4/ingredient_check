from database import fridge_db
from database import ingredient_db, recipe_ingredient_db, recipe_db


######## 레시피 다이렉션을 위한 변수들 ########
recipe_lst = ["김치찌개", "오므라이스", "제육"]
sugestion_lst = [0, 1, 2]
recipe_direct = 0
themeColor = "#f6ddd9"

'''
냉장고 속의 재료 출력
'''
def fridge_list(win, tk, ttk):
    ##### label #####
    fredge_label = tk.Label(
        win,
        text="냉장고 재료",
        bg=themeColor,
        font=("Helvetica", 14)
    )

    ##### table #####
    fridge_db.db_file = "./database/ingredients.db"
    fridge_df = fridge_db.read_ingredients_table()

    # Create a Treeview widget
    tree = ttk.Treeview(win)

    vsb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    vsb.place(x=590, y=114, height=200+21)
    style = ttk.Style()
    style.configure("Treeview.Heading", background=themeColor)

    # Define the columns
    tree["columns"] = list(fridge_df.columns)
    tree["show"] = "headings"  # Hide the first empty column

    # Define the column headings
    for column in fridge_df.columns:
        tree.heading(column, text=column)
        tree.column(column, anchor='center')

    # Insert the data into the Treeview
    for index, row in fridge_df.iterrows():
        tree.insert("", "end", values=list(row))


    ##### separator #####
    separator = ttk.Separator(win, orient='horizontal')


    ### packing ###
    fredge_label.pack(fill=tk.BOTH, ipady=900*0.05)
    tree.pack(ipadx=900*0.55, padx=40)
    separator.pack(fill=tk.X, pady=60, padx=40)


'''
TODO: 추천 레시피 순서를 sugestion_lst에 삽입
'''
def recipe_sort():
    global sugestion_lst
    
    fridge_db.db_file = "./database/ingredients.db"
    recipe_db.db_file = "./database/recipes.db"
    ingredient_db.db_file = "./database/recipes.db"
    recipe_ingredient_db.db_file = "./database/recipes.db"

    fred = fridge_db.read_ingredients_table() 
    omlet = recipe_ingredient_db.read_reci_2_ingred_table('오므라이스')["ingredient_name"]
    kimchi = recipe_ingredient_db.read_reci_2_ingred_table('김치찌개')["ingredient_name"]
    jeyuk = recipe_ingredient_db.read_reci_2_ingred_table('제육볶음')["ingredient_name"]

    omlet_cnt, kimchi_cnt, jeyuk_cnt = 0, 0, 0

    for oml in omlet:
        for fre in fred["name"]:
            if oml == fre:
                omlet_cnt += 1
                break

    for kim in kimchi:
        for fre in fred["name"]:
            if kim == fre:
                kimchi_cnt += 1
                break

    for je in jeyuk:
        for fre in fred["name"]:
            if je == fre:
                jeyuk_cnt += 1
                break

    omlet_cnt /= omlet.shape[0]
    kimchi_cnt /= kimchi.shape[0]
    jeyuk_cnt /= jeyuk.shape[0]

    # recipe_lst = ["김치찌개", "오므라이스", "제육"]
    # sugestion_lst = [0, 1, 2]
    
    if jeyuk_cnt >= kimchi_cnt and jeyuk_cnt >= omlet_cnt:
        if kimchi_cnt >= omlet_cnt:
            sugestion_lst = [2, 0, 1]
        else:
            sugestion_lst = [2, 1, 0]
    elif omlet_cnt >= kimchi_cnt and omlet_cnt >= jeyuk_cnt:
        if kimchi_cnt >= jeyuk_cnt:
            sugestion_lst = [1, 0, 2]
        else:
            sugestion_lst = [1, 2, 0]
    else:
        if jeyuk_cnt >= omlet_cnt:
            sugestion_lst = [0, 2, 1]
        else:
            sugestion_lst = [0, 1, 2]
            
    print("omlet_cnt", omlet_cnt)
    print("kimchi_cnt", kimchi_cnt)
    print("jeyuk_cnt", jeyuk_cnt)


'''
추천 레시피 순서로 버튼 순서 변경
'''
def recipe_button(win, tk, btn_callback):
    ##### label #####
    suggest_label = tk.Label(
        win, 
        text="추천 레시피",
        bg=themeColor,
        font=("Helvetica", 15)
    )

    ##### button #####
    button1 = tk.Button(
        win,
        text=recipe_lst[sugestion_lst[0]],
        command=btn_callback
    )
    button2 = tk.Button(
        win,
        text=recipe_lst[sugestion_lst[1]],
        command=btn_callback
    )
    button3 = tk.Button(
        win,
        text=recipe_lst[sugestion_lst[2]],
        command=btn_callback
    )
    
    ##### label #####
    empty_label = tk.Label(
        win
    )

    suggest_label.pack(fill=tk.BOTH, ipady=900*0.05)
    button1.pack(side=tk.LEFT, expand=True, ipady=900*0.01)
    button2.pack(side=tk.LEFT, expand=True, ipady=900*0.01)
    button3.pack(side=tk.LEFT, expand=True, ipady=900*0.01)
    empty_label.pack(fill=tk.BOTH, ipady=900*0.05)
