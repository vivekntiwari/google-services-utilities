#!/usr/bin/env python3
"""
Google Drive File Manager

A CLI application to analyze Google Drive files:
- Find top 100 largest files
- Detect duplicate files by name
"""

import sys
import csv
import json
from datetime import datetime
from tabulate import tabulate
from auth_handler import DriveAuthHandler
from file_analyzer import FileAnalyzer


def print_header():
    """Print application header"""
    print("\n" + "="*60)
    print("           Google Drive File Manager")
    print("="*60)


def print_menu(cache_age=None):
    """Print main menu options"""
    print("\nOptions:")
    print("  1. Find top 100 largest files")
    print("  2. Find duplicate files by name")
    print("  3. Find duplicate folders")
    print("  4. Refresh data from Google Drive")
    if cache_age:
        print(f"  5. View cache info (Last updated: {cache_age})")
    else:
        print("  5. View cache info")
    print("  6. Exit")
    print()


def display_largest_files(analyzer: FileAnalyzer):
    """Display the largest files in a formatted table with folder paths"""
    print("\n🔍 Finding largest files...")
    largest_files = analyzer.find_largest_files(limit=100)
    
    if not largest_files:
        print("No files found.")
        return
    
    # Prepare table data
    table_data = []
    for i, file in enumerate(largest_files, 1):
        name = file.get('name', 'Unknown')
        size = FileAnalyzer.format_size(file.get('size', 0))
        folder_path = file.get('folder_path', '/My Drive')
        
        # Truncate name and path if too long
        if len(name) > 35:
            name = name[:32] + "..."
        if len(folder_path) > 40:
            folder_path = "..." + folder_path[-37:]
        
        table_data.append([i, name, size, folder_path])
    
    # Display table
    headers = ["#", "File Name", "Size", "Folder Path"]
    print("\n" + "="*120)
    print(f"Top {len(largest_files)} Largest Files")
    print("="*120)
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Calculate total size
    total_size = sum(f.get('size', 0) for f in largest_files)
    print(f"\nTotal size of top {len(largest_files)} files: {FileAnalyzer.format_size(total_size)}")
    
    # Offer export
    export = input("\nExport to CSV? (y/n): ").strip().lower()
    if export == 'y':
        export_largest_to_csv(largest_files)


def display_duplicate_files(analyzer: FileAnalyzer):
    """Display duplicate files grouped by name with folder paths"""
    print("\n🔍 Finding duplicate files (same name AND size)...")
    duplicates = analyzer.find_duplicate_names()
    
    if not duplicates:
        print("No duplicate files found (same name AND size).")
        return
    
    # Sort by number of duplicates (most duplicates first)
    sorted_duplicates = sorted(
        duplicates.items(), 
        key=lambda x: len(x[1]), 
        reverse=True
    )
    
    print("\n" + "="*120)
    print(f"Found {len(duplicates)} file names with duplicates")
    print("="*120)
    
    for name, files in sorted_duplicates:
        print(f"\n📄 '{name}' ({len(files)} copies)")
        print("-" * 120)
        
        table_data = []
        for file in files:
            size = FileAnalyzer.format_size(int(file.get('size', 0))) if 'size' in file else 'N/A'
            folder_path = file.get('folder_path', '/My Drive')
            modified = file.get('modifiedTime', 'N/A')
            
            # Format modified time
            if modified != 'N/A':
                try:
                    dt = datetime.fromisoformat(modified.replace('Z', '+00:00'))
                    modified = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    pass
            
            # Truncate folder path if too long
            if len(folder_path) > 50:
                folder_path = "..." + folder_path[-47:]
            
            table_data.append([size, folder_path, modified])
        
        headers = ["Size", "Folder Path", "Modified"]
        print(tabulate(table_data, headers=headers, tablefmt="simple"))
    
    # Offer export
    export = input("\nExport to JSON? (y/n): ").strip().lower()
    if export == 'y':
        export_duplicates_to_json(duplicates)


def display_duplicate_folders(analyzer: FileAnalyzer):
    """Display duplicate folders grouped by name with their paths"""
    print("\n🔍 Finding duplicate folders...")
    duplicates = analyzer.find_duplicate_folders()
    
    if not duplicates:
        print("No duplicate folder names found.")
        return
    
    # Sort by number of duplicates (most duplicates first)
    sorted_duplicates = sorted(
        duplicates.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )
    
    print("\n" + "="*120)
    print(f"Found {len(duplicates)} folder names with duplicates")
    print("="*120)
    
    for name, folders in sorted_duplicates:
        print(f"\n📁 '{name}' ({len(folders)} instances)")
        print("-" * 120)
        
        table_data = []
        for folder in folders:
            folder_path = folder.get('folder_path', '/My Drive')
            modified = folder.get('modifiedTime', 'N/A')
            
            # Format modified time
            if modified != 'N/A':
                try:
                    dt = datetime.fromisoformat(modified.replace('Z', '+00:00'))
                    modified = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    pass
            
            # Truncate folder path if too long
            display_path = folder_path
            if len(display_path) > 80:
                display_path = "..." + display_path[-77:]
            
            table_data.append([display_path, modified])
        
        headers = ["Full Path", "Modified"]
        print(tabulate(table_data, headers=headers, tablefmt="simple"))
    
    print(f"\n💡 Tip: Review these duplicate folders to consolidate your Drive organization")
    
    # Offer export
    export = input("\nExport to JSON? (y/n): ").strip().lower()
    if export == 'y':
        export_duplicate_folders_to_json(duplicates)


