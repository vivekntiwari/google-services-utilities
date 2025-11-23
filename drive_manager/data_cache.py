"""
Data Cache Module

Handles caching of Google Drive file metadata to avoid repeated API calls.
Stores data in JSON format for fast subsequent runs.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class DataCache:
    """Manages local cache of Google Drive file metadata"""
    
    def __init__(self, cache_file='drive_cache.json'):
        """
        Initialize the data cache.
        
        Args:
            cache_file: Path to cache file
        """
        self.cache_file = cache_file
        
    def save_files(self, files: List[Dict], metadata: Optional[Dict] = None):
        """
        Save file metadata to cache.
        
        Args:
            files: List of file dictionaries from Google Drive API
            metadata: Optional metadata about the cache (e.g., fetch time)
        """
        cache_data = {
            'metadata': metadata or {
                'fetched_at': datetime.now().isoformat(),
                'total_files': len(files)
            },
            'files': files
        }
        
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            print(f"✅ Cached {len(files)} files to {self.cache_file}")
        except Exception as e:
            print(f"❌ Error saving cache: {e}")
    
    def load_files(self) -> Optional[List[Dict]]:
        """
        Load file metadata from cache.
        
        Returns:
            List of file dictionaries, or None if cache doesn't exist
        """
        if not os.path.exists(self.cache_file):
            return None
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            files = cache_data.get('files', [])
            metadata = cache_data.get('metadata', {})
            
            fetched_at = metadata.get('fetched_at', 'Unknown')
            total_files = metadata.get('total_files', len(files))
            
            print(f"📦 Loaded {total_files} files from cache")
            print(f"   Last fetched: {fetched_at}")
            
            return files
        except Exception as e:
            print(f"❌ Error loading cache: {e}")
            return None
    
    def cache_exists(self) -> bool:
        """Check if cache file exists"""
        return os.path.exists(self.cache_file)
    
    def get_cache_age(self) -> Optional[str]:
        """
        Get the age of the cache.
        
        Returns:
            Human-readable cache age string, or None if cache doesn't exist
        """
        if not self.cache_exists():
            return None
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            fetched_at_str = cache_data.get('metadata', {}).get('fetched_at')
            if not fetched_at_str:
                return "Unknown"
            
            fetched_at = datetime.fromisoformat(fetched_at_str)
            age = datetime.now() - fetched_at
            
            if age.days > 0:
                return f"{age.days} day{'s' if age.days != 1 else ''} ago"
            elif age.seconds > 3600:
                hours = age.seconds // 3600
                return f"{hours} hour{'s' if hours != 1 else ''} ago"
            elif age.seconds > 60:
                minutes = age.seconds // 60
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            else:
                return "Just now"
        except Exception:
            return "Unknown"
    
    def delete_cache(self):
        """Delete the cache file"""
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
            print(f"🗑️  Deleted cache file: {self.cache_file}")
        else:
            print("No cache file to delete")
