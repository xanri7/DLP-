# DLP architecture

## Responsibilities

- **Windows agent:** runs monitoring channels, detection, local policy evaluation, enforcement, and synchronization.
- **Linux server:** owns policy creation, editing, versioning, and central policy storage; receives events and serves the dashboard.
- **Agent policy cache:** stores the latest validated policy snapshot for offline use. The agent does not author or manage policies.

## Initial monitoring channels

- `clipboard`: monitor clipboard text changes and inspect content for sensitive information.
- `usb`: detect removable drives and inspect file-copy activity targeting them.

Each channel implements the shared interface in `agent/channels/base.py` and forwards normalized activity to the same detection → policy → enforcement → event pipeline. Future channels (email or browser uploads, for example) should add adapters rather than duplicate that pipeline.

## Policy synchronization

1. An administrator changes a policy through the server dashboard/API.
2. The server persists the change and increments the policy version.
3. The agent periodically checks the current version over HTTPS.
4. If a newer version exists, the agent downloads and validates the policy snapshot.
5. The agent replaces its local cache only after successful validation and persistence.
6. When offline, the agent uses its last valid cache and queues events for later upload.

## API outline

- `GET /api/v1/policies/version` — current policy version.
- `GET /api/v1/policies` — active policy snapshot for agents.
- `POST /api/v1/policies` — create policy (administrator authorization required).
- `PUT /api/v1/policies/{id}` — update policy.
- `DELETE /api/v1/policies/{id}` — disable policy.
- `POST /api/v1/events` — ingest agent events.
- `POST /api/v1/agents/heartbeat` — update agent status.

## Security and scope

Use HTTPS, authenticate agents, validate policy schemas and versions, protect the local cache, and avoid logging clipboard contents or matched sensitive values. Monitoring/detection is not the same as enforcement: each Windows control must be implemented and tested for its specific operation. These channel and service files are scaffolding, not completed monitoring or enforcement implementations.
