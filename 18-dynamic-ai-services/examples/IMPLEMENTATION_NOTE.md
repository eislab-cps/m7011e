# Implementation Note

## Where is the code?

The complete, production-ready Python code for all services is included in **README.md**:

- **Part 1**: Blog service + Content AI server (full working code)
- **Part 2**: Comment service + Moderation AI server (full working code)
- **Part 3-6**: Advanced patterns (caching, fallbacks, cost management, A/B testing)

## Why in the README?

This tutorial is about **patterns and architecture** for integrating AI into services. The README provides:

1. **Complete working examples** - Copy-paste ready code
2. **Inline explanations** - Code with context
3. **Progressive complexity** - From simple to advanced
4. **Reference documentation** - Easy to search and learn from

## How to use this tutorial

### Option 1: Copy from README (Recommended)

1. Read through the README
2. Copy the code sections for the service you want to build
3. Create the files as shown (`services/blog-service/app.py`, etc.)
4. Run with `make install-all` and `make run-*`

### Option 2: Use the examples here

This directory contains simplified starter templates. The README has the full implementations.

### Option 3: Build your own

Use the patterns from the README to build AI-powered features in your own services!

## Quick Reference

**Blog Service Architecture:**
```
User Request → Blog Service (Flask) → Content AI Server → Anthropic Claude
                    ↓                        ↓
              Cache (Redis) ←────────────────┘
```

**Code Location in README:**
- `services/blog-service/app.py` - Part 1
- `ai-servers/content-ai/server.py` - Part 1
- `services/comment-service/app.py` - Part 2
- `ai-servers/moderation-ai/server.py` - Part 2

## Examples in this directory

- `simple-blog-service.py` - Minimal AI-powered service
- `simple-ai-server.py` - Minimal AI server
- `docker-compose.yml` - Run everything with Docker
- `kubernetes.yaml` - Deploy to Kubernetes

## Getting Started

```bash
# 1. Read README.md Part 1
# 2. Copy the code for blog service and content-ai server
# 3. Install dependencies
make install-all

# 4. Set your API key
export ANTHROPIC_API_KEY=your-key

# 5. Run the services
make run-content-ai   # Terminal 1
make run-blog-service # Terminal 2

# 6. Test it
make test
```

## Learning Path

1. **Start with Part 1** (README) - Content generation
2. **Read the code carefully** - Understand the patterns
3. **Try Part 2** - Content moderation
4. **Explore Part 3-6** - Advanced patterns
5. **Build your own** - Apply to your services

The goal is to learn the **architecture and patterns**, not just copy-paste code!
