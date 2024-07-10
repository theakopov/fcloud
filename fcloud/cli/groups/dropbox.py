import requests
import os
from textwrap import dedent

from ...exceptions.base_errors import FcloudError
from ...exceptions.exceptions import FcloudException
from ...exceptions.config_errors import ConfigError

from ...drivers.dropbox.models import TokenData
from ...drivers.dropbox.models import DropboxAuth

from ...utils.config import edit_config
from ...utils.config import get_field


class Dropbox:
    def __init__(self):
        self._auth_link = "https://www.dropbox.com/oauth2/authorize?client_id={}&token_access_type=offline&response_type=code"

    def get_token(self):
        """Will generate a link, to get a permanent token
        that fcloud will use to receive and upload files to the cloud"""
        title, message = ConfigError.field_error
        error = (title, message.format("app_key", os.environ["FCLOUD_CONFIG_PATH"]))
        app_key = get_field("app_key", error, section="DROPBOX")

        token = input(
            dedent(
                f"""\
                Get the token at this link: {self._auth_link.format(app_key)}\n
                Your token: """
            )
        )

        title, message = ConfigError.field_error
        error = (title, message.format("app_secret", os.environ["FCLOUD_CONFIG_PATH"]))
        app_secret = get_field("app_secret", error, section="DROPBOX")

        auth = DropboxAuth(
            token=token,
            app_secret=app_secret,
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
            raise FcloudException("Api error", str(e))
        result = response.json()

        if not result.get("error"):
            return TokenData(**result)
        else:
            raise FcloudException(
                result.get("error", FcloudError.uknown_error),
                result.get("error_description", "No error description").capitalize(),
            )
