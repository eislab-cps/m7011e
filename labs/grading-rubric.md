# Grading Rubric: Dynamic Web System Project

## Overview

**CRITICAL**: This project evaluates **individual technical knowledge and understanding**, not feature quantity or team output. Each student receives **individual oral examination** to demonstrate their personal mastery of concepts.

**Evaluation Focus**: 
- Deep understanding of implemented technologies
- Ability to explain architectural decisions and alternatives
- Security knowledge and threat awareness
- System design principles and trade-offs
- **NOT**: Feature count, visual design, or team productivity

## Grading Scale

| Grade | Description | Requirements Met |
|-------|-------------|------------------|
| **5** | Excellent | All core requirements + 2 advanced features + exceptional quality |
| **4** | Good | All core requirements + 1 advanced feature + solid implementation |
| **3** | Satisfactory | All core requirements + basic implementation |
| **F** | Fail | Core requirements not met |

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

### Individual Oral Examination (25 points - MOST IMPORTANT)

**Each student examined separately for 20-30 minutes**

| Criteria | Grade 5 (23-25 pts) | Grade 4 (18-22 pts) | Grade 3 (13-17 pts) | Fail (0-12 pts) |
|----------|---------------------|---------------------|---------------------|-----------------|
| **Code Ownership** | Can explain every line of their code, design rationale, and alternative approaches | Can explain most of their code and justify key decisions | Can explain basic functionality they implemented | Cannot explain their own code or design decisions |
| **System Architecture** | Can draw complete system from memory, explain all interactions, discuss scaling strategies | Can explain system components and data flow, basic scaling considerations | Can explain their component's role in overall system | Cannot explain system design or their component's place |
| **Technology Mastery** | Deep understanding of chosen technologies, can compare with alternatives, explain limitations | Good grasp of technologies used, can explain basic trade-offs | Basic understanding of technologies sufficient for implementation | Superficial or incorrect understanding of technologies |
| **Problem Solving** | Can propose multiple solutions to hypothetical problems, explain trade-offs, discuss emerging trends | Can suggest improvements and handle basic system modification questions | Can identify obvious issues and suggest simple fixes | Cannot think critically about the system or propose solutions |

---

## Final Grade Calculation

### Grade 5 (Excellent): 85-100 points
- All core requirements (75 points)
- Two advanced features (20 points)
- Excellent documentation and oral defense (25 points)

### Grade 4 (Good): 70-84 points  
- All core requirements (75 points)
- One advanced feature (10 points)
- Good documentation and oral defense (20 points)

### Grade 3 (Satisfactory): 55-69 points
- All core requirements (75 points)
- Acceptable documentation and oral defense (15 points)

### Fail: <55 points
- Core requirements not adequately met

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