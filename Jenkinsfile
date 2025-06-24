pipeline {
    agent any

    environment {
        // Defines the name for our Docker image
        IMAGE_NAME = "my-ecommerce-app"
        // Gets the current git commit hash to use as a tag
        IMAGE_TAG = "build-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    echo 'Installing Python dependencies...'
                    bat 'pip install -r requirements.txt'
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    echo 'Running tests...'
                    bat 'pytest'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}..."
                    // Assumes Docker is configured in the Jenkins environment
                    bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push Docker Image') {
            // This stage would typically push the image to a container registry
            // like Docker Hub, Amazon ECR, or Google Container Registry.
            // It requires credentials to be configured in Jenkins.
            steps {
                script {
                    echo "Skipping Docker push for this example..."
                    // Example command:
                    // withCredentials([dockerServer(credentialsId: 'dockerhub-creds')]) {
                    //   bat "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                    // }
                }
            }
        }

        stage('Deploy') {
            // This stage is highly dependent on the target environment.
            // It might involve running 'docker-compose up' on a server,
            // using 'kubectl apply' for Kubernetes, or using a cloud provider's SDK.
            steps {
                echo 'Deploying the application...'
                echo 'This is a placeholder. A real deployment script would go here.'
            }
        }

        stage('Test') {
            steps {
                sh 'python manage.py migrate'
                sh 'pytest'
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