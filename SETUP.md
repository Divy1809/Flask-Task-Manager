# Quick Setup Instructions

## 🚀 Running the Application Locally (Development)

The Flask application is already configured and running on Replit!

**Access the application:**
- Click the "Webview" button in Replit
- Or visit: http://localhost:5000

**Features available:**
1. Register a new user account
2. Login with your credentials
3. Create, view, update, and delete tasks
4. Manage task priorities and status

---

## 🐳 Running with Podman/Docker (Containerized)

### Option 1: Using Management Scripts (Recommended)

```bash
# Build the container image
./scripts/build.sh

# Run the container
./scripts/run.sh

# Access at http://localhost:5000

# View logs
./scripts/manage.sh logs

# Stop the container
./scripts/manage.sh stop
```

### Option 2: Using Docker Compose

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Option 3: Manual Podman/Docker Commands

```bash
# Build the image
podman build -f Containerfile -t taskmanager:latest .

# Run the container
podman run -d \
  --name flask-taskmanager \
  -p 5000:5000 \
  -v taskmanager-data:/data \
  -e SESSION_SECRET="your-secret-key" \
  taskmanager:latest

# Access at http://localhost:5000
```

---

## 📦 Container Management

### Available Scripts

All scripts are in the `scripts/` directory:

- **build.sh** - Build container image with versioning
- **run.sh** - Run container with proper configuration
- **push.sh** - Push image to Docker Hub
- **manage.sh** - Complete lifecycle management

### Management Commands

```bash
# View all available commands
./scripts/manage.sh

# Common operations
./scripts/manage.sh start      # Start container
./scripts/manage.sh stop       # Stop container
./scripts/manage.sh restart    # Restart container
./scripts/manage.sh logs       # View logs
./scripts/manage.sh health     # Check health
./scripts/manage.sh backup     # Backup database
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest test_app.py -v

# Run with coverage
pytest test_app.py --cov=app

# Current test results: 15/16 passing (93.75%)
```

---

## 🌐 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user

### Tasks
- `GET /api/tasks` - Get all tasks (requires auth)
- `POST /api/tasks` - Create task (requires auth)
- `GET /api/tasks/<id>` - Get specific task (requires auth)
- `PUT /api/tasks/<id>` - Update task (requires auth)
- `DELETE /api/tasks/<id>` - Delete task (requires auth)

### Health
- `GET /health` - Health check endpoint

---

## 📚 Documentation

For complete documentation, see **README.md** which includes:
- Architecture overview
- Detailed installation instructions
- API documentation with examples
- Container operations guide
- Deployment instructions
- Troubleshooting guide

---

## 🎓 Capstone Project Features

This project demonstrates:
- ✅ Flask web application with authentication
- ✅ RESTful API design
- ✅ SQLite database with ORM
- ✅ Multi-stage container builds
- ✅ Security best practices (non-root user, password hashing)
- ✅ Container lifecycle management
- ✅ CI/CD with GitHub Actions
- ✅ Comprehensive testing
- ✅ Production-ready deployment

---

## 🔧 Environment Variables

**For Local Development:**
- `SESSION_SECRET` - Session encryption key
- `FLASK_ENV` - Environment (development/production)

**For Container Deployment:**
- `SESSION_SECRET` - Session encryption key (required)
- `SQLALCHEMY_DATABASE_URI` - Database path (default: sqlite:////data/tasks.db)
- `PORT` - Application port (default: 5000)

---

## ⚠️ Important Notes

1. **Security**: Change SESSION_SECRET in production
2. **Data Persistence**: Container uses volume mounting for database persistence
3. **Production**: Use Gunicorn (included in container) instead of Flask dev server
4. **Registry**: Update Docker Hub username in scripts before pushing

---

For questions or issues, refer to README.md or open an issue on GitHub.
