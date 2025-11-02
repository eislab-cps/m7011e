# Tutorial 2: Docker and Docker Compose

This tutorial introduces Docker, a platform for developing, shipping, and running applications in containers. You'll learn how to containerize the todo application from Tutorial 1, create Docker images, and use Docker Compose to orchestrate multiple containers.

## Learning Objectives

By completing this tutorial, you will understand:
- What containers are and why they're useful
- How Docker works and its core concepts
- How to write Dockerfiles
- How to build and run Docker images
- How to use Docker Compose for multi-container applications
- Networking between containers
- Volume management for persistent data
- Best practices for containerizing applications

---

## What is Docker?

**Docker** is a platform for developing, shipping, and running applications inside containers.

### Containers vs Virtual Machines

```mermaid
flowchart TB
    subgraph VM["Virtual Machines Architecture"]
        Host1["Host Operating System"]
        Hypervisor["Hypervisor"]
        VM1["VM 1<br/>Guest OS + App"]
        VM2["VM 2<br/>Guest OS + App"]
        VM3["VM 3<br/>Guest OS + App"]

        Host1 --> Hypervisor
        Hypervisor --> VM1
        Hypervisor --> VM2
        Hypervisor --> VM3
    end

    subgraph Container["Containers Architecture"]
        Host2["Host Operating System"]
        Docker["Docker Engine"]
        C1["Container 1<br/>App + Libs"]
        C2["Container 2<br/>App + Libs"]
        C3["Container 3<br/>App + Libs"]

        Host2 --> Docker
        Docker --> C1
        Docker --> C2
        Docker --> C3
    end

    style VM fill:#ffe6e6,stroke:#cc0000
    style Container fill:#e6ffe6,stroke:#00cc00
```

**Key Differences:**

| Aspect | Virtual Machines | Containers |
|--------|-----------------|------------|
| **Isolation** | Hardware-level | Process-level |
| **Startup Time** | Minutes | Seconds |
| **Size** | GBs | MBs |
| **Resource Usage** | Heavy | Lightweight |
| **OS** | Each VM has full OS | Share host OS kernel |
| **Portability** | Less portable | Highly portable |

### Why Use Docker?

1. **Consistency**: "Works on my machine" → Works everywhere
2. **Isolation**: Applications run in isolated environments
3. **Portability**: Run anywhere Docker is installed
4. **Efficiency**: Lightweight compared to VMs
5. **Scalability**: Easy to scale up/down
6. **Version Control**: Images are versioned and reproducible
7. **Microservices**: Perfect for microservice architectures

### Docker Concepts

#### 1. Image
A **Docker image** is a read-only template containing:
- Application code
- Runtime environment
- Libraries and dependencies
- Configuration files

Think of it as a "snapshot" or "class" in programming.

#### 2. Container
A **container** is a running instance of an image.

Think of it as an "object" created from the image "class".

**Analogy:**
- Image = Recipe
- Container = Cake baked from recipe

#### 3. Dockerfile
A **Dockerfile** is a text file with instructions to build an image.

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

#### 4. Docker Registry
A **registry** stores Docker images (like GitHub for code).

- **Docker Hub**: Public registry (hub.docker.com)
- **Private registries**: For internal company use
- **GitHub Container Registry**: ghcr.io
- **Amazon ECR, Google GCR, Azure ACR**: Cloud provider registries

#### 5. Docker Compose
**Docker Compose** is a tool for defining and running multi-container applications using a YAML file.

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
  frontend:
    build: ./frontend
    ports:
      - "8080:8080"
```

---

## Docker Architecture

```mermaid
flowchart TB
    Client["Docker Client<br/>(docker CLI)"]
    Daemon["Docker Daemon<br/>(dockerd)"]
    Registry["Docker Registry<br/>(Docker Hub)"]

    subgraph "Docker Host"
        Daemon
        Images["Images"]
        Containers["Containers"]
    end

    Client -->|"docker commands"| Daemon
    Daemon -->|"pull/push"| Registry
    Daemon -->|"creates"| Containers
    Images -->|"run"| Containers

    style Client fill:#e1f5ff,stroke:#01579b
    style Daemon fill:#fff9c4,stroke:#f57f17
    style Registry fill:#f3e5f5,stroke:#4a148c
