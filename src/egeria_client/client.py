"""
This is a simple class to create and manage a connection to an Egeria backend

"""
import os
import sys

import requests
from enum import Enum
from requests import Timeout, ConnectTimeout, ConnectionError, Response


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
    PropertyServerException,
)


class RequestType(Enum):
    """
    Enum class for RequestType containing 4 values - GET, POST, PUT, PATCH, DELETE
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


...


class Client:
    """
    An abstract class used to establish connectivity for an Egeria Client
    for a particular server, platform and user.

    Attributes:
        server_name : str
            Name of the OMAG server to use
        platform_url : str
            URL of the server platform to connect to
        end_user_id : str
            The identity of the user calling the method - this sets a default optionally used by the methods
            when the user doesn't pass the user_id on a method call.
        user_id : str
            The identity used to connect to the server
        user_pwd : str
            The password used to authenticate the server identity

    Methods:
        __init__(self, server_name: str,
                 platform_url: str,
                 end_user_id: str,
                 user_id: str = None,
                 user_pwd: str = None
                 )
         Initializes the connection - throwing an exception if there is a problem



    """

    json_header = {"Content-Type": "application/json"}

    def __init__(
        self,
        server_name: str,
        platform_url: str,
        user_id: str = None,
        user_pwd: str = None,
        verify_flag: bool = False,
    ):
        self.server_name = None
        self.platform_url = None
        self.user_id = user_id
        self.user_pwd = user_pwd
        self.ssl_verify = verify_flag
        api_key = os.environ.get("API_KEY")
        self.headers = {"Content-Type": "application/json", "x-api-key": api_key}

        class_name = sys._getframe(2).f_code
        caller_method = sys._getframe(1).f_code.co_name

        v_url = validate_url(platform_url)
        # Todo: Document and cleanup
        # I am changing the logic here because a server may not yet exist and users may not be configured
        # v_srv = validate_server_name(server_name)
        # v_usr = validate_user_id(user_id)
        # if v_url & v_srv & v_usr:
        if v_url:
            self.platform_url = platform_url
            self.server_name = server_name
            self.user_id = user_id
            self.session = requests.Session()
        else:
            if platform_url:
                msg = OMAGCommonErrorCode.SERVER_URL_MALFORMED.value[
                    "message_template"
                ].format(platform_url)
            else:
                msg = OMAGCommonErrorCode.SERVER_URL_NOT_SPECIFIED.value[
                    "message_template"
                ]

            raise InvalidParameterException(
                msg,
                OMAGCommonErrorCode.SERVER_URL_MALFORMED,
                class_name,
                caller_method,
                self.platform_url,
            )

    def make_request(
        self, request_type: str, endpoint: str, payload: str = None
    ) -> Response:
        """
        Function to make an API call via the Requests Library. Raise an exception if the HTTP response code
        is not 200/201. IF there is a REST communication exception, raise InvalidParameterException.

        :param request_type: Type of Request.
               Supported Values - GET, POST, (not PUT, PATCH, DELETE).
               Type - String
        :param endpoint: API Endpoint. Type - String
        :param payload: API Request Parameters or Query String.
               Type - String or Dict
        :return: Response. Type - JSON Formatted String
        """
        class_name = sys._getframe(2).f_code.co_name
        caller_method = sys._getframe(1).f_code.co_name
        try:
            response = ""
            if request_type == "GET":
                response = requests.get(
                    endpoint, timeout=30, params=payload, verify=self.ssl_verify
                )
            elif request_type == "POST":
                response = requests.post(
                    endpoint,
                    headers=self.headers,
                    timeout=30,
                    json=payload,
                    verify=self.ssl_verify,
                )
            elif request_type == "DELETE":
                response = requests.delete(endpoint, timeout=30, verify=self.ssl_verify)

            if response.status_code in (200, 201):
                related_code = response.json().get("relatedHTTPCode")
                if related_code == 200:
                    return response
                else:
                    msg = OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API.value[
                        "message_template"
                    ].format(
                        str(related_code),
                        caller_method,
                        # class_name,
                        endpoint,
                        OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API.value[
                            "message_id"
                        ],
                    )
                    raise InvalidParameterException(
                        msg,
                        OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API,
                        class_name,
                        caller_method,
                        [endpoint],
                    )
                return response
            if response.status_code in (400, 401, 403, 404, 405):
                msg = OMAGCommonErrorCode.CLIENT_SIDE_REST_API_ERROR.value[
                    "message_template"
                ].format(
                    response.status_code,
                    caller_method,
                    class_name,
                    endpoint,
                    OMAGCommonErrorCode.CLIENT_SIDE_REST_API_ERROR.value["message_id"],
                )
                raise InvalidParameterException(
                    msg,
                    OMAGCommonErrorCode.CLIENT_SIDE_REST_API_ERROR,
                    class_name,
                    caller_method,
                    [endpoint, str(response.status_code)],
                )
            elif response.status_code in (500, 501, 502, 503, 504):
                msg = OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API.value[
                    "message_template"
                ].format(
                    response.status_code,
                    caller_method,
                    endpoint,
                    OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API.value["message_id"],
                )
                raise PropertyServerException(
                    msg,
                    OMAGCommonErrorCode.EXCEPTION_RESPONSE_FROM_API,
                    class_name,
                    caller_method,
                    [endpoint, str(response.status_code)],
                )

        except (
            requests.ConnectionError,
            requests.ConnectTimeout,
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
                endpoint,
                OMAGCommonErrorCode.CLIENT_SIDE_REST_API_ERROR.value["message_id"],
            )
            # logging.error(e)
            raise InvalidParameterException(
                msg,
                OMAGCommonErrorCode.CLIENT_SIDE_REST_API_ERROR,
                class_name,
                caller_method,
                # [url, str(response.status_code)],
                [endpoint],
            )


if __name__ == "__main__":
    try:
        connection = Client(
            "active-metadata-store", "https://127.0.0.1:9443", "garygeeke", "foo"
        )
    except Exception as e:
        print(e)
