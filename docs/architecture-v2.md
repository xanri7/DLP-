# DLP architecture and shared contracts

## Components

- **Windows Agent:** clipboard and USB channels, detection, local policy evaluation, enforcement, policy cache, and synchronization.
- **Linux Server:** authoritative JSON policy management, REST API, event persistence, agent status, and web dashboard.
- **Web Dashboard:** HTML/CSS/JavaScript served by Flask. It talks only to the server REST API; it does not connect directly to endpoint agents.
- **Common contracts:** `common/schemas.py` and the JSON Schema files define the shared payload formats and allowed values.

## Policy authority and synchronization

The server is the only policy authority. Administrators create and edit policies in the dashboard. The server validates and stores a JSON document with an incrementing `policy_version`. The agent periodically checks the version, downloads a newer document, validates it, and replaces its local cache. If offline, the agent continues with its last valid cache and queues events for later upload.

Example policy document:

```json
{
  "policy_version": 1,
  "policies": [
    {
      "id": "POL-001",
      "name": "Block high-sensitivity USB transfers",
      "enabled": true,
      "channel": "usb",
      "conditions": {"sensitivity": ["high", "critical"]},
      "action": "BLOCK"
    }
  ]
}
```

## Shared vocabulary

- Channels: `clipboard`, `usb`
- Decisions: `ALLOW`, `WARN`, `BLOCK`
- Severities: `low`, `medium`, `high`, `critical`
- Enforcement statuses: `SUCCESS`, `FAILED`, `NOT_REQUIRED`
- Timestamps: ISO 8601 UTC strings
- API prefix: `/api/v1/`
- Payload encoding: UTF-8 JSON

Do not invent alternate spellings or casing in individual modules. Every channel emits the same normalized event structure.

## Event contract

Every event contains `event_id`, `agent_id`, `channel`, `timestamp`, `event_type`, `findings`, `decision`, `policy_id`, and `enforcement_status`. Findings contain a type, severity, and count. Do not send raw clipboard text or full sensitive file contents to the server.

## API outline

- `GET /api/v1/policies/version` — current policy version.
- `GET /api/v1/policies` — current JSON policy document for agents.
- `POST /api/v1/policies` — create policy from dashboard.
- `PUT /api/v1/policies/{id}` — update policy.
- `DELETE /api/v1/policies/{id}` — disable policy (soft delete).
- `POST /api/v1/events` — ingest agent event.
- `GET /api/v1/events` — list recent events for dashboard.
- `POST /api/v1/agents/heartbeat` — agent heartbeat (planned).

## Dashboard

The Flask server serves the dashboard at `/`. HTML provides the page structure, CSS styles it, and JavaScript calls the REST API to display and manage policies and review events. The browser must not access the agent's local store directly.

## Security and implementation status

Use HTTPS and authenticate both agents and administrators before deployment. The current policy CRUD endpoints are a development scaffold and do not yet enforce authentication or authorization; do not expose them to an untrusted network. Protect the local policy cache and validate downloaded documents before replacing it.

Monitoring/detection is not the same as enforcement: each Windows control must be implemented and tested for its specific operation. The clipboard and USB channel files remain integration points until their Windows monitoring and enforcement code is completed.
