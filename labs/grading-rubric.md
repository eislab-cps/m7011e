# Grading Rubric: Dynamic Web System Project

## Overview

**GRADING MODEL**: Teams receive **shared grades** based on system quality and implementation. Individual students must **pass oral examination** to receive the team grade.

**Evaluation Focus**: 
- **Team Grade**: System architecture, feature implementation, production readiness
- **Individual Requirement**: Pass/fail oral exam verifying meaningful technical participation
- **NOT**: Individual performance differences, feature count, or visual design

## Team Grading Scale

| Grade | Description | System Requirements |
|-------|-------------|-------------------|
| **5** | Excellent | Production-ready system + 2 advanced features + exceptional documentation |
| **4** | Good | Well-structured system + 1 advanced feature + comprehensive testing |
| **3** | Satisfactory | All core requirements + basic implementation + working deployment |
| **F** | Fail | Core requirements not met OR student fails oral examination |

---

## Core Requirements (Required for Passing)

### 1. Full-Stack Implementation (20 points)

| Criteria | Grade 5 (18-20 pts) | Grade 4 (14-17 pts) | Grade 3 (10-13 pts) | Fail (0-9 pts) |
|----------|---------------------|---------------------|---------------------|-----------------|
| **Backend Architecture** | Microservices or well-structured monolith with clear separation | Well-organized monolith with clear modules | Basic monolithic structure | Poor structure, mixed concerns |
| **API Design** | RESTful with comprehensive endpoints, proper HTTP methods/status codes | RESTful with most endpoints, good HTTP practices | Basic REST API with essential endpoints | Non-RESTful or poorly designed API |
| **Database Design** | Optimized schema with proper relationships, indexing | Good schema design with relationships | Basic schema meeting requirements | Poor schema design |
| **Frontend Integration** | Seamless API integration with error handling | Good integration with basic error handling | Basic functional integration | Poor or non-functional integration |

### 2. Authentication & Security (15 points)

| Criteria | Grade 5 (14-15 pts) | Grade 4 (11-13 pts) | Grade 3 (8-10 pts) | Fail (0-7 pts) |
|----------|---------------------|---------------------|---------------------|-----------------|
| **Authentication** | Robust JWT/OAuth with refresh tokens, secure storage | JWT/OAuth properly implemented | Basic authentication working | Weak or broken authentication |
| **Authorization** | RBAC implemented, proper access control | Basic role separation | Simple user/admin distinction | No authorization controls |
| **Input Validation** | Comprehensive validation, sanitization, XSS/SQL injection prevention | Good validation on most inputs | Basic validation implemented | Minimal or no validation |
| **HTTPS & Security** | Full HTTPS, security headers, secure coding practices | HTTPS implemented, basic security measures | HTTPS working | No HTTPS or security measures |

### 3. Cloud-Native Deployment (15 points)

| Criteria | Grade 5 (14-15 pts) | Grade 4 (11-13 pts) | Grade 3 (8-10 pts) | Fail (0-7 pts) |
|----------|---------------------|---------------------|---------------------|-----------------|
| **Containerization** | Optimized multi-stage Dockerfiles, security best practices | Well-structured Dockerfiles | Basic working Dockerfiles | Poor or non-functional containers |
| **Kubernetes Deployment** | Complete Helm charts, resource management, health checks | Good Helm charts, basic resource management | Basic Kubernetes deployment | Non-functional K8s deployment |
| **Configuration Management** | Proper secrets, ConfigMaps, environment separation | Good use of secrets and configs | Basic configuration setup | Hardcoded configurations |

### 4. Testing & Quality (15 points)

| Criteria | Grade 5 (14-15 pts) | Grade 4 (11-13 pts) | Grade 3 (8-10 pts) | Fail (0-7 pts) |
|----------|---------------------|---------------------|---------------------|-----------------|
| **Test Coverage** | >75% coverage, unit + integration + edge cases | 70%+ coverage, good test variety | 60%+ coverage, basic tests | <60% coverage or poor tests |
| **Error Handling** | Comprehensive error scenarios, graceful failures | Good error handling, some edge cases | Basic error cases covered | Poor error handling |
| **Code Quality** | Clean, well-documented, following best practices | Good code organization and practices | Acceptable code quality | Poor code quality |

### 5. CI/CD & DevOps (10 points)

| Criteria | Grade 5 (9-10 pts) | Grade 4 (7-8 pts) | Grade 3 (5-6 pts) | Fail (0-4 pts) |
|----------|---------------------|---------------------|---------------------|-----------------|
| **CI/CD Pipeline** | Comprehensive pipeline, automated testing, security scanning | Good pipeline with testing | Basic automated deployment | Manual or broken deployment |
| **Monitoring** | Comprehensive monitoring, logging, alerting | Basic monitoring implemented | Minimal monitoring setup | No monitoring |

---

## Advanced Features (Choose 1 for Grade 4, 2 for Grade 5)

