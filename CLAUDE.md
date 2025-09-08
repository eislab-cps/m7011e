# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview
This repository contains educational materials for the **Design of Dynamic Web Systems (M7011E)** course at Luleå University of Technology. It focuses on Kubernetes-based web application deployment using Helm charts and includes hands-on tutorials for students.

## Repository Structure

### Main Directories
- `tutorials/` - Step-by-step tutorials covering web application deployment on Kubernetes
- `labs/` - Assignment and lab materials (currently empty)
- `old/` - Legacy Helm charts and Kubernetes configurations for reference

### Key Tutorial Components
- `tutorials/1-getting-started/` - Development environment setup and cluster connection
- `tutorials/2-k8s-helloworld/` - Complete Helm chart example with SSL/TLS automation

## Common Development Commands

### Kubernetes Operations
```bash
# Create namespace
kubectl create namespace <namespace-name>

# Deploy with Helm
helm install <release-name> -f values.yaml -n <namespace> .

# Update deployment
helm upgrade <release-name> -f values.yaml -n <namespace> .

# Check deployment status
kubectl get all -n <namespace>

# View pod logs
kubectl logs -l app=<app-name> -n <namespace>

# Cleanup (delete entire namespace)
kubectl delete namespace <namespace-name>
```

### Helm Development
```bash
# Validate template rendering
helm template <release-name> -f values.yaml .

# Install chart from current directory
helm install <release-name> -f values.yaml -n <namespace> .

# List releases in namespace
helm list -n <namespace>

# Rollback to previous version
helm rollback <release-name> -n <namespace>
```

## Architecture Patterns

### Helm Chart Structure
The repository follows standard Helm chart conventions:
- `Chart.yaml` - Chart metadata and versioning
- `values.yaml` - Configuration values with domain and application settings
- `templates/` - Kubernetes resource templates (Deployment, Service, Ingress, ConfigMap)

### SSL/TLS Automation
Uses **cert-manager** with Let's Encrypt for automatic certificate provisioning:
- `letsencrypt-staging` - For development and testing
- `letsencrypt-prod` - For production deployments
- Automatic certificate renewal via ACME protocol

### Resource Management
- **Namespaces** - Isolation and organization of student applications
- **ConfigMaps** - HTML content and application configuration
- **Ingress** - External access with automatic SSL termination using Traefik

## Domain Configuration
Student assignments use personalized subdomains following the pattern:
`<app-name>.ltu-m7011e-<student-name>.se`

When working with tutorials or examples, ensure domain names in `values.yaml` files match the assigned student domain structure.

## Troubleshooting Commands
```bash
# Check certificate status
kubectl get certificate -n <namespace>

# Verify DNS resolution
nslookup <domain-name>

# Describe ingress configuration
kubectl describe ingress <ingress-name> -n <namespace>

# Check pod events and status
kubectl describe pods -n <namespace>
```