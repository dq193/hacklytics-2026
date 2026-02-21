# Health Insurance API

A FastAPI application for managing health insurance users.

## Features

- User management (Create, Read, Update)
- SQLite database for user data storage
- Environment variable configuration

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

## Environment Variables

Create a `.env` file in the project root:

```bash
DATABASE_URL=health_insurance.db
HOST=0.0.0.0
PORT=8000
