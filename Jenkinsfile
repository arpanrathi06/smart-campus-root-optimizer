```groovy
pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REGISTRY = '404571418135.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPOSITORY = 'smart-campus-route-optimizer'
        IMAGE_NAME = '404571418135.dkr.ecr.ap-south-1.amazonaws.com/smart-campus-route-optimizer'
        KUBECONFIG = '/var/lib/jenkins/.kube/config'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                sh '''
                    set -e
                    python3 -m venv .venv-ci
                    .venv-ci/bin/pip install -r requirements.txt
                    .venv-ci/bin/python -m unittest discover -s tests -v
                    .venv-ci/bin/python -m py_compile app.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    set -e
                    docker build \
                      -t "$IMAGE_NAME:$BUILD_NUMBER" \
                      -t "$IMAGE_NAME:latest" .
                '''
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                sh '''
                    set -e
                    aws ecr get-login-password --region "$AWS_REGION" |
                      docker login --username AWS --password-stdin "$ECR_REGISTRY"

                    docker push "$IMAGE_NAME:$BUILD_NUMBER"
                    docker push "$IMAGE_NAME:latest"
                    docker logout "$ECR_REGISTRY"
                '''
            }
        }

        stage('Refresh ECR Pull Secret') {
            steps {
                sh '''
                    set -e
                    aws ecr get-login-password --region "$AWS_REGION" > /tmp/ecr-token-$BUILD_NUMBER

                    minikube kubectl -- delete secret ecr-secret \
                      --ignore-not-found=true

                    minikube kubectl -- create secret docker-registry ecr-secret \
                      --docker-server="$ECR_REGISTRY" \
                      --docker-username=AWS \
                      --docker-password="$(cat /tmp/ecr-token-$BUILD_NUMBER)"

                    rm -f /tmp/ecr-token-$BUILD_NUMBER
                '''
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                    set -e
                    sed "s|image: .*smart-campus-route-optimizer:.*|image: $IMAGE_NAME:$BUILD_NUMBER|" \
  k8s/deployment.yaml | minikube kubectl -- apply -f -

                    minikube kubectl -- apply -f k8s/service.yaml

                    minikube kubectl -- rollout status \
                      deployment/campus-navigator --timeout=180s
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                    set -e
                    minikube kubectl -- get pods
                    minikube kubectl -- get deployments
                    minikube kubectl -- get services
                    minikube kubectl -- get endpoints campus-navigator
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished. Review stage results and Console Output.'
        }
    }
}
```
