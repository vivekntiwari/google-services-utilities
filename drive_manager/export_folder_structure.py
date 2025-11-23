"""
Export Folder Structure to CSV

Reads drive_cache.json and creates a CSV file with recursive folder structure,
showing file names and sizes at every level.
"""

import json
import csv
from datetime import datetime
from collections import defaultdict
from typing import List, Dict


def load_cache(cache_file='drive_cache.json') -> List[Dict]:
    """Load files from cache"""
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        return cache_data.get('files', [])
    except Exception as e:
        print(f"❌ Error loading cache: {e}")
        return []


def build_folder_hierarchy(files: List[Dict]) -> Dict:
    """Build a hierarchical folder structure"""
    # Create a mapping of folder IDs to their information
    folders = {}
    file_items = {}
    
    for item in files:
        item_id = item.get('id')
        item_name = item.get('name', 'Unnamed')
        item_type = item.get('mimeType', '')
        item_size = int(item.get('size', 0))
        parents = item.get('parents', [])
        
        if 'folder' in item_type:
            folders[item_id] = {
                'id': item_id,
                'name': item_name,
                'parents': parents,
                'children': [],
                'files': [],
                'total_size': 0
            }
        else:
            file_items[item_id] = {
                'id': item_id,
                'name': item_name,
                'size': item_size,
                'parents': parents,
                'mimeType': item_type
            }
    
    # Build parent-child relationships for folders
    for folder_id, folder_info in folders.items():
        for parent_id in folder_info['parents']:
            if parent_id in folders:
                folders[parent_id]['children'].append(folder_id)
    
    # Assign files to their parent folders
    for file_id, file_info in file_items.items():
        for parent_id in file_info['parents']:
            if parent_id in folders:
                folders[parent_id]['files'].append(file_info)
    
    return folders, file_items


def get_folder_path(folder_id: str, folders: Dict, path_cache: Dict = None) -> str:
    """Get the full path of a folder"""
    if path_cache is None:
        path_cache = {}
    
    if folder_id in path_cache:
        return path_cache[folder_id]
    
    if folder_id not in folders:
        return ""
    
    folder = folders[folder_id]
    folder_name = folder['name']
    
    # If no parents or parent is root, return just the folder name
    if not folder['parents']:
        path_cache[folder_id] = folder_name
        return folder_name
    
    # Get parent path
    parent_id = folder['parents'][0]
    parent_path = get_folder_path(parent_id, folders, path_cache)
    
    if parent_path:
        full_path = f"{parent_path}/{folder_name}"
    else:
        full_path = folder_name
    
    path_cache[folder_id] = full_path
    return full_path


def format_size(size_bytes: int) -> str:
    """Format size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def export_to_csv(files: List[Dict], output_file: str):
    """Export folder structure to CSV"""
    print("🔄 Building folder hierarchy...")
    folders, file_items = build_folder_hierarchy(files)
    
    print("🔄 Generating folder paths...")
    path_cache = {}
    
    # Prepare CSV data
    csv_data = []
    
    # Add all files with their folder paths
    for file_info in file_items.values():
        file_name = file_info['name']
        file_size = file_info['size']
        file_size_formatted = format_size(file_size)
        
        # Get folder path
        if file_info['parents']:
            parent_id = file_info['parents'][0]
            folder_path = get_folder_path(parent_id, folders, path_cache)
        else:
            folder_path = "/"
        
        csv_data.append({
            'Type': 'File',
            'Path': folder_path,
            'Name': file_name,
            'Size (Bytes)': file_size,
            'Size (Formatted)': file_size_formatted,
            'MIME Type': file_info.get('mimeType', '')
        })
    
    # Add all folders
    for folder_id, folder_info in folders.items():
        folder_name = folder_info['name']
        folder_path = get_folder_path(folder_id, folders, path_cache)
        
        # Calculate total size of files in this folder (direct children only)
        total_size = sum(f['size'] for f in folder_info['files'])
        
        csv_data.append({
            'Type': 'Folder',
            'Path': folder_path,
            'Name': folder_name,
            'Size (Bytes)': total_size,
            'Size (Formatted)': format_size(total_size),
            'MIME Type': 'application/vnd.google-apps.folder'
        })
    
    # Sort by path and name
    csv_data.sort(key=lambda x: (x['Path'], x['Type'], x['Name']))
    
    # Write to CSV
    print(f"📝 Writing to {output_file}...")
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Type', 'Path', 'Name', 'Size (Bytes)', 'Size (Formatted)', 'MIME Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"✅ Exported {len(csv_data)} items to {output_file}")
    print(f"   - {len(file_items)} files")
    print(f"   - {len(folders)} folders")


def main():
    """Main function"""
    print("📂 Google Drive Folder Structure Exporter")
    print("=" * 60)
    
    # Load cache
    files = load_cache()
    if not files:
        print("❌ No files found in cache")
        return
    
    print(f"📦 Loaded {len(files)} items from cache")
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"drive_structure_{timestamp}.csv"
    
    # Export to CSV
    export_to_csv(files, output_file)
    
    print("\n✨ Done!")


if __name__ == "__main__":
    main()
