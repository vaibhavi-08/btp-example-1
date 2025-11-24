pipeline {
    agent any

    options {
        skipDefaultCheckout true
        timestamps()
        durabilityHint('PERFORMANCE_OPTIMIZED')
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
                    sh 'mvn clean compile'
                }
            }
        }

        stage('Build') {
            steps {
                withMaven(maven: 'Maven 3.8.7') {
                    sh 'mvn clean package'
                }
            }
        }

        stage('Test') {
            steps {
                withMaven(maven: 'Maven 3.8.7') {
                    sh 'mvn test'
                }
            }
        }

        stage('Quality') {
            steps {
                // If you have quality commands (sonar, lint, etc.), add them here.
                // Currently left intentionally empty as in your original file.
                echo 'No quality commands defined in JSON — stage intentionally empty'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
