# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
#
# Common processing of REST API errors.
#
...
from src.egeria_client.config import isDebug
from enum import Enum
import json
import requests
import validators

# todo check - import inspect

comment_types = (
    "ANSWER",
    "OTHER",
    "QUESTION",
    "STANDARD_COMMENT",
    "SUGGESTION",
    "USAGE_EXPERIENCE",
)
star_ratings = (
    "FIVE_STARS",
    "FOUR_STARS",
    "NO_RECOMMENDATION",
    "ONE_STAR",
    "THREE_STARS",
    "TWO_STARS",
)


class Asset:
    def __init__(self, asset_body: dict):
        pass


class MessageDefinition:
    def __init__(
        self,
        message_id: str,
        message_template: str,
        system_action: str,
        user_action: str,
        params: [str],
    ):
        self.message_id = message_id
        self.message_template = message_template
        self.system_action = system_action
        self.user_action = user_action
        self.params = params

    def __str__(self):
        return (
            "messageId="
            + self.message_id
            + ", messageTemplate="
            + self.message_template
            + ", systemAction="
            + self.system_action
            + ", userAction="
            + self.user_action
            + ", params="
            + str(self.params)
        )


class ExceptionMessageDefinition(MessageDefinition):
    def __init__(
        self,
        http_error_code: str,
        message_id: str,
        message_template: str,
        system_action: str,
        user_action: str,
        params: [str] = None,
    ):
        MessageDefinition.__init__(
            self, message_id, message_template, system_action, user_action, params
        )
        self.http_error_code = http_error_code

    def __str__(
        self,
    ):
        return (
            "http_error_code="
            + self.http_error_code
            + "messageId="
            + self.message_id
            + ", messageTemplate="
            + self.message_template
            + ", systemAction="
            + self.system_action
            + ", userAction="
            + self.user_action
            + ", params="
            + str(self.params)
        )


