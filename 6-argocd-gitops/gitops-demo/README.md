# GitOps Demo - Hello World Application

This directory contains a sample application structured for GitOps deployment with Argo CD.

## Directory Structure

```
gitops-demo/
├── environments/
│   ├── dev/
│   │   └── values.yaml          # Development environment configuration
│   ├── staging/
│   │   └── values.yaml          # Staging environment configuration
│   └── production/
│       └── values.yaml          # Production environment configuration
└── hello-world-app/
    ├── Chart.yaml               # Helm chart metadata
    └── templates/
        ├── deployment.yaml      # Kubernetes deployment
        ├── service.yaml         # Service definition
        ├── ingress.yaml         # Ingress for external access
        └── configmap.yaml       # Application HTML content
```

## How to Use

### 1. Fork/Copy to Your Git Repository

This demo needs to be in a Git repository for Argo CD to access it.

```bash
# Create a new Git repository
git init
git add .
git commit -m "Initial GitOps demo"

# Push to your remote repository (GitHub, GitLab, etc.)
git remote add origin https://github.com/YOUR_USERNAME/m7011e-gitops.git
git push -u origin main
```

### 2. Customize for Your Environment

Edit the values files for each environment and change:

**environments/dev/values.yaml:**
```yaml
domain: helloworld-dev.ltu-m7011e-yourname.se
email: your.email@ltu.se
```

**environments/staging/values.yaml:**
```yaml
domain: helloworld-staging.ltu-m7011e-yourname.se
email: your.email@ltu.se
```

**environments/production/values.yaml:**
```yaml
domain: helloworld-prod.ltu-m7011e-yourname.se
email: your.email@ltu.se
```

### 3. Deploy with Argo CD

See the main tutorial README for complete Argo CD deployment instructions.

**Quick commands:**

```bash
# Create dev environment application
argocd app create hello-world-dev \
  --repo https://github.com/YOUR_USERNAME/m7011e-gitops.git \
  --path hello-world-app \
  --dest-namespace hello-world-dev \
  --values ../environments/dev/values.yaml

# Sync the application
argocd app sync hello-world-dev
```

## Environment Differences

| Environment | Replicas | Domain | Cert Issuer | Purpose |
|-------------|----------|--------|-------------|---------|
| Development | 1 | helloworld-dev.* | staging | Testing new features |
| Staging | 2 | helloworld-staging.* | staging | Pre-production validation |
| Production | 3 | helloworld-prod.* | production | Live user traffic |

## Making Changes

### Update the Application

1. Edit the values file for your environment
2. Commit and push to Git
3. Argo CD automatically detects and syncs (if auto-sync enabled)

**Example - Scale development:**

```bash
# Edit values file
nano environments/dev/values.yaml
# Change replicas: 3

# Commit and push
git commit -am "Scale dev environment to 3 replicas"
git push origin main

# Watch Argo CD sync
argocd app get hello-world-dev
```

### Promote Between Environments

Typical flow: dev → staging → production

```bash
# Test in dev
git checkout -b feature/new-message
# Edit environments/dev/values.yaml
git commit -am "Update message in dev"
git push origin feature/new-message

# After testing, promote to staging
# Edit environments/staging/values.yaml with same changes
git commit -am "Promote to staging"
git push origin feature/new-message

# After staging validation, merge to main for production
git checkout main
git merge feature/new-message
# Edit environments/production/values.yaml
git commit -am "Promote to production"
git push origin main
```

## Testing Locally

Before pushing to Git, test your Helm chart locally:

```bash
# Test dev environment
helm template hello-world-app -f environments/dev/values.yaml .

# Install locally to test namespace
helm install test-dev hello-world-app -f environments/dev/values.yaml -n test-dev --create-namespace

# Cleanup
helm uninstall test-dev -n test-dev
kubectl delete namespace test-dev
```

## Troubleshooting

### Verify Helm Chart Syntax

```bash
helm lint hello-world-app
```

### Check Generated Manifests

```bash
helm template hello-world-app -f environments/dev/values.yaml .
```

### Validate Values

```bash
# Check what values will be used
helm show values hello-world-app
```

## Next Steps

1. Customize the application templates for your needs
2. Add more environments if needed
3. Integrate with CI/CD to update image tags
4. Add more complex applications (databases, microservices)
5. Implement app-of-apps pattern for multiple applications
