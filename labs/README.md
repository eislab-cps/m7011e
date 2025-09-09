# Lab Assignment: Build Your Own Dynamic Web System

## Overview

This is the main lab assignment for the **Design of Dynamic Web Systems (M7011E)** course. You will design and implement a complete dynamic web system that demonstrates modern full-stack development principles, cloud-native deployment, and production-ready practices.

## Prerequisites

Based on your completed courses, you should have:
- **Programming Skills**: Object-oriented programming experience (Java/similar)
- **Database Knowledge**: SQL and database design principles
- **Web Basics**: Client-server communication concepts
- **Version Control**: Git experience for collaborative development

**New Technologies You'll Learn**: Docker, Kubernetes, CI/CD pipelines, cloud-native development patterns.

## Assignment Structure

### Students work in teams of 3 people (or 2 if odd number of students)
- Choose your own project idea
- Must fulfill all core technical requirements  
- Focus on backend architecture, security, and scalability
- **Each team gets dedicated Kubernetes cluster access**
- **Technology Stack Support**: Full support for Node.js/Python, basic guidance for Go/Rust

## Project Proposal (Week 1)

Submit a **1-page proposal** including:

📋 **Use the [Project Proposal Template](project-proposal-template.md)** for detailed guidance and structure.

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

📋 **See [Technical Requirements](technical-requirements.md)** for detailed specifications.

### 0. Dynamic Web System
*Learning Objective: Understand dynamic web systems*
- **Dynamic Content**: Content changes based on user interactions or data (e.g., user profiles, real-time updates)
Task 1: Design and propose a dynamic web system (see project proposal template)

### 1. Full-Stack Implementation
*Learning Objective: Build dynamic web systems*

- **Frontend**: React (recommended) Vue (limited TA support) Angular (no suppport) (student choice) - **Note: Focus minimal, backend emphasis**
- **Backend API**: Node.js/Python/Go (recommended)
- **Database**: PostgreSQL or MongoDB or omething else (student choice)
Task 1: Well-designed schema with proper relationships (must be able to explain and motivate design choices) 
Task 2: Docment in Github
- **Containerization**: Docker for all services with multi-stage builds
- **Deployment**: All components deployed on Kubernetes with Helm charts
- **Microservices architecture**: Brake down into multiple services (e.g., user service, content service)
- **Testing**: Minimum 60% code coverage on backend (not UI)
Task 1: Implement tests (unit/integration). At least 2 endpoint failure test cases (e.g., unauthorized access, validation errors)
Task 2: Implement Github action (see tutorials provided)
- **Documentation**: README, API docs, deployment guide

### 2. API Design & Communication
*Learning Objective: Create application-programming interface*

- **RESTful API**: with proper HTTP methods and status codes
- **Event-driven architecture**: Use message queues (e.g., RabbitMQ, Kafka) to decouple services (loosly coupled)
- **Authentication**: JWT or OAuth 2.0 implementation based on Keyclock
- **API Documentation**: OpenAPI/Swagger/Async API specifications

### 3. System Design & Architecture
*Learning Objective: Model, simulate, predict and evaluate web systems*

- **Architecture Diagram**: C4 model or similar architectural documentation
Task 1: Document in Github
- **Database Schema**: Well-designed schema with proper relationships (must be able to explain and motivate design choices) 
Task 1: Docment in Github
- **Performance Analysis**: Load testing results and bottleneck identification 
Task 1: Implement script/tool that generate traffic to simulate load. 
Task 2: Implement tool for observability and monitoring (Prometheous/Grafana or equivalent).
Task 3: Document performance metrics and bottlenecks identified using monitoring tools

### 4. Security & Ethics
*Learning Objective: Ethical handling of sensitive data*

- **Secure Authentication**: Proper password hashing, session management
Task 1: Implement secure authentication mechanism (e.g., JWT, OAuth 2.0)
Task 2: Document protection against SQL injection, XSS attacks
- **HTTPS**: SSL/TLS certificates (automatic via Let's Encrypt)
Task 1: Implement HTTPS for all communications (see tutorials provided)
Task 2: Document how certificates are managed and renewed
- **Data Privacy**: GDPR compliance considerations documented
Task 1: Document how GDRP data privacy measures (e.g., data minimization, user consent) could be implemented. Being able to reason about Etnical handling of sensitive data, how does the system ensure data privacy and security? How does it affect the world? 

## Advanced Features (Choose One for Higher Grades)

### Option A: Advanced Personalization
**Example**: Recipe sharing platform with live recommendation updates. The web system must be context aware and adapt to content, previous user interactions, and real-time events.

For example)
- **Collaborative filtering**: "Users similar to you just liked..." appears immediately  
- **LLM/MCP integration**: Personalized recipe suggestions based on dietary preferences. Note students must pay for their own LLM API usage (e.g., OpenAI, Anthropic), or model on local machines using Ollama, etc. Does not work on provided K8s cluster.
- **Dynamic UI updates**: Recommendations update in real-time as user interacts, adapts based on user task

