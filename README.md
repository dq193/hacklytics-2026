# Health Insurance API

A FastAPI application for managing health insurance users with authentication.

## Features

- User registration and authentication
- Bearer token-based authentication
- SQLite database for user data storage
- Password hashing with bcrypt
- JWT token generation and validation
- Protected endpoints with middleware
- Environment variable configuration for security

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and set your configuration values
```

## Environment Variables

Create a `.env` file in the project root based on `.env.example`:

```bash
# Secret key for JWT token generation
# Generate a new secure key for production use
SECRET_KEY=your-secret-key-here-change-in-production-please-use-a-long-random-string

# Database configuration
DATABASE_URL=health_insurance.db

# JWT Configuration
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**Security Notes:** 
- The `.env` file is automatically excluded from git by `.gitignore`
- Always use a strong, randomly generated SECRET_KEY in production
- Never commit your actual `.env` file to version control
- Configure HOST and PORT appropriately for your deployment environment

## Running the application

```bash
# Using hypercorn directly
hypercorn main:app --reload

# Or run directly (uses environment variables)
python main.py
```

The API will be available at `http://localhost:8000` (or your configured HOST:PORT)

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Public Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /register` - Register a new user
- `POST /login` - Login and get access token

### Protected Endpoints (Require Bearer Token)

- `GET /users/me` - Get current user information
- `GET /users` - Get all users (requires authentication)
- `PUT /users/me` - Update current user information

## User Data Model

Each user contains:
- `full_name` (string): User's full name
- `email` (string): Unique email address
- `password_hash` (string): Hashed password
- `income_profile` (float): User's income profile
- `coverage` (string): Insurance coverage type
- `created_at` (datetime): Account creation timestamp
- `updated_at` (datetime): Last update timestamp

## Example Usage

### Register a new user

```bash
curl -X POST "http://localhost:8000/register" \\
  -H "Content-Type: application/json" \\
  -d '{
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123",
    "income_profile": 75000.0,
    "coverage": "premium"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/login" \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }'
```

### Access protected endpoint

```bash
curl -X GET "http://localhost:8000/users/me" \\
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Testing

Run the test script to verify API functionality:

```bash
python test_api.py
```

## Database

The application uses SQLite database (`health_insurance.db`) which is automatically created on first run. The database file is excluded from git by default.

## Security Notes

- ✅ SECRET_KEY is loaded from environment variables
- ✅ DATABASE_URL is configurable via environment variables
- ✅ JWT settings (ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES) are configurable
- ✅ Server settings (HOST, PORT) are configurable
- ✅ All environment files are excluded from version control
- Use HTTPS in production
- Implement rate limiting for authentication endpoints
- Consider adding email verification for registration

## Environment Variable Summary

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | fallback-secret-key-for-development-only | JWT signing secret (CHANGE IN PRODUCTION) |
| `DATABASE_URL` | health_insurance.db | SQLite database file path |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | JWT token expiration time in minutes |
| `ALGORITHM` | HS256 | JWT signing algorithm |
| `HOST` | 0.0.0.0 | Server bind address |
| `PORT` | 8000 | Server port |

## Generating a Secure Secret Key

You can generate a secure secret key using Python:

```bash
python -c "import secrets; print(f'SECRET_KEY={secrets.token_urlsafe(32)}')"
```

## Production Deployment

For production deployment:

1. Set a strong, randomly generated `SECRET_KEY`
2. Configure appropriate `HOST` and `PORT` values
3. Use HTTPS/TLS encryption
4. Set up proper database backups
5. Configure monitoring and logging
6. Implement rate limiting and security headers
