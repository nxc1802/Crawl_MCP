"""
Core scraper module for Hekate Universal Web Scraper
Main scraping engine with anti-detection and smart extraction
"""

import time
import random
import requests
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging
from datetime import datetime

from .config import HekateConfig
from .detector import WebsiteDetector
from .extractor import DataExtractor

logger = logging.getLogger(__name__)

class HekateScraper:
    """Main scraper class with universal website support"""
    
    def __init__(self, config: HekateConfig = None):
        self.config = config or HekateConfig()
        self.detector = WebsiteDetector()
        self.extractor = DataExtractor(self.config)
        self.session = requests.Session()
        self.stats = {
            'pages_scraped': 0,
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'start_time': None,
            'end_time': None
        }
        
        self._setup_session()
    
    def _setup_session(self):
        """Setup session with anti-detection features"""
        # Set random user agent
        user_agent = random.choice(self.config.USER_AGENTS)
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        logger.info(f"Session initialized with User-Agent: {user_agent[:50]}...")
    
    def _rotate_user_agent(self):
        """Rotate user agent for anti-detection"""
        user_agent = random.choice(self.config.USER_AGENTS)
        self.session.headers.update({'User-Agent': user_agent})
        logger.debug(f"Rotated User-Agent to: {user_agent[:50]}...")
    
    def _human_delay(self):
        """Add human-like delay between requests"""
        delay = random.uniform(self.config.MIN_DELAY, self.config.MAX_DELAY)
        time.sleep(delay)
        logger.debug(f"Applied human delay: {delay:.2f}s")
    
    def _get_page(self, url: str, retries: int = None) -> Optional[requests.Response]:
        """
        Get page with retry logic and anti-detection
        """
        retries = retries or self.config.MAX_RETRIES
        
        for attempt in range(retries):
            try:
                logger.info(f"Requesting {url} (attempt {attempt + 1}/{retries})")
                
                # Rotate user agent every few requests
                if self.stats['total_requests'] % 3 == 0:
                    self._rotate_user_agent()
                
                response = self.session.get(
                    url,
                    timeout=self.config.REQUEST_TIMEOUT,
                    allow_redirects=True
                )
                
                self.stats['total_requests'] += 1
                
                if response.status_code == 200:
                    self.stats['successful_requests'] += 1
                    logger.info(f"Successfully fetched {url}")
                    return response
                else:
                    logger.warning(f"HTTP {response.status_code} for {url}")
                    
            except requests.exceptions.RequestException as e:
                self.stats['failed_requests'] += 1
                logger.error(f"Request failed for {url}: {e}")
                
                if attempt < retries - 1:
                    delay = (attempt + 1) * 2  # Exponential backoff
                    logger.info(f"Retrying in {delay}s...")
                    time.sleep(delay)
            
            # Apply human delay between attempts
            self._human_delay()
        
        logger.error(f"Failed to fetch {url} after {retries} attempts")
        return None
    
    def scrape_single_page(self, url: str, extract_types: List[str] = None) -> Dict[str, Any]:
        """
        Scrape a single page with smart detection
        """
        if extract_types is None:
            extract_types = ['text', 'images', 'links', 'metadata']
        
        logger.info(f"Starting single page scrape: {url}")
        self.stats['start_time'] = datetime.now()
        
        # Get the page
        response = self._get_page(url)
        if not response:
            return {
                'success': False,
                'error': 'Failed to fetch page',
                'url': url
            }
        
        # Parse HTML
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"Failed to parse HTML for {url}: {e}")
            return {
                'success': False,
                'error': f'HTML parsing failed: {e}',
                'url': url
            }
        
        # Detect website type and structure
        website_type = self.detector.detect_website_type(url, response.text)
        page_structure = self.detector.detect_page_structure(soup, website_type)
        optimal_selectors = self.detector.get_optimal_selectors(website_type, page_structure)
        
        # Extract data based on requested types
        extraction_result = {
            'success': True,
            'url': url,
            'website_type': website_type,
            'language': self.detector.detect_language(response.text),
            'encoding': self.detector.detect_encoding(response.text),
            'page_complexity': self.detector.analyze_page_complexity(soup),
            'extraction_types': extract_types,
            'data': {}
        }
        
        # Extract requested data types
        if 'text' in extract_types:
            extraction_result['data']['text_content'] = self.extractor.extract_text_content(
                soup, optimal_selectors.get('content', [])
            )
        
        if 'images' in extract_types:
            extraction_result['data']['images'] = self.extractor.extract_images(soup, url)
        
        if 'links' in extract_types:
            extraction_result['data']['links'] = self.extractor.extract_links(soup, url)
        
        if 'metadata' in extract_types:
            extraction_result['data']['metadata'] = self.extractor.extract_metadata(soup)
        
        if 'structured_data' in extract_types:
            extraction_result['data']['structured_data'] = self.extractor.extract_structured_data(soup)
        
        if 'tables' in extract_types:
            extraction_result['data']['tables'] = self.extractor.extract_tables(soup)
        
        if 'forms' in extract_types:
            extraction_result['data']['forms'] = self.extractor.extract_forms(soup)
        
        if 'navigation' in extract_types:
            extraction_result['data']['navigation'] = self.extractor.extract_navigation(soup, url)
        
        # Add summary statistics
        extraction_result['summary'] = {
            'text_items': len(extraction_result['data'].get('text_content', [])),
            'images': len(extraction_result['data'].get('images', [])),
            'links': len(extraction_result['data'].get('links', [])),
            'structured_data_items': len(extraction_result['data'].get('structured_data', [])),
            'tables': len(extraction_result['data'].get('tables', [])),
            'forms': len(extraction_result['data'].get('forms', [])),
            'navigation_menus': len(extraction_result['data'].get('navigation', []))
        }
        
        self.stats['pages_scraped'] += 1
        self.stats['end_time'] = datetime.now()
        
        logger.info(f"Successfully scraped {url}: {extraction_result['summary']}")
        
        return extraction_result
    
    def scrape_multiple_pages(self, urls: List[str], extract_types: List[str] = None) -> Dict[str, Any]:
        """
        Scrape multiple pages with progress tracking
        """
        if extract_types is None:
            extract_types = ['text', 'images', 'links', 'metadata']
        
        logger.info(f"Starting multi-page scrape: {len(urls)} URLs")
        self.stats['start_time'] = datetime.now()
        
        results = {
            'success': True,
            'total_pages': len(urls),
            'successful_pages': 0,
            'failed_pages': 0,
            'pages': [],
            'summary': {
                'total_text_items': 0,
                'total_images': 0,
                'total_links': 0,
                'total_structured_data': 0,
                'total_tables': 0,
                'total_forms': 0,
                'total_navigation': 0
            }
        }
        
        for i, url in enumerate(urls, 1):
            logger.info(f"Scraping page {i}/{len(urls)}: {url}")
            
            page_result = self.scrape_single_page(url, extract_types)
            
            if page_result['success']:
                results['successful_pages'] += 1
                results['pages'].append(page_result)
                
                # Update summary statistics
                summary = page_result.get('summary', {})
                results['summary']['total_text_items'] += summary.get('text_items', 0)
                results['summary']['total_images'] += summary.get('images', 0)
                results['summary']['total_links'] += summary.get('links', 0)
                results['summary']['total_structured_data'] += summary.get('structured_data_items', 0)
                results['summary']['total_tables'] += summary.get('tables', 0)
                results['summary']['total_forms'] += summary.get('forms', 0)
                results['summary']['total_navigation'] += summary.get('navigation_menus', 0)
            else:
                results['failed_pages'] += 1
                results['pages'].append(page_result)
            
            # Add delay between pages
            if i < len(urls):
                self._human_delay()
        
        self.stats['end_time'] = datetime.now()
        
        logger.info(f"Multi-page scrape completed: {results['successful_pages']}/{len(urls)} successful")
        
        return results
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get current session statistics"""
        duration = None
        if self.stats['start_time'] and self.stats['end_time']:
            duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        return {
            'pages_scraped': self.stats['pages_scraped'],
            'total_requests': self.stats['total_requests'],
            'successful_requests': self.stats['successful_requests'],
            'failed_requests': self.stats['failed_requests'],
            'success_rate': (self.stats['successful_requests'] / max(self.stats['total_requests'], 1)) * 100,
            'duration_seconds': duration,
            'config': self.config.validate_config()
        }
    
    def reset_stats(self):
        """Reset session statistics"""
        self.stats = {
            'pages_scraped': 0,
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'start_time': None,
            'end_time': None
        }
        logger.info("Session statistics reset") 