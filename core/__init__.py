"""
Core module for Hekate Universal Web Scraper
"""

from .config import HekateConfig
from .scraper import HekateScraper
from .detector import WebsiteDetector
from .extractor import DataExtractor

__all__ = ['HekateConfig', 'HekateScraper', 'WebsiteDetector', 'DataExtractor'] 