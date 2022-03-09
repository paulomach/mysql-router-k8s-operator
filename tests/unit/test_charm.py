# Copyright 2021 Canonical Ltd.
# See LICENSE file for licensing details.

import unittest
from unittest.mock import Mock

from ops.model import ActiveStatus
from ops.testing import Harness

from charm import MysqlRouterOperatorCharm


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = Harness(MysqlRouterOperatorCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()
        self.harness.model.app
        self.maxDiff = None

    def test_mysqlrouter_pebble_ready(self):
        # Check the initial Pebble plan is empty
        initial_plan = self.harness.get_container_pebble_plan("mysqlrouter")
        self.assertEqual(initial_plan.to_yaml(), "{}\n")

        # updated config
        self.harness.update_config(
            {"mysql_host": "localhost", "mysql_user": "root", "mysql_password": "password"}
        )

        # Expected plan after updated config
        expected_plan = {
            "services": {
                "mysqlrouter": {
                    "override": "replace",
                    "summary": "mysqlrouter",
                    "command": "sleep 3600",
                    "startup": "enabled",
                    "environment": {
                        "MYSQL_PORT": 3306,
                        "MYSQL_HOST": "localhost",
                        "MYSQL_USER": "root",
                        "MYSQL_PASSWORD": "password",
                    },
                }
            },
        }
        # Get the mysqlrouter container from the model
        container = self.harness.model.unit.get_container("mysqlrouter")
        # Emit the PebbleReadyEvent carrying the mysqlrouter container
        self.harness.charm.on.mysqlrouter_pebble_ready.emit(container)
        # Get the plan now we've run PebbleReady
        updated_plan = self.harness.get_container_pebble_plan("mysqlrouter").to_dict()
        # Check we've got the plan we expected

        self.assertEqual(expected_plan, updated_plan)

        # Check the service was started
        service = self.harness.model.unit.get_container("mysqlrouter").get_service("mysqlrouter")
        self.assertTrue(service.is_running())
        # Ensure we set an ActiveStatus with no message
        self.assertEqual(self.harness.model.unit.status, ActiveStatus())
