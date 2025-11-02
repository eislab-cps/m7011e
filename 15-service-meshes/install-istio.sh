#!/bin/bash

# Install Istio on Kubernetes
#
# This script:
# 1. Downloads Istio
# 2. Installs Istio with demo profile
# 3. Enables automatic sidecar injection
# 4. Installs observability add-ons (Kiali, Jaeger, Prometheus, Grafana)

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║       Installing Istio Service Mesh                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if istioctl is already installed
if command -v istioctl &> /dev/null; then
    echo "✅ istioctl already installed"
    istioctl version
else
    echo "Downloading Istio..."
    cd ~
    curl -L https://istio.io/downloadIstio | sh -

    # Find the Istio directory
    ISTIO_DIR=$(ls -d ~/istio-* | head -n 1)

    echo "Adding istioctl to PATH..."
    export PATH=$ISTIO_DIR/bin:$PATH

    echo "⚠️  Add this to your ~/.bashrc or ~/.zshrc:"
    echo "export PATH=$ISTIO_DIR/bin:\$PATH"
    echo ""
fi

# Install Istio
echo "Installing Istio with demo profile..."
istioctl install --set profile=demo -y

echo ""
echo "Waiting for Istio control plane to be ready..."
kubectl wait --for=condition=ready pod -l app=istiod -n istio-system --timeout=300s

# Enable automatic sidecar injection for default namespace
echo ""
echo "Enabling automatic sidecar injection for default namespace..."
kubectl label namespace default istio-injection=enabled --overwrite 2>&1 | grep -v "not labeled" || true
echo "✅ Sidecar injection enabled for default namespace"

# Install observability add-ons
echo ""
echo "Installing observability add-ons..."
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/jaeger.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/grafana.yaml

echo ""
echo "Waiting for observability tools to be ready..."
sleep 10
kubectl wait --for=condition=ready pod -l app=kiali -n istio-system --timeout=300s || echo "⚠️  Kiali not ready yet"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║       Istio Installation Complete!                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Installed components:"
echo "  ✅ Istio control plane (istiod)"
echo "  ✅ Istio ingress gateway"
echo "  ✅ Istio egress gateway"
echo "  ✅ Kiali (service mesh dashboard)"
echo "  ✅ Jaeger (distributed tracing)"
echo "  ✅ Prometheus (metrics)"
echo "  ✅ Grafana (dashboards)"
echo ""
echo "Verify installation:"
echo "  kubectl get pods -n istio-system"
echo ""
echo "Access Kiali dashboard:"
echo "  kubectl port-forward -n istio-system svc/kiali 20001:20001"
echo "  Then open: http://localhost:20001"
echo ""
echo "Access Jaeger tracing:"
echo "  kubectl port-forward -n istio-system svc/tracing 16686:80"
echo "  Then open: http://localhost:16686"
echo ""
echo "Access Grafana:"
echo "  kubectl port-forward -n istio-system svc/grafana 3000:3000"
echo "  Then open: http://localhost:3000"
echo ""
