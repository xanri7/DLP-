# DLP

A first prototype of a Data Loss Prevention system.

## Components

- **Agent:** monitors clipboard changes and removable-drive connection events on Windows.
- **Detection:** checks clipboard text locally for basic sensitive-data patterns. Raw content is not sent to the server.
- **Policy:** downloads policies from the server and keeps a local JSON cache for offline use.
- **Server:** stores policies, receives agent events, and serves a basic dashboard.

## Run the server

```bash
python -m venv .venv
pip install -r requirements.txt
python -m server.app
```

Open http://127.0.0.1:5000.

## Run the agent

In a second terminal:

```bash
set DLP_SERVER_URL=http://127.0.0.1:5000
python -m agent.main
```

On Windows, install the requirements in the same environment. Clipboard monitoring uses the Windows clipboard; USB monitoring currently detects removable-drive connection and removal.

## Current prototype limits

- USB file-copy/extraction detection and USB blocking are not implemented yet; the current USB channel detects device connection changes.
- Clipboard decisions are detected and reported, but full OS-level prevention is not implemented yet.
- Events are held in server memory and reset when the server restarts.
- Policies are edited through the `PUT /api/v1/policies` endpoint; a policy editor in the dashboard can be added next.
- Detection patterns are basic examples and need to be refined for the data types the project will protect.

The project is intentionally kept small so these capabilities can be built incrementally.
