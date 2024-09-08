from os import getenv

from google.cloud import secretmanager


def get_secret(secret_name):
    secretManagerClient = secretmanager.SecretManagerServiceClient()
    project_id = getenv("project_id")
    request = {"name": f"projects/{project_id}/secrets/{secret_name}/versions/latest"}
    response = secretManagerClient.access_secret_version(request=request)
    secret_string = response.payload.data.decode("UTF-8")
    return secret_string