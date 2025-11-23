"""
Google Services Dashboard - FastAPI Backend

Serves API endpoints for Drive and Photos data.
Also serves the built React frontend in production.
"""

import sys
import os
from typing import List, Dict
from pathlib import Path

# Add parent directory to path to import managers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import managers
from drive_manager.file_analyzer import FileAnalyzer
from drive_manager.data_cache import DataCache as DriveCache
from photos_manager.photos_analyzer import PhotosAnalyzer
from photos_manager.photos_cache import PhotosCache

app = FastAPI(title="Google Services Dashboard API")

# CORS middleware for development (React dev server on different port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and CRA defaults
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths to cache files
DRIVE_CACHE_PATH = os.path.join("drive_manager", "drive_cache.json")
PHOTOS_CACHE_PATH = os.path.join("photos_manager", "photos_cache.json")

# Initialize analyzers (cache-only mode)
drive_cache = DriveCache(DRIVE_CACHE_PATH)
photos_cache = PhotosCache(PHOTOS_CACHE_PATH)
drive_analyzer = FileAnalyzer(service=None, cache_file=DRIVE_CACHE_PATH)
photos_analyzer = PhotosAnalyzer(service=None, cache_file=PHOTOS_CACHE_PATH)


# API Endpoints
@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics"""
    drive_files = drive_analyzer.load_from_cache() or []
    photos_items = photos_analyzer.load_from_cache() or []
    
    return {
        "drive": {
            "count": len(drive_files),
            "age": drive_cache.get_cache_age() or "Unknown",
            "size": get_total_size(drive_files, "size")
        },
        "photos": {
            "count": len(photos_items),
            "age": photos_cache.get_cache_age() or "Unknown",
            "size": get_total_size(photos_items, "estimated_size")
        }
    }


@app.get("/api/drive/largest")
async def get_drive_largest(limit: int = 100):
    """Get largest Drive files"""
    try:
        files = drive_analyzer.find_largest_files(limit=limit)
        
        result = []
        for f in files:
            result.append({
                "name": f.get("name", "Unknown"),
                "path": f.get("folder_path", "/"),
                "size": f.get("size", 0),
                "size_fmt": drive_analyzer.format_size(f.get("size", 0)),
                "type": f.get("mimeType", ""),
                "link": f.get("webViewLink", "")
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/drive/duplicates")
async def get_drive_duplicates():
    """Get duplicate Drive files"""
    try:
        duplicates = drive_analyzer.find_duplicate_names()
        
        result = []
        for name, files in duplicates.items():
            group = {
                "name": name,
                "count": len(files),
                "size": files[0].get("size", 0),
                "size_fmt": drive_analyzer.format_size(files[0].get("size", 0)),
                "files": []
            }
            
            for f in files:
                group["files"].append({
                    "path": f.get("folder_path", "/"),
                    "modified": f.get("modifiedTime", ""),
                    "link": f.get("webViewLink", "")
                })
            
            result.append(group)
        
        # Sort by size descending
        result.sort(key=lambda x: x["size"], reverse=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/photos/largest")
async def get_photos_largest(limit: int = 100):
    """Get largest Photos items"""
    try:
        items = photos_analyzer.find_largest_items(limit=limit)
        
        result = []
        for item in items:
            result.append({
                "filename": item.get("filename", "Unknown"),
                "dimensions": photos_analyzer.format_dimensions(
                    item.get("width"), item.get("height")
                ),
                "size": item.get("estimated_size", 0),
                "size_fmt": photos_analyzer.format_size(item.get("estimated_size", 0)),
                "created": item.get("creationTime", ""),
                "url": item.get("productUrl", "")
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/photos/duplicates")
async def get_photos_duplicates():
    """Get duplicate Photos items"""
    try:
        duplicates = photos_analyzer.find_duplicate_items()
        
        result = []
        for name, items in duplicates.items():
            group = {
                "name": name,
                "count": len(items),
                "size": items[0].get("estimated_size", 0),
                "size_fmt": photos_analyzer.format_size(items[0].get("estimated_size", 0)),
                "files": []
            }
            
            for item in items:
                group["files"].append({
                    "dimensions": photos_analyzer.format_dimensions(
                        item.get("width"), item.get("height")
                    ),
                    "created": item.get("creationTime", ""),
                    "url": item.get("productUrl", "")
                })
            
            result.append(group)
        
        # Sort by size descending
        result.sort(key=lambda x: x["size"], reverse=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_total_size(items: List[Dict], size_key: str) -> str:
    """Calculate total size of items"""
    total = sum(int(item.get(size_key, 0) or 0) for item in items)
    return drive_analyzer.format_size(total)


# Serve React app in production
REACT_BUILD_DIR = Path(__file__).parent.parent / "web_ui" / "dist"

if REACT_BUILD_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(REACT_BUILD_DIR / "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        """Serve React app for all non-API routes"""
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404)
        
        file_path = REACT_BUILD_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        
        # Serve index.html for client-side routing
        return FileResponse(REACT_BUILD_DIR / "index.html")
