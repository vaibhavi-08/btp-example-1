pipeline {
    agent any

    tools {
        maven 'Maven 3.8.7'
        jdk 'JDK 11'
    }

    options {
        durabilityHint('PERFORMANCE_OPTIMIZED')
        timestamps()
        skipDefaultCheckout(true)
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                withMaven(maven: 'Maven 3.8.7') {
                    sh 'mvn -B clean compile'
                }
            }
        }

        stage('Build') {
            steps {
                withMaven(maven: 'Maven 3.8.7') {
                    sh 'mvn -B -DskipTests deploy'
                }
            }
        }

        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        withMaven(maven: 'Maven 3.8.7') {
                            sh 'mvn -B test'
                        }
                    }
                }
                stage('Integration Tests') {
                    steps {
                        withMaven(maven: 'Maven 3.8.7') {
                            sh 'mvn -B verify -DskipUnitTests'
                        }
                    }
                }
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                }
            }
        }

        stage('Quality') {
            steps {
                withMaven(maven: 'Maven 3.8.7') {
                    sh 'mvn -B org.owasp:dependency-check-maven:check -DskipTests'
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: '**/dependency-check-report.html', fingerprint: true
                }
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed 😢"
        }
        success {
            echo "✔ Pipeline executed successfully! 🎉"
        }
    }
}