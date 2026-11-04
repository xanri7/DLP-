"""Validated local policy cache placeholder."""

class PolicyCache:
    def load(self):
        raise NotImplementedError

    def save_atomically(self, policy_document):
        raise NotImplementedError
