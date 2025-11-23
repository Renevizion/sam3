"""
FastAPI server for SAM3 - Fast and minimal implementation
Loads models lazily to minimize startup time and memory usage
"""
import os
import tempfile
import io
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
import numpy as np

# Global model instances (lazy loaded)
_image_model = None
_image_processor = None
_video_predictor = None

app = FastAPI(title="SAM3 Web Application")

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_image_model():
    """Lazy load image model and processor"""
    global _image_model, _image_processor
    if _image_model is None:
        print("Loading SAM3 image model...")
        from sam3.model_builder import build_sam3_image_model
        from sam3.model.sam3_image_processor import Sam3Processor
        
        _image_model = build_sam3_image_model()
        _image_processor = Sam3Processor(_image_model)
        print("SAM3 image model loaded successfully")
    return _image_model, _image_processor


def get_video_predictor():
    """Lazy load video predictor"""
    global _video_predictor
    if _video_predictor is None:
        print("Loading SAM3 video predictor...")
        from sam3.model_builder import build_sam3_video_predictor
        
        _video_predictor = build_sam3_video_predictor()
        print("SAM3 video predictor loaded successfully")
    return _video_predictor


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "SAM3 API Server"}


@app.get("/api/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "cuda_available": torch.cuda.is_available(),
        "image_model_loaded": _image_model is not None,
        "video_predictor_loaded": _video_predictor is not None,
    }


@app.post("/api/process/image")
async def process_image(
    file: UploadFile = File(...),
    text_prompt: str = Form(...),
):
    """
    Process an image with SAM3 using a text prompt
    Returns the processed image with segmentation masks
    """
    try:
        # Load model (lazy)
        model, processor = get_image_model()
        
        # Read and process image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        
        # Run SAM3 inference
        inference_state = processor.set_image(image)
        output = processor.set_text_prompt(state=inference_state, prompt=text_prompt)
        
        # Get results
        masks = output["masks"]
        boxes = output["boxes"]
        scores = output["scores"]
        
        # Visualize results
        result_image = visualize_masks(image, masks, boxes, scores)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            result_image.save(tmp.name, format="PNG")
            tmp_path = tmp.name
        
        # Return as file response
        return FileResponse(
            tmp_path,
            media_type="image/png",
            filename=f"result_{file.filename}",
            background=lambda: os.unlink(tmp_path)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.post("/api/process/video")
async def process_video(
    file: UploadFile = File(...),
    text_prompt: str = Form(...),
):
    """
    Process a video with SAM3 using a text prompt
    Returns the processed video with tracking masks
    """
    try:
        # Load video predictor (lazy)
        video_predictor = get_video_predictor()
        
        # Save uploaded video to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_video_path = tmp.name
        
        # Start video processing session
        response = video_predictor.handle_request(
            request=dict(
                type="start_session",
                resource_path=tmp_video_path,
            )
        )
        
        session_id = response["session_id"]
        
        # Add text prompt
        response = video_predictor.handle_request(
            request=dict(
                type="add_prompt",
                session_id=session_id,
                frame_index=0,
                text=text_prompt,
            )
        )
        
        output = response["outputs"]
        
        # Process output and create result video
        # For now, return metadata about the processing
        # In production, you would render the video with masks
        os.unlink(tmp_video_path)
        
        return {
            "status": "success",
            "message": "Video processed successfully",
            "session_id": session_id,
            "num_frames": len(output) if isinstance(output, list) else 0,
            "prompt": text_prompt,
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


def visualize_masks(image, masks, boxes, scores, threshold=0.5):
    """
    Visualize segmentation masks on the image
    Simple visualization with colored masks
    """
    import numpy as np
    from PIL import ImageDraw
    
    # Convert image to numpy array
    img_array = np.array(image)
    result = img_array.copy()
    
    # Filter by score threshold
    if len(scores) > 0:
        valid_indices = scores > threshold
        masks = masks[valid_indices]
        boxes = boxes[valid_indices]
        scores = scores[valid_indices]
    
    # Draw masks
    colors = [
        (255, 0, 0, 100),    # Red
        (0, 255, 0, 100),    # Green
        (0, 0, 255, 100),    # Blue
        (255, 255, 0, 100),  # Yellow
        (255, 0, 255, 100),  # Magenta
        (0, 255, 255, 100),  # Cyan
    ]
    
    overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for idx, (mask, box, score) in enumerate(zip(masks, boxes, scores)):
        color = colors[idx % len(colors)]
        
        # Draw mask
        if isinstance(mask, torch.Tensor):
            mask = mask.cpu().numpy()
        
        # Create mask overlay
        mask_img = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
        colored_mask = Image.new('RGBA', image.size, color)
        overlay.paste(colored_mask, (0, 0), mask_img)
        
        # Draw bounding box
        if isinstance(box, torch.Tensor):
            box = box.cpu().numpy()
        x1, y1, x2, y2 = box
        draw.rectangle([x1, y1, x2, y2], outline=color[:3], width=2)
    
    # Composite result
    result_img = Image.alpha_composite(image.convert('RGBA'), overlay)
    return result_img.convert('RGB')


# Mount static files (frontend) - will be added later
# Uncomment when frontend is built
try:
    app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")
    print("Serving frontend from ../frontend/dist")
except Exception as e:
    print(f"Frontend not available: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
