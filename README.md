# Flask Application

Simple Flask app with two routes:

- `/` -> `Hello, World!`
- `/greet/<name>` -> personalized greeting

## Project Structure

- `flask-application.py` - main Flask app
- `requirements.txt` - Python dependencies
- `Dockerfile` - container image definition

## Prerequisites

- Python 3.12 (or compatible)
- `pip`
- Optional: Docker

## Run Locally

1. Create and activate virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip3 install -r requirements.txt
```

3. Start the app:

```bash
python3 flask-application.py
```

App runs on `http://127.0.0.1:9000`.

## Test Endpoints

```bash
curl http://127.0.0.1:9000/
curl http://127.0.0.1:9000/greet/Manish
```

## Run with Docker

1. Build image:

```bash
docker build -t flask-application .
```

2. Run container:

```bash
docker run --rm -p 9000:9000 flask-application
```

Open `http://127.0.0.1:9000`.

## Push to Amazon ECR

Prerequisite (authenticate Docker to ECR):

```bash
aws ecr get-login-password --region <aws-region> | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com
```

Build and push image:

```bash
docker push <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<image-name>:latest
```
