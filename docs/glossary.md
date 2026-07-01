# Glossary

<!-- toc:start -->
- [Airbyte](#airbyte)
- [Connector](#connector)
- [DAG](#dag)
- [Relation](#relation)
- [Source of truth](#source-of-truth)
<!-- toc:end -->

## Airbyte

An open-source data replication platform and managed service for moving data from sources to destinations. In these notes, distinguish a full Airbyte instance from PyAirbyte, which runs connector-powered data extraction from Python without the full server.

## Connector

A component that knows how to read from a source system or write to a destination system. In Airbyte, connectors are the reusable building blocks behind sources, destinations, and connections.

## DAG

A directed acyclic graph. In dbt learning notes, this usually refers to the dependency graph between sources, models, seeds, snapshots, tests, and downstream resources.

## Relation

A database object reference such as a table or view, often including database, schema, and identifier/name components.

## Source of truth

The authoritative reference for a claim. For product behavior, prefer official documentation over rough notes, memory, generated text, or unofficial articles.
