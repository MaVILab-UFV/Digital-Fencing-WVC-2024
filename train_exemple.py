from ultralytics import YOLO

model = YOLO('yolov8n.pt')

results = model.train(data='smartClass_exemple.yaml', epochs=100, imgsz=416, device=0, batch=300, pretrained=True)