"""HTTP communication with the central DLP server."""

import requests

from common.contracts import API_PREFIX


class ServerClient:
    def __init__(self, server_url):
        self.base_url = server_url.rstrip("/") + API_PREFIX

    def get_policies(self):
        response = requests.get(f"{self.base_url}/policies", timeout=5)
        response.raise_for_status()
        return response.json()

    def send_event(self, event):
        response = requests.post(f"{self.base_url}/events", json=event, timeout=5)
        response.raise_for_status()
        return response.json()
