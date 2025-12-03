# Calculations API Backend

- FastAPI service providing authenticated calculator operations persisted in PostgreSQL.
- Docker Compose orchestrates API, Postgres, and pgAdmin for local usage.
- GitHub Actions pipeline runs automated tests, Trivy scan, and pushes Docker images.

---

## Requirements

- Docker Desktop or Docker Engine with Compose plugin.
- Python 3.12+ (only needed for running tests outside containers).
- Optional `.env` file to override `DATABASE_URL`, `JWT_SECRET_KEY`, etc.

---

## Quick Start


- Access endpoints:
	- API root → http://localhost:8000
	- Swagger → http://localhost:8000/docs
	- Health → http://localhost:8000/health
	- pgAdmin → http://localhost:5050 (user `admin@example.com`, password `admin`).
- Stop services with `Ctrl+C`; remove containers via `docker compose down`.

---

## Local Testing

- Create venv: `python3 -m venv .venv`.
- Activate: `source .venv/bin/activate`.
- Install deps: `pip install -r requirements.txt`.

---

## CI/CD

- Workflow file: `.github/workflows/test.yml`.
- Job order:
	- Test suite (unit, integration, e2e).
	- Trivy image scan (fails on HIGH/CRITICAL findings).
	- Docker Hub push (`shivajiburle/assignmentsqsqla:latest` + SHA tag).
- Required secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`.
- Capture screenshot of a green workflow for submission evidence.

---

## Submission Checklist

- Screenshot: Swagger request returning success (e.g., `/auth/login`).
- Screenshot: GitHub Actions run showing all jobs passed.
- Provide Docker Hub repository link.
- Include reflection document (`REFLECTION.md`).
