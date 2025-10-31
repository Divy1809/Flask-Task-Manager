# Flask Task Manager - Containerized Application

A comprehensive, production-ready task management web application built with Flask and containerized using Podman/Docker. This capstone project demonstrates mastery of Linux container technologies, RESTful API design, and modern DevOps practices.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Container Operations](#container-operations)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality
- **User Authentication**: Secure registration and login system with password hashing
- **Task Management**: Complete CRUD operations (Create, Read, Update, Delete)
- **RESTful API**: Well-structured API endpoints with proper HTTP methods
- **Responsive UI**: Bootstrap-based interface that works on all devices
- **Session Management**: Secure cookie-based session handling
- **Data Persistence**: SQLite database with volume mounting for data retention

### Container Features
- **Multi-stage Build**: Optimized container image size
- **Security**: Non-root user execution, minimal base image
- **Health Checks**: Built-in container health monitoring
- **Production Ready**: Gunicorn WSGI server with multiple workers
- **CI/CD Integration**: Automated testing and deployment pipeline
- **Volume Management**: Persistent data storage

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client Browser                        │
└───────────────────┬─────────────────────────────────────┘
                    │ HTTP/HTTPS
┌───────────────────▼─────────────────────────────────────┐
│              Nginx/Load Balancer (Optional)              │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│           Flask Application Container                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Gunicorn WSGI Server (4 workers)              │   │
│  └──────────────────┬──────────────────────────────┘   │
│                     │                                    │
│  ┌──────────────────▼──────────────────────────────┐   │
│  │  Flask Application                              │   │
│  │  ├── Routes (API Endpoints)                     │   │
│  │  ├── Models (ORM)                               │   │
│  │  ├── Templates (Jinja2)                         │   │
│  │  └── Static Files (CSS/JS)                      │   │
│  └──────────────────┬──────────────────────────────┘   │
│                     │                                    │
│  ┌──────────────────▼──────────────────────────────┐   │
│  │  SQLite Database (/data/tasks.db)              │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                    │
         ┌──────────▼──────────┐
         │  Volume Mount       │
         │  (taskmanager-data) │
         └─────────────────────┘
```

## 📦 Prerequisites

### Required Software
- **Container Runtime**: Podman (recommended) or Docker
  - Podman: `sudo apt install podman` (Debian/Ubuntu)
  - Docker: `sudo apt install docker.io`
- **Python 3.9+**: For local development
- **Git**: For version control

### Optional Tools
- **Docker Compose / Podman Compose**: For multi-container setups
- **curl**: For API testing
- **jq**: For JSON formatting

## 🚀 Quick Start

### Using Pre-built Container Scripts

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/flask-taskmanager.git
   cd flask-taskmanager
   ```

2. **Build the container image**
   ```bash
   ./scripts/build.sh
   ```

3. **Run the container**
   ```bash
   ./scripts/run.sh
   ```

4. **Access the application**
   - Open your browser: http://localhost:5000
   - Register a new account
   - Start managing tasks!

### Using Docker Compose

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

## 📥 Installation

### Local Development Setup

1. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   export FLASK_APP=app.main:app
   export FLASK_ENV=development
   ```

4. **Run the application**
   ```bash
   python -m app.main
   ```

5. **Access at** http://localhost:5000

### Container Build from Source

```bash
# Using Podman
podman build -f Containerfile -t taskmanager:latest .

# Using Docker
docker build -f Containerfile -t taskmanager:latest .
```

## 🐳 Container Operations

### Using Management Scripts

The project includes comprehensive management scripts in the `scripts/` directory:

#### Build Image
```bash
./scripts/build.sh [version]
# Example: ./scripts/build.sh v1.0.0
```

#### Run Container
```bash
./scripts/run.sh
```

#### Push to Registry
```bash
export DOCKER_USERNAME=yourusername
./scripts/push.sh [version]
```

#### Container Management
```bash
# Start container
./scripts/manage.sh start

# Stop container
./scripts/manage.sh stop

# View logs
./scripts/manage.sh logs

# Check health
./scripts/manage.sh health

# Backup database
./scripts/manage.sh backup

# View all options
./scripts/manage.sh
```

### Manual Container Operations

#### Podman Commands
```bash
# Run container
podman run -d \
  --name flask-taskmanager \
  -p 5000:5000 \
  -v taskmanager-data:/data \
  -e SESSION_SECRET="your-secret" \
  taskmanager:latest

# View logs
podman logs -f flask-taskmanager

# Execute shell
podman exec -it flask-taskmanager /bin/bash

# Stop container
podman stop flask-taskmanager

# Remove container
podman rm flask-taskmanager
```

#### Docker Commands
Replace `podman` with `docker` in the above commands.

## 📚 API Documentation

### Base URL
```
http://localhost:5000
```

### Authentication Endpoints

#### Register New User
```http
POST /api/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123"
}

Response (201 Created):
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2024-01-01T12:00:00"
  }
}
```

#### Login
```http
POST /api/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepass123"
}

