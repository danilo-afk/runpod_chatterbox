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

# Preload: apenas baixa os pesos do modelo (sem importar chatterbox que requer cuda)
RUN python -c "from huggingface_hub import snapshot_download; snapshot_download('ResembleAI/chatterbox_multilingual', local_dir='/root/.cache/chatterbox_multilingual')"

# Start the container
CMD ["python3", "-u", "rp_handler.py"]


