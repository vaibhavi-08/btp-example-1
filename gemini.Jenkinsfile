pipeline {
    agent any

    options {
        // Skips the default declarative checkout so we can define it explicitly
        skipDefaultCheckout()
    }

    environment {
        // Credentials and Registry info defined directly in the pipeline as requested
        REGISTRY_CREDS   = 'dockerhub-credentials'
        DEPLOY_SSH_CREDS = 'deploy-server-ssh'
        DOCKER_REGISTRY  = 'registry-1.docker.io'
    }

    stages {
        stage('Checkout') {
            steps {
                // Explicitly checkout the code from SCM
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                script {
                    // Read variables from pipeline.config and inject them into the environment
                    def props = readProperties file: 'pipeline.config'
                    env.DOCKER_IMAGE   = props.DOCKER_IMAGE
                    env.DEPLOY_HOST    = props.DEPLOY_HOST
                    env.DEPLOY_USER    = props.DEPLOY_USER
                    env.DEPLOY_BRANCH  = props.DEPLOY_BRANCH
                    env.CONTAINER_NAME = props.CONTAINER_NAME
                }
                
                // Set up a Python virtual environment and install dependencies
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build') {
            steps {
                script {
                    // Build the Docker image using the variable from pipeline.config
                    // We assign it to a variable so we can push it later
                    dockerImage = docker.build("${env.DOCKER_IMAGE}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Quality') {
            steps {
                // Run a linter (like flake8) to check code quality
                sh '''
                    . venv/bin/activate
                    pip install flake8
                    # Fails the build if there are syntax errors or undefined names
                    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                '''
            }
        }

        stage('Test') {
            steps {
                // Run tests using pytest against the tests/ directory
                sh '''
                    . venv/bin/activate
                    pip install pytest
                    pytest tests/
                '''
            }
        }

        stage('Deploy') {
            when {
                // Only trigger the deploy stage if we are on the branch specified in the config
                branch "${env.DEPLOY_BRANCH}"
            }
            steps {
                script {
                    // 1. Push the built image to Docker Hub
                    docker.withRegistry("https://${env.DOCKER_REGISTRY}", env.REGISTRY_CREDS) {
                        dockerImage.push("${env.BUILD_NUMBER}")
                        dockerImage.push("latest")
                    }

                    // 2. SSH into the deployment server (your laptop) to run the container
                    sshagent(credentials: [env.DEPLOY_SSH_CREDS]) {
                        sh """
                            ssh -o StrictHostKeyChecking=no ${env.DEPLOY_USER}@${env.DEPLOY_HOST} '
                                # Pull the newly built image
                                docker pull ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER}
                                
                                # Stop and remove the existing container if it is running
                                docker stop ${env.CONTAINER_NAME} || true
                                docker rm ${env.CONTAINER_NAME} || true
                                
                                # Start the new container
                                docker run -d --name ${env.CONTAINER_NAME} ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER}
                            '
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Clean up the workspace after the pipeline finishes
            cleanWs()
        }
    }
}