const $ = (selector) => document.querySelector(selector);

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Request failed");
  return data;
}

function renderPolicies(document) {
  $("#policy-version").textContent = document.policy_version;
  const policies = document.policies || [];
  $("#policy-count").textContent = policies.filter((p) => p.enabled).length;
  $("#policies").innerHTML = policies.length ? policies.map((p) => `
    <tr>
      <td><strong>${escapeHtml(p.name)}</strong><small>${escapeHtml(p.id)}</small></td>
      <td>${escapeHtml(p.channel)}</td>
      <td>${escapeHtml((p.conditions.sensitivity || []).join(", ") || "Any")}</td>
      <td><span class="action ${p.action.toLowerCase()}">${escapeHtml(p.action)}</span></td>
      <td>${p.enabled ? "Enabled" : "Disabled"}</td>
      <td>${p.enabled ? `<button class="button-secondary" data-disable="${escapeHtml(p.id)}">Disable</button>` : "—"}</td>
    </tr>`).join("") : '<tr><td colspan="6">No policies created yet.</td></tr>';
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}

async function loadDashboard() {
  try {
    const policies = await api("/api/v1/policies");
    renderPolicies(policies);
  } catch (error) {
    $("#policy-message").textContent = error.message;
  }
  try {
    const events = await api("/api/v1/events");
    const rows = events.events || [];
    $("#event-count").textContent = rows.length;
    $("#events").textContent = rows.length
      ? rows.map((event) => `${event.timestamp} · ${event.channel} · ${event.decision}`).join("\\n")
      : "No incidents recorded yet.";
  } catch (_) {
    $("#event-count").textContent = "—";
    $("#events").textContent = "Event API is not connected yet.";
  }
}

$("#policy-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const policy = {
    name: $("#policy-name").value.trim(),
    enabled: true,
    channel: $("#policy-channel").value,
    conditions: { sensitivity: [$("#policy-severity").value] },
    action: $("#policy-action").value
  };
  try {
    await api("/api/v1/policies", { method: "POST", body: JSON.stringify(policy) });
    $("#policy-form").reset();
    $("#policy-message").textContent = "Policy saved on the server.";
    await loadDashboard();
  } catch (error) {
    $("#policy-message").textContent = error.message;
  }
});

$("#policies").addEventListener("click", async (event) => {
  const button = event.target.closest("[data-disable]");
  if (!button) return;
  try {
    await api(`/api/v1/policies/${encodeURIComponent(button.dataset.disable)}`, { method: "DELETE" });
    await loadDashboard();
  } catch (error) {
    $("#policy-message").textContent = error.message;
  }
});

loadDashboard();
