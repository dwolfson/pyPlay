# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
#
# Unit tests for the Utils helper functions using the Pytest framework.
#
from datetime import time
import requests
import pytest
import warnings

from contextlib import contextmanager
from contextlib import nullcontext as does_not_raise

import egeria_client.client
from src.egeria_client.util_exp import (
    issue_get,
    issue_post,
    issue_data_post,
    issue_put,
    process_error_response,
    print_guid_list,
    get_last_guid,
    validate_user_id,
    validate_server_name,
    validate_guid,
    validate_name,
    validate_search_string,
    validate_public,
    validate_url,
    InvalidParameterException,
    PropertyServerException,
    RESTConnectionException,
)


@pytest.fixture()
def basic_server():
    platform = "https://127.0.0.1:9443"


class TestClient:
    # @pytest.mark.xfail
    @pytest.mark.parametrize(
        "url, user_id, status_code, expectation",
        [
            (
                "https://google.com",
                "garygeeke",
                404,
                pytest.raises(InvalidParameterException),
            ),
            (
                "https://localhost:9443",
                "garygeeke",
                400,
                pytest.raises(InvalidParameterException),
            ),
            (
                "https://127.0.0.1:9443",
                "garygeeke",
                200,
                does_not_raise(),
            ),
            (
                "https://127.0.0.1:9443",
                "",
                404,
                pytest.raises(InvalidParameterException),
            ),
            (
                "https://127.0.0.1:9443/open-metadata/admin-services/users/garygeeke/servers/active-metadata-store",
                "meow",
                404,
                pytest.raises(InvalidParameterException),
            ),
            (
                "https://wolfsonnet.me:9443/open-metadata/admin-services/users/garygeeke/servers/active-metadata-store",
                "woof",
                503,
                pytest.raises(InvalidParameterException),
            ),
            ("", "", 400, pytest.raises(InvalidParameterException)),
        ],
    )
    def test_make_get_request(self, url, user_id, status_code, expectation):
        server = "None"
        user_pwd = "nonesuch"
        response = ""
        with expectation as excinfo:
            t_client = egeria_client.client.Client(
                server, url, user_id, user_pwd, False
            )
            endpoint = (
                url
                + "/open-metadata/admin-services/users/"
                + user_id
                + "/stores/connection"
            )
            if t_client is not None:
                response = t_client.make_request("GET", endpoint, None)

        if excinfo:
            print(
                f"\nException: {excinfo.value.message_id} with http code {excinfo.value.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.value.class_name}")
            print(f"\t\t   Caller: {excinfo.value.action_description}")
            print(f"\t\t   System: {excinfo.value.system_action}")
            print(f"\t\t   Message: {excinfo.value.error_msg}")
            print(f"\t\t   User Action: {excinfo.value.user_action}")
        else:
            if (response is not None) & (response.status_code is None):
                assert excinfo.value.http_error_code == str(status_code), "Invalid URL"

            else:
                assert response.status_code == status_code, "Invalid URL"


if __name__ == "__main__":
    print("something")
