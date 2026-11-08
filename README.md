# DLP System

> Project scaffold only. No application functionality is implemented yet.

## Architecture placeholders

- **Agent:** Windows endpoint component. Future responsibilities: channel monitoring, local detection, policy caching, enforcement, and event reporting.
- **Server:** Central Flask-based web application. Future responsibilities: policy management, agent communication, event ingestion, and dashboard delivery.
- **Common:** Shared contracts and naming conventions used by both Agent and Server.
- **Dashboard:** Browser-based interface served by the Server. Administrators will open it using the Server's URL.
- **Event database:** Server-side persistent storage for normalized event metadata. Raw sensitive content should not be transmitted or stored.

## Planned communication

- Agent periodically polls the Server for the latest policy version.
- Server returns updated policies only when the Agent's cached version is outdated.
- Agent stores the received policy document in its local cache.
- Agent submits normalized event metadata to the Server.
- Server stores events in its database and exposes them to the dashboard.

## Planned API placeholders

- `GET /api/v1/policies` — retrieve the current policy document or updates.
- `POST /api/v1/events` — submit an event from an Agent.
- `GET /api/v1/events` — retrieve events for the dashboard.

## Current status

This repository contains structure and TODO placeholders only. Implementations, database schema, polling logic, API routes, monitoring, detection, enforcement, and dashboard behavior are intentionally left for development.
