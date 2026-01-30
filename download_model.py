"""Pré-download do modelo ChatterboxMultilingualTTS no build."""
from huggingface_hub import snapshot_download

# Baixa todos os arquivos do modelo para o cache local
snapshot_download("ResembleAI/ChatterboxMultilingualTTS")
print("Modelo baixado com sucesso!")
