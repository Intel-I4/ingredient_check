import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from ui import fridge_ui
from cam.webcam import Webcam
from database import recipe_ingredient_db

########## 전역 변수부 ##########
page = 1
webcam = None
themeColor = "#f6ddd9"
recipe = 0

########## 함수 정의부 ##########

def next_frame(btn = 0):
    global page, webcam, recipe
    page += 1
    if page >= 4:
        page = 4
        fridge_ui.reclip_list(frame4, tk, recipe)   # recpie 값에 따라 해당 레시피 출력
        frame4.lift()
    elif page == 3:
        recipe = btn              # 레시피 버튼 값 recipe 변수에 저장
        
        if webcam is not None:
            webcam.start_webcam(recipe)  # frame3이 보일 때 웹캠 시작
            
        frame3.lift()
    elif page == 2:
        if webcam is not None:
            webcam.stop_webcam()  # frame2에서는 웹캠 정지
        frame2.lift()
    elif page == 1:
        frame1.lift()


def prev_frame():
    global page, webcam
    page -= 1
    if page <= 1:
        page = 1
        frame1.lift()
    elif page == 2:
        frame2.lift()
    elif page == 3:
        if webcam is not None:
            webcam.start_webcam(recipe)  # frame3이 보일 때 웹캠 시작
        frame3.lift()
    elif page == 4:
        frame4.lift()


def load_image():
    try:
        # 이미지 로드 및 리사이징
        image = Image.open("ui/main_page.jpeg")
        image = image.resize((300, 300), Image.LANCZOS)
        img = ImageTk.PhotoImage(image)
        return img
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


##########  main ##########

# tkinter 윈도우 생성
root = tk.Tk()
root.title("요리 프로젝트")
root.resizable(False, False)
root.configure(bg=themeColor)
win_width = 640
win_height = 960
root_size_text = str(win_width) + "x" + str(win_height)
root.geometry(root_size_text)

##### frame4 #####

frame4 = tk.Frame(root, bg=themeColor, border=2)
frame4.place(x=0, y=0, width=win_width, height=win_height)

# 버튼 frame4
but_frame4 = tk.Frame(frame4, border=10, bg=themeColor)
but_frame4.place(x=450, y=850, width=150, height=60)
tk.Button(but_frame4, text='다음', command=next_frame).pack(side=tk.RIGHT, padx=10)
tk.Button(but_frame4, text='이전', command=prev_frame).pack(side=tk.RIGHT)


##### frame3 #####

frame3 = tk.Frame(root, bg=themeColor, border=2)
frame3.place(x=0, y=0, width=640, height=960)


# 카메라 로드
cam_label = tk.Label(frame3)
cam_label.pack()


# 출력 재료 데이터 텍스트
tk.Label(frame3, font=('consolas', 20)).pack(fill='y')

# frame3 재료결과 title
title = tk.Label(frame3, text='필요한 재료',font =("Helvetica", 20), fg='red', bg='white')
title.place(x=0, y=480, width=320, height=100)
title_two = tk.Label(frame3, text='준비된 재료',font =("Helvetica", 20), fg='green', bg='white')
title_two.place(x=320, y=480, width=320, height=100)
# frame3 재료결과 title 위치, 크기조정
ingredient = tk.Label(frame3, fg='red', bg='white', font=(15))
ingredient.place(x=0, y=550, width=320, height=300)
ingredient2 = tk.Label(frame3, fg='green', bg='white', font=(15))
ingredient2.place(x=320, y=550, width=320, height=300)


# 웹캠 객체 생성
webcam = Webcam(cam_label, ingredient, ingredient2)


# 버튼 frame3
but_frame3 = tk.Frame(frame3, border=10, bg=themeColor)
but_frame3.place(x=450, y=850, width=150, height=60)

tk.Button(but_frame3, text='다음', command=next_frame).pack(side=tk.RIGHT, padx=10)
tk.Button(but_frame3, text='이전', command=prev_frame).pack(side=tk.RIGHT)


##### frame2 #####

frame2 = tk.Frame(root, bg=themeColor, border=2)
frame2.place(x=0, y=0, width=win_width, height=win_height)
# 냉장고 속의 재료 출력
fridge_ui.fridge_list(frame2, tk, ttk)
# 추천 레시피 순서를 sugestion_lst에 삽입
fridge_ui.recipe_sort()
# 추천 레시피 순서로 버튼 순서 변경
fridge_ui.recipe_button(frame2, tk, next_frame)

# 버튼 frame2
but_frame2 = tk.Frame(frame2, border=10, bg=themeColor)
but_frame2.place(x=450, y=850, width=150, height=60)


##### frame1 #####

frame1 = tk.Frame(root, bg=themeColor, border=2)
frame1.place(x=0, y=0, width=win_width, height=win_height)
tk.Label(frame1, text="요린이를 위한\n레시피 추천", bg=themeColor, 
         font=("Arial", 40,"bold")).place(x=170, y=180)

# 이미지 로드
main_img = load_image()
tk.Label(frame1, image=main_img , bg=themeColor).place(x=170, y=300)

# 버튼 frame1
but_frame1 = tk.Frame(frame1, border=10, bg=themeColor)
but_frame1.place(x=170, y=600, width=300, height=150)
tk.Button(but_frame1, text='시작하기', command=next_frame,
          width=20, height=10, bg=themeColor, font=('Helvetica', 30),
          border=10).pack(fill='x', expand=True)


root.mainloop()


