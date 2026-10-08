pipeline {
    agent any

    environment {
        STUDENT_NAME = 'Danil'
        STUDENT_SURNAME = 'Kukurekin'
        STUDENT_GROUP = 'IT2-2312'
        STUDENT_ID = '37554'
        IMAGE_NAME = 'kukurekin-danil-devops'
        CONTAINER_NAME = 'kukurekin-danil-container'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --oneline'
            }
        }
        stage('Build') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m compileall app'
            }
        }
        stage('Test') {
            steps {
                sh '''docker run --rm -v "$WORKSPACE":/app -w /app python:3.12-slim \\
                    sh -c "pip install --no-cache-dir -r requirements-dev.txt && python -m unittest discover -s tests -v"'''
            }
        }
        stage('Docker Build') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }
        stage('Docker Run') {
            steps {
                sh 'docker rm -f $CONTAINER_NAME || true'
                sh '''docker run -d --name $CONTAINER_NAME -p 8000:8000 \\
                    -e STUDENT_NAME=$STUDENT_NAME \\
                    -e STUDENT_SURNAME=$STUDENT_SURNAME \\
                    -e STUDENT_GROUP=$STUDENT_GROUP \\
                    -e STUDENT_ID=$STUDENT_ID \\
                    $IMAGE_NAME'''
                sh 'docker ps --filter name=$CONTAINER_NAME'
                sh 'docker logs $CONTAINER_NAME'
            }
        }
    }

    post {
        success {
            echo "Student: ${STUDENT_NAME} ${STUDENT_SURNAME}"
            echo "Group: ${STUDENT_GROUP}"
            echo "Student ID: ${STUDENT_ID}"
        }
    }
}
