from dataclasses import dataclass


@dataclass
class YandexAuth:
    token: str
    client_id: str
    client_secret: str
