# SAM3 Web Application

A fast and minimal web application for SAM3 (Segment Anything with Concepts) - optimized for low latency and ease of use.

## Features

- 🚀 **Fast & Lightweight**: Lazy model loading minimizes startup time
- 🎯 **Image Processing**: Segment objects in images using text prompts
- 🎥 **Video Processing**: Track and segment objects in videos
- 🌐 **Unified Server**: Single FastAPI server serves both API and frontend
- 🐳 **Docker Ready**: CUDA 12.6 support for GPU acceleration

## Architecture

- **Backend**: FastAPI with lazy-loaded SAM3 models
- **Frontend**: React + Vite for fast builds and development
- **Deployment**: Docker with NVIDIA CUDA support

## Quick Start

### Prerequisites

- Python 3.12
- Node.js 18+ (for frontend development)
- CUDA 12.6+ (for GPU acceleration)
- Hugging Face token (for model downloads)

### Development Setup

1. **Install SAM3 package**:
```bash
pip install -e .
```

2. **Set up backend**:
```bash
cd backend
pip install -r requirements.txt
```

3. **Set up frontend**:
```bash
cd frontend
npm install
```

4. **Run development servers**:

Backend (terminal 1):
```bash
cd backend
python main.py
```

Frontend (terminal 2):
```bash
cd frontend
npm run dev
```

Access the app at `http://localhost:5173`

### Production Build

1. **Build frontend**:
```bash
cd frontend
npm run build
```

2. **Update backend** to serve static files (uncomment the line in `main.py`):
```python
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
```

3. **Run unified server**:
```bash
cd backend
python main.py
```

Access the app at `http://localhost:8000`

### Docker Deployment

1. **Build Docker image**:
```bash
docker build -t sam3-app .
```

2. **Run container**:
```bash
docker run --gpus all -p 8000:8000 \
  -e HF_TOKEN=your_huggingface_token \
  sam3-app
```

## API Endpoints

### Health Check
```
GET /api/health
```

### Process Image
```
POST /api/process/image
Content-Type: multipart/form-data

Parameters:
- file: image file
- text_prompt: text description of objects to segment
```

### Process Video
```
POST /api/process/video
Content-Type: multipart/form-data

Parameters:
- file: video file
- text_prompt: text description of objects to track
```

## Environment Variables

- `HF_TOKEN`: Hugging Face token for model downloads (required)
- `KIE_API_KEY`: kie.ai API key (optional, for future features)

## Performance Optimizations

- **Lazy Loading**: Models are loaded only when first needed
- **Minimal Dependencies**: Only essential packages included
- **Efficient Processing**: Direct tensor operations without unnecessary conversions
- **Fast Frontend**: Vite for near-instant HMR and optimized builds

## Project Structure

```
sam3/
├── backend/
│   ├── main.py              # FastAPI server
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Styles
│   │   └── main.jsx        # Entry point
│   ├── index.html          # HTML template
│   ├── vite.config.js      # Vite configuration
│   └── package.json        # Node dependencies
├── Dockerfile              # Docker configuration
└── README_APP.md          # This file
```

## License

See [LICENSE](LICENSE) file.
