# Using Local AI Models with Ollama

Run AI models on your own computer - **no API keys, no costs, complete privacy**.

## Why Local Models?

**Advantages:**
- ✅ **Free**: No API costs, unlimited usage
- ✅ **Privacy**: Data never leaves your machine
- ✅ **No API key**: No signup, no billing
- ✅ **Offline**: Works without internet
- ✅ **Learning**: Understand how LLMs work

**Trade-offs:**
- ⚠️ Slower than cloud APIs (depends on your hardware)
- ⚠️ Lower quality than GPT-4/Claude (but improving!)
- ⚠️ Requires disk space (models are 2-40GB)
- ⚠️ Needs decent hardware (8GB+ RAM recommended)

## Quick Start

### 1. Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### 2. Start Ollama

```bash
ollama serve
```

Keep this running in a terminal.

### 3. Pull a Model

```bash
# Recommended for students (smallest, fastest)
ollama pull llama3.2        # 2GB - Fast, good quality

# Other options:
ollama pull llama2          # 3.8GB - Very reliable
ollama pull mistral         # 4.1GB - Great for coding
ollama pull phi             # 1.3GB - Tiny, surprisingly good
ollama pull codellama       # 3.8GB - Optimized for code

# For powerful machines:
ollama pull llama3.1:70b    # 40GB - Best quality, slow
```

### 4. Test It

```bash
ollama run llama3.2

>>> Write a haiku about Kubernetes
Pods orchestrate work
Containers deploy and scale
Cloud native dreams

>>> /bye
```

### 5. Run the Local AI Server

```bash
cd ai-servers/local-ai

# Install dependencies
pip install -r requirements.txt

# Start server
python ollama_server.py
```

### 6. Update Blog Service

```bash
cd services/blog-service

# Update AI_SERVER_URL to point to local server
export AI_SERVER_URL=http://localhost:8081

python app.py
```

### 7. Test It!

```bash
curl -X POST http://localhost:8080/api/blog/suggest-topics \
  -H "Content-Type: application/json" \
  -d '{
    "interests": ["kubernetes", "AI"],
    "count": 3
  }' | python -m json.tool
```

## Choosing a Model

### llama3.2 (Recommended for Students)

- **Size**: 2GB
- **RAM**: 4GB minimum
- **Speed**: Fast (2-5 seconds)
- **Quality**: Good
- **Best for**: Learning, development, testing

```bash
ollama pull llama3.2
export AI_MODEL=llama3.2
python ollama_server.py
```

### llama2 (Reliable Choice)

- **Size**: 3.8GB
- **RAM**: 8GB minimum
- **Speed**: Medium (3-8 seconds)
- **Quality**: Very good
- **Best for**: Production testing

```bash
ollama pull llama2
export AI_MODEL=llama2
python ollama_server.py
```

### mistral (Great for Technical Content)

- **Size**: 4.1GB
- **RAM**: 8GB minimum
- **Speed**: Medium (3-7 seconds)
- **Quality**: Excellent for coding/technical
- **Best for**: Technical documentation

```bash
ollama pull mistral
export AI_MODEL=mistral
python ollama_server.py
```

### phi (Smallest, Fastest)

- **Size**: 1.3GB
- **RAM**: 2GB minimum
- **Speed**: Very fast (1-3 seconds)
- **Quality**: Decent for simple tasks
- **Best for**: Low-resource environments

```bash
ollama pull phi
export AI_MODEL=phi
python ollama_server.py
```

## Performance Comparison

### Cloud APIs (Claude, GPT-4)

```
Request latency: 1-3 seconds
Quality: Excellent
Cost: $0.001 - $0.01 per request
Requires: API key, internet
```

### Local Models (Ollama)

```
Request latency: 2-10 seconds (depends on hardware)
Quality: Good to very good
Cost: $0.00
Requires: Disk space, RAM
```

### Example: Blog Topic Generation

**Cloud (Claude Haiku):**
```
Latency: 2.3s
Quality: 9/10
Topics: Highly creative, well-structured
Cost: $0.001
```

**Local (llama3.2):**
```
Latency: 4.5s (M1 Mac)
Quality: 7/10
Topics: Good, occasionally generic
Cost: $0.00
```

## Hardware Requirements

### Minimum (for testing):

- **RAM**: 4GB
- **Disk**: 5GB free
- **CPU**: Any modern CPU
- **Model**: phi (1.3GB) or llama3.2 (2GB)

### Recommended (for development):

- **RAM**: 8GB+
- **Disk**: 10GB free
- **CPU**: Multi-core (4+ cores)
- **Model**: llama3.2 (2GB) or mistral (4GB)

### Optimal (for production testing):

- **RAM**: 16GB+
- **Disk**: 50GB free
- **CPU**: 8+ cores or Apple Silicon
- **GPU**: Optional (NVIDIA GPU speeds up inference)
- **Model**: llama3.1 (8GB) or llama3.1:70b (40GB)

## Model Comparison

