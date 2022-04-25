# python take_video.py --cam_id 1 --width 752 --height 480 --path ./camera_video.avi

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

    print(cam.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter(
        args.path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        cam.get(cv2.CAP_PROP_FPS),
        (int(width * 2), int(height)),
        isColor=False,
    )

    while cam.isOpened():
        ok, frame = cam.read()

        left_data = frame[0, ::2]
        right_data = frame[0, 1::2]
        left_frame = np.reshape(left_data, (height, width))
        right_frame = np.reshape(right_data, (height, width))
        finally_frame = np.hstack([left_frame, right_frame])

        if ok:
            cv2.imshow("Video", finally_frame)
            out.write(finally_frame)
        else:
            raise Exception('something went wrong')

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cam.release()
    out.release()
    cv2.destroyAllWindows()
    print("success")


main()
