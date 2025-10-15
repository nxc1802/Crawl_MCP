"""
Data extraction module for Hekate Universal Web Scraper
Handles extraction of various data types from websites
"""

import re
import json
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class DataExtractor:
    """Extracts various types of data from web pages"""
    
    def __init__(self, config):
        self.config = config
    
    def extract_text_content(self, soup: BeautifulSoup, selectors: List[str]) -> List[Dict[str, Any]]:
        """
        Extract text content using provided selectors
        """
        extracted_data = []
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 10:  # Minimum text length
                    data = {
                        'type': 'text',
                        'selector': selector,
                        'content': text,
                        'tag': element.name,
                        'classes': element.get('class', []),
                        'id': element.get('id', ''),
                        'attributes': dict(element.attrs)
                    }
                    extracted_data.append(data)
        
        return extracted_data
    
    def extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """
        Extract image information
        """
        images = []
        
        for img in soup.find_all('img'):
            src = img.get('src', '')
            alt = img.get('alt', '')
            title = img.get('title', '')
            
            if src:
                # Make relative URLs absolute
                if not src.startswith(('http://', 'https://')):
                    src = urljoin(base_url, src)
                
                image_data = {
                    'type': 'image',
                    'src': src,
                    'alt': alt,
                    'title': title,
                    'width': img.get('width', ''),
                    'height': img.get('height', ''),
                    'classes': img.get('class', []),
                    'id': img.get('id', ''),
                    'attributes': dict(img.attrs)
                }
                images.append(image_data)
        
        return images
    
    def extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """
        Extract link information
        """
        links = []
        
        for link in soup.find_all('a'):
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            if href:
                # Make relative URLs absolute
                if not href.startswith(('http://', 'https://')):
                    href = urljoin(base_url, href)
                
                link_data = {
                    'type': 'link',
                    'href': href,
                    'text': text,
                    'title': link.get('title', ''),
                    'target': link.get('target', ''),
                    'classes': link.get('class', []),
                    'id': link.get('id', ''),
                    'attributes': dict(link.attrs)
                }
                links.append(link_data)
        
        return links
    
    def extract_structured_data(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract structured data (JSON-LD, Microdata, etc.)
        """
        structured_data = []
        
        # Extract JSON-LD
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                structured_data.append({
                    'type': 'json-ld',
                    'data': data
                })
            except (json.JSONDecodeError, TypeError):
                continue
        
        # Extract Microdata
        microdata_elements = soup.find_all(attrs={'itemtype': True})
        for element in microdata_elements:
            microdata = {
                'type': 'microdata',
                'itemtype': element.get('itemtype', ''),
                'itemid': element.get('itemid', ''),
                'itemscope': element.get('itemscope', ''),
                'properties': {}
            }
            
            # Extract properties
            for prop in element.find_all(attrs={'itemprop': True}):
                prop_name = prop.get('itemprop', '')
                prop_value = prop.get_text(strip=True) or prop.get('content', '')
                if prop_name and prop_value:
                    microdata['properties'][prop_name] = prop_value
            
            if microdata['properties']:
                structured_data.append(microdata)
        
        return structured_data
    
    def extract_tables(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract table data
        """
        tables = []
        
        for table in soup.find_all('table'):
            table_data = {
                'type': 'table',
                'headers': [],
                'rows': [],
                'classes': table.get('class', []),
                'id': table.get('id', '')
            }
            
            # Extract headers
            headers = table.find_all(['th', 'td'])
            if headers:
                table_data['headers'] = [h.get_text(strip=True) for h in headers[:len(headers)//2]]
            
            # Extract rows
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if cells:
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    table_data['rows'].append(row_data)
            
            if table_data['rows']:
                tables.append(table_data)
        
        return tables
    
    def extract_forms(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract form information
        """
        forms = []
        
        for form in soup.find_all('form'):
            form_data = {
                'type': 'form',
                'action': form.get('action', ''),
                'method': form.get('method', 'get'),
                'id': form.get('id', ''),
                'classes': form.get('class', []),
                'fields': []
            }
            
            # Extract form fields
            for field in form.find_all(['input', 'textarea', 'select']):
                field_data = {
                    'type': field.name,
                    'name': field.get('name', ''),
                    'id': field.get('id', ''),
                    'value': field.get('value', ''),
                    'placeholder': field.get('placeholder', ''),
                    'required': field.get('required', False),
                    'classes': field.get('class', [])
                }
                
                if field.name == 'select':
                    options = []
                    for option in field.find_all('option'):
                        options.append({
                            'value': option.get('value', ''),
                            'text': option.get_text(strip=True)
                        })
                    field_data['options'] = options
                
                form_data['fields'].append(field_data)
            
            forms.append(form_data)
        
        return forms
    
    def extract_metadata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract page metadata
        """
        metadata = {
            'type': 'metadata',
            'title': '',
            'description': '',
            'keywords': '',
            'author': '',
            'language': '',
            'charset': '',
            'viewport': '',
            'robots': '',
            'canonical': '',
            'og_tags': {},
            'twitter_tags': {}
        }
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text(strip=True)
        
        # Extract meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            property = meta.get('property', '').lower()
            content = meta.get('content', '')
            
            if name == 'description':
                metadata['description'] = content
            elif name == 'keywords':
                metadata['keywords'] = content
            elif name == 'author':
                metadata['author'] = content
            elif name == 'robots':
                metadata['robots'] = content
            elif name == 'viewport':
                metadata['viewport'] = content
            elif property.startswith('og:'):
                metadata['og_tags'][property] = content
            elif property.startswith('twitter:'):
                metadata['twitter_tags'][property] = content
        
        # Extract charset
        charset_meta = soup.find('meta', charset=True)
        if charset_meta:
            metadata['charset'] = charset_meta.get('charset', '')
        
        # Extract canonical URL
        canonical = soup.find('link', rel='canonical')
        if canonical:
            metadata['canonical'] = canonical.get('href', '')
        
        return metadata
    
    def extract_navigation(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """
        Extract navigation menu structure
        """
        navigation = []
        
        # Find navigation elements
        nav_elements = soup.find_all(['nav', 'menu', 'ul', 'ol'])
        
        for nav in nav_elements:
            nav_data = {
                'type': 'navigation',
                'tag': nav.name,
                'classes': nav.get('class', []),
                'id': nav.get('id', ''),
                'items': []
            }
            
            # Extract navigation items
            for item in nav.find_all('a'):
                href = item.get('href', '')
                text = item.get_text(strip=True)
                
                if href and text:
                    if not href.startswith(('http://', 'https://')):
                        href = urljoin(base_url, href)
                    
                    nav_data['items'].append({
                        'text': text,
                        'href': href,
                        'title': item.get('title', ''),
                        'target': item.get('target', '')
                    })
            
            if nav_data['items']:
                navigation.append(nav_data)
        
        return navigation
    
    def extract_all(self, soup: BeautifulSoup, base_url: str, selectors: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Extract all types of data from a page
        """
        extraction_result = {
            'url': base_url,
            'timestamp': None,
            'metadata': {},
            'text_content': [],
            'images': [],
            'links': [],
            'structured_data': [],
            'tables': [],
            'forms': [],
            'navigation': [],
            'summary': {}
        }
        
        try:
            # Extract metadata first
            extraction_result['metadata'] = self.extract_metadata(soup)
            
            # Extract text content
            if 'content' in selectors:
                extraction_result['text_content'] = self.extract_text_content(soup, selectors['content'])
            
            # Extract images
            extraction_result['images'] = self.extract_images(soup, base_url)
            
            # Extract links
            extraction_result['links'] = self.extract_links(soup, base_url)
            
            # Extract structured data
            extraction_result['structured_data'] = self.extract_structured_data(soup)
            
            # Extract tables
            extraction_result['tables'] = self.extract_tables(soup)
            
            # Extract forms
            extraction_result['forms'] = self.extract_forms(soup)
            
            # Extract navigation
            extraction_result['navigation'] = self.extract_navigation(soup, base_url)
            
            # Generate summary
            extraction_result['summary'] = {
                'text_items': len(extraction_result['text_content']),
                'images': len(extraction_result['images']),
                'links': len(extraction_result['links']),
                'structured_data_items': len(extraction_result['structured_data']),
                'tables': len(extraction_result['tables']),
                'forms': len(extraction_result['forms']),
                'navigation_menus': len(extraction_result['navigation'])
            }
            
            logger.info(f"Extracted {extraction_result['summary']['text_items']} text items, "
                       f"{extraction_result['summary']['images']} images, "
                       f"{extraction_result['summary']['links']} links from {base_url}")
            
        except Exception as e:
            logger.error(f"Error extracting data from {base_url}: {e}")
            extraction_result['error'] = str(e)
        
        return extraction_result 