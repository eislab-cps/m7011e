# M7011E - Dynamic Web Systems Tutorials

Tutorials for building web applications, packaging them with Docker, and deploying them to your group's **K3s** cluster. They are grouped below by learning stage, from a first local application to deployment, security, and evaluation.

**One platform, two names:** K3s is the Kubernetes distribution used in this course. Kubernetes is the underlying platform; **K8s** is only an abbreviation for Kubernetes, not another tool to install. We use **K3s** when referring to the course cluster. Official names such as the Kubernetes API, `kubectl`, and `networking.k8s.io/v1` still apply.

## Getting Started

Clone this repository and start with the [Introduction](./00-introduction/README.md), which explains the internet, HTTP, cloud computing, and Kubernetes before any setup. Then continue with [Tutorial 1](./01-basic-webapp/README.md). Follow each tutorial's prerequisites and run its commands from the directory specified there.

- **Local development:** Python 3.10 or newer, pip, Git, and a web browser. The React tutorials also use Node.js and npm.
- **Containers:** Docker Engine or Docker Desktop with Docker Compose.
- **K3s environment:** Your group receives an Ubuntu VM, public IP, and configured domain. [Tutorial 5B](./05b-k3s-setup/README.md) installs K3s and HTTPS. [Tutorial 6](./06-k3s-remote-access-and-helm/README.md) installs Helm and explains optional remote access from your laptop. [Tutorial 7](./07-k3s-deploy-applications/README.md) deploys an application to that existing cluster.
- **Cluster services:** Tutorial 5B sets up the ingress, storage provisioner, and certificate issuers used later. Replace example namespaces, domains, credentials, and registry names with your own values; additional subdomains need matching DNS.

These are teaching examples. Some store data in memory or use development servers; deployment on Kubernetes alone does not make an application ready for production.

**Course activities (2026):** form your project group in Canvas now (deadline 4 November), and sign up separately for the design seminar on 16, 17 or 19 November. Prepare for Casper's **13 November environment demonstration** using [Tutorial 5B's demonstration brief](./05b-k3s-setup/DEMONSTRATION.md). Teams aiming for Grade 5 should read [scientific experiments and test harnesses](./10-testing-ci/SCIENTIFIC-EVALUATION.md) while planning their proposal.

## How to Work Through a Tutorial

First explain **which problem the technology solves**, **what an alternative would do**, and **which tradeoff you accept**. For each command, identify **where it runs**, **what it changes**, and **what result would show that it worked**. Read [Understanding the commands](./COMMANDS.md) if shell syntax, ports, environment variables, or Kubernetes options are unfamiliar.

Work in small steps:

1. **Predict:** Write down what you expect the next command to do. Does it read information, start a process, change a deployment, or delete something?
2. **Run and observe:** Run one step, then inspect its output, the browser Network tab, or the relevant application logs.
3. **Explain:** Describe the result in your own words. An error message is evidence about which part of the system you have reached.
4. **Change one thing:** Try a different request body, port, replica count, or configuration value. Predict the difference before running it.

Keep a short lab record with the command, your prediction, the observed result, and an explanation. Being able to adapt a command and diagnose its failure is part of the exercise.

