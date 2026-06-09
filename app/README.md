# Orders API

Small FastAPI service used by the SRE automation demo.

## Local Run

```bash
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```

Health endpoints:

- `GET /health`
- `GET /ready`
- `GET /metrics`

## Container Build

```bash
docker build -t orders-api:local app
docker run --rm -p 8080:8080 orders-api:local
```