```

**Components:**

1. **Docker Client**: Command-line tool (`docker` command)
2. **Docker Daemon**: Background service that manages containers
3. **Docker Registry**: Stores and distributes images
4. **Images**: Templates for containers
5. **Containers**: Running instances

**Workflow:**
```
1. Write Dockerfile
2. Build image: docker build -t myapp .
3. Run container: docker run myapp
4. Push to registry: docker push myapp
5. Pull on another machine: docker pull myapp
6. Run anywhere!
```

---

## Prerequisites

- Completed Tutorial 1 (Basic Web Application)
- Docker Desktop installed:
  - **macOS**: https://docs.docker.com/desktop/install/mac-install/
  - **Windows**: https://docs.docker.com/desktop/install/windows-install/
  - **Linux**: https://docs.docker.com/engine/install/

### Verify Installation

```bash
# Check Docker version
docker --version
# Should show: Docker version 24.x.x or higher

# Check Docker Compose version
docker compose version
# Should show: Docker Compose version v2.x.x or higher

# Test Docker installation
docker run hello-world
# Should download and run a test container
```

---

## Project Structure

We'll containerize the todo app from Tutorial 1:

```
2-docker/
├── README.md              # This file
├── backend/
│   ├── app.py            # Flask API (from Tutorial 1)
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Backend container definition
├── frontend/
│   ├── index.html        # Frontend (from Tutorial 1)
│   └── Dockerfile        # Frontend container definition
└── docker-compose.yml    # Multi-container orchestration
```

---

## Part 1: Containerize the Backend

Let's create a Docker image for the Flask backend.

### Step 1: Review Backend Files

First, let's copy the backend from Tutorial 1:

```bash
# From the 2-docker directory
cp -r ../01-basic-webapp/backend .
```

### Step 2: Create Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]
```

**Dockerfile Explained:**

- `FROM`: Base image (Python 3.11 slim version)
- `WORKDIR`: Sets working directory inside container
- `COPY`: Copies files from host to container
- `RUN`: Executes commands during build (install dependencies)
- `EXPOSE`: Documents which port the app uses
- `ENV`: Sets environment variables
- `CMD`: Default command to run when container starts

### Step 3: Build Backend Image

```bash
cd backend

# Build the image
docker build -t todo-backend .

# Explanation:
# -t todo-backend  : Tag (name) the image "todo-backend"
# .                : Build context (current directory)
```

You'll see output like:
```
[+] Building 5.2s (10/10) FINISHED
 => [1/5] FROM python:3.11-slim
 => [2/5] WORKDIR /app
 => [3/5] COPY requirements.txt .
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY . .
 => exporting to image
 => => naming to docker.io/library/todo-backend
```

### Step 4: Run Backend Container

```bash
# Run the container (runs in foreground, you'll see logs)
docker run -p 8000:8000 todo-backend

# Explanation:
# -p 8000:8000     : Map port 8000 on host to port 8000 in container
# todo-backend     : Use the "todo-backend" image
```

**What you'll see:**
- The container starts and shows Flask logs
- You'll see "Starting Flask server..." and requests as they happen
- Press `Ctrl+C` to stop the container

**Important - Docker Networking:**
The Flask app binds to `0.0.0.0:8000` (not `127.0.0.1`). Here's why:
- `127.0.0.1` only accepts connections from inside the container
- `0.0.0.0` accepts connections from anywhere (required for Docker)
- The `-p 8000:8000` flag maps your host's port 8000 to the container's port 8000
- You access it via `localhost:8000` on your host machine

**To run in background (optional):**
```bash
# Run in detached mode (background)
docker run -d -p 8000:8000 todo-backend

# View logs from background container
docker logs <container-id>

# Get container ID
docker ps
```

### Step 5: Test Backend

Open a **new terminal window** (keep the container running in the first terminal):

```bash
# Test the API
curl http://localhost:8000/api/todos

# Or open in browser
open http://localhost:8000/api/todos

# Check running containers
docker ps
```

### Step 6: Useful Docker Commands

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a running container (use container ID from docker ps)
docker stop <container-id>

