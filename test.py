from ultralytics import YOLO
import cv2

# Set image path
image_path = "SUN.png"

# Load model (use your custom model if trained)
model = YOLO("yolov5s.pt")

# Run detection
results = model(image_path)[0]

# Load image
img = cv2.imread(image_path)

# Draw boxes
for box in results.boxes:
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    conf = float(box.conf[0])
    cls = int(box.cls[0])
    label = f"{model.names[cls]} {conf:.2f}"

    cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
    cv2.putText(img, label, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

# Show result
cv2.imshow("Detections", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
