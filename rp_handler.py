import runpod
import time
import torchaudio
import os
import tempfile
import base64
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from pathlib import Path

model = None
output_filename = "output.wav"

def handler(event):
    global model

    job_input = event['input']
    text = job_input.get('text') or job_input.get('prompt')
    language_id = job_input.get('language_id', 'pt')
    audio_prompt_url = job_input.get('audio_prompt_url')

    if not text:
        return {"error": "Campo 'text' é obrigatório"}

    print(f"Request: text='{text[:80]}...', lang={language_id}")

    # Lazy load: carrega modelo só no primeiro request
    if model is None:
        print("Lazy loading model on first request...")
        initialize_model()

    try:
        # Gera áudio com Chatterbox Multilingual
        gen_kwargs = {
            "text": text,
            "language_id": language_id,
        }

        # Voice cloning via arquivo de referência (opcional)
        if audio_prompt_url:
            audio_path = download_audio_prompt(audio_prompt_url)
            gen_kwargs["audio_prompt_path"] = audio_path

        audio_tensor = model.generate(**gen_kwargs)

        # Converte para base64
        audio_base64 = audio_tensor_to_base64(audio_tensor, model.sr)

        response = {
            "status": "success",
            "audio_base64": audio_base64,
            "metadata": {
                "sample_rate": model.sr,
                "language_id": language_id,
                "audio_shape": list(audio_tensor.shape)
            }
        }

        # Limpa arquivo de referência se baixou
        if audio_prompt_url and 'audio_path' in dir():
            try:
                os.remove(audio_path)
            except Exception:
                pass

        return response

    except Exception as e:
        print(f"Erro: {e}")
        return {"error": str(e)}

def audio_tensor_to_base64(audio_tensor, sample_rate):
    """Convert audio tensor to base64 encoded WAV data."""
    try:
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            torchaudio.save(tmp_file.name, audio_tensor, sample_rate)
            
            # Read back as binary data
            with open(tmp_file.name, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Clean up temporary file
            os.unlink(tmp_file.name)
            
            # Encode as base64
            return base64.b64encode(audio_data).decode('utf-8')
            
    except Exception as e:
        print(f"Error converting audio to base64: {e}")
        raise


def download_audio_prompt(url):
    """Baixa arquivo de áudio de referência para voice cloning."""
    import urllib.request
    tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    urllib.request.urlretrieve(url, tmp.name)
    print(f"Audio prompt baixado: {tmp.name}")
    return tmp.name


def initialize_model():
    global model

    if model is not None:
        print("Model already initialized")
        return model

    # Login no HuggingFace para modelo gated
    hf_token = os.environ.get("HF_TOKEN")
    if hf_token:
        from huggingface_hub import login
        login(token=hf_token)
        print("HuggingFace login OK")

    # Usa cache do RunPod se disponível
    cache_dir = "/runpod-volume/huggingface-cache/hub"
    if os.path.exists(cache_dir):
        os.environ["HF_HOME"] = cache_dir
        print(f"Using RunPod cache: {cache_dir}")

    print("Initializing ChatterboxMultilingualTTS model...")
    start = time.time()
    model = ChatterboxMultilingualTTS.from_pretrained(device="cuda")
    print(f"Model initialized in {time.time() - start:.1f}s")

if __name__ == '__main__':
    # Não carrega modelo na inicialização - lazy load no primeiro request
    print("Worker ready - model will load on first request")
    runpod.serverless.start({'handler': handler })
