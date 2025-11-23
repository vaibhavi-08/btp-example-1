pipeline {
    agent any

    tools {
        maven 'Maven_3.8.7'
        jdk 'JDK11'
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
                withMaven(maven: 'maven_3_5_0') {
                    sh 'mvn -B clean compile'
                }
            }
        }

        stage('Build') {
            steps {
                withMaven(maven: 'maven_3_5_0') {
                    // Using -DskipTests saves time here
                    sh 'mvn -B -DskipTests deploy'
                }
            }
        }

        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        withMaven(maven: 'maven_3_5_0') {
                            sh 'mvn -B test'
                        }
                    }
                }
                stage('Integration Tests') {
                    steps {
                        withMaven(maven: 'maven_3_5_0') {
                            // verify runs integration tests if configured
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
                // Minimal dependency vulnerability scan
                withMaven(maven: 'maven_3_5_0') {
                    // OWASP Dependency Check (light version)
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