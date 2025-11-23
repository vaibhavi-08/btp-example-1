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
                withMaven(maven: 'maven 3.8.7') {
                    sh 'mvn clean compile'
                }
            }
        }

        stage('Build') {
            steps {
                withMaven(maven: 'maven 3.8.7') {
                    sh 'mvn clean package'
                }
            }
        }

        stage('Test & Quality') {
            failFast true
            parallel {

                stage('Test') {
                    steps {
                        withMaven(maven: 'maven 3.8.7') {
                            sh 'mvn test'
                        }
                    }
                }

                stage('Quality') {
                    steps {
                        echo 'No quality commands defined in JSON — stage intentionally empty'
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