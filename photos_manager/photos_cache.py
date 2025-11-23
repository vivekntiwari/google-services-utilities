"""
Photos Cache Module

Handles caching of Google Photos metadata to avoid repeated API calls.
Reuses DataCache class from data_cache.py with a different cache file.
"""

from data_cache import DataCache


class PhotosCache(DataCache):
    """Manages local cache of Google Photos metadata"""
    
    def __init__(self, cache_file='photos_cache.json'):
        """
        Initialize the photos cache.
        
        Args:
            cache_file: Path to cache file (default: photos_cache.json)
        """
        super().__init__(cache_file)
