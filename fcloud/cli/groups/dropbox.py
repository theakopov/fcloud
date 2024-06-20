import configparser
import requests
from os import environ
from textwrap import dedent

from ...drivers.dropbox.config_error import DropboxConfigError
from ...exceptions.base_error import FcloudError

from ...drivers.dropbox.models import TokenData
from ...drivers.dropbox.models import DropboxAuth

from ...utils.config import edit_config
from ...utils.config import get_config_data
from ...utils.error import echo_error


class Dropbox:
    def __init__(self):
        self._auth_link = "https://www.dropbox.com/oauth2/authorize?client_id={}&token_access_type=offline&response_type=code"

    def get_token(self):
        config = configparser.ConfigParser()
        config.read(environ.get("FCLOUD_CONFIG_PATH"))
        app_key = get_config_data("DROPBOX", "app_key")

        if not app_key:
            echo_error(DropboxConfigError.app_key_empty_error)
        token = input(
            dedent(
                f"""
        Get the token at this link: {self._auth_link.format(app_key)}\n
        Your token: """
            )
        )

        auth = DropboxAuth(
            token=token,
            app_secret=get_config_data(
                "DROPBOX", "app_secret", DropboxConfigError.app_secret_error
            ),
            app_key=app_key,
        )
        access_token = self._get_access_token(auth)
        edit_config("DROPBOX", "token", access_token.refresh_token)

    def _get_access_token(self, auth: DropboxAuth) -> TokenData:
        try:
            response = requests.post(
                "https://api.dropboxapi.com/oauth2/token",
                data={"code": auth.token, "grant_type": "authorization_code"},
                auth=(
                    auth.app_key,
                    auth.app_secret,
                ),
            )
        except Exception as e:
            echo_error(("Api error", str(e)))
        result = response.json()

        if not result.get("error"):
            return TokenData(**result)
        else:
            echo_error(
                (
                    result.get("error", FcloudError.uknown_error),
                    result.get(
                        "error_description", "No error description"
                    ).capitalize(),
                )
            )
