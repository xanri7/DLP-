# DLP — Data Loss Prevention

A lightweight Python prototype for identifying sensitive information in files, applying configurable allow/warn/block policies, and recording security events through a small Flask server and web dashboard.

The project is designed as a simple client-server application:
- **Agent** runs on an endpoint, inspects files, evaluates policy, and invokes the configured enforcement adapter.
- **Server** provides a Flask API, stores events, and serves a dashboard for reviewing detections and policy outcomes.
- **Common** contains data structures shared by the agent and server.

## Project structure

```text
agent/
  main.py
  pipeline.py
  channels/
    base.py                # Shared channel interface
    clipboard.py           # Clipboard channel
    usb.py                 # USB extraction channel
  detection/
    scanner.py
    rules.py
  policy/
    engine.py              # Evaluates locally cached policies
    cache.py               # Local versioned policy cache
  sync/
    client.py              # Server communication
    local_store.py         # Offline cache and event queue
server/
  app.py
  routes/
    policies.py            # Policy API
    events.py               # Event API
    agents.py               # Agent heartbeat API
  policy/
    manager.py              # Central policy management
    store.py                # Authoritative policy storage
  database/
    events.py               # Event persistence
  services/
    synchronization.py
    authentication.py
  templates/                # Dashboard templates
  static/                   # Dashboard CSS and JavaScript
common/
  schemas.py               # Shared event and result structures
tests/
  test_detection.py
  test_policy.py
  test_api.py
docs/
  architecture.md
```

## Architecture

The project uses a modular Windows endpoint agent and a central Linux server:
- **Monitoring channels:** the initial channels are clipboard and USB. Each channel is an adapter that feeds the shared DLP pipeline.
- **Policy authority:** policy creation, editing, versioning, and central storage belong to the server.
- **Agent policy cache:** the agent downloads versioned policies and keeps a local cache for offline operation; it does not manage policies.
- **Synchronization:** the agent checks policy versions, uploads events, sends heartbeats, and queues events locally while offline.

See [docs/architecture-v2.md](docs/architecture-v2.md) for the data flow and API outline.

## Current status

This repository is a **starter scaffold**. The files define the intended component boundaries; they do not yet implement a complete DLP system. In particular, file monitoring is not the same as preventing uploads, and a policy decision of `BLOCK` does not prove an operation was blocked. Enforcement must be implemented and tested for the target operating system and transfer path.

## Development setup

Requires Python 3.11 or newer.

```bash
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
- Linux/macOS: `source .venv/bin/activate`

Install the small set of application dependencies:

```bash
python -m pip install -r requirements.txt
```

Run tests with:

```bash
python -m pytest
```

The server entry point will be `python -m server.app` once the Flask application is implemented.

## Team workflow

- `main` is the shared stable branch.
- `Agent` is for endpoint agent, detection, policy, and enforcement work.
- `Server` is for the Flask API, event storage, and dashboard.
- Use feature branches and pull requests to merge reviewed changes into `main`.
- Keep shared structures in `common/schemas.py` and coordinate changes with both teams.

## Security notes

- Use synthetic test data; do not commit real sensitive files or credentials.
- Keep local secrets in an untracked `.env` file.
- Avoid writing sensitive file contents or matched secret values to logs.
- Treat enforcement results as untrusted until the underlying control has been verified.
