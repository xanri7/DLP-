# DLP System

A lightweight Data Loss Prevention prototype with a Windows endpoint Agent and a central Flask-based Server.

## Architecture

- **Agent:** Endpoint component responsible for channel monitoring, local detection, policy caching, enforcement, and event reporting.
- **Server:** Central Flask-based application responsible for policy management, agent communication, event ingestion, and dashboard delivery.
- **Common:** Shared contracts used by the Agent and Server.
- **Dashboard:** Browser-based interface served by the Server.
- **Event database:** Server-side storage for normalized event metadata. Raw sensitive content should not be transmitted or stored.

## Current implementation

- Clipboard channel prototype polls text clipboard contents every 2.5 seconds.
- Clipboard changes are represented as structured local `ChannelEvent` objects.
- `EventReport` contains metadata only; raw clipboard content is excluded from its serialized representation.
- The prototype prints clipboard content and event metadata locally for testing. Use dummy data during demonstrations.

Run the clipboard prototype from the repository root:

```bash
python -m pip install -r requirements.txt
python -m agent.channels.clipboard
```

Press Ctrl+C to stop monitoring.

## Planned communication

- Agent periodically polls the Server for the latest policy version.
- Server returns updated policies when the Agent's cached version is outdated.
- Agent stores the received policy document in its local cache.
- Agent submits normalized event metadata to the Server.
- Server stores events in its database and exposes them to the dashboard.

## Planned API

- `GET /api/v1/policies` — retrieve the current policy document or updates.
- `POST /api/v1/events` — submit an event from an Agent.
- `GET /api/v1/events` — retrieve events for the dashboard.

## Not implemented yet

Detection rules, policy evaluation, enforcement, USB monitoring, policy polling, Server API routes, database persistence, and dashboard behavior remain under development.
