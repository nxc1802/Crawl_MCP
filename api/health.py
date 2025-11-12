"""
Vercel serverless function - Health check endpoint
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import HekateConfig

config = HekateConfig()

def handler(event, context=None):
    """Health check handler"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'status': 'healthy',
            'version': '1.0.0',
            'features': config.FEATURES,
            'message': 'Hekate Universal Web Scraper is running'
        })
    }

