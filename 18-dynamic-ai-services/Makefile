.PHONY: help install-all install-content-ai install-blog-service test clean run-all

help:
	@echo "Tutorial 17 - Dynamic AI-Powered Services"
	@echo "==========================================="
	@echo ""
	@echo "Available targets:"
	@echo "  make install-all         - Install all services"
	@echo "  make install-content-ai  - Install content AI server"
	@echo "  make install-blog-service - Install blog service"
	@echo "  make run-content-ai      - Run content AI server"
	@echo "  make run-blog-service    - Run blog service"
	@echo "  make test                - Test the services"
	@echo "  make clean               - Clean Python cache"
	@echo ""
	@echo "Quick start:"
	@echo "  1. export ANTHROPIC_API_KEY=your-key"
	@echo "  2. make install-all"
	@echo "  3. Start Redis: redis-server (in another terminal)"
	@echo "  4. make run-content-ai (in another terminal)"
	@echo "  5. make run-blog-service (in another terminal)"
	@echo "  6. make test"
	@echo ""
	@echo "Requirements:"
	@echo "  - Python 3.10+"
	@echo "  - Anthropic API key"
	@echo "  - Redis running"
	@echo ""

install-all: install-content-ai install-blog-service install-moderation-ai install-comment-service install-local-ai
	@echo ""
	@echo "✅ All services installed!"
	@echo ""
	@echo "Next steps (choose one AI provider):"
	@echo ""
	@echo "Option A: Local AI (FREE, no API key):"
	@echo "  1. brew install ollama  # or download from ollama.ai"
	@echo "  2. ollama serve"
	@echo "  3. ollama pull llama3.2"
	@echo "  4. make run-local-ai"
	@echo "  5. make run-blog-service (in another terminal)"
	@echo ""
	@echo "Option B: Cloud AI (requires API key):"
	@echo "  1. export ANTHROPIC_API_KEY=your-key"
	@echo "  2. make run-content-ai"
	@echo "  3. make run-blog-service (in another terminal)"
	@echo ""

install-content-ai:
	@echo "Installing content AI server..."
	cd ai-servers/content-ai && pip install -r requirements.txt
	@echo "✅ Content AI server installed"

install-moderation-ai:
	@echo "Installing moderation AI server..."
	cd ai-servers/moderation-ai && pip install -r requirements.txt
	@echo "✅ Moderation AI server installed"

install-blog-service:
	@echo "Installing blog service..."
	cd services/blog-service && pip install -r requirements.txt
	@echo "✅ Blog service installed"

install-comment-service:
	@echo "Installing comment service..."
	cd services/comment-service && pip install -r requirements.txt
	@echo "✅ Comment service installed"

install-local-ai:
	@echo "Installing local AI server (Ollama)..."
	cd ai-servers/local-ai && pip install -r requirements.txt
	@echo "✅ Local AI server installed"
	@echo ""
	@echo "Next: Install Ollama"
	@echo "  macOS: brew install ollama"
	@echo "  Linux: curl -fsSL https://ollama.ai/install.sh | sh"
	@echo "  Windows: https://ollama.ai/download"
	@echo ""

run-content-ai:
	@echo "Starting content AI server..."
	@echo "Make sure ANTHROPIC_API_KEY is set!"
	@echo ""
	@if [ -z "$$ANTHROPIC_API_KEY" ]; then \
		echo "❌ ANTHROPIC_API_KEY not set!"; \
		echo "Run: export ANTHROPIC_API_KEY=your-key"; \
		exit 1; \
	fi
	cd ai-servers/content-ai && python server.py

run-moderation-ai:
	@echo "Starting moderation AI server..."
	@echo "Make sure ANTHROPIC_API_KEY is set!"
	@echo ""
	@if [ -z "$$ANTHROPIC_API_KEY" ]; then \
		echo "❌ ANTHROPIC_API_KEY not set!"; \
		exit 1; \
	fi
	cd ai-servers/moderation-ai && python server.py

run-blog-service:
	@echo "Starting blog service..."
	@echo "Make sure Redis and content-ai are running!"
	@echo ""
	cd services/blog-service && python app.py

run-comment-service:
	@echo "Starting comment service..."
	@echo "Make sure PostgreSQL and moderation-ai are running!"
	@echo ""
	cd services/comment-service && python app.py

run-local-ai:
	@echo "Starting local AI server (Ollama)..."
	@echo ""
	@echo "Prerequisites:"
	@echo "  1. Ollama must be running: ollama serve"
	@echo "  2. Model must be pulled: ollama pull llama3.2"
	@echo ""
	@echo "Testing Ollama connection..."
	@curl -s http://localhost:11434/api/tags > /dev/null 2>&1 || (echo "❌ Ollama not running! Start with: ollama serve" && exit 1)
	@echo "✅ Ollama is running"
	@echo ""
	@cd ai-servers/local-ai && python ollama_server.py