class OMAGCommonErrorCode(Enum):
    SERVER_URL_NOT_SPECIFIED = dict(
        http_error_code="400",
        message_id="OMAG-COMMON-400-001",
        message_template="The OMAG Server Platform URL is null",
        system_action="The system is unable to identify the OMAG Server Platform.",
        user_action="Create a new client and pass the URL for the server on the constructor.",
    )

    SERVER_URL_MALFORMED = dict(
        http_error_code="400",
        message_id="OMAG-COMMON-400-002",
        message_template="The OMAS Server URL %s is not in a recognized format",
        system_action="The system is unable to connect to the OMAG Server Platform to fulfill any requests.",
        user_action="Create a new client and pass the correct URL for the server on the constructor.",
    )

    SERVER_NAME_NOT_SPECIFIED = dict(
        http_error_code="400",
        message_id="OMAG-COMMON-400-003",
        message_template="The OMAG Server name is null",
        system_action="The system is unable to locate to the OMAG Server to fulfill any request.",
        user_action="Create a new client and pass the correct name for the server on the constructor.",
    )

    NULL_USER_ID = dict(
        http_error_code="400",
        message_id="OMAG-COMMON-400-004",
        message_template="The user identifier (user id) passed on the {0} operation is null",
        system_action="The system is unable to process the request without a user id..",
        user_action="Correct the code in the caller to provide the user id.",
    )

    NULL_GUID = dict(
        http_error_code="400",
        message_id="OMAG-COMMON-400-005",
        message_template="The unique identifier (guid) passed on the {0} parameter of the {1} operation is null",
        system_action="The system is unable to process the request without a guid.",
        user_action="Correct the code in the caller to provide the guid.",
    )

    NULL_NAME = dict(
        http_error_code="400",
        message_id="OMAG-COMMON-400-006",
        message_template="The name passed on the {0} parameter of the {1} operation is null",
        system_action="The system is unable to process the request without a name.",
        user_action="Correct the code in the caller to provide the name on the parameter.",
    )

    NULL_ARRAY_PARAMETER = dict(
        http_error_code="400",
        message_id="OMAG-COMMON-400-007",
        message_template="The array value passed on the {0} parameter of the {1} operation is null or empty",
        system_action="The system is unable to process the request without this value.",
        user_action="Correct the code in the caller to provide the array.",
    )

    NEGATIVE_START_FROM = dict(
        http_error_code="400",
        message_id="OMAG-COMMON-400-008",
        message_template="The starting point for the results {0}, passed on the {1} parameter of the {2} operation, is negative",
        system_action="The system is unable to process the request with this invalid value.  It should be zero for the start of the values, or a number greater than 0 to start partway down the list.",
        user_action="Correct the code in the caller to provide a non-negative value for the starting point.",
    )

    NEGATIVE_PAGE_SIZE = dict(
        http_error_code="400",
        message_id="OMAG-COMMON-400-009",
        message_template="The page size for the results {0}, passed on the {1} parameter of the {2} operation, is negative",
        system_action="The system is unable to process the request with this invalid value.  It should be zero to return all the result, or greater than zero to set a maximum.",
        user_action="Correct the code in the caller to provide a non-negative value for the page size.",
    )

    MAX_PAGE_SIZE = dict(
        http_error_code="400",
        message_id="OMAG-COMMON-400-010",
        message_template="The number of records to return, {0}, passed on the {1} parameter of the {2} operation, is greater than the allowable maximum of {3}",
        system_action="The system is unable to process the request with this page size value.",
        user_action="Correct the code in the caller to provide a smaller page size.",
    )

    NULL_ENUM = dict(
        http_error_code="400",
        message_id="OMAG-COMMON-400-012",
        message_template="The enumeration value passed on the {0} parameter of the {1} operation is null",
        system_action="The system is unable to process the request without a enumeration value.",
        user_action="Correct the code in the caller to provide the enumeration value.",
    )

    NULL_TEXT = dict(
        http_error_code="400",
        message_id="OMAG-COMMON-400-013",
        message_template="The text field passed on the {0} parameter of the {1} operation is null",
        system_action="The system is unable to process the request without this text value.",
        user_action="Correct the code in the caller to provide a value in the text field.",
    )

    NULL_OBJECT = dict(
        http_error_code="400",
        message_id="OMAG-COMMON-400-015",
        message_template="The object passed on the {0} parameter of the {1} operation is null",
        system_action="The system is unable to process the request without this object.",
        user_action="Correct the code in the caller to provide the object.",
    )

    NULL_SEARCH_STRING = dict(
        http_error_code="400",
        message_id="OMAG-COMMON-400-022",
        message_template="The search string passed on the {0} parameter of the {1} operation is null",
        system_action="The system is unable to process the request without a search string.",
        user_action="Correct the code in the caller to provide the search string.",
    )


class PropertyServerException(Exception):
    """Exception due to a problem retrieving information from the property server"""

    pass


class UserNotAuthorizedException(Exception):
    """Exception as the requesting user is not authorized to issue this request"""

    pass


class InvalidParameterException(Exception):
    """Exception due to invalid parameters such as one of the parameters is null or invalid"""

    def __init__(
        self,
        message: ExceptionMessageDefinition,
        class_name,
        action_description,
        param_name=None,
        params=None,
    ):
        if param_name is not None:
            self.message = message.message_template % params
        else:
            self.message = message.message_template
        self.class_name = class_name
        self.action_description = action_description
        self.param_name = param_name
        self.http_error_code = message.http_error_code
        self.message_id = message.message_id
        self.system_action = message.system_action
        self.user_action = message.user_action
        self.params = params


"""

Validators and error handlers for common parameters

"""
max_paging_size = 100


def validate_user_id(user_id: str, class_name, method_name):
    if (user_id is None) or len(user_id) == 0:
        msg = ExceptionMessageDefinition(
            OMAGCommonErrorCode.SERVER_URL_NOT_SPECIFIED.value["http_error_code"],
            OMAGCommonErrorCode.SERVER_URL_NOT_SPECIFIED.value["message_id"],
            OMAGCommonErrorCode.SERVER_URL_NOT_SPECIFIED.value["message_template"],
            OMAGCommonErrorCode.SERVER_URL_NOT_SPECIFIED.value["system_action"],
            OMAGCommonErrorCode.SERVER_URL_NOT_SPECIFIED.value["user_action"]
            # None,
        )
        raise InvalidParameterException(msg, class_name, method_name, None, None)
    else:
        return True


