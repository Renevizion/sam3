# SAM 3 Web Application - Quick Start Guide

## What This Application Does

This web application provides a user-friendly interface for SAM 3 (Segment Anything Model 3) to:
1. **Track objects in real-time** from your webcam
2. **Process video files** for batch tracking
3. **Visualize segmentation masks** overlaid on video streams

## Directory Structure

```
webapp/
├── README.md              # Comprehensive documentation
├── start.sh              # Script to start both frontend & backend
├── backend/              # Python/FastAPI backend
│   ├── main.py          # FastAPI application with WebSocket & REST endpoints
│   ├── run.py           # Backend startup script
│   ├── requirements.txt # Python dependencies
│   └── test_backend.py  # Backend tests
└── frontend/            # React/Vite frontend
    ├── src/
    │   ├── App.jsx      # Main React component
    │   └── App.css      # Styling
    ├── package.json     # Node dependencies
    └── ...
```

## Prerequisites Checklist

Before running the application, ensure you have:

- [ ] Python 3.12+ installed
- [ ] Node.js 18+ installed
- [ ] SAM 3 repository cloned and set up
- [ ] Access to SAM 3 weights on Hugging Face (optional for testing, required for actual tracking)
- [ ] Authenticated with Hugging Face CLI (if using real model)
- [ ] GPU with CUDA support (recommended for real-time performance)

## Installation Steps

### 1. Install SAM 3 Base Package

From the repository root:

```bash
# Create and activate conda environment
conda create -n sam3 python=3.12
conda activate sam3

# Install PyTorch with CUDA
pip install torch==2.7.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# Install SAM 3
pip install -e .
```

### 2. Install Backend Dependencies

```bash
cd webapp/backend
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies

```bash
cd webapp/frontend
npm install
```

## Running the Application

### Option 1: Start Both Servers with One Command (Recommended)

From the repository root:

```bash
./webapp/start.sh
```

This will:
- Start the backend on `http://localhost:8000`
- Start the frontend on `http://localhost:5173`
- Display logs from both servers
- Allow you to stop both with Ctrl+C

### Option 2: Start Servers Individually

**Terminal 1 - Backend:**
```bash
cd webapp/backend
python3 run.py
# Or directly: python3 main.py
```

**Terminal 2 - Frontend:**
```bash
cd webapp/frontend
npm run dev
```

## Using the Application

1. **Open your browser** to `http://localhost:5173`

2. **For Live Camera Tracking:**
   - Click the "📹 Live Camera" button
   - Grant camera permissions when prompted
   - Your webcam feed will appear with real-time SAM 3 tracking
   - Objects will be highlighted with green overlay masks

3. **For Video File Processing:**
   - Click the "📁 Upload Video" button
   - Select a video file (MP4, AVI, MOV, etc.)
   - The video will play in the canvas
   - A session will be created on the backend for tracking

## API Endpoints

The backend provides several endpoints:

- `GET /` - Root endpoint with API info
- `GET /health` - Health check and model status
- `WS /ws/track` - WebSocket for live frame streaming
- `POST /process-video` - Upload video files for processing
- `GET /docs` - Interactive API documentation (Swagger UI)

Visit `http://localhost:8000/docs` for interactive API documentation.

## Troubleshooting

### Backend Won't Start

**Issue:** Module not found errors
```bash
# Solution: Install dependencies
cd webapp/backend
pip install -r requirements.txt
```

**Issue:** SAM 3 model fails to load
- Make sure you've installed the base SAM 3 package: `pip install -e .` from repo root
- For testing without weights, the application will work but won't perform actual tracking
- For production use, authenticate with Hugging Face: `huggingface-cli login`

### Frontend Won't Start

**Issue:** Node modules not found
```bash
# Solution: Install dependencies
cd webapp/frontend
npm install
```

**Issue:** Build errors
```bash
# Solution: Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Camera Not Accessible

- **Grant Permissions:** Check browser settings to allow camera access
- **HTTPS Required:** Modern browsers require HTTPS for camera access (not needed for localhost)
- **Camera In Use:** Close other applications using the camera

### WebSocket Connection Failed

- **Backend Not Running:** Verify backend is running on port 8000
- **CORS Issues:** Check browser console for CORS errors
- **Firewall:** Ensure firewall allows connections to localhost:8000

## Performance Notes

- **Real-time tracking (30 FPS)** requires a powerful GPU (NVIDIA A100, H200, RTX 4090, etc.)
- **CPU-only mode** will work but at 1-5 FPS
- **Frame quality:** You can adjust JPEG quality in App.jsx (currently 0.5, range 0.0-1.0)
- **Resolution:** Lower camera resolution improves performance

## Development

### Running Tests

**Backend:**
```bash
cd webapp/backend
python3 test_backend.py
```

**Frontend:**
```bash
cd webapp/frontend
npm test
```

### Building for Production

**Frontend:**
```bash
cd webapp/frontend
npm run build
# Output will be in dist/ directory
```

**Backend:**
```bash
# Use gunicorn for production
pip install gunicorn
cd webapp/backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Technical Details

### WebSocket Protocol

The live tracking uses WebSocket for low-latency communication:

1. Frontend captures frame from webcam
2. Converts frame to JPEG and base64 encodes it
3. Sends to backend via WebSocket
4. Backend decodes, processes with SAM 3
5. Returns segmentation masks as JSON
6. Frontend draws masks over video

### Video Upload Flow

1. User selects video file
2. Frontend displays video locally
3. File uploads to backend via HTTP POST
4. Backend creates SAM 3 tracking session
5. Session can be used to add prompts and track objects

## Next Steps

1. **Add Prompt Interface:** Allow users to specify text prompts for tracking specific objects
2. **Save Results:** Export tracked videos with overlays
3. **Multiple Object Tracking:** Track and identify multiple objects with IDs
4. **Performance Metrics:** Display FPS and processing time
5. **Authentication:** Add user authentication for production deployment

## Support

For issues:
- SAM 3 Model: [GitHub Issues](https://github.com/facebookresearch/sam3/issues)
- Web Application: Open an issue in this repository
- Hugging Face Access: Contact Meta AI via Hugging Face

## License

Follows the SAM 3 license. See main repository LICENSE file.
