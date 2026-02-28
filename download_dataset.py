# Download helmet dataset
import kagglehub

try:
    # Download helmet detection dataset
    path = kagglehub.dataset_download("andrewmvd/hard-hat-detection")
    print(f"Downloaded to: {path}")
except Exception as e:
    print(f"Error: {e}")
    
    # Try alternative
    try:
        path = kagglehub.dataset_download("tuonghoang/hard-hat-images-with-keypoints")
        print(f"Alternative downloaded to: {path}")
    except Exception as e2:
        print(f"Alternative also failed: {e2}")
