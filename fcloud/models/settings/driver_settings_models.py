from dataclasses import dataclass


@dataclass()
class DropboxAuth:
    token: str
    app_secret: str
    app_key: str
