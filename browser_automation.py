# -*- coding: utf-8 -*-
"""
NeuralSite Browser Automation Module
基于Playwright的浏览器自动化 - 用于施工数据填报、查询等
"""

import json
from playwright.sync_api import sync_playwright
from datetime import datetime
from typing import Dict, List, Optional


class NeuralSiteBrowser:
    """NeuralSite浏览器自动化"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.page = None
        self.playwright = None
    
    def start(self):
        """启动浏览器"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        print(f"[OK] Browser started (headless={self.headless})")
        return self
    
    def open(self, url: str) -> str:
        """打开URL"""
        self.page.goto(url, wait_until="domcontentloaded")
        return self.page.url
    
    def snapshot(self) -> Dict:
        """获取页面快照"""
        # 获取可交互元素
        elements = self.page.query_selector_all("button, input, select, a, textarea")
        
        items = []
        for i, el in enumerate(elements):
            try:
                tag = el.evaluate("el => el.tagName")
                text = el.inner_text().strip()[:50] if el.inner_text() else ""
                placeholder = el.get_attribute("placeholder") or ""
                name = el.get_attribute("name") or ""
                id_ = el.get_attribute("id") or ""
                type_ = el.get_attribute("type") or ""
                
                if text or placeholder:
                    items.append({
                        "ref": f"@e{i+1}",
                        "tag": tag.lower(),
                        "text": text,
                        "placeholder": placeholder,
                        "name": name,
                        "id": id_,
                        "type": type_
                    })
            except:
                pass
        
        return {
            "url": self.page.url,
            "title": self.page.title(),
            "elements": items
        }
    
    def click(self, ref: str):
        """点击元素"""
        # 解析 ref 如 @e1
        idx = int(ref.replace("@e", "")) - 1
        elements = self.page.query_selector_all("button, input, select, a, textarea")
        
        if idx < len(elements):
            elements[idx].click()
            print(f"[OK] Clicked {ref}")
    
    def fill(self, ref: str, text: str):
        """填写表单"""
        idx = int(ref.replace("@e", "")) - 1
        elements = self.page.query_selector_all("button, input, select, a, textarea")
        
        if idx < len(elements):
            el = elements[idx]
            el.fill(text)
            print(f"[OK] Filled {ref}: {text}")
    
    def screenshot(self, path: str = None):
        """截图"""
        if not path:
            path = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.page.screenshot(path=path)
        print(f"[OK] Screenshot: {path}")
        return path
    
    def get_text(self, selector: str = None) -> str:
        """获取文本"""
        if selector:
            el = self.page.query_selector(selector)
            return el.inner_text() if el else ""
        return self.page.inner_text("body")
    
    def close(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("[OK] Browser closed")


# ========== 便捷函数 ==========

def open_url(url: str, headless: bool = True) -> NeuralSiteBrowser:
    """快速打开URL"""
    browser = NeuralSiteBrowser(headless=headless)
    browser.start()
    browser.open(url)
    return browser


# ========== 预设场景 ==========

class ConstructionAutomation:
    """施工自动化场景"""
    
    def __init__(self, browser: NeuralSiteBrowser):
        self.browser = browser
    
    def query_weather(self, city: str = "上海") -> str:
        """查询天气"""
        url = f"https://www.weather.com.cn/weather/101{city}100101.shtml"
        self.browser.open(url)
        self.browser.page.wait_for_timeout(2000)
        return self.browser.get_text()
    
    def query_material_price(self, material: str = "沥青") -> str:
        """查询材料价格 (示例)"""
        # 这里可以用其他价格查询网站
        url = f"https://www.baidu.com/s?wd={material}价格"
        self.browser.open(url)
        self.browser.page.wait_for_timeout(2000)
        return self.browser.get_text("#content_left")
    
    def fill_construction_form(self, data: Dict):
        """填报施工数据 (示例框架)"""
        # 需要根据实际表单定制
        print(f"[INFO] Filling form: {data}")


# ========== 测试 ==========

if __name__ == "__main__":
    print("="*50)
    print("NeuralSite Browser Test")
    print("="*50)
    
    # 测试打开网页
    browser = NeuralSiteBrowser(headless=True)
    browser.start()
    
    # 打开示例页面
    print("\n[1] Opening example.com...")
    browser.open("https://example.com")
    print(f"    Title: {browser.page.title()}")
    
    # 获取快照
    print("\n[2] Getting snapshot...")
    snapshot = browser.snapshot()
    print(f"    Elements found: {len(snapshot['elements'])}")
    for item in snapshot['elements'][:5]:
        print(f"    {item['ref']}: {item['tag']} - {item['text'][:30]}")
    
    # 截图
    print("\n[3] Taking screenshot...")
    browser.screenshot("test.png")
    
    # 关闭
    browser.close()
    
    print("\n[OK] Test complete!")
