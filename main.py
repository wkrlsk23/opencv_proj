
import cv2
import os
from tkinter import filedialog
from tkinter import messagebox

classifier_path = "haarcascade_frontalface_default.xml"


def video_reading(file):
    cap = cv2.VideoCapture(file)
    face_cascade = cv2.CascadeClassifier(classifier_path)
    cv2.namedWindow("Video_Face", cv2.WINDOW_NORMAL)
    cv2.createTrackbar("Scale_factor", "Video_Face", 80, 200, lambda x : x)
    cv2.createTrackbar("minNeighbor", "Video_Face", 3, 6, lambda x : x)

    while True:
        sf = (cv2.getTrackbarPos("Scale_factor", "Video_Face")+100)* 0.01
        mn = cv2.getTrackbarPos("minNeighbor", "Video_Face")
        if sf == 1.0:
            sf += 0.01
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, sf, mn, minSize=[30, 30])
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, 'Detected Face', (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
        cv2.imshow('Face', frame)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    files = filedialog.askopenfilenames(initialdir=os.path.join(os.path.expanduser('~'), 'Desktop'),
                                        title="파일을 선택 해 주세요",
                                        filetypes=(("*.mp4", "*mp4"), ("*.avi", "*avi")))

    if files == '':
        messagebox.showwarning("경고", "파일을 추가 하세요")
    files = files[0].replace("/", "\\\\")
    print(files)
    video_reading(files)