test:
	@echo "Testing services..."
	@echo ""
	@echo "1. Testing content AI health..."
	@curl -s http://localhost:8081/health | python -m json.tool || echo "❌ Content AI not running"
	@echo ""
	@echo "2. Testing blog service health..."
	@curl -s http://localhost:8080/health | python -m json.tool || echo "❌ Blog service not running"
	@echo ""
	@echo "3. Generating blog topics..."
	@curl -s -X POST http://localhost:8080/api/blog/suggest-topics \
		-H "Content-Type: application/json" \
		-d '{"interests": ["kubernetes", "AI"], "count": 3}' | python -m json.tool
	@echo ""
	@echo "4. Checking metrics..."
	@curl -s http://localhost:8080/metrics | grep ai_ | head -10
	@echo ""
	@echo "✅ Tests complete!"

test-moderation:
	@echo "Testing moderation service..."
	@echo ""
	@echo "1. Testing moderation AI health..."
	@curl -s http://localhost:8082/health | python -m json.tool
	@echo ""
	@echo "2. Testing comment service health..."
	@curl -s http://localhost:8083/health | python -m json.tool
	@echo ""
	@echo "3. Posting a safe comment..."
	@curl -s -X POST http://localhost:8083/api/comments \
		-H "Content-Type: application/json" \
		-d '{"user_id": 1, "post_id": 1, "text": "Great article! Very helpful."}' | python -m json.tool
	@echo ""

check-redis:
	@echo "Checking Redis..."
	@redis-cli ping > /dev/null 2>&1 && echo "✅ Redis is running" || echo "❌ Redis is not running (start with: redis-server)"

check-api-key:
	@echo "Checking API keys and Ollama..."
	@echo ""
	@echo "Cloud API (Anthropic):"
	@if [ -z "$$ANTHROPIC_API_KEY" ]; then \
		echo "  ⚠️  ANTHROPIC_API_KEY not set (optional if using Ollama)"; \
	else \
		echo "  ✅ ANTHROPIC_API_KEY is set"; \
	fi
	@echo ""
	@echo "Local AI (Ollama):"
	@curl -s http://localhost:11434/api/tags > /dev/null 2>&1 && \
		echo "  ✅ Ollama is running" || \
		echo "  ⚠️  Ollama not running (optional if using cloud API)"
	@echo ""
	@echo "At least one AI provider should be available!"
	@echo ""

verify: check-redis check-api-key
	@echo ""
	@echo "Checking Python version..."
	@python3 --version
	@echo ""
	@echo "Checking installations..."
	@python3 -c "import flask; print('✅ Flask installed')" 2>/dev/null || echo "❌ Flask not installed (run: make install-all)"
	@python3 -c "import anthropic; print('✅ Anthropic SDK installed')" 2>/dev/null || echo "❌ Anthropic not installed (run: make install-all)"
	@python3 -c "import redis; print('✅ Redis client installed')" 2>/dev/null || echo "❌ Redis client not installed (run: make install-all)"
	@echo ""

clean:
	@echo "Cleaning Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned"

status:
	@echo "Service Status:"
	@echo "==============="
	@echo ""
	@echo "AI Servers:"
	@curl -s http://localhost:8081/health > /dev/null 2>&1 && \
		(curl -s http://localhost:8081/health | grep -q "local-ai" && \
			echo "  ✅ Local AI (Ollama): Running (port 8081)" || \
			echo "  ✅ Cloud AI: Running (port 8081)") || \
		echo "  ❌ AI Server: Not running (port 8081)"
	@curl -s http://localhost:8082/health > /dev/null 2>&1 && echo "  ✅ Moderation AI: Running (port 8082)" || echo "  ⚠️  Moderation AI: Not running (port 8082)"
	@echo ""
	@echo "Services:"
	@curl -s http://localhost:8080/health > /dev/null 2>&1 && echo "  ✅ Blog Service: Running (port 8080)" || echo "  ❌ Blog Service: Not running"
	@curl -s http://localhost:8083/health > /dev/null 2>&1 && echo "  ✅ Comment Service: Running (port 8083)" || echo "  ⚠️  Comment Service: Not running"
	@echo ""
	@echo "Infrastructure:"
	@redis-cli ping > /dev/null 2>&1 && echo "  ✅ Redis: Running" || echo "  ❌ Redis: Not running"
	@curl -s http://localhost:11434/api/tags > /dev/null 2>&1 && echo "  ✅ Ollama: Running" || echo "  ⚠️  Ollama: Not running (optional)"
	@echo ""

metrics:
	@echo "AI Metrics:"
	@echo "==========="
	@echo ""
	@echo "Blog Service:"
	@curl -s http://localhost:8080/metrics | grep ai_ || echo "Service not running"
	@echo ""
	@echo "Content AI Server:"
	@curl -s http://localhost:8081/metrics | grep ai_ || echo "Service not running"
	@echo ""

logs-blog:
	@echo "Recent AI requests from blog service:"
	@curl -s http://localhost:8080/metrics | grep -E "ai_requests_total|ai_cache"

logs-ai:
	@echo "Recent AI API calls:"
	@curl -s http://localhost:8081/metrics | grep -E "ai_calls_total|ai_tokens"

cost:
	@echo "Estimated AI Costs:"
	@echo "==================="
	@echo ""
	@curl -s http://localhost:8080/metrics | grep ai_cost || echo "No cost data yet"
	@echo ""
	@echo "Note: Costs are estimated based on token usage"
	@echo "Haiku pricing: ~$0.001 per typical request"
	@echo ""
