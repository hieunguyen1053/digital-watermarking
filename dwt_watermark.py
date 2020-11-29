import math

import cv2
import numpy as np
import pywt

from attack import Attack
from watermark import Watermark


class DWT_Watermark(Watermark):
    def __init__(self):
        pass

    def __gene_embed_space(self, vec):
        shape = vec.shape
        vec = vec.flatten()
        combo_neg_idx = np.array(
            [1 if vec[i] < 0 else 0 for i in range(len(vec))])

        vec_pos = np.abs(vec)
        int_part = np.floor(vec_pos)
        frac_part = np.round(vec_pos - int_part, 2)

        bi_int_part = []
        for i in range(len(int_part)):
            bi = list(bin(int(int_part[i]))[2:])
            bie = [0] * (16 - len(bi))
            bie.extend(bi)
            bi_int_part.append(np.array(bie, dtype=np.uint16))
        bi_int_part = np.array(bi_int_part)

        sig = []
        for i in range(len(bi_int_part)):
            sig.append(bi_int_part[i][10])
        sig = np.array(sig).reshape(shape)
        return np.array(bi_int_part), frac_part.reshape(shape), combo_neg_idx.reshape(shape), sig

    def __embed_sig(self, bi_int_part, frac_part, combo_neg_idx, signature):
        shape = frac_part.shape

        frac_part = frac_part.flatten()
        combo_neg_idx = combo_neg_idx.flatten()

        m = len(signature)
        n = len(bi_int_part)

        if m >= n:
            for i in range(n):
                bi_int_part[i][10] = signature[i]
        if m < n:
            rate = n//m
            for i in range(m):
                for j in range(rate):
                    bi_int_part[i + j * m][10] = signature[i]

        em_int_part = []
        for i in range(len(bi_int_part)):
            s = '0b'
            s += (''.join([str(j) for j in bi_int_part[i]]))
            em_int_part.append(eval(s))

        em_combo = np.array(em_int_part) + np.array(frac_part)
        em_combo = np.array([-1 * em_combo[i] if combo_neg_idx[i] == 1 else em_combo[i]
                             for i in range(len(em_combo))]).reshape(shape)
        return em_combo.reshape(shape)

    def __extract_sig(self, ext_sig, siglen):
        ext_sig = list(ext_sig.flatten())

        m = len(ext_sig)
        n = siglen
        ext_sigs = []

        if n > m:
            ext_sigs.append(ext_sig + ([0] * (n-m)))

        if n <= m:
            rate = m//n
            for i in range(rate):
                ext_sigs.append(ext_sig[i * n: (i+1) * n])

        return ext_sigs

    def inner_embed(self, B, signature):
        w, h = B.shape[:2]
        LL, (HL, LH, HH) = pywt.dwt2(
            np.array(B[:32 * (w // 32), :32 * (h // 32)]), 'haar')
        LL_1, (HL_1, LH_1, HH_1) = pywt.dwt2(LL, 'haar')
        LL_2, (HL_2, LH_2, HH_2) = pywt.dwt2(LL_1, 'haar')
        LL_3, (HL_3, LH_3, HH_3) = pywt.dwt2(LL_2, 'haar')
        LL_4, (HL_4, LH_4, HH_4) = pywt.dwt2(LL_3, 'haar')
        bi_int_part, frac_part, combo_neg_idx, _ = self.__gene_embed_space(
            HH_3)
        HH_3 = self.__embed_sig(bi_int_part, frac_part,
                                combo_neg_idx, signature)

        LL_3 = pywt.idwt2((LL_4, (HL_4, LH_4, HH_4)), 'haar')
        LL_2 = pywt.idwt2((LL_3, (HL_3, LH_3, HH_3)), 'haar')
        LL_1 = pywt.idwt2((LL_2, (HL_2, LH_2, HH_2)), 'haar')
        LL = pywt.idwt2((LL_1, (HL_1, LH_1, HH_1)), 'haar')
        B[:32 * (w // 32), :32 * (h // 32)
          ] = pywt.idwt2((LL, (HL, LH, HH)), 'haar')

        return B

    def inner_extract(self, B):
        w, h = B.shape[:2]

        LL, (HL, LH, HH) = pywt.dwt2(
            B[:32 * (w // 32), :32 * (h // 32)], 'haar')
        LL_1, (HL_1, LH_1, HH_1) = pywt.dwt2(LL, 'haar')
        LL_2, (HL_2, LH_2, HH_2) = pywt.dwt2(LL_1, 'haar')
        LL_3, (HL_3, LH_3, HH_3) = pywt.dwt2(LL_2, 'haar')
        LL_4, (HL_4, LH_4, HH_4) = pywt.dwt2(LL_3, 'haar')

        _, _, _, ori_sig = self.__gene_embed_space(HH_3)
        sig = self.__extract_sig(ori_sig, self.sig_size**2)
        return sig