Start with [an HTTP request and response](./01-basic-webapp/README.md#2-follow-one-http-request) before studying APIs, [service boundaries](./05-microservices-and-k3s/README.md#start-with-one-business-operation) before deploying microservices, and [TLS and certificates](./07-k3s-deploy-applications/README.md#before-deploying-how-https-reaches-your-application) before configuring HTTPS. The [Keycloak overview](./12-keycloak/README.md#before-deploying-follow-one-sign-in) connects these ideas to authentication.

## Tutorials by Learning Stage

Follow the stages in order and check each tutorial's prerequisites. Tutorial numbers remain stable for course references. The introduction and tutorials 3–5 (including 4b) explain concepts; the practical tutorials provide commands, application files, charts, and exercises.

### 1. Getting Started: Build Locally

Understand a web request, build a small application, and package it. You can complete these tutorials on your laptop before receiving a VM.

| Tutorial | Topics |
| --- | --- |
| [00 - Introduction](./00-introduction/README.md) | The internet, HTTP, cloud computing, and the role of K3s in the course. |
| [01 - Basic Web Application](./01-basic-webapp/README.md) | Flask REST API, vanilla JavaScript, HTTP, JSON, CORS, and Swagger UI. Todos are stored in memory. |
| [02 - Docker and Docker Compose](./02-docker/README.md) | Containerize the todo app, write Dockerfiles, run services with Compose, and understand networking and volumes. |

### 2. Designing Your System

Choose technologies and boundaries for a problem you understand. These chapters explain the choices before asking you to install the cluster.

| Tutorial | Topics |
| --- | --- |
| [03 - Databases](./03-databases/README.md) | Relational, document, key-value, time-series, graph, and vector databases; consistency and database selection. |
| [04 - Frameworks](./04-frameworks/README.md) | Frontend and backend frameworks, SPA and SSR patterns, and framework choices for different services. |
| [04b - Software Architectures](./04b-architectures/README.md) | Layers, modular monoliths, ports and adapters, services, events, pipelines, plug-ins, data patterns, BFFs, serverless, and real-time delivery; exercises on boundaries and failures. |
| [05 - Microservices and K3s Concepts](./05-microservices-and-k3s/README.md) | Service boundaries and the Kubernetes concepts used by K3s: Pods, Services, controllers, routing, and scaling. |

### 3. Setting Up Your Environment

These tutorials have distinct jobs: **5B creates the cluster**, **6 prepares the clients**, and **7 in the next stage deploys an application**. Remote laptop access in Tutorial 6 is optional; installing Helm is needed for the later chart exercises.

| Tutorial | Topics |
| --- | --- |
| [05B - K3s on Your VM and HTTPS](./05b-k3s-setup/README.md) | SSH, K3s components and installation, copying the administrator kubeconfig with private permissions, Traefik, cert-manager, staging and production Let's Encrypt certificates, and troubleshooting. |
| [06 - K3s Remote Access and Helm](./06-k3s-remote-access-and-helm/README.md) | Install Helm on the VM or laptop; optionally connect laptop clients to the existing cluster through SSH. |

### 4. Building and Deploying Applications

Use the environment to run a web application and its database, then develop a richer frontend.

| Tutorial | Topics |
| --- | --- |
| [07 - Deploy Applications on K3s](./07-k3s-deploy-applications/README.md) | Deploy, inspect, update, and remove a Hello World application with Helm, Services, Ingress, and HTTPS. |
| [08 - PostgreSQL](./08-postgresql/README.md) | Deploy PostgreSQL using Helm, a StatefulSet, persistent storage, and port forwarding. |
| [09 - React with Claude Code](./09-claude-code-frontend/README.md) | Rebuild the todo frontend with React through an iterative AI-assisted workflow. |

### 5. Testing, Delivery, and Evaluation

Check behavior automatically and make deployments repeatable. Plan [scientific experiments and a test harness](./10-testing-ci/SCIENTIFIC-EVALUATION.md) here if you are aiming for Grade 5.

| Tutorial | Topics |
| --- | --- |
| [10 - Testing and CI](./10-testing-ci/README.md) | Write backend and frontend tests, collect coverage, and create GitHub Actions workflows. Includes a [quick start](./10-testing-ci/QUICKSTART.md). |
| [11 - Argo CD and GitOps](./11-argocd-gitops/README.md) | Install Argo CD and use Git and Helm to manage application deployments across environments. |

### 6. Identity and Data Services

Add shared identity and access control, and explore a document database when it fits your application's data.

| Tutorial | Topics |
| --- | --- |
| [12 - Keycloak](./12-keycloak/README.md) | Deploy Keycloak with PostgreSQL, configure realms and clients, and work through three React/Flask examples covering login, JWT verification, and roles. |
| [13 - MongoDB](./13-mongodb/README.md) | Deploy MongoDB with Helm and persistent storage, connect with mongosh or Python, and practice document operations. |

### 7. Optional Advanced Topics

Continue with tutorials 14-16 in `advanced/` after the main sequence. Messaging introduces RabbitMQ, monitoring builds on those examples, and service meshes add Istio.

| Tutorial | Topics |
| --- | --- |
| [14 - Service Communication](./advanced/14-service-communication/README.md) | RabbitMQ, producers and consumers, acknowledgments, work queues, publish/subscribe, and dead-letter queues. Includes a [deployment guide](./advanced/14-service-communication/DEPLOYMENT.md) and [Python examples](./advanced/14-service-communication/examples/README.md). |
| [15 - Monitoring](./advanced/15-monitoring/README.md) | Prometheus metrics, Grafana dashboards, Python instrumentation, RabbitMQ monitoring, and alert rules. Includes a [deployment guide](./advanced/15-monitoring/DEPLOYMENT.md) and [example services](./advanced/15-monitoring/examples/README.md). |
| [16 - Service Meshes](./advanced/16-service-meshes/README.md) | Istio routing, retries, circuit breakers, canary releases, mutual TLS, authorization, and fault injection. Includes a [quick start](./advanced/16-service-meshes/QUICKSTART.md) and a [simple demo](./advanced/16-service-meshes/examples/README.md). |

## Repository Layout

```text
00-introduction/                 Internet, HTTP, cloud, and Kubernetes basics
01-basic-webapp/                 Flask API and JavaScript frontend
02-docker/                       Dockerfiles and Compose configuration
03-databases/                    Database concepts
04-frameworks/                   Framework guide
04b-architectures/               Architecture styles and tradeoffs
05-microservices-and-k3s/        Microservices and cluster concepts
05b-k3s-setup/                   VM, SSH, K3s, kubeconfig, and HTTPS setup
06-k3s-remote-access-and-helm/   Helm installation and optional laptop access
07-k3s-deploy-applications/      Application deployment with a Hello World Helm chart
08-postgresql/                   PostgreSQL Helm chart and helper scripts
09-claude-code-frontend/         React and Claude Code walkthrough
10-testing-ci/                   Testing guide, quick start, and test dependencies
11-argocd-gitops/                Argo CD installation and GitOps demo charts
12-keycloak/                     Keycloak chart, setup scripts, and three example apps
13-mongodb/                      MongoDB Helm chart and helper scripts
advanced/
  14-service-communication/      RabbitMQ chart and Python messaging examples
  15-monitoring/                 Monitoring chart, dashboards, and example services
  16-service-meshes/             Istio installation script and demo manifests
```
