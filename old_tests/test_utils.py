# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
#
# Unit tests for the Utils helper functions using the Pytest framework.
#

import pytest
from src.egeria_client.utils import (
    issue_get,
    issue_post,
    issue_data_post,
    issue_put,
    process_error_response,
    print_guid_list,
    get_last_guid,


    validate_user_id,
    validate_url,
    InvalidParameterException,
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
            assert (
                validate_user_id(user_id, "test_class", "test_method") == result
            ), "Invalid user id"

        except InvalidParameterException as e:
            print(f"\nException: {e.message_id} with http code {e.http_error_code}")
            print(f"\t\t   System: {e.system_action}")
            print(f"\t\t   Message: {e.message}")
            print(f"\t\t   User Action: {e.user_action}")

    @pytest.mark.parametrize(
        "url, result",
        [
            ("https://google.com", True),
            (
                "https://127.0.0.1:9443/open-metadata/platform-services/users/garygeeke/server-platform/servers/active-metadata-store/instance",
                True,
            ),
            (
                "https://localhost.local:9443/open-metadata/platform-services/users/garygeeke/server-platform/servers/active-metadata-store/instance",
                True,
            ),
            ("", False),
            ("http://localhost:9444", False),
        ],
    )
    def test_validate_url(self, url, result):
        """
        Test the url validator

        Parameters
        ----------
        url : the url string to check
        result : the expected outcome

        """
        try:
            assert (
                validate_url(url, "test-connection", "test-method") == result
            ), "Invalid URL"

        except InvalidParameterException as e:
            print(f"\nException: {e.message_id} with http code {e.http_error_code}")
            print(f"\t\t   System: {e.system_action}")
            print(f"\t\t   Message: {e.message}")
            print(f"\t\t   User Action: {e.user_action}")


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


@pytest.mark.parametrize(
    "url, result",
    [
        ("https://google.com", 200),
        (
            "https://127.0.0.1:9443/open-metadata/platform-services/users/garygeeke/server-platform/servers/active-metadata-store/instance",
            200,
        ),
        (
            "https://localhost.local:9443/open-metadata/platform-services/users/garygeeke/server-platform/servers/active-metadata-store/instance",
            200,
        ),
        ("", 400),
        ("http://localhost:9444", 200),
    ],
)
def test_issue_get(url, http_code):
    try:
        assert issue_get(url) == http_code, "Invalid URL"

    except InvalidParameterException as e:
        print(f"\nException: {e.message_id} with http code {e.http_error_code}")
        print(f"\t\t   System: {e.system_action}")
        print(f"\t\t   Message: {e.message}")
        print(f"\t\t   User Action: {e.user_action}")


if __name__ == "__main__":
    test_connection()
