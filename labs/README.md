# Lab Assignment: Design and Implement Your Own Dynamic Web System

## Overview
This is the main lab assignment for the **Design of Dynamic Web Systems (M7011E)** course. You will design and implement a complete dynamic web system that demonstrates modern full-stack development principles, cloud-native deployment, and production-ready practices.

## Prerequisites
Based on your completed courses, you should have:
- **Programming Skills**: Object-oriented programming experience (Java/similar).
- **Database Knowledge**: SQL and database design principles.
- **Web Basics**: Client-server communication concepts.
- **Version Control**: Git experience for collaborative development.

**New Technologies You'll Learn**: Docker, Kubernetes, CI/CD pipelines, cloud-native development patterns.

## Assignment Structure
### Students work in teams of 3 people (or 2 if odd number of students)
- Students that find a groups will be assigned to a group of 3 by the instructor
- Choose your own project idea
- Must fulfill all core technical requirements  
- Focus on backend architecture, security, and scalability
- Each team gets dedicated Kubernetes cluster access. Contact TA for access info and credentials.

## Project Proposal (Week 1)
Submit a **1-page proposal** including:

**Use the [Project Proposal Template](project-proposal-template.md)** for detailed guidance and structure.
- **Problem Statement**: What problem are you solving?
- **Core Features**: List 3-5 main features your system will provide
- **Target Users**: Who will use your system?
- **Technology Stack**: Justify your choice of backend, database, and frontend technologies
- **System Architecture**: High-level diagram showing components and their interactions
- **Requirements Mapping**: How you will demonstrate each grading requirement
- **Development Roadmap**: Timeline and milestones

### Example Project Ideas:
- Social platform for student organizations
- Collaborative study tool with real-time features
- Personal finance tracker with AI insights
- Recipe sharing platform with recommendations
- Fitness tracking with social challenges
- Local news aggregator with personalization
- Movie night planning with voting system
- Lecture note sharing with collaborative annotations

## Core Technical Requirements
All projects **MUST** include these elements to pass:

### 1. Dynamic Web System
*Learning Objective: Understand dynamic web systems*

The system must be dynamic, meaning content changes based on user interactions or data (e.g., user profiles, real-time updates).

**REQ1**: System must include an approved project proposal document submitted to instructor.
**REQ2**: System must demonstrate content adaptation based on approved proposal design.
**REQ3**: System must include documented examples of dynamic content changes.
**REQ4**: System must implement at least two types of dynamic behavior (e.g., user-specific content, real-time data updates, adaptive interfaces).
**REQ5**: System must respond differently to different user states or interactions.

### 1. Full-Stack Implementation
*Learning Objective: Build dynamic web systems*

The system must be a full-stack web application with frontend, backend, and database components, and be based on microservices architecture.

**REQ6**: System must include functional frontend using React (recommended), Vue (limited support), or Angular (no support) - **Note: Minimal focus, backend emphasis**.
**REQ7**: System must include backend API built with Node.js/Python/Go (recommended).
**REQ8**: System must achieve minimum 50% code coverage on backend services (UI testing not required).
**REQ9**: System must include functional GitHub Actions CI/CD pipeline.
**REQ10**: System must include at least 2 endpoint failure test cases per service/components (e.g., unauthorized access, validation errors).
**REQ11**: System must select and implement a suitable database technology (e.g., PostgreSQL, MongoDB) with justification for the choice based on project requirements
**REQ12**: System must include documented and well-designed database schema with proper relationships (must be able to explain and motivate design choices).

### 2. Cloud-Native Deployment
*Learning Objective: Deploy and manage web systems in cloud environments*

The system must be deployed in a cloud-native manner using containerization and orchestration tools.

**REQ13**: System must include Docker containerization for all services with multi-stage builds.
**REQ14**: System must implement microservices architecture with multiple logical services (e.g., user service, content service).
**REQ15**: System must include Kubernetes deployment for all components using Helm charts.
**REQ16**: Project must include observability and monitoring tools (Prometheus/Grafana or equivalent).

### 2. API Design & Communication
*Learning Objective: Create application-programming interface*

The system must expose a well-designed API for frontend-backend communication and inter-service communication.

**REQ17**: System must implement RESTful API with proper HTTP methods and status codes.
**REQ18**: System must implement event-driven architecture using message queues (e.g., RabbitMQ, Kafka) for communication between microservices (loosely coupled).
**REQ19**: System must implement authentication using JWT or OAuth 2.0 based on Keycloak.
**REQ20**: System must include comprehensive API documentation using OpenAPI/Swagger/AsyncAPI specifications.

### 4. System Design & Architecture
*Learning Objective: Model, simulate, predict and evaluate web systems*

The system must demonstrate sound architectural design principles and performance considerations.

**REQ21**: Project must include comprehensive architecture diagram using C4 model or equivalent architectural documentation, and documentation in GitHub repository.
**REQ22**: Project must include performance analysis with load testing results and bottleneck identification.
**REQ23**: Project must include implemented script/tool that generates traffic to simulate system load.

### 5. Security & Ethics
*Learning Objective: Ethical handling of sensitive data*

The system must implement security best practices and consider ethical implications of data handling.

**REQ24**: Project must implement secure authentication with proper password hashing and session management (e.g., JWT, OAuth 2.0).
**REQ25**: Project must include documented protection against SQL injection and XSS attacks.
**REQ26**: Project must implement HTTPS for all communications using SSL/TLS certificates (automatic via Let's Encrypt).
**REQ27**: Project must include documentation of certificate management and renewal processes.
**REQ28**: Project must include GDPR compliance considerations and data privacy measures documentation.
**REQ29**: Project must document how data privacy measures (e.g., data minimization, user consent) are implemented.
**REQ30**: Project must include ethical analysis of sensitive data handling, privacy implications, and societal impact.

## Advanced Features (Choose One for Higher Grades)
To achieve Grade 4 or 5, teams must implement one advanced feature from the options below to enhance their chosen project. This is in addition to all core requirements.

### Option A: Advanced Personalization
Add intelligent personalization capabilities to your existing application.

**Example Features:**
- **Collaborative Filtering**: Real-time user similarity recommendations adapted to your domain.
- **Dynamic UI Updates**: Interface elements that adapt in real-time based on user behavior.
- **LLM/MCP Integration**: Context-aware content suggestions based on user preferences (Note: students must pay for their own LLM API usage e.g., OpenAI, Anthropic, or use local models with Ollama, etc. Does not work on provided K8s cluster).

### Option B: Advanced Cloud-Native Architecture
Enhance your application with sophisticated cloud-native patterns.

**Example Features:**
- **Event Sourcing**: Store all user actions as events for complex querying and system reconstruction.
- **Service Mesh**: Implement Istio for advanced traffic management and observability.
- **Custom Kubernetes Operators**: Build operators for auto-scaling based on your application's specific metrics.
- **Distributed Tracing**: Track request flows across your microservices for performance optimization.
- **GitOps CI/CD**: Implement advanced deployment pipelines with automated rollbacks.

### Option C: Progressive Web App (PWA) with Offline Support
Transform your application to work seamlessly offline.

**Example Features:**
- **Service Workers**: Cache your application's assets and API responses for offline functionality.
- **Local Data Management**: Store user data locally with conflict-free synchronization when online.
- **Push Notifications**: Engage users with notifications even when your app is closed.
- **Responsive Design**: Optimize your interface for all device types and screen sizes.
- **Performance Optimization**: Achieve fast load times and smooth interactions.

### Option D: Advanced Security Features
Implement enterprise-grade security for your application.

**Example Features:**
- **Zero-Trust Model**: Authenticate and authorize every request, including internal communications.
- **End-to-End Encryption**: Encrypt all sensitive data at rest and in transit.
- **Role-Based Access Control (RBAC)**: Implement fine-grained permissions for your user types.
- **Security Auditing**: Log and monitor all access and changes to sensitive data

### Option E: Advanced Real-Time Features
Add sophisticated real-time capabilities to your application.

**Example Features:**
- **WebSocket Scaling**: Handle high concurrent user loads with live updates.
- **Real-Time Collaboration**: Enable simultaneous multi-user interactions with conflict resolution.
- **Live Data Synchronization**: Provide instant updates across all connected clients.
- **Connection Resilience**: Implement automatic reconnection and state recovery for real-time sessions.

# Grading Criteria

## Individual Oral Examination (Pass/Fail Requirement)
Each student is examined **individually** (20-minute session) and must demonstrate understanding of:
- Personal contributions to the system architecture and implementation.
- System architecture, data flow, and component interactions.
- Technologies used and fundamental concepts.
- Security implementation and testing approaches.
- Ability to troubleshoot and modify the system.

**Individual Assessment**: Each team member must pass their individual oral examination to receive the team grade. If any team member fails the oral exam, they receive a failing grade regardless of team system quality.


## Grades levels

### Grade 3 (Pass) - Core Implementation
- All core technical requirements (REQ1-REQ39) fully implemented.
- >50% test coverage on backend code with comprehensive failure scenario testing.
- Working Kubernetes deployment with proper monitoring.
- Complete project documentation.

### Grade 4 (Good) - Advanced Implementation
- All Grade 3 requirements significantly exceeded in quality and sophistication.
- One advanced feature (Option A-E) successfully implemented.
- 60%+ test coverage including integration tests and edge cases.
- Comprehensive documentation and monitoring.

### Grade 5 (Excellent) - Production-Ready System
- All Grade 4 requirements met.
- **Scientific Evaluation** with quantitative analysis demonstrating advanced system capabilities. Students must demonstrate rigorous, quantitative evaluation in their chosen area(s). The goal is scientific rigor and technical depth.

**Scientific Evaluation Options** (choose at least one with rigorous analysis):

**Scalability Analysis:**
- Load testing script/tool that generates realistic traffic to simulate system load.
- Documented evidence of how system scales (horizontally/vertically) to handle increased load.
- Performance metrics and bottleneck identification under various load conditions.

**Resiliency Analysis:**
- High availability implementation for critical services (e.g., user authentication).
- Chaos engineering script/tool that randomly restarts critical microservices to simulate failures
- Documented analysis of how system handles failures with minimal user impact.
- Evidence of seamless microservice updates without affecting user experience.

**Advanced Feature Evaluation:**
- Quantitative analysis of advanced feature performance and effectiveness.
- Comparative analysis showing improvement over baseline implementation
- Technical innovation demonstrating deep understanding of web systems principles.

**Advanced Testing Strategy:**
- 70%+ test coverage with end-to-end tests.
- Comprehensive edge case and failure scenario testing using mockups/emulators/simulations.
- Automated testing pipeline with multiple test environments and deployment strategies.

## Technical Support
- Dedicated Kubernetes cluster per team** (K3s with Rancher UI).
- Full cluster admin privileges for experimentation (each team has isolated cluster).
- Persistent storage and load balancer access.
- Weekly lab sessions with instructor and TA
- Office hours available on demand.
- Canvas discussion forum for questions. Note that questions can be asked anomymously.

## Submission Requirements
- **Git Repository**: All code in version control with meaningful commits.
- **TA Demo**: Working application demonstration to teaching assistant.
- **Documentation**: Comprehensive README and technical documentation in GitHub repository.
- **AI Usage Declaration**: Documentation of AI interactions and validation process.
  - **Use [AI Usage Declaration Template](ai-usage.md)**
