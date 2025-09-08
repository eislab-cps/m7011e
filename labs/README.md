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

### Option A: Real-Time Personalization
**Example**: Recipe sharing platform with live recommendation updates
- **WebSocket-based live updates**: When user likes a recipe, recommendations instantly update
- **Real-time collaborative filtering**: "Users similar to you just liked..." appears immediately  
- **Live cooking session features**: Real-time ingredient substitution suggestions during cooking
- **Dynamic difficulty adjustment**: Recipe complexity adapts based on user's cooking success rate

### Option B: AI-Powered Dynamic Content with LLM Integration
**Example**: Study group platform with MCP-enabled AI tutoring system
- **MCP-powered AI agents**: Implement Model Context Protocol for sophisticated AI tool integration
- **Dynamic LLM interactions**: Claude/GPT integration that adapts responses based on user's learning progress
- **Contextual knowledge retrieval**: AI agents access course materials, user progress, and learning analytics
- **Personalized content generation**: LLMs generate custom explanations, quizzes, and study materials
- **Multi-modal AI responses**: Text, code examples, and structured data based on learning context
- **AI workflow automation**: Autonomous task planning for personalized study schedules

### Option C: Data-Driven Dynamic Features
**Example**: Fitness tracking app with behavioral adaptation
- **Usage pattern analysis**: Track when/how users interact with different features
- **Dynamic dashboard layouts**: Homepage widgets reorder based on user's most-used features
- **Behavioral workout recommendations**: Suggest exercises based on user's activity patterns and preferences
- **Context-aware notifications**: Notification timing/content adapts based on user's response patterns

### Option D: Advanced Cloud-Native Architecture  
**Example**: Event-driven microservices for social media platform
- **Event sourcing for user activities**: All user actions stored as events, enabling complex queries
- **Microservices with service mesh**: User service, content service, notification service with Istio
- **Advanced Kubernetes operators**: Custom operators for auto-scaling based on user engagement
- **Distributed tracing**: Track request flow across microservices for performance optimization

### Option E: Real-Time Collaborative Editing
**Example**: Collaborative documentation platform with live editing capabilities
- **CRDT implementation**: Conflict-free Replicated Data Types for seamless multi-user editing
- **Real-time cursors and selections**: See other users' cursors, selections, and edits in real-time
- **Operational transforms**: Handle concurrent edits without conflicts or data loss
- **Presence awareness**: Show who's online and actively editing documents
- **Version history with branching**: Track document changes with ability to branch and merge edits
- **WebSocket scaling**: Horizontal scaling of real-time connections across multiple servers

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
- Basic security measures (authentication, HTTPS, input validation)
- 60% test coverage with functional tests
- Working Kubernetes deployment
- Basic documentation

#### Grade 4 (Good) - **System Requirements**  
- Well-structured architecture with clear component separation
- One advanced feature implemented (real-time, AI, performance, or advanced DevOps)
- 70%+ test coverage including integration tests and edge cases
- Comprehensive documentation and monitoring
- CI/CD pipeline with multiple environments

#### Grade 5 (Excellent) - **System Requirements**
- Production-ready system with advanced architecture
- Two advanced features demonstrating innovation
- Comprehensive testing, security, and monitoring
- Advanced DevOps practices (blue-green deployment, observability)
- Exceptional documentation and system design

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
