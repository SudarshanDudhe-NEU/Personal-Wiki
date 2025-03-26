# Running Llama 3.2 Locally with Ollama

This guide provides step-by-step instructions for installing and running Llama 3.2 on local systems using Ollama, with special focus on optimizations for MacBook Air with M2 chip.

## What is Ollama?

Ollama is a platform for running large language models locally on your machine. It's specifically optimized for:

- **Apple Silicon**: Enhanced performance on M1/M2 processors
- **Quantized Models**: Support for resource-efficient model variants
- **Command Line Interface**: Simple terminal-based interactions
- **API Integration**: Built-in HTTP server for application integration

## System Requirements

- **Hardware**: MacBook Air M2 with 8GB RAM (or any compatible system)
- **OS**: macOS 12.0+ (or Linux/Windows with appropriate adjustments)
- **Storage**: Minimum 1GB free space (more recommended)
- **Network**: Internet connection for model downloads

## Installation Steps

### 1. Download and Install Ollama

1. Visit [Ollama's official download page](https://ollama.com/download)
2. Download the appropriate version for your OS
3. For macOS:
   ```bash
   # Install with Homebrew (alternative method)
   brew install ollama
   ```
   Or simply drag the Ollama app to your Applications folder

### 2. Start Ollama

1. Launch Ollama from Applications folder
2. Verify installation by opening Terminal and running:
   ```bash
   ollama --version
   ```

### 3. Install Llama 3.2 Model

```bash
# Pull the Llama 3.2 model (size options available)
ollama pull llama3.2

# For more efficiency on 8GB RAM systems, use:
ollama pull llama3.2:8b-q4_K_M
```

## Using Llama 3.2

### Interactive Mode

```bash
# Start an interactive chat session
ollama run llama3.2
```

Example interaction:
```
>>> What projects would benefit from local LLMs?
Local LLMs are particularly valuable for projects requiring privacy, 
offline functionality, or reduced latency. These include personal 
knowledge management systems, sensitive document analysis, local 
coding assistants, and embedded AI applications where data security 
is paramount...
```

### API Usage

Ollama runs a local API server on port 11434. You can interact with it using curl:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Explain quantum computing in simple terms",
  "stream": false
}'
```

## Performance Optimization

For MacBook Air M2 with 8GB RAM:

1. **Choose appropriate model size**:
   - For better performance: `llama3.2:8b` (smaller model)
   - For higher quality: `llama3.2` (full model, may be slower)

2. **System optimization**:
   - Close unnecessary applications
   - Monitor memory usage with Activity Monitor
   - Consider creating a swap file if needed

3. **Command parameters**:
   ```bash
   # Control context size to reduce memory usage
   ollama run llama3.2 --context 2048
   ```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Out of memory errors | Use smaller model variant or reduce context size |
| Slow responses | Close background applications, try a more quantized model |
| Command not found | Ensure Ollama is in your PATH |
| Model download fails | Check internet connection, try again |

## Advanced Usage

### Embedding Ollama in Python Applications

```python
import requests

def query_llm(prompt, model="llama3.2"):
    response = requests.post('http://localhost:11434/api/generate', 
                            json={
                                'model': model,
                                'prompt': prompt
                            })
    return response.json()['response']

# Example usage
result = query_llm("Write a haiku about programming")
print(result)
```

### Custom Model Configuration

Create a Modelfile for customized behavior:

```
# Custom Llama 3.2 configuration
FROM llama3.2
PARAMETER temperature 0.7
PARAMETER top_p 0.9
SYSTEM You are a helpful AI assistant focusing on technical documentation.
```

Save as `Modelfile` and build:

```bash
ollama create tech-assistant -f Modelfile
ollama run tech-assistant
```

## Resources

- [Ollama GitHub Repository](https://github.com/ollama/ollama)
- [Llama 3 Documentation](https://ai.meta.com/llama/)
- [Model Quantization Explained](https://ollama.com/blog/how-quantization-works)

## Updates and Maintenance

- Check for Ollama updates regularly
- New model versions can be pulled with `ollama pull llama3.2:latest`
- Remove unused models with `ollama rm model-name` to free disk space