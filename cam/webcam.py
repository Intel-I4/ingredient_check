import cv2
import torch
import numpy as np
from easyocr import Reader
from ultralytics import YOLO
from torchvision import transforms
from PIL import Image, ImageDraw, ImageFont, ImageTk

from ui import fridge_ui
from database import label_change
from database import recipe_ingredient_db as ri_db


db_file = "./database/recipes.db"

color_lst = [(255, 0, 0), (255, 94, 0), (255, 228, 0), (29, 219, 22),
             (0, 216, 255), (0, 0, 255), (95, 0, 255), (250, 224, 212),
             (153, 138, 0), (0, 130, 153)]

# 나눔고딕 폰트 파일의 경로 설정
font_path = "./ocr_model/NanumGothic.ttf"

all_frame_labels = []


def draw_text(img, text, pos, font, font_size=40, font_color=(0, 255, 0)):
    pil_img = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_img)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font file not found. Using default font.")
        font = ImageFont.load_default()

    draw.text(pos, text, font=font, fill=font_color)
    return np.array(pil_img)


class Webcam:
    def __init__(self, cam_lbl, txt_lbl, ex_txt_lbl):
        self.cam_lbl = cam_lbl  # GUI에 이미지를 표시할 라벨
        self.txt_lbl = txt_lbl
        self.ex_txt_lbl = ex_txt_lbl
        self.cam = None  # 웹캠 객체 초기화
        self.model = None  # YOLO 모델 객체 초기화
        self.device = torch.device('cuda' if torch.cuda.is_available()
                                   else 'CPU')  # GPU 사용 가능 여부에 따라 장치 선택

        # 모든 프레임에서 받은 레이블을 저장할 리스트
        self.all_frame_labels = []
        self.pre_menu = []
        self.none_menu = []

    def load_model(self, model_path='best01.pt'):
        try:
            print("YOLO 모델 로드 중...")

            # YOLO 모델 로드 및 장치에 할당
            self.model = YOLO(model_path).to(self.device)

            print("YOLO 모델 로드 완료.")
            print("OCR 모델 로드 중...")

            self.ocr_reader = Reader(['ko'], gpu=True, model_storage_directory='./ocr_model/',
                    user_network_directory='./ocr_model/',
                    recog_network='custom') # ocr 모델 로드

            print("OCR 모델 로드 완료.")
        except Exception as e:
            print(f"모델 로드 오류: {e}")

    def detect_and_label_objects(self, name):
        # detected_objects = ['beef', 'carrot', 'chicken', 'chili', 'egg',
        #                     'garlic', 'kimchi', 'leek', 'onion', 'potato']

        # translated_labels = [label_change.label_ch(label) for label in name]
        translated_labels = [label_change.label_ch(name)]

        return translated_labels

    def start_webcam(self, recipe):
        sugest_recipe = fridge_ui.sugestion_lst[recipe]

        self.none_menu = ri_db.find_ingred(fridge_ui.recipe_lst[sugest_recipe])
        self.full_menu = ri_db.find_ingred(fridge_ui.recipe_lst[sugest_recipe])

        if self.cam is None:
            # 웹캠 초기화 (0은 첫 번째 웹캠을 의미)
            self.cam = cv2.VideoCapture("./20240628_155846_1.mp4")

        self.none_menu = recipe_ingredient_db.find_ingred(fridge_ui.recipe_lst[fridge_ui.sugestion_lst[recipe]])
        
        self.full_menu = recipe_ingredient_db.find_ingred(fridge_ui.recipe_lst[fridge_ui.sugestion_lst[recipe]])
        
        if self.cam is None:  
            self.cam = cv2.VideoCapture(0)  # 웹캠 초기화 (0은 첫 번째 웹캠을 의미)
            self.load_model()  # YOLO 모델 로드
            if not self.cam.isOpened():
                print("Error: 웹캠을 열 수 없습니다.")
                self.cam = None
                return
            self.update_camera()  # 카메라 업데이트 시작

    def find_common_and_different(self, ingred_list, cam_list):
        ingred_set = set(ingred_list)
        cam_set = set(cam_list)

        # 카메라에 비춰졌는데 레시피에 필요한 재료
        common_values = ingred_set.intersection(cam_set)
        # print(common_values)

        if list(common_values) == []:
            different_values = ingred_set
        else:
            different_values = (ingred_set - cam_set)
            different_values = different_values.union(cam_set - ingred_set)

        # 준비가 안된 재료들 배치 정렬 저장
        self.none_menu.clear()
        self.none_menu = different_values

        # 준비된 재료 배치 정렬 저장
        ex_ingred_list = list(set(self.full_menu) - set(self.none_menu))
        ex_ingred_list_str = ""
        for num in range(len(ex_ingred_list)):
            if num is None:
                continue
            elif num % 5 == 0:
                ex_ingred_list_str += "\n" + ex_ingred_list[num]
            else:
                ex_ingred_list_str += " " + ex_ingred_list[num]

        self.ex_txt_lbl["text"] = ex_ingred_list_str

        ingred_list = list(self.none_menu)
        ingred_str = ""

        for num in range(len(ingred_list)):
            if num is None:
                continue
            elif num % 5 == 0:
                ingred_str = ingred_str + "\n" + ingred_list[num]
            else:
                ingred_str = ingred_str + " " + ingred_list[num]

        self.txt_lbl["text"] = ingred_str

    def update_camera(self):
        global color_lst, all_frame_labels

        if self.cam is not None and self.cam.isOpened():
            ret, frame = self.cam.read()  # 프레임 읽기
            if ret:
                # 프레임을 BGR에서 RGB로 변환
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # PIL Image로 변환
                pil_image = Image.fromarray(frame_rgb)

                # 전처리 적용
                transform = transforms.Compose([
                    transforms.Resize((416, 416)),  # 이미지 크기 조정
                    transforms.ToTensor(),  # 텐서로 변환
                ])

                # 모델 입력 텐서 생성
                input_tensor = transform(pil_image)
                input_tensor = input_tensor.unsqueeze(0).to(self.device)

                # 객체 감지 수행
                with torch.no_grad():
                    detections = self.model(input_tensor)[0]  # 감지 결과 얻기

                # 감지 결과가 존재하는 경우
                if detections.boxes is not None:
                    # 바운딩 박스 데이터를 numpy 배열로 변환
                    boxes = detections.boxes.data.cpu().numpy()

                    # 감지된 레이블 리스트 초기화 (현재 프레임에 대해서만)
                    # current_frame_labels = []
                    for box in boxes:
                        self.all_frame_labels.clear()
                        # 좌표, 점수, 레이블 추출
                        x1, y1, x2, y2, score, label = box.astype(float)
                        x1 = int(x1 / 416 * 640)
                        x2 = int(x2 / 416 * 640)
                        y1 = int(y1 / 416 * 480)
                        y2 = int(y2 / 416 * 480)
                        label_name = detections.names[int(label)]  # 레이블 이름 추출

                        # 객체 감지 및 라벨 변환
                        translated_labels = self.detect_and_label_objects(label_name)

                        # 변환된 라벨을 all_frame_labels 리스트에 저장
                        self.all_frame_labels.extend(translated_labels)
                        # print(self.all_frame_labels)
                        # print(self.all_frame_labels)

                        self.find_common_and_different(self.none_menu, self.all_frame_labels)

                        # 바운딩 박스 그리기
                        cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), color_lst[int(label)], 2)
                        # 바운딩 박스 위에 레이블과 점수 표시
                        cv2.putText(frame_rgb, f'{label_name}: {score:.2f}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_lst[int(label)], 2)

                # OCR을 이용해 텍스트 인식 및 그리기
                if self.ocr_reader:
                    try:
                        result = self.ocr_reader.readtext(frame_rgb)
                        for (bbox, text, confidence) in result:
                            for word in self.full_menu:
                                if word in text:  # 텍스트가 리스트에 포함된 단어를 포함하는지 확인     
                                    txt = word
                                    # 텍스트를 준비된 재료로 처리
                                    self.find_common_and_different(self.none_menu, [txt])

                                    print(f"텍스트: {text}, 신뢰도: {confidence}, 바운딩 박스: {bbox}")

                                    # 바운딩 박스 그리기
                                    (top_left, _, bottom_right, _) = bbox
                                    top_left = tuple(map(int, top_left))
                                    bottom_right = tuple(map(int, bottom_right))

                                    cv2.rectangle(frame_rgb, top_left, bottom_right, (0, 255, 0), 2)
                                    # 텍스트와 신뢰도 표시
                                    lbl = f'{text} ({confidence:.2f})'
                                    frame_rgb = draw_text(frame_rgb, lbl,
                                                          (top_left[0],
                                                           top_left[1] - 40),
                                                          font_path, 40,
                                                          (0, 255, 0))
                    except Exception as e:
                        print(f"OCR 오류: {e}")

                # OpenCV BGR 형식으로 변환
                # annotated_frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                annotated_frame = frame_rgb

                # GUI에 표시할 ImageTk 형식으로 변환
                img = ImageTk.PhotoImage(Image.fromarray(annotated_frame))

                # 라벨 이미지 업데이트
                self.cam_lbl['image'] = img
                self.cam_lbl.image = img  # 가비지 컬렉션을 피하기 위해 참조 유지

                # 다음 업데이트 스케줄링
                self.cam_lbl.after(30, self.update_camera)

            else:
                print("Error: 웹캠에서 프레임을 읽을 수 없습니다.")
        else:
            print("Error: 웹캠을 사용할 수 없거나 이미 정지되었습니다.")

    def stop_webcam(self):
        if self.cam is not None:
            self.cam.release()  # 웹캠 자원 해제
            self.cam = None
            self.cam_lbl['image'] = None  # 라벨 이미지 초기화 (화면에서 이미지 제거)
