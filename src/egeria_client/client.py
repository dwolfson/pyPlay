"""
This is a simple class to create and manage a connection to an Egeria backend

"""
import sys
import requests
from requests import Timeout, ConnectTimeout, ConnectionError, Response
import validators

from src.egeria_client.util_exp import (
    issue_data_post,
    process_error_response,
    print_guid_list,
    get_last_guid,
    issue_post,
    issue_get,
    OMAGCommonErrorCode,
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


...


class Client:
    """
    An abstract class used to establish connectivity for an Egeria Client
    for a particular server, platform and user.

    Attributes:
        server_name : str
            Name of the OMAG server to use
        server_platform_url : str
            URL of the server platform to connect to
        end_user_id : str
            The identity of the user calling the method - this sets a default optionally used by the methods
            when the user doesn't pass the user_id on a method call.
        server_user_id : str
            The identity used to connect to the server
        server_user_pwd : str
            The password used to authenticate the server identity

    Methods:
        __init__(self, server_name: str,
                 server_platform_url: str,
                 end_user_id: str,
                 server_user_id: str = None,
                 server_user_pwd: str = None
                 )
         Initializes the connection - throwing an exception if there is a problem



    """

    json_header = {"Content-Type": "application/json"}

    def __init__(
        self,
        server_name: str,
        server_platform_url: str,
        server_user_id: str = None,
        server_user_pwd: str = None,
        verify: bool = False,
    ):
        self.server_name = None
        self.server_platform_url = None
        self.server_user_id = server_user_id
        self.server_user_pwd = server_user_pwd
        self.ssl_verify = verify

        class_name = sys._getframe(2).f_code
        caller_method = sys._getframe(1).f_code.co_name

        try:
            v_url = validate_url(server_platform_url)
            v_srv = validate_server_name(server_name)
            v_usr = validate_user_id(server_user_id)
            if v_url & v_srv & v_usr:
                self.server_platform_url = server_platform_url
                self.server_name = server_name
                self.user_id = server_user_id
                self.session = requests.Session()
            else:
                raise Exception("Unexpected Exception")
        except InvalidParameterException as e:
            msg = OMAGCommonErrorCode.CLIENT_SIDE_REST_API_ERROR.value[
                "message_template"
            ].format(
                e.args[0],
                caller_method,
                class_name,
                server_platform_url,
                OMAGCommonErrorCode.CLIENT_SIDE_REST_API_ERROR.value["message_id"],
            )
            raise RESTConnectionException(
                msg,
                OMAGCommonErrorCode.CLIENT_SIDE_REST_API_ERROR,
                class_name,
                caller_method,
                self.server_platform_url,
            )

    def connect_test(self):
        url = (
            self.server_platform_url
            + "/open-metadata/admin-services/users/"
            + self.user_id
            + "/stores/connection"
        )
        class_name = sys._getframe(2).f_code
        caller_method = sys._getframe(1).f_code.co_name
        try:

            response = self.session.get(url, verify=self.ssl_verify)

        except (
            requests.ConnectionError,
            requests.ConnectTimeout,
            requests.ConnectionError,
            requests.HTTPError,
            requests.RequestException,
            requests.Timeout,
        ) as e:
            msg = OMAGCommonErrorCode.CLIENT_SIDE_REST_API_ERROR.value[
                "message_template"
            ].format(
                e.args[0],
                caller_method,
                class_name,
                url,
                OMAGCommonErrorCode.CLIENT_SIDE_REST_API_ERROR.value["message_id"],
            )
            raise RESTConnectionException(
                msg,
                OMAGCommonErrorCode.CLIENT_SIDE_REST_API_ERROR,
                class_name,
                caller_method,
                url,
            )

        except Exception as e:
            print(f"An exception occurred: {e}")
            raise Exception(e)

        if response.status_code == 200:
            return response
        else:
            if response.status_code in (400, 401, 403, 404, 405):
                msg = OMAGCommonErrorCode.CLIENT_SIDE_REST_API_ERROR.value[
                    "message_template"
                ].format(
                    response.status_code,
                    caller_method,
                    class_name,
                    url,
                    OMAGCommonErrorCode.CLIENT_SIDE_REST_API_ERROR.value["message_id"],
                )
                raise RESTConnectionException(
                    msg,
                    OMAGCommonErrorCode.CLIENT_SIDE_REST_API_ERROR,
                    class_name,
                    caller_method,
                    url,
                )
            elif response.status_code in (500, 501, 502, 503, 504):
                msg = OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API.value[
                    "message_template"
                ].format(
                    response.status_code,
                    caller_method,
                    url,
                    OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API.value["message_id"],
                )
                raise RESTConnectionException(
                    msg,
                    OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API,
                    class_name,
                    caller_method,
                    url,
                )


if __name__ == "__main__":
    try:
        connection = Client(
            "active-metadata-store", "https://127.0.0.1:9443", "garygeeke", "foo"
        )
    except Exception as e:
        print(e)
