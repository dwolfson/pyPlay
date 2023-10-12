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

#
#  Test field validators
#
class TestValidators:
    """
    A class to test all the base field validators using Pytest.
    These validators do not require a connection to Egeria.

    Attributes:


    Methods:
        test_validate_user_id(user_id,method_name)
            check for null or empty string

        test_validate_server_name()

        test_validate_public()

        test_validate_url(url, class_name, method_name)

        test_validate_server()

    """

    @pytest.mark.parametrize("user_id, result", [("foo", True), ("", False)])
    def test_validate_user_id(self, user_id, result):
        """
        Test the validator for user_id

        Parameters
        ----------
        user_id : the string to validate
        result :  the expected outcome

        """
        try:
            assert validate_user_id(user_id) == result, "Invalid user id"

        except InvalidParameterException as e:
            print(f"\n\nException: {e.error_msg}")
            print(
                f"\t\t   Error Code: {e.message_id} with http code {e.http_error_code}"
            )
            print(f"\t\t   Class: {e.class_name}")
            print(f"\t\t   Caller: {e.action_description}")
            print(f"\t\t   System: {e.system_action}")
            print(f"\t\t   User Action: {e.user_action}")

    @pytest.mark.parametrize("server_name, result", [("cocoMDS1", True), ("", False)])
    def test_validate_server_name(self, server_name, result):
        """
        Test the validator for a server name

        Parameters
        ----------
        server_name : the string to validate
        result :  the expected outcome

        """
        try:
            assert validate_server_name(server_name) == result, "Invalid Server Name"

        except InvalidParameterException as e:
            print(f"\n\nException: {e.error_msg}")
            print(
                f"\t\t   Error Code: {e.message_id} with http code {e.http_error_code}"
            )
            print(f"\t\t   Class: {e.class_name}")
            print(f"\t\t   Caller: {e.action_description}")
            print(f"\t\t   System: {e.system_action}")
            print(f"\t\t   User Action: {e.user_action}")

    @pytest.mark.parametrize("guid, result", [("12341234-1234213", True), ("", False)])
    def test_validate_guid(self, guid, result):
        """
        Test the validator for a GUID

        Parameters
        ----------
        guid : the string to validate
        result :  the expected outcome

        """
        try:
            assert validate_guid(guid) == result, "Invalid GUID"

        except InvalidParameterException as e:
            print(f"\n\nException: {e.error_msg}")
            print(
                f"\t\t   Error Code: {e.message_id} with http code {e.http_error_code}"
            )
            print(f"\t\t   Class: {e.class_name}")
            print(f"\t\t   Caller: {e.action_description}")
            print(f"\t\t   System: {e.system_action}")
            print(f"\t\t   User Action: {e.user_action}")

    @pytest.mark.parametrize("name, result", [("garygeeke", True), ("", False)])
    def test_validate_name(self, name, result):
        """
        Test the validator for a name

        Parameters
        ----------
        name : the string to validate
        result :  the expected outcome

        """
        try:
            assert validate_name(name) == result, "Invalid Name"

        except InvalidParameterException as e:
            print(f"\n\nException: {e.error_msg}")
            print(
                f"\t\t   Error Code: {e.message_id} with http code {e.http_error_code}"
            )
            print(f"\t\t   Class: {e.class_name}")
            print(f"\t\t   Caller: {e.action_description}")
            print(f"\t\t   System: {e.system_action}")
            print(f"\t\t   User Action: {e.user_action}")

    @pytest.mark.parametrize(
        "search_string, result", [("sustainability", True), ("", False)]
    )
    def test_validate_search_string(self, search_string, result):
        """
        Test the validator for a search_string

        Parameters
        ----------
        search_string : the string to validate
        result :  the expected outcome

        """
        try:
            assert (
                validate_search_string(search_string) == result
            ), "Invalid search string"

        except InvalidParameterException as e:
            print(f"\n\nException: {e.error_msg}")
            print(
                f"\t\t   Error Code: {e.message_id} with http code {e.http_error_code}"
            )
            print(f"\t\t   Class: {e.class_name}")
            print(f"\t\t   Caller: {e.action_description}")
            print(f"\t\t   System: {e.system_action}")
            print(f"\t\t   User Action: {e.user_action}")

    @pytest.mark.parametrize("is_public, result", [(True, True), (None, False)])
    def test_validate_public(self, is_public, result):
        """
        Test the validator for public flag

        Parameters
        ----------
        is_public : the string to validate
        result :  the expected outcome

        """
        try:
            assert validate_public(is_public) == result, "Invalid public flag"

        except InvalidParameterException as e:
            print(f"\n\nException: {e.error_msg}")
            print(
                f"\t\t   Error Code: {e.message_id} with http code {e.http_error_code}"
            )
            print(f"\t\t   Class: {e.class_name}")
            print(f"\t\t   Caller: {e.action_description}")
            print(f"\t\t   System: {e.system_action}")
            print(f"\t\t   User Action: {e.user_action}")

    @pytest.mark.parametrize(
        "url, result, expectation",
        [
            ("https://google.com", True, does_not_raise()),
            (
                "https://127.0.0.1:9443/open-metadata/platform-services/users/garygeeke/server-platform/servers/active-metadata-store/instance",
                True,
                does_not_raise(),
            ),
            (
                "https://localhost.local:9443/open-metadata/platform-services/users/garygeeke/server-platform/servers/active-metadata-store/instance",
                True,
                does_not_raise(),
            ),
            ("", False, pytest.raises(InvalidParameterException)),
            ("http://localhost:9444", False, pytest.raises(InvalidParameterException)),
        ],
    )
    def test_validate_url(self, url, result, expectation):
        """
        Test the url validator

        Parameters
        ----------
        url : the url string to check
        result : the expected outcome

        """

        with expectation as e:
            res = validate_url(url)

            assert res == result, "Invalid URL"

        if e:
            print(f"\n\nException: {e.value.error_msg} ")
            print(
                f"\t\t   Error Code: {e.value.message_id} with http code {e.value.http_error_code}"
            )
            print(f"\t\t   Class: {e.value.class_name}")
            print(f"\t\t   Caller: {e.value.action_description}")
            print(f"\t\t   System: {e.value.system_action}")
            print(f"\t\t   User Action: {e.value.user_action}")


#
#  Test HTTP Requests
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
