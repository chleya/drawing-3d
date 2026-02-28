# Test YOLO Detector
from yolo_detector import YOLODetector
import numpy as np

print("=" * 50)
print("YOLO Safety Detector Test")
print("=" * 50)

# Create detector
detector = YOLODetector()

# Load model
print("\n[1] Loading model...")
if detector.load_model():
    print("Model loaded successfully!")
    
    # Test with blank frame
    print("\n[2] Testing with blank frame...")
    test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    detections = detector.detect_frame(test_frame)
    print(f"Detections: {len(detections)} objects")
    
    # Stats
    stats = detector.get_stats()
    print(f"Stats: {stats}")
    
    print("\n[SUCCESS] YOLO is working!")
else:
    print("Failed to load model")
