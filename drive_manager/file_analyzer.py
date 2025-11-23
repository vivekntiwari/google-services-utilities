"""
Google Drive File Analyzer

Analyzes Google Drive files to find largest files and duplicates.
Separated into data fetching and analysis for caching support.
"""

from typing import List, Dict, Tuple, Optional
from collections import defaultdict
from data_cache import DataCache


class FileAnalyzer:
    """Analyzes Google Drive files"""
    
    def __init__(self, service=None, cache_file='drive_cache.json'):
        """
        Initialize the file analyzer.
        
        Args:
            service: Authenticated Google Drive API service object (optional if using cache)
            cache_file: Path to cache file for storing/loading metadata
        """
        self.service = service
        self.all_files = []
        self.cache = DataCache(cache_file)
        
    def fetch_from_drive(self, save_to_cache=True) -> List[Dict]:
        """
        Fetch all files from Google Drive API with pagination.
        This is the data fetching module - separated from analysis.
        Includes folder path building for better organization.
        
        Args:
            save_to_cache: Whether to save fetched data to cache
            
        Returns:
            List of file dictionaries with metadata including folder paths
        """
        if not self.service:
            raise ValueError("Google Drive service is required to fetch from API")
        
        print("🔄 Fetching files from Google Drive API...")
        files = []
        page_token = None
        
        try:
            while True:
                # Request files with specific fields including parents
                response = self.service.files().list(
                    pageSize=1000,  # Max allowed per request
                    fields="nextPageToken, files(id, name, size, mimeType, parents, modifiedTime, webViewLink)",
                    pageToken=page_token,
                    # Exclude trashed files
                    q="trashed=false"
                ).execute()
                
                batch = response.get('files', [])
                files.extend(batch)
                
                page_token = response.get('nextPageToken')
                print(f"  Retrieved {len(files)} files so far...")
                
                if not page_token:
                    break
                    
        except Exception as e:
            print(f"❌ Error fetching files: {e}")
            return files
        
        print(f"✅ Total files retrieved: {len(files)}")
        
        # Build folder structure map
        print("🗂️  Building folder structure...")
        folder_map = self._build_folder_map(files)
        
        # Add folder paths to each file
        for file in files:
            file['folder_path'] = self._get_folder_path(file, folder_map)
        
        print(f"✅ Folder structure complete")
        
        # Save to cache if requested
        if save_to_cache and files:
            self.cache.save_files(files)
        
        self.all_files = files
        return files
    
    def load_from_cache(self) -> Optional[List[Dict]]:
        """
        Load files from cache instead of fetching from API.
        
        Returns:
            List of file dictionaries, or None if cache doesn't exist
        """
        files = self.cache.load_files()
        if files:
            self.all_files = files
        return files
    
    def get_all_files(self, use_cache=True, refresh=False) -> List[Dict]:
        """
        Get all files - from cache if available, otherwise from API.
        
        Args:
            use_cache: Whether to use cached data if available
            refresh: Force refresh from API even if cache exists
            
        Returns:
            List of file dictionaries with metadata
        """
        # Force refresh from API
        if refresh:
            return self.fetch_from_drive(save_to_cache=True)
        
        # Try cache first if enabled
        if use_cache and self.cache.cache_exists():
            files = self.load_from_cache()
            if files:
                return files
        
        # Fall back to API fetch
        return self.fetch_from_drive(save_to_cache=True)
    
    def find_largest_files(self, limit=100) -> List[Dict]:
        """
        Find the largest files by size.
        
        Args:
            limit: Number of largest files to return (default: 100)
            
        Returns:
            List of file dictionaries sorted by size (largest first)
        """
        if not self.all_files:
            self.get_all_files()
        
        # Filter files that have a size (some items like folders don't)
        files_with_size = [
            f for f in self.all_files 
            if 'size' in f and f['size'] is not None
        ]
        
        # Convert size to int and sort
        for f in files_with_size:
            f['size'] = int(f['size'])
        
        # Sort by size descending
        sorted_files = sorted(files_with_size, key=lambda x: x['size'], reverse=True)
        
        return sorted_files[:limit]
    
    def find_duplicate_names(self) -> Dict[str, List[Dict]]:
        """
        Find files with duplicate names AND sizes.
        
        Returns:
            Dictionary mapping file names to list of files with that name and size
            Only includes names that appear more than once with the same size
        """
        if not self.all_files:
            self.get_all_files()
        
        # Group files by name AND size (composite key)
        name_size_groups = defaultdict(list)
        for file in self.all_files:
            # Skip folders and files without size
            if file.get('mimeType') == 'application/vnd.google-apps.folder':
                continue
            if 'size' not in file or file['size'] is None:
                continue
                
            name = file.get('name', 'Unknown')
            size = int(file.get('size', 0))
            # Create composite key: name + size
            key = f"{name}|{size}"
            name_size_groups[key].append(file)
        
        # Filter to only duplicates (name+size appearing more than once)
        # Convert back to name-only keys for display
        duplicates = {}
        for key, files in name_size_groups.items():
            if len(files) > 1:
                name = key.split('|')[0]  # Extract name from composite key
                # If this name already exists, append to it
                if name in duplicates:
                    duplicates[name].extend(files)
                else:
                    duplicates[name] = files
        
        return duplicates
    
    def _build_folder_map(self, files: List[Dict]) -> Dict[str, Dict]:
        """
        Build a map of all folders with their metadata.
        
        Args:
            files: List of all files and folders
            
        Returns:
            Dictionary mapping folder IDs to folder metadata
        """
        folder_map = {}
        
        # First pass: collect all folders
        for item in files:
            folder_map[item['id']] = {
                'name': item.get('name', 'Unknown'),
                'parents': item.get('parents', []),
                'is_folder': item.get('mimeType') == 'application/vnd.google-apps.folder'
            }
        
        return folder_map
    
    def _get_folder_path(self, file: Dict, folder_map: Dict[str, Dict]) -> str:
        """
        Get the full folder path for a file using the folder map.
        
        Args:
            file: File dictionary
            folder_map: Map of folder IDs to metadata
            
        Returns:
            Full folder path string (e.g., "/My Drive/Documents/Work")
        """
        if 'parents' not in file or not file['parents']:
            return "/My Drive"
        
        path_parts = []
        current_id = file['parents'][0]  # Use first parent
        max_depth = 20  # Prevent infinite loops
        
        for _ in range(max_depth):
            if current_id not in folder_map:
                break
            
            folder_info = folder_map[current_id]
            path_parts.insert(0, folder_info['name'])
            
            # Move to parent
            if folder_info['parents']:
                current_id = folder_info['parents'][0]
            else:
                break
        
        if path_parts:
            return "/My Drive/" + "/".join(path_parts)
        return "/My Drive"
    
    def find_duplicate_folders(self) -> Dict[str, List[Dict]]:
        """
        Find folders with duplicate names.
        
        Returns:
            Dictionary mapping folder names to list of folders with that name
            Only includes names that appear more than once
        """
        if not self.all_files:
            self.get_all_files()
        
        # Filter to only folders
        folders = [
            f for f in self.all_files
            if f.get('mimeType') == 'application/vnd.google-apps.folder'
        ]
        
        # Group folders by name
        name_groups = defaultdict(list)
        for folder in folders:
            name = folder.get('name', 'Unknown')
            name_groups[name].append(folder)
        
        # Filter to only duplicates
        duplicates = {
            name: folders
            for name, folders in name_groups.items()
            if len(folders) > 1
        }
        
        return duplicates
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """
        Format file size in human-readable format.
        
        Args:
            size_bytes: File size in bytes
            
        Returns:
            Formatted size string (e.g., "1.5 GB", "234 MB")
        """
        if size_bytes is None:
            return "N/A"
        
        # Convert to appropriate unit
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.2f} PB"
