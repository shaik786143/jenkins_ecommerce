pipeline {
    agent any

    environment {
        // Defines the name for our Docker image
        IMAGE_NAME = "my-ecommerce-app"
        // Gets the current git commit hash to use as a tag
        IMAGE_TAG = "build-${env.BUILD_NUMBER}"
        DOCKER_IMAGE = "shaik054/my-ecommerce-app:${env.BUILD_NUMBER}"
        DOCKERHUB_CREDENTIALS = credentials('00d25bb4-f749-428e-ab65-387917b38244')
        PROD_SERVER = "ubuntu@123.45.67.89"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                bat 'pytest'
            }
        }
        stage('Build Docker Image') {
            steps {
                bat "docker build -t ${DOCKER_IMAGE} ."
            }
        }
        stage('Push Docker Image') {
            steps {
                bat "docker login -u %DOCKERHUB_CREDENTIALS_USR% -p %DOCKERHUB_CREDENTIALS_PSW%"
                bat "docker push ${DOCKER_IMAGE}"
            }
        }
        stage('Deploy to Production') {
            steps {
                sshagent(['prod-server-ssh-id']) {
                    bat """
                    ssh %PROD_SERVER% "docker pull ${DOCKER_IMAGE} && docker stop my-ecommerce-app || true && docker rm my-ecommerce-app || true && docker run -d --name my-ecommerce-app -p 80:8000 --env-file /home/ubuntu/my-ecommerce/.env ${DOCKER_IMAGE}"
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
            // Clean up workspace or send notifications
        }
    }
} 