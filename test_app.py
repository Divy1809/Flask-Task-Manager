"""
Unit Tests for Flask Task Manager Application
Comprehensive test suite covering all API endpoints and functionality.
"""

import pytest
import json
from app import create_app, db
from app.models import User, Task

@pytest.fixture
def app():
    """
    Create and configure a test Flask application.
    
    Returns:
        Flask: Test application instance
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """
    Create a test client for the application.
    
    Args:
        app: Test application fixture
        
    Returns:
        FlaskClient: Test client
    """
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """
    Create an authenticated test client.
    
    Args:
        client: Test client fixture
        
    Returns:
        tuple: (client, user_data)
    """
    # Register a test user
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    client.post('/api/register', 
                data=json.dumps(user_data),
                content_type='application/json')
    
    # Login the user
    client.post('/api/login',
                data=json.dumps({
                    'username': user_data['username'],
                    'password': user_data['password']
                }),
                content_type='application/json')
    
    return client, user_data

class TestHealthEndpoint:
    """Test suite for health check endpoint."""
    
    def test_health_check(self, client):
        """Test health endpoint returns success."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'database' in data

class TestUserRegistration:
    """Test suite for user registration."""
    
    def test_successful_registration(self, client):
        """Test user can register successfully."""
        user_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123'
        }
        response = client.post('/api/register',
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'User registered successfully'
        assert 'user' in data
    
    def test_duplicate_username(self, client):
        """Test registration fails with duplicate username."""
        user_data = {
            'username': 'duplicate',
            'email': 'first@example.com',
            'password': 'password123'
        }
        client.post('/api/register',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        # Try to register with same username
        user_data['email'] = 'second@example.com'
        response = client.post('/api/register',
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'already exists' in data['error']
    
    def test_invalid_registration_data(self, client):
        """Test registration fails with invalid data."""
        # Missing fields
        response = client.post('/api/register',
                              data=json.dumps({'username': 'test'}),
                              content_type='application/json')
        assert response.status_code == 400
        
        # Short username
        response = client.post('/api/register',
                              data=json.dumps({
                                  'username': 'ab',
                                  'email': 'test@example.com',
                                  'password': 'password123'
                              }),
                              content_type='application/json')
        assert response.status_code == 400
        
        # Short password
        response = client.post('/api/register',
                              data=json.dumps({
                                  'username': 'testuser',
                                  'email': 'test@example.com',
                                  'password': '12345'
                              }),
                              content_type='application/json')
        assert response.status_code == 400

class TestUserLogin:
    """Test suite for user authentication."""
    
    def test_successful_login(self, client):
        """Test user can login with correct credentials."""
        # Register user first
        user_data = {
            'username': 'logintest',
            'email': 'login@example.com',
            'password': 'password123'
        }
        client.post('/api/register',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        # Login
        response = client.post('/api/login',
                              data=json.dumps({
                                  'username': 'logintest',
                                  'password': 'password123'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Login successful'
    
    def test_invalid_credentials(self, client):
        """Test login fails with wrong password."""
        # Register user
        user_data = {
            'username': 'wrongpass',
            'email': 'wrong@example.com',
            'password': 'correct123'
        }
        client.post('/api/register',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        # Try wrong password
        response = client.post('/api/login',
                              data=json.dumps({
                                  'username': 'wrongpass',
                                  'password': 'wrong123'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid' in data['error']
    
    def test_nonexistent_user(self, client):
        """Test login fails for non-existent user."""
        response = client.post('/api/login',
                              data=json.dumps({
                                  'username': 'nonexistent',
                                  'password': 'password123'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 401

class TestTaskOperations:
    """Test suite for task CRUD operations."""
    
    def test_create_task(self, auth_client):
        """Test creating a new task."""
        client, _ = auth_client
        task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'pending',
            'priority': 'high'
        }
        
        response = client.post('/api/tasks',
                              data=json.dumps(task_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Task created successfully'
        assert data['task']['title'] == 'Test Task'
    
    def test_get_all_tasks(self, auth_client):
        """Test retrieving all tasks for a user."""
        client, _ = auth_client
        
        # Create some tasks
        for i in range(3):
            client.post('/api/tasks',
                       data=json.dumps({
                           'title': f'Task {i}',
                           'description': f'Description {i}'
                       }),
                       content_type='application/json')
        
        # Get all tasks
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['tasks']) == 3
    
    def test_update_task(self, auth_client):
        """Test updating an existing task."""
        client, _ = auth_client
        
        # Create a task
        response = client.post('/api/tasks',
                              data=json.dumps({
                                  'title': 'Original Title',
                                  'description': 'Original Description'
                              }),
                              content_type='application/json')
        task_id = json.loads(response.data)['task']['id']
        
        # Update the task
        response = client.put(f'/api/tasks/{task_id}',
                             data=json.dumps({
                                 'title': 'Updated Title',
                                 'status': 'completed'
                             }),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['task']['title'] == 'Updated Title'
        assert data['task']['status'] == 'completed'
    
    def test_delete_task(self, auth_client):
        """Test deleting a task."""
        client, _ = auth_client
        
        # Create a task
        response = client.post('/api/tasks',
                              data=json.dumps({
                                  'title': 'Task to Delete'
                              }),
                              content_type='application/json')
        task_id = json.loads(response.data)['task']['id']
        
        # Delete the task
        response = client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        
        # Verify it's gone
        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 404
    
    def test_task_requires_authentication(self, client):
        """Test that task operations require authentication."""
        response = client.get('/api/tasks')
        assert response.status_code == 401
    
    def test_cannot_access_other_users_tasks(self, app):
        """Test users cannot access other users' tasks."""
        with app.test_client() as client1, app.test_client() as client2:
            # Create two users
            user1_data = {'username': 'user1', 'email': 'user1@test.com', 'password': 'pass123'}
            user2_data = {'username': 'user2', 'email': 'user2@test.com', 'password': 'pass123'}
            
            client1.post('/api/register', data=json.dumps(user1_data), content_type='application/json')
            client2.post('/api/register', data=json.dumps(user2_data), content_type='application/json')
            
            client1.post('/api/login', data=json.dumps({'username': 'user1', 'password': 'pass123'}), content_type='application/json')
            client2.post('/api/login', data=json.dumps({'username': 'user2', 'password': 'pass123'}), content_type='application/json')
            
            # User1 creates a task
            response = client1.post('/api/tasks', data=json.dumps({'title': 'User1 Task'}), content_type='application/json')
            task_id = json.loads(response.data)['task']['id']
            
            # User2 tries to access it
            response = client2.get(f'/api/tasks/{task_id}')
            assert response.status_code == 403

class TestWebPages:
    """Test suite for web page routes."""
    
    def test_index_page(self, client):
        """Test home page loads."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_dashboard_requires_login(self, client):
        """Test dashboard requires authentication."""
        response = client.get('/dashboard', follow_redirects=False)
        assert response.status_code == 302  # Redirect to login
    
    def test_authenticated_dashboard(self, auth_client):
        """Test authenticated users can access dashboard."""
        client, _ = auth_client
        response = client.get('/dashboard')
        assert response.status_code == 200

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
