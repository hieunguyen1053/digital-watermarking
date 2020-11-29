import argparse

import cv2
import numpy as np

from attack import Attack
from dct_watermark import DCT_Watermark
from dwt_watermark import DWT_Watermark

def main(args):
    img = cv2.imread(args.origin)
    wm = cv2.imread(args.watermark, cv2.IMREAD_GRAYSCALE)

    if args.type == 'DCT':
        model = DCT_Watermark()
    elif args.type == 'DWT':
        model = DWT_Watermark()
    else:
        model = DCT_Watermark()

    if args.option == 'embedding':
        emb_img = model.embed(img, wm)
        cv2.imwrite(args.output, emb_img)
    elif args.option == 'extracting':
        signature = model.extract(img)
        cv2.imwrite(args.output, signature)

if __name__ == "__main__":
    description = '\n'.join([
        "Example:",
        "   python main.py --type DCT --option embedding --origin cover.jpg --watermark watermark.jpg --output watermarked.jpg"
    ])

    parser = argparse.ArgumentParser(prog="compare", formatter_class=argparse.RawTextHelpFormatter, description=description)
    parser.add_argument("--type", default="DCT", help="DCT or DWT or attack")
    parser.add_argument("--option", default="embedding", help="embedding or extracting")
    parser.add_argument("--origin", default="./images/cover.jpg", help="origin image file")
    parser.add_argument("--watermark", default="./images/watermark.jpg", help="watermark image file")
    parser.add_argument("--output", default="./images/watermarked.jpg", help="embedding image file")

    main(parser.parse_args())