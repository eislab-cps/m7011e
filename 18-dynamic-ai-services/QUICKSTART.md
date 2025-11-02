# Quick Start - Dynamic AI Services

Get an AI-powered blog service running in 5 minutes.

## Prerequisites

- Python 3.10+
- Redis running locally or Tutorial 15's Redis on Kubernetes
- **AI Provider** (choose one):
  - **Option A: Ollama (FREE, recommended)** - See below
  - **Option B: Anthropic API** (costs money) - Get key at https://console.anthropic.com/

---

## Option A: Quick Start with Ollama (FREE)

### Step 1: Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### Step 2: Start Ollama and Pull Model

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Pull a model (one-time, ~2GB download)
ollama pull llama3.2

# Test it
ollama run llama3.2
>>> Write a haiku about coding
>>> /bye
```

### Step 3: Install and Run Local AI Server

```bash
cd ai-servers/local-ai
pip install -r requirements.txt
python ollama_server.py
```

You should see:
```
Local AI Server (Ollama) Starting
Ollama Host: http://localhost:11434
Default Model: llama3.2
```

### Step 4: Run Blog Service

In another terminal:

```bash
cd services/blog-service
pip install -r requirements.txt
export AI_SERVER_URL=http://localhost:8081
python app.py
```

### Step 5: Test It!

```bash
curl -X POST http://localhost:8080/api/blog/suggest-topics \
  -H "Content-Type: application/json" \
  -d '{
    "interests": ["kubernetes", "AI"],
    "count": 3
  }' | python -m json.tool
```

**Done!** You're running AI locally, no API key needed! 🎉

---

## Option B: Quick Start with Cloud API

### Step 1: Get API Key

```bash
# Sign up for Anthropic API
# Visit: https://console.anthropic.com/

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...
```

## Step 2: Install Dependencies

```bash
# Content AI server
cd ai-servers/content-ai
pip install -r requirements.txt

# Blog service
cd ../services/blog-service
pip install -r requirements.txt
```

## Step 3: Start Redis

```bash
# Option A: Local Redis
redis-server

# Option B: Port-forward from Kubernetes (Tutorial 15)
kubectl port-forward svc/redis 6379:6379
```

## Step 4: Start AI Server

```bash
cd ai-servers/content-ai
export ANTHROPIC_API_KEY=your-key-here
python server.py
```

You should see:
```
Content AI Server Starting...
Model: claude-3-haiku-20240307
 * Running on http://0.0.0.0:8081
```

## Step 5: Start Blog Service

In a new terminal:

```bash
cd services/blog-service
python app.py
```

You should see:
```
Blog Service with AI Starting...
AI Server: http://localhost:8081
Redis: localhost
 * Running on http://0.0.0.0:8080
```

## Step 6: Test It!

```bash
# Test 1: Generate blog topics
curl -X POST http://localhost:8080/api/blog/suggest-topics \
  -H "Content-Type: application/json" \
  -d '{
    "interests": ["kubernetes", "microservices", "AI"],
    "count": 5
  }' | python -m json.tool

# Expected output:
{
  "topics": [
    "Building Scalable Microservices with Kubernetes",
    "AI-Powered Service Discovery in Kubernetes",
    "Monitoring Microservices: Prometheus + AI",
    "Kubernetes Security Best Practices for AI Workloads",
    "Cost Optimization for AI Microservices"
  ],
  "source": "ai",
  "cached": false
}

# Test 2: Generate blog outline
curl -X POST http://localhost:8080/api/blog/generate-outline \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Getting Started with Kubernetes",
    "audience": "beginners",
    "length": "medium"
  }' | python -m json.tool

# Expected output:
{
  "outline": {
    "introduction": "Brief overview of what Kubernetes is and why it matters",
    "main_points": [
      "Container orchestration basics",
      "Key Kubernetes concepts (Pods, Services, Deployments)",
      "Setting up your first cluster",
      "Deploying your first application",
      "Basic kubectl commands"
    ],
    "conclusion": "Next steps and resources for learning more"
  },
  "source": "ai",
  "cached": false
}

# Test 3: Check metrics
curl http://localhost:8080/metrics | grep ai_

# You should see:
ai_requests_total{endpoint="generate_blog_topics",model="claude-3-haiku-20240307"} 1.0
ai_cache_hits_total 0.0
ai_cache_misses_total 1.0
ai_cost_total{model="claude-3-haiku-20240307"} 0.01
```

## Step 7: Test Caching

Run the same request again:

```bash
curl -X POST http://localhost:8080/api/blog/suggest-topics \
  -H "Content-Type: application/json" \
  -d '{
    "interests": ["kubernetes", "microservices", "AI"],
    "count": 5
  }' | python -m json.tool
```

Notice:
- Response is much faster
- `"cached": true` in the response
- Metrics show `ai_cache_hits_total` increased

## Using Make (Easier)

Alternatively, use the Makefile:

```bash
# Install everything
make install-all

# Start all services
make run-all

# Test
make test
```

## Troubleshooting

### "ANTHROPIC_API_KEY not set"

```bash
# Make sure you've exported it
export ANTHROPIC_API_KEY=sk-ant-your-key

# Verify
echo $ANTHROPIC_API_KEY
```

### "Connection refused to Redis"

```bash
# Check Redis is running
redis-cli ping
# Should return: PONG

# If not running:
redis-server

