#!/usr/bin/env python3
# Copyright 2021 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""MySQL-Router charm."""

import logging

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)


class MysqlRouterOperatorCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.mysqlrouter_pebble_ready, self._on_mysqlrouter_pebble_ready)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_mysqlrouter_pebble_ready(self, event):
        """Define and start a workload using the Pebble API."""
        # Get a reference the container attribute on the PebbleReadyEvent
        container = event.workload
        # Define an initial Pebble layer configuration
        pebble_layer = self._mysqlrouter_layer()
        # Add initial Pebble config layer using the Pebble API
        container.add_layer("mysqlrouter", pebble_layer, combine=True)
        # Autostart any services that were defined with startup: enabled
        container.autostart()
        # Learn more about statuses in the SDK docs:
        # https://juju.is/docs/sdk/constructs#heading--statuses
        self.unit.status = ActiveStatus()

    def _mysqlrouter_layer(self) -> dict:
        """Returns a Pebble configuration layer for mysqlrouter."""
        return {
            "summary": "mysqlrouter layer",
            "description": "pebble config layer for mysqlrouter",
            "services": {
                "mysqlrouter": {
                    "override": "replace",
                    "summary": "mysqlrouter",
                    "command": "sleep 3600",
                    "startup": "enabled",
                    "environment": {
                        "MYSQL_PORT": self.model.config["mysql_port"],
                        "MYSQL_HOST": self.model.config["mysql_host"],
                        "MYSQL_USER": self.model.config["mysql_user"],
                        "MYSQL_PASSWORD": self.model.config["mysql_password"],
                    },
                }
            },
        }

    def _on_config_changed(self, event) -> None:
        """Handle config-changed event."""
        container = self.unit.get_container("mysqlrouter")

        layer = self._mysqlrouter_layer()

        plan = container.get_plan()

        if plan.services != layer["services"]:
            logger.info("Config changed")
            container.add_layer("mysqlrouter", layer, combine=True)

            if container.get_service("mysqlrouter").is_running():
                container.stop("mysqlrouter")

            container.start("mysqlrouter")
            logging.info("mysqlrouter restarted")

        self.unit.status = ActiveStatus()


if __name__ == "__main__":
    main(MysqlRouterOperatorCharm)
