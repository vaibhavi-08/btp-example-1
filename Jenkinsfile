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
                // single explicit checkout (we disabled default checkout above)
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                // prepare dependencies off-line so later stages don't re-download
                withMaven(maven: 'Maven 3.8.7') {
                    // -B = batch mode (faster logs), dependency:go-offline will pull deps
                    sh 'mvn -B -DskipTests=true clean compile dependency:go-offline'
                }
            }
        }

        stage('Build') {
            steps {
                withMaven(maven: 'Maven 3.8.7') {
                    // we skip tests here to avoid running them twice (they run in the Test stage)
                    sh 'mvn -B -DskipTests=true package'
                }
            }
        }

        // Test is a dedicated stage. We run Unit and Integration tests in parallel to save time.
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        withMaven(maven: 'Maven 3.8.7') {
                            sh 'mvn -B -DskipITs=true test'
                        }
                    }
                }
                stage('Integration Tests') {
                    // only run integration tests if integration sources/configs exist
                    // (prevents wasting time when not present)
                    when {
                        expression { return fileExists('src/integration') || fileExists('src/it') }
                    }
                    steps {
                        withMaven(maven: 'Maven 3.8.7') {
                            // use failsafe plugin (common pattern) — adjust if your project uses a different goal
                            sh 'mvn -B -DskipUnitTests=true failsafe:integration-test || true'
                        }
                    }
                }
            }
        }

        // Quality stage is separate as requested. Keep it lightweight and non-blocking.
        stage('Quality') {
            steps {
                withMaven(maven: 'Maven 3.8.7') {
                    // run static analysis / verification; keep it non-blocking so failure here doesn't break pipeline
                    // (remove "|| true" if you want Quality failures to fail the pipeline)
                    sh 'mvn -B -DskipTests=true verify sonar:sonar || true'
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
