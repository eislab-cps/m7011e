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

### 1. Full-Stack Implementation
*Learning Objective: Build dynamic web systems*

- **Frontend**: React/Vue/Angular (student choice) - **Note: Focus minimal, backend emphasis**
- **Backend API**: Node.js/Python (recommended) or Go/Rust (advanced, limited TA support)
- **Database**: PostgreSQL (recommended) or MongoDB (justify choice)
- **Deployment**: All components deployed on Kubernetes with Helm charts

**Stack Recommendations by Experience:**
- **Beginner-Friendly**: Node.js + Express + PostgreSQL + React
- **Python Preference**: Python + FastAPI + PostgreSQL + Vue
- **Advanced Challenge**: Go/Rust + PostgreSQL + Angular (limited support)

### 2. API Design & Communication
*Learning Objective: Create application-programming interface*

- **RESTful API** with proper HTTP methods and status codes
- **Authentication**: JWT or OAuth 2.0 implementation
- **API Documentation**: OpenAPI/Swagger specifications
- **Input Validation**: Comprehensive request validation and sanitization

### 3. System Design & Architecture
*Learning Objective: Model, simulate, predict and evaluate web systems*

- **Architecture Diagram**: C4 model or similar architectural documentation
- **Database Schema**: Well-designed schema with proper relationships
- **Performance Analysis**: Load testing results and bottleneck identification
- **Scalability Plan**: Detailed plan for handling 100x current user load

### 4. Security & Ethics
*Learning Objective: Ethical handling of sensitive data*

- **Secure Authentication**: Proper password hashing, session management
- **Input Sanitization**: Protection against SQL injection, XSS attacks
- **HTTPS**: SSL/TLS certificates (automatic via Let's Encrypt)
- **Data Privacy**: GDPR compliance considerations documented

### 5. Production Readiness
*Learning Objective: Professional development practices*

- **CI/CD Pipeline**: GitHub Actions or GitLab CI with automated deployments
- **Automated Testing**: Minimum 60% code coverage on backend (not UI)
- **Error Handling**: At least 2 endpoint failure test cases (e.g., unauthorized access, validation errors)
- **Monitoring**: Basic monitoring with Prometheus/Grafana or equivalent
- **Documentation**: README, API docs, deployment guide

## Advanced Features (Choose One for Higher Grades)

### Option A: Real-Time Features
- WebSocket implementation for live updates
- Real-time notifications or messaging
- Collaborative editing capabilities
- Live presence indicators

### Option B: AI Integration
- LLM chatbot integration
- Recommendation system with collaborative filtering
- Semantic search functionality
- AI-generated content or insights

### Option C: Performance Optimization
- Redis caching strategy implementation
- CDN integration for static assets
- Database query optimization
- Performance monitoring and alerting

### Option D: Advanced DevOps
- Comprehensive Grafana monitoring dashboards
- Blue-green or canary deployment strategy
- Feature flags system
- Chaos engineering or resilience testing

## Grading Criteria

**IMPORTANT**: Grades measure **individual technical knowledge**, not feature quantity or visual design. Each team member will have an **individual oral examination** to demonstrate their understanding of:
- System architecture decisions and trade-offs
- Security implementations and vulnerability prevention  
- Code they wrote and why they wrote it that way
- How their component integrates with the overall system
- Alternative approaches they considered

### Grade 3 (Pass) - **Knowledge Requirements**
- **Individual Understanding**: Can explain their own code and basic system design
- **Architecture Knowledge**: Understands monolithic vs microservices trade-offs
- **Security Awareness**: Can explain authentication flow and basic security measures
- **Testing Knowledge**: Understands what their tests validate and why
- **Deployment Understanding**: Can explain Docker and Kubernetes basics
- **Integration Knowledge**: Understands how frontend/backend/database connect

### Grade 4 (Good) - **Knowledge Requirements**
- **Advanced Architecture**: Can justify architectural decisions and discuss alternatives
- **Deep Security Knowledge**: Understands OWASP top 10, can explain threat modeling
- **Testing Strategy**: Can explain test pyramid, integration vs unit tests, edge cases
- **DevOps Understanding**: Can explain CI/CD pipeline stages and deployment strategies  
- **Performance Awareness**: Can identify bottlenecks and explain caching strategies
- **System Integration**: Understands service communication, error handling, monitoring

### Grade 5 (Excellent) - **Knowledge Requirements**
- **Expert Architecture**: Can discuss scalability patterns, CAP theorem, distributed systems
- **Security Expert**: Can explain zero-trust principles, secure coding practices, compliance
- **Advanced DevOps**: Can explain blue-green vs canary deployments, chaos engineering
- **System Design**: Can design systems for scale, explain database sharding, caching layers
- **Performance Expert**: Can explain profiling, optimization strategies, monitoring best practices
- **Innovation**: Can propose and justify novel solutions, discuss emerging technologies
- **Teaching Ability**: Can explain complex concepts clearly, mentor others

## Deliverables & Realistic Timeline

1. **Week 1**: Project proposal (1 page)
2. **Week 2**: Database design + local development setup
3. **Week 3**: Core API implementation + basic tests
4. **Week 4**: Docker containerization + basic Kubernetes deployment
5. **Week 5**: Authentication + security implementation
6. **Week 6**: Advanced features + CI/CD pipeline
7. **Week 7**: Production hardening + comprehensive testing
8. **Week 8**: Final presentation and demonstration

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
- **Live Demo**: Working application deployed on Kubernetes
- **Documentation**: Comprehensive README and technical documentation
- **Individual Oral Examination**: Each team member examined separately on:
  - Their specific contributions and implementation decisions
  - Understanding of the overall system architecture
  - Alternative approaches and trade-offs considered
  - Ability to extend or modify the system
  - Knowledge of underlying technologies and principles

## Important Guidelines

### AI Usage Policy
- AI tools (ChatGPT, Claude, Cursor) encouraged for learning and development
- You must understand and be able to explain ALL code and design decisions
- 60%+ test coverage required for all AI-generated code
- Full accountability for submitted work regardless of origin

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
| 8 | Presentation | Demo day, oral examinations |

---

**Remember**: Focus on backend architecture, security, and scalability. The goal is to build a production-ready system that demonstrates enterprise-level development practices.