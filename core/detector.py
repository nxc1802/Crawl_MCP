"""
Website structure detector for Hekate Universal Web Scraper
Automatically detects website type and structure for optimal extraction
"""

import re
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class WebsiteDetector:
    """Detects website type and structure for optimal scraping"""
    
    def __init__(self):
        self.website_patterns = {
            'news': [
                r'news', r'article', r'headline', r'breaking',
                r'cnn\.com', r'bbc\.com', r'reuters\.com',
                r'\.news', r'press', r'media'
            ],
            'ecommerce': [
                r'shop', r'store', r'buy', r'product',
                r'amazon\.com', r'ebay\.com', r'shopify\.com',
                r'\.shop', r'cart', r'checkout'
            ],
            'blog': [
                r'blog', r'post', r'article', r'wordpress',
                r'\.blog', r'medium\.com', r'blogspot\.com',
                r'entry', r'post-content'
            ],
            'corporate': [
                r'about', r'contact', r'company', r'corporate',
                r'\.com/about', r'\.com/contact', r'\.com/company',
                r'team', r'careers', r'press'
            ],
            'social': [
                r'facebook\.com', r'twitter\.com', r'instagram\.com',
                r'linkedin\.com', r'youtube\.com', r'tiktok\.com',
                r'social', r'profile', r'feed'
            ]
        }
        
        self.content_indicators = {
            'news': ['headline', 'article', 'news', 'breaking', 'latest'],
            'ecommerce': ['product', 'price', 'buy', 'cart', 'shop'],
            'blog': ['post', 'blog', 'entry', 'author', 'published'],
            'corporate': ['about', 'contact', 'company', 'team', 'careers'],
            'social': ['profile', 'feed', 'post', 'share', 'follow']
        }
    
    def detect_website_type(self, url: str, html_content: str = None) -> str:
        """
        Detect website type based on URL and content
        """
        domain = urlparse(url).netloc.lower()
        path = urlparse(url).path.lower()
        
        # Check URL patterns
        for website_type, patterns in self.website_patterns.items():
            for pattern in patterns:
                if re.search(pattern, domain) or re.search(pattern, path):
                    logger.info(f"Detected website type: {website_type} from URL pattern")
                    return website_type
        
        # If no URL pattern match, analyze content
        if html_content:
            return self._detect_from_content(html_content)
        
        # Default to general
        return 'general'
    
    def _detect_from_content(self, html_content: str) -> str:
        """
        Detect website type from HTML content
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text().lower()
        
        scores = {}
        for website_type, indicators in self.content_indicators.items():
            score = 0
            for indicator in indicators:
                if indicator in text_content:
                    score += 1
            scores[website_type] = score
        
        # Find the type with highest score
        if scores:
            best_type = max(scores, key=scores.get)
            if scores[best_type] > 0:
                logger.info(f"Detected website type: {best_type} from content analysis")
                return best_type
        
        return 'general'
    
    def detect_page_structure(self, soup: BeautifulSoup, website_type: str = None) -> Dict[str, Any]:
        """
        Detect page structure and extract selectors
        """
        structure = {
            'title_selectors': [],
            'content_selectors': [],
            'image_selectors': [],
            'link_selectors': [],
            'navigation_selectors': []
        }
        
        # Detect title elements
        title_elements = soup.find_all(['h1', 'h2', 'h3'])
        for element in title_elements:
            if element.get_text().strip():
                structure['title_selectors'].append(element.name)
        
        # Detect content elements
        content_elements = soup.find_all(['p', 'article', 'div'])
        for element in content_elements:
            if len(element.get_text().strip()) > 50:  # Minimum content length
                structure['content_selectors'].append(element.name)
        
        # Detect image elements
        image_elements = soup.find_all('img')
        if image_elements:
            structure['image_selectors'].append('img')
        
        # Detect link elements
        link_elements = soup.find_all('a')
        if link_elements:
            structure['link_selectors'].append('a')
        
        # Detect navigation elements
        nav_elements = soup.find_all(['nav', 'menu'])
        for element in nav_elements:
            structure['navigation_selectors'].append(element.name)
        
        return structure
    
    def get_optimal_selectors(self, website_type: str, page_structure: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Get optimal selectors based on website type and detected structure
        """
        from .config import HekateConfig
        
        # Start with universal selectors
        selectors = HekateConfig.UNIVERSAL_SELECTORS.copy()
        
        # Add website-specific templates
        if website_type in HekateConfig.WEBSITE_TEMPLATES:
            template = HekateConfig.WEBSITE_TEMPLATES[website_type]
            for key, template_selectors in template.items():
                if key in selectors:
                    selectors[key].extend(template_selectors)
        
        # Add detected structure selectors
        for key, detected_selectors in page_structure.items():
            if key in selectors:
                selectors[key].extend(detected_selectors)
        
        # Remove duplicates while preserving order
        for key in selectors:
            seen = set()
            unique_selectors = []
            for selector in selectors[key]:
                if selector not in seen:
                    seen.add(selector)
                    unique_selectors.append(selector)
            selectors[key] = unique_selectors
        
        return selectors
    
    def detect_language(self, html_content: str) -> str:
        """
        Detect website language
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check lang attribute
        lang_attr = soup.find('html').get('lang', '') if soup.find('html') else ''
        if lang_attr:
            return lang_attr.split('-')[0]
        
        # Check meta tags
        meta_lang = soup.find('meta', attrs={'http-equiv': 'content-language'})
        if meta_lang:
            return meta_lang.get('content', '').split('-')[0]
        
        # Analyze text content for language patterns
        text = soup.get_text()[:1000]  # First 1000 characters
        
        # Simple language detection patterns
        if re.search(r'[가-힣]', text):  # Korean
            return 'ko'
        elif re.search(r'[一-龯]', text):  # Chinese
            return 'zh'
        elif re.search(r'[あ-ん]', text):  # Japanese
            return 'ja'
        elif re.search(r'[а-я]', text):  # Russian
            return 'ru'
        elif re.search(r'[à-ÿ]', text):  # French
            return 'fr'
        elif re.search(r'[ä-ü]', text):  # German
            return 'de'
        else:
            return 'en'  # Default to English
    
    def detect_encoding(self, html_content: str) -> str:
        """
        Detect HTML encoding
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check meta charset
        meta_charset = soup.find('meta', charset=True)
        if meta_charset:
            return meta_charset.get('charset')
        
        # Check meta http-equiv
        meta_equiv = soup.find('meta', attrs={'http-equiv': 'content-type'})
        if meta_equiv:
            content = meta_equiv.get('content', '')
            if 'charset=' in content:
                return content.split('charset=')[1]
        
        return 'utf-8'  # Default encoding
    
    def analyze_page_complexity(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Analyze page complexity for scraping strategy
        """
        analysis = {
            'total_elements': len(soup.find_all()),
            'text_elements': len(soup.find_all(['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])),
            'image_elements': len(soup.find_all('img')),
            'link_elements': len(soup.find_all('a')),
            'form_elements': len(soup.find_all('form')),
            'table_elements': len(soup.find_all('table')),
            'script_elements': len(soup.find_all('script')),
            'style_elements': len(soup.find_all('style')),
            'iframe_elements': len(soup.find_all('iframe'))
        }
        
        # Calculate complexity score
        total = analysis['total_elements']
        if total > 0:
            analysis['complexity_score'] = {
                'text_ratio': analysis['text_elements'] / total,
                'image_ratio': analysis['image_elements'] / total,
                'link_ratio': analysis['link_elements'] / total,
                'interactive_ratio': (analysis['form_elements'] + analysis['script_elements']) / total
            }
        
        return analysis 