class Prediction:
    def __init__(
            self,
            box,
            score,
            category,
    ):
        self.box = box
        self.score = score
        self.category = category


def detect_frame(model, frame) -> list[Prediction]:
    results = model(frame)
    predictions: list[Prediction] = []
    for prediction in results.pred:
        predictions.append(Prediction(
            prediction[:, :4],
            prediction[:, 4],
            prediction[:, 5],
        ))
    return predictions
