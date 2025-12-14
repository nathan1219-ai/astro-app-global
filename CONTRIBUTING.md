# Contributing Guide

## Branch & Commit
- Default branch: `main`
- Use feature branches for larger changes and open a PR
- Commit message types: `feat`, `fix`, `chore`, `docs`, `refactor`, `perf`, `test`

## Frontend
- Node 18, npm
- Dev: `npm run dev`
- Build: `npm run build`

## Backend
- Python 3.10, `requirements.txt`
- Dev: `uvicorn app:app --host 127.0.0.1 --port 8000 --reload`

## Environment
- Do not commit secrets
- Use `.env` files locally and CI/environment secrets in production