### Real-Time Features (10 points)

| Implementation Quality | Points | Description |
|----------------------|--------|-------------|
| **Excellent** | 9-10 | WebSockets with scaling considerations, real-time collaboration |
| **Good** | 7-8 | Working WebSocket implementation, basic real-time features |
| **Basic** | 5-6 | Simple real-time updates implemented |
| **Poor** | 0-4 | Non-functional or poorly implemented |

### AI Integration (10 points)

| Implementation Quality | Points | Description |
|----------------------|--------|-------------|
| **Excellent** | 9-10 | Sophisticated AI features, proper error handling, cost optimization |
| **Good** | 7-8 | Working AI integration with good user experience |
| **Basic** | 5-6 | Basic AI functionality implemented |
| **Poor** | 0-4 | Non-functional or poorly implemented |

### Performance Optimization (10 points)

| Implementation Quality | Points | Description |
|----------------------|--------|-------------|
| **Excellent** | 9-10 | Multi-layer caching, CDN, database optimization, performance testing |
| **Good** | 7-8 | Good caching strategy, performance improvements demonstrated |
| **Basic** | 5-6 | Basic caching or optimization implemented |
| **Poor** | 0-4 | Minimal or no optimization |

### Advanced DevOps (10 points)

| Implementation Quality | Points | Description |
|----------------------|--------|-------------|
| **Excellent** | 9-10 | Comprehensive monitoring, advanced deployment strategies, resilience testing |
| **Good** | 7-8 | Good monitoring and deployment practices |
| **Basic** | 5-6 | Basic advanced DevOps practices |
| **Poor** | 0-4 | Minimal or poorly implemented |

---

## Documentation & Communication (15 points)

### Documentation Quality

| Criteria | Grade 5 (14-15 pts) | Grade 4 (11-13 pts) | Grade 3 (8-10 pts) | Fail (0-7 pts) |
|----------|---------------------|---------------------|---------------------|-----------------|
| **Architecture Documentation** | Complete C4 diagrams, comprehensive system documentation | Good architectural documentation | Basic architecture documented | Poor or missing documentation |
| **API Documentation** | Interactive OpenAPI docs, comprehensive examples | Good API documentation | Basic API documentation | Poor or missing API docs |
| **Setup Instructions** | Complete deployment guide, automated setup | Good setup instructions | Basic setup documented | Poor or missing instructions |

## Individual Oral Examination (Pass/Fail)

**Each student examined separately for 20 minutes**

### Pass Criteria (Required to receive team grade):

| Assessment Area | Pass Requirement |
|----------------|------------------|
| **Design Decision Ownership** | Can explain and justify architectural and implementation decisions they were involved in |
| **System Architecture** | Can draw basic system architecture and explain component interactions and data flow |
| **AI Collaboration** | Can demonstrate effective use of AI tools and validation of AI-generated solutions |
| **Technology Understanding** | Shows familiarity with key technologies and can explain trade-offs and alternatives |
| **Problem-Solving** | Can modify system components and reason about hypothetical changes or improvements |

### Fail Conditions (Receives failing grade regardless of team performance):

- Cannot explain or justify design decisions they were involved in
- No understanding of basic system architecture or data flow
- Cannot demonstrate how they validated AI-generated code or suggestions
- Cannot answer fundamental questions about technologies used or their trade-offs
- Cannot reason about system modifications or improvements
- Clear evidence of minimal participation in technical decision-making
- Cannot demonstrate understanding of security or testing approaches

---

## Final Grade Assignment

### Grade Assignment Formula:
```
IF (student passes oral exam) AND (team system meets requirements):
    student_grade = team_system_grade
ELSE:
    student_grade = FAIL
```

### Team System Grade Determination:

**Grade 5**: Production-ready system with 2 advanced features, exceptional documentation, comprehensive testing and monitoring

**Grade 4**: Well-structured system with 1 advanced feature, good documentation, solid testing and CI/CD

**Grade 3**: All core requirements implemented, basic documentation, 60%+ test coverage, working deployment

**Fail**: Core requirements not met OR any team member fails oral examination

---

## Common Failure Patterns

### Automatic Failure Conditions:
- Cannot explain their own code during oral examination
- Major security vulnerabilities (SQL injection, exposed credentials)
- Non-functional deployment on Kubernetes
- Plagiarism or academic dishonesty
- Less than 60% test coverage on backend code

### Warning Signs:
- Over-reliance on AI without understanding
- Hardcoded secrets or credentials in code
- No error handling or input validation
- Cannot draw system architecture from memory
- Tests only cover happy path scenarios

---

## Grade Appeal Process

Students may request grade review by:
1. Demonstrating missing functionality that wasn't observed
2. Providing additional documentation that wasn't considered
3. Explaining technical decisions that were misunderstood

Appeals must be submitted within one week of grade notification with specific technical justification.