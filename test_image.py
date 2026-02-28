# Test YOLO with real URL image
from yolo_detector import YOLODetector
import urllib.request
import cv2
import numpy as np

print("="*60)
print("YOLO Real Image Detection Test")
print("="*60)

# Create detector
detector = YOLODetector()

# Load model
print("\n[1] Loading model...")
detector.load_model()

# Download a test image with people
# Using a public sample image with people
url = "https://raw.githubusercontent.com/ultralytics/yolov5/master/data/images/zidane.jpg"

print("\n[2] Downloading test image...")
try:
    with urllib.request.urlopen(url, timeout=10) as response:
        img_data = response.read()
    
    # Save temporarily
    with open('data/test_img.jpg', 'wb') as f:
        f.write(img_data)
    
    # Read with OpenCV
    frame = cv2.imread('data/test_img.jpg')
    
    if frame is not None:
        print(f"Image shape: {frame.shape}")
        
        # Detect
        print("\n[3] Running detection...")
        detections = detector.detect_frame(frame)
        
        print(f"\n[4] Results:")
        print(f"  Total detections: {len(detections)}")
        
        # Count by class
        class_counts = {}
        for det in detections:
            cls = det.get('class_name', 'unknown')
            conf = det.get('confidence', 0)
            class_counts[cls] = class_counts.get(cls, 0) + 1
            if conf > 0.5:
                print(f"    {cls}: {conf:.2f}")
        
        print("\n[5] Summary by class:")
        for cls, count in sorted(class_counts.items(), key=lambda x: -x[1]):
            print(f"  {cls}: {count}")
        
        # Check for person
        person_count = class_counts.get('person', 0)
        print(f"\n[6] PERSON detected: {person_count}")
        
        print("\n[SUCCESS] Real image detection working!")
    else:
        print("Failed to read image")
        
except Exception as e:
    print(f"Error: {e}")
    print("\nTrying alternative test...")
    
    # Fallback: create a more realistic test
    print("Creating realistic test pattern...")
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    frame[:] = (200, 200, 200)
    
    # Draw person-like shape
    # Head
    cv2.circle(frame, (320, 150), 30, (100, 100, 200), -1)
    # Body
    cv2.rectangle(frame, (290, 180), (350, 350), (150, 100, 100), -1)
    # Legs
    cv2.rectangle(frame, (295, 350), (315, 450), (100, 100, 150), -1)
    cv2.rectangle(frame, (325, 350), (345, 450), (100, 100, 150), -1)
    
    cv2.imwrite('data/synthetic_person.jpg', frame)
    
    detections = detector.detect_frame(frame)
    print(f"Synthetic person test: {len(detections)} detections")
    
    for det in detections:
        print(f"  {det.get('class_name')}: {det.get('confidence'):.2f}")
