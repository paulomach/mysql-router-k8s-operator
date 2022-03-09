build:
	charmcraft pack

deploy-local:
	juju deploy ./mysqlrouter-operator_ubuntu-20.04-amd64.charm --resource mysql-router-image=mysql/mysql-router:8.0

remove:
	juju remove-application mysqlrouter-operator

watch-test-log:
	juju debug-log -m $(juju models|grep test-charm|awk '{ print $1 }')