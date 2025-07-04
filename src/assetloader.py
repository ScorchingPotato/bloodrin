# assets.py - Simple AssetLoader class

import pygame
from pathlib import Path

class AssetLoader:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.loaded = False
        
        # Asset directory - handle both local and web paths
        try:
            # For local development
            self.assets_dir = Path(__file__).parent.parent / "assets" / "img"
        except:
            # Fallback for web/alternative contexts
            self.assets_dir = Path("assets/img")
        print(f"Assets directory: {self.assets_dir}")
    
    def load_all(self):
        """Load all assets - call after pygame.init()"""
        if self.loaded:
            return
        
        print("Loading assets...")
        
        # Define all your assets here
        asset_files = {
            'figurines': 'figurines.png',
            'enemies': 'enemies.png',
            'bloodbar': 'bloodbar.png',
            'enemybar': 'enemybar.png',
            'mouse-select': 'cursors/select.png',
            'mouse-grab': 'cursors/grab.png',
            'mouse-block': 'cursors/block.png',
            'mouse-attack': 'cursors/attack.png',
            'mouse-help': 'cursors/help.png',
        }
        
        # Load each asset
        for name, filename in asset_files.items():
            self._load_image(name, filename)
        
        self.loaded = True
        print("Assets loaded!")
    
    def _load_image(self, name, filename):
        """Load a single image"""
        try:
            # Try multiple path variations
            possible_paths = [
                Path("assets/img") / filename,  # From project root
                Path("../assets/img") / filename,  # One level up
                self.assets_dir / filename,  # Absolute path
                Path.cwd() / "assets" / "img" / filename  # Current working directory
            ]
            
            image = None
            for path in possible_paths:
                try:
                    if path.exists():
                        print(f"Attempting to load: {path}")
                        image = pygame.image.load(str(path.absolute()))
                        if image:
                            image = image.convert_alpha()
                            print(f"✓ Loaded: {name} from {path}")
                            break
                except pygame.error as e:
                    print(f"Failed attempt for {path}: {e}")
                    continue
            
            if image:
                self.images[name] = image
            else:
                print(f"⚠ Warning: {filename} not found in any location")
                # Create placeholder
                self.images[name] = pygame.Surface((32, 32))
                self.images[name].fill((255, 0, 255))  # Magenta placeholder
                
        except Exception as e:
            print(f"✗ Error loading {name}: {e}")
            # Create error placeholder
            self.images[name] = pygame.Surface((32, 32))
            self.images[name].fill((255, 0, 0))  # Red error
    
    def get(self, name):
        """Get an asset by name"""
        if not self.loaded:
            print("Warning: Assets not loaded yet!")
            return None
        return self.images.get(name)
    
    def __getitem__(self, name):
        """Allow dictionary-style access: assets['figurines']"""
        return self.get(name)

# Global instance
assets = AssetLoader()