import cv2

# Try to open default camera
cap = cv2.VideoCapture(0)
print(f"Camera 0 opened: {cap.isOpened()}")

if not cap.isOpened():
    # Try other indices
    for i in range(1, 5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera {i} opened: True")
            break
    else:
        print("No camera found")
else:
    print("Default camera works!")
    
    # Try to read a frame
    ret, frame = cap.read()
    if ret:
        print(f"Frame read OK: {frame.shape}")
    else:
        print("Cannot read frame")
    
cap.release()
