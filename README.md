# DLP

A lightweight, extensible Data Loss Prevention system.

## Components
- **Agent**: Windows endpoint monitoring for clipboard and USB activity.
- **Server**: Central policy management, event ingestion, and web dashboard.
- **Shared contracts**: JSON schemas and API definitions used by both components.

The server is the source of truth for policies. Agents keep a validated local cache and can continue enforcing the last valid policy set while offline.

## Current scope
Clipboard monitoring and USB extraction are the initial channels. New channels should be added through independent adapters.

## Development
See [docs/architecture.md](docs/architecture.md). The `Agent` and `Server` branches contain the component skeletons.