# Remove a stopped container
docker rm <container-id>

# Stop and remove in one command
docker rm -f <container-id>

# List images
docker images

# Remove image
docker rmi todo-backend

# Execute command in running container
docker exec -it <container-id> bash

# View container details
docker inspect <container-id>
```

---

## Part 2: Containerize the Frontend

The frontend is static HTML/CSS/JS, so we'll use Python's built-in HTTP server to serve it.

### Step 1: Copy Frontend Files

```bash
# From the 2-docker directory
cp -r ../01-basic-webapp/frontend .
```

### Step 2: Create Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy frontend files
COPY index.html .

# Expose port 8080
EXPOSE 8080

# Start Python HTTP server
CMD ["python3", "-m", "http.server", "8080"]
```

**Dockerfile Explained:**

- `FROM python:3.11-slim`: Use Python base image (same as backend for consistency)
- `WORKDIR /app`: Set working directory inside container
- `COPY index.html .`: Copy our HTML file to container
- `EXPOSE 8080`: Document that the app uses port 8080
- `CMD`: Run Python's built-in HTTP server on port 8080

**Why Python HTTP server?**
- Simple and minimal - no extra dependencies
- Perfect for serving static files in development
- Uses the same base image as backend (consistency)
- No need to learn Nginx configuration

**Note**: For production, you might use Nginx or a CDN, but Python's HTTP server is perfect for learning and development!

### Step 3: Build and Run Frontend

```bash
cd frontend

# Build the image
docker build -t todo-frontend .

# Run the container (in foreground)
docker run -p 8080:8080 todo-frontend

# You'll see output like:
# Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

Open a **new terminal** and test:

```bash
# Test in browser
open http://localhost:8080

# Or use curl
curl http://localhost:8080
```

**Note**: The frontend and backend are in separate containers now, but they can't communicate yet. We'll fix this with Docker Compose!

**To stop:** Press `Ctrl+C` in the terminal running the container.

---

## Part 3: Docker Compose - Orchestrate Multiple Containers

Docker Compose allows you to define and run multi-container applications.

### Step 1: Create docker-compose.yml

Create `docker-compose.yml` in the `2-docker` directory:

```yaml
version: '3.8'

services:
  # Backend service
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: todo-backend
    ports:
      - "8000:8000"
    environment:
      - FLASK_APP=app.py
      - PYTHONUNBUFFERED=1
    networks:
      - todo-network
    restart: unless-stopped

  # Frontend service
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: todo-frontend
    ports:
      - "8080:80"
    depends_on:
      - backend
    networks:
      - todo-network
    restart: unless-stopped

# Define custom network
networks:
  todo-network:
    driver: bridge
```

**docker-compose.yml Explained:**

- `version`: Compose file format version
- `services`: Define containers
- `build`: Build image from Dockerfile
- `ports`: Map host port to container port
- `environment`: Set environment variables
- `depends_on`: Start order (frontend waits for backend)
- `networks`: Connect containers on same network
- `restart`: Restart policy

### Step 2: Run with Docker Compose

```bash
# From 2-docker directory
# Start all services
docker compose up

# Or run in background
docker compose up -d

# View logs
docker compose logs

# Follow logs
docker compose logs -f

# View specific service logs
docker compose logs backend
docker compose logs frontend
```

### Step 3: Test the Application

Open http://localhost:8080 in your browser. The frontend should now be able to communicate with the backend!

### Step 4: Docker Compose Commands

```bash
# Start services
docker compose up -d

# Stop services (keeps containers)
docker compose stop

# Start stopped services
docker compose start

# Stop and remove containers
docker compose down

# Stop, remove containers, and remove volumes
docker compose down -v

# Rebuild images
docker compose build

# Rebuild and start
docker compose up --build

# View running services
docker compose ps

# Execute command in service
docker compose exec backend bash

# View logs
docker compose logs -f

