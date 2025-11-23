"""
Google Photos Cache Module

Extends DataCache for Google Photos metadata caching.
"""

import sys

# Handle imports based on how the module is being used
if __name__ == '__main__' or 'photos_manager' not in sys.modules:
    # Running standalone or from within photos_manager directory
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'drive_manager'))
    from data_cache import DataCache
else:
    # Being imported as part of photos_manager package
    from drive_manager.data_cache import DataCache


class PhotosCache(DataCache):
    """Manages local cache of Google Photos metadata"""
    
    def __init__(self, cache_file='photos_cache.json'):
        """
        Initialize the photos cache.
        
        Args:
            cache_file: Path to cache file (default: photos_cache.json)
        """
        super().__init__(cache_file)