def validate_server_name():
    pass


def validate_public():
    pass


def validate_url(url: str, class_name, method_name) -> bool:
    if (url is None) or (len(url) == 0):
        msg = ExceptionMessageDefinition(
            OMAGCommonErrorCode.SERVER_URL_NOT_SPECIFIED.value["http_error_code"],
            OMAGCommonErrorCode.SERVER_URL_NOT_SPECIFIED.value["message_id"],
            OMAGCommonErrorCode.SERVER_URL_NOT_SPECIFIED.value["message_template"],
            OMAGCommonErrorCode.SERVER_URL_NOT_SPECIFIED.value["system_action"],
            OMAGCommonErrorCode.SERVER_URL_NOT_SPECIFIED.value["user_action"]
            # None,
        )
        raise InvalidParameterException(msg, class_name, method_name, None, None)

    result = validators.url(url)
    # print(f"validation result is {result}")
    if result is not True:
        msg = ExceptionMessageDefinition(
            OMAGCommonErrorCode.SERVER_URL_MALFORMED.value["http_error_code"],
            OMAGCommonErrorCode.SERVER_URL_MALFORMED.value["message_id"],
            OMAGCommonErrorCode.SERVER_URL_MALFORMED.value["message_template"],
            OMAGCommonErrorCode.SERVER_URL_MALFORMED.value["system_action"],
            OMAGCommonErrorCode.SERVER_URL_MALFORMED.value["user_action"],
            {url},
        )
        raise InvalidParameterException(msg, class_name, method_name, "URL", {url})
    else:
        return True


def validate_server():
    pass


#
# OCF Common services
# Working with assets - this set of functions displays assets returned from the open metadata repositories.
#
class comment:
    def __init__(
        self,
        comment_guid: str,
        comment_type: str,
        comment_text: str,
        comment_owner: str,
        is_public: bool,
    ):
        self.comment_guid: str = comment_guid
        self.comment_type: str = comment_type
        self.comment_text: str = comment_text
        self.comment_owner: str = comment_owner
        self.is_public: bool = is_public

        if self.comment_type not in comment_types:
            raise ValueError(comment_type + " is an Invalid comment type")


def get_asset_universe(
    serverName,
    serverPlatformName,
    serverPlatformURL,
    serviceURLMarker,
    userId,
    assetGUID,
):
    connectedAssetURL = (
        serverPlatformURL
        + "/servers/"
        + serverName
        + "/open-metadata/common-services/"
        + serviceURLMarker
        + "/connected-asset/users/"
        + userId
    )
    getAsset = connectedAssetURL + "/assets/" + assetGUID
    response = issueGet(getAsset)
    asset = response.json().get("asset")
    if asset:
        return response.json()
    else:
        print("No Asset returned")
        process_error_response(serverName, "fixme", serverPlatformURL, response)


def get_related_assets(
    serverName,
    serverPlatformName,
    serverPlatformURL,
    serviceURLMarker,
    userId,
    assetGUID,
):
    """
    Parameters
    ----------
    serverName :
    serverPlatformName :
    serverPlatformURL :
    serviceURLMarker :
    userId :
    assetGUID :

    Returns
    -------

    """
    connectedAssetURL = (
        serverPlatformURL
        + "/servers/"
        + serverName
        + "/open-metadata/common-services/"
        + serviceURLMarker
        + "/connected-asset/users/"
        + userId
    )
    getRelatedAsset = (
        connectedAssetURL
        + "/assets/"
        + assetGUID
        + "/related-assets?elementStart=0&maxElements=50"
    )
    response = issue_get(getRelatedAsset)
    if response.status_code == 200:
        relatedHTTPCode = response.json().get("relatedHTTPCode")
        if relatedHTTPCode == 200:
            return response.json().get("list")
        else:
            printUnexpectedResponse(
                serverName, serverPlatformName, serverPlatformURL, response
            )
    else:
        printUnexpectedResponse(
            serverName, serverPlatformName, serverPlatformURL, response
        )


