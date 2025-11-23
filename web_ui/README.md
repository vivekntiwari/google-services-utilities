# DriveUtility App

A modern React application for managing and analyzing Google Drive and Google Photos storage, built with the exact design from `design.txt`.

## Features

- **Dual Tab Interface**: Switch between Google Drive and Google Photos
- **Storage Analytics**: View stats on storage usage, file counts, and duplicates
- **Largest Files Detection**: Find the top 100 files consuming the most space
- **Duplicate Detection**: Identify duplicate files by name and size
- **Export Functionality**: Export data to CSV or JSON formats
- **Smart Caching**: Toggle caching for faster data retrieval
- **Real-time Progress**: Visual progress bars during scans

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Lucide React** - Icon library
- **FastAPI Backend** - Python backend at `http://localhost:8000`

## Getting Started

### Prerequisites

- Node.js 16+ installed
- FastAPI backend running on port 8000

### Installation

```bash
cd web_ui
npm install
```

### Development

```bash
npm run dev
```

The app will be available at **http://localhost:5173**

### Production Build

```bash
npm run build
npm run preview
```

## API Integration

The app connects to the FastAPI backend at `http://localhost:8000/api` with the following endpoints:

- `GET /api/stats` - Get Drive and Photos statistics
- `GET /api/drive/largest` - Get largest Drive files
- `GET /api/drive/duplicates` - Get Drive duplicates
- `GET /api/photos/largest` - Get largest Photos
- `GET /api/photos/duplicates` - Get Photos duplicates

### Mock Data Fallback

If the backend is unavailable, the app automatically falls back to mock data generators to ensure a smooth development experience.

## Design

This app implements the exact design specification from `design.txt`, featuring:

- Slate color palette (slate-50 to slate-900)
- Professional typography with Inter font
- Smooth animations and transitions
- Responsive grid layouts
- Interactive stat cards and action cards

## License

MIT
