# Deployment Guide

## Overview

This guide provides instructions for deploying the Taskeri backend in different environments. It covers environment setup, database configuration, application deployment, and maintenance procedures.

## System Requirements

- **Python**: 3.8+
- **Database**: MySQL 8.0+

## Environment Setup

### Development Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/taskeri.git
   cd taskeri
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (create a `.env` file):
   ```
   # Database
   DB_USERNAME=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=taskeri

   # JWT
   JWT_SECRET_KEY=your-secret-key-at-least-32-chars
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

   # Server
   HOST=localhost
   PORT=8000
   
   ```

5. **Initialize the database**:
   ```bash
   alembic upgrade head
   ```

6. **Run the development server**:
   ```bash
   python main.py
   ```

