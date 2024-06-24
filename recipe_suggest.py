import pandas as pd
import tkinter as tk
from tkinter import ttk

from database.recipe import recipe
from database import fridge_db
from ui import fridge_ui


win = tk.Tk()
win.title("Recipe Suggestion")
win.resizable(False, False)
win.configure(bg='pink')  
win_width = 640
win_height = 960
win_size_text = str(win_width) + "x" + str(win_height)
win.geometry(win_size_text)




######## UI 출력 ########
'''
냉장고 속의 재료 출력
'''
fridge_ui.fridge_list(win, tk, ttk)

'''
추천 레시피 순서를 sugestion_lst에 삽입
'''
fridge_ui.recipe_sort()
'''
추천 레시피 순서로 버튼 순서 변경
'''
fridge_ui.recipe_button(win, tk, ttk)


win.mainloop()