### Option B: Advanced Cloud-Native Architecture  
**Example**: Event-driven microservices for social media platform

Examles)
- **Event sourcing for user activities**: All user actions stored as events, enabling complex queries
- **Microservices with service mesh**: User service, content service, notification service with Istio
- **Advanced Kubernetes operators**: Custom operators for auto-scaling based on user engagement
- **Distributed tracing**: Track request flow across microservices for performance optimization
- **CI/CD/GitOps**: GitHub Actions or GitLab CI with automated deployments



### Option C: Progresss Web App (PWA) with Offline Support
**Example**: Fitness tracking app with offline capabilities
- **Service Workers**: Cache assets and API responses for offline use
- **IndexedDB/CRDT**: Store user data locally when offline, sync when back online
- **Push Notifications**: Remind users of workouts even when app is closed
- **Responsive Design**: Works seamlessly across devices
- **Performance Optimization**: Fast load times and smooth interactions

### Option D: Advanded Security Features<F15>
**Example**: Zero-trust architecture, role-based access control
- **Zero-trust model**: Every request authenticated and authorized, even within the network
- **Encryption at rest and in transit**: All sensitive data encrypted using strong algorithms
- **Role-based access control (RBAC)**: Fine-grained permissions for different user roles
- **Security Auditing**: Log and monitor all access and changes to sensitive data
- **Automated Security Testing**: Integrate security scans into CI/CD pipeline

### Option E: Advanded Real-Time Features
**Example**: Real-time multi-player game or collaborative tool

For example)
- **WebSocket-based live updates**: When user likes a recipe, recommendations instantly update
- **Live cooking session features**: Real-time ingredient substitution suggestions during cooking

## Grading Criteria

**IMPORTANT**: **Team receives shared grade** based on system quality and implementation. Each team member must **pass individual oral examination** to receive the team grade. The oral exam verifies you participated meaningfully in technical work and understand:
- Your personal contributions to the system
- Basic system architecture and data flow
- Technologies used and fundamental concepts
- Security and testing approaches implemented

### Team Grading Based on System Quality

**All team members receive the same grade based on the delivered system:**

#### Grade 3 (Pass) - **System Requirements**
- All core technical requirements implemented
- 50%+ test coverage on backend code

#### Grade 4 (Good) - **System Requirements**  
- Previous grade 3 requirements met
- Advanced feature implemented (Option A-E)
- 60%+ test coverage including integration tests and edge cases
- Comprehensive documentation and monitoring

#### Grade 5 (Excellent) - **System Requirements**
- Previous grade 4 requirements met
- Scientific sound evaluation of advanced implementation (options A-E), for example, being able to to demonstrate how the system can be scaled (horizontally/vertically) to handle increased load, demonstrate how the system handles failures and ensures minimal user impact, off line support.
- 70%+ test coverage with end-to-end tests, strategy how to handle edge cases and failure scenarios with mockups/emulators/simulations etc.

TODO: Fix the the text below and 
**Scalability Plan**: Detailed plan for handling 100x current user load
Tasks 1: Implement script/tool that generate traffic to simulate load.
Tasks 2: Document how system can be scaled (horizontally/vertically) to handle increased load.

- **Resiliency Plan**: Evaluate how user experience implication of restarting microservices. 
Task 1: Implement high availability for critical services (e.g., user authentication)
Task 2: Implement script/tool that randomly restart critical microservices to simulate failure.
Task 3: Document how system handles failures and ensures minimal user impact. Can it be done seamlessly wihtout affecting user experience? How can microservices be updated?

NOTE: Social impact and business model are not graded, but should be considered in project proposal, and is condifered for the rigid scientific sound evaluation of advanced implementation (options A-E).

### Oral Examination: Pass/Fail Requirement

**To receive your team grade, you must PASS the individual oral examination by demonstrating:**
- Understanding of your personal contributions
- Basic system architecture knowledge
- Familiarity with technologies used
- Awareness of security and testing implementations

📋 **See [Oral Examination Guide](oral-examination-guide.md)** for detailed preparation instructions and assessment criteria.

## Deliverables & Realistic Timeline

