# mysql-router-k8s-operator

## Description

Charmed operator for mysql-router under k8s.

## Usage

Just run `juju deploy mysql-router-k8s-operator` to deploy the charm.

## Relations

Relations are defined in `metadata.yaml` are:

* Requires: mysql-db
* Provides: mysql-db

## OCI Images

Currently using the following OCI images:

* mysql-router: mysql/mysql-router:8.0

## Contributing

Please see the [Juju SDK docs](https://juju.is/docs/sdk) for guidelines on
enhancements to this charm following best practice guidelines, and
[CONTRIBUTING.md](https://github.com/paulomach/mysql-router-k8s-operator/blob/main/CONTRIBUTING.md)
for developer guidance.
