# Google Services Dashboard

A modern React + FastAPI web application to review your Google Drive and Photos data.

## Features

- 📊 **Dashboard** - Overview of Drive and Photos statistics
- 📁 **Drive Review** - View largest files and duplicates
- 📷 **Photos Review** - Analyze photos and duplicates
- ⚡ **Fast** - Uses local cache for instant loading
- 🎨 **Modern UI** - Built with React and Tailwind CSS

## Architecture

- **Backend**: FastAPI (Python) - Serves API endpoints
- **Frontend**: React 18 + Vite - Modern, fast development
- **Styling**: Tailwind CSS - Utility-first CSS framework
- **Routing**: React Router v6 - Client-side routing

## Setup

### Prerequisites

- Python 3.x
- Node.js 18+
- npm

### Installation

1. **Install Backend Dependencies**
   ```bash
   pip install -r web_dashboard/requirements.txt
   ```

2. **Install Frontend Dependencies**
   ```bash
   cd web_ui
   npm install
   ```

## Development

Run both backend and frontend in development mode:

1. **Start Backend** (Terminal 1)
   ```bash
   uvicorn web_dashboard.app:app --reload
   ```
   Backend runs on: http://localhost:8000

2. **Start Frontend** (Terminal 2)
   ```bash
   cd web_ui
   npm run dev
   ```
   Frontend runs on: http://localhost:5173

The frontend will proxy API requests to the backend automatically.

## Production Build

1. **Build React App**
   ```bash
   cd web_ui
   npm run build
   ```

2. **Start Backend** (serves both API and React app)
   ```bash
   uvicorn web_dashboard.app:app
   ```

3. **Access** at http://localhost:8000

## Project Structure

```
Utilities/
├── web_dashboard/          # FastAPI Backend
│   ├── app.py             # API server
│   └── requirements.txt
└── web_ui/                # React Frontend
    ├── src/
    │   ├── components/    # Reusable components
    │   ├── pages/         # Page components
    │   ├── api.js         # API client
    │   └── App.jsx        # Main app
    ├── package.json
    └── vite.config.js
```

## API Endpoints

- `GET /api/stats` - Dashboard statistics
- `GET /api/drive/largest` - Largest Drive files
- `GET /api/drive/duplicates` - Duplicate Drive files
- `GET /api/photos/largest` - Largest Photos
- `GET /api/photos/duplicates` - Duplicate Photos
