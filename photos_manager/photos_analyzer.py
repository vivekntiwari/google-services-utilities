"""
Google Photos Analyzer

Analyzes Google Photos to find largest items and duplicates.
Similar to FileAnalyzer but adapted for Google Photos API.
"""

from typing import List, Dict, Optional
from collections import defaultdict
from photos_cache import PhotosCache


class PhotosAnalyzer:
    """Analyzes Google Photos items"""
    
    def __init__(self, service=None, cache_file='photos_cache.json'):
        """
        Initialize the photos analyzer.
        
        Args:
            service: Authenticated Google Photos API service object (optional if using cache)
            cache_file: Path to cache file for storing/loading metadata
        """
        self.service = service
        self.all_items = []
        self.cache = PhotosCache(cache_file)
        
    def fetch_from_photos(self, save_to_cache=True) -> List[Dict]:
        """
        Fetch all photos and videos from Google Photos API with pagination.
        
        Args:
            save_to_cache: Whether to save fetched data to cache
            
        Returns:
            List of media item dictionaries with metadata
        """
        if not self.service:
            raise ValueError("Google Photos service is required to fetch from API")
        
        print("🔄 Fetching media items from Google Photos API...")
        items = []
        page_token = None
        
        try:
            while True:
                # Request media items with pagination
                if page_token:
                    response = self.service.mediaItems().list(
                        pageSize=100,  # Max allowed per request
                        pageToken=page_token
                    ).execute()
                else:
                    response = self.service.mediaItems().list(
                        pageSize=100
                    ).execute()
                
                batch = response.get('mediaItems', [])
                
                # Extract relevant metadata from each item
                for item in batch:
                    metadata = item.get('mediaMetadata', {})
                    
                    # Determine size - Photos API doesn't always provide size directly
                    # We'll use width * height as a proxy, or mark as unknown
                    width = int(metadata.get('width', 0))
                    height = int(metadata.get('height', 0))
                    
                    # Estimate size based on dimensions (rough approximation)
                    # This is not perfect but gives us something to work with
                    estimated_size = width * height * 3 if width and height else 0
                    
                    processed_item = {
                        'id': item.get('id'),
                        'filename': item.get('filename', 'Unknown'),
                        'mimeType': item.get('mimeType', ''),
                        'productUrl': item.get('productUrl', ''),
                        'baseUrl': item.get('baseUrl', ''),
                        'creationTime': metadata.get('creationTime', ''),
                        'width': width,
                        'height': height,
                        'estimated_size': estimated_size,
                        'photo': metadata.get('photo', {}),
                        'video': metadata.get('video', {})
                    }
                    
                    items.append(processed_item)
                
                page_token = response.get('nextPageToken')
                print(f"  Retrieved {len(items)} items so far...")
                
                if not page_token:
                    break
                    
        except Exception as e:
            print(f"❌ Error fetching items: {e}")
            return items
        
        print(f"✅ Total items retrieved: {len(items)}")
        
        # Save to cache if requested
        if save_to_cache and items:
            self.cache.save_files(items)
        
        self.all_items = items
        return items
    
    def load_from_cache(self) -> Optional[List[Dict]]:
        """
        Load items from cache instead of fetching from API.
        
        Returns:
            List of item dictionaries, or None if cache doesn't exist
        """
        items = self.cache.load_files()
        if items:
            self.all_items = items
        return items
    
    def get_all_items(self, use_cache=True, refresh=False) -> List[Dict]:
        """
        Get all items - from cache if available, otherwise from API.
        
        Args:
            use_cache: Whether to use cached data if available
            refresh: Force refresh from API even if cache exists
            
        Returns:
            List of item dictionaries with metadata
        """
        # Force refresh from API
        if refresh:
            return self.fetch_from_photos(save_to_cache=True)
        
        # Try cache first if enabled
        if use_cache and self.cache.cache_exists():
            items = self.load_from_cache()
            if items:
                return items
        
        # Fall back to API fetch
        return self.fetch_from_photos(save_to_cache=True)
    
    def find_largest_items(self, limit=100) -> List[Dict]:
        """
        Find the largest photos/videos by dimensions.
        
        Args:
            limit: Number of largest items to return (default: 100)
            
        Returns:
            List of item dictionaries sorted by size (largest first)
        """
        if not self.all_items:
            self.get_all_items()
        
        # Filter items that have dimensions
        items_with_size = [
            item for item in self.all_items 
            if item.get('estimated_size', 0) > 0
        ]
        
        # Sort by estimated size descending
        sorted_items = sorted(
            items_with_size, 
            key=lambda x: x.get('estimated_size', 0), 
            reverse=True
        )
        
        return sorted_items[:limit]
    
    def find_duplicate_items(self) -> Dict[str, List[Dict]]:
        """
        Find photos/videos with duplicate filenames AND similar sizes.
        
        Returns:
            Dictionary mapping filenames to list of items with that name and similar size
            Only includes names that appear more than once with similar sizes
        """
        if not self.all_items:
            self.get_all_items()
        
        # Group items by filename AND estimated size (composite key)
        name_size_groups = defaultdict(list)
        for item in self.all_items:
            filename = item.get('filename', 'Unknown')
            size = item.get('estimated_size', 0)
            
            # Create composite key: filename + size
            key = f"{filename}|{size}"
            name_size_groups[key].append(item)
        
        # Filter to only duplicates (name+size appearing more than once)
        # Convert back to name-only keys for display
        duplicates = {}
        for key, items in name_size_groups.items():
            if len(items) > 1:
                filename = key.split('|')[0]  # Extract filename from composite key
                # If this filename already exists, append to it
                if filename in duplicates:
                    duplicates[filename].extend(items)
                else:
                    duplicates[filename] = items
        
        return duplicates
    
    @staticmethod
    def format_size(size_pixels: int) -> str:
        """
        Format size in human-readable format.
        For photos, this is based on pixel dimensions.
        
        Args:
            size_pixels: Estimated size in pixels
            
        Returns:
            Formatted size string
        """
        if size_pixels is None or size_pixels == 0:
            return "N/A"
        
        # Convert to megapixels
        megapixels = size_pixels / 1_000_000
        
        if megapixels < 1:
            return f"{size_pixels:,} px"
        elif megapixels < 1000:
            return f"{megapixels:.2f} MP"
        else:
            gigapixels = megapixels / 1000
            return f"{gigapixels:.2f} GP"
    
    @staticmethod
    def format_dimensions(width: int, height: int) -> str:
        """
        Format dimensions as WxH.
        
        Args:
            width: Width in pixels
            height: Height in pixels
            
        Returns:
            Formatted dimension string
        """
        if not width or not height:
            return "N/A"
        return f"{width}x{height}"
