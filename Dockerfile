FROM runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    ffmpeg

RUN python -m pip install --no-deps chatterbox-tts

WORKDIR /
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY rp_handler.py /

# Preload multilingual model (downloads ~3.3GB de modelos do HuggingFace)
RUN python -c "from chatterbox.mtl_tts import ChatterboxMultilingualTTS; model = ChatterboxMultilingualTTS.from_pretrained(device='cuda')"

# Start the container
CMD ["python3", "-u", "rp_handler.py"]


