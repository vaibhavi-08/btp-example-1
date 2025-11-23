pipeline {
    agent any

    environment {
        MAVEN_OPTS = "-Duser.home=${WORKSPACE}/.m2"
    }

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
                sh 'mvn dependency:resolve -B'
            }
        }

        stage('Build') {
            steps {
                sh '''
                    mvn clean compile -B
                    mvn package -DskipTests -B
                    mvn dependency:analyze -B
                    mvn dependency:tree -B
                '''
            }
            post {
                success {
                    archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
                }
            }
        }

        stage('Test & Quality') {
            failFast true
            parallel {

                stage('Test') {
                    steps {
                        sh '''
                            mvn test -B
                            mvn verify -DskipUnitTests -B
                        '''
                    }
                    post {
                        always {
                            junit 'target/surefire-reports/*.xml'
                            archiveArtifacts artifacts: 'target/site/jacoco/jacoco.xml'
                        }
                    }
                }

                stage('Quality') {
                    steps {
                        sh '''
                            mvn checkstyle:check -B
                            mvn pmd:check -B
                            mvn dependency-check-maven:check -DskipTests -B
                        '''
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: 'target/site/checkstyle/checkstyle.xml'
                            archiveArtifacts artifacts: 'target/site/pmd/pmd.xml'
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs() // Complete cleanup to avoid cache bloat
        }
    }
}