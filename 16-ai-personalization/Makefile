.PHONY: help install-training install-service train build push deploy clean verify test-local

# Configuration
DOCKER_USERNAME ?= johan
IMAGE_NAME = recommendation-service
IMAGE_TAG ?= latest
FULL_IMAGE = $(DOCKER_USERNAME)/$(IMAGE_NAME):$(IMAGE_TAG)

help:
	@echo "Tutorial 15 - AI Personalization"
	@echo "================================="
	@echo ""
	@echo "Available targets:"
	@echo "  make verify          - Verify your setup"
	@echo "  make install-training - Install training dependencies"
	@echo "  make install-service  - Install service dependencies"
	@echo "  make train           - Train the ML model"
	@echo "  make test-local      - Run service locally"
	@echo "  make build           - Build Docker image"
	@echo "  make push            - Push Docker image to registry"
	@echo "  make deploy          - Deploy to Kubernetes"
	@echo "  make clean           - Clean generated files"
	@echo ""
	@echo "Quick start:"
	@echo "  make verify"
	@echo "  make install-training"
	@echo "  make train"
	@echo "  make install-service"
	@echo "  make test-local"
	@echo ""
	@echo "For Kubernetes deployment:"
	@echo "  export DOCKER_USERNAME=your-username"
	@echo "  make build"
	@echo "  make push"
	@echo "  make deploy"
	@echo ""

verify:
	@echo "Running setup verification..."
	@./verify-setup.sh

install-training:
	@echo "Installing training dependencies..."
	cd training && pip install -r requirements.txt
	@echo "✅ Training dependencies installed"

install-service:
	@echo "Installing service dependencies..."
	cd service && pip install -r requirements.txt
	@echo "✅ Service dependencies installed"

train:
	@echo "Training ML model..."
	cd training && python3 train_model.py
	@echo ""
	@echo "✅ Model trained successfully!"
	@echo "Copying model files to service directory..."
	cp training/*.pkl service/
	@echo "✅ Model files copied to service/"
	@ls -lh service/*.pkl

build: train
	@echo "Building Docker image: $(FULL_IMAGE)"
	cd service && docker build -t $(FULL_IMAGE) .
	@echo "✅ Docker image built: $(FULL_IMAGE)"

push:
	@echo "Pushing Docker image: $(FULL_IMAGE)"
	docker push $(FULL_IMAGE)
	@echo "✅ Image pushed to registry"

deploy:
	@echo "Deploying to Kubernetes..."
	@echo "1. Deploying Redis..."
	kubectl apply -f redis-deployment.yaml
	@echo ""
	@echo "2. Updating recommendation service image reference..."
	@if [ "$(DOCKER_USERNAME)" != "johan" ]; then \
		sed -i.bak "s|johan/recommendation-service:latest|$(FULL_IMAGE)|g" recommendation-service.yaml; \
		echo "   Updated image to: $(FULL_IMAGE)"; \
	else \
		echo "   Using default image: $(FULL_IMAGE)"; \
	fi
	@echo ""
	@echo "3. Deploying recommendation service..."
	kubectl apply -f recommendation-service.yaml
	@echo ""
	@echo "✅ Deployment complete!"
	@echo ""
	@echo "Check status with:"
	@echo "  kubectl get pods"
	@echo "  kubectl get svc"

test-local:
	@echo "Starting recommendation service locally..."
	@echo "Press Ctrl+C to stop"
	@echo ""
	@if [ ! -f service/user_features.pkl ]; then \
		echo "⚠️  Model files not found. Running 'make train' first..."; \
		$(MAKE) train; \
	fi
	cd service && python3 recommendation_service.py

clean:
	@echo "Cleaning generated files..."
	rm -f training/*.pkl
	rm -f service/*.pkl
	rm -f training/__pycache__
	rm -f service/__pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned"

test-api:
	@echo "Testing recommendation service API..."
	@echo ""
	@echo "1. Health check:"
	@curl -s http://localhost:8080/health | python3 -m json.tool || echo "Service not running?"
	@echo ""
	@echo "2. Get recommendations for user 1:"
	@curl -s http://localhost:8080/api/recommendations/1 | python3 -m json.tool || echo "Service not running?"
	@echo ""
	@echo "3. Get popular items:"
	@curl -s http://localhost:8080/api/popular | python3 -m json.tool || echo "Service not running?"
	@echo ""
	@echo "4. Metrics:"
	@curl -s http://localhost:8080/metrics | grep recommendation || echo "Service not running?"

test-k8s:
	@echo "Testing recommendation service on Kubernetes..."
	@POD=$$(kubectl get pod -l app=recommendation-service -o jsonpath='{.items[0].metadata.name}' 2>/dev/null); \
	if [ -z "$$POD" ]; then \
		echo "❌ No recommendation-service pod found"; \
		exit 1; \
	fi; \
	echo "Using pod: $$POD"; \
	echo ""; \
	echo "1. Health check:"; \
	kubectl exec -it $$POD -- curl -s http://localhost:8080/health | python3 -m json.tool; \
	echo ""; \
	echo "2. Get recommendations:"; \
	kubectl exec -it $$POD -- curl -s http://localhost:8080/api/recommendations/1 | python3 -m json.tool; \
	echo ""; \
	echo "✅ Service is working on Kubernetes!"

logs:
	@POD=$$(kubectl get pod -l app=recommendation-service -o jsonpath='{.items[0].metadata.name}' 2>/dev/null); \
	if [ -z "$$POD" ]; then \
		echo "❌ No recommendation-service pod found"; \
		exit 1; \
	fi; \
	echo "Showing logs for: $$POD"; \
	kubectl logs -f $$POD

status:
	@echo "Kubernetes Status:"
	@echo "=================="
	@echo ""
	@echo "Pods:"
	@kubectl get pods -l app=recommendation-service -o wide
	@kubectl get pods -l app=redis -o wide
	@echo ""
	@echo "Services:"
	@kubectl get svc recommendation-service redis
	@echo ""
	@echo "Deployments:"
	@kubectl get deployment recommendation-service redis
