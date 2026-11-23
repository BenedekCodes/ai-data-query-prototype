"""Initialize the disposable local Polaris catalog."""

import json
import os
from urllib.parse import urlencode
from urllib.error import HTTPError
from urllib.request import Request, urlopen


BASE_URL = "http://polaris:8181"


def request(path: str, data: bytes | None, headers: dict[str, str], method: str = "POST") -> dict:
    req = Request(BASE_URL + path, data=data, headers=headers, method=method)
    with urlopen(req, timeout=30) as response:
        body = response.read()
    return json.loads(body) if body else {}


def main() -> None:
    credentials = urlencode(
        {
            "grant_type": "client_credentials",
            "client_id": os.environ["POLARIS_CLIENT_ID"],
            "client_secret": os.environ["POLARIS_CLIENT_SECRET"],
            "scope": "PRINCIPAL_ROLE:ALL",
        }
    ).encode()
    token = request(
        "/api/catalog/v1/oauth/tokens",
        credentials,
        {"Content-Type": "application/x-www-form-urlencoded"},
    )["access_token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Polaris-Realm": "POLARIS",
    }
    try:
        request("/api/management/v1/catalogs/explorer", None, headers, method="GET")
    except HTTPError as error:
        if error.code != 404:
            raise
    else:
        print("Polaris catalog already exists.")
        return

    catalog = {
        "catalog": {
            "name": "explorer",
            "type": "INTERNAL",
            "readOnly": False,
            "properties": {"default-base-location": "s3://explorer"},
            "storageConfigInfo": {
                "storageType": "S3",
                "allowedLocations": ["s3://explorer"],
                "endpoint": "http://storage:9000",
                "endpointInternal": "http://storage:9000",
                "pathStyleAccess": True,
                "region": "us-west-2",
            },
        }
    }
    request("/api/management/v1/catalogs", json.dumps(catalog).encode(), headers)
    request(
        "/api/management/v1/catalogs/explorer/catalog-roles/catalog_admin/grants",
        json.dumps({"type": "catalog", "privilege": "CATALOG_MANAGE_CONTENT"}).encode(),
        headers,
        method="PUT",
    )
    print("Polaris catalog created.")


if __name__ == "__main__":
    main()
