import cv2
import sys
import os
import time
import numpy as np
from tkinter import filedialog
from tkinter import messagebox

#글로벌 변수 작성 (video와 photo에 필요할 경우 형식을 추가)
classifier_path = "./haarcascade_frontalface_default.xml"
video = ["avi", "mp4"]
photo = ["png", "jpeg", "jpg"]
FPS = 60

#한글 경로 파일 읽기
def korean_directory_import(path):
    img_array = np.fromfile(path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

#한글 경로 파일 출력
def korean_directory_export(path,img):
    ret, img_arr = cv2.imencode(os.path.splitext(path)[1], img, cv2.IMREAD_COLOR)
    if ret :
        with open(path, mode='w+b') as f:
            img_arr.tofile(f)

def face_detecting(sf, mn, frame):
    #그림을 GrayScale로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #CascadeClassifier 불러오기
    face_cascade = cv2.CascadeClassifier(classifier_path)

    #Classifier로 얼굴 인식 실행
    faces = face_cascade.detectMultiScale(gray, sf, mn)

    #얼굴 인식 결과를 이미지에 그리기 , 그 결과를 출력
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, 'Detected Face', (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
    return frame

def photo_reading(file):
    #그림 불러오기 (한글경로로)
    photo = korean_directory_import(file)

    #얼굴 인식 부분
    photo = face_detecting(1.8, 3, photo)
    cv2.imshow('Face', photo)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def video_reading(file):
    #변수 선언
    prev_time = 0

    #비디오캡처 및 조정창 생성
    cap = cv2.VideoCapture(file)
    cv2.namedWindow("Video_Face", cv2.WINDOW_NORMAL)
    cv2.createTrackbar("Scale_factor", "Video_Face", 80, 200, lambda x : x)
    cv2.createTrackbar("minNeighbor", "Video_Face", 3, 6, lambda x : x)

    while True:
        #매 프레임 마다 트랙바 변수 불러오기
        sf = (cv2.getTrackbarPos("Scale_factor", "Video_Face")+100)* 0.01
        mn = cv2.getTrackbarPos("minNeighbor", "Video_Face")
        if sf == 1.0:
            sf += 0.01
        
        #fram 읽기 및 FPS 조정
        ret, frame = cap.read()
        current_time = time.time() - prev_time
        if (ret is True) and (current_time > 1./ FPS) :
            prev_time = time.time()

            #얼굴 인식 부분
            frame = face_detecting(sf, mn, frame)
            cv2.imshow('Face', frame)
            if cv2.waitKey(1) == 27:
                break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    
    #파일 타입 설정
    v_ftypes = ""
    p_ftypes = ""
    for t in video:
        v_ftypes = v_ftypes + "*." + t + " "
    for t in photo:
        p_ftypes = p_ftypes + "*." + t + " "

    #파일 불러오기, 파일이 없을 때 앱을 강제 종료
    files = filedialog.askopenfilenames(initialdir=os.path.join(os.path.expanduser('~'), 'Desktop'),
                                        title="파일을 선택 해 주세요",
                                        filetypes=[("video", v_ftypes),
                                                  ("photo", p_ftypes)] )
    if files == '':
        messagebox.showwarning("경고", "파일을 추가 하세요")
        sys.exit()
    
    #파일 경로 다듬기
    files = files[0].replace("/", "\\\\")
    form = files.split(".")[-1]
    
    #form은 마지막을 의미한 form에 따라서 변수가 
    if form in video :
        video_reading(files)
    elif form in photo :
        photo_reading(files)
