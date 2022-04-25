import json
import cv2
import numpy
import yolov5
from detector import Prediction


def create_network(
    class_names_path,
    weights_path,
):
    classes = open(class_names_path).read().strip().split('\n')
    numpy.random.seed(42)
    colors = numpy.random.randint(0, 255, size=(len(classes), 3), dtype='uint8')

    # model = yolov5.load('./model/weights.pt')
    model = yolov5.load('yolov5s')
    model.conf = 0.9
    model.iou = 0.45
    model.agnostic = False
    model.multi_label = False

    return {'classes': classes, 'colors': colors, 'model': model}


def get_class_color(class_name, classes, colors) -> int:
    class_index = classes.index(class_name)
    return colors[class_index]


def draw_bounding_box(
    img,
    classes: list[str],
    colors: list[int],
    prediction: Prediction,
):
    x, y = prediction.box[:, 2]
    color = get_class_color(prediction.category, classes, colors)
    cv2.rectangle(img, prediction.box[:, 2], prediction.box[2, :], color, 2)
    cv2.putText(img, prediction.category + ' ' + prediction.score, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                color, 2)


def write_json(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)
