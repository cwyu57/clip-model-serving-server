# CLIP Model Serving Server

A FastAPI-based service for serving OpenAI's CLIP model, providing image and text embedding generation capabilities with built-in authentication, search logging, and feedback collection.

## Features

- Fast and scalable CLIP model inference
- JWT-based authentication
- Search logging and analytics
- User feedback collection
- Docker-ready deployment
- Comprehensive API documentation with OpenAPI/Swagger

## Prerequisites

Before you begin, ensure you have the following installed on your macOS system:

### Required Tools

1. **Homebrew** - Package manager for macOS
   ```bash
   # Install Homebrew if you don't have it
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Development Tools**
   ```bash
   brew install uv just gum
   ```
   - `uv` - Fast Python package installer and resolver
   - `just` - Command runner for project tasks
   - `gum` - Tool for glamorous shell scripts (used in migrations)

   **Optional: Enable `just` auto-completion for zsh**

   Add the following to your `~/.zshrc`:
   ```bash
   fpath+=($(brew --prefix)/share/zsh/site-functions)
   autoload -Uz compinit
   compinit
   ```
   Then reload your shell: `source ~/.zshrc`

3. **Docker Desktop** - For running PostgreSQL

   Download and install from [docker.com](https://www.docker.com/products/docker-desktop/)

   This includes both Docker and Docker Compose.

4. **Python 3.13** - Managed automatically by `uv`

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/cwyu57/clip-model-serving-server.git
cd clip-model-serving-server
```

### 2. Install Python Dependencies

```bash
uv sync --dev
```

This will create a virtual environment and install all dependencies defined in `pyproject.toml`.

### 3. Set Up Environment Variables

```bash
cp .env.example .env
```

### 4. Run Database Migrations

Apply database schema migrations:

```bash
just pg-up && just migrate
```

### 5. Start the Development Server

You can run the application in different ways:

**Option A: Local Development (Recommended for development)**

Run the app locally while connecting to Docker infrastructure:
```bash
just local
```

This runs the Python app on your local machine (with hot reload) while connecting to PostgreSQL in Docker containers.

**Option B: Full Docker Stack**

Run everything in Docker (app + infrastructure):
```bash
just dev
```

### 6. Access the API Documentation

Open the interactive OpenAPI documentation in your browser:

```bash
open http://localhost:8000/docs
```

## Usage

### Authentication

The API uses JWT-based authentication. Use the following credentials for testing:

**Default Test User:**
- Username: `user-1`, `user-2`, `user-3`, `user-4`, `user-5`
- Password: `password123`
