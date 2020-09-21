help:
	@echo
	@echo
	@echo "  -----------------------------------------------------------------------------------------------------------"
	@echo "  Box Platform Event Stream Poller Makefile"
	@echo "  -----------------------------------------------------------------------------------------------------------"
	@echo "  dev        to build the development Docker image""
	@echo "  prod       to build the production Docker image""
	@echo
	@echo

dev:
    docker-compose -f docker-compose.dev.yml down
	docker-compose -f docker-compose.dev.yml up --build

prod:
    docker-compose down
	docker-compose up --build