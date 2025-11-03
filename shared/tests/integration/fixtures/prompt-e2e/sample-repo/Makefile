.PHONY: dev api web

dev:
	$(MAKE) -j web api

web:
	cd apps/web && npm run dev

api:
	cd services/api && uvicorn app:app --reload --port 8001
