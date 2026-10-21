# Smart Campus Route Optimizer — Website

This starter web project preserves the 16 building names and 22 weighted undirected connections in the supplied C++ program. It provides shortest path using Dijkstra, adjacency list, adjacency matrix and Prim minimum spanning tree through a Flask API and responsive browser UI.

## Important
The original source is an interactive C++ console application. This website reimplements its graph data and Dijkstra/Prim features in Python so they can be accessed over HTTP. It does not compile or execute the original C++ file. If your evaluator requires the C++ executable itself to be integrated, that needs a separate wrapper/refactor.

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
python app.py
```
Open http://127.0.0.1:5000

## Run with Docker
```bash
docker build -t smart-campus-route-optimizer:local .
docker run --rm -p 5000:5000 smart-campus-route-optimizer:local
```

## API
- GET /api/health
- GET /api/buildings
- GET /api/adjacency
- GET /api/matrix
- GET /api/shortest-path?source=0&destination=15
- GET /api/mst

## CCA 2 / Jenkins
1. Create GitHub repo `smart-campus-route-optimizer` and push this folder.
2. Create a Docker Hub repo with the same name.
3. Replace `DOCKERHUB_USERNAME` in Jenkinsfile with your Docker Hub username.
4. In Jenkins, add Username with password credentials ID `dockerhub-creds`; use a Docker Hub access token as the password.
5. Create a Pipeline job using Pipeline script from SCM, Git, your repository URL, branch `*/main`.
6. Ensure the Jenkins execution user has Python 3, the `python3-venv` package, Docker, Minikube and access to the Minikube cluster.
7. Run Build Now. Then change a visible label in `static/index.html`, commit and push, and run Build Now again.

## AWS note
An EC2 t2.micro has 1 GiB RAM. Jenkins, Docker and Minikube together may not run reliably at that size. Check costs and eligibility, then consider a larger instance (e.g. 2 vCPU and 4 GiB RAM) for the practical.

## Verify Kubernetes
```bash
sudo -u jenkins -H minikube kubectl -- get pods
sudo -u jenkins -H minikube kubectl -- get deployments
sudo -u jenkins -H minikube kubectl -- get services
```
For a temporary demo port-forward, run:
```bash
sudo -u jenkins -H minikube kubectl -- port-forward --address 0.0.0.0 service/campus-navigator 8081:80
```
Restrict inbound TCP 8081 in the EC2 security group to your own IP, then open `http://EC2_PUBLIC_IP:8081`. Stop the command with Ctrl+C after the demo. Do not expose it publicly.

## Troubleshooting
```bash
sudo systemctl status jenkins
sudo docker version
sudo -u jenkins -H minikube status
sudo -u jenkins -H minikube kubectl -- logs deployment/campus-navigator
```
