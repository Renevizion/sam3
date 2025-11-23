# SAM3 Web Application - User Guide

## Overview

This guide walks you through using the SAM3 web application for object segmentation and tracking.

## Main Interface

The application features a clean, modern interface with two main sections:

### 1. Image Processing Tab 📷

**Purpose**: Segment objects in static images using text prompts

**How to use**:
1. Click "📁 Upload Image" to select an image file
2. Preview of your image will appear
3. Enter a text prompt (e.g., "a dog", "person wearing red")
4. Click "🚀 Process Image" button
5. View the result with colored masks and bounding boxes
6. Download the result using "⬇️ Download Result" button

**Example Prompts**:
- Simple objects: `"a car"`, `"a person"`, `"a cat"`
- Specific attributes: `"a person in red shirt"`, `"white car"`
- Multiple objects: `"dogs"`, `"all people"`

### 2. Video Processing Tab 🎥

**Purpose**: Track and segment objects across video frames

**How to use**:
1. Click "📁 Upload Video" to select a video file (MP4, AVI, etc.)
2. Preview of your video will appear
3. Enter a text prompt describing what to track
4. Click "🚀 Process Video" button
5. View processing results (frame count, status)

**Example Prompts**:
- `"a person"` - track a person throughout the video
- `"red car"` - track a specific colored vehicle
- `"basketball"` - track a moving object

## Features

### Real-time Feedback
- ✅ File upload confirmation
- ⏳ Processing status indicator
- 🔄 Loading animations
- ❌ Error messages when issues occur

### Visual Results
- **Colored Masks**: Each detected object gets a unique color overlay
- **Bounding Boxes**: Precise object boundaries
- **Score Display**: Confidence scores for detections
- **Download Option**: Save processed images locally

## Tips for Best Results

### Image Processing
- **Resolution**: Works best with images up to 2048x2048
- **Clarity**: Use clear, well-lit images
- **Prompts**: Be specific but not overly complex
- **Multiple Objects**: The model handles multiple instances

### Video Processing
- **Length**: Keep videos under 1-2 minutes for faster processing
- **Frame Rate**: Standard 24-30 fps works best
- **Quality**: Higher quality input = better tracking
- **Consistency**: Objects should be visible throughout

## Common Use Cases

### Security & Surveillance
- Track people or vehicles in footage
- Detect specific objects or people
- Monitor activity patterns

### Sports Analysis
- Track players or balls
- Analyze player movements
- Highlight specific actions

### Content Creation
- Isolate subjects for editing
- Create masks for effects
- Track objects for compositing

### Research & Development
- Object detection experiments
- Tracking algorithm testing
- Dataset annotation

## Keyboard Shortcuts

Currently, all interactions are mouse/touch-based. Keyboard shortcuts may be added in future versions.

## Browser Compatibility

**Recommended Browsers**:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Mobile Support**:
- iOS Safari (partial)
- Android Chrome (partial)

Note: Desktop browsers provide the best experience.

## API Documentation

For developers who want to integrate with the API directly:

### Endpoints

**Health Check**
```
GET /api/health
Response: {"status": "healthy", "cuda_available": true, ...}
```

**Process Image**
```
POST /api/process/image
Content-Type: multipart/form-data
Body:
  - file: image file
  - text_prompt: string
Response: Processed image (PNG)
```

**Process Video**
```
POST /api/process/video
Content-Type: multipart/form-data
Body:
  - file: video file
  - text_prompt: string
Response: JSON with processing results
```

## Troubleshooting

### "Processing failed" error
- Check file size (max 100MB by default)
- Ensure image/video format is supported
- Try a simpler prompt
- Check server logs for details

### Slow processing
- First request loads models (10-15s delay)
- Large files take longer
- Consider resizing input
- Check if GPU is being used

### No results shown
- Prompt may not match any objects
- Try more generic prompts
- Check image quality and clarity
- Lower score threshold in config

### Frontend not loading
- Ensure frontend was built: `cd frontend && npm run build`
- Check server logs for errors
- Verify static files exist in `frontend/dist`

## Performance Expectations

**Image Processing**:
- Small images (< 1MP): ~2-3 seconds
- Medium images (1-4MP): ~3-5 seconds
- Large images (4-8MP): ~5-10 seconds

**Video Processing**:
- Short clips (< 30s): ~15-30 seconds
- Medium clips (30s-2min): ~30-120 seconds
- Long clips (2-5min): ~2-5 minutes

*Times assume GPU acceleration and subsequent requests (after model loading)*

## Privacy & Data

- **Local Processing**: All processing happens on your server
- **No Data Retention**: Files are deleted after processing
- **No Telemetry**: No usage data is collected
- **Open Source**: Full transparency in code

## Support

For issues, questions, or feature requests:
- Check the main README.md
- Review troubleshooting section
- Check server logs
- Open an issue on GitHub

## Credits

Built with:
- **SAM3**: Meta AI's Segment Anything Model 3
- **FastAPI**: Modern Python web framework
- **React**: UI framework
- **Vite**: Fast build tool

## Version Information

Current Version: 1.0.0
Last Updated: 2025
License: See LICENSE file