def get_comments(
    serverName,
    serverPlatformName,
    serverPlatformURL,
    serviceURLMarker,
    userId,
    assetGUID,
):
    connectedAssetURL = (
        serverPlatformURL
        + "/servers/"
        + serverName
        + "/open-metadata/common-services/"
        + serviceURLMarker
        + "/connected-asset/users/"
        + userId
    )
    commentQuery = (
        connectedAssetURL
        + "/assets/"
        + assetGUID
        + "/comments?elementStart=0&maxElements=50"
    )
    response = issueGet(commentQuery)
    responseObjects = response.json().get("list")
    if responseObjects:
        return responseObjects
    else:
        print("No comments returned")
        process_error_response(serverName, "fixme", serverPlatformURL, response)


def get_comment_replies(
    serverName,
    serverPlatformName,
    serverPlatformURL,
    serviceURLMarker,
    userId,
    assetGUID,
    commentGUID,
):
    connectedAssetURL = (
        serverPlatformURL
        + "/servers/"
        + serverName
        + "/open-metadata/common-services/"
        + serviceURLMarker
        + "/connected-asset/users/"
        + userId
    )
    commentReplyQuery = (
        connectedAssetURL
        + "/assets/"
        + assetGUID
        + "/comments/"
        + commentGUID
        + "/replies?elementStart=0&maxElements=50"
    )
    response = issueGet(commentReplyQuery)
    responseObjects = response.json().get("list")
    if responseObjects:
        return responseObjects
    else:
        print("No comments returned")
        process_error_response(serverName, "fixme", serverPlatformURL, response)


def get_api_operations(
    serverName,
    serverPlatformName,
    serverPlatformURL,
    serviceURLMarker,
    userId,
    apiSchemaTypeGUID,
):
    connectedAssetURL = (
        serverPlatformURL
        + "/servers/"
        + serverName
        + "/open-metadata/common-services/"
        + serviceURLMarker
        + "/connected-asset/users/"
        + userId
    )
    requestURL = (
        connectedAssetURL
        + "/assets/schemas/apis/"
        + apiSchemaTypeGUID
        + "/api-operations?elementStart=0&maxElements=50"
    )
    response = issueGet(requestURL)
    responseObjects = response.json().get("list")
    if response.status_code == 200:
        relatedHTTPCode = response.json().get("relatedHTTPCode")
        if relatedHTTPCode == 200:
            return response.json().get("list")
        else:
            printUnexpectedResponse(
                serverName, serverPlatformName, serverPlatformURL, response
            )
    else:
        printUnexpectedResponse(
            serverName, serverPlatformName, serverPlatformURL, response
        )


def get_schema_attributes_from_schema_type(
    serverName,
    serverPlatformName,
    serverPlatformURL,
    serviceURLMarker,
    userId,
    schemaTypeGUID,
):
    ocfURL = (
        serverPlatformURL
        + "/servers/"
        + serverName
        + "/open-metadata/common-services/"
        + serviceURLMarker
        + "/connected-asset/users/"
        + userId
    )
    getSchemaAttributesURL = (
        ocfURL
        + "/assets/schemas/"
        + schemaTypeGUID
        + "/schema-attributes?elementStart=0&maxElements=100"
    )
    response = issueGet(getSchemaAttributesURL)
    schemaAttributes = response.json().get("list")
    if schemaAttributes:
        return schemaAttributes
    else:
        print("No Schema attributes retrieved")
        process_error_response(serverName, "fixme", serverPlatformURL, response)


def print_response(response):
    """

    Args:
        response:

    Returns:
        : str
    """
    prettyResponse = json.dumps(response.json(), indent=4)
    print(" ")
    print("Response: ")
    print(prettyResponse)
    print(" ")


