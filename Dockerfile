FROM runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    git wget curl ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-deps chatterbox-tts

WORKDIR /
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY rp_handler.py /

CMD ["python3", "-u", "rp_handler.py"]


