.PHONY: help install-all install-postgres install-prometheus install-kubernetes test-postgres test-prometheus test-kubernetes verify clean

help:
	@echo "Tutorial 16 - MCP Integration"
	@echo "=============================="
	@echo ""
	@echo "Available targets:"
	@echo "  make verify              - Verify your setup"
	@echo "  make install-all         - Install all MCP servers"
	@echo "  make install-postgres    - Install PostgreSQL MCP server"
	@echo "  make install-prometheus  - Install Prometheus MCP server"
	@echo "  make install-kubernetes  - Install Kubernetes MCP server"
	@echo "  make test-postgres       - Test PostgreSQL MCP server"
	@echo "  make test-prometheus     - Test Prometheus MCP server"
	@echo "  make test-kubernetes     - Test Kubernetes MCP server"
	@echo "  make configure           - Generate MCP configuration"
	@echo "  make clean               - Clean Python cache files"
	@echo ""
	@echo "Quick start:"
	@echo "  1. make verify"
	@echo "  2. make install-all"
	@echo "  3. make configure"
	@echo "  4. Edit ~/.config/claude-code/mcp_settings.json"
	@echo "  5. Restart Claude Code"
	@echo ""

verify:
	@echo "Verifying setup..."
	@echo ""
	@echo "Checking Python..."
	@python3 --version || (echo "❌ Python 3 not found" && exit 1)
	@echo "✅ Python found"
	@echo ""
	@echo "Checking kubectl..."
	@kubectl version --client || echo "⚠️  kubectl not found (needed for kubernetes-mcp)"
	@echo ""
	@echo "Checking PostgreSQL connectivity..."
	@psql -h localhost -U postgres -d tododb -c "SELECT 1" > /dev/null 2>&1 && echo "✅ PostgreSQL accessible" || echo "⚠️  PostgreSQL not accessible (start port-forward if needed)"
	@echo ""
	@echo "Checking Prometheus connectivity..."
	@curl -s http://localhost:9090/api/v1/query?query=up > /dev/null 2>&1 && echo "✅ Prometheus accessible" || echo "⚠️  Prometheus not accessible (start port-forward if needed)"
	@echo ""

install-all: install-postgres install-prometheus install-kubernetes
	@echo ""
	@echo "✅ All MCP servers installed!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run 'make configure' to generate configuration"
	@echo "  2. Copy configuration to ~/.config/claude-code/mcp_settings.json"
	@echo "  3. Restart Claude Code"
	@echo ""

install-postgres:
	@echo "Installing PostgreSQL MCP server..."
	cd servers/postgres-mcp && pip install -r requirements.txt
	@echo "✅ PostgreSQL MCP server installed"

install-prometheus:
	@echo "Installing Prometheus MCP server..."
	cd servers/prometheus-mcp && pip install -r requirements.txt
	@echo "✅ Prometheus MCP server installed"

install-kubernetes:
	@echo "Installing Kubernetes MCP server..."
	cd servers/kubernetes-mcp && pip install -r requirements.txt
	@echo "✅ Kubernetes MCP server installed"

test-postgres:
	@echo "Testing PostgreSQL MCP server..."
	@echo "Note: This test requires PostgreSQL to be running"
	@echo ""
	@cd servers/postgres-mcp && \
	export DB_HOST=localhost && \
	export DB_PORT=5432 && \
	export DB_NAME=tododb && \
	export DB_USER=postgres && \
	export DB_PASSWORD=postgres && \
	python3 -m py_compile postgres_server.py && \
	echo "✅ PostgreSQL MCP server syntax valid"

test-prometheus:
	@echo "Testing Prometheus MCP server..."
	@echo "Note: This test requires Prometheus to be running"
	@echo ""
	@cd servers/prometheus-mcp && \
	export PROMETHEUS_URL=http://localhost:9090 && \
	python3 -m py_compile prometheus_server.py && \
	echo "✅ Prometheus MCP server syntax valid"

test-kubernetes:
	@echo "Testing Kubernetes MCP server..."
	@echo "Note: This test requires kubectl to be configured"
	@echo ""
	@cd servers/kubernetes-mcp && \
	python3 -m py_compile kubernetes_server.py && \
	echo "✅ Kubernetes MCP server syntax valid"

configure:
	@echo "Generating MCP configuration..."
	@echo ""
	@CURRENT_DIR=$$(pwd) && \
	echo "{" && \
	echo '  "mcpServers": {' && \
	echo '    "postgres": {' && \
	echo '      "command": "python3",' && \
	echo '      "args": ["'$$CURRENT_DIR'/servers/postgres-mcp/postgres_server.py"],' && \
	echo '      "env": {' && \
	echo '        "DB_HOST": "localhost",' && \
	echo '        "DB_PORT": "5432",' && \
	echo '        "DB_NAME": "tododb",' && \
	echo '        "DB_USER": "postgres",' && \
	echo '        "DB_PASSWORD": "postgres"' && \
	echo '      }' && \
	echo '    },' && \
	echo '    "prometheus": {' && \
	echo '      "command": "python3",' && \
	echo '      "args": ["'$$CURRENT_DIR'/servers/prometheus-mcp/prometheus_server.py"],' && \
	echo '      "env": {' && \
	echo '        "PROMETHEUS_URL": "http://localhost:9090"' && \
	echo '      }' && \
	echo '    },' && \
	echo '    "kubernetes": {' && \
	echo '      "command": "python3",' && \
	echo '      "args": ["'$$CURRENT_DIR'/servers/kubernetes-mcp/kubernetes_server.py"]' && \
	echo '    }' && \
	echo '  }' && \
	echo '}' && \
	echo "" && \
	echo "Copy this configuration to: ~/.config/claude-code/mcp_settings.json" && \
	echo ""

clean:
	@echo "Cleaning Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned"

port-forward-postgres:
	@echo "Port-forwarding PostgreSQL..."
	@echo "Press Ctrl+C to stop"
	kubectl port-forward svc/postgres 5432:5432

port-forward-prometheus:
	@echo "Port-forwarding Prometheus..."
	@echo "Press Ctrl+C to stop"
	kubectl port-forward -n monitoring svc/prometheus 9090:9090

status:
	@echo "MCP Servers Status:"
	@echo "==================="
	@echo ""
	@echo "PostgreSQL MCP:"
	@cd servers/postgres-mcp && python3 -c "import mcp; print('  ✅ MCP SDK installed')" 2>/dev/null || echo "  ❌ MCP SDK not installed"
	@cd servers/postgres-mcp && python3 -c "import psycopg2; print('  ✅ psycopg2 installed')" 2>/dev/null || echo "  ❌ psycopg2 not installed"
	@echo ""
	@echo "Prometheus MCP:"
	@cd servers/prometheus-mcp && python3 -c "import mcp; print('  ✅ MCP SDK installed')" 2>/dev/null || echo "  ❌ MCP SDK not installed"
	@cd servers/prometheus-mcp && python3 -c "import requests; print('  ✅ requests installed')" 2>/dev/null || echo "  ❌ requests not installed"
	@echo ""
	@echo "Kubernetes MCP:"
	@cd servers/kubernetes-mcp && python3 -c "import mcp; print('  ✅ MCP SDK installed')" 2>/dev/null || echo "  ❌ MCP SDK not installed"
	@kubectl version --client > /dev/null 2>&1 && echo "  ✅ kubectl installed" || echo "  ❌ kubectl not installed"
	@echo ""
