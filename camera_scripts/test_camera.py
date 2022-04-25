# python test_camera.py --cam_id 1 --split True

import cv2
import numpy as np
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cam_id", type=int, help='camera id')
    parser.add_argument("--split", type=bool, help='split on two window')

    return parser.parse_args()


def main():
    args = parse_args()

    cam = cv2.VideoCapture(args.cam_id)
    width = int(cam.get(3))
    height = int(cam.get(4))
    cam.set(cv2.CAP_PROP_CONVERT_RGB, 0)

    while cam.isOpened():
        ok, frame = cam.read()

        left_data = frame[0, ::2]
        right_data = frame[0, 1::2]
        left_frame = np.reshape(left_data, (height, width))
        right_frame = np.reshape(right_data, (height, width))
        finally_frame = np.hstack([left_frame, right_frame])

        if ok:
            if args.split:
                cv2.imshow("Left camera", left_frame)
                cv2.imshow("Right camera", right_frame)
            else:
                cv2.imshow("Camera", finally_frame)
        else:
            raise Exception('something went wrong')

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


main()
