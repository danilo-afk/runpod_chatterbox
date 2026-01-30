"""Pré-download do modelo ChatterboxMultilingualTTS no build."""
import os
from huggingface_hub import snapshot_download

token = os.environ.get("HF_TOKEN")
snapshot_download("ResembleAI/ChatterboxMultilingualTTS", token=token)
print("Modelo baixado com sucesso!")
