from multi_camera_manager import MultiCameraManager
print("MultiCameraManager import OK")

# Quick test
manager = MultiCameraManager()
status = manager.get_status()
print(f"Status: {status}")
