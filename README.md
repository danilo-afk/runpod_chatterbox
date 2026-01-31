# RunPod Serverless Endpoint for Voice Cloning

[![Runpod](https://api.runpod.io/badge/danilo-afk/runpod_chatterbox)](https://console.runpod.io/hub/danilo-afk/runpod_chatterbox)

## Overview
* REST API
* Call Endpoint API with YouTube link and prompt
* Downloads first 60 seconds of provided YouTube audio
* Invokes [Chatterbox TTS model](https://github.com/resemble-ai/chatterbox) 
* Returns base64 encoded WAV audio

## Deploy

### Pré-requisitos
1. Conta no RunPod ([link de referência](https://runpod.io?ref=3lyngjfm))
2. Token do HuggingFace com acesso ao modelo `ResembleAI/ChatterboxMultilingualTTS`
   - Aceite os termos em https://huggingface.co/ResembleAI/ChatterboxMultilingualTTS
   - Crie token em https://huggingface.co/settings/tokens

### Configuração do Endpoint

1. **Configure o Model Cache** (ESSENCIAL para evitar timeout):
   - Vá em https://console.runpod.io/serverless
   - Clique em "New Endpoint"
   - Em **Model** ou **Cached Models**, adicione: `ResembleAI/ChatterboxMultilingualTTS`
   - Isso pré-baixa o modelo para `/runpod-volume/huggingface-cache/hub/`

2. **Configure o Secret HF_TOKEN**:
   - Vá em **Secrets** (menu lateral)
   - Crie secret `HF_TOKEN` com seu token do HuggingFace

3. **Configure o Endpoint**:
   - GitHub Repo: `https://github.com/danilo-afk/runpod_chatterbox`
   - Em **Environment Variables**, adicione:
     - `HF_TOKEN` → selecione a secret criada acima
   - Workers: configure conforme demanda (ex: 0-3 workers)
   - GPU: RTX 4090 ou superior recomendado

4. **Anote as credenciais**:
   - `Endpoint ID` em https://console.runpod.io/serverless
   - `API key` em https://console.runpod.io/user/settings

## Usage 

### JavaScript 

```js
const requestConfig = {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + RP_API_KEY
  },
  body: JSON.stringify({
    "input": {
      "prompt": "Hello world",
      "yt_url": "https://www.youtube.com/shorts/jcNzoONhrmE",
    }
  })
};
const url = "https://api.runpod.ai/v2/" + RP_ENDPOINT + "/runsync";
const response = await fetch(url, requestConfig);
let data = await response.json();
data = data.output

// audio data in data.audio_base64
```

## Performance

* **Inicialização**: ~30s com model cache configurado corretamente
* **Sem cache**: 3-4 minutos (download de 2GB+ na primeira execução)
* **Recomendação**: SEMPRE configure o model cache conforme instruções acima
