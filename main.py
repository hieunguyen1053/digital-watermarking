import argparse

import cv2
import inquirer
import numpy as np

from attack import Attack
from dct_watermark import DCT_Watermark
from dwt_watermark import DWT_Watermark


def main(args):
    img = cv2.imread(args.origin)
    wm = cv2.imread(args.watermark, cv2.IMREAD_GRAYSCALE)

    questions = [
        inquirer.List("type", message="Choice type", choices=["DCT", "DWT", "Attack"]),
    ]
    answers = inquirer.prompt(questions)
    if answers['type'] in ["DCT", "DWT"]:
        if answers['type'] == 'DCT':
            model = DCT_Watermark()
        elif answers['type'] == 'DWT':
            model = DWT_Watermark()

        questions = [
            inquirer.List("option", message="Choice option", choices=["embedding", "extracting"]),
        ]
        answers = inquirer.prompt(questions)

        if answers["option"] == "embedding":
            emb_img = model.embed(img, wm)
            cv2.imwrite(args.output, emb_img)
            print("Embedded to {}".format(args.output))
        elif answers["option"] == 'extracting':
            signature = model.extract(img)
            cv2.imwrite(args.output, signature)
            print("Extracted to {}".format(args.output))

    elif answers["type"] == "Attack":
        questions = [
            inquirer.List("action", message="Choice action", choices=[
                "blur", "rotate180", "rotate90", "chop5", "chop10", "chop30",
                "gray", "saltnoise", "randline", "cover", "brighter10", "darker10",
                "largersize", "smallersize"
            ]),
        ]
        answers = inquirer.prompt(questions)
        ACTION_MAP = {
            "blur": Attack.blur,
            "rotate180": Attack.rotate180,
            "rotate90": Attack.rotate90,
            "chop5": Attack.chop5,
            "chop10": Attack.chop10,
            "chop30": Attack.chop30,
            "gray": Attack.gray,
            "saltnoise": Attack.saltnoise,
            "randline": Attack.randline,
            "cover": Attack.cover,
            "brighter10": Attack.brighter10,
            "darker10": Attack.darker10,
            "largersize": Attack.largersize,
            "smallersize": Attack.smallersize,
        }
        att_img = ACTION_MAP[answers["action"]](img)
        cv2.imwrite(args.output, att_img)
        print("Save as {}".format(args.output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="compare", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--origin", default="./images/cover.jpg", help="origin image file")
    parser.add_argument("--watermark", default="./images/watermark.jpg", help="watermark image file")
    parser.add_argument("--output", default="./images/watermarked.jpg", help="embedding image file")
    args = parser.parse_args()
    main(parser.parse_args())