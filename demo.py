#!/usr/bin/env python3
"""
Demo script to run Hekate web interface
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web.app import HekateWebApp

def run_demo():
    """Run the Hekate web interface demo"""
    
    print("🚀 Starting Hekate Universal Web Scraper Demo")
    print("=" * 60)
    print("🌐 Web Interface will be available at: http://localhost:8080")
    print("📋 Features:")
    print("   • Universal website scraping")
    print("   • Smart detection and extraction")
    print("   • Anti-detection with human behavior")
    print("   • Real-time results display")
    print("   • Multiple extraction types")
    print("=" * 60)
    print("💡 Try scraping: https://apec2025.kr/?menuno=1")
    print("💡 Or any other website you want to test")
    print("=" * 60)
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Create and run the web application
        app = HekateWebApp()
        app.run()
        
    except KeyboardInterrupt:
        print("\n✅ Server stopped successfully")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_demo() 