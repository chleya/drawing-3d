from firecrawl import FirecrawlApp

a = FirecrawlApp(api_key="fc-2c1cdfc9ed354caeaa7182bec1e79a65")
methods = [m for m in dir(a) if not m.startswith('_')]
print("Available methods:")
for m in methods:
    print(f"  {m}")