# Scale services (run multiple instances)
docker compose up -d --scale backend=3
```

---

## Part 4: Container Networking

### How Containers Communicate

When using Docker Compose, containers can communicate using service names:

```javascript
// Frontend can reach backend using service name
fetch('http://backend:8000/api/todos')
```

**Docker creates DNS resolution:**
- Service name `backend` → IP address of backend container
- Service name `frontend` → IP address of frontend container

### Network Types

1. **Bridge Network** (default)
   - Containers on same bridge can communicate
   - Isolated from other networks
   - Used in our docker-compose.yml

2. **Host Network**
   - Container shares host's network
   - No isolation
   - Better performance

3. **None Network**
   - No networking
   - Complete isolation

### Network Commands

```bash
# List networks
docker network ls

# Inspect network
docker network inspect todo-network

# Create network
docker network create my-network

# Connect container to network
docker network connect my-network backend

# Disconnect container from network
docker network disconnect my-network backend
```

---

## Part 5: Understanding Data Persistence

### The Problem

**Important**: When a container stops or is removed, all data inside it is lost!

In our todo app:
- Todos are stored in memory (in the Python list)
- When you restart the backend container, all todos disappear
- This is fine for development, but not for production

### The Solution: Volumes

Docker **volumes** are the solution for persisting data across container restarts.

```mermaid
flowchart LR
    Container["Container<br/>(can be deleted)"]
    Volume["Docker Volume<br/>(persistent storage)"]
    HostFS["Host Filesystem<br/>/var/lib/docker/volumes/"]

    Container <-->|"reads/writes"| Volume
    Volume <-->|"stored on"| HostFS

    style Container fill:#ffe6e6,stroke:#cc0000
    style Volume fill:#e6f3ff,stroke:#0066cc
    style HostFS fill:#fff3e6,stroke:#cc8800
```

### Types of Data Storage

1. **Volumes** (recommended for production)
   - Managed by Docker
   - Persist even if container is deleted
   - Can be shared between containers
   - Example: Database data, uploaded files

2. **Bind Mounts** (good for development)
   - Mount a host directory into container
   - Direct access to host filesystem
   - Example: Mounting source code for live reloading

3. **tmpfs Mounts** (temporary data)
   - Stored in memory only
   - Deleted when container stops
   - Fast, but not persistent
   - Example: Temporary cache

### Adding Persistence (Next Steps)

To make our todo app production-ready, you would:

1. **Add a database** (PostgreSQL, MySQL, MongoDB)
2. **Use a named volume** to persist database data
3. **Update backend code** to use database instead of in-memory list
4. **See Tutorial 6** for PostgreSQL deployment on Kubernetes

**Example docker-compose.yml with database** (for reference):
```yaml
services:
  backend:
    # ... existing config ...
    environment:
      - DATABASE_URL=postgresql://user:pass@database:5432/todos

  database:
    image: postgres:16-alpine
    volumes:
      - postgres-data:/var/lib/postgresql/data  # Persistent volume

volumes:
  postgres-data:  # Named volume definition
```

### Useful Volume Commands

```bash
# List all volumes
docker volume ls

# Create a volume
docker volume create my-volume

# Inspect volume details
docker volume inspect my-volume

# Remove unused volumes
docker volume prune

# Remove specific volume
docker volume rm my-volume
```

---

## Part 6: Docker Best Practices

### 1. Use Official Base Images

```dockerfile
# Good - official image
FROM python:3.11-slim

# Avoid - unknown source
FROM random-user/python
```

### 2. Use Specific Tags (not `latest`)

```dockerfile
# Good - specific version
FROM python:3.11-slim

# Bad - unpredictable
FROM python:latest
```

### 3. Minimize Layers

```dockerfile
# Good - single RUN layer
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Bad - multiple layers
RUN apt-get update
RUN apt-get install -y package1
RUN apt-get install -y package2
```

### 4. Use .dockerignore

Create `.dockerignore` to exclude files:

```
# .dockerignore
__pycache__
*.pyc
.git
.env
node_modules
.vscode
*.md
```

### 5. Don't Run as Root

```dockerfile
# Create non-root user
RUN addgroup --system --gid 1001 appuser && \
    adduser --system --uid 1001 --gid 1001 appuser

# Switch to non-root user
USER appuser
```

### 6. Multi-Stage Builds

Reduce image size by using multiple stages:

```dockerfile
# Stage 1: Build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Production
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

