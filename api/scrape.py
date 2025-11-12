"""
Vercel serverless function - Scraping endpoint
"""

import sys
import os
import json
from flask import request, jsonify

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import HekateConfig
from core.scraper import HekateScraper
from utils.helpers import validate_url

# Initialize scraper
config = HekateConfig()
scraper = HekateScraper(config)

def handler(event, context=None):
    """Serverless handler for scraping"""
    try:
        # Parse request body
        if hasattr(event, 'get_json'):
            data = event.get_json()
        else:
            body = event.get('body', '{}')
            if isinstance(body, str):
                data = json.loads(body)
            else:
                data = body
        
        if not data:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No data provided'})
            }
        
        url = data.get('url', '').strip()
        if not url:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'URL is required'})
            }
        
        # Validate URL
        if not validate_url(url):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid URL format'})
            }
        
        # Get extraction types
        extract_types = data.get('extract_types', ['text', 'images', 'links', 'metadata'])
        
        # Perform scraping
        result = scraper.scrape_single_page(url, extract_types)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

