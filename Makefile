.PHONY: run db-interactive

run:
	@docker compose up --build

db-interactive:
	@docker exec -it face-tracker-postgres psql -U tracker -d tracker

stop:
	@docker compose down