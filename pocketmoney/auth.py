import os

from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials
from .settings import CLIENT_SECRET_FILE, SCOPES
import argparse


if __name__ == "__main__":
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'sheets.pocketmoney.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        secret_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), CLIENT_SECRET_FILE
        )
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            secret_file, SCOPES
        )
    return credentials