| Model | Size | RAM | Speed | Quality | Best For |
|-------|------|-----|-------|---------|----------|
| phi | 1.3GB | 2GB | ⚡⚡⚡ | ⭐⭐⭐ | Testing, low resources |
| llama3.2 | 2GB | 4GB | ⚡⚡ | ⭐⭐⭐⭐ | **Students (Recommended)** |
| llama2 | 3.8GB | 8GB | ⚡ | ⭐⭐⭐⭐ | Reliable production testing |
| mistral | 4.1GB | 8GB | ⚡ | ⭐⭐⭐⭐⭐ | Technical content |
| codellama | 3.8GB | 8GB | ⚡ | ⭐⭐⭐⭐ | Code generation |
| llama3.1 | 8GB | 16GB | ⚡ | ⭐⭐⭐⭐⭐ | High quality |
| llama3.1:70b | 40GB | 64GB | 💤 | ⭐⭐⭐⭐⭐ | Best quality (slow) |

## Provider Abstraction

You can easily switch between providers by changing the AI_SERVER_URL:

```bash
# Use local Ollama
export AI_SERVER_URL=http://localhost:8081
python app.py

# Use Claude (Anthropic)
export AI_SERVER_URL=http://localhost:8081
export ANTHROPIC_API_KEY=your-key
cd ai-servers/content-ai && python server.py

# Use OpenAI
export AI_SERVER_URL=http://localhost:8081
export OPENAI_API_KEY=your-key
cd ai-servers/openai-ai && python server.py
```

## Switching Between Providers

### Development Workflow

```bash
# 1. Start with local model for development
ollama serve
python ai-servers/local-ai/ollama_server.py

# 2. Test with your service
export AI_SERVER_URL=http://localhost:8081
python services/blog-service/app.py

# 3. When ready, test with cloud API
export ANTHROPIC_API_KEY=your-key
python ai-servers/content-ai/server.py

# Service automatically switches to cloud AI
```

### Configuration File Approach

Create `.env`:

```bash
# Provider selection
AI_PROVIDER=ollama  # or anthropic, openai

# Ollama settings
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Anthropic settings (if using cloud)
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-haiku-20240307

# Service settings
AI_SERVER_URL=http://localhost:8081
REDIS_HOST=localhost
```

## Troubleshooting

### "Cannot connect to Ollama"

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

### "Model not found"

```bash
# List installed models
ollama list

# Pull the model
ollama pull llama3.2
```

### Slow responses

```bash
# Use a smaller model
ollama pull phi  # 1.3GB, much faster
export AI_MODEL=phi

# Or reduce generation length in prompts
```

### Out of memory

```bash
# Use a smaller model
ollama pull phi

# Or close other applications
# Or increase swap space
```

### Poor quality responses

```bash
# Use a larger model
ollama pull mistral

# Or improve your prompts
# Or switch to cloud API for critical features
```

## Example: Full Local Setup

```bash
# 1. Install Ollama
brew install ollama

# 2. Start Ollama
ollama serve &

# 3. Pull model
ollama pull llama3.2

# 4. Start Redis
redis-server &

# 5. Start local AI server
cd ai-servers/local-ai
pip install -r requirements.txt
export AI_MODEL=llama3.2
python ollama_server.py &

# 6. Start blog service
cd ../../services/blog-service
export AI_SERVER_URL=http://localhost:8081
python app.py &

# 7. Test it
curl -X POST http://localhost:8080/api/blog/suggest-topics \
  -H "Content-Type: application/json" \
  -d '{"interests": ["python", "AI"], "count": 3}'
```

Everything runs locally, no API keys needed! 🎉

## Cost Comparison

### Cloud APIs (per 1000 requests)

| Provider | Model | Cost |
|----------|-------|------|
| Anthropic | Claude Haiku | ~$1.00 |
| OpenAI | GPT-3.5 Turbo | ~$0.50 |
| OpenAI | GPT-4 | ~$30.00 |

### Local (Ollama)

| Model | Cost |
|-------|------|
| Any | **$0.00** |

**For a student project with 10,000 requests:**
- Cloud API: $10 - $300
- Local Ollama: **$0**

## Production Recommendations

### For Learning (Tutorial 17)

✅ **Use local models (Ollama)**
- No costs
- Learn without limits
- Privacy
- Recommended: llama3.2

### For Production

Consider hybrid approach:
- **Development**: Local models (free, fast iteration)
- **Staging**: Cloud API (test quality)
- **Production**: Cloud API with caching (quality + cost control)

Or all local if:
- Privacy is critical
- High volume (>100k requests/month)
- You have good hardware
- Quality requirements are moderate

## Advanced: GPU Acceleration

If you have an NVIDIA GPU:

```bash
# Ollama automatically uses GPU if available
# Check GPU usage:
nvidia-smi

# Much faster inference:
# llama3.2: 0.5-2s (vs 4-5s on CPU)
# llama3.1:70b: Becomes feasible (vs unusably slow on CPU)
```

## Next Steps

1. **Try different models** - Compare quality vs speed
2. **Optimize prompts** - Smaller models need better prompts
3. **Implement caching** - Reduce duplicate AI calls
4. **A/B test** - Local vs cloud quality
5. **Monitor performance** - Track latency and quality

Local models are improving rapidly. What works today will be better tomorrow! 🚀
