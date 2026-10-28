#!/bin/bash
# Install a matching Istio control plane and sample observability add-ons.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

ISTIO_VERSION="${ISTIO_VERSION:-1.31.3}"
ISTIO_DOWNLOAD_DIR="${ISTIO_DOWNLOAD_DIR:-$PWD/.istio}"
ISTIO_DIR="$ISTIO_DOWNLOAD_DIR/istio-$ISTIO_VERSION"

if [ ! -x "$ISTIO_DIR/bin/istioctl" ]; then
    mkdir -p "$ISTIO_DOWNLOAD_DIR"
    (
        cd "$ISTIO_DOWNLOAD_DIR"
        curl -fsSL https://istio.io/downloadIstio | ISTIO_VERSION="$ISTIO_VERSION" sh -
    )
fi

export PATH="$ISTIO_DIR/bin:$PATH"
istioctl version --remote=false

# Register the OTLP collector; installing Jaeger alone does not enable tracing.
cat > "$ISTIO_DOWNLOAD_DIR/tracing-install.yaml" <<'YAML'
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  profile: demo
  meshConfig:
    enableTracing: true
    extensionProviders:
    - name: jaeger
      opentelemetry:
        service: jaeger-collector.istio-system.svc.cluster.local
        port: 4317
YAML

istioctl install -f "$ISTIO_DOWNLOAD_DIR/tracing-install.yaml" -y
kubectl rollout status deployment/istiod -n istio-system --timeout=300s
kubectl label namespace default istio-injection=enabled --overwrite

# Use the sample add-ons shipped with this exact Istio version.
for addon in prometheus grafana jaeger kiali; do
    kubectl apply -f "$ISTIO_DIR/samples/addons/$addon.yaml"
done

kubectl apply -f - <<'YAML'
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata:
  name: mesh-tracing
  namespace: istio-system
spec:
  tracing:
  - providers:
    - name: jaeger
    randomSamplingPercentage: 100
YAML

for component in prometheus grafana jaeger kiali; do
    kubectl rollout status "deployment/$component" -n istio-system --timeout=300s
done

printf '\nIstio and sample observability add-ons are ready.\n'
printf 'For this terminal, run: export PATH="%s/bin:$PATH"\n' "$ISTIO_DIR"
printf 'Kiali: kubectl port-forward -n istio-system svc/kiali 20001:20001\n'
printf 'Jaeger: kubectl port-forward -n istio-system svc/tracing 16686:80\n'
printf 'Grafana: kubectl port-forward -n istio-system svc/grafana 3000:3000\n'
