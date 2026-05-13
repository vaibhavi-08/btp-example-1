pipeline {
    agent any

    environment {
        CONFIG_FILE = 'pipeline.config'
        REGISTRY_CREDS = 'dockerhub-credentials'
        DEPLOY_SSH_CREDS = 'deploy-server-ssh'
        DOCKER_REGISTRY = 'registry-1.docker.io'
    }

    stages {
        stage('checkout') {
            steps {
                checkout scm
                script {
                    // Parse pipeline.config (KEY=VALUE format)
                    def configLines = readFile(CONFIG_FILE).readLines()
                    def config = [:]
                    configLines.each { line ->
                        if (line && !line.trim().startsWith('#') && line.contains('=')) {
                            def parts = line.split('=', 2)
                            config[parts[0].trim()] = parts[1].trim()
                        }
                    }
                    env.DOCKER_IMAGE = config.DOCKER_IMAGE
                    env.DEPLOY_HOST = config.DEPLOY_HOST
                    env.DEPLOY_USER = config.DEPLOY_USER
                    env.DEPLOY_BRANCH = config.DEPLOY_BRANCH
                    env.CONTAINER_NAME = config.CONTAINER_NAME
                    echo "Loaded config: Image=${env.DOCKER_IMAGE}, Host=${env.DEPLOY_HOST}, Branch=${env.DEPLOY_BRANCH}"
                }
            }
        }

        stage('setup') {
            steps {
                script {
                    // Create virtual environment and install dependencies
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        pip install pytest pytest-cov flake8
                    '''
                }
            }
        }

        stage('build') {
            steps {
                script {
                    // Build Docker image with build number and latest tag
                    sh "docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER} ."
                    sh "docker tag ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('quality') {
            steps {
                script {
                    // Run static code analysis with flake8
                    sh '''
                        . venv/bin/activate
                        # Critical errors check (fail build on these)
                        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                        # Style checks (warnings only)
                        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                    '''
                }
            }
        }

        stage('test') {
            steps {
                script {
                    // Run pytest with coverage and JUnit XML output
                    sh '''
                        . venv/bin/activate
                        pytest tests/ -v --cov=. --cov-report=xml --junitxml=reports/test-results.xml
                    '''
                }
                post {
                    always {
                        // Publish test results if reports exist
                        junit allowEmptyResults: true, testResults: 'reports/test-results.xml'
                    }
                }
            }
        }

        stage('deploy') {
            when {
                branch "${env.DEPLOY_BRANCH}"
            }
            steps {
                script {
                    // Push Docker image to registry
                    withCredentials([usernamePassword(
                        credentialsId: REGISTRY_CREDS,
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh "echo ${DOCKER_PASS} | docker login ${DOCKER_REGISTRY} -u ${DOCKER_USER} --password-stdin"
                        sh "docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER}"
                        sh "docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:latest"
                        sh "docker logout ${DOCKER_REGISTRY}"
                    }

                    // Deploy to your laptop via SSH
                    sshagent(credentials: [DEPLOY_SSH_CREDS]) {
                        sh """
                            ssh -o StrictHostKeyChecking=no -o ConnectTimeout=30 ${DEPLOY_USER}@${DEPLOY_HOST} \\
                                "echo '${DOCKER_PASS}' | docker login ${DOCKER_REGISTRY} -u '${DOCKER_USER}' --password-stdin && \\
                                docker pull ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER} && \\
                                docker stop ${CONTAINER_NAME} 2>/dev/null || true && \\
                                docker rm ${CONTAINER_NAME} 2>/dev/null || true && \\
                                docker run -d --name ${CONTAINER_NAME} ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER} && \\
                                docker logout ${DOCKER_REGISTRY}"
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            // Cleanup: remove Docker artifacts and workspace
            sh 'docker rmi ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER} 2>/dev/null || true'
            cleanWs()
        }
        failure {
            echo '❌ Pipeline FAILED - Check console output for details'
        }
        success {
            echo "✅ Pipeline SUCCESS - Deployed ${DOCKER_IMAGE}:${BUILD_NUMBER} to ${DEPLOY_HOST}"
        }
    }
}