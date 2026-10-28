# Tutorial 7 - Deploy a simple web app on Kubernetes 

This tutorial will guide you through deploying a simple application using Helm to verify your Kubernetes setup is working correctly.

Run the following commands from `07-k8s-helloworld/`. The cluster needs the `traefik` ingress class, cert-manager, a `letsencrypt-staging` ClusterIssuer, and DNS for your chosen hostname pointing to the ingress controller. Check these with course staff if you use another cluster.

## Understanding Helm
Helm is a package manager for Kubernetes that simplifies application deployment and management. Think of it like `apt` for Ubuntu or `brew` for macOS, but specifically designed for Kubernetes applications.

### How Helm Works
Helm uses a templating system to generate Kubernetes YAML manifests. Here's how the files in this project work together:

**Project Structure:**
```
07-k8s-helloworld/
├── Chart.yaml              # Chart metadata and version info
├── values.yaml             # Configuration values
└── templates/              # Template directory
    ├── deployment.yaml     # Pod deployment template
    ├── service.yaml        # Service template (networking)
    ├── ingress.yaml        # External access template
    └── configmap.yaml      # HTML content template
```

**Template Processing:**
1. **Values**: The `values.yaml` file contains your configuration (domain, app name, replicas, etc.)
2. **Templates**: Files in `templates/` contain Kubernetes YAML with placeholders like `{{ .Values.app.name }}`
3. **Processing**: Helm substitutes placeholders with actual values from `values.yaml`
4. **Deployment**: Generated YAML manifests are applied to your cluster

**Example Template Usage:**
In `templates/deployment.yaml`, you'll see:
```yaml
name: {{ .Values.app.name }}        # Becomes: hello-world
replicas: {{ .Values.app.replicas }} # Becomes: 1
```

## Project Components
This Helm chart creates several Kubernetes resources:

- **Deployment**: Manages your application pods (nginx containers)
- **Service**: Provides internal networking to reach your pods
- **Ingress**: Enables external access with automatic SSL/TLS certificates
- **ConfigMap**: Contains your HTML content served by nginx

### Automatic SSL Certificate Management
The ingress configuration automatically provisions SSL/TLS certificates using **Let's Encrypt** and **cert-manager**. Here's how it works:

**ACME Protocol**: ACME (Automatic Certificate Management Environment) is a protocol that enables automatic SSL certificate issuance and renewal. It's the standard protocol used by Let's Encrypt to verify domain ownership and issue certificates without manual intervention.

**Certificate Issuer Configuration**:
In the ingress template, you'll see metadata like this:
```yaml
metadata:
  name: {{ .Values.app.name }}
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-staging
```

The `cert-manager.io/cluster-issuer` annotation tells cert-manager which certificate issuer to use:

