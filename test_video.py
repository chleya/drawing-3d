# Test YOLO with video
from yolo_detector import YOLODetector

print("="*60)
print("YOLO Video Detection Test")
print("="*60)

# Create detector
detector = YOLODetector()

# Load model
print("\n[1] Loading model...")
detector.load_model()

# Process video
print("\n[2] Processing video...")
result = detector.process_video('data/test_video.mp4', max_frames=30)

print("\n[3] Results:")
print(f"  Frames processed: {result.get('frames_processed', 0)}")
print(f"  Total detections: {result.get('stats', {}).get('total_detections', 0)}")

# Count by class
if 'results' in result:
    class_counts = {}
    for frame_result in result['results']:
        for det in frame_result.get('detections', []):
            cls = det.get('class_name', 'unknown')
            class_counts[cls] = class_counts.get(cls, 0) + 1
    
    print("\n[4] Detections by class:")
    for cls, count in sorted(class_counts.items(), key=lambda x: -x[1]):
        print(f"  {cls}: {count}")

print("\n[SUCCESS] Test completed!")
