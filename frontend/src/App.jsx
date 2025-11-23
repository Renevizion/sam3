import { useState } from 'react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('image')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  // Image processing state
  const [imageFile, setImageFile] = useState(null)
  const [imagePrompt, setImagePrompt] = useState('')
  const [imagePreview, setImagePreview] = useState(null)

  // Video processing state
  const [videoFile, setVideoFile] = useState(null)
  const [videoPrompt, setVideoPrompt] = useState('')
  const [videoPreview, setVideoPreview] = useState(null)

  // Kie.ai generator state
  const [kiePrompt, setKiePrompt] = useState('')

  const handleImageFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setImageFile(file)
      setImagePreview(URL.createObjectURL(file))
      setResult(null)
      setError(null)
    }
  }

  const handleVideoFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setVideoFile(file)
      setVideoPreview(URL.createObjectURL(file))
      setResult(null)
      setError(null)
    }
  }

  const processImage = async () => {
    if (!imageFile || !imagePrompt.trim()) {
      setError('Please upload an image and enter a prompt')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', imageFile)
    formData.append('text_prompt', imagePrompt)

    try {
      const response = await fetch('/api/process/image', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Failed to process image')
      }

      const blob = await response.blob()
      const resultUrl = URL.createObjectURL(blob)
      setResult(resultUrl)
    } catch (err) {
      setError(err.message || 'An error occurred while processing the image')
    } finally {
      setLoading(false)
    }
  }

  const processVideo = async () => {
    if (!videoFile || !videoPrompt.trim()) {
      setError('Please upload a video and enter a prompt')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', videoFile)
    formData.append('text_prompt', videoPrompt)

    try {
      const response = await fetch('/api/process/video', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Failed to process video')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'An error occurred while processing the video')
    } finally {
      setLoading(false)
    }
  }

  const generateImageKie = async () => {
    if (!kiePrompt.trim()) {
      setError('Please enter a prompt')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('text_prompt', kiePrompt)

    try {
      const response = await fetch('/api/generate/image-kie', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(errorText || 'Failed to generate image')
      }

      const blob = await response.blob()
      const resultUrl = URL.createObjectURL(blob)
      setResult(resultUrl)
    } catch (err) {
      setError(err.message || 'An error occurred while generating the image')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🎯 SAM3 Web Application</h1>
        <p>Segment Anything with Concepts - Fast & Easy</p>
      </header>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'image' ? 'active' : ''}`}
          onClick={() => setActiveTab('image')}
        >
          📷 Image Processing
        </button>
        <button
          className={`tab ${activeTab === 'video' ? 'active' : ''}`}
          onClick={() => setActiveTab('video')}
        >
          🎥 Video Processing
        </button>
        <button
          className={`tab ${activeTab === 'generator' ? 'active' : ''}`}
          onClick={() => setActiveTab('generator')}
        >
          🎨 Image Generator
        </button>
      </div>

      <div className="content">
        {activeTab === 'image' && (
          <div className="panel">
            <h2>Process Image with SAM3</h2>
            
            <div className="upload-section">
              <label htmlFor="image-upload" className="upload-label">
                {imagePreview ? '✓ Image Loaded' : '📁 Upload Image'}
              </label>
              <input
                id="image-upload"
                type="file"
                accept="image/*"
                onChange={handleImageFileChange}
                className="file-input"
              />
            </div>

            {imagePreview && (
              <div className="preview">
                <img src={imagePreview} alt="Preview" />
              </div>
            )}

            <div className="prompt-section">
              <label htmlFor="image-prompt">Text Prompt:</label>
              <input
                id="image-prompt"
                type="text"
                value={imagePrompt}
                onChange={(e) => setImagePrompt(e.target.value)}
                placeholder="e.g., 'a dog', 'person wearing red shirt'"
                className="prompt-input"
              />
            </div>

            <button
              onClick={processImage}
              disabled={loading || !imageFile || !imagePrompt.trim()}
              className="process-btn"
            >
              {loading ? '⏳ Processing...' : '🚀 Process Image'}
            </button>

            {error && <div className="error">{error}</div>}

            {result && typeof result === 'string' && (
              <div className="result">
                <h3>Result:</h3>
                <img src={result} alt="Result" />
                <a href={result} download="sam3_result.png" className="download-btn">
                  ⬇️ Download Result
                </a>
              </div>
            )}
          </div>
        )}

        {activeTab === 'video' && (
          <div className="panel">
            <h2>Process Video with SAM3</h2>
            
            <div className="upload-section">
              <label htmlFor="video-upload" className="upload-label">
                {videoPreview ? '✓ Video Loaded' : '📁 Upload Video'}
              </label>
              <input
                id="video-upload"
                type="file"
                accept="video/*"
                onChange={handleVideoFileChange}
                className="file-input"
              />
            </div>

            {videoPreview && (
              <div className="preview">
                <video src={videoPreview} controls />
              </div>
            )}

            <div className="prompt-section">
              <label htmlFor="video-prompt">Text Prompt:</label>
              <input
                id="video-prompt"
                type="text"
                value={videoPrompt}
                onChange={(e) => setVideoPrompt(e.target.value)}
                placeholder="e.g., 'a person', 'a red car'"
                className="prompt-input"
              />
            </div>

            <button
              onClick={processVideo}
              disabled={loading || !videoFile || !videoPrompt.trim()}
              className="process-btn"
            >
              {loading ? '⏳ Processing...' : '🚀 Process Video'}
            </button>

            {error && <div className="error">{error}</div>}

            {result && typeof result === 'object' && (
              <div className="result">
                <h3>Processing Complete!</h3>
                <p>✅ Status: {result.status}</p>
                <p>📊 Frames processed: {result.num_frames || 'N/A'}</p>
                <p>📝 Prompt: {result.prompt}</p>
                <p className="note">
                  Note: Video visualization is in development. 
                  Results show tracking was successful.
                </p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'generator' && (
          <div className="panel">
            <h2>Generate Image with kie.ai Nano Banana</h2>
            
            <div className="prompt-section">
              <label htmlFor="kie-prompt">Text Prompt:</label>
              <textarea
                id="kie-prompt"
                value={kiePrompt}
                onChange={(e) => setKiePrompt(e.target.value)}
                placeholder="e.g., 'a beautiful sunset over mountains', 'a cute robot'"
                className="prompt-textarea"
                rows="4"
              />
            </div>

            <button
              onClick={generateImageKie}
              disabled={loading || !kiePrompt.trim()}
              className="process-btn"
            >
              {loading ? '⏳ Generating...' : '✨ Generate with Nano Banana'}
            </button>

            {error && <div className="error">{error}</div>}

            {result && typeof result === 'string' && (
              <div className="result">
                <h3>Generated Image:</h3>
                <img src={result} alt="Generated" />
                <a href={result} download="kie_generated.png" className="download-btn">
                  ⬇️ Download Image
                </a>
              </div>
            )}
          </div>
        )}
      </div>

      <footer className="footer">
        <p>Powered by SAM3 (Meta AI) • Fast & Minimal Implementation</p>
      </footer>
    </div>
  )
}

export default App
