import cv2
img = cv2.imread("Abdul Kalam.png")
cascade = cv2.CascadeClassifier("haarcascade_frontalcatface.xml")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)