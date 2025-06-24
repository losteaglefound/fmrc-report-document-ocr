backend-dev:
	uvicorn backend.api.main:app --reload

backend-prod:
	uvicorn backend.api.main:app --host 0.0.0.0 --port 8000

