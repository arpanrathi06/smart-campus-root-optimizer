pipeline {
    agent any
    environment {
        IMAGE_NAME = 'arpanrathi/smart-campus-route-optimizer'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build and Test') {
            steps {
                sh 'python3 -m venv .venv-ci'
                sh '.venv-ci/bin/pip install -r requirements.txt'
                sh '.venv-ci/bin/python -m unittest discover -s tests -v'
                sh '.venv-ci/bin/python -m py_compile app.py'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER -t $IMAGE_NAME:latest .'
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_TOKEN')]) {
                    sh '''
                        set +x
                        echo "$DOCKER_TOKEN" | docker login --username "$DOCKER_USER" --password-stdin
                        docker push "$IMAGE_NAME:$BUILD_NUMBER"
                        docker push "$IMAGE_NAME:latest"
                        docker logout
                    '''
                }
            }
        }
        stage('Deploy to Minikube') {
            steps {
                sh '''
                    sed "s|DOCKERHUB_USERNAME/smart-campus-route-optimizer|$IMAGE_NAME:$BUILD_NUMBER|g" k8s/deployment.yaml | minikube kubectl -- apply -f -
                    minikube kubectl -- apply -f k8s/service.yaml
                    minikube kubectl -- rollout status deployment/campus-navigator --timeout=180s
                '''
            }
        }
        stage('Verify') {
            steps {
                sh '''
                    minikube kubectl -- get pods
                    minikube kubectl -- get deployments
                    minikube kubectl -- get services
                    minikube kubectl -- get endpoints campus-navigator
                '''
            }
        }
    }
    post {
        always { echo 'Pipeline finished. Review stage results and Console Output.' }
    }
}
