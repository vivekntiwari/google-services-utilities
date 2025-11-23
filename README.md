# Google Services Utilities

A collection of Python CLI applications to manage and analyze your Google services.

## Projects

### 📁 [Drive Manager](./drive_manager/)

Analyze your Google Drive files:
- Find top 100 largest files
- Detect duplicate files (by name AND size)
- Find duplicate folders
- Export folder structure to CSV
- Smart caching for faster analysis

**Quick Start:**
```bash
cd drive_manager
python drive_manager.py
```

---

### 📷 [Photos Manager](./photos_manager/)

Analyze your Google Photos library:
- Find top 100 largest photos/videos
- Detect duplicate photos (by filename AND size)
- Smart caching for faster analysis
- Export results to CSV/JSON

**Quick Start:**
```bash
cd photos_manager
python photos_manager.py
```

---

## Setup

Each project has its own setup instructions in its respective README:
- [Drive Manager Setup](./drive_manager/README.md)
- [Photos Manager Setup](./photos_manager/README.md)

Both require OAuth credentials from Google Cloud Console.

## Features

Both applications share similar architecture:
- ✅ OAuth2 authentication
- ✅ Smart caching to reduce API calls
- ✅ Duplicate detection (name + size matching)
- ✅ Export functionality (CSV/JSON)
- ✅ Interactive CLI with formatted tables

## Privacy

🔒 Both applications only request **read-only** access to your data. Nothing is ever uploaded, modified, or deleted.
