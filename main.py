#!/usr/bin/env python3
"""
Main entry point for Hekate Universal Web Scraper
"""

import sys
import os
import logging
from datetime import datetime

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import HekateConfig
from core.scraper import HekateScraper
from utils.helpers import setup_logging
from web.app import HekateWebApp

def main():
    """Main entry point for Hekate scraper"""
    try:
        print("\n" + "=" * 70)
        print("🚀 HEKATE - UNIVERSAL WEB SCRAPER")
        print("=" * 70)
        print("🎯 FEATURES:")
        print("   ✅ Universal website support")
        print("   ✅ Smart detection and extraction")
        print("   ✅ Anti-detection with human behavior")
        print("   ✅ Web interface for easy use")
        print("   ✅ Comprehensive data extraction")
        print("   ✅ Proxy support and rotation")
        print("   ✅ Error handling and recovery")
        print("=" * 70)
        print("🌐 WEB INTERFACE:")
        print("   • Open http://localhost:8080 in your browser")
        print("   • Enter any website URL to scrape")
        print("   • Choose extraction types")
        print("   • View results in real-time")
        print("=" * 70)
        
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # Create and run the web application
        app = HekateWebApp()
        app.run()
        
    except KeyboardInterrupt:
        logger.info("\n🛑 Server stopped by user")
        print("\n✅ Server shutdown completed successfully")
    except Exception as e:
        logger.error(f"❌ Server failed to start: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 