"""
Human behavior simulation for Hekate Universal Web Scraper
"""

import random
import time
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class HumanBehavior:
    """Simulates human-like behavior for anti-detection"""
    
    def __init__(self):
        self.mouse_movements = []
        self.scroll_patterns = []
        self.click_patterns = []
        self.typing_patterns = []
        
        self._setup_patterns()
    
    def _setup_patterns(self):
        """Setup realistic human behavior patterns"""
        # Mouse movement patterns (relative coordinates)
        self.mouse_movements = [
            [(0, 0), (10, 5), (20, 15), (30, 25)],  # Smooth diagonal
            [(0, 0), (5, 10), (15, 20), (25, 30)],  # Reverse diagonal
            [(0, 0), (15, 5), (25, 15), (35, 25)],  # Fast diagonal
            [(0, 0), (5, 15), (15, 25), (25, 35)],  # Slow diagonal
        ]
        
        # Scroll patterns (pixels per scroll)
        self.scroll_patterns = [
            [100, 150, 200, 250],  # Gradual increase
            [200, 150, 100, 50],   # Gradual decrease
            [150, 150, 150, 150],  # Consistent
            [50, 200, 100, 300],   # Random
        ]
        
        # Click patterns (delays in seconds)
        self.click_patterns = [
            [0.1, 0.3, 0.2, 0.4],  # Varied delays
            [0.2, 0.2, 0.2, 0.2],  # Consistent
            [0.5, 0.1, 0.3, 0.2],  # Mixed
            [0.1, 0.5, 0.1, 0.3],  # Alternating
        ]
        
        # Typing patterns (delays between characters)
        self.typing_patterns = [
            [0.1, 0.2, 0.1, 0.3, 0.1],  # Natural variation
            [0.15, 0.15, 0.15, 0.15],    # Consistent
            [0.05, 0.25, 0.1, 0.2],      # Fast then slow
            [0.2, 0.1, 0.3, 0.05],       # Slow then fast
        ]
    
    def simulate_mouse_movement(self, target_x: int, target_y: int) -> List[tuple]:
        """Simulate realistic mouse movement to target coordinates"""
        pattern = random.choice(self.mouse_movements)
        movements = []
        
        current_x, current_y = 0, 0
        for dx, dy in pattern:
            current_x += dx
            current_y += dy
            movements.append((current_x, current_y))
        
        # Ensure we reach the target
        if movements[-1] != (target_x, target_y):
            movements.append((target_x, target_y))
        
        logger.debug(f"Simulated mouse movement: {len(movements)} steps to ({target_x}, {target_y})")
        return movements
    
    def simulate_scroll(self, total_distance: int) -> List[int]:
        """Simulate realistic scrolling behavior"""
        pattern = random.choice(self.scroll_patterns)
        scrolls = []
        
        remaining = total_distance
        for scroll_amount in pattern:
            if remaining <= 0:
                break
            
            actual_scroll = min(scroll_amount, remaining)
            scrolls.append(actual_scroll)
            remaining -= actual_scroll
        
        logger.debug(f"Simulated scroll: {len(scrolls)} scrolls, total {sum(scrolls)}px")
        return scrolls
    
    def simulate_click_delays(self, num_clicks: int) -> List[float]:
        """Simulate realistic delays between clicks"""
        pattern = random.choice(self.click_patterns)
        delays = []
        
        for i in range(num_clicks):
            delay = pattern[i % len(pattern)]
            delays.append(delay)
        
        logger.debug(f"Simulated click delays: {delays}")
        return delays
    
    def simulate_typing(self, text: str) -> List[float]:
        """Simulate realistic typing behavior"""
        pattern = random.choice(self.typing_patterns)
        delays = []
        
        for i, char in enumerate(text):
            if char == ' ':
                delay = random.uniform(0.1, 0.3)  # Longer delay for spaces
            else:
                delay = pattern[i % len(pattern)]
            delays.append(delay)
        
        logger.debug(f"Simulated typing: {len(text)} chars, {len(delays)} delays")
        return delays
    
    def random_delay(self, min_delay: float = 0.5, max_delay: float = 2.0):
        """Add a random delay to simulate human thinking time"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        logger.debug(f"Applied random delay: {delay:.2f}s")
    
    def simulate_page_interaction(self, page_type: str = 'general'):
        """Simulate realistic page interaction based on page type"""
        if page_type == 'news':
            # News sites: quick scroll, read headlines
            scrolls = self.simulate_scroll(random.randint(500, 1500))
            for scroll in scrolls:
                time.sleep(random.uniform(0.1, 0.3))
            
        elif page_type == 'ecommerce':
            # E-commerce: slower browsing, product examination
            scrolls = self.simulate_scroll(random.randint(300, 800))
            for scroll in scrolls:
                time.sleep(random.uniform(0.3, 0.8))
            
        elif page_type == 'blog':
            # Blog: medium speed, reading behavior
            scrolls = self.simulate_scroll(random.randint(400, 1000))
            for scroll in scrolls:
                time.sleep(random.uniform(0.2, 0.5))
            
        else:
            # General: mixed behavior
            scrolls = self.simulate_scroll(random.randint(200, 800))
            for scroll in scrolls:
                time.sleep(random.uniform(0.1, 0.6))
        
        logger.debug(f"Simulated page interaction for {page_type} page")
    
    def get_behavior_profile(self) -> Dict[str, Any]:
        """Get current behavior simulation profile"""
        return {
            'mouse_movement_patterns': len(self.mouse_movements),
            'scroll_patterns': len(self.scroll_patterns),
            'click_patterns': len(self.click_patterns),
            'typing_patterns': len(self.typing_patterns),
            'realistic_delays': True,
            'human_like_interactions': True
        } 