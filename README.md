# M7011E - Dynamic Web Systems Tutorials

A comprehensive, hands-on course covering modern web development, containerization, microservices architecture, and production-ready cloud-native application deployment with Kubernetes.

Learn to build enterprise-grade systems with:
- **Microservices Architecture**: Design, deploy, and scale distributed systems
- **Container Orchestration**: Master Kubernetes for production workloads
- **DevOps Practices**: GitOps, CI/CD, and infrastructure as code
- **Security**: Authentication, authorization, and zero-trust networking
- **Observability**: Monitoring, logging, and distributed tracing
- **Resilience**: Message queues, circuit breakers, and service mesh patterns

## Technology Stack

By completing these tutorials, you will gain hands-on experience with:

**Core Technologies:**
- Docker & Docker Compose
- Kubernetes (K8s)
- Helm Charts
- Python (Flask, FastAPI)
- JavaScript (React, Node.js)

**Infrastructure & DevOps:**
- Argo CD (GitOps)
- PostgreSQL databases
- RabbitMQ message broker
- Nginx ingress controller
- GitHub Actions (CI/CD pipelines)

**Testing:**
- pytest (Python testing framework)
- Jest & React Testing Library (JavaScript testing)
- Code coverage tools (pytest-cov, Codecov)
- Test automation and continuous integration

**Security & Identity:**
- Keycloak (OAuth 2.0, OIDC)
- Istio service mesh (mTLS, authorization policies)
- Role-Based Access Control (RBAC)

**Observability:**
- Prometheus (metrics collection)
- Grafana (dashboards & visualization)
- Jaeger (distributed tracing)
- Kiali (service mesh visualization)

**Service Mesh:**
- Istio (traffic management, security, observability)
- Envoy proxy (sidecar pattern)

**AI & Machine Learning:**
- Ollama (local LLM runtime)
- scikit-learn (ML models)
- Model Context Protocol (MCP)
- Anthropic Claude API (optional cloud AI)

**Documentation:**
- Mermaid (diagrams as code)
- OpenAPI/Swagger (API specifications)
- AI-powered documentation generation

## Tutorials

### [01-basic-webapp](./01-basic-webapp/)
Build a simple REST API web application with Flask and vanilla JavaScript.

**Covers:**
- Client-server architecture and communication
- REST vs JSON-RPC comparison
- Flask REST API development with Swagger/OpenAPI documentation
- Frontend-backend communication with Fetch API
- CORS and HTTP methods
- JSON data format
- In-memory data storage

### [02-docker](./02-docker/)
Containerize the todo application using Docker and Docker Compose.

**Covers:**
- Docker fundamentals (images, containers, registries)
- Writing Dockerfiles for backend and frontend
- Container vs VM architecture
- Docker Compose for multi-container orchestration
- Container networking and service discovery
- Data persistence with volumes
- Docker best practices and optimization
- Debugging containerized applications

### [03-databases](./03-databases/)
Comprehensive overview of database types and when to use each one.

**Covers:**
- Database fundamentals (ACID, BASE, CAP theorem)
- SQL vs NoSQL databases
- PostgreSQL (Relational database)
- MongoDB (Document database)
- Redis (Key-value store/cache)
- SQLite (Embedded database)
- InfluxDB/TimescaleDB (Time-series databases)
- Neo4j (Graph database)
- Pinecone/Weaviate (Vector databases for AI/ML)
- Database selection criteria and trade-offs
- Use case examples and best practices

### [04-frameworks](./04-frameworks/)
Comprehensive guide to choosing the right frameworks for building modern microservices architectures.

**Covers:**
- Frontend frameworks (React, Vue, Svelte, Angular, Rust/WebAssembly)
- Microservices-friendly backend frameworks (Flask, FastAPI, Express.js, NestJS, Go, Rust, Java)
- Framework selection criteria for microservices
- When to use each framework for specific services
- Polyglot microservices architecture (different frameworks per service)
- Real-world microservices use cases
- Why monolithic frameworks (Django, Rails) don't fit microservices
- Performance, scalability, and deployment considerations
- AI-assisted development friendliness
- SPA vs SSR architecture patterns

### [05-microservices-and-k8s](./05-microservices-and-k8s/)
Introduction to microservices architecture and deploying microservices on Kubernetes.

**Covers:**
- Microservices architecture fundamentals
- Monolithic vs microservices comparison
- When to use microservices (and when not to)
- Microservices design principles (single responsibility, database-per-service)
- Building a multi-service application (User Service, Todo Service)
- API Gateway pattern with Nginx
- Service-to-service communication in Kubernetes
- Kubernetes DNS and service discovery
- Independent deployment and scaling
- Health checks and observability basics
- Polyglot microservices example (Flask + FastAPI)

