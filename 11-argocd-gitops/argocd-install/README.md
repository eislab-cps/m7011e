# Argo CD Installation Helm Chart

This Helm chart simplifies the installation of Argo CD on the LTU Kubernetes cluster for the M7011E course.

## What This Chart Does

1. Installs Argo CD using the official manifests (namespace created via Helm)
2. Configures ingress for web UI access with SSL certificates
3. Sets up resource limits appropriate for the course environment

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

# Wait for installation to complete (this may take 2-3 minutes)
kubectl get pods -n argocd -w
```

The installation job will automatically:
1. Install ArgoCD from official manifests
2. Configure ArgoCD for Traefik ingress (insecure mode with TLS termination)
3. Set the external URL from your `values.yaml`
4. Restart the server to apply configuration

No manual configuration needed!

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
- The namespace is created by Helm using the `--create-namespace` flag
- ArgoCD server runs in insecure mode (HTTP) - TLS is terminated by Traefik
- Resource limits are set for course usage - adjust for production
- Ingress is configured for Traefik (default on LTU cluster)
- SSL certificates use Let's Encrypt staging by default
- The installation job may take a few minutes to complete

## How It Works

The Helm chart uses a Kubernetes Job to:
1. Apply the official ArgoCD installation manifests
2. Automatically configure ArgoCD for Traefik ingress
3. Set up TLS termination at the ingress level
4. Restart the server with the correct configuration

This means you don't need any manual post-installation steps!
