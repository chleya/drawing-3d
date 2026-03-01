# -*- coding: utf-8 -*-
"""
Simple browser automation using Playwright
"""

from playwright.sync_api import sync_playwright
import sys

def open_browser(url="https://example.com"):
    """Open browser and navigate to URL"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        print(f"Opened: {page.url}")
        print(f"Title: {page.title()}")
        
        # Get content
        content = page.content()
        print("\n=== Page Content (first 2000 chars) ===")
        print(content[:2000])
        
        browser.close()
        return page

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    open_browser(url)

if __name__ == "__main__":
    main()
