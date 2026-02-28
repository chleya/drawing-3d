from firecrawl import FirecrawlApp

API_KEY = "fc-2c1cdfc9ed354caeaa7182bec1e79a65"
app = FirecrawlApp(api_key=API_KEY)

print("Testing scrape...")
result = app.scrape("https://example.com")
print(f"Type: {type(result)}")
print(f"Attributes: {dir(result)}")

if result:
    print(f"\nHas markdown: {hasattr(result, 'markdown')}")
    print(f"Has text: {hasattr(result, 'text')}")
    print(f"Has html: {hasattr(result, 'html')}")
    if hasattr(result, 'markdown'):
        print(f"Markdown type: {type(result.markdown)}")
        print(f"Markdown length: {len(result.markdown) if result.markdown else 0}")
