for trains:
python train.py --img 640 --data road.yaml --weights yolov5x.pt --batch 16 --epochs 500

for tests:
python detect.py --source ./data/road/test/images/ --weights ../weights.pt --conf 0.49 --name road

весы:
runs/train/exp13/weights/best.pt


for export 
python export.py --weights ../weights.pt --include onnx
указать нужные весы