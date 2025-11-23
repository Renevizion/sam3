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

### Fastest Setup (Recommended)

Run the quick start script:
```bash
chmod +x quickstart.sh
./quickstart.sh
```

This will:
1. Check dependencies
2. Install all required packages
3. Build the frontend
4. Set up the environment

Then configure your environment:
```bash
cp .env.example .env
# Edit .env and add your HF_TOKEN
```

Start the application:
```bash
cd backend
python main.py
```

Access at `http://localhost:8000`

### Development Mode

To run both frontend and backend in development mode:
```bash
chmod +x dev.sh
./dev.sh
```

This starts:
- Backend at `http://localhost:8000`
- Frontend at `http://localhost:5173` (with hot reload)

### Manual Development Setup

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

**Using Docker Compose (Recommended):**

1. **Set environment variables**:
```bash
cp .env.example .env
# Edit .env and set your HF_TOKEN
```

2. **Start the container**:
```bash
docker-compose up -d
```

3. **Check status**:
```bash
docker-compose logs -f
```

**Using Docker directly:**

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

Configuration via environment variables or `.env` file:

- `HF_TOKEN`: Hugging Face token for model downloads (required)
- `KIE_API_KEY`: kie.ai API key (optional, for future features)
- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `8000`)
- `CUDA_VISIBLE_DEVICES`: GPU device ID (default: `0`)
- `FRONTEND_DIR`: Frontend build directory (default: `../frontend/dist`)
- `TEMP_DIR`: Temporary files directory (default: `/tmp`)
- `MAX_UPLOAD_SIZE`: Max file upload size in MB (default: `100`)
- `SCORE_THRESHOLD`: Detection score threshold (default: `0.5`)

Example `.env` file:
```bash
HF_TOKEN=hf_your_token_here
PORT=8000
CUDA_VISIBLE_DEVICES=0
SCORE_THRESHOLD=0.5
```

## Performance Optimizations

- **Lazy Loading**: Models are loaded only when first needed (not at startup)
- **Minimal Dependencies**: Only essential packages included
- **Efficient Processing**: Direct tensor operations without unnecessary conversions
- **Fast Frontend**: Vite for near-instant HMR and optimized builds
- **Configurable Thresholds**: Adjust score thresholds for speed/accuracy trade-off
- **GPU Acceleration**: CUDA support for fast inference
- **Static File Caching**: Frontend served efficiently from FastAPI

## Benchmarks

Approximate performance on NVIDIA A100:
- Image processing: ~2-5 seconds per image
- Video processing: ~30-60 seconds per minute of video
- Model loading: ~10-15 seconds (first request only)

## Troubleshooting

**Models not loading?**
- Ensure `HF_TOKEN` is set correctly
- Check Hugging Face access to facebook/sam3 model
- Verify CUDA is available: `python -c "import torch; print(torch.cuda.is_available())"`

**Frontend not showing?**
- Run `cd frontend && npm run build`
- Check `FRONTEND_DIR` in config
- Verify static files exist in `frontend/dist`

**Out of memory?**
- Reduce image/video size before upload
- Lower `SCORE_THRESHOLD` to get fewer detections
- Use CPU mode by setting `CUDA_VISIBLE_DEVICES=-1`

**Slow processing?**
- Ensure GPU is being used
- Models load on first request (expect delay)
- Consider reducing input resolution

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
