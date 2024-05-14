import json
import os
from google.cloud import secretmanager
import flask
import functions_framework

# Retrieve Job-defined env vars
PROJECT_ID = os.getenv("PROJECT_ID", "neon-nexus-297211")
FRAME_KEY_SECRET = os.getenv("FRAME_KEY_SECRET", "frame-key")
FRAME_KEY_SECRET_VERSION = os.getenv("FRAME_KEY_SECRET_VERSION", 1)


@functions_framework.http
def hello(request: flask.Request) -> flask.typing.ResponseReturnValue:
    try:
        request_body = json.loads(request.data.decode("UTF-8"))
    except:
        request_body = json.loads("{}")

    print("Function Execution Started")
    print(request_body)

    api_key = get_secret_manager_secret_version()
    # print(f"Secret Value: {secret}.")

    # return f"Secret Value: {api_key}."
    return json.dumps(request_body)


def get_secret_manager_secret_version():
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{FRAME_KEY_SECRET}/versions/{FRAME_KEY_SECRET_VERSION}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
