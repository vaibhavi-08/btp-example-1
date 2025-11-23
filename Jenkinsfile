pipeline {
    agent any

    options {
        skipDefaultCheckout true
        timestamps()
        durabilityHint('PERFORMANCE_OPTIMIZED')
    }

    tools {
        maven 'Maven 3.8.7'    // From JSON "tools" (setup + build)
        jdk 'JDK 11'       // From JSON "tools" (setup + build)
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                sh 'git checkout SCM'
            }
        }

        stage('Setup') {
            steps {
                sh 'mvn dependency:resolve'
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean compile'
                sh 'mvn package -DskipTests'
            }
        }

        stage('Test & Quality') {
            failFast true
            parallel {

                stage('Test') {
                    steps {
                        sh 'mvn test'
                        sh 'mvn verify'
                    }
                }

                stage('Quality') {
                    steps {
                        sh 'mvn checkstyle:check'
                        sh 'mvn pmd:check'
                        sh 'mvn dependency-check:check'
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}