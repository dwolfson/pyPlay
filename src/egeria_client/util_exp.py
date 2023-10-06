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
import sys
import inspect


comment_types = ("ANSWER", "OTHER", "QUESTION", "STANDARD_COMMENT", "SUGGESTION", "USAGE_EXPERIENCE")
star_ratings = ("FIVE_STARS", "FOUR_STARS", "NO_RECOMMENDATION", "ONE_STAR", "THREE_STARS", "TWO_STARS")



class EgeriaErrorCode(Enum):
    def __str__(self):
        return ("http_error_code=" + self.value["http_error_code"] +
                "messageId=" + self.value["message_id"] +
                ", message=" + self.value["message_template"] +
                ", systemAction=" + self.value["system_action"] +
                ", userAction=" + self.value["user_action"]
                )

class RESTClientConnectorErrorCodes(EgeriaErrorCode):
    CLIENT_SIDE_REST_API_ERROR = dict(http_error_code='503', message_id="CLIENT-SIDE-REST-API-CONNECTOR-503-002",
                                    message_template="A client-side exception {0} was received by method {1} from\
                                     API call {2} to server {3} on platform {4}.  The error message was {5}",
                                    system_action="The client has issued a call to the open metadata access service\
                                     REST API in a remote server and has received an exception from the local client libraries.",
                                    user_action="Review the error message to determine the cause of the error.\
                                     Check that the server is running an the URL is correct. Look for errors in\
                                      the local server's console to understand and correct the cause of the error. \
                                      Then rerun the request")
    EXCEPTION_RESPONSE_FROM_API = dict(http_error_code="503", message_id="CLIENT-SIDE-REST-API-CONNECTOR-503-003 ",
                                message_template = "A {0} exception was received from REST API call {1} to server \
                                {2}: error message was: {3}",
                                system_action = "The system has issued a call to an open metadata access service\
                                 REST API in a remote server and has received an exception response.",
                                user_action = "The error message should indicate the cause of the error. \
                                 Otherwise look for errors in the remote server's audit log and console to understand \
                                 and correct the source of the error.")

class OMAGCommonErrorCode(EgeriaErrorCode):
    SERVER_URL_NOT_SPECIFIED = dict(http_error_code='400', message_id="OMAG-COMMON-400-001",
                                    message_template="The OMAG Server Platform URL is null",
                                    system_action="The system is unable to identify the OMAG Server Platform.",
                                    user_action="Create a new client and pass the URL for the server on the constructor.")

    SERVER_URL_MALFORMED = dict(http_error_code='400', message_id="OMAG-COMMON-400-002",
                                message_template="The OMAS Server URL: {0} is not in a recognized format",
                                system_action="The system is unable to connect to the OMAG Server Platform to fulfill any requests.",
                                user_action="Create a new client and pass the correct URL for the server on the constructor.")

    SERVER_NAME_NOT_SPECIFIED = dict(http_error_code='400', message_id="OMAG-COMMON-400-003",
                                     message_template="The OMAG Server name is null",
                                     system_action="The system is unable to locate to the OMAG Server to fulfill any request.",
                                     user_action="Create a new client and pass the correct name for the server on the constructor.")

    NULL_USER_ID = dict(http_error_code='400', message_id="OMAG-COMMON-400-004",
                        message_template="The user identifier (user_id) passed on the {0} operation is null",
                        system_action="The system is unable to process the request without a user id..",
                        user_action="Correct the code in the caller to provide the user id.")

    NULL_GUID = dict(http_error_code='400', message_id="OMAG-COMMON-400-005",
                     message_template="The unique identifier (guid) passed on the {0} parameter of the {1} operation is null",
                     system_action="The system is unable to process the request without a guid.",
                     user_action="Correct the code in the caller to provide the guid.")

    NULL_NAME = dict(http_error_code='400', message_id="OMAG-COMMON-400-006",
                     message_template="The name passed on the {0} parameter of the {1} operation is null",
                     system_action="The system is unable to process the request without a name.",
                     user_action="Correct the code in the caller to provide the name on the parameter.")

    NULL_ARRAY_PARAMETER = dict(http_error_code='400', message_id="OMAG-COMMON-400-007",
                                message_template="The array value passed on the {0} parameter of the {1} operation is null or empty",
                                system_action="The system is unable to process the request without this value.",
                                user_action="Correct the code in the caller to provide the array.")

    NEGATIVE_START_FROM = dict(http_error_code='400', message_id="OMAG-COMMON-400-008",
                               message_template="The starting point for the results {0}, passed on the {1} parameter of the {2} operation, is negative",
                               system_action="The system is unable to process the request with this invalid value.  It should be zero for the start of the values, or a number greater than 0 to start partway down the list.",
                               user_action="Correct the code in the caller to provide a non-negative value for the starting point.")

    NEGATIVE_PAGE_SIZE = dict(http_error_code='400', message_id="OMAG-COMMON-400-009",
                              message_template="The page size for the results {0}, passed on the {1} parameter of the {2} operation, is negative",
                              system_action="The system is unable to process the request with this invalid value.  It should be zero to return all the result, or greater than zero to set a maximum.",
                              user_action="Correct the code in the caller to provide a non-negative value for the page size.")

    MAX_PAGE_SIZE = dict(http_error_code='400', message_id="OMAG-COMMON-400-010",
                         message_template="The number of records to return, {0}, passed on the {1} parameter of the {2} operation, is greater than the allowable maximum of {3}",
                         system_action="The system is unable to process the request with this page size value.",
                         user_action="Correct the code in the caller to provide a smaller page size.")

    NULL_ENUM = dict(http_error_code='400', message_id="OMAG-COMMON-400-012",
                     message_template="The enumeration value passed on the {0} parameter of the {1} operation is null",
                     system_action="The system is unable to process the request without a enumeration value.",
                     user_action="Correct the code in the caller to provide the enumeration value.")

    NULL_TEXT = dict(http_error_code='400', message_id="OMAG-COMMON-400-013",
                     message_template="The text field passed on the {0} parameter of the {1} operation is null",
                     system_action="The system is unable to process the request without this text value.",
                     user_action="Correct the code in the caller to provide a value in the text field.")

    NULL_OBJECT = dict(http_error_code='400', message_id="OMAG-COMMON-400-015",
                       message_template="The object passed on the {0} parameter of the {1} operation is null",
                       system_action="The system is unable to process the request without this object.",
                       user_action="Correct the code in the caller to provide the object.")

    NULL_SEARCH_STRING = dict(http_error_code='400', message_id="OMAG-COMMON-400-022",
                              message_template="The search string passed on the {0} parameter of the {1} operation is null",
                              system_action="The system is unable to process the request without a search string.",
                              user_action="Correct the code in the caller to provide the search string.")



class EgeriaException(Exception):
    def __init__(self, error_msg: str , class_name: str, action_description: str,
                 error_code: EgeriaErrorCode, params: [str]) :
        self.error_msg = error_msg
        self.class_name = class_name
        self.action_description = action_description
        self.http_error_code = error_code.value["http_error_code"]
        self.message_id = error_code.value["message_id"]
        self.message_template = error_code.value["message_template"]
        self.system_action = error_code.value["system_action"]
        self.user_action = error_code.value["user_action"]
        self.params = params
    def __str__(self ):
        return (self.error_msg + \
                " occurred in class: " + self.class_name +\
                " in method: " + self.action_description
                )

class InvalidParameterException(EgeriaException):
    """ Exception due to invalid parameters such as one of the parameters is null or invalid"""

    def __init__(self, error_msg: str, class_name: str, action_description: str,
                 error_code: OMAGCommonErrorCode, params: [str]):

        EgeriaException.__init__(self, error_msg, class_name, action_description, error_code, params)



class PropertyServerException(EgeriaException):
    """Exception due to a problem retrieving information from the property server"""
    def __init__(self, error_msg: str, class_name: str, action_description: str,
                 error_code: OMAGCommonErrorCode, params: [str]):
        EgeriaException.__init__(self, error_msg, class_name, action_description, error_code, params)

class UserNotAuthorizedException(EgeriaException):
    """ Exception as the requesting user is not authorized to issue this request"""
    pass

class RESTConnectionException(EgeriaException):
    """ Exception that wraps exceptions coming from the Request package """
    def __init__(self, error_msg: str, class_name: str, action_description: str,
                 error_code: RESTClientConnectorErrorCodes, params: [str]):
        EgeriaException.__init__(self, error_msg, class_name, action_description, error_code, params)


"""

Validators and error handlers for common parameters

"""
max_paging_size = 100


def validate_user_id(user_id: str, class_name, method_name) -> bool:
    if (user_id is None) or len(user_id) == 0:
        msg = str(OMAGCommonErrorCode.NULL_USER_ID.value["message_template"])
        raise InvalidParameterException(msg, class_name, sys._getframe(2).f_code,
                                        OMAGCommonErrorCode.NULL_USER_ID, None)
    else:
        return True


def validate_server_name(server_name: str, class_name, method_name)-> bool:
    if (server_name is None) or (len(server_name)==0):
        msg = str(OMAGCommonErrorCode.SERVER_NAME_NOT_SPECIFIED.value["message_template"])
        raise InvalidParameterException(msg, class_name, sys._getframe(2).f_code,
                                        OMAGCommonErrorCode.SERVER_NAME_NOT_SPECIFIED, None)
    else:
        return True

def validate_guid(guid: str, class_name, method_name)-> bool:
    if (guid is None) or (len(guid)==0):
        msg = str(OMAGCommonErrorCode.NULL_GUID.value["message_template"])
        raise InvalidParameterException(msg, class_name, sys._getframe(2).f_code,
                                        OMAGCommonErrorCode.NULL_GUID, None)
    else:
        return True

def validate_name(name: str, class_name, method_name)-> bool:
    if (name is None) or (len(name)==0):
        msg = str(OMAGCommonErrorCode.NULL_NAME.value["message_template"])
        raise InvalidParameterException(msg, class_name, sys._getframe(2).f_code,
                                        OMAGCommonErrorCode.NULL_NAME, None)
    else:
        return True

def validate_search_string(search_string: str, class_name, method_name)-> bool:
    if (search_string is None) or (len(search_string)==0):
        msg = str(OMAGCommonErrorCode.NULL_SEARCH_STRING.value["message_template"])
        raise InvalidParameterException(msg, class_name, sys._getframe(2).f_code,
                                        OMAGCommonErrorCode.NULL_SEARCH_STRING, None)
    else:
        return True


def validate_public():
    pass


def validate_url(url: str, class_name, method_name) -> bool:
    if (url is None) or (len(url) == 0):
        msg = str(OMAGCommonErrorCode.SERVER_URL_NOT_SPECIFIED.value["message_template"])
        raise InvalidParameterException(msg, class_name, sys._getframe(2).f_code,
                                        OMAGCommonErrorCode.SERVER_URL_NOT_SPECIFIED,None)

    result = validators.url(url)
    # print(f"validation result is {result}")
    if result is not True:
        msg = OMAGCommonErrorCode.SERVER_URL_MALFORMED.value["message_template"].format(url)
        raise InvalidParameterException(msg, sys._getframe(2).f_code, sys._getframe(1).f_code.co_name,
                                        OMAGCommonErrorCode.SERVER_URL_MALFORMED, url)
    else:
        return True

#
# Rest calls, these functions issue rest calls and print debug if required.
#
def issue_post(url, method_name,
               body: json = {"class": "NullRequestBody"},
               headers: json = {'Content-Type': 'application/json'}):
    """

    Args:
        url:
        body:

    Returns:
        object:

    """
    response = None
    validate_url(url, "class?",method_name)

    try:
        response = requests.post(url, json=body, headers=headers, verify=False)
    except (ConnectionError, TimeoutError) as e:
        msg = RESTClientConnectorErrorCodes.CLIENT_SIDE_REST_API_ERROR.value["message_template"].format(e, \
            method_name, sys._getframe(2).f_code, url)
        raise RESTConnectionException(msg, sys._getframe(2).f_code, sys._getframe(1).f_code.co_name,
                                        RESTClientConnectorErrorCodes.CLIENT_SIDE_REST_API_ERROR, url)

    if response.status_code != 200:
        print_unexpected_response(serverName, serverPlatformName, serverPlatformURL, response)
    else:
        relatedHTTPCode = response.json().get('relatedHTTPCode')
        if relatedHTTPCode != 200:
            print_unexpected_response(serverName, serverPlatformName, serverPlatformURL, response)
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
    jsonHeader = {'content-type': 'application/json'}
    response = requests.post(url, data=body, verify=False, headers=jsonHeader)
    return (response)


def issue_put(url, body):
    """

    Args:
        url:
        body:

    Returns:
        object:

    """
    if (isDebug):
        print_rest_request("PUT " + url)
        print_rest_request_body(body)
    jsonHeader = {'content-type': 'application/json'}
    response = requests.put(url, json=body, headers=jsonHeader, verify=False)
    if (isDebug):
        print_rest_response(response)
    return response


def issue_get(url):
    """

    Args:
        url:

    Returns:
        object:

    """
    if (isDebug):
        print_rest_request("GET " + url)
    jsonHeader = {'content-type': 'application/json'}
    response = requests.get(url, headers=jsonHeader, verify=False)
    if (isDebug):
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
        print_unexpected_response(serverName, serverPlatformName, serverPlatformURL, response)
    else:
        relatedHTTPCode = response.json().get('relatedHTTPCode')
        if relatedHTTPCode != 200:
            print_unexpected_response(serverName, serverPlatformName, serverPlatformURL, response)
    return []




def print_guid_list(guids):
    if guids == None:
        print("No assets created")
    else:
        prettyGUIDs = json.dumps(guids, indent=4)
        print(prettyGUIDs)


#
# OCF Common services
# Working with assets - this set of functions displays assets returned from the open metadata repositories.
#
class comment():
    def __init__(self, comment_guid: str, comment_type: str, comment_text: str, comment_owner: str, is_public: bool):
        self.comment_guid: str = comment_guid
        self.comment_type: str = comment_type
        self.comment_text: str = comment_text
        self.comment_owner: str = comment_owner
        self.is_public: bool = is_public

        if self.comment_type not in comment_types:
            raise ValueError(comment_type + " is an Invalid comment type")


def getAssetUniverse(serverName, serverPlatformName, serverPlatformURL, serviceURLMarker, userId, assetGUID):
    connectedAssetURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/common-services/' + serviceURLMarker + '/connected-asset/users/' + userId
    getAsset = connectedAssetURL + '/assets/' + assetGUID
    response = issueGet(getAsset)
    asset = response.json().get('asset')
    if asset:
        return response.json()
    else:
        print("No Asset returned")
        process_error_response(serverName, 'fixme', serverPlatformURL, response)


def get_related_assets(serverName, serverPlatformName, serverPlatformURL, serviceURLMarker, userId, assetGUID):
    connectedAssetURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/common-services/' + serviceURLMarker + '/connected-asset/users/' + userId
    getRelatedAsset = connectedAssetURL + '/assets/' + assetGUID + '/related-assets?elementStart=0&maxElements=50'
    response = issueGet(getRelatedAsset)
    if response.status_code == 200:
        relatedHTTPCode = response.json().get('relatedHTTPCode')
        if relatedHTTPCode == 200:
            return response.json().get('list')
        else:
            printUnexpectedResponse(serverName, serverPlatformName, serverPlatformURL, response)
    else:
        printUnexpectedResponse(serverName, serverPlatformName, serverPlatformURL, response)


