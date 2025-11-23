# Google Drive Manager

A Python CLI application to analyze your Google Drive files.

## Features

- 📊 **Find Largest Files** - Identify your top 100 largest files
- 🔍 **Detect Duplicate Files** - Find duplicates by filename AND size
- 📁 **Find Duplicate Folders** - Identify folders with the same name
- 💾 **Smart Caching** - Cache metadata locally to avoid repeated API calls
- 📤 **Export Results** - Export findings to CSV or JSON formats
- 🗂️ **Folder Structure Export** - Export entire Drive structure to CSV

## Setup

### 1. Install Dependencies

```bash
cd drive_manager
pip install -r requirements.txt
```

### 2. Get Google Drive API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Drive API**
4. Go to **Credentials** → **Create Credentials** → **OAuth client ID**
5. Choose **Desktop app** as the application type
6. Download the credentials JSON file
7. Save it as `credentials.json` in the `drive_manager` directory

## Usage

### Drive Manager

Run the Drive Manager:

```bash
cd drive_manager
python drive_manager.py
```

#### Menu Options

1. **Find top 100 largest files** - Shows your largest files with sizes and folder paths
2. **Find duplicate files by name** - Detects duplicates by matching both filename and size
3. **Find duplicate folders** - Identifies folders with the same name
4. **Refresh data from Google Drive** - Fetches latest data from API and updates cache
5. **View cache info** - Shows cache statistics and last update time
6. **Exit** - Close the application

### Folder Structure Export

Export your entire Drive folder structure to CSV:

```bash
cd drive_manager
python export_folder_structure.py
```

This creates a CSV file with:
- Type (File/Folder)
- Full path
- Name
- Size (bytes and formatted)
- MIME type

## Files Created

- `token.json` - OAuth authentication token (auto-generated)
- `drive_cache.json` - Cached file metadata (auto-generated)
- `credentials.json` - OAuth credentials (you provide this)
- `largest_files_*.csv` - Exported largest files reports
- `duplicate_files_*.json` - Exported duplicate files reports
- `duplicate_folders_*.json` - Exported duplicate folders reports
- `drive_structure_*.csv` - Exported folder structure

## Privacy

🔒 This application only requests read-only access to your Google Drive. Your files are never uploaded, modified, or deleted.
