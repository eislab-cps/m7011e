.PHONY: help install check-ollama generate-example validate clean

help:
	@echo "AI Documentation Generator - Tutorial 18"
	@echo ""
	@echo "Available targets:"
	@echo "  make install          - Install dependencies"
	@echo "  make check-ollama     - Check if Ollama is running"
	@echo "  make generate-example - Generate documentation for example service"
	@echo "  make validate         - Validate generated documentation"
	@echo "  make clean            - Clean generated documentation"
	@echo ""
	@echo "Quick start:"
	@echo "  1. make install"
	@echo "  2. Start Ollama (in another terminal): ollama serve"
	@echo "  3. make generate-example"
	@echo "  4. make validate"

install:
	@echo "Installing dependencies..."
	pip install -r scripts/requirements.txt
	@echo "✅ Dependencies installed"

check-ollama:
	@echo "Checking Ollama..."
	@curl -s http://localhost:11434/api/tags > /dev/null 2>&1 && \
		echo "✅ Ollama is running" || \
		(echo "❌ Ollama not running!" && \
		 echo "" && \
		 echo "Start Ollama with: ollama serve" && \
		 echo "Or use cloud AI server from Tutorial 17" && \
		 exit 1)

generate-example: check-ollama
	@echo "Generating documentation for user_service example..."
	@cd ../17-dynamic-ai-services/ai-servers/local-ai && \
		(lsof -ti:8081 | xargs kill -9 2>/dev/null || true) && \
		python ollama_server.py > /tmp/ai-server.log 2>&1 & \
		echo $$! > /tmp/ai-server.pid
	@sleep 2
	@python scripts/generate_docs.py examples/user_service.py
	@kill `cat /tmp/ai-server.pid` 2>/dev/null || true
	@rm -f /tmp/ai-server.pid
	@echo ""
	@echo "✅ Documentation generated!"
	@echo ""
	@echo "View the results:"
	@echo "  cat docs/user_service/README.md"
	@echo "  cat docs/user_service/architecture.mmd"
	@echo "  cat docs/user_service/openapi.yaml"

validate:
	@if [ ! -d "docs/user_service" ]; then \
		echo "❌ No documentation found. Run 'make generate-example' first."; \
		exit 1; \
	fi
	@python scripts/validate_docs.py docs/user_service

clean:
	@echo "Cleaning generated documentation..."
	@rm -rf docs/
	@echo "✅ Cleaned"

# Additional targets for different documentation types

generate-architecture:
	@echo "Generating architecture diagram only..."
	@python -c "from scripts.generate_docs import *; import sys; \
		code = read_code_file('examples/user_service.py'); \
		diagram = generate_architecture_diagram(code, 'user_service'); \
		print(diagram)"

generate-openapi:
	@echo "Generating OpenAPI spec only..."
	@python -c "from scripts.generate_docs import *; import sys; \
		code = read_code_file('examples/user_service.py'); \
		spec = generate_openapi_spec(code, 'user_service'); \
		print(spec)"

# Examples of common documentation tasks

example-prompts:
	@echo "Example AI prompts for documentation:"
	@echo ""
	@echo "1. Generate architecture diagram:"
	@echo "   'Analyze this service and create a Mermaid architecture diagram showing components and data flow'"
	@echo ""
	@echo "2. Generate sequence diagram:"
	@echo "   'Create a Mermaid sequence diagram for the user registration flow'"
	@echo ""
	@echo "3. Generate API docs:"
	@echo "   'Generate OpenAPI 3.0 specification for all endpoints'"
	@echo ""
	@echo "4. Generate README:"
	@echo "   'Create a comprehensive README with features, setup, and usage examples'"
	@echo ""
	@echo "Try these in: ollama run llama3.2"

test-mermaid:
	@echo "Testing Mermaid diagram rendering..."
	@echo "Opening mermaid.live in browser..."
	@open "https://mermaid.live" || xdg-open "https://mermaid.live" || echo "Visit https://mermaid.live to test diagrams"