Response (200 OK):
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

### Task Endpoints

#### Create Task
```http
POST /api/tasks
Content-Type: application/json
Authentication: Required (session)

{
  "title": "Complete project documentation",
  "description": "Write comprehensive README",
  "status": "pending",
  "priority": "high"
}

Response (201 Created):
{
  "message": "Task created successfully",
  "task": {
    "id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive README",
    "status": "pending",
    "priority": "high",
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00"
  }
}
```

#### Get All Tasks
```http
GET /api/tasks
Authentication: Required (session)

Response (200 OK):
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "description": "Write comprehensive README",
      "status": "pending",
      "priority": "high",
      "created_at": "2024-01-01T12:00:00"
    }
  ]
}
```

#### Update Task
```http
PUT /api/tasks/{task_id}
Content-Type: application/json
Authentication: Required (session)

{
  "title": "Updated title",
  "status": "completed",
  "priority": "medium"
}

Response (200 OK):
{
  "message": "Task updated successfully",
  "task": { ... }
}
```

#### Delete Task
```http
DELETE /api/tasks/{task_id}
Authentication: Required (session)

Response (200 OK):
{
  "message": "Task deleted successfully"
}
```

### Health Check
```http
GET /health

Response (200 OK):
{
  "status": "healthy",
  "database": "connected",
  "message": "Application is running normally"
}
```

## 💻 Development

### Project Structure
```
flask-taskmanager/
├── app/
│   ├── __init__.py          # Application factory
│   ├── main.py              # Entry point
│   ├── models.py            # Database models
│   ├── routes.py            # API routes
│   └── templates/           # HTML templates
│       ├── index.html
│       ├── add_task.html
│       └── view_tasks.html
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles
│   └── js/
│       └── app.js           # Frontend JavaScript
├── scripts/
│   ├── build.sh             # Build container
│   ├── run.sh               # Run container
│   ├── push.sh              # Push to registry
│   └── manage.sh            # Container management
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions pipeline
├── Containerfile            # Container definition
├── docker-compose.yml       # Multi-container setup
├── requirements.txt         # Python dependencies
├── start.sh                 # Container startup script
├── test_app.py              # Unit tests
└── README.md                # This file
```

### Running Tests

```bash
# Run all tests
pytest test_app.py -v

# Run with coverage
pytest test_app.py --cov=app --cov-report=html

# Run specific test class
pytest test_app.py::TestTaskOperations -v
```

### Code Quality

```bash
# Linting with flake8
flake8 app/ --max-line-length=127

# Format with black
black app/

# Type checking with mypy
mypy app/
```

## 🚢 Deployment

### Container Registry

#### Push to Docker Hub
```bash
# Login
podman login docker.io

# Tag image
podman tag taskmanager:latest docker.io/yourusername/taskmanager:v1.0

# Push
podman push docker.io/yourusername/taskmanager:v1.0
```

#### Pull and Run
```bash
podman pull docker.io/yourusername/taskmanager:v1.0
podman run -d -p 5000:5000 docker.io/yourusername/taskmanager:v1.0
```

### Production Deployment

#### Environment Variables
```bash
export SESSION_SECRET="strong-random-secret-key"
export FLASK_ENV=production
export DATABASE_URL="postgresql://..." # Optional: PostgreSQL
```

#### With Reverse Proxy (Nginx)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### GitHub Actions CI/CD

The project includes automated CI/CD pipeline that:
1. Runs unit tests on every push
2. Builds container image
3. Pushes to Docker Hub on main branch
4. Performs security scans
5. Deploys on release tags

**Setup Required Secrets:**
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password/token

## 🔧 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill the process or change port
podman run -p 8080:5000 taskmanager:latest
```

#### Permission Denied
```bash
# Add user to docker/podman group
sudo usermod -aG docker $USER
# OR
sudo usermod -aG podman $USER

# Logout and login again
```

#### Database Locked
```bash
# Stop all containers
podman stop flask-taskmanager

# Remove database lock
podman volume inspect taskmanager-data
# Manually remove .db-journal file if needed
```

#### Container Won't Start
```bash
# Check logs
podman logs flask-taskmanager

# Check health
podman inspect --format='{{.State.Health.Status}}' flask-taskmanager

# Rebuild image
./scripts/build.sh
```

### Health Check

```bash
# Via API
curl http://localhost:5000/health

# Via container inspect
podman inspect --format='{{json .State.Health}}' flask-taskmanager | jq
```

### Database Backup and Restore

```bash
# Backup
./scripts/manage.sh backup

# Restore
./scripts/manage.sh restore ./backups/taskmanager_backup_20240101_120000.db
```

## 📖 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Podman Documentation](https://docs.podman.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bootstrap Documentation](https://getbootstrap.com/)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Flask framework and community
- Podman/Docker container technology
- Bootstrap for responsive design
- All open-source contributors

---

**Project Status**: ✅ Production Ready

**Last Updated**: October 2025

For questions or support, please open an issue on GitHub.
