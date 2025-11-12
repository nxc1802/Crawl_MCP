"""
Vercel serverless function - Main entry point
Serves the web interface and handles all routes
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, send_from_directory
from core.config import HekateConfig
from core.scraper import HekateScraper
from utils.helpers import validate_url, setup_logging

# Setup logging
setup_logging()

# Create Flask app
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'web', 'templates'),
    static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'web', 'static')
)

# Initialize config and scraper
config = HekateConfig()
scraper = HekateScraper(config)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'features': config.FEATURES,
        'stats': scraper.get_session_stats()
    })

@app.route('/api/info')
def api_info():
    """API information"""
    return jsonify({
        'name': 'Hekate Universal Web Scraper',
        'version': '1.0.0',
        'description': 'Universal web scraper with smart detection and anti-detection features',
        'endpoints': {
            'GET /health': 'Health check',
            'GET /api/info': 'API information',
            'POST /scrape': 'Main scraping endpoint',
            'GET /stats': 'Scraping statistics'
        }
    })

@app.route('/scrape', methods=['POST', 'OPTIONS'])
def scrape():
    """Main scraping endpoint"""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        url = data.get('url', '').strip()
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Validate URL
        if not validate_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Get extraction types
        extract_types = data.get('extract_types', ['text', 'images', 'links', 'metadata'])
        max_pages = data.get('max_pages', 1)
        
        # Perform scraping
        if max_pages == 1:
            result = scraper.scrape_single_page(url, extract_types)
        else:
            result = scraper.scrape_single_page(url, extract_types)
        
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def stats():
    """Get scraping statistics"""
    return jsonify(scraper.get_session_stats())

@app.route('/config')
def get_config():
    """Get current configuration"""
    return jsonify(config.validate_config())

# Vercel serverless handler
def handler(event, context=None):
    """Handler for Vercel serverless deployment"""
    with app.request_context(event):
        return app.full_dispatch_request()