### [06-k8s-getting-started](./06-k8s-getting-started/)
Set up your development environment and connect to the Kubernetes cluster.

**Covers:**
- Installing kubectl, helm, and Docker/Podman
- Connecting to the LTU Kubernetes cluster via Rancher
- Configuring kubectl with cluster credentials
- Basic Kubernetes concepts and architecture

### [07-k8s-helloworld](./07-k8s-helloworld/)
Deploy a web application using Helm charts with automatic SSL certificates.

**Covers:**
- Helm templating and package management
- Kubernetes resources (Deployments, Services, Ingress, ConfigMaps)
- Automatic HTTPS with Let's Encrypt and cert-manager
- Application deployment and troubleshooting
- Working with namespaces and labels

### [08-postgresql](./08-postgresql/)
Deploy a PostgreSQL database on Kubernetes using Helm charts with persistent storage.

**Covers:**
- PostgreSQL deployment using StatefulSets
- Persistent storage with PersistentVolumeClaims
- Database configuration with ConfigMaps and Secrets
- Port forwarding to access databases locally
- Database client tools installation and usage
- StatefulSet vs Deployment comparison
- Data persistence in Kubernetes

### [09-claude-code-frontend](./09-claude-code-frontend/)
Rebuild the Tutorial 1 todo list using React and Claude Code, learning effective AI-assisted development techniques.

**Covers:**
- Effective prompt engineering for AI-assisted development
- Step-by-step React development with Claude Code
- Converting vanilla JavaScript to React
- API integration and state management
- Tailwind CSS styling
- Iterative development workflow
- Common issues and troubleshooting with AI assistance

### [10-testing-ci](./10-testing-ci/)
Implement comprehensive testing strategies and automated CI pipelines with GitHub Actions for your microservices.

**Covers:**
- Testing pyramid (unit, integration, end-to-end tests)
- Backend testing with pytest (unit, integration, API tests)
- Frontend testing with Jest and React Testing Library
- Mocking and test fixtures
- Code coverage reporting (pytest-cov, Codecov)
- Test-driven development (TDD) practices
- GitHub Actions CI/CD pipelines
- Automated testing on pull requests
- Branch protection with required status checks
- Testing best practices for microservices

### [11-argocd-gitops](./11-argocd-gitops/)
Implement continuous deployment with Argo CD and GitOps principles for automated Kubernetes deployments.

**Covers:**
- GitOps principles and declarative deployment
- Traditional CI/CD vs GitOps architecture
- Argo CD installation and configuration
- Automated synchronization from Git repositories
- Application health monitoring and self-healing
- Multi-environment deployment strategies (dev, staging, production)
- Rollback and version control for infrastructure
- Integration with Helm charts
- Sync waves, hooks, and advanced patterns
- Troubleshooting and debugging GitOps deployments

### [12-keycloak](./12-keycloak/)
Deploy Keycloak for centralized Identity and Access Management (IAM) with OAuth 2.0 and OpenID Connect.

**Covers:**
- Understanding OAuth 2.0, OpenID Connect (OIDC), and JWT
- Keycloak deployment on Kubernetes with PostgreSQL
- Realm, client, user, and role configuration
- Authentication flows (Authorization Code, Client Credentials)
- Integrating Keycloak with React and Flask applications
- Role-Based Access Control (RBAC)
- Social login integration (GitHub, Google)
- Multi-factor authentication (MFA)
- Token verification and API security
- Production security best practices

### [13-service-communication](./13-service-communication/)
Implement reliable service-to-service communication with RabbitMQ message queuing and learn asynchronous messaging patterns.

**Covers:**
- Synchronous vs Asynchronous communication patterns
- RabbitMQ deployment on Kubernetes with Helm
- Message queue fundamentals (producers, consumers, exchanges, queues)
- Work queue pattern for task distribution
- Publish/Subscribe pattern for event broadcasting
- Dead Letter Queues (DLQ) for failed message handling
- Message durability and acknowledgments
- Service decoupling and resilience
- Monitoring queue depth and message rates
- Real-world microservices communication patterns

### [14-monitoring](./14-monitoring/)
Monitor microservices and message queues with Prometheus metrics and Grafana dashboards for real-time observability.

**Covers:**
- Monitoring fundamentals (Four Golden Signals, RED Method, USE Method)
- Prometheus metrics collection and storage
- Instrumenting Python applications with prometheus-client
- Metric types (Counter, Gauge, Histogram, Summary)
- Flask API instrumentation for HTTP metrics
- RabbitMQ consumer monitoring and queue depth tracking
- Grafana dashboard creation and visualization
- PromQL queries for request rate, error rate, and latency
- Alert rules and thresholds
- Cardinality management and best practices
- Kubernetes service discovery with Prometheus
- Production monitoring patterns

