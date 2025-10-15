"""
Proxy management for Hekate Universal Web Scraper
"""

import random
import requests
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class ProxyManager:
    """Manages proxy rotation and validation"""
    
    def __init__(self, proxy_list: List[str] = None):
        self.proxies = proxy_list or []
        self.working_proxies = []
        self.failed_proxies = []
        self.current_proxy_index = 0
        
    def add_proxy(self, proxy: str):
        """Add a proxy to the list"""
        if proxy not in self.proxies:
            self.proxies.append(proxy)
            logger.info(f"Added proxy: {proxy}")
    
    def add_proxies_from_file(self, file_path: str):
        """Load proxies from a file"""
        try:
            with open(file_path, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
            self.proxies.extend(proxies)
            logger.info(f"Loaded {len(proxies)} proxies from {file_path}")
        except FileNotFoundError:
            logger.error(f"Proxy file not found: {file_path}")
        except Exception as e:
            logger.error(f"Error loading proxies from {file_path}: {e}")
    
    def test_proxy(self, proxy: str, test_url: str = "http://httpbin.org/ip") -> bool:
        """Test if a proxy is working"""
        try:
            proxies = {
                'http': proxy,
                'https': proxy
            }
            
            response = requests.get(
                test_url,
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.debug(f"Proxy {proxy} is working")
                return True
            else:
                logger.debug(f"Proxy {proxy} failed with status {response.status_code}")
                return False
                
        except Exception as e:
            logger.debug(f"Proxy {proxy} failed: {e}")
            return False
    
    def validate_proxies(self, test_url: str = "http://httpbin.org/ip"):
        """Validate all proxies and separate working from failed ones"""
        logger.info(f"Validating {len(self.proxies)} proxies...")
        
        self.working_proxies = []
        self.failed_proxies = []
        
        for proxy in self.proxies:
            if self.test_proxy(proxy, test_url):
                self.working_proxies.append(proxy)
            else:
                self.failed_proxies.append(proxy)
        
        logger.info(f"Validation complete: {len(self.working_proxies)} working, {len(self.failed_proxies)} failed")
    
    def get_next_proxy(self) -> Optional[str]:
        """Get the next working proxy in rotation"""
        if not self.working_proxies:
            logger.warning("No working proxies available")
            return None
        
        proxy = self.working_proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.working_proxies)
        
        return proxy
    
    def get_random_proxy(self) -> Optional[str]:
        """Get a random working proxy"""
        if not self.working_proxies:
            return None
        
        return random.choice(self.working_proxies)
    
    def mark_proxy_failed(self, proxy: str):
        """Mark a proxy as failed and move it to failed list"""
        if proxy in self.working_proxies:
            self.working_proxies.remove(proxy)
            self.failed_proxies.append(proxy)
            logger.warning(f"Marked proxy as failed: {proxy}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get proxy statistics"""
        return {
            'total_proxies': len(self.proxies),
            'working_proxies': len(self.working_proxies),
            'failed_proxies': len(self.failed_proxies),
            'success_rate': (len(self.working_proxies) / max(len(self.proxies), 1)) * 100
        } 