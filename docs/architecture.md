# Architecture

## Ownership
- The **Server** owns policy creation, updates, deletion/disablement, and authoritative storage.
- The **Agent** stores only a local cache of the latest valid policy document.
- The dashboard communicates with the Server API; it does not communicate directly with agents.

## Agent flow
1. A channel adapter observes an activity (clipboard or USB).
2. Detection inspects metadata/content locally and returns findings.
3. The policy engine evaluates the activity against the cached policies.
4. Enforcement applies the decision where supported.
5. A normalized event is sent to the server. Raw sensitive content must never be included.

## Policy synchronization
The agent checks the server policy version, downloads policies only when changed, validates the document, and atomically replaces its cache. If the server is unavailable, it uses the last valid cache.

## Extensibility
Each monitoring channel implements the shared channel adapter interface. Future channels (for example email or file transfer) should not require changes to the policy store or event contract.

## Branch ownership
- `main`: shared baseline, contracts, and architecture.
- `Agent`: Windows endpoint agent skeleton.
- `Server`: Flask API, policy store, event storage, and dashboard skeleton.
