# Argo CD Installation Helm Chart

This Helm chart simplifies the installation of Argo CD on the LTU Kubernetes cluster for the M7011E course.

## What This Chart Does

1. Creates the `argocd` namespace
2. Installs Argo CD using the official manifests
3. Configures ingress for web UI access with SSL certificates
4. Sets up resource limits appropriate for the course environment

## Prerequisites

- kubectl configured and connected to LTU cluster
- Helm 3 installed
- Access to a domain for Argo CD UI (e.g., argocd.ltu-m7011e-yourname.se)

## Configuration

Edit `values.yaml` before installation:

```yaml
argocd:
  domain: argocd.ltu-m7011e-johan.se  # Change to your domain
  email: your.email@ltu.se            # Change to your email
```

## Installation

```bash
# Install Argo CD (namespace will be created automatically)
helm install argocd -f values.yaml -n argocd --create-namespace .

# Wait for installation to complete
kubectl get pods -n argocd -w
```

## Access Argo CD

### Get Initial Password

```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d && echo
```

### Port Forward (Local Access)

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Then open: https://localhost:8080

### Ingress (Domain Access)

If you configured a domain, access at: https://argocd.ltu-m7011e-yourname.se

## Login Credentials

- **Username**: `admin`
- **Password**: (from the secret above)

## Verify Installation

```bash
# Check all pods are running
kubectl get pods -n argocd

# Check ingress
kubectl get ingress -n argocd

# Check Argo CD version
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server -o jsonpath='{.items[0].spec.containers[0].image}'
```

## Uninstall

```bash
helm uninstall argocd -n argocd
kubectl delete namespace argocd
```

## Troubleshooting

### Pods Not Starting

```bash
kubectl describe pods -n argocd
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-server
```

### Ingress Not Working

```bash
kubectl describe ingress argocd-server -n argocd
kubectl get certificate -n argocd
```

### Certificate Issues

```bash
# Check cert-manager
kubectl get certificate -n argocd
kubectl describe certificate argocd-tls -n argocd

# Switch to production issuer in values.yaml when ready
# certIssuer: letsencrypt-prod
```

## Notes

- This chart uses the official Argo CD installation manifests
- Resource limits are set for course usage - adjust for production
- Ingress is configured for Traefik (default on LTU cluster)
- SSL certificates use Let's Encrypt staging by default
- The installation job may take a few minutes to complete
