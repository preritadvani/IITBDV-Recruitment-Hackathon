from ultralytics import YOLO
import cv2

model = YOLO("best.pt")

image = cv2.imread("image.png")
results = model(image)

heights = []
widths = []
depths = []

actual_height = 0.3
focal_length_mm = 1000

for box in results[0].boxes:
    x1, y1, x2, y2 = map(int, box.xyxy[0])

    height = y2 - y1
    width = x2 - x1

    heights.append(height)
    widths.append(width)

    depth = actual_height * focal_length_mm / height
    depths.append(depth)

    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    label = f"{depth:.2f}m"
    cv2.putText(
        image,
        label,
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

cv2.imwrite("output.png", image)

cv2.imshow("Detections", image)
cv2.waitKey(0)
cv2.destroyAllWindows()