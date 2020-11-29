import cv2
import numpy as np

from attack import Attack
from watermark import Watermark


class DCT_Watermark(Watermark):
    def __init__(self):
        self.Q = 10
        self.size = 2

    def inner_embed(self, B: np.ndarray, signature):
        sig_size = self.sig_size
        size = self.size

        w, h = B.shape[:2]
        embed_pos = [(0, 0)]
        if w > 2 * sig_size * size:
            embed_pos.append((w-sig_size*size, 0))
        if h > 2 * sig_size * size:
            embed_pos.append((0, h-sig_size*size))
        if len(embed_pos) == 3:
            embed_pos.append((w-sig_size*size, h-sig_size*size))

        for x, y in embed_pos:
            for i in range(x, x+sig_size * size, size):
                for j in range(y, y+sig_size*size, size):
                    v = np.float32(B[i:i + size, j:j + size])
                    v = cv2.dct(v)
                    v[size-1, size-1] = self.Q * \
                        signature[((i-x)//size) * sig_size + (j-y)//size]
                    v = cv2.idct(v)
                    maximum = max(v.flatten())
                    minimum = min(v.flatten())
                    if maximum > 255:
                        v = v - (maximum - 255)
                    if minimum < 0:
                        v = v - minimum
                    B[i:i+size, j:j+size] = v
        return B

    def inner_extract(self, B):
        sig_size = 100
        size = self.size

        ext_sig = np.zeros(sig_size**2, dtype=np.int)

        for i in range(0, sig_size * size, size):
            for j in range(0, sig_size * size, size):
                v = cv2.dct(np.float32(B[i:i+size, j:j+size]))
                if v[size-1, size-1] > self.Q / 2:
                    ext_sig[(i//size) * sig_size + j//size] = 1
        return [ext_sig]


if __name__ == "__main__":
    img = cv2.imread("./images/cover.jpg")
    wm = cv2.imread("./images/watermark.jpg", cv2.IMREAD_GRAYSCALE)
    dct = DCT_Watermark()
    wmd = dct.embed(img, wm)
    cv2.imwrite("./images/watermarked.jpg", wmd)

    img = cv2.imread("./images/watermarked.jpg")

    img = Attack.gray(img)
    cv2.imwrite("./images/watermarked.jpg", img)

    dct = DCT_Watermark()
    signature = dct.extract(img)
    cv2.imwrite("./images/signature.jpg", signature)
