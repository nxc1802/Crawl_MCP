"""
Flask web application for Hekate Universal Web Scraper
"""

from flask import Flask, render_template, request, jsonify
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import HekateConfig
from core.scraper import HekateScraper
from utils.helpers import setup_logging, save_results_to_json

# Setup logging
setup_logging()

logger = logging.getLogger(__name__)

class HekateWebApp:
    """Flask web application for Hekate scraper"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.config = HekateConfig()
        self.scraper = HekateScraper(self.config)
        self.setup_routes()
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            """Main page"""
            return render_template('index.html')
        
        @self.app.route('/health')
        def health():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'version': '1.0.0',
                'features': self.config.FEATURES,
                'stats': self.scraper.get_session_stats()
            })
        
        @self.app.route('/api/info')
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
        
        @self.app.route('/scrape', methods=['POST'])
        def scrape():
            """Main scraping endpoint"""
            try:
                data = request.get_json()
                
                if not data:
                    return jsonify({'error': 'No data provided'}), 400
                
                url = data.get('url', '').strip()
                if not url:
                    return jsonify({'error': 'URL is required'}), 400
                
                # Validate URL
                from utils.helpers import validate_url
                if not validate_url(url):
                    return jsonify({'error': 'Invalid URL format'}), 400
                
                # Get extraction types
                extract_types = data.get('extract_types', ['text', 'images', 'links', 'metadata'])
                max_pages = data.get('max_pages', 1)
                
                logger.info(f"Starting scrape for {url}")
                
                # Perform scraping
                if max_pages == 1:
                    result = self.scraper.scrape_single_page(url, extract_types)
                else:
                    # For multiple pages, we'll just scrape the single page for now
                    # In a real implementation, you'd extract links and follow them
                    result = self.scraper.scrape_single_page(url, extract_types)
                
                # Save results if requested
                if data.get('save_results', False):
                    filename = data.get('filename', None)
                    saved_file = save_results_to_json(result, filename)
                    if saved_file:
                        result['saved_file'] = saved_file
                
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"Scraping error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/stats')
        def stats():
            """Get scraping statistics"""
            return jsonify(self.scraper.get_session_stats())
        
        @self.app.route('/config')
        def config():
            """Get current configuration"""
            return jsonify(self.config.validate_config())
    
    def run(self, host=None, port=None, debug=None):
        """Run the Flask application"""
        host = host or self.config.HOST
        port = port or self.config.DEFAULT_PORT
        debug = debug if debug is not None else self.config.DEBUG_MODE
        
        logger.info("=" * 60)
        logger.info("🚀 HEKATE UNIVERSAL WEB SCRAPER")
        logger.info("=" * 60)
        logger.info(f"🌐 Server: http://{host}:{port}")
        logger.info("🔧 Features:")
        logger.info("   • Universal website support")
        logger.info("   • Smart detection and extraction")
        logger.info("   • Anti-detection with human behavior")
        logger.info("   • Web interface for easy use")
        logger.info("=" * 60)
        
        self.app.run(host=host, port=port, debug=debug, threaded=True)

def create_app():
    """Factory function to create Flask app"""
    app_instance = HekateWebApp()
    return app_instance.app

if __name__ == '__main__':
    app = HekateWebApp()
    app.run() 