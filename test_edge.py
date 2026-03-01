# Quick test edge node
import os
os.makedirs("F:/drawing_3d/data", exist_ok=True)

from edge_node import EdgeNode

print("Testing Edge Node...")
edge = EdgeNode(camera_url=0, log_file="F:/drawing_3d/data/edge_logs.jsonl")
result = edge.run_edge_loop(max_frames=10)
print(f"\nResult: {result}")
