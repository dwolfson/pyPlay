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
    RESTConnectionException,
)


class TestClient:
    # @pytest.mark.xfail
    @pytest.mark.parametrize(
        "url, user_id, status_code, expectation",
        [
            (
                "https://google.com",
                "garygeeke",
                503,
                pytest.raises(RESTConnectionException),
            ),
            (
                "https://localhost:9443",
                "garygeeke",
                503,
                pytest.raises(RESTConnectionException),
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
                503,
                does_not_raise(),
            ),
            # (
            #         "https://127.0.0.1:9443/open-metadata/admin-services/users/garygeeke/servers/active-metadata-store",
            #         "503",
            #         pytest.raises(RESTConnectionException),
            #         # does_not_raise(),
            # ),
            # (
            #         "https://wolfsonnet.me:9443/open-metadata/admin-services/users/garygeeke/servers/active-metadata-store",
            #         "404",
            #         pytest.raises(RESTConnectionException),
            # ),
            # ("", "400", pytest.raises(InvalidParameterException)),
        ],
    )
    def test_connect_test(self, url, user_id, status_code, expectation):
        response = None
        # status_code = 200
        # url = "https://127.0.0.1:9443"
        server = "None"
        # user_id = "garygeeke"
        user_pwd = "nonesuch"
        # excinfo = None

        with expectation as excinfo:
            test_client = egeria_client.client.Client(
                server, url, user_id, user_pwd, False
            )
            response = test_client.connect_test()

        if response is None:
            assert excinfo.value.http_error_code == str(status_code), "Invalid URL"
            print(excinfo)
        else:
            assert int(response.status_code) == status_code, "Invalid URL"

        if excinfo:
            print(
                f"\nException: {excinfo.value.message_id} with http code {excinfo.value.http_error_code}"
            )
            print(f"\t\t   Class: {excinfo.value.class_name}")
            print(f"\t\t   Caller: {excinfo.value.action_description}")
            print(f"\t\t   System: {excinfo.value.system_action}")
            print(f"\t\t   Message: {excinfo.value.error_msg}")
            print(f"\t\t   User Action: {excinfo.value.user_action}")


#
#  Test field validators
#


class TestHttpRequests:
    """
    A class to test all the helper methods used to make HTTP requests using Pytest.

    Attributes:

    Methods:
        test_issue_get(url)
        test_issue_post(url, result)
        test_issue_data_post(url, body)
        test_issue_put(url, body)

    """

    def __init__(
        self, error_msg, class_name, method_name, action_description, error_code, params
    ):
        pass


@pytest.mark.parametrize(
    "url, status_code, expectation",
    [
        ("https://google.com", 200, does_not_raise()),
        (
            "https://localhost:9443/open-metadata/admin-services/users/garygeeke/servers/active-metadata-store/configuration",
            400,
            pytest.raises(InvalidParameterException),
        ),
        (
            "https://127.0.0.1:9443/open-metadata/admin-services/users/garygeeke/servers/active-metadata-store/configuration",
            200,
            does_not_raise(),
        ),
        (
            "https://127.0.0.1:9443/open-metadata/admin-services/users/garygeeke/servers/active-metadata-store",
            "503",
            pytest.raises(RESTConnectionException),
            # does_not_raise(),
        ),
        (
            "https://wolfsonnet.me:9443/open-metadata/admin-services/users/garygeeke/servers/active-metadata-store",
            "404",
            pytest.raises(RESTConnectionException),
        ),
        ("", "400", pytest.raises(InvalidParameterException)),
    ],
)
def test_issue_get(url, status_code, expectation):
    response = None
    with expectation as excinfo:
        response = issue_get(url)
    if response is None:
        assert excinfo.value.http_error_code == str(status_code), "Invalid URL"
        print(excinfo)
    else:
        assert int(response.status_code) == status_code, "Invalid URL"

    if excinfo:
        print(
            f"\nException: {excinfo.value.message_id} with http code {excinfo.value.http_error_code}"
        )
        print(f"\t\t   Class: {excinfo.value.class_name}")
        print(f"\t\t   Caller: {excinfo.value.action_description}")
        print(f"\t\t   System: {excinfo.value.system_action}")
        print(f"\t\t   Message: {excinfo.value.error_msg}")
        print(f"\t\t   User Action: {excinfo.value.user_action}")


def test_issue_post():
    response = None
    url = "https://127.0.0.1:9443/servers/active-metadata-store/open-metadata/access-services/asset-manager/users/garygeeke/glossaries"
    body = {
        "class": "ReferenceableRequestBody",
        "elementProperties": {
            "class": "GlossaryProperties",
            "qualifiedName": "Goldfish" + str(time),
            "displayName": "A goldfish",
            "description": "This glossary is the main glossary for the Abu Dhabi government.",
            "language": "English/Arabic",
            "usage": "This glossary provides the approved glossary terms.",
        },
    }

    response = issue_post(url, body)
    if response is None:
        assert False, "Post failed to execute"

    else:
        assert int(response.status_code) == 200, "Invalid URL"


# @pytest.mark.skip("under construction")
def test_issue_data_post():
    response = None
    url = "https://wolfsonnet.me:9443/servers/active-metadata-store/open-metadata/access-services/asset-manager/users/garygeeke/glossaries"
    body = {
        "class": "ReferenceableRequestBody",
        "elementProperties": {
            "class": "GlossaryProperties",
            "qualifiedName": "Goldfish" + str(time),
            "displayName": "A goldfish",
            "description": "This glossary is the main glossary for the Abu Dhabi government.",
            "language": "English/Arabic",
            "usage": "This glossary provides the approved glossary terms.",
        },
    }

    response = issue_post(url, body)
    if response is None:
        assert False, "Post failed to execute"

    else:
        assert int(response.status_code) == 200, "Invalid URL"


# @pytest.mark.xfail
def test_http_issues():
    response = None
    status_code = 503
    url = "https://wolfsonnet.me:9443/open-metadata/admin-services/users/garygeeke/servers/active-metadata-store"

    with pytest.raises(RESTConnectionException) as excinfo:
        response = issue_get(url)
    if response is None:
        assert excinfo.value.http_error_code == str(status_code), "Invalid URL"
        print(excinfo)
    else:
        assert int(response.status_code) == status_code, "Invalid URL"

    if excinfo:
        print(
            f"\nException: {excinfo.value.message_id} with http code {excinfo.value.http_error_code}"
        )
        print(f"\t\t   Class: {excinfo.value.class_name}")
        print(f"\t\t   Caller: {excinfo.value.action_description}")
        print(f"\t\t   System: {excinfo.value.system_action}")
        print(f"\t\t   Message: {excinfo.value.error_msg}")
        print(f"\t\t   User Action: {excinfo.value.user_action}")


if __name__ == "__main__":
    print("something")
