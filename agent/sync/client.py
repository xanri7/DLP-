"""Server policy-version check, policy download, and event reporting client."""

class ServerClient:
    def get_policy_version(self):
        raise NotImplementedError

    def download_policies(self):
        raise NotImplementedError

    def submit_event(self, event):
        raise NotImplementedError
