async function loadEvents() {
  const body = document.querySelector("#events");
  try {
    const response = await fetch("/api/v1/events");
    const events = await response.json();
    body.innerHTML = "";
    if (!events.length) {
      body.innerHTML = '<tr><td colspan="5">No events received yet.</td></tr>';
      return;
    }
    for (const event of events) {
      const row = document.createElement("tr");
      const values = [
        event.timestamp || "",
        event.agent_id || "",
        event.channel || "",
        (event.findings || []).map(item => item.type + " (" + item.count + ")").join(", ") || "None",
        event.decision || ""
      ];
      for (const value of values) {
        const cell = document.createElement("td");
        cell.textContent = value;
        row.appendChild(cell);
      }
      body.appendChild(row);
    }
  } catch {
    body.innerHTML = '<tr><td colspan="5">Could not load events.</td></tr>';
  }
}
document.querySelector("#refresh").addEventListener("click", loadEvents);
loadEvents();