# Or use Kubernetes:
kubectl port-forward svc/redis 6379:6379
```

### "AI request failed"

```bash
# Check AI server is running
curl http://localhost:8081/health

# Check API key is valid
# Visit: https://console.anthropic.com/
```

### "Failed to parse AI response"

This happens sometimes with AI responses. The code includes fallbacks:
- Will retry with improved prompt
- Falls back to template-based generation
- Check logs for details

### High latency on first request

The first AI call is always slower because:
1. No cache yet
2. API cold start
3. Model initialization

Subsequent requests with same parameters will be cached and instant!

## Next Steps

1. **Try content moderation** - See Part 2 of README
2. **Monitor costs** - Check Prometheus metrics
3. **Experiment with prompts** - Edit `server.py` to improve results
4. **Add your own AI tools** - Create new endpoints
5. **Deploy to Kubernetes** - See Part 7 of README

## Cost Monitoring

```bash
# Check total cost
curl http://localhost:8080/metrics | grep ai_cost_total

# Example output:
ai_cost_total{model="claude-3-haiku-20240307"} 0.03

# This means you've spent $0.03 so far
```

**Haiku pricing** (as of 2024):
- Input: $0.25 per 1M tokens
- Output: $1.25 per 1M tokens
- Typical blog topic request: ~$0.001 (0.1 cents)
- With caching: Even cheaper!

## Example Workflow

```bash
# 1. User asks for blog topics
curl -X POST http://localhost:8080/api/blog/suggest-topics \
  -d '{"interests": ["python", "data science"], "count": 3}'

# 2. User picks a topic
TOPIC="Building Data Pipelines with Python"

# 3. Generate outline
curl -X POST http://localhost:8080/api/blog/generate-outline \
  -d "{\"topic\": \"$TOPIC\", \"audience\": \"intermediate\"}"

# 4. Check what this cost
curl http://localhost:8080/metrics | grep ai_cost
```

## Comparing with Tutorial 16

**Tutorial 16 (Platform Operations):**
```bash
# You ask Claude Code:
"What tables are in my database?"

# Claude uses MCP to query PostgreSQL
# Returns: todos, users, comments, etc.
```

**Tutorial 17 (Dynamic Services):**
```bash
# Your user makes API request
POST /api/blog/suggest-topics

# Your service calls AI
# AI generates topics
# User gets AI-powered response
```

**Key difference**:
- Tutorial 16: AI helps YOU operate the platform
- Tutorial 17: AI helps YOUR USERS use your services

## Switching Between Providers

Want to try both local and cloud? Just change the AI server:

```bash
# Use local Ollama (free)
# Terminal 1:
cd ai-servers/local-ai && python ollama_server.py

# Use cloud Claude (costs money)
# Terminal 1:
export ANTHROPIC_API_KEY=your-key
cd ai-servers/content-ai && python server.py

# Your service doesn't care which one you use!
# It just calls AI_SERVER_URL (defaults to localhost:8081)
```

## Which Should I Use?

**For this tutorial (learning):**
- ✅ **Use Ollama** - Free, learn without limits

**For real projects:**
- Start with Ollama (free development)
- Upgrade to cloud if you need higher quality
- Use caching to reduce costs

See [LOCAL_MODELS.md](./LOCAL_MODELS.md) for detailed comparison!

## Load Testing

```bash
# Install hey (HTTP load tester)
# brew install hey  # or go install github.com/rakyll/hey@latest

# Test without cache (different topics each time)
for i in {1..10}; do
  curl -X POST http://localhost:8080/api/blog/suggest-topics \
    -d "{\"interests\": [\"topic$i\"], \"count\": 3}"
done

# Test with cache (same topics)
hey -n 100 -c 10 -m POST \
  -H "Content-Type: application/json" \
  -d '{"interests": ["kubernetes"], "count": 3}' \
  http://localhost:8080/api/blog/suggest-topics

# Check metrics
curl http://localhost:8080/metrics | grep -E "ai_(cache|latency)"
```

## Integration with Frontend

```javascript
// React component
async function BlogTopicSuggester() {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(false);

  const generateTopics = async () => {
    setLoading(true);

    const response = await fetch('/api/blog/suggest-topics', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        interests: ['kubernetes', 'AI'],
        count: 5
      })
    });

    const data = await response.json();
    setTopics(data.topics);
    setLoading(false);
  };

  return (
    <div>
      <button onClick={generateTopics} disabled={loading}>
        {loading ? 'Generating...' : 'Suggest Topics'}
      </button>

      <ul>
        {topics.map(topic => <li key={topic}>{topic}</li>)}
      </ul>
    </div>
  );
}
```

## Debugging

```bash
# Check AI server logs
cd ai-servers/content-ai
python server.py
# Watch for errors

# Check blog service logs
cd services/blog-service
python app.py
# Watch for errors

# Check Redis
redis-cli
> KEYS ai:*
> GET "ai:generate_blog_topics:..."
> TTL "ai:generate_blog_topics:..."

# Monitor in real-time
watch -n 1 'curl -s http://localhost:8080/metrics | grep ai_'
```

## Success Indicators

✅ AI server responds to /health
✅ Blog service responds to /health
✅ First request generates topics (slow, ~2-5s)
✅ Second identical request is cached (fast, <50ms)
✅ Metrics show increasing ai_requests_total
✅ Redis contains cached responses

You're ready for Tutorial 17! 🚀
