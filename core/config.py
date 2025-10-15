"""
Configuration module for Hekate Universal Web Scraper
Centralizes all configuration settings and constants
"""

import os
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HekateConfig:
    """Centralized configuration for the Hekate scraper system"""
    
    # Server Configuration
    DEFAULT_PORT = int(os.getenv('PORT', 8080))
    HOST = '0.0.0.0'
    DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Scraping Configuration
    MAX_PAGES_LIMIT = int(os.getenv('MAX_PAGES', 50))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 5))
    REQUEST_TIMEOUT = int(os.getenv('TIMEOUT', 30))
    REQUEST_DELAY = int(os.getenv('REQUEST_DELAY', 2))
    
    # Rate Limiting
    MIN_DELAY = 1
    MAX_DELAY = 5
    PAGE_DELAY_MIN = 2
    PAGE_DELAY_MAX = 6
    
    # Export Configuration
    EXPORT_DIRECTORY = "data/results"
    AUTO_EXPORT_THRESHOLD = 10
    
    # Enhanced User Agents for better anti-detection
    USER_AGENTS = [
        # Latest Chrome browsers
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        
        # Latest Firefox browsers
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        
        # Edge browsers
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        
        # Safari browsers
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        
        # Mobile browsers for variety
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
    ]
    
    # Feature Flags
    FEATURES = {
        'smart_detection': True,
        'anti_detection': True,
        'proxy_support': True,
        'human_behavior': True,
        'multi_page_crawling': True,
        'json_export': True,
        'performance_optimization': True,
        'image_extraction': True,
        'link_following': True
    }
    
    # Universal Selectors for different website types
    UNIVERSAL_SELECTORS = {
        'title': [
            'h1', 'h2', 'h3',
            '.title', '.headline', '.post-title',
            '[class*="title"]', '[class*="headline"]',
            'title'
        ],
        'content': [
            'p', 'article', '.content', '.post-content',
            '.article-content', '.entry-content',
            '[class*="content"]', '[class*="text"]'
        ],
        'images': [
            'img', '.image', '.photo',
            '[class*="image"]', '[class*="photo"]',
            '[class*="img"]'
        ],
        'links': [
            'a', '.link', '.nav-link',
            '[class*="link"]', '[class*="nav"]'
        ],
        'navigation': [
            'nav', '.navigation', '.menu',
            '[class*="nav"]', '[class*="menu"]'
        ]
    }
    
    # Website-specific templates
    WEBSITE_TEMPLATES = {
        'news': {
            'title': ['h1', '.headline', '.title'],
            'content': ['.article-content', '.post-content', 'article'],
            'date': ['.date', '.published', 'time'],
            'author': ['.author', '.byline', '.writer']
        },
        'ecommerce': {
            'title': ['h1', '.product-title', '.item-title'],
            'price': ['.price', '.cost', '.amount'],
            'description': ['.description', '.details', '.info'],
            'images': ['.product-image', '.item-image', 'img']
        },
        'blog': {
            'title': ['h1', '.post-title', '.entry-title'],
            'content': ['.post-content', '.entry-content', 'article'],
            'date': ['.date', '.published', 'time'],
            'author': ['.author', '.byline']
        },
        'corporate': {
            'title': ['h1', '.page-title', '.section-title'],
            'content': ['.content', '.main-content', 'main'],
            'contact': ['.contact', '.address', '.phone'],
            'about': ['.about', '.company-info']
        }
    }
    
    # System Messages
    STARTUP_MESSAGE = """
    🚀 HEKATE - UNIVERSAL WEB SCRAPER
    =================================
    🌐 Universal scraping for any website
    🎯 Smart detection and extraction
    🤖 Anti-detection with human behavior
    📊 Comprehensive data extraction
    =================================
    """
    
    @classmethod
    def get_logging_config(cls):
        """Get logging configuration"""
        return {
            'level': logging.INFO,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'handlers': [
                logging.FileHandler('logs/hekate.log'),
                logging.StreamHandler()
            ]
        }
    
    @classmethod
    def get_flask_config(cls):
        """Get Flask configuration"""
        return {
            'host': cls.HOST,
            'port': cls.DEFAULT_PORT,
            'debug': cls.DEBUG_MODE,
            'threaded': True
        }
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return status"""
        return {
            'server': {
                'port': cls.DEFAULT_PORT,
                'host': cls.HOST,
                'debug': cls.DEBUG_MODE
            },
            'scraping': {
                'max_pages': cls.MAX_PAGES_LIMIT,
                'max_retries': cls.MAX_RETRIES,
                'timeout': cls.REQUEST_TIMEOUT,
                'delay': cls.REQUEST_DELAY
            },
            'features': cls.FEATURES,
            'user_agents_count': len(cls.USER_AGENTS)
        } 