# Lab Assignment: 
## Design and Implement Your Own Dynamic Web System

## Overview
This document coverts the lab assignment for the **Design of Dynamic Web Systems (M7011E)** course, where you will design and implement a complete dynamic web system, and also demonstrates modern full-stack development principles, cloud-native deployment, and production-ready practices.

## Prerequisites
Based on your completed courses, you should have:
- **Programming Skills**: Object-oriented programming experience (Java/similar)
- **Database Knowledge**: SQL and database design principles
- **Web Basics**: Client-server communication concepts
- **Version Control**: Git experience for collaborative development

## Assignment Structure
### Students work in teams of 3 people (or 2 if odd number of students)
- Students that find a groups will automatically be assigned to a group of 3 by the instructor
- Choose your own project idea
- Must fulfill all core technical requirements  
- Focus on backend architecture, security, and scalability (no frontend polish, UX design, or mobile apps)
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
- Travel itinerary planner with shared editing
- Volunteer coordination platform for community service
- Campus resource sharing platform (e.g., textbooks, equipment)
- Local marketplace for students to buy/sell items
- Study group finder with matching algorithms
- Campus event calendar with personalized recommendations
- Online tutoring platform with session scheduling
- Group project management tool with task assignments
- Multiplayer games with real-time interaction

## Core Technical Requirements
All projects **MUST** include these elements to pass:

### 1. Dynamic Web System
*Learning Objective: Understand dynamic web systems*

The system must be dynamic, meaning content changes based on user interactions or data (e.g., user profiles, real-time updates).

**REQ1**: Students must propose project proposal document and get it approved by the instructors

**REQ2**: System must demonstrate content adaptation based on approved proposal design, specifically system must implement at least two types of dynamic behavior (e.g., user-specific content, real-time data updates, adaptive interfaces)

### 2. Full-Stack Implementation
*Learning Objective: Build dynamic web systems*

The system must be a full-stack web application with frontend, backend, and database components, and be based on microservices architecture.

**REQ3**: System must include functional frontend using React (recommended), Vue (limited support), or Angular (no support) - **Note: Minimal focus, backend emphasis**

**REQ4**: System must include backend API built with Node.js/Python/Go (recommended)

**REQ5**: System must achieve minimum 50% code coverage on backend services (UI testing not required)

**REQ6**: System must include functional GitHub Actions CI/CD pipeline

**REQ7**: System must include at least 2 endpoint failure test cases per service/components (e.g., unauthorized access, validation errors)

**REQ8**: System must select and implement a suitable database technology (e.g., PostgreSQL, MongoDB) with justification for the choice based on project requirements

**REQ9**: System must include documented and well-designed database schema with proper relationships (must be able to explain and motivate design choices)

### 3. Cloud-Native Deployment
*Learning Objective: Deploy and manage web systems in cloud environments*

The system must be deployed in a cloud-native manner using containerization and orchestration tools.

**REQ10**: System must include Docker containerization

**REQ11**: System must implement microservices architecture with multiple logical services (e.g., user service, content service)

**REQ12**: System must include Kubernetes deployment for all components using Helm charts

**REQ13**: Project must include observability and monitoring tools (Prometheus/Grafana or equivalent)

### 4. API Design & Communication
*Learning Objective: Create application-programming interface*

The system must expose a well-designed API for frontend-backend communication and inter-service communication.

**REQ14**: System must implement RESTful API with proper HTTP methods and status codes

**REQ15**: System must implement loosly coupled where indvidual microservices can be updated, restarted seperately, e.g implement an event-driven architecture using message queues (RabbitMQ, Kafka) for intra-communication between microservices.

**REQ16**: System must include comprehensive API documentation using OpenAPI/Swagger/AsyncAPI specifications

### 5. System Design & Architecture
*Learning Objective: Model, simulate, predict and evaluate web systems*

The system must demonstrate sound architectural design principles and performance considerations.

**REQ17**: Project must include comprehensive architecture diagram using C4 model or equivalent architectural documentation, and documentation in GitHub repository

**REQ18**: Project must include performance analysis with load testing results and bottleneck identification

**REQ19**: Project must include implemented script/tool that generates traffic to simulate system load

### 6. Security & Ethics
*Learning Objective: Ethical handling of sensitive data*

The system must implement security best practices and consider ethical implications of data handling.

**REQ20**: System must implement secure authentication using JWT or OAuth 2.0 based on Keycloak

**REQ21**: System must provide authorization mechanisms to restrict access to sensitive data and operations based on user roles

**REQ22**: Project must include documented protection against SQL injection and XSS attacks

**REQ23**: Project must implement HTTPS for all communications using SSL/TLS certificates (automatic via Let's Encrypt)

**REQ24**: Project must include documentation of certificate management and automatic renewal processes

**REQ25**: Project must include GDPR compliance considerations and data privacy measures documentation

**REQ26**: Project must document how data privacy measures (e.g., data minimization, user consent) are implemented

**REQ27**: Project must include ethical analysis of sensitive data handling, privacy implications, and societal impact

## Advanced Features (Choose One for Higher Grades)
To achieve Grade 4 or 5, teams must implement one advanced feature from the options below to enhance their chosen project. This is in addition to all core requirements.

### Option A: Advanced Personalization
Add intelligent personalization capabilities to your existing application.

**Example Features:**
- **Collaborative Filtering**: Real-time user similarity recommendations adapted to your domain
- **Dynamic UI Updates**: Interface elements that adapt in real-time based on user behavior
- **LLM/MCP Integration**: Context-aware content suggestions based on user preferences (Note: students must pay for their own LLM API usage e.g., OpenAI, Anthropic, or use local models with Ollama, etc. Does not work on provided K8s cluster)

### Option B: Advanced Cloud-Native Architecture
Enhance your application with sophisticated cloud-native patterns.

**Example Features:**
- **Event Sourcing**: Store all user actions as events for complex querying and system reconstruction
- **Service Mesh**: Implement Istio for advanced traffic management and observability
- **Custom Kubernetes Operators**: Build operators for auto-scaling based on your application's specific metrics
- **Distributed Tracing**: Track request flows across your microservices for performance optimization
- **GitOps CI/CD**: Implement advanced deployment pipelines with automated rollbacks

### Option C: Progressive Web App (PWA) with Offline Support
Transform your application to work seamlessly offline.

**Example Features:**
- **Service Workers**: Cache your application's assets and API responses for offline functionality
- **Local Data Management**: Store user data locally with conflict-free synchronization when online
- **Push Notifications**: Engage users with notifications even when your app is closed
- **Responsive Design**: Optimize your interface for all device types and screen sizes
- **Performance Optimization**: Achieve fast load times and smooth interactions

### Option D: Advanced Security Features
Implement enterprise-grade security for your application.

**Example Features:**
- **Zero-Trust Model**: Authenticate and authorize every request, including internal communications
- **End-to-End Encryption**: Encrypt all sensitive data at rest and in transit
- **Role-Based Access Control (RBAC)**: Implement fine-grained permissions for your user types
- **Security Auditing**: Log and monitor all access and changes to sensitive data
- **Automated Security Testing**: Integrate security scans into CI/CD pipeline with vulnerability detection

### Option E: Advanced Real-Time Features
Add sophisticated real-time capabilities to your application.

**Example Features:**
- **WebSocket Scaling**: Handle high concurrent user loads with live updates
- **Real-Time Collaboration**: Enable simultaneous multi-user interactions with conflict resolution
- **Live Data Synchronization**: Provide instant updates across all connected clients
- **Connection Resilience**: Implement automatic reconnection and state recovery for real-time sessions

# Grading Criteria

**IMPORTANT**: Teams receive **shared grades** based on system quality and implementation. Each team member must **pass individual oral examination** to receive the team grade.

## Individual Oral Examination (Pass/Fail Requirement)
Each student is examined **individually** (20-minute session) and must demonstrate understanding of:
- Personal contributions to the system architecture and implementation
- System architecture, data flow, and component interactions
- Technologies used and fundamental concepts
- Security implementation and testing approaches
- Ability to troubleshoot and modify the system

**Individual Assessment**: Each team member must pass their individual oral examination to receive the team grade. If any team member fails the oral exam, they receive a failing grade regardless of team system quality.

## Grade Levels

### Grade 3
- All core technical requirements (REQ1-REQ27) fully implemented
- 50%+ test coverage on backend code with comprehensive failure scenario testing
- Working Kubernetes deployment with proper monitoring
- Complete project documentation

### Grade 4
- All Grade 3 requirements significantly exceeded in quality and sophistication
- One advanced feature (Option A-E) successfully implemented
- 60%+ test coverage including integration tests and edge cases
- Comprehensive documentation and monitoring
- Exceptional architectural design or performance optimization

### Grade 5
- All Grade 4 requirements met
- Scientific Evaluation with quantitative analysis demonstrating advanced system capabilities. **Note**: Students must demonstrate rigorous, quantitative evaluation in their chosen area(s). The goal is scientific rigor and technical depth, not just feature addition.

**Scientific Evaluation Options** (choose at least one with rigorous scientific analysis):

**Scalability Analysis:**
- Load testing script/tool that generates realistic traffic to simulate system load
- Documented evidence of how system scales (horizontally/vertically) to handle increased load
- Performance metrics and bottleneck identification under various load conditions

**Resiliency Analysis:**
- High availability implementation for critical services (e.g., user authentication)
- Chaos engineering script/tool that randomly restarts critical microservices to simulate failures
- Documented analysis of how system handles failures with minimal user impact
- Evidence of seamless microservice updates without affecting user experience

**Advanced Feature Evaluation:**
- Quantitative analysis of advanced feature performance and effectiveness
- Comparative analysis showing improvement over baseline implementation
- Technical innovation demonstrating deep understanding of web systems principles

**Advanced Testing Strategy:**
- 70%+ test coverage with end-to-end tests
- Comprehensive edge case and failure scenario testing using mockups/emulators/simulations
- Automated testing pipeline with multiple test environments and deployment strategies

AP: Johan
Announcement course start
Avboka pass/lektioner ej använda
Lektion: Intro 
Tutorial: CI/CD/Gitops
Tutoral: Keycloak
Skapa VM:ar/Kubernetes

AP: Casper
Canvas: Flytta in material in Canvas
Förbereda workshops 
Canvas: Länkar till videos/publikt material
Midterm demo
Presentation guidelines
