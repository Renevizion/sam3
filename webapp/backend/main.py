"""
SAM 3 Web Application Backend
FastAPI server with WebSocket for live camera tracking and REST endpoint for video processing.
"""

from fastapi import FastAPI, WebSocket, UploadFile, File, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import base64
import tempfile
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SAM 3 Factory Monitor API")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance (will be initialized on first use)
model = None


def get_model():
    """
    Lazy load the SAM 3 model
    
    Note: This function imports the SAM 3 model builder which requires:
    1. The SAM 3 package to be installed (pip install -e . from repo root)
    2. Access to SAM 3 weights on Hugging Face (optional for testing)
    3. Authentication with Hugging Face CLI (huggingface-cli login)
    
    For testing without weights, this function can be mocked.
    """
    global model
    if model is None:
        try:
            # Import SAM 3 model builder
            # This assumes sam3 package is installed via pip install -e .
            from sam3.model_builder import build_sam3_video_predictor
            
            logger.info("Loading SAM 3 model...")
            model = build_sam3_video_predictor()
            logger.info("SAM 3 model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load SAM 3 model: {e}")
            logger.error("Make sure you have:")
            logger.error("1. Requested access to sam3.pt weights on Hugging Face")
            logger.error("2. Authenticated with 'huggingface-cli login'")
            raise
    return model


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "SAM 3 Factory Monitor API",
        "endpoints": {
            "websocket": "/ws/track",
            "video_upload": "/process-video"
        }
    }


@app.websocket("/ws/track")
async def live_tracking(websocket: WebSocket):
    """
    WebSocket endpoint for real-time camera feed tracking.
    
    Receives base64-encoded frames from the frontend and returns SAM 3 segmentation masks.
    """
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    try:
        sam_model = get_model()
        session_id = None
        frame_index = 0
        
        while True:
            try:
                # Receive base64-encoded frame from client
                data = await websocket.receive_text()
                
                # Decode base64 image
                if "," in data:
                    # Remove data:image/jpeg;base64, prefix if present
                    img_data = data.split(",")[1]
                else:
                    img_data = data
                
                img_bytes = base64.b64decode(img_data)
                nparr = np.frombuffer(img_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if frame is None:
                    await websocket.send_json({"error": "Failed to decode frame"})
                    continue
                
                # Initialize session on first frame
                if session_id is None:
                    # Create a temporary file for the frame
                    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                        cv2.imwrite(tmp.name, frame)
                        temp_path = tmp.name
                    
                    try:
                        # Start a session with SAM 3 video predictor
                        response = sam_model.handle_request(
                            request=dict(
                                type="start_session",
                                resource_path=temp_path,
                            )
                        )
                        session_id = response.get("session_id")
                        logger.info(f"Started SAM 3 session: {session_id}")
                    finally:
                        # Clean up temp file
                        os.unlink(temp_path)
                
                # For tracking, we could add prompts dynamically
                # For now, send basic tracking response
                # In a full implementation, you'd track objects frame by frame
                
                masks = []
                # TODO: Implement proper frame-by-frame tracking with SAM 3
                # This would involve maintaining object IDs across frames
                
                await websocket.send_json({
                    "masks": masks,
                    "frame_index": frame_index,
                    "session_id": session_id
                })
                
                frame_index += 1
                
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected")
                break
            except Exception as e:
                logger.error(f"Error processing frame: {e}")
                await websocket.send_json({"error": str(e)})
                
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        logger.info("WebSocket connection closed")


@app.post("/process-video")
async def process_video(file: UploadFile = File(...)):
    """
    Process an uploaded video file with SAM 3 tracking.
    
    Args:
        file: Uploaded video file (MP4, AVI, etc.)
        
    Returns:
        JSON response with processing status and results
    """
    try:
        logger.info(f"Processing uploaded video: {file.filename}")
        
        # Validate file type
        if not file.filename:
            return JSONResponse(
                status_code=400,
                content={"error": "No filename provided"}
            )
        
        # Read uploaded file
        contents = await file.read()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=Path(file.filename).suffix, delete=False) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name
        
        try:
            sam_model = get_model()
            
            # Start a session with the video
            response = sam_model.handle_request(
                request=dict(
                    type="start_session",
                    resource_path=tmp_path,
                )
            )
            session_id = response.get("session_id")
            
            logger.info(f"Started video processing session: {session_id}")
            
            # TODO: Process the video and generate tracked outputs
            # This would involve:
            # 1. Adding text/visual prompts for objects to track
            # 2. Running SAM 3 tracking across all frames
            # 3. Saving the results to a new video file with overlays
            
            return JSONResponse(
                content={
                    "status": "Complete",
                    "session_id": session_id,
                    "filename": file.filename,
                    "message": "Video uploaded and session created. Add prompts to track specific objects."
                }
            )
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)
            
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check if model can be loaded
        get_model()
        return {"status": "healthy", "model": "loaded"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
