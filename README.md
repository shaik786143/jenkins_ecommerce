# My E-Commerce Project

This is a comprehensive e-commerce platform built with Django, designed to showcase modern backend development practices, including REST APIs, database management, and a fully automated CI/CD pipeline.

## 1. Project Purpose and Use

The goal of this project is to create a functional and scalable e-commerce backend. It serves as a practical example of integrating various technologies to build, test, and deploy a web application automatically.

Key features include:
- A RESTful API for managing products.
- A dual-database setup for separating transactional data from analytics.
- A containerized environment for consistent development and deployment.
- An automated CI/CD pipeline for continuous integration and delivery.

## 2. Technologies Used

This project integrates a variety of modern technologies:

- **Backend**: Django, Django REST Framework (DRF)
- **Databases**:
    - **MySQL**: For primary application data (products, users, etc.).
    - **SQLite**: For a separate analytics and reporting database.
- **Frontend**: Basic HTML, CSS, and JavaScript for interacting with the API.
- **Testing**: `pytest` with `pytest-django` for testing Django applications.
- **CI/CD**:
    - **Jenkins**: For orchestrating the automated pipeline.
    - **ngrok**: For exposing the local Jenkins instance to GitHub webhooks during development.
- **Containerization**: Docker and Docker Compose for creating reproducible environments.
- **Environment Management**: `python-dotenv` for managing environment variables.

## 3. Project Structure

The project is organized into several key directories:

```
.
├── frontend/             # Contains basic frontend files (HTML, CSS, JS)
├── my_ecommerce/         # The main Django project directory
│   ├── settings.py       # Django settings, database configs, app definitions
│   ├── urls.py           # Root URL configuration
│   └── routers.py        # Custom database router for the dual-DB setup
├── reporting/            # Django app for analytics and reporting features
├── testapp/              # Django app for core e-commerce features (e.g., products)
├── Dockerfile            # Instructions to build the Docker image for the application
├── docker-compose.yml    # Defines multi-container services (e.g., app, database)
├── Jenkinsfile           # Defines the stages for the Jenkins CI/CD pipeline
├── manage.py             # Django's command-line utility
├── populate.py           # Script to populate the database with initial data
└── requirements.txt      # Python package dependencies
```

## 4. Automated CI/CD Pipeline Implementation

A key feature of this project is its automated build pipeline, which runs tests and prepares the application for deployment on every code push.

### Where It Was Implemented

- **Jenkins**: A pipeline job was created and configured to use the `Jenkinsfile` from the repository. The "GitHub hook trigger" was enabled.
- **GitHub**: In the repository's **Settings > Webhooks**, a new webhook was created.
- **Local Machine**: The `ngrok` client was used to create a public URL that forwards traffic to the local Jenkins server on port `8080`.

### How It Was Implemented

1.  **The Trigger**: When code is pushed to the GitHub repository, a `push` event is fired.
2.  **Webhook Notification**: The configured GitHub webhook sends a JSON payload containing information about the push event to the public `ngrok` URL.
3.  **The Tunnel**: `ngrok` receives this request and securely forwards it to `http://localhost:8080/github-webhook/` on the local machine.
4.  **Jenkins Activation**: The Jenkins GitHub plugin, listening at that endpoint, receives the request, verifies it came from the correct repository, and automatically starts a new build for the corresponding branch.
5.  **Pipeline Execution**: Jenkins then executes the stages defined in the `Jenkinsfile` (e.g., checking out code, running tests, etc.).

This setup enables a seamless, automated workflow from code commit to build verification, forming the foundation of a modern CI/CD process.

# E-Commerce Analytics Dashboard

This project is a comprehensive E-Commerce Analytics Dashboard designed to showcase a range of backend development skills. It features a Django-powered backend, RESTful APIs, performance enhancements with Memcached, and containerization with Docker.

## Key Features

*   **Real-time Analytics**: Monitor sales and inventory with a dynamic dashboard.
*   **RESTful APIs**: A suite of APIs built with Django REST Framework to manage e-commerce data.
*   **High Performance**: Integrated Memcached to reduce query times and enhance server performance.
*   **Containerized Deployment**: Dockerized microservices for easy deployment on platforms like AWS EC2.
*   **Comprehensive Testing**: High unit test coverage with automated testing pipelines to ensure code quality and reliability.
*   **Modern Frontend Integration**: Designed to seamlessly partner with front-end teams, providing a clear and efficient backend logic.

## Project Goals

This project aims to demonstrate the following capabilities:

-   Developing and maintaining REST APIs with Django, with a focus on reducing average response time.
-   Deploying containerized microservices on cloud infrastructure.
-   Achieving high unit test coverage through automated testing.
-   Collaborating effectively with front-end teams to align user experience and back-end logic.

## Technology Stack

-   **Backend**: Django, Django REST Framework
-   **Caching**: Memcached
-   **Database**: PostgreSQL (or SQLite for development)
-   **Containerization**: Docker, Docker Compose
-   **Testing**: Pytest
-   **Frontend**: (To be decided - likely a simple HTML/CSS/JS application)

#   e c o m m e r c e _ j e n k i n s 
 
 