"""
Helper functions for Hekate Universal Web Scraper
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

def save_results_to_json(data: Dict[str, Any], filename: str = None) -> str:
    """
    Save scraping results to JSON file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scraping_results_{timestamp}.json"
    
    # Ensure data directory exists
    os.makedirs("data/results", exist_ok=True)
    filepath = os.path.join("data/results", filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Failed to save results: {e}")
        return None

def load_results_from_json(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Load scraping results from JSON file
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Results loaded from {filepath}")
        return data
    except Exception as e:
        logger.error(f"Failed to load results from {filepath}: {e}")
        return None

def validate_url(url: str) -> bool:
    """
    Validate if URL is properly formatted
    """
    import re
    
    # Basic URL validation pattern
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))

def clean_text(text: str) -> str:
    """
    Clean and normalize text content
    """
    import re
    
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\:\;\-\(\)]', '', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def extract_domain(url: str) -> str:
    """
    Extract domain from URL
    """
    from urllib.parse import urlparse
    
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return ""

def get_file_size(filepath: str) -> int:
    """
    Get file size in bytes
    """
    try:
        return os.path.getsize(filepath)
    except OSError:
        return 0

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def create_summary_report(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a summary report from scraping results
    """
    summary = {
        'timestamp': datetime.now().isoformat(),
        'total_pages': 0,
        'successful_pages': 0,
        'failed_pages': 0,
        'total_items_extracted': 0,
        'extraction_breakdown': {},
        'file_size': 0,
        'processing_time': 0
    }
    
    if 'pages' in results:
        summary['total_pages'] = len(results['pages'])
        summary['successful_pages'] = sum(1 for page in results['pages'] if page.get('success', False))
        summary['failed_pages'] = summary['total_pages'] - summary['successful_pages']
    
    if 'summary' in results:
        summary['total_items_extracted'] = sum(results['summary'].values())
        summary['extraction_breakdown'] = results['summary']
    
    return summary

def setup_logging(log_level: str = "INFO", log_file: str = "logs/hekate.log"):
    """
    Setup logging configuration
    """
    import logging
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logger.info(f"Logging configured: level={log_level}, file={log_file}")

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file system usage
    """
    import re
    
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    
    return filename

def generate_unique_filename(base_name: str, extension: str = "json") -> str:
    """
    Generate unique filename with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_base = sanitize_filename(base_name)
    return f"{safe_base}_{timestamp}.{extension}" 