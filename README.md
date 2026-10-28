# M7011E - Dynamic Web Systems Tutorials

Tutorials for building web applications, packaging them with Docker, and deploying them to Kubernetes. The main sequence covers web fundamentals, databases, frameworks, testing, GitOps, and authentication. Optional tutorials cover messaging, monitoring, and service meshes.

## Getting Started

Clone this repository and start with [Tutorial 1](./01-basic-webapp/README.md). Follow each tutorial's prerequisites and run its commands from the directory specified there.

- **Local development:** Python 3.10 or newer, pip, Git, and a web browser. The React tutorials also use Node.js and npm.
- **Containers:** Docker Engine or Docker Desktop with Docker Compose.
- **Kubernetes:** Access to the course cluster (or a suitable development cluster), kubectl, and Helm. [Tutorial 6](./06-k8s-getting-started/README.md) explains the course cluster setup.
- **Cluster services:** Some examples rely on an ingress controller, cert-manager, and a storage class supplied by the cluster. Replace example namespaces, domains, credentials, and registry names with your own values.

These are teaching examples. Some store data in memory or use development servers; deployment on Kubernetes alone does not make an application ready for production.

## How to Work Through a Tutorial

For each command, identify **where it runs**, **what it changes**, and **what result would show that it worked**. Read [Understanding the commands](./COMMANDS.md) if shell syntax, ports, environment variables, or Kubernetes options are unfamiliar.

Work in small steps:

1. **Predict:** Write down what you expect the next command to do. Does it read information, start a process, change a deployment, or delete something?
2. **Run and observe:** Run one step, then inspect its output, the browser Network tab, or the relevant application logs.
3. **Explain:** Describe the result in your own words. An error message is evidence about which part of the system you have reached.
4. **Change one thing:** Try a different request body, port, replica count, or configuration value. Predict the difference before running it.

Keep a short lab record with the command, your prediction, the observed result, and an explanation. Being able to adapt a command and diagnose its failure is part of the exercise.

Start with [an HTTP request and response](./01-basic-webapp/README.md#2-follow-one-http-request) before studying APIs, [service boundaries](./05-microservices-and-k8s/README.md#start-with-one-business-operation) before deploying microservices, and [TLS and certificates](./07-k8s-helloworld/README.md#before-deploying-how-https-reaches-your-application) before configuring HTTPS. The [Keycloak overview](./12-keycloak/README.md#before-deploying-follow-one-sign-in) connects these ideas to authentication.

## Main Tutorials

Work through tutorials 1-13 in order. Tutorials 3-5 explain concepts and include illustrative snippets; the other tutorials provide application files, deployment charts, or exercises to follow.

| Tutorial | Topics |
| --- | --- |
| [01 - Basic Web Application](./01-basic-webapp/README.md) | Flask REST API, vanilla JavaScript, HTTP, JSON, CORS, and Swagger UI. Todos are stored in memory. |
| [02 - Docker and Docker Compose](./02-docker/README.md) | Containerize the todo app, write Dockerfiles, run services with Compose, and understand networking and volumes. |
| [03 - Databases](./03-databases/README.md) | Relational, document, key-value, time-series, graph, and vector databases; consistency and database selection. |
| [04 - Frameworks](./04-frameworks/README.md) | Frontend and backend frameworks, SPA and SSR patterns, and framework choices for different services. |
| [05 - Microservices and Kubernetes](./05-microservices-and-k8s/README.md) | Service boundaries, API gateways, service discovery, deployment, scaling, and communication patterns. |
| [06 - Kubernetes: Getting Started](./06-k8s-getting-started/README.md) | Install tools, obtain a kubeconfig through Rancher, and connect to the course cluster. |
| [07 - Kubernetes: Hello World](./07-k8s-helloworld/README.md) | Deploy an Nginx application using Helm, Services, Ingress, and TLS certificates. |
| [08 - PostgreSQL](./08-postgresql/README.md) | Deploy PostgreSQL using Helm, a StatefulSet, persistent storage, and port forwarding. |
| [09 - React with Claude Code](./09-claude-code-frontend/README.md) | Rebuild the todo frontend with React through an iterative AI-assisted workflow. |
| [10 - Testing and CI](./10-testing-ci/README.md) | Write backend and frontend tests, collect coverage, and create GitHub Actions workflows. Includes a [quick start](./10-testing-ci/QUICKSTART.md). |
| [11 - Argo CD and GitOps](./11-argocd-gitops/README.md) | Install Argo CD and use Git and Helm to manage application deployments across environments. |
| [12 - Keycloak](./12-keycloak/README.md) | Deploy Keycloak with PostgreSQL, configure realms and clients, and work through three React/Flask examples covering login, JWT verification, and roles. |
| [13 - MongoDB](./13-mongodb/README.md) | Deploy MongoDB with Helm and persistent storage, connect with mongosh or Python, and practice document operations. |

## Optional Advanced Tutorials

Continue with tutorials 14-16 in `advanced/` after the main sequence. Messaging introduces RabbitMQ, monitoring builds on those examples, and service meshes add Istio.

| Tutorial | Topics |
| --- | --- |
| [14 - Service Communication](./advanced/14-service-communication/README.md) | RabbitMQ, producers and consumers, acknowledgments, work queues, publish/subscribe, and dead-letter queues. Includes a [deployment guide](./advanced/14-service-communication/DEPLOYMENT.md) and [Python examples](./advanced/14-service-communication/examples/README.md). |
| [15 - Monitoring](./advanced/15-monitoring/README.md) | Prometheus metrics, Grafana dashboards, Python instrumentation, RabbitMQ monitoring, and alert rules. Includes a [deployment guide](./advanced/15-monitoring/DEPLOYMENT.md) and [example services](./advanced/15-monitoring/examples/README.md). |
| [16 - Service Meshes](./advanced/16-service-meshes/README.md) | Istio routing, retries, circuit breakers, canary releases, mutual TLS, authorization, and fault injection. Includes a [quick start](./advanced/16-service-meshes/QUICKSTART.md) and a [simple demo](./advanced/16-service-meshes/examples/README.md). |

## Repository Layout

```text
01-basic-webapp/              Flask API and JavaScript frontend
02-docker/                    Dockerfiles and Compose configuration
03-databases/                 Database concepts
04-frameworks/                Framework guide
05-microservices-and-k8s/      Architecture guide and illustrative examples
06-k8s-getting-started/        Cluster setup instructions
07-k8s-helloworld/             Hello World Helm chart
08-postgresql/                PostgreSQL Helm chart and helper scripts
09-claude-code-frontend/       React and Claude Code walkthrough
10-testing-ci/                Testing guide, quick start, and test dependencies
11-argocd-gitops/              Argo CD installation and GitOps demo charts
12-keycloak/                  Keycloak chart, setup scripts, and three example apps
13-mongodb/                   MongoDB Helm chart and helper scripts
advanced/
  14-service-communication/   RabbitMQ chart and Python messaging examples
  15-monitoring/             Monitoring chart, dashboards, and example services
  16-service-meshes/         Istio installation script and demo manifests
```
