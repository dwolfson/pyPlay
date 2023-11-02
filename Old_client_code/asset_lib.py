# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
#
# OCF Common services
# Working with assets - this set of functions displays assets returned from the open metadata repositories.
#
# import utils
import requests
import json
from src.egeria_client.utils import process_error_response, issue_get


class Asset:
    pass


class AssetUniverse:
    pass


class Comment:
    """This class holds a comment object and is created by parsing
    a passed in JSON object containing comment information"""

    def __init__(self, comment_object: str):
        comment = comment_object.get("comment")
        self.replyCount = comment_object.get("replyCount")
        if not comment:
            print("no comment")
            return None
        self.comment_guid = comment.get("guid")
        self.comment_type = comment.get("commentType")
        self.comment_text = comment.get("commentText")
        self.comment_user = comment.get("user")
        self.is_public = comment.get("isPublic")
        # self.reply_count = comment.get('replyCount')

    def __str__(self):
        s = f"comment GUID: {self.comment_guid}\n"
        s = s + f"comment Type: {self.comment_type}\n"
        s = s + f"created by  : {self.comment_user}\n"
        s = s + f"public      : {self.is_public} \n"
        s = s + f"comment Text: {self.comment_text}\n"
        s = s + f"replies     : {self.replyCount} \n"
        return s


def print_asset_summary(asset):
    elementHeader = asset.get("elementHeader")
    elementType = elementHeader.get("type")
    assetTypeName = elementType.get("typeName")
    requestType = elementHeader.get("guid")
    assetProperties = asset.get("assetProperties")
    assetQualifiedName = assetProperties.get("qualifiedName")
    print(assetQualifiedName)
    print(assetTypeName + " \t| " + requestType + " | " + assetQualifiedName)


def print_asset_detail(asset):
    elementHeader = asset.get("elementHeader")
    elementType = elementHeader.get("type")
    assetTypeName = elementType.get("typeName")
    assetSuperTypes = elementType.get("superTypeNames")
    requestType = elementHeader.get("guid")
    assetProperties = asset.get("assetProperties")
    assetQualifiedName = assetProperties.get("qualifiedName")
    assetDisplayName = assetProperties.get("displayName")
    assetCatalogBean = assetProperties.get("description")
    assetOwner = assetProperties.get("owner")
    assetOrigin = assetProperties.get("otherOriginValues")
    assetOwnerType = assetProperties.get("ownerTypeName")
    assetZones = assetProperties.get("zoneMembership")
    assetLatestChange = assetProperties.get("latestChange")
    if not requestType:
        requestType = "<null>"
    if not assetDisplayName:
        assetDisplayName = "<none>"
    print(assetDisplayName + " [" + requestType + "]")
    if not assetQualifiedName:
        assetQualifiedName = "<null>"
    print("  qualifiedName: " + assetQualifiedName)
    if assetCatalogBean:
        print("  description:   " + assetCatalogBean)
    print(
        "  type:          "
        + assetTypeName
        + " [%s]" % ", ".join(map(str, assetSuperTypes))
    )
    if assetOwner:
        print("  owner:         " + assetOwner + " [" + assetOwnerType + "]")
    if assetOrigin:
        contact = assetOrigin.get("contact")
        dept = assetOrigin.get("originatingDept")
        org = assetOrigin.get("originatingOrganization")
        print("  origin:        contact=" + contact + ", dept=" + dept + ", org=" + org)
    if assetZones:
        print("  zones:         " + "%s" % ", ".join(map(str, assetZones)))
    if assetLatestChange:
        print("  latest change: " + assetLatestChange)


def print_asset_list_summary(assets):
    print(" ")
    for x in range(len(assets)):
        printAssetSummary(assets[x])


def print_asset_list_detail(assets):
    print("\n--------------------------------------\n")
    for x in range(len(assets)):
        printAssetDetail(assets[x])
        print("\n--------------------------------------\n")


def print_guid_list(guids):
    if guids == None:
        print("No assets created")
    else:
        prettyGUIDs = json.dumps(guids, indent=4)
        print(prettyGUIDs)


def get_last_guid(guids):
    if guids == None:
        return "<unknown>"
    else:
        for guid in guids:
            returnGUID = guid
        return returnGUID


