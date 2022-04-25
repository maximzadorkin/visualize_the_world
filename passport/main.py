import argparse
import os
from global_coordinates import Coordinates
from passport import passport_road_infrastructure, ObjectPassport
from utils import write_json


def validate_args(args):
    input_stereo_video_path: bool = not os.path.isfile(args.input_stereo_video_path)
    invalid_gpx_file: bool = not os.path.isfile(args.input_gpx_file)
    if input_stereo_video_path or invalid_gpx_file:
        raise TypeError('Неверный формат входящего файла')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_stereo_video_path", type=str, help="Видео левой камеры для обработки")
    parser.add_argument("input_gpx_path", type=str, help="GPS данные")
    parser.add_argument("output_file_path", type=str, help="Файл для вывода результата в формате json")

    parser.add_argument("frame_rate", type=str, help="Кадры в секунду")
    parser.add_argument("cameras_distance", type=str, help="Расстояние между камерами")
    parser.add_argument("cameras_focal_length", type=str, help="Фокусное расстояние объективов камеры")
    parser.add_argument("cameras_field_view", type=str, help="Поле зрения камеры в горизонтальной плоскости [градусы]")

    args = parser.parse_args()
    validate_args(args)
    return args


def main():
    args = parse_args()

    gpx_file = open(args.input_gpx_path, 'r')
    coordinates = Coordinates(gpx_file)

    left_camera_video = open(args.input_left_video_path)
    right_camera_video = open(args.input_right_video_path)
    objects_passport: list[ObjectPassport] = passport_road_infrastructure(
        left_camera_video,
        right_camera_video,
        coordinates,
        frame_rate=args.frame_rate or 120, # Camera frame rate (maximum at 120 fps)
        cameras_distance=args.cameras_distance or 9,  # Distance between the cameras [cm]
        cameras_focal_length=args.cameras_focal_length or 6,  # Camera lense's focal length [mm]
        cameras_field_view=args.cameras_field_view or 56.6,  # Camera field of view in the horisontal plane [degrees]
    )

    write_json(args.output_file_path, objects_passport)


main()
