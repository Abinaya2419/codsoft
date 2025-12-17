import cv2
import os
import numpy as np



BASE_PATH = r"C:\Users\abina\archive"
IMAGE_NAME = "abdul kalam.png"
OUTPUT_NAME = "abdul_kalam_bigbox.png"

image_path = os.path.join(BASE_PATH, IMAGE_NAME)
output_path = os.path.join(BASE_PATH, OUTPUT_NAME)

img = cv2.imread(image_path)

if img is None:
    print(" Error loading image")
    exit()

h_img, w_img = img.shape[:2]


cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                "haarcascade_frontalface_default.xml")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = cascade.detectMultiScale(gray, scaleFactor=1.05,
                                 minNeighbors=4, minSize=(30, 30))

if len(faces) == 0:
    print(" No face detected")
    exit()

(x, y, w, h) = faces[0]


margin_factor = 1.3   

side = int(max(w, h) * margin_factor)


cx = x + w // 2
cy = y + h // 2

x1 = cx - side // 2
y1 = cy - side // 2
x2 = x1 + side
y2 = y1 + side


x1 = max(0, x1)
y1 = max(0, y1)
x2 = min(w_img - 1, x2)
y2 = min(h_img - 1, y2)

cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 4)


cv2.putText(img, "Face", (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

cv2.imshow("APJ", img)
cv2.imwrite(output_path, img)
print("Saved:", output_path)

cv2.waitKey(0)
cv2.destroyAllWindows()
