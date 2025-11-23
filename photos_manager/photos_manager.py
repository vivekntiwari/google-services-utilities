#!/usr/bin/env python3
"""
Google Photos Manager

A CLI application to analyze Google Photos:
- Find top 100 largest photos/videos
- Detect duplicate photos/videos by filename and size
"""

import sys
import csv
import json
from datetime import datetime
from tabulate import tabulate
from photos_auth_handler import PhotosAuthHandler
from photos_analyzer import PhotosAnalyzer


def print_header():
    """Print application header"""
    print("\n" + "="*60)
    print("         Google Photos Manager")
    print("="*60)


def print_menu(cache_age=None):
    """Print main menu options"""
    print("\nOptions:")
    print("  1. Find top 100 largest photos/videos")
    print("  2. Find duplicate photos/videos")
    print("  3. Refresh data from Google Photos")
    if cache_age:
        print(f"  4. View cache info (Last updated: {cache_age})")
    else:
        print("  4. View cache info")
    print("  5. Exit")
    print()


def display_largest_items(analyzer: PhotosAnalyzer):
    """Display the largest photos/videos in a formatted table"""
    print("\n🔍 Finding largest photos/videos...")
    largest_items = analyzer.find_largest_items(limit=100)
    
    if not largest_items:
        print("No items found.")
        return
    
    # Prepare table data
    table_data = []
    for i, item in enumerate(largest_items, 1):
        filename = item.get('filename', 'Unknown')
        dimensions = PhotosAnalyzer.format_dimensions(
            item.get('width', 0), 
            item.get('height', 0)
        )
        size = PhotosAnalyzer.format_size(item.get('estimated_size', 0))
        creation_time = item.get('creationTime', 'N/A')
        
        # Format creation time
        if creation_time != 'N/A':
            try:
                dt = datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
                creation_time = dt.strftime('%Y-%m-%d %H:%M')
            except:
                pass
        
        # Truncate filename if too long
        if len(filename) > 40:
            filename = filename[:37] + "..."
        
        table_data.append([i, filename, dimensions, size, creation_time])
    
    # Display table
    headers = ["#", "Filename", "Dimensions", "Size", "Created"]
    print("\n" + "="*100)
    print(f"Top {len(largest_items)} Largest Photos/Videos")
    print("="*100)
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Offer export
    export = input("\nExport to CSV? (y/n): ").strip().lower()
    if export == 'y':
        export_largest_to_csv(largest_items)


def display_duplicate_items(analyzer: PhotosAnalyzer):
    """Display duplicate photos/videos grouped by filename"""
    print("\n🔍 Finding duplicate photos/videos (same filename AND size)...")
    duplicates = analyzer.find_duplicate_items()
    
    if not duplicates:
        print("No duplicate photos/videos found (same filename AND size).")
        return
    
    # Sort by number of duplicates (most duplicates first)
    sorted_duplicates = sorted(
        duplicates.items(), 
        key=lambda x: len(x[1]), 
        reverse=True
    )
    
    print("\n" + "="*100)
    print(f"Found {len(duplicates)} filenames with duplicates")
    print("="*100)
    
    for filename, items in sorted_duplicates:
        print(f"\n📷 '{filename}' ({len(items)} copies)")
        print("-" * 100)
        
        table_data = []
        for item in items:
            dimensions = PhotosAnalyzer.format_dimensions(
                item.get('width', 0), 
                item.get('height', 0)
            )
            size = PhotosAnalyzer.format_size(item.get('estimated_size', 0))
            created = item.get('creationTime', 'N/A')
            
            # Format creation time
            if created != 'N/A':
                try:
                    dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    created = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    pass
            
            table_data.append([dimensions, size, created])
        
        headers = ["Dimensions", "Size", "Created"]
        print(tabulate(table_data, headers=headers, tablefmt="simple"))
    
    # Offer export
    export = input("\nExport to JSON? (y/n): ").strip().lower()
    if export == 'y':
        export_duplicates_to_json(duplicates)


def export_largest_to_csv(items):
    """Export largest items to CSV"""
    filename = f"largest_photos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Rank', 'Filename', 'Dimensions', 'Size (pixels)', 'Created', 'URL'])
            
            for i, item in enumerate(items, 1):
                writer.writerow([
                    i,
                    item.get('filename', 'Unknown'),
                    PhotosAnalyzer.format_dimensions(item.get('width', 0), item.get('height', 0)),
                    item.get('estimated_size', 0),
                    item.get('creationTime', 'N/A'),
                    item.get('productUrl', 'N/A')
                ])
        
        print(f"✅ Exported to {filename}")
    except Exception as e:
        print(f"❌ Error exporting: {e}")


def export_duplicates_to_json(duplicates):
    """Export duplicate items to JSON"""
    filename = f"duplicate_photos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        # Convert to serializable format
        export_data = {}
        for name, items in duplicates.items():
            export_data[name] = [
                {
                    'id': item.get('id'),
                    'filename': item.get('filename'),
                    'dimensions': PhotosAnalyzer.format_dimensions(
                        item.get('width', 0), 
                        item.get('height', 0)
                    ),
                    'size': item.get('estimated_size'),
                    'created': item.get('creationTime'),
                    'url': item.get('productUrl')
                }
                for item in items
            ]
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(export_data, jsonfile, indent=2)
        
        print(f"✅ Exported to {filename}")
    except Exception as e:
        print(f"❌ Error exporting: {e}")


def show_cache_info(analyzer: PhotosAnalyzer):
    """Display cache information"""
    print("\n📊 Cache Information")
    print("=" * 60)
    
    if not analyzer.cache.cache_exists():
        print("❌ No cache file found")
        print("   Run option 3 to fetch data and create cache")
        return
    
    cache_age = analyzer.cache.get_cache_age()
    print(f"📁 Cache file: {analyzer.cache.cache_file}")
    print(f"⏰ Last updated: {cache_age}")
    
    # Load cache to get item count
    items = analyzer.cache.load_files()
    if items:
        print(f"📦 Total items cached: {len(items)}")
        
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
        auth_handler = PhotosAuthHandler()
        service = auth_handler.authenticate()
        print("✅ Successfully connected to Google Photos")
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        sys.exit(1)
    
    # Initialize analyzer
    analyzer = PhotosAnalyzer(service)
    
    # Check for existing cache
    cache_age = analyzer.cache.get_cache_age()
    if cache_age:
        print(f"\n💡 Found cached data from {cache_age}")
        print("   Using cache for faster analysis. Choose option 3 to refresh.")
    
    # Main loop
    while True:
        print_menu(cache_age)
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            display_largest_items(analyzer)
        elif choice == '2':
            display_duplicate_items(analyzer)
        elif choice == '3':
            print("\n🔄 Refreshing data from Google Photos...")
            analyzer.get_all_items(use_cache=False, refresh=True)
            cache_age = analyzer.cache.get_cache_age()
            print("✅ Data refreshed and cache updated")
        elif choice == '4':
            show_cache_info(analyzer)
        elif choice == '5':
            print("\n👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
