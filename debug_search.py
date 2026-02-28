from firecrawl import FirecrawlApp

API_KEY = "fc-2c1cdfc9ed354caeaa7182bec1e79a65"
app = FirecrawlApp(api_key=API_KEY)

print("Testing search...")
result = app.search("construction safety", limit=3)

print(f"Type: {type(result)}")
print(f"Attributes: {dir(result)}")
print(f"Data: {result.data}")
print(f"Raw: {result}")
