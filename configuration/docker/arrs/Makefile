# -----------------------------------------------------------------------------
# Makefile — common operations for the *arr stack.
#
# Run `make` (or `make help`) to see all targets.
#
# Note: Makefile recipes are tab-indented (not spaces). Editors that auto-
# convert tabs will break this file. If you see "missing separator" errors,
# check your editor's whitespace settings.
# -----------------------------------------------------------------------------

.DEFAULT_GOAL := help

.PHONY: help bootstrap up down restart pull ps logs backup config \
        logs-prowlarr logs-sabnzbd logs-sonarr logs-radarr logs-lidarr logs-bazarr \
        logs-gluetun logs-qbittorrent logs-plundrio

help: ## show this help
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) \
		| awk -F':.*## ' '{printf "  %-18s %s\n", $$1, $$2}'

bootstrap: ## initialise .env and directory tree
	./bootstrap.sh

up: ## start the stack in detached mode
	docker compose up -d

down: ## stop and remove containers (volumes preserved)
	docker compose down

restart: ## restart all services
	docker compose restart

pull: ## pull latest images and recreate containers
	docker compose pull
	docker compose up -d

ps: ## show service status
	docker compose ps

logs: ## tail logs from all services
	docker compose logs -f --tail=100

config: ## render the resolved compose configuration
	docker compose config

backup: ## archive ./config to backups/
	./backup.sh

# Per-service log tails — useful when one app is misbehaving and the
# combined log stream is too noisy.
logs-prowlarr: ## tail Prowlarr logs
	docker compose logs -f --tail=100 prowlarr

logs-sabnzbd: ## tail SABnzbd logs
	docker compose logs -f --tail=100 sabnzbd

logs-sonarr: ## tail Sonarr logs
	docker compose logs -f --tail=100 sonarr

logs-radarr: ## tail Radarr logs
	docker compose logs -f --tail=100 radarr

logs-lidarr: ## tail Lidarr logs
	docker compose logs -f --tail=100 lidarr

logs-bazarr: ## tail Bazarr logs
	docker compose logs -f --tail=100 bazarr

# These services are commented out in docker-compose.yml by default. The
# targets are kept active so they're available the moment you enable the
# services; until then, `make logs-gluetun` will report "no such service".
logs-gluetun: ## tail gluetun logs (only when service is enabled)
	docker compose logs -f --tail=100 gluetun

logs-qbittorrent: ## tail qBittorrent logs (only when service is enabled)
	docker compose logs -f --tail=100 qbittorrent

logs-plundrio: ## tail plundrio (put.io) logs (only when service is enabled)
	docker compose logs -f --tail=100 plundrio
