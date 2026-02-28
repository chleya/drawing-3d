import requests
import json
import os

# Test API
base_url = "http://localhost:5000"

# Test 1: stats
print("="*50)
print("Test 1: /api/safety/stats")
print("="*50)
r = requests.get(f"{base_url}/api/safety/stats")
print(r.json())

# Test 2: image detection - use an existing test image
print("\n" + "="*50)
print("Test 2: /api/safety (image)")
print("="*50)

# Check what images we have
print("Available test files:")
for f in os.listdir('.'):
    if f.endswith(('.jpg', '.png', '.jpeg', '.mp4')):
        print(f"  - {f}")

# Try with any available image
test_images = [f for f in os.listdir('.') if f.endswith(('.jpg', '.png', '.jpeg'))]
if test_images:
    data = {"source": test_images[0], "is_video": False}
    r = requests.post(f"{base_url}/api/safety", json=data)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))
else:
    print("No test images found, using URL...")
    # Use a URL instead
    data = {"source": "https://ultralytics.com/images/zidane.jpg", "is_video": False, "is_url": True}
    r = requests.post(f"{base_url}/api/safety", json=data)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False)[:500])

# Test 3: search API (Firecrawl)
print("\n" + "="*50)
print("Test 3: /api/search")
print("="*50)
data = {"query": "construction safety", "limit": 3}
r = requests.post(f"{base_url}/api/search", json=data)
print(json.dumps(r.json(), indent=2, ensure_ascii=False))
