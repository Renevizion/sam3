import React, { useRef, useEffect, useState } from 'react';
import './App.css';

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const socketRef = useRef(null);
  const animationRef = useRef(null);
  const [isLive, setIsLive] = useState(true);
  const [masks, setMasks] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [status, setStatus] = useState('Initializing...');
  const [uploadProgress, setUploadProgress] = useState(null);

  // WebSocket connection management
  useEffect(() => {
    const connectWebSocket = () => {
      try {
        const wsUrl = 'ws://localhost:8000/ws/track';
        socketRef.current = new WebSocket(wsUrl);
        
        socketRef.current.onopen = () => {
          setIsConnected(true);
          setStatus('Connected to SAM 3 server');
          console.log('WebSocket connected');
        };
        
        socketRef.current.onmessage = (e) => {
          try {
            const data = JSON.parse(e.data);
            if (data.masks) {
              setMasks(data.masks);
            }
            if (data.error) {
              setStatus(`Error: ${data.error}`);
            }
          } catch (err) {
            console.error('Error parsing WebSocket message:', err);
          }
        };
        
        socketRef.current.onerror = (error) => {
          console.error('WebSocket error:', error);
          setStatus('Connection error - check if backend is running');
          setIsConnected(false);
        };
        
        socketRef.current.onclose = () => {
          setIsConnected(false);
          setStatus('Disconnected from server');
          console.log('WebSocket disconnected');
        };
      } catch (error) {
        console.error('Failed to create WebSocket:', error);
        setStatus('Failed to connect to backend');
      }
    };

    connectWebSocket();

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);

  // Camera and drawing loop
  useEffect(() => {
    if (isLive) {
      // Start camera
      navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } })
        .then(stream => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            videoRef.current.play();
            setStatus('Camera active - streaming to SAM 3');
          }
        })
        .catch(err => {
          console.error('Error accessing camera:', err);
          setStatus('Camera access denied or not available');
        });
    } else {
      // Stop camera
      if (videoRef.current && videoRef.current.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks();
        tracks.forEach(track => track.stop());
        videoRef.current.srcObject = null;
      }
    }

    // Drawing loop
    const drawLoop = () => {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      
      if (!video || !canvas) {
        animationRef.current = requestAnimationFrame(drawLoop);
        return;
      }

      const ctx = canvas.getContext('2d');
      
      // Draw video frame to canvas
      if (video.readyState === video.HAVE_ENOUGH_DATA) {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Send frame to backend if in live mode and connected
        if (isLive && socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
          try {
            const dataUrl = canvas.toDataURL('image/jpeg', 0.5);
            socketRef.current.send(dataUrl);
          } catch (err) {
            console.error('Error sending frame:', err);
          }
        }
        
        // Draw SAM 3 mask overlays
        if (masks.length > 0) {
          ctx.fillStyle = "rgba(0, 255, 0, 0.5)";
          ctx.strokeStyle = "rgba(0, 255, 0, 0.8)";
          ctx.lineWidth = 2;
          
          masks.forEach((mask) => {
            if (mask && mask.length > 0) {
              ctx.beginPath();
              mask.forEach(([x, y], i) => {
                if (i === 0) {
                  ctx.moveTo(x, y);
                } else {
                  ctx.lineTo(x, y);
                }
              });
              ctx.closePath();
              ctx.fill();
              ctx.stroke();
            }
          });
        }
      }
      
      animationRef.current = requestAnimationFrame(drawLoop);
    };

    drawLoop();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isLive, masks]);

  const handleSwitchToLive = () => {
    setIsLive(true);
    setMasks([]);
    setStatus('Switching to live camera...');
    if (videoRef.current) {
      videoRef.current.src = '';
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setIsLive(false);
    setMasks([]);
    setStatus('Loading video file...');
    
    // Display video in player
    if (videoRef.current) {
      videoRef.current.srcObject = null;
      videoRef.current.src = URL.createObjectURL(file);
      videoRef.current.load();
      videoRef.current.play();
    }
    
    // Upload to backend for processing
    try {
      setUploadProgress('Uploading...');
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch('http://localhost:8000/process-video', {
        method: 'POST',
        body: formData,
      });
      
      const result = await response.json();
      
      if (response.ok) {
        setStatus(`Video uploaded: ${result.message}`);
        setUploadProgress('Upload complete!');
      } else {
        setStatus(`Upload error: ${result.error || 'Unknown error'}`);
        setUploadProgress('Upload failed');
      }
      
      setTimeout(() => setUploadProgress(null), 3000);
    } catch (error) {
      console.error('Upload error:', error);
      setStatus(`Upload failed: ${error.message}`);
      setUploadProgress('Upload failed');
      setTimeout(() => setUploadProgress(null), 3000);
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>🏭 SAM 3 Factory Monitor</h1>
        <div className="status-bar">
          <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '● Connected' : '○ Disconnected'}
          </span>
          <span className="status-text">{status}</span>
        </div>
      </div>
      
      <div className="controls">
        <button 
          className={`btn ${isLive ? 'btn-active' : 'btn-secondary'}`}
          onClick={handleSwitchToLive}
        >
          📹 Live Camera
        </button>
        
        <label className="btn btn-secondary file-upload-btn">
          📁 Upload Video
          <input 
            type="file" 
            accept="video/*" 
            onChange={handleFileUpload}
            style={{ display: 'none' }}
          />
        </label>
        
        {uploadProgress && (
          <span className="upload-progress">{uploadProgress}</span>
        )}
      </div>
      
      <div className="video-container">
        <video 
          ref={videoRef} 
          autoPlay 
          muted 
          playsInline
          width="640" 
          height="480"
          style={{ display: 'none' }}
        />
        <canvas 
          ref={canvasRef} 
          width="640" 
          height="480"
          className="canvas-display"
        />
        <div className="info-overlay">
          <div className="info-text">
            {isLive ? '🔴 LIVE' : '▶ VIDEO'}
          </div>
          {masks.length > 0 && (
            <div className="mask-count">
              {masks.length} object{masks.length !== 1 ? 's' : ''} tracked
            </div>
          )}
        </div>
      </div>
      
      <div className="footer">
        <p className="help-text">
          <strong>Instructions:</strong> 
          Use the Live Camera to track objects in real-time via your webcam, 
          or upload a video file for batch processing. 
          SAM 3 will automatically detect and track objects across frames.
        </p>
        <p className="note">
          ⚠️ <strong>Note:</strong> Real-time tracking requires GPU acceleration. 
          Make sure the backend has access to the SAM 3 model weights from Hugging Face.
        </p>
      </div>
    </div>
  );
}

export default App;
