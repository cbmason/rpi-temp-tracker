#!/bin/bash
set -e

# Substitute env vars into dashboard template
envsubst '${LOCATION}' \
  < /etc/grafana/provisioning/dashboards/dashboard.template.json \
  > /etc/grafana/provisioning/dashboards/dashboard.json

exec /run.sh