from typing import Optional
from global_coordinates import Coordinates
import cv2
from detector import detect_frame
from utils import create_network, draw_bounding_box


class ObjectPassport:

    def __init__(
            self,
            identifier,
            class_name,
            x: Optional[float] = 0,
            y: Optional[float] = 0,
            z: Optional[float] = 0,
    ) -> None:
        self.identifier = identifier
        self.class_name = class_name
        self.x = x
        self.y = y
        self.z = z


def passport_road_infrastructure(
    stereo_camera_video,
    coordinates: Coordinates,
    frame_rate,
    cameras_distance,
    cameras_focal_length,
    cameras_field_view,
) -> list[ObjectPassport]:
    utils = create_network(
        class_names_path='./model/classes.txt',
        cfg_path='./model/yolov5s.yaml',
        weights_path='./model/weights.pt',
    )

    video1 = cv2.VideoCapture(stereo_camera_video)
    passports: list[ObjectPassport] = []
    utils = create_network(
        class_names_path='./model/classes.txt',
        weights_path='./model/weights.pt',
    )

    while stereo_camera_video.isOpened():
        ok, frame = video1.read()

        left_frame = frame[0, ::2]
        right_frame = frame[0, 1::2]
        tracking_layer = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        tracking_layer = tracking_layer.transpose((2, 0, 1))

        if ok:
            predictions = detect_frame(utils['model'], left_frame)
            for prediction in predictions:

                identifier = 0
                identifiers = []  # tracking ids
                if identifier not in identifiers:
                    object_coordinates = get_object_position()
                    passports.append(ObjectPassport(
                        identifier=identifier,
                        class_name=object_coordinates,
                        latitude=object_coordinates.latitude,
                        longitude=object_coordinates.longitude,
                        elevation=object_coordinates.elevation,
                    ))
                    identifiers.append(identifier)


    return passports


