# Kubernetes Tutorials
A hands-on introduction to Kubernetes and application deployment.

## Tutorials
### [1-basic-webapp](./1-basic-webapp/)
Build a simple REST API web application with Flask and vanilla JavaScript.

**Covers:**
- Client-server architecture and communication
- REST vs JSON-RPC comparison
- Flask REST API development
- Frontend-backend communication with Fetch API
- CORS and HTTP methods
- JSON data format
- In-memory data storage

### [2-k8s-getting-started](./2-k8s-getting-started/)
Set up your development environment and connect to the Kubernetes cluster.

**Covers:**
- Installing kubectl, helm, and Docker/Podman
- Connecting to the LTU Kubernetes cluster via Rancher
- Configuring kubectl with cluster credentials

### [3-k8s-helloworld](./3-k8s-helloworld/)
Deploy a web application using Helm charts with automatic SSL certificates.

**Covers:**
- Helm templating and package management
- Kubernetes resources (Deployments, Services, Ingress, ConfigMaps)
- Automatic HTTPS with Let's Encrypt and cert-manager
- Application deployment and troubleshooting

### [4-postgresql](./4-postgresql/)
Deploy a PostgreSQL database on Kubernetes using Helm charts with persistent storage.

**Covers:**
- PostgreSQL deployment using StatefulSets
- Persistent storage with PersistentVolumeClaims
- Database configuration with ConfigMaps
- Port forwarding to access databases locally
- Database client tools installation and usage
