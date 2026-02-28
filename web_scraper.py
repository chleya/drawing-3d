# -*- coding: utf-8 -*-
"""
Firecrawl Web Scraper - 网络爬虫集成
用于采集安全法规、竞品分析、知识获取

API Key: fc-2c1cdfc9ed354caeaa7182bec1e79a65
"""

import os
from firecrawl import FirecrawlApp

# API Key
API_KEY = "fc-2c1cdfc9ed354caeaa7182bec1e79a65"


class WebScraper:
    """网页爬虫 - 基于Firecrawl"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        self.app = FirecrawlApp(api_key=self.api_key)
    
    def scrape(self, url: str) -> dict:
        """爬取单个URL
        
        Args:
            url: 目标URL
        
        Returns:
            dict: 爬取结果
        """
        try:
            result = self.app.scrape(url)
            return {
                'status': 'success',
                'url': url,
                'markdown': result.markdown if hasattr(result, 'markdown') and result.markdown else None,
                'html': result.html if hasattr(result, 'html') and result.html else None,
                'links': result.links if hasattr(result, 'links') else [],
            }
        except Exception as e:
            return {
                'status': 'error',
                'url': url,
                'message': str(e)
            }
    
    def search(self, query: str, limit: int = 5) -> dict:
        """搜索网页
        
        Args:
            query: 搜索关键词
            limit: 结果数量
        
        Returns:
            dict: 搜索结果
        """
        try:
            result = self.app.search(query, limit=limit)
            # result.web 是网页结果列表, result.news 是新闻结果
            results_list = []
            
            if hasattr(result, 'web') and result.web:
                for item in result.web:
                    results_list.append({
                        'title': getattr(item, 'title', 'N/A'),
                        'url': getattr(item, 'url', 'N/A'),
                        'description': getattr(item, 'description', 'N/A'),
                    })
            
            return {
                'status': 'success',
                'query': query,
                'results': results_list
            }
        except Exception as e:
            return {
                'status': 'error',
                'query': query,
                'message': str(e)
            }
    
    def crawl(self, url: str, limit: int = 10) -> dict:
        """爬取整个网站
        
        Args:
            url: 目标网站
            limit: 最大页面数
        
        Returns:
            dict: 爬取结果
        """
        try:
            result = self.app.crawl(url, limit=limit)
            return {
                'status': 'success',
                'url': url,
                'pages': len(result.data) if hasattr(result, 'data') else 0,
                'data': result.data if hasattr(result, 'data') else []
            }
        except Exception as e:
            return {
                'status': 'error',
                'url': url,
                'message': str(e)
            }


# ==================== 预设功能 ====================

def search_safety_news():
    """搜索安全相关新闻"""
    scraper = WebScraper()
    return scraper.search("construction site safety regulations China 2026", limit=5)


def search_helmet_detection():
    """搜索安全帽检测技术"""
    scraper = WebScraper()
    return scraper.search("YOLO helmet detection deep learning", limit=5)


def competitive_research():
    """竞品调研"""
    scraper = WebScraper()
    return scraper.search("smart construction site management system", limit=5)


# ==================== 测试 ====================

if __name__ == "__main__":
    print("="*60)
    print("Firecrawl Web Scraper Test")
    print("="*60)
    
    scraper = WebScraper()
    
    # 测试搜索
    print("\n[1] Testing search...")
    result = scraper.search("construction safety helmet", limit=3)
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        results = result.get('results', [])
        print(f"Results: {len(results)}")
        for r in results:
            print(f"  - {r.get('title', 'N/A')[:60]}")
    
    # 测试爬取
    print("\n[2] Testing scrape...")
    result2 = scraper.scrape("https://example.com")
    print(f"Status: {result2['status']}")
    if result2['status'] == 'success':
        markdown = result2.get('markdown', '')
        print(f"Markdown length: {len(markdown) if markdown else 0}")
        if markdown:
            print(f"First 100 chars: {markdown[:100]}")
    
    print("\n[SUCCESS] Firecrawl is working!")
