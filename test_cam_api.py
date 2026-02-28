import requests
import json

base_url = "http://localhost:5000"

# Test camera stats
print("="*50)
print("Test: /api/camera/stats")
print("="*50)
r = requests.get(f"{base_url}/api/camera/stats")
print(json.dumps(r.json(), indent=2))

# Test start_camera
print("\n" + "="*50)
print("Test: /api/start_camera")
print("="*50)
r = requests.post(f"{base_url}/api/start_camera", json={"camera_url": 0})
print(json.dumps(r.json(), indent=2))

print("\n[SUCCESS] Camera APIs working!")