- **letsencrypt-staging**: Used for testing and development. Issues certificates from Let's Encrypt's staging environment, which has higher rate limits but produces certificates that browsers will show as "untrusted" (perfect for testing)
- **letsencrypt-prod**: Used for production environments. Issues trusted certificates from Let's Encrypt's production environment, and has stricter [rate limits](https://letsencrypt.org/docs/rate-limits/), including separate limits for registered domains and repeated identifier sets

**The Process**:
1. When you deploy the application, cert-manager detects the `cert-manager.io/cluster-issuer: letsencrypt-staging` annotation
2. Cert-manager uses the ACME protocol to contact Let's Encrypt's servers
3. Let's Encrypt validates that you control the domain (through HTTP-01 challenge)
4. Once verified, Let's Encrypt issues a free SSL certificate
5. The certificate is stored as a Kubernetes secret and automatically applied to your ingress

**Benefits**:
- Free SSL certificates from a trusted Certificate Authority
- Automatic renewal before certificate expiration
- No manual certificate management required
- Industry-standard security for your web application

HTTPS becomes available after DNS, ingress routing, and certificate issuance succeed. The default staging certificate is untrusted by browsers. Switch the annotation to an existing `letsencrypt-prod` issuer when you are ready for a trusted certificate.

## Configure Your Application
### 1. Edit the Values File
Modify `values.yaml` to match your assigned domain:

```yaml
# values.yaml
app:
  name: hello-world
  replicas: 1

domain: helloworld.ltu-m7011e-johan.se  # Change this to your domain

message: "Hello from Kubernetes with SSL!"
```

**Important**: Replace `ltu-m7011e-johan.se` with your actual assigned domain name. The chart does not create the ClusterIssuer; its ACME email is configured by the cluster administrator, not by this chart's unused `email` value.

## Understanding Kubernetes Namespaces
A **namespace** in Kubernetes is like a virtual cluster within your physical cluster. It provides:

- **Isolation**: Resources in different namespaces are separated from each other
- **Organization**: Group related resources together (e.g., development, staging, production)
- **Resource Management**: Apply quotas and policies per namespace
- **Naming**: Avoid conflicts by allowing same resource names in different namespaces

Think of namespaces as folders on your computer - they help organize and separate your applications.

## Deploy the Application
### 1. Create Namespace
Create a dedicated namespace for your hello world application:

```bash
kubectl create namespace helloworld
```

This groups your application resources. Network isolation requires separate NetworkPolicies; namespaces alone do not block traffic.

### 2. Install with Helm
Deploy your application using Helm:

```bash
helm install helloworld -f values.yaml -n helloworld .
```

**Command breakdown:**
- `helm install` - Deploy a new application
- `helloworld` - Name of this deployment (release name)
- `-f values.yaml` - Use your custom values file
- `-n helloworld` - Deploy into the "helloworld" namespace
- `.` - Use the current directory as the chart source

## Verify Deployment
Check that your application is running:

```bash
# Check pods in the namespace
kubectl get pods -n helloworld

# Check all resources
kubectl get all -n helloworld

# Check if your ingress is configured
kubectl get ingress -n helloworld

# View your application's HTML content
kubectl get configmap hello-world-html -n helloworld -o yaml
```

### Expected Output
Your pods should show as `Running`:
```bash
NAME                           READY   STATUS    RESTARTS   AGE
hello-world-xxxxxxxxxx-xxxxx   1/1     Running   0          2m
```

Your application should now be accessible at your configured domain (e.g., `https://helloworld.ltu-m7011e-johan.se`).

![Helloworld](./webapp.png)

## How the Application Works
This application demonstrates several key Kubernetes concepts:

1. **nginx Container**: Serves a custom HTML page
2. **ConfigMap**: Stores the HTML content that gets mounted into the nginx container
3. **Service**: Provides stable internal networking (ClusterIP)
4. **Ingress**: Handles external traffic and SSL termination using Traefik and Let's Encrypt
5. **Deployment**: Ensures your specified number of replicas are always running

## Troubleshooting
If something goes wrong, you can debug with these commands:

```bash
# Check Helm releases
helm list -n helloworld

# View detailed pod information
kubectl describe pods -n helloworld

# Check application logs
kubectl logs -l app=hello-world -n helloworld

# Check ingress status
kubectl describe ingress hello-world -n helloworld

# Verify certificate status
kubectl get certificate -n helloworld

# Check if DNS is resolving correctly
nslookup your-domain.ltu-m7011e-johan.se
```

### Common Issues
- **Pod not starting**: Check `kubectl describe pod` for resource constraints or image issues
- **Website not accessible**: Verify ingress configuration and DNS resolution
- **SSL certificate issues**: Check certificate issuer status and Let's Encrypt rate limits
- **Template errors**: Run `helm template . -f values.yaml` to test template rendering

## Advanced Usage
### Update Your Application
After making changes to values or templates:
```bash
helm upgrade helloworld -f values.yaml -n helloworld .
```

### View Generated YAML
To see what Kubernetes resources Helm will create:
```bash
helm template helloworld -f values.yaml .
```

### Rollback Changes
If an update causes issues:
```bash
helm rollback helloworld -n helloworld
```

## Cleanup (when finished)

After verifying and experimenting with the app, remove the release:

```bash
helm uninstall helloworld -n helloworld
```

If the namespace is dedicated to this exercise and you no longer need any of its resources:

```bash
kubectl delete namespace helloworld
```
