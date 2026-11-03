"""Authentication interface for enrolled endpoint agents."""
class AuthenticationService:
    def authenticate_agent(self, api_key: str) -> bool:
        raise NotImplementedError