def get_asset_universe(
    serverName,
    serverPlatformName,
    serverPlatformURL,
    serviceURLMarker,
    userId,
    requestType,
) -> json:
    connectedAssetURL = (
        serverPlatformURL
        + "/servers/"
        + serverName
        + "/open-metadata/common-services/"
        + serviceURLMarker
        + "/connected-asset/users/"
        + userId
    )
    getAsset = connectedAssetURL + "/assets/" + requestType
    response = issue_get(getAsset)
    asset = response.json().get("asset")
    if asset:
        return response.json()
    else:
        print("No Asset returned")
        process_error_response(serverName, "fixme", serverPlatformURL, response)


def print_comment_list(responseObjects):
    print(" ")
    if len(responseObjects) == 0:
        print("No comments found")
    else:
        if len(responseObjects) == 1:
            print("1 comment found:")
        else:
            print(str(len(responseObjects)) + " comments found:")
    for x in range(len(responseObjects)):
        print_comment(responseObjects[x])


def print_asset_comments(
    serverName,
    serverPlatformName,
    serverPlatformURL,
    serviceURLMarker,
    userId,
    asset_guid,
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
        + asset_guid
        + "/comments?elementStart=0&maxElements=50"
    )
    response = issue_get(commentQuery)
    responseObjects = response.json().get("list")

    if responseObjects:
        print_comment_list(responseObjects)
    else:
        print("No comments returned")
        process_error_response(serverName, "fixme", serverPlatformURL, response)


def print_asset_comment_replies(
    serverName,
    serverPlatformName,
    serverPlatformURL,
    serviceURLMarker,
    userId,
    requestType,
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
        + requestType
        + "/comments/"
        + commentGUID
        + "/replies?elementStart=0&maxElements=50"
    )
    response = issue_get(commentReplyQuery)
    responseObjects = response.json().get("list")
    if responseObjects:
        print_comment_list(responseObjects)
    else:
        print("No comments returned")
        process_error_response(serverName, "fixme", serverPlatformURL, response)


def print_asset_universe(
    serverName,
    serverPlatformName,
    serverPlatformURL,
    serviceURLMarker,
    userId,
    asset_guid,
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
    getAsset = connectedAssetURL + "/assets/" + asset_guid
    print(" ")
    print("GET " + getAsset)
    #    response = requests.get(getAsset, ssl_verify=False)
    response = issue_get(getAsset)
    print("Returns:")
    prettyResponse = json.dumps(response.json(), indent=4)
    print(prettyResponse)
    print(" ")


def print_related_assets(
    serverName,
    serverPlatformName,
    serverPlatformURL,
    serviceURLMarker,
    userId,
    requestType,
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
    getRelatedAsset = (
        connectedAssetURL
        + "/assets/"
        + requestType
        + "/related-assets?elementStart=0&maxElements=50"
    )
    print(" ")
    print("GET " + getRelatedAsset)
    response = requests.get(getRelatedAsset, verify=False)
    print("Returns:")
    prettyResponse = json.dumps(response.json(), indent=4)
    print(prettyResponse)
    print(" ")


def print_comment2(commentObject):
    c = Comments(commentObject)
    print(c)


def print_comment(commentObject):
    if commentObject:
        comment = commentObject.get("comment")
        #    print(comment)
        print("in print_comment")
        replyCount = commentObject.get("replyCount")
        if comment:
            comment_guid = comment.get("guid")
            comment_type = comment.get("commentType")
            comment_text = comment.get("commentText")
            comment_user = comment.get("user")
            # comment_replies = comment.get('replyCount')
            isPublic = comment.get("isPublic")
            if comment_guid:
                print("  comment guid:  " + comment_guid)
            if comment_type:
                print("  comment type: " + comment_type)
            if comment_text:
                print("  comment text: " + comment_text)
            if comment_user:
                print("  created by:   " + comment_user)
            if isPublic:
                print("  public:       " + str(isPublic))
            if replyCount:
                print(" # Replies: " + replyCount)


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
        process_error_response(
            serverName, serverPlatformName, serverPlatformURL, response
        )