### 7. Use Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

Or in docker-compose.yml:

```yaml
services:
  backend:
    # ...
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 5s
```

### 8. Optimize Layer Caching

```dockerfile
# Good - dependencies cached separately
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Bad - rebuilds deps every code change
COPY . .
RUN pip install -r requirements.txt
```

---

## Part 7: Debugging Docker Applications

### Common Issues and Solutions

#### 1. Container Exits Immediately

```bash
# First, get the container ID
docker ps -a

# Check logs (replace <container-id> with actual ID)
docker logs <container-id>

# Check exit code
docker inspect <container-id> --format='{{.State.ExitCode}}'

# Run interactively to debug
docker run -it todo-backend sh
```

**With Docker Compose:**
```bash
# View logs for specific service
docker compose logs backend

# Follow logs in real-time
docker compose logs -f backend
```

#### 2. Cannot Connect to Other Container

```bash
# Check if both containers are on same network (with Docker Compose)
docker compose ps

# Check network
docker network inspect todo-network

# Verify DNS resolution (backend to frontend)
docker compose exec backend ping frontend

# Check ports
docker compose exec backend netstat -tlnp
```

#### 3. Port Already in Use

```bash
# Find what's using the port
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port in docker-compose.yml
ports:
  - "8001:8000"
```

#### 4. Out of Disk Space

```bash
# Clean up stopped containers
docker container prune

# Clean up unused images
docker image prune

# Clean up unused volumes
docker volume prune

# Clean up everything
docker system prune -a --volumes
```

### Debugging Commands

**For individual containers:**
```bash
# Get container ID first
docker ps

# Execute shell in running container
docker exec -it <container-id> bash

# Copy files from container
docker cp <container-id>:/app/app.py ./app.py

# Copy files to container
docker cp ./app.py <container-id>:/app/app.py

# View resource usage
docker stats

# View processes in container
docker top <container-id>

# View file changes in container
docker diff <container-id>
```

**With Docker Compose:**
```bash
# Execute command in service
docker compose exec backend bash

# View logs
docker compose logs backend

# Restart specific service
docker compose restart backend

# View resource usage
docker compose ps
```

---

## Part 8: Pushing Images to Registry

### Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag your image
docker tag todo-backend username/todo-backend:v1.0

# Push to Docker Hub
docker push username/todo-backend:v1.0

# Pull on another machine
docker pull username/todo-backend:v1.0
```

### GitHub Container Registry

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag image
docker tag todo-backend ghcr.io/username/todo-backend:v1.0

# Push image
docker push ghcr.io/username/todo-backend:v1.0
```

---

## Exercise: Containerize Your Application

### Goal

Containerize an existing application or create a new multi-service application.

### Requirements

1. **Create Dockerfiles** for each service
2. **Use Docker Compose** to orchestrate services
3. **Add a database** with persistent volume
4. **Implement health checks**
5. **Use environment variables** for configuration
6. **Add .dockerignore** files
7. **Document** how to build and run

### Bonus Challenges

- Use multi-stage builds to optimize image size
- Implement health checks for containers
- Add environment files (.env) for configuration
- Use Docker secrets for sensitive data
- Create development and production compose files
- Implement automated builds with GitHub Actions

---

## Summary

You've learned:

- What Docker is and how containers differ from VMs
- Core Docker concepts: images, containers, Dockerfile, registry
- How to write Dockerfiles and build images
- How to run and manage containers
- How to use Docker Compose for multi-container apps
- Container networking and how services communicate
- Data persistence with volumes
- Docker best practices and optimization
- Debugging containerized applications
- Pushing images to registries

**Key Takeaway**: Docker enables consistent, portable, and efficient application deployment by packaging applications with all their dependencies into lightweight containers.

---

## What's Next?

Tutorial 3 will cover **Databases**, where you'll learn about different types of databases and when to use each one!

Tutorial 4 will introduce **Kubernetes**, where you'll learn to orchestrate Docker containers at scale across multiple machines!

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Play with Docker](https://labs.play-with-docker.com/) - Free online Docker playground
- [Docker Cheat Sheet](https://docs.docker.com/get-started/docker_cheatsheet.pdf)
