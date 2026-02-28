# Test Firecrawl with URL scraping
from firecrawl import FirecrawlApp
import os

API_KEY = "fc-2c1cdfc9ed354caeaa7182bec1e79a65"
os.environ['FIRECRAWL_API_KEY'] = API_KEY

print("Testing Firecrawl URL scraping...")

app = FirecrawlApp(api_key=API_KEY)

# Try scraping a simple page
try:
    result = app.scrape_url('https://example.com', formats=['markdown', 'text'])
    print(f"\nStatus: success")
    print(f"Title: {result.title if hasattr(result, 'title') else 'N/A'}")
    print(f"Text length: {len(result.text) if hasattr(result, 'text') else 0}")
    print(f"First 200 chars: {result.text[:200] if hasattr(result, 'text') else 'N/A'}")
except Exception as e:
    print(f"Error: {e}")

# Try search
print("\n" + "="*50)
print("Testing search...")
try:
    result = app.search("artificial intelligence", limit=3)
    print(f"Search status: success")
    print(f"Data type: {type(result.data)}")
    print(f"Data length: {len(result.data) if hasattr(result, 'data') else 0}")
    if hasattr(result, 'data') and result.data:
        for item in result.data[:3]:
            print(f"  - {str(item)[:100]}")
except Exception as e:
    print(f"Search error: {e}")

print("\n[Done]")
