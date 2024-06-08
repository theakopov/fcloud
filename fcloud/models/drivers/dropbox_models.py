from dataclasses import dataclass


@dataclass(frozen=True)
class TokenData:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str
    uid: int
    account_id: str
