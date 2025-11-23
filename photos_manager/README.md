# Google Photos Manager

A Python CLI application to analyze your Google Photos library.

## Features

- 📊 **Find Largest Photos/Videos** - Identify your top 100 largest media items by dimensions
- 🔍 **Detect Duplicates** - Find duplicate photos/videos by filename AND size
- 💾 **Smart Caching** - Cache metadata locally to avoid repeated API calls
- 📤 **Export Results** - Export findings to CSV or JSON formats

## Setup

### 1. Install Dependencies

```bash
cd photos_manager
pip install -r requirements.txt
```

### 2. Get Google Photos API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Photos Library API**
4. Go to **Credentials** → **Create Credentials** → **OAuth client ID**
5. Choose **Desktop app** as the application type
6. Download the credentials JSON file
7. Save it as `photos_credentials.json` in the `photos_manager` directory

## Usage

Run the Photos Manager:

```bash
cd photos_manager
python photos_manager.py
```

### First Run

On first run, the application will:
1. Open your browser for OAuth authentication
2. Ask you to grant access to your Google Photos (read-only)
3. Save the authentication token as `photos_token.json`

### Menu Options

1. **Find top 100 largest photos/videos** - Shows your largest media items with dimensions and creation dates
2. **Find duplicate photos/videos** - Detects duplicates by matching both filename and size
3. **Refresh data from Google Photos** - Fetches latest data from API and updates cache
4. **View cache info** - Shows cache statistics and last update time
5. **Exit** - Close the application

### Export Options

After viewing results, you can export:
- **Largest items** → CSV file with rankings and metadata
- **Duplicates** → JSON file with grouped duplicates

## Files Created

- `photos_token.json` - OAuth authentication token (auto-generated)
- `photos_cache.json` - Cached photo metadata (auto-generated)
- `photos_credentials.json` - OAuth credentials (you provide this)
- `largest_photos_*.csv` - Exported largest items reports
- `duplicate_photos_*.json` - Exported duplicate reports

## Important Notes

⚠️ **API Limitation**: Google Photos API has restrictions effective March 31, 2025. After this date, the Library API will only access photos/videos uploaded by your application. This tool works with your existing library before that deadline.

🔒 **Privacy**: This application only requests read-only access to your Google Photos. Your photos are never uploaded or modified.

💡 **Size Estimation**: Google Photos API doesn't provide file sizes directly. The app estimates size based on dimensions (width × height × 3 bytes per pixel). This is a rough approximation but useful for comparison.