def export_largest_to_csv(files):
    """Export largest files to CSV"""
    filename = f"largest_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Rank', 'File Name', 'Size (Bytes)', 'Size (Formatted)', 'Link'])
            
            for i, file in enumerate(files, 1):
                writer.writerow([
                    i,
                    file.get('name', 'Unknown'),
                    file.get('size', 0),
                    FileAnalyzer.format_size(file.get('size', 0)),
                    file.get('webViewLink', 'N/A')
                ])
        
        print(f"✅ Exported to {filename}")
    except Exception as e:
        print(f"❌ Error exporting: {e}")


def export_duplicates_to_json(duplicates):
    """Export duplicate files to JSON"""
    filename = f"duplicate_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        # Convert to serializable format
        export_data = {}
        for name, files in duplicates.items():
            export_data[name] = [
                {
                    'id': f.get('id'),
                    'name': f.get('name'),
                    'size': f.get('size'),
                    'size_formatted': FileAnalyzer.format_size(int(f.get('size', 0))) if 'size' in f else 'N/A',
                    'modified': f.get('modifiedTime'),
                    'link': f.get('webViewLink')
                }
                for f in files
            ]
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(export_data, jsonfile, indent=2)
        
        print(f"✅ Exported to {filename}")
    except Exception as e:
        print(f"❌ Error exporting: {e}")


def export_duplicate_folders_to_json(duplicates):
    """Export duplicate folders to JSON"""
    filename = f"duplicate_folders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        # Convert to serializable format
        export_data = {}
        for name, folders in duplicates.items():
            export_data[name] = [
                {
                    'id': f.get('id'),
                    'name': f.get('name'),
                    'folder_path': f.get('folder_path', '/My Drive'),
                    'modified': f.get('modifiedTime'),
                    'link': f.get('webViewLink')
                }
                for f in folders
            ]
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(export_data, jsonfile, indent=2)
        
        print(f"✅ Exported to {filename}")
    except Exception as e:
        print(f"❌ Error exporting: {e}")


def show_cache_info(analyzer: FileAnalyzer):
    """Display cache information"""
    print("\n📊 Cache Information")
    print("=" * 60)
    
    if not analyzer.cache.cache_exists():
        print("❌ No cache file found")
        print("   Run option 1 or 2 to fetch data and create cache")
        return
    
    cache_age = analyzer.cache.get_cache_age()
    print(f"📁 Cache file: {analyzer.cache.cache_file}")
    print(f"⏰ Last updated: {cache_age}")
    
    # Load cache to get file count
    files = analyzer.cache.load_files()
    if files:
        print(f"📦 Total files cached: {len(files)}")
        
        # Calculate cache size
        import os
        cache_size = os.path.getsize(analyzer.cache.cache_file)
        cache_size_mb = cache_size / (1024 * 1024)
        print(f"💾 Cache file size: {cache_size_mb:.2f} MB")


def main():
    """Main application loop"""
    print_header()
    
    # Authenticate
    try:
        auth_handler = DriveAuthHandler()
        service = auth_handler.authenticate()
        print("✅ Successfully connected to Google Drive")
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        sys.exit(1)
    
    # Initialize analyzer
    analyzer = FileAnalyzer(service)
    
    # Check for existing cache
    cache_age = analyzer.cache.get_cache_age()
    if cache_age:
        print(f"\n💡 Found cached data from {cache_age}")
        print("   Using cache for faster analysis. Choose option 3 to refresh.")
    
    # Main loop
    while True:
        print_menu(cache_age)
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            display_largest_files(analyzer)
        elif choice == '2':
            display_duplicate_files(analyzer)
        elif choice == '3':
            display_duplicate_folders(analyzer)
        elif choice == '4':
            print("\n🔄 Refreshing data from Google Drive...")
            analyzer.get_all_files(use_cache=False, refresh=True)
            cache_age = analyzer.cache.get_cache_age()
            print("✅ Data refreshed and cache updated")
        elif choice == '5':
            show_cache_info(analyzer)
        elif choice == '6':
            print("\n👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
