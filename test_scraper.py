#!/usr/bin/env python3
"""
Test script for Hekate Universal Web Scraper
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import HekateConfig
from core.scraper import HekateScraper
from utils.helpers import setup_logging

def test_scraper():
    """Test the scraper with APEC 2025 website"""
    
    print("🧪 Testing Hekate Universal Web Scraper")
    print("=" * 50)
    
    # Setup logging
    setup_logging()
    
    # Create scraper instance
    config = HekateConfig()
    scraper = HekateScraper(config)
    
    # Test URL
    test_url = "https://apec2025.kr/?menuno=1"
    
    print(f"🌐 Testing URL: {test_url}")
    print("📊 Extraction types: text, images, links, metadata")
    print("-" * 50)
    
    try:
        # Perform scraping
        result = scraper.scrape_single_page(
            url=test_url,
            extract_types=['text', 'images', 'links', 'metadata']
        )
        
        if result['success']:
            print("✅ Scraping completed successfully!")
            print(f"🌍 Website type: {result.get('website_type', 'unknown')}")
            print(f"🌐 Language: {result.get('language', 'unknown')}")
            print(f"📝 Encoding: {result.get('encoding', 'unknown')}")
            
            # Show summary
            summary = result.get('summary', {})
            print("\n📊 Extraction Summary:")
            print(f"   • Text items: {summary.get('text_items', 0)}")
            print(f"   • Images: {summary.get('images', 0)}")
            print(f"   • Links: {summary.get('links', 0)}")
            print(f"   • Structured data: {summary.get('structured_data_items', 0)}")
            print(f"   • Tables: {summary.get('tables', 0)}")
            print(f"   • Forms: {summary.get('forms', 0)}")
            print(f"   • Navigation menus: {summary.get('navigation_menus', 0)}")
            
            # Show some sample data
            data = result.get('data', {})
            
            if data.get('text_content'):
                print(f"\n📝 Sample text content ({len(data['text_content'])} items):")
                for i, item in enumerate(data['text_content'][:3]):
                    content = item.get('content', '')[:100]
                    print(f"   {i+1}. {content}...")
            
            if data.get('images'):
                print(f"\n🖼️ Sample images ({len(data['images'])} items):")
                for i, img in enumerate(data['images'][:3]):
                    src = img.get('src', '')
                    alt = img.get('alt', 'No alt text')
                    print(f"   {i+1}. {src} (alt: {alt})")
            
            if data.get('links'):
                print(f"\n🔗 Sample links ({len(data['links'])} items):")
                for i, link in enumerate(data['links'][:3]):
                    href = link.get('href', '')
                    text = link.get('text', 'No text')
                    print(f"   {i+1}. {text} -> {href}")
            
            # Show session stats
            stats = scraper.get_session_stats()
            print(f"\n📈 Session Statistics:")
            print(f"   • Pages scraped: {stats['pages_scraped']}")
            print(f"   • Total requests: {stats['total_requests']}")
            print(f"   • Success rate: {stats['success_rate']:.1f}%")
            
        else:
            print("❌ Scraping failed!")
            print(f"Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scraper() 