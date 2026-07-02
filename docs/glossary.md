# Glossary

<!-- toc:start -->
- [Airbyte](#airbyte)
- [Connector](#connector)
- [CI](#ci)
- [DAG](#dag)
- [Deployment environment](#deployment-environment)
- [dbt profile](#dbt-profile)
- [dbt target](#dbt-target)
- [Environment secret](#environment-secret)
- [Production target](#production-target)
- [Protected branch](#protected-branch)
- [Relation](#relation)
- [Source of truth](#source-of-truth)
- [Target schema](#target-schema)
<!-- toc:end -->

## Airbyte

An open-source data replication platform and managed service for moving data from sources to destinations. In these notes, distinguish a full Airbyte instance from PyAirbyte, which runs connector-powered data extraction from Python without the full server.

## Connector

A component that knows how to read from a source system or write to a destination system. In Airbyte, connectors are the reusable building blocks behind sources, destinations, and connections.

## CI

Continuous integration. In these notes, CI usually means an automated check that runs against a proposed change before merge, such as a GitHub Actions job that builds and tests modified dbt resources in an isolated target schema.

## DAG

A directed acyclic graph. In dbt learning notes, this usually refers to the dependency graph between sources, models, seeds, snapshots, tests, and downstream resources.

## Deployment environment

A named deployment target controlled by an automation platform. In GitHub Actions, an environment can hold environment-scoped secrets and deployment protection rules such as required reviewers, wait timers, or branch restrictions.

## dbt profile

A named connection configuration in `profiles.yml`. A dbt project can point to a profile by name, and that profile can contain multiple targets such as `dev` and `prod`.

## dbt target

The active output inside a dbt profile. In dbt Core, target values come from `profiles.yml` and are available in Jinja through the `target` variable, including values such as `target.name`, `target.schema`, and adapter-specific connection fields.

## Environment secret

A secret scoped to a named automation environment. In GitHub Actions, a job that references a protected environment cannot access that environment's secrets until the protection rules pass.

## Production target

The dbt target that writes production data for end users. It should normally be used by controlled automation with production-scoped credentials, not by a developer's local shell.

## Protected branch

A GitHub branch with rules that must pass before changes can be merged or pushed, such as pull request review, required status checks, merge queue, or restrictions on who can push.

## Relation

A database object reference such as a table or view, often including database, schema, and identifier/name components.

## Source of truth

The authoritative reference for a claim. For product behavior, prefer official documentation over rough notes, memory, generated text, or unofficial articles.

## Target schema

The default schema or dataset where dbt builds relations for the active target. By default, custom schema configs are appended to this value, which helps keep each developer's work isolated.
