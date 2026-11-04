# DLP

A small Data Loss Prevention project with two parts:

- **Agent** — runs on Windows and monitors clipboard and USB activity.
- **Server** — manages policies and provides the web dashboard.

The server is the source of truth for policies. The agent keeps a local JSON cache so it can use the latest valid policies while offline.

## Project structure

```text
agent/
  main.py
  clipboard.py
  usb.py
  policy_cache.py
server/
  app.py
  policies.json
  templates/
    index.html
  static/
    style.css
    app.js
requirements.txt
```

## Setup

```bash
python -m venv .venv
# Activate the virtual environment
pip install -r requirements.txt
```

Run the server:

```bash
python -m server.app
```

Clipboard and USB monitoring are initial development targets. Additional monitoring channels can be added as separate agent modules.
