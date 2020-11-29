import cv2
import numpy as np

class Watermark:
    sig_size = 100

    @staticmethod
    def __gene_signature(wm, size):
        wm = cv2.resize(wm, (size, size))
        wm = np.where(wm < np.mean(wm), 0, 1)
        return wm

    def inner_embed(self, B, signature):
        pass

    def inner_extract(self, B):
        pass

    def embed(self, cover, wm):
        B = None
        img = None
        signature = None

        if len(cover.shape) > 2:
            img = cv2.cvtColor(cover, cv2.COLOR_BGR2YUV)
            signature = self.__gene_signature(wm, self.sig_size).flatten()
            B = img[:, :, 0]

        if len(cover.shape) > 2:
            img[:, :, 0] = self.inner_embed(B, signature)
            cover = cv2.cvtColor(img, cv2.COLOR_YUV2BGR)
        else:
            cover = B
        return cover

    def extract(self, wmimg):
        B = None
        if len(wmimg.shape) > 2:
            (B, G, R) = cv2.split(cv2.cvtColor(wmimg, cv2.COLOR_BGR2YUV))
        else:
            B = wmimg
        ext_sig = self.inner_extract(B)[0]
        ext_sig = np.array(ext_sig).reshape((self.sig_size, self.sig_size))
        ext_sig = np.where(ext_sig == 1, 255, 0)
        return ext_sig