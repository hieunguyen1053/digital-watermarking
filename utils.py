import cv2
import numpy as np

if __name__ == "__main__":
    img = cv2.imread("./images/watermark.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = img.shape[:2]
    for xi in range(0, w):
        for xj in range(0, h):
            img[xi, xj] = 255 if img[xi, xj] > np.mean(img) else 0
    cv2.imwrite("./images/watermark.jpg", img)
