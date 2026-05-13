pipeline {
    agent any

    environment {
        REGISTRY_CREDS   = 'dockerhub-credentials'
        DEPLOY_SSH_CREDS = 'deploy-server-ssh'
        DOCKER_REGISTRY  = 'registry-1.docker.io'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                script {

                    // Read values from pipeline.config
                    def config = readProperties file: 'pipeline.config'

                    env.DOCKER_IMAGE  = config.DOCKER_IMAGE
                    env.DEPLOY_HOST   = config.DEPLOY_HOST
                    env.DEPLOY_USER   = config.DEPLOY_USER
                    env.DEPLOY_BRANCH = config.DEPLOY_BRANCH
                    env.CONTAINER_NAME = config.CONTAINER_NAME
                }

                sh '''
                    python3 -m venv venv
                    . venv/bin/activate

                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build') {
            when {
                branch env.DEPLOY_BRANCH
            }

            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Quality') {
            steps {
                sh '''
                    . venv/bin/activate

                    # Run flake8 only if installed
                    if command -v flake8 >/dev/null 2>&1; then
                        flake8 .
                    else
                        echo "flake8 not installed, skipping quality checks"
                    fi
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate

                    # Run pytest if tests folder exists
                    if [ -d "tests" ]; then
                        pytest tests/
                    else
                        echo "No tests directory found"
                    fi
                '''
            }
        }

        stage('Deploy') {
            when {
                branch env.DEPLOY_BRANCH
            }

            steps {

                script {

                    // Push image to Docker registry
                    docker.withRegistry("https://${DOCKER_REGISTRY}", REGISTRY_CREDS) {
                        dockerImage.push('latest')
                        dockerImage.push("${BUILD_NUMBER}")
                    }
                }

                sshagent(credentials: [DEPLOY_SSH_CREDS]) {

                    sh """
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '

                        docker pull ${DOCKER_IMAGE}:latest

                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true

                        docker run -d \
                            --name ${CONTAINER_NAME} \
                            ${DOCKER_IMAGE}:latest
                    '
                    """
                }
            }
        }
    }

    post {

        success {
            echo 'Pipeline executed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}