# python take_shot.py --cam_id 1 --path ./shot.jpg

import cv2
import numpy as np
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cam_id", type=int, help='camera id')
    parser.add_argument("--path", type=str, help='saving path')

    return parser.parse_args()


def main():
    args = parse_args()

    cam = cv2.VideoCapture(args.cam_id)
    width = int(cam.get(3))
    height = int(cam.get(4))
    cam.set(cv2.CAP_PROP_CONVERT_RGB, 0)

    ok, frame = cam.read()

    left_data = frame[0, ::2]
    right_data = frame[0, 1::2]
    left_frame = np.reshape(left_data, (height, width))
    right_frame = np.reshape(right_data, (height, width))

    if ok:
        cv2.imwrite(args.path, np.hstack([left_frame, right_frame]))
        print("success")
    else:
        raise Exception('something went wrong')

    cam.release()
    cv2.destroyAllWindows()


main()
