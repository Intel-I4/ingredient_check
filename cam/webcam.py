import cv2
from PIL import Image, ImageTk


class Webcam:
    def __init__(self, label):
        self.label = label
        self.cam = None

    def start_webcam(self):
        if self.cam is None:  # Check if the webcam is already started
            self.cam = cv2.VideoCapture(0)
            if not self.cam.isOpened():
                print("Error: Could not open webcam.")
                self.cam = None
                return
            self.update_camera()

    def update_camera(self):
        if self.cam is not None and self.cam.isOpened():
            ret, frame = self.cam.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(Image.fromarray(img))
                self.label['image'] = img
                self.label.image = img  # Keep a reference to avoid garbage collection
                self.label.after(10, self.update_camera)  # Update every 10 milliseconds
            else:
                print("Error: Unable to read frame from webcam.")
        else:
            print("Error: Webcam not available or already stopped.")

    def stop_webcam(self):
        if self.cam is not None:
            self.cam.release()
            self.cam = None
            self.label['image'] = None  # Clear the image from the label
