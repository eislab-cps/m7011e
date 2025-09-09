## Core Technical Requirements
All projects **MUST** include these elements to pass:

### 1. Dynamic Web System
*Learning Objective: Understand dynamic web systems*

The system must be dynamic, meaning content changes based on user interactions or data (e.g., user profiles, real-time updates).

**REQ1**: System must include an approved project proposal document submitted to instructor

**REQ2**: System must demonstrate content adaptation based on approved proposal design

**REQ3**: System must include documented examples of dynamic content changes

**REQ4**: System must implement at least two types of dynamic behavior (e.g., user-specific content, real-time data updates, adaptive interfaces)

**REQ5**: System must respond differently to different user states or interactions

### 2. Full-Stack Implementation
*Learning Objective: Build dynamic web systems*

The system must be a full-stack web application with frontend, backend, and database components, and be based on microservices architecture.

**REQ6**: System must include functional frontend using React (recommended), Vue (limited support), or Angular (no support) - **Note: Minimal focus, backend emphasis**

**REQ7**: System must include backend API built with Node.js/Python/Go (recommended)

**REQ8**: System must achieve minimum 50% code coverage on backend services (UI testing not required)

**REQ9**: System must include functional GitHub Actions CI/CD pipeline

**REQ10**: System must include at least 2 endpoint failure test cases per service/components (e.g., unauthorized access, validation errors)

**REQ11**: System must select and implement a suitable database technology (e.g., PostgreSQL, MongoDB) with justification for the choice based on project requirements

**REQ12**: System must include documented and well-designed database schema with proper relationships (must be able to explain and motivate design choices)

### 3. Cloud-Native Deployment
*Learning Objective: Deploy and manage web systems in cloud environments*

The system must be deployed in a cloud-native manner using containerization and orchestration tools.

**REQ13**: System must include Docker containerization for all services with multi-stage builds

**REQ14**: System must implement microservices architecture with multiple logical services (e.g., user service, content service)

**REQ15**: System must include Kubernetes deployment for all components using Helm charts

**REQ16**: Project must include observability and monitoring tools (Prometheus/Grafana or equivalent)

### 4. API Design & Communication
*Learning Objective: Create application-programming interface*

The system must expose a well-designed API for frontend-backend communication and inter-service communication.

**REQ17**: System must implement RESTful API with proper HTTP methods and status codes

**REQ18**: System must implement event-driven architecture using message queues (e.g., RabbitMQ, Kafka) for communication between microservices (loosely coupled)

**REQ19**: System must implement authentication using JWT or OAuth 2.0 based on Keycloak

**REQ20**: System must include comprehensive API documentation using OpenAPI/Swagger/AsyncAPI specifications

### 5. System Design & Architecture
*Learning Objective: Model, simulate, predict and evaluate web systems*

The system must demonstrate sound architectural design principles and performance considerations.

**REQ21**: Project must include comprehensive architecture diagram using C4 model or equivalent architectural documentation, and documentation in GitHub repository

**REQ22**: Project must include performance analysis with load testing results and bottleneck identification

**REQ23**: Project must include implemented script/tool that generates traffic to simulate system load

### 6. Security & Ethics
*Learning Objective: Ethical handling of sensitive data*

The system must implement security best practices and consider ethical implications of data handling.

**REQ24**: Project must implement secure authentication with proper password hashing and session management (e.g., JWT, OAuth 2.0)

**REQ25**: Project must include documented protection against SQL injection and XSS attacks

**REQ26**: Project must implement HTTPS for all communications using SSL/TLS certificates (automatic via Let's Encrypt)

**REQ27**: Project must include documentation of certificate management and renewal processes

**REQ28**: Project must include GDPR compliance considerations and data privacy measures documentation

**REQ29**: Project must document how data privacy measures (e.g., data minimization, user consent) are implemented

**REQ30**: Project must include ethical analysis of sensitive data handling, privacy implications, and societal impact