1. **Week 1**: Project proposal (1 page)
2. **Week 2**: Database design + local development setup
3. **Week 3**: Core API implementation + basic tests
4. **Week 4**: Docker containerization + basic Kubernetes deployment
5. **Week 5**: Authentication + security implementation
6. **Week 6**: Advanced features + CI/CD pipeline
7. **Week 7**: Production hardening + comprehensive testing
8. **Week 8**: Individual oral examinations with TA demo

**Kubernetes Learning Path**: Weeks 1-2 tutorials, Week 4 deployment, Weeks 5-7 optimization

## Technical Support

**Infrastructure Support:**
- **Dedicated Kubernetes cluster per team** (K3s with Rancher UI)
- Full cluster admin privileges for experimentation
- Persistent storage and load balancer access
- **No resource conflicts** - each team has isolated environment

**Learning Support:**
- Weekly lab sessions with instructor and TA
- **Full support**: Node.js (Express), Python (FastAPI), PostgreSQL, React/Vue
- **Basic guidance**: Go, Rust, MongoDB, Angular
- Office hours available on demand
- Canvas discussion forum for questions
- Hands-on workshops for Docker/Kubernetes fundamentals

**Cluster Experimentation**: Freedom to try different K8s configurations without affecting other teams

## Submission Requirements

- **Git Repository**: All code in version control with meaningful commits
- **TA Demo**: Working application demonstration to teaching assistant
- **Documentation**: Comprehensive README and technical documentation
- **Pre-Assessment Document**: Individual technical reflection (2 pages) submitted before oral exam
  - 📋 **Use [Pre-Assessment Document Template](pre-assessment-document.md)**
- **AI Usage Portfolio**: Documentation of AI interactions and validation process
  - 📋 **Use [AI Usage Portfolio Template](ai-usage-portfolio.md)**
- **Individual Oral Examination**: 20-minute pass/fail examination to verify technical understanding
  - Must pass to receive team grade
  - Focuses on design decisions, system understanding, and AI collaboration effectiveness

## Important Guidelines

### AI-Assisted Development Policy

**AI tools (Claude Code, ChatGPT, Cursor, etc.) are strongly encouraged** for modern software development practices.

#### **Encouraged AI Usage:**
- Code generation and implementation assistance
- Architecture and design pattern suggestions  
- Documentation and comment generation
- Debugging and error resolution
- Test case generation and validation

#### **Your Responsibilities:**
- **Understand everything**: Must explain all design decisions and architectural choices
- **Validate AI output**: Test and verify all AI-generated code thoroughly
- **Document AI interactions**: Maintain log of AI usage and validation process
- **Own the decisions**: You are accountable for all technical choices, regardless of origin

#### **Assessment Focus:**
- **Design reasoning**: Why did you choose this architecture/approach?
- **Alternative evaluation**: What other options did you consider?
- **AI collaboration**: How effectively did you use AI assistance?
- **System understanding**: Can you modify and extend the system?

**Key Principle**: Assessment focuses on your **engineering judgment and system understanding**, not code authorship.

### Academic Integrity
- Work must be original to your team
- Proper attribution for external libraries and resources
- No copying from other student projects
- Collaboration between teams is encouraged, but implementations must be unique

## Timeline

| Week | Focus | Deliverables |
|------|-------|-------------|
| 1 | Project Planning | Proposal, Team Formation |
| 2 | Architecture & Setup | Database design, Kubernetes deployment |
| 3 | Core Development | Basic API endpoints, Authentication |
| 4 | Integration | Frontend-backend connection, CI/CD |
| 5 | Advanced Features | Choose and implement advanced option |
| 6 | Testing & Security | Comprehensive testing, security review |
| 7 | Polish & Documentation | Final documentation, performance tuning |
| 8 | Assessment | Individual oral examinations, TA demos |

---

**Remember**: Focus on backend architecture, security, and scalability. The goal is to build a production-ready system that demonstrates enterprise-level development practices.

---

## Supporting Documents

📚 **Complete Lab Assignment Documentation:**

- **[Project Proposal Template](project-proposal-template.md)** - Detailed template for Week 1 submission
- **[Technical Requirements](technical-requirements.md)** - Comprehensive technical specifications  
- **[Grading Rubric](grading-rubric.md)** - Detailed assessment criteria and point breakdown
- **[Pre-Assessment Document Template](pre-assessment-document.md)** - Individual reflection template
- **[AI Usage Portfolio Template](ai-usage-portfolio.md)** - AI collaboration documentation template
- **[Oral Examination Guide](oral-examination-guide.md)** - Preparation guide and assessment criteria

💡 **Read all supporting documents** before starting your project to understand the complete requirements and expectations.
