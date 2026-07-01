# Airbyte Notes

Use this section for Airbyte data replication, connectors, deployment, and local learning workflows.

<!-- toc:start -->
- [Core concepts](#core-concepts)
- [Review habits](#review-habits)
<!-- toc:end -->

## Core concepts

- [Running Airbyte from a Mac](running-on-mac.md)

## Review habits

When adding Airbyte notes, distinguish between:

- Airbyte Cloud, self-managed Airbyte Core, and hybrid or enterprise deployments;
- a full Airbyte instance with a web UI, scheduler, API, state, and secrets, versus a PyAirbyte script or notebook;
- deployment mechanics such as Docker, Kubernetes, Helm, and `abctl`, versus connector configuration and sync behavior;
- local evaluation choices and production choices, especially around credentials, persistence, logs, storage, and upgrades.
