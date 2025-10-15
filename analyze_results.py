#!/usr/bin/env python3
"""
Analyze scraping results to ensure completeness
"""

import json
import sys
import os
from collections import Counter
from urllib.parse import urlparse

def analyze_scraping_results(filepath):
    """Analyze scraping results for completeness"""
    
    print("Analyzing scraping results...")
    print("=" * 60)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Basic info
    print(f"File: {os.path.basename(filepath)}")
    print(f"URL: {data.get('url', 'N/A')}")
    print(f"Website Type: {data.get('website_type', 'N/A')}")
    print(f"Language: {data.get('language', 'N/A')}")
    print(f"Encoding: {data.get('encoding', 'N/A')}")
    print()
    
    # Page complexity analysis
    complexity = data.get('page_complexity', {})
    print("Page Complexity Analysis:")
    print(f"   Total elements: {complexity.get('total_elements', 0)}")
    print(f"   Text elements: {complexity.get('text_elements', 0)}")
    print(f"   Image elements: {complexity.get('image_elements', 0)}")
    print(f"   Link elements: {complexity.get('link_elements', 0)}")
    print(f"   Script elements: {complexity.get('script_elements', 0)}")
    print()
    
    # Summary statistics
    summary = data.get('summary', {})
    print("Extraction Summary:")
    print(f"   Text items: {summary.get('text_items', 0)}")
    print(f"   Images: {summary.get('images', 0)}")
    print(f"   Links: {summary.get('links', 0)}")
    print(f"   Structured data: {summary.get('structured_data_items', 0)}")
    print(f"   Tables: {summary.get('tables', 0)}")
    print(f"   Forms: {summary.get('forms', 0)}")
    print(f"   Navigation menus: {summary.get('navigation_menus', 0)}")
    print()
    
    # Detailed analysis
    detailed_data = data.get('data', {})
    
    # Text content analysis
    text_content = detailed_data.get('text_content', [])
    if text_content:
        print("Text Content Analysis:")
        print(f"   Total text items: {len(text_content)}")
        
        # Analyze text content for key information
        all_text = ' '.join([item.get('content', '') for item in text_content])
        
        # Check for key APEC information
        key_terms = [
            'APEC 2025', 'KOREA', 'Gyeongju', 'Jeju', 'Incheon', 'Busan', 'Seoul',
            'Economic Leaders', 'Ministerial Meeting', 'Senior Officials',
            'Building a Sustainable Tomorrow', 'Connect, Innovate, Prosper'
        ]
        
        found_terms = []
        for term in key_terms:
            if term.lower() in all_text.lower():
                found_terms.append(term)
        
        print(f"   Key terms found: {len(found_terms)}/{len(key_terms)}")
        for term in found_terms:
            print(f"     + {term}")
        
        # Check for specific content types
        content_types = {
            'meetings': ['meeting', 'conference', 'summit'],
            'locations': ['gyeongju', 'jeju', 'incheon', 'busan', 'seoul'],
            'dates': ['2025', 'july', 'may', 'october'],
            'officials': ['minister', 'director', 'president', 'ambassador']
        }
        
        for content_type, keywords in content_types.items():
            found = sum(1 for keyword in keywords if keyword in all_text.lower())
            print(f"   {content_type.title()}: {found}/{len(keywords)} keywords found")
    
    # Image analysis
    images = detailed_data.get('images', [])
    if images:
        print(f"\nImage Analysis:")
        print(f"   Total images: {len(images)}")
        
        # Analyze image types
        image_types = Counter()
        for img in images:
            src = img.get('src', '')
            alt = img.get('alt', '')
            
            if 'visual' in src.lower():
                image_types['visual'] += 1
            elif 'banner' in src.lower():
                image_types['banner'] += 1
            elif 'icon' in src.lower() or 'ico' in src.lower():
                image_types['icon'] += 1
            else:
                image_types['other'] += 1
        
        for img_type, count in image_types.items():
            print(f"   {img_type.title()}: {count}")
    
    # Link analysis
    links = detailed_data.get('links', [])
    if links:
        print(f"\nLink Analysis:")
        print(f"   Total links: {len(links)}")
        
        # Analyze link types
        link_types = Counter()
        external_links = []
        internal_links = []
        
        for link in links:
            href = link.get('href', '')
            text = link.get('text', '')
            
            if href.startswith('http'):
                parsed = urlparse(href)
                if parsed.netloc == 'apec2025.kr':
                    internal_links.append(href)
                else:
                    external_links.append(href)
                    link_types['external'] += 1
            else:
                internal_links.append(href)
                link_types['internal'] += 1
            
            # Categorize by content
            if any(keyword in text.lower() for keyword in ['meeting', 'conference']):
                link_types['meetings'] += 1
            elif any(keyword in text.lower() for keyword in ['news', 'press']):
                link_types['news'] += 1
            elif any(keyword in text.lower() for keyword in ['social', 'media']):
                link_types['social'] += 1
            elif any(keyword in text.lower() for keyword in ['visit', 'travel']):
                link_types['travel'] += 1
        
        print(f"   Internal links: {len(internal_links)}")
        print(f"   External links: {len(external_links)}")
        
        for link_type, count in link_types.items():
            print(f"   {link_type.title()}: {count}")
        
        # Show some external links
        if external_links:
            print(f"\n   External links found:")
            for link in external_links[:5]:  # Show first 5
                print(f"     - {link}")
    
    # Metadata analysis
    metadata = detailed_data.get('metadata', {})
    if metadata:
        print(f"\nMetadata Analysis:")
        print(f"   Title: {metadata.get('title', 'N/A')}")
        print(f"   Description: {metadata.get('description', 'N/A')[:100]}...")
        print(f"   Keywords: {metadata.get('keywords', 'N/A')}")
        print(f"   Author: {metadata.get('author', 'N/A')}")
        print(f"   Viewport: {metadata.get('viewport', 'N/A')}")
    
    # Completeness assessment
    print(f"\nCompleteness Assessment:")
    
    # Check if all major sections were found
    sections_found = []
    
    if any('APEC 2025' in item.get('content', '') for item in text_content):
        sections_found.append('Main title')
    
    if any('Gyeongju' in item.get('content', '') for item in text_content):
        sections_found.append('Location information')
    
    if any('meeting' in item.get('content', '').lower() for item in text_content):
        sections_found.append('Meeting information')
    
    if any('social' in item.get('alt', '').lower() for item in images):
        sections_found.append('Social media links')
    
    if any('youtube' in item.get('alt', '').lower() for item in images):
        sections_found.append('YouTube presence')
    
    print(f"   Sections found: {len(sections_found)}")
    for section in sections_found:
        print(f"     + {section}")
    
    # Overall assessment
    total_score = len(sections_found)
    max_score = 5  # Expected sections
    
    if total_score >= max_score:
        print(f"\nEXCELLENT: All major information has been successfully extracted!")
    elif total_score >= 3:
        print(f"\nGOOD: Most information has been extracted successfully.")
    else:
        print(f"\nPARTIAL: Some information may be missing.")
    
    print(f"   Completeness score: {total_score}/{max_score} ({total_score/max_score*100:.1f}%)")

if __name__ == "__main__":
    # Find the most recent results file
    results_dir = "data/results"
    if os.path.exists(results_dir):
        files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
        if files:
            # Sort by modification time (newest first)
            files.sort(key=lambda x: os.path.getmtime(os.path.join(results_dir, x)), reverse=True)
            latest_file = os.path.join(results_dir, files[0])
            analyze_scraping_results(latest_file)
        else:
            print("No results files found in data/results/")
    else:
        print("Results directory not found") 