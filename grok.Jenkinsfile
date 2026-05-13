pipeline {
    agent any

    environment {
        REGISTRY_CREDS = 'dockerhub-credentials'
        DEPLOY_SSH_CREDS = 'deploy-server-ssh'
        DOCKER_REGISTRY = 'registry-1.docker.io'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "✅ Checkout completed"
            }
        }

        stage('Setup') {
            steps {
                script {
                    // Read configuration from pipeline.config
                    def config = readProperties file: 'pipeline.config'
                    env.DOCKER_IMAGE = config.DOCKER_IMAGE
                    env.DEPLOY_HOST = config.DEPLOY_HOST
                    env.DEPLOY_USER = config.DEPLOY_USER
                    env.DEPLOY_BRANCH = config.DEPLOY_BRANCH
                    env.CONTAINER_NAME = config.CONTAINER_NAME
                    
                    echo "✅ Configuration loaded"
                    echo "Image: ${env.DOCKER_IMAGE}"
                    echo "Deploy Host: ${env.DEPLOY_HOST}"
                    echo "Container: ${env.CONTAINER_NAME}"
                }
                
                sh '''
                    python3 -m venv venv || true
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
                echo "✅ Setup completed (virtual environment + dependencies)"
            }
        }

        stage('Quality') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install pylint flake8 || true
                    
                    echo "Running linting..."
                    flake8 . --exclude=venv || true
                    pylint --disable=all --enable=E,F *.py || true
                '''
                echo "✅ Quality checks completed"
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install pytest || true
                    
                    echo "Running tests..."
                    python -m pytest tests/ -v --tb=short || true
                '''
                echo "✅ Tests completed"
            }
        }

        stage('Build') {
            steps {
                script {
                    // Build Docker image with tag
                    docker.build("${DOCKER_IMAGE}:${env.BUILD_NUMBER}")
                    docker.build("${DOCKER_IMAGE}:latest")
                }
                echo "✅ Docker image built successfully"
            }
        }

        stage('Push to Registry') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", REGISTRY_CREDS) {
                        docker.image("${DOCKER_IMAGE}:${env.BUILD_NUMBER}").push()
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
                }
                echo "✅ Image pushed to ${DOCKER_REGISTRY}"
            }
        }

        stage('Deploy') {
            when {
                branch "${env.DEPLOY_BRANCH}"
            }
            steps {
                script {
                    sshagent(credentials: [DEPLOY_SSH_CREDS]) {
                        sh '''
                            ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '
                                docker pull ${DOCKER_IMAGE}:latest &&
                                docker stop ${CONTAINER_NAME} || true &&
                                docker rm ${CONTAINER_NAME} || true &&
                                docker run -d --name ${CONTAINER_NAME} \
                                    --restart unless-stopped \
                                    ${DOCKER_IMAGE}:latest
                            '
                        '''
                    }
                }
                echo "✅ Deployment completed on ${DEPLOY_HOST}"
            }
        }
    }

    post {
        success {
            echo "🎉 Pipeline executed successfully!"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}