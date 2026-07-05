# Load .env so LOCATION is available for host-side templating.
# (`-include` avoids a hard error before .env exists.)
-include .env
export

DASHBOARD_TEMPLATE := grafana/dashboard.template.json
DASHBOARD_OUT      := grafana/provisioning/dashboards/dashboard.json

.PHONY: render up down logs

# Substitute ${LOCATION} into the dashboard JSON that Grafana provisions.
render:
	@test -n "$(LOCATION)" || { echo "LOCATION not set - copy env_template to .env and fill it in"; exit 1; }
	@command -v envsubst >/dev/null || { echo "envsubst not found - install gettext-base (sudo apt install gettext-base)"; exit 1; }
	@mkdir -p $(dir $(DASHBOARD_OUT))
	envsubst '$${LOCATION}' < $(DASHBOARD_TEMPLATE) > $(DASHBOARD_OUT)
	@echo "Rendered dashboard for LOCATION=$(LOCATION)"

up: render
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f
