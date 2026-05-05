# Deployment Document - Portfolio Generator

## 1. Application Overview
This project provides a Portfolio Generator API with a simple frontend page. Users can create and fetch portfolio entries through Flask endpoints, and verify service health for deployment monitoring.

### API Endpoints
| Method | URL | Description | Example Response |
|---|---|---|---|
| GET | `/health` | Health check for uptime verification | `{"status":"ok"}` |
| GET | `/api/portfolios` | Returns all portfolio items | `{"items":[...],"count":1}` |
| GET | `/api/portfolios/<id>` | Returns one portfolio by id | `{"id":1,"name":"Hadi","title":"Software Engineer","bio":"..."}` |
| POST | `/api/portfolios` | Creates a portfolio entry from JSON body | `{"id":1,"name":"Hadi","title":"Software Engineer","bio":"..."}` |

## 2. Architecture Diagram
```text
Browser
   |
   v
AWS EC2 (Ubuntu 22.04, t2.micro)
   |
   v
Docker Container (portfolio-generator:v1)
   |
   v
Flask App (app.py + frontend static files)
```

## 3. Tools and Technologies
| Tool | Why It Was Used |
|---|---|
| Linux (Ubuntu) | Host OS on EC2 for deployment and server commands |
| Python 3.11 | Runtime for Flask backend |
| Flask | API framework for endpoints and health route |
| flask-cors | Enable CORS for cross-origin requests |
| Git | Version control with traceable commits |
| GitHub | Repository hosting and collaboration |
| Docker | Containerized and reproducible runtime |
| GitHub Actions | Automated testing and Docker build pipeline |
| AWS EC2 | Public cloud VM to host the app on internet |

## 4. Local Setup Instructions
1. Clone repository:
```bash
git clone <YOUR_REPO_URL>
cd Portfolio-Generator-main
```
2. Build Docker image:
```bash
docker build -t portfolio-generator:v1 .
```
3. Run container:
```bash
docker run -d --name portfolio-generator -p 5000:5000 portfolio-generator:v1
```
4. Test health endpoint:
```bash
curl http://localhost:5000/health
```

## 5. CI/CD Pipeline Explanation
The workflow is located at `.github/workflows/ci.yml` and triggers on each push to `main`.

1. `test` job installs Python dependencies and runs:
```bash
python -m pytest test_app.py -v
```
2. `build-docker` job runs only after tests pass (`needs: test`), builds Docker image, starts a container, and runs a health check with curl.
3. If tests fail, the Docker build job does not execute.

## 6. Deployment Steps (AWS EC2)
1. Launch EC2 instance:
   - Type: `t2.micro`
   - AMI: Ubuntu 22.04 LTS
   - Storage: default 8GB
2. Configure security group inbound rules:
   - TCP 22 from your IP (SSH)
   - TCP 5000 from `0.0.0.0/0` (app)
3. Connect via SSH:
```bash
ssh -i /path/to/key.pem ubuntu@<EC2_PUBLIC_IP>
```
4. Install Docker:
```bash
sudo apt update
sudo apt install -y docker.io git
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker
```
5. Clone repo and build image:
```bash
git clone <YOUR_REPO_URL>
cd Portfolio-Generator-main
docker build -t portfolio-generator:v1 .
```
6. Run container with auto-restart:
```bash
docker run -d --name portfolio-generator --restart=always -p 5000:5000 portfolio-generator:v1
```
7. Verify from local machine:
```bash
curl http://<EC2_PUBLIC_IP>:5000/health
```

## 7. Testing Evidence
Including screenshots or terminal outputs for:
1. `python -m pytest test_app.py -v` passing all tests.
<img width="1150" height="351" alt="WhatsApp Image 2026-05-06 at 2 39 07 AM" src="https://github.com/user-attachments/assets/ce71209e-993a-440f-a4cd-6fcc2d8f4358" />

<img src="C:\Users\HT\OneDrive\Desktop\Portfolio-Generator-main\WhatsApp Image 2026-05-06 at 2.34.11.jpeg" alt="Description" width="400">
2. GitHub Actions showing `test` and `build-docker` jobs green.
3. Live endpoint response:
```bash
curl http://13.206.218.164:5000/health
```

## 8. Challenges and Solutions
1. **Challenge:** App originally existed as a frontend-only React project and did not meet Flask API rubric.  
   **Solution:** Added Flask backend (`app.py`) with required endpoints, status codes, CORS, and tests.

2. **Challenge:** Need reproducible cloud run and automated validation.  
   **Solution:** Added Dockerfile and GitHub Actions workflow with test gate and live container health check.
3.**Challenge:**User Interface was not clear enough that hindered the Key generation and overall deployement.
**Solution:** We read multiple AWS for easy understanding and implementing the deployement steps.
4.**Challenge**: Instance broken deployment
**Solution**: Changed the overall file structure.
5.**Challenge:**Permisison denied Api
**Solution:** We re-analyzed and re-applied the nessecsary steps in AWS to change the instance back.
6.**Challenege:**Server Initilized and deployment not proceeded
**Solution:** We re-tested through curl comands and test comands for analyzing the specificpoint of error.
7.**Challeneges:** Connecting Server and backend
**Solution:**:The server and backend werent able to connect,so we had t o choose another method that is g
## 9. Lessons Learned
1. Building deployment-ready software needs API design, test automation, and infrastructure setup together.
2. `needs: test` in GitHub Actions prevents deploying unverified code.
3. Docker `--restart=always` is critical for resilience after instance reboot.
4. Security groups directly control accessibility even when app is running correctly.
5. A clear deployment document makes troubleshooting and demo preparation much easier.
6.Ubuntu on oracle may causes problems for actual deployment as due to access rights.
