pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        MAVEN_OPTS = '-Dmaven.test.failure.ignore=false'
    }

    stages {
        stage('Checkout') {
            steps {
                // No submodules or LFS according to JSON, so simple SCM checkout is enough
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    set -e

                    echo "[Setup] Preparing Maven dependency cache..."

                    # Pre-fetch dependencies to speed up later Maven runs
                    mvn -B dependency:go-offline || mvn -B dependency:resolve

                    echo "[Setup] Maven dependency setup complete."
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    set -e

                    echo "[Build] Cleaning and packaging application (skipping tests for speed)..."
                    mvn -B -DskipTests clean package

                    echo "[Build] Build artifacts available under target/ (e.g., target/*.jar)."
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    set -e

                    echo "[Test] Running JUnit tests via Maven..."
                    mvn -B test

                    echo "[Test] Test phase complete."
                '''
            }
        }

        stage('Quality') {
            steps {
                sh '''
                    set +e

                    echo "[Quality] No static analysis or security tools configured in this repo."
                    echo "[Quality] Hint: Consider adding SpotBugs, Checkstyle, or other static analysis tools"
                    echo "[Quality]       to improve code quality and catch vulnerabilities earlier."

                    # If in future you add tools, you can plug them here, e.g.:
                    # mvn -B spotbugs:check
                    # mvn -B checkstyle:check

                    exit 0
                '''
            }
        }

        stage('Package') {
            steps {
                sh '''
                    set -e

                    echo "[Package] Collecting JAR artifacts from target/..."
                    ls -1 target/*.jar || echo "[Package] No JAR files found in target/."

                    echo "[Package] Archiving JARs as build artifacts..."
                '''
                archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
            }
        }

        stage('Deploy') {
            when {
                expression {
                    // No deployment config in JSON; keep deploy manual and only on main/master
                    return env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'master'
                }
            }
            steps {
                script {
                    input message: "No deployment configuration detected. Proceed with manual deploy step?", ok: "Continue"
                }
                sh '''
                    echo "[Deploy] No automated deployment target configured for this project."
                    echo "[Deploy] You can implement deployment here (e.g., kubectl apply, scp, etc.)."
                '''
            }
        }
    }
}
