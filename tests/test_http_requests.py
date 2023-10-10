#
#  Test HTTP Requests
#
import pytest
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
                405,
                pytest.raises(InvalidParameterException, RESTConnectionException),
            ),
            (
                "https://127.0.0.1:9443/open-metadata/admin-services/users/garygeeke/servers/active-metadata-store/configuration",
                200,
                does_not_raise(),
            ),
            (
                "https://127.0.0.1:9443/open-metadata/admin-services/users/garygeeke/servers/active-metadata-store",
                405,
                pytest.raises(InvalidParameterException, RESTConnectionException),
            ),
            ("", 200, does_not_raise()),
        ],
    )
    def test_issue_get(self, url, status_code, expectation):
        with expectation as excinfo:
            response = issue_get(url)
            assert response.status_code == status_code, "Invalid URL"

            if excinfo:
                print(
                    f"\nException: {excinfo.value.message_id} with http code {e.http_error_code}"
                )
                print(f"\t\t   Class: {excinfo.value.class_name}")
                print(f"\t\t   Caller: {excinfo.value.action_description}")
                print(f"\t\t   System: {excinfo.value.system_action}")
                print(f"\t\t   Message: {excinfo.value.error_msg}")
                print(f"\t\t   User Action: {excinfo.value.user_action}")

        # try:
        #     response = issue_get(url)
        #     if response:
        #         assert response.status_code == status_code, "Invalid URL"
        #
        # except InvalidParameterException as e:
        #     print(f"\nException: {e.message_id} with http code {e.http_error_code}")
        #     print(f"\t\t   Class: {e.class_name}")
        #     print(f"\t\t   Caller: {e.action_description}")
        #     print(f"\t\t   System: {e.system_action}")
        #     print(f"\t\t   Message: {e.error_msg}")
        #     print(f"\t\t   User Action: {e.user_action}")
        #
        # except RESTConnectionException as e:
        #     print(f"\nException: {e.message_id} with http code {e.http_error_code}")
        #     print(f"\t\t   Class: {e.class_name}")
        #     print(f"\t\t   Caller: {e.action_description}")
        #     print(f"\t\t   System: {e.system_action}")
        #     print(f"\t\t   Message: {e.error_msg}")
        #     print(f"\t\t   User Action: {e.user_action}")


if __name__ == "__main__":
    print("something")
