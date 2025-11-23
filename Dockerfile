# Use NVIDIA CUDA base image with CUDA 12.6
FROM nvidia/cuda:12.6.0-cudnn-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CUDA_HOME=/usr/local/cuda

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.12 \
    python3.12-dev \
    python3-pip \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.12 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Set working directory
WORKDIR /app

# Install PyTorch with CUDA 12.6 support
RUN pip install torch==2.7.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# Clone and install SAM3
RUN git clone https://github.com/facebookresearch/sam3.git /tmp/sam3 && \
    cd /tmp/sam3 && \
    pip install -e .

# Copy backend requirements and install
COPY backend/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy backend code
COPY backend/ /app/backend/
COPY sam3/ /app/sam3/
COPY assets/ /app/assets/

# Copy frontend build (if exists)
COPY frontend/dist/ /app/frontend/dist/ 2>/dev/null || true

# Expose port
EXPOSE 8000

# Environment variables for API keys (to be set at runtime)
ENV HF_TOKEN=""
ENV KIE_API_KEY=""

# Run the application
CMD ["python", "backend/main.py"]
