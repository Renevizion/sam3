# SAM 3 Web Application - Factory Monitor

A 2026-ready web application that enables real-time object tracking using SAM 3 (Segment Anything Model 3) for both live camera feeds and uploaded video files.

## Overview

This web application provides:
- **Live Camera Tracking**: Real-time object segmentation and tracking from your webcam
- **Video File Processing**: Upload and process video files with SAM 3 tracking
- **WebSocket Streaming**: Low-latency communication between frontend and backend
- **Interactive UI**: Modern React interface with visual feedback

## Architecture

### Backend (Python/FastAPI)
- **WebSocket endpoint** (`/ws/track`): Handles real-time camera frame streaming
- **REST endpoint** (`/process-video`): Processes uploaded video files
- **SAM 3 Integration**: Uses the SAM 3 video predictor for object tracking

### Frontend (React/Vite)
- **Camera Access**: Native browser webcam integration
- **Canvas Rendering**: Real-time visualization with mask overlays
- **File Upload**: Support for MP4, AVI, and other video formats
- **Dual Mode**: Toggle between live camera and video file playback

## Prerequisites

### System Requirements
- **Python**: 3.12 or higher
- **Node.js**: 18.0 or higher
- **PyTorch**: 2.7 or higher with CUDA 12.6+
- **GPU**: NVIDIA GPU (A100, H200, or equivalent) recommended for real-time tracking
- **RAM**: 16GB minimum, 32GB recommended

### Model Weights
⚠️ **Important**: You must request access to SAM 3 weights on Hugging Face before running the backend.

1. Visit the [SAM 3 Hugging Face repository](https://huggingface.co/facebook/sam3)
2. Request access to the model weights
3. Once approved, authenticate with Hugging Face CLI:
   ```bash
   pip install huggingface_hub
   huggingface-cli login
   ```

## Installation

### 1. Install SAM 3 Repository
```bash
# Clone the repository
git clone https://github.com/facebookresearch/sam3.git
cd sam3

# Create conda environment
conda create -n sam3 python=3.12
conda activate sam3

# Install PyTorch with CUDA support
pip install torch==2.7.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# Install SAM 3
pip install -e .
```

### 2. Setup Backend
```bash
cd webapp/backend

# Install backend dependencies
pip install -r requirements.txt
```

### 3. Setup Frontend
```bash
cd webapp/frontend

# Install frontend dependencies
npm install
```

## Running the Application

### Start Backend Server

From the `webapp/backend` directory:

```bash
python main.py
```

The backend will start on `http://localhost:8000`

**Verify the backend is running:**
```bash
curl http://localhost:8000/health
```

### Start Frontend Development Server

From the `webapp/frontend` directory:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

### Live Camera Tracking

1. Click the **"📹 Live Camera"** button
2. Grant camera permissions when prompted
3. The application will:
   - Stream frames from your webcam
   - Send frames to the SAM 3 backend via WebSocket
   - Display segmentation masks overlaid on the video
4. SAM 3 will track objects across frames, maintaining object identity

### Video File Processing

1. Click the **"📁 Upload Video"** button
2. Select a video file (MP4, AVI, MOV, etc.)
3. The video will:
   - Play in the canvas display
   - Upload to the backend for processing
   - Create a SAM 3 tracking session
4. Add prompts (text or visual) to track specific objects

## API Documentation

### WebSocket Endpoint: `/ws/track`

**Purpose**: Real-time frame streaming for live camera tracking

**Protocol**:
- Client sends: Base64-encoded JPEG frames
- Server responds: JSON with segmentation masks

**Message Format**:
```javascript
// Client -> Server
"data:image/jpeg;base64,/9j/4AAQSkZJRg..."

// Server -> Client
{
  "masks": [[[x1, y1], [x2, y2], ...], ...],
  "frame_index": 42,
  "session_id": "abc123"
}
```

### REST Endpoint: `POST /process-video`

**Purpose**: Upload and process video files

**Request**:
```bash
curl -X POST http://localhost:8000/process-video \
  -F "file=@video.mp4"
```

**Response**:
```json
{
  "status": "Complete",
  "session_id": "xyz789",
  "filename": "video.mp4",
  "message": "Video uploaded and session created."
}
```

### Health Check: `GET /health`

**Purpose**: Verify backend status and model availability

**Response**:
```json
{
  "status": "healthy",
  "model": "loaded"
}
```

## Performance Considerations

### GPU Acceleration
- **Required for real-time tracking** (30 FPS)
- Without GPU, expect 1-5 FPS depending on CPU
- Recommended: NVIDIA A100, H200, or RTX 4090

### Optimization Tips
1. **Reduce frame resolution**: Lower webcam resolution for better performance
2. **Adjust JPEG quality**: Change `toDataURL('image/jpeg', 0.5)` quality parameter
3. **Frame skipping**: Process every Nth frame instead of all frames
4. **Batch processing**: Use video upload for non-real-time processing

## Troubleshooting

### Backend Issues

**Error: "Failed to load SAM 3 model"**
- Ensure you've requested and been granted access to SAM 3 weights on Hugging Face
- Authenticate with `huggingface-cli login`
- Verify PyTorch and CUDA are properly installed

**Error: "CUDA out of memory"**
- Reduce batch size or frame resolution
- Use a GPU with more VRAM
- Process videos in smaller chunks

### Frontend Issues

**Camera not accessible**
- Grant camera permissions in browser settings
- Use HTTPS in production (required for camera access)
- Check if another application is using the camera

**WebSocket connection failed**
- Verify backend is running on `http://localhost:8000`
- Check firewall settings
- Look for CORS errors in browser console

## Development

### Backend Structure
```
webapp/backend/
├── main.py              # FastAPI application
└── requirements.txt     # Python dependencies
```

### Frontend Structure
```
webapp/frontend/
├── src/
│   ├── App.jsx         # Main React component
│   ├── App.css         # Styles
│   └── main.jsx        # Entry point
├── package.json        # Node dependencies
└── vite.config.js      # Vite configuration
```

### Testing

**Backend tests**:
```bash
cd webapp/backend
pytest
```

**Frontend tests**:
```bash
cd webapp/frontend
npm test
```

## Production Deployment

### Backend Deployment

1. Use a production ASGI server:
   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

2. Configure CORS for your domain:
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

3. Add authentication and rate limiting

### Frontend Deployment

1. Build for production:
   ```bash
   npm run build
   ```

2. Serve the `dist/` directory with nginx, Vercel, or Netlify

3. Update WebSocket URL to production backend

### Security Considerations

- Use HTTPS/WSS in production
- Implement authentication (JWT, OAuth)
- Add rate limiting to prevent abuse
- Validate and sanitize all file uploads
- Set file size limits

## License

This project follows the SAM 3 license. See the main repository LICENSE file for details.

## Support

For issues related to:
- **SAM 3 model**: See [SAM 3 GitHub Issues](https://github.com/facebookresearch/sam3/issues)
- **Web application**: Open an issue in this repository
- **Model weights access**: Contact Meta AI through Hugging Face

## Acknowledgments

Built with:
- [SAM 3](https://github.com/facebookresearch/sam3) by Meta AI
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [Vite](https://vite.dev/)