def print_unexpected_response(
    serverName, serverPlatformName, serverPlatformURL, response
):
    """

    Args:
        serverName:
        serverPlatformName:
        serverPlatformURL:
        response:
    """
    if response.status_code == 200:
        relatedHTTPCode = response.json().get("relatedHTTPCode")
        if relatedHTTPCode == 200:
            print("Unexpected response from server " + serverName)
            print_response(response)
        else:
            exceptionErrorMessage = response.json().get("exceptionErrorMessage")
            exceptionSystemAction = response.json().get("exceptionSystemAction")
            exceptionUserAction = response.json().get("exceptionUserAction")
            if exceptionErrorMessage != None:
                print(exceptionErrorMessage)
                print(" * " + exceptionSystemAction)
                print(" * " + exceptionUserAction)
            else:
                print("Unexpected response from server " + serverName)
                print_response(response)
    else:
        print(
            "Unexpected response from server platform "
            + serverPlatformName
            + " at "
            + serverPlatformURL
        )
        print_response(response)


#
# Rest calls, these functions issue rest calls and print debug if required.
#

def issue_get(url): object
"""
Wrap a get request, validating the url first and raising an exception if needed
Args:
    url: the URL to issue an HTTP GET to 
Returns:
    object: the response object returned from the requests package

"""
    if isDebug:
        print_rest_request("GET " + url)
    jsonHeader = {"content-type": "application/json"}
    validate_url(url)
    response = requests.get(url, headers=jsonHeader, verify=False)
    if isDebug:
        print_rest_response(response)
    return response

def issue_post(
    url,
    body: json = {"class": "NullRequestBody"},
    headers: json = {"Content-Type": "application/json"}
    ):
    """

    Args:
        url:
        body:

    Returns:
        object:

    """
    response = None
    if isDebug:
        print_rest_request("POST " + url)
        print_rest_request_body(body)
    jsonHeader = {"content-type": "application/json"}
    # try:
    response = requests.post(url, json=body, headers=jsonHeader, verify=False)
    # except Exception as e:
    #     print(f"Exception in issue_post: {e}")

    if isDebug:
        print_rest_response(response)
    return response


def issue_data_post(url, body):
    """

    Args:
        url:
        body:

    Returns:
        response:

    """

    # jsonHeader = {'content-type': 'text/plain'}
    jsonHeader = {"content-type": "application/json"}
    response = requests.post(url, data=body, verify=False, headers=jsonHeader)
    return response


def issue_put(url, body):
    """

    Args:
        url:
        body:

    Returns:
        object:

    """
    if isDebug:
        print_rest_request("PUT " + url)
        print_rest_request_body(body)
    jsonHeader = {"content-type": "application/json"}
    response = requests.put(url, json=body, headers=jsonHeader, verify=False)
    if isDebug:
        print_rest_response(response)
    return response





def print_rest_request(url):
    """

    Args:
        url:
    """
    print(" ")
    print(url)


def print_rest_request_body(body):
    """

    Args:
        body:
    """
    prettyBody = json.dumps(body, indent=4)
    print(prettyBody)
    print(" ")


def print_rest_response(response):
    """

    Args:
        response:
    """
    print("Returns:")
    prettyResponse = json.dumps(response.json(), indent=4)
    print(prettyResponse)
    print(" ")


def process_error_response(serverName, serverPlatformName, serverPlatformURL, response):
    """

    Args:
        serverName:
        serverPlatformName:
        serverPlatformURL:
        response:

    Returns:

    """
    if response.status_code != 200:
        print_unexpected_response(
            serverName, serverPlatformName, serverPlatformURL, response
        )
    else:
        relatedHTTPCode = response.json().get("relatedHTTPCode")
        if relatedHTTPCode != 200:
            print_unexpected_response(
                serverName, serverPlatformName, serverPlatformURL, response
            )
    return []


def post_and_print_result(url, json=None, headers=None):
    """

    Args:
        url:
        json:
        headers:
    """
    print("   ...... (POST", url, ")")
    response = requests.post(url, json=json, headers=headers, verify=False)
    print("   ...... Response: ", response.json())


def print_guid_list(guids):
    if guids == None:
        print("No assets created")
    else:
        prettyGUIDs = json.dumps(guids, indent=4)
        print(prettyGUIDs)


def get_last_guid(guids):
    """

    Args:
        guids:

    Returns:

    """
    if guids == None:
        return "<unknown>"
    else:
        for guid in guids:
            returnGUID = guid
        return returnGUID