def getComments(serverName, serverPlatformName, serverPlatformURL, serviceURLMarker, userId, assetGUID):
    connectedAssetURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/common-services/' + serviceURLMarker + '/connected-asset/users/' + userId
    commentQuery = connectedAssetURL + '/assets/' + assetGUID + '/comments?elementStart=0&maxElements=50'
    response = issueGet(commentQuery)
    responseObjects = response.json().get('list')
    if responseObjects:
        return responseObjects
    else:
        print("No comments returned")
        process_error_response(serverName, 'fixme', serverPlatformURL, response)


def getCommentReplies(serverName, serverPlatformName, serverPlatformURL, serviceURLMarker, userId, assetGUID,
                      commentGUID):
    connectedAssetURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/common-services/' + serviceURLMarker + '/connected-asset/users/' + userId
    commentReplyQuery = connectedAssetURL + '/assets/' + assetGUID + '/comments/' + commentGUID + '/replies?elementStart=0&maxElements=50'
    response = issueGet(commentReplyQuery)
    responseObjects = response.json().get('list')
    if responseObjects:
        return responseObjects
    else:
        print("No comments returned")
        process_error_response(serverName, 'fixme', serverPlatformURL, response)


def getAPIOperations(serverName, serverPlatformName, serverPlatformURL, serviceURLMarker, userId, apiSchemaTypeGUID):
    connectedAssetURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/common-services/' + serviceURLMarker + '/connected-asset/users/' + userId
    requestURL = connectedAssetURL + '/assets/schemas/apis/' + apiSchemaTypeGUID + '/api-operations?elementStart=0&maxElements=50'
    response = issueGet(requestURL)
    responseObjects = response.json().get('list')
    if response.status_code == 200:
        relatedHTTPCode = response.json().get('relatedHTTPCode')
        if relatedHTTPCode == 200:
            return response.json().get('list')
        else:
            printUnexpectedResponse(serverName, serverPlatformName, serverPlatformURL, response)
    else:
        printUnexpectedResponse(serverName, serverPlatformName, serverPlatformURL, response)


def getSchemaAttributesFromSchemaType(serverName, serverPlatformName, serverPlatformURL, serviceURLMarker, userId,
                                      schemaTypeGUID):
    ocfURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/common-services/' + serviceURLMarker + '/connected-asset/users/' + userId
    getSchemaAttributesURL = ocfURL + '/assets/schemas/' + schemaTypeGUID + '/schema-attributes?elementStart=0&maxElements=100'
    response = issueGet(getSchemaAttributesURL)
    schemaAttributes = response.json().get('list')
    if schemaAttributes:
        return schemaAttributes
    else:
        print("No Schema attributes retrieved")
        process_error_response(serverName, 'fixme', serverPlatformURL, response)


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


def print_unexpected_response(serverName, serverPlatformName, serverPlatformURL, response):
    """

    Args:
        serverName:
        serverPlatformName:
        serverPlatformURL:
        response:
    """
    if response.status_code == 200:
        relatedHTTPCode = response.json().get('relatedHTTPCode')
        if relatedHTTPCode == 200:
            print("Unexpected response from server " + serverName)
            print_response(response)
        else:
            exceptionErrorMessage = response.json().get('exceptionErrorMessage')
            exceptionSystemAction = response.json().get('exceptionSystemAction')
            exceptionUserAction = response.json().get('exceptionUserAction')
            if exceptionErrorMessage != None:
                print(exceptionErrorMessage)
                print(" * " + exceptionSystemAction)
                print(" * " + exceptionUserAction)
            else:
                print("Unexpected response from server " + serverName)
                print_response(response)
    else:
        print("Unexpected response from server platform " + serverPlatformName + " at " + serverPlatformURL)
        print_response(response)




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
