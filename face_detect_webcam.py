import cv2
import numpy as np



def main():
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FPS, 5)
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    if not capture.isOpened():
        exit()

    # モデルを読み込む
    face_detector = cv2.FaceDetectorYN_create("yunet_n_320_320.onnx", "", (0, 0))

    while True:
        result, img = capture.read()
        if result is False:
            cv2.waitKey(0)
            break

        height, width, _ = img.shape
        face_detector.setInputSize((width, height))

        _, faces = face_detector.detect(img)
        faces = faces if faces is not None else []
        
        for face in faces:
            box = list(map(int, face[:4]))
            color = (0, 0, 255)
            thickness = 2
            cv2.rectangle(img, box, color, thickness, cv2.LINE_AA)
            
            confidence = "{:.2f}". format(face[-1])
            position = (box[0], box[1] - 10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 0.5
            thickness = 2
            cv2. putText(img, confidence, position, font, scale, color, thickness, cv2.LINE_AA)

        cv2.imshow('Image Authenticator', img)
        key = cv2.waitKey(1)
        if key == 27:
            break
        
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