---

## Optional Advanced Tutorials

The following tutorials are **optional** and cover advanced topics. You can complete the core course (Tutorials 1-14) and come back to these later.

### [15-service-meshes](./15-service-meshes/)
Implement advanced traffic management, security, and observability with Istio service mesh.

**Covers:**
- Service mesh fundamentals and sidecar pattern
- Istio architecture (control plane, data plane, Envoy proxy)
- Automatic sidecar injection for transparent proxying
- Traffic management (VirtualServices, DestinationRules)
- Intelligent routing, retries, timeouts, and circuit breakers
- Canary deployments and traffic splitting for progressive rollouts
- A/B testing with header-based routing
- Automatic mutual TLS (mTLS) encryption between services
- Zero-trust security with authorization policies
- Distributed tracing with Jaeger
- Service mesh visualization with Kiali
- Fault injection for resilience testing
- Integration with Prometheus and Grafana
- Production best practices and performance considerations

### [16-ai-personalization](./16-ai-personalization/) 
Add intelligent, personalized recommendations to your microservices using machine learning.

**Covers:**
- Recommendation systems fundamentals (collaborative filtering)
- Training ML models with scikit-learn
- Serving models as microservices
- Redis caching for fast predictions
- Prometheus metrics for ML services
- Model versioning and deployment
- A/B testing ML models with Istio
- Performance optimization (caching, precomputation)
- Model monitoring and drift detection
- Continuous training pipelines
- Integration with existing microservices stack

### [17-mcp-ai-ops](./17-mcp-ai-ops/) 
Connect your entire microservices platform to AI assistants using the Model Context Protocol (MCP) for AI-powered operations.

**Covers:**
- Model Context Protocol (MCP) fundamentals
- Building MCP servers in Python
- PostgreSQL MCP server for database queries
- Prometheus MCP server for metrics analysis
- Kubernetes MCP server for cluster management
- Configuring Claude Code with MCP servers
- Real-world AI-assisted debugging workflows
- Security best practices (read-only access, authentication, audit logging)
- Multi-service queries combining database, metrics, and cluster data
- Natural language interface for DevOps tasks

### [18-dynamic-ai-services](./18-dynamic-ai-services/)
Build microservices that use AI at runtime to provide intelligent, dynamic features to end users.

**Covers:**
- Service-to-AI integration architecture
- Content generation service with AI-powered blog suggestions
- Real-time content moderation using AI
- Natural language to SQL query translation
- Redis caching strategies for AI responses
- Fallback patterns and circuit breakers
- Cost tracking and budget management for AI API calls
- A/B testing AI features vs traditional logic
- Batch processing and async AI calls for performance
- Prometheus metrics for AI usage monitoring
- Production deployment with Docker and Kubernetes

---

## Learning Path

### Core Tutorials (Required)

The core tutorials are designed to be completed in order:

1. **Foundation** (Tutorial 1): Build a basic web application
2. **Containerization** (Tutorial 2): Package your application with Docker
3. **Data Storage** (Tutorial 3): Understand different database types
4. **Framework Selection** (Tutorial 4): Choose the right frontend and backend frameworks
5. **Microservices** (Tutorial 5): Learn microservices architecture patterns
6. **Orchestration** (Tutorials 6-7): Set up and deploy to Kubernetes
7. **Persistence** (Tutorial 8): Add database storage on Kubernetes
8. **Modern Frontend** (Tutorial 9): Build with React and AI assistance
9. **Testing & CI** (Tutorial 10): Implement comprehensive testing and automated CI pipelines
10. **Automation** (Tutorial 11): Implement GitOps with Argo CD
11. **Security** (Tutorial 12): Add authentication and authorization with Keycloak
12. **Messaging** (Tutorial 13): Implement asynchronous communication with RabbitMQ
13. **Observability** (Tutorial 14): Monitor services with Prometheus and Grafana

**After completing tutorials 1-14, you will have a complete production-ready, enterprise-grade microservices platform.**

### Optional Advanced Tutorials

These tutorials are **optional** and cover advanced topics. You can explore them based on your interests:

- **Tutorial 15 (Service Mesh)**: Advanced traffic management and security with Istio
- **Tutorial 16 (AI/ML)**: Add intelligent personalization with machine learning
- **Tutorial 17 (AI Ops)**: AI-powered platform operations with MCP for DevOps
- **Tutorial 18 (AI Services)**: Build services that use AI to enhance user features
