import tkinter as tk
from PIL import Image, ImageTk

from ui import fridge_ui
from database import recipe_db


themeColor = "#f6ddd9"


def load_image(img_path):
    try:
        # 이미지 로드 및 리사이징
        image = Image.open(img_path)
        image = image.resize((300, 300), Image.LANCZOS)
        img = ImageTk.PhotoImage(image)
        return img
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


def recipe_frame(win, h, w, num, next_fun, prev_fun):
    recipe_frame = []
    count = 0

    # db recipe call
    recipe_db.db_file = "./database/recipes.db"
    recipe_str = recipe_db.read_steps_recipe(fridge_ui.recipe_lst
                                             [fridge_ui.sugestion_lst[num]])
    recipe_lst = recipe_str.split("\n")


    # 레시피 리스트에 있는 레시피의 내용을 각 frame 별로 분할
    for recip in recipe_lst:
        # 레시피 줄바꿈 처리
        recip_lst = recip.split(" ")
        recip_str = ""

        for num in range(len(recip_lst)):
            if num % 8 == 0:
                recip_str = recip_str + "\n" + recip_lst[num]
            else:
                recip_str = recip_str + " " + recip_lst[num]


        ##### ui object #####
        frame = tk.Frame(win, bg=themeColor, border=2)
        frame.place(x=0, y=0, width=w, height=h)
        step_lbl = tk.Label(frame, text=recip_str,
                            bg=themeColor, font=("Arial", 15))
        count += 1
        empty_lbl = tk.Label(frame)

        # 이미지 로드
        step_img = load_image("ui/image/step.png")
        img_lbl = tk.Label(frame, image=step_img, bg=themeColor)

        prv_btn = tk.Button(frame, text='이전', command=prev_fun)
        next_btn = tk.Button(frame, text='다음', command=next_fun)


        ##### 배치 #####
        step_lbl.pack(side=tk.TOP, expand=True, padx=20, ipady=50)
        img_lbl.pack(side=tk.TOP, expand=True, padx=20, pady=50)
        empty_lbl.pack(side=tk.TOP, expand=True, padx=20, pady=50)
        prv_btn.place(x=458, y=865)
        next_btn.place(x=523, y=865)

        ##### frame list append #####
        recipe_frame.append(frame)

    return recipe_frame
