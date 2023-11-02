# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
#   
import basic_utils
#
# Working with assets - this set of functions are for authoring assets.
# Using the Asset Owner OMAS interface to create and query assets.  Notice that the interface returns all of the asset contents.
# 

def assetOwnerCreateAsset(assetTypeURL, serverName, serverPlatformName, serverPlatformURL, userId, displayName, description, fullPath):
    assetOwnerURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/access-services/asset-owner/users/' + userId
    createAssetURL = assetOwnerURL + assetTypeURL
        
    createAssetBody = {
        "class" : "NewCSVFileAssetRequestBody",
        "displayName" : displayName,
        "description" : description,
        "fullPath" : fullPath
    }
    response=issuePost(createAssetURL, createAssetBody)
    guids = response.json().get('guids')
    if guids:
        return guids
    else:
        print ("No assets created")
        processErrorResponse(serverName, serverPlatformName, serverPlatformURL, response)
    
def assetOwnerCreateAsset(assetTypeURL, serverName, serverPlatformName, serverPlatformURL, userId, displayName, description, fullPath):
    assetOwnerURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/access-services/asset-owner/users/' + userId
    createAssetURL = assetOwnerURL + assetTypeURL
    jsonHeader = {'content-type':'application/json'}
    createAssetBody = {
        "class" : "NewCSVFileAssetRequestBody",
        "displayName" : displayName,
        "description" : description,
        "fullPath" : fullPath
    }
    response=issuePost(createAssetURL, createAssetBody)
    guids = response.json().get('guids')
    if guids:
        return guids
    else:
        print ("No assets created")
        processErrorResponse(serverName, serverPlatformName, serverPlatformURL, response)
    
def assetOwnerCreateCSVAsset(serverName, serverPlatformName, serverPlatformURL, userId, displayName, description, fullPath):
    return assetOwnerCreateAsset('/assets/data-files/csv', serverName, serverPlatformName, serverPlatformURL, userId, displayName, description, fullPath)

def assetOwnerCreateAvroAsset(serverName, serverPlatformName, serverPlatformURL, userId, displayName, description, fullPath):
    return assetOwnerCreateAsset('/assets/data-files/avro', serverName, serverPlatformName, serverPlatformURL, userId, displayName, description, fullPath)

def assetOwnerCreateCSVAssetWithColumnHeaders(serverName, serverPlatformName, serverPlatformURL, userId, displayName, description, fullPath, columnHeaders):
    assetOwnerURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/access-services/asset-owner/users/' + userId
    createAssetURL = assetOwnerURL + '/assets/data-files/csv'
    createAssetBody = {
        "class" : "NewCSVFileAssetRequestBody",
        "displayName" : displayName,
        "description" : description,
        "fullPath" : fullPath,
        "columnHeaders" : columnHeaders
    }
    response=issuePost(createAssetURL, createAssetBody)
    guids = response.json().get('guids')
    if guids:
        return guids
    else:
        print ("No CSV assets created")
        processErrorResponse(serverName, serverPlatformName, serverPlatformURL, response)

def assetOwnerGetSchemaAttributesFromSchemaType(serverName, serverPlatformName, serverPlatformURL, serviceURLMarker, userId, schemaTypeGUID):
    return getSchemaAttributesFromSchemaType(serverName, serverPlatformName, serverPlatformURL, serviceURLMarker, userId, schemaTypeGUID)
        
# Delete the asset with the supplied guid.     
def assetOwnerDelete(serverName, serverPlatformName, serverPlatformURL, userId, assetGUID):
    assetOwnerURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/access-services/asset-owner/users/' + userId
    deleteAssetURL = assetOwnerURL + '/assets/"+ assetGUID + "/delete'
    response=issuePost(deleteAssetURL, {})

    if relatedHTTPCode == 200:
        print ("deleted Asset")
        return []
    else:    
        processErrorResponse(serverName, serverPlatformName, serverPlatformURL, response)
        
def assetOwnerSearchForAssets(serverName, serverPlatformName, serverPlatformURL, userId, searchString):
    assetOwnerURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/access-services/asset-owner/users/' + userId
    getAssetsURL = assetOwnerURL + '/assets/by-search-string?startFrom=0&pageSize=50'
    response = issueDataPost(getAssetsURL, searchString)
    if response:
        assets = response.json().get('assets')
        if assets:
            return assets
        else:
            print ("No assets found")
            processErrorResponse(serverName, serverPlatformName, serverPlatformURL, response)
    else:
        print ("Search Request Failed")        

def assetOwnerPrintAssets(serverName, serverPlatformName, serverPlatformURL, userId, searchString):
    assets = assetOwnerSearchForAssets(serverName, serverPlatformName, serverPlatformURL, userId, searchString)
    if assets:
        if len(assets) == 1:
            print ("1 asset found:")
        else:
            print (str(len(assets)) + " assets found:")
        printAssetListSummary(assets)
        printAssetListDetail(assets)
        
def assetOwnerFindAssetQualifiedName(serverName, serverPlatformName, serverPlatformURL, userId, searchString):
    qualifiedName = None
    assets = None
    assets = assetOwnerSearchForAssets(serverName, serverPlatformName, serverPlatformURL, userId, searchString)
    if assets == None:
        time.sleep(1)
        assets = assetOwnerSearchForAssets(serverName, serverPlatformName, serverPlatformURL, userId, searchString)
    if assets:
        if len(assets) == 1:
            assetProperties = assets[0].get('assetProperties')
            qualifiedName = assetProperties.get('qualifiedName')
        else:
            print (str(len(assets)) + " assets found:")
    return qualifiedName

def assetOwnerDeleteAssets(serverName, serverPlatformName, serverPlatformURL, userId, searchString):
    assets = assetOwnerSearchForAssets(serverName, serverPlatformName, serverPlatformURL, userId, searchString)
    if assets:
        if len(assets) == 1:
            print ("1 asset to delete")
        else:
            print (str(len(assets)) + " assets to delete:")
        for asset in assets:
            elementHeader = asset.get('elementHeader')
            assetGUID = elementHeader.get('guid')
            assetProperties = asset.get('assetProperties')
            assetQualifiedName = assetProperties.get('qualifiedName')
            print("Deleting asset " + assetQualifiedName)
            assetOwnerCreateAssetDelete(serverName, serverPlatformName, serverPlatformURL, userId, assetGUID)

def addOwner(serverName, serverPlatformName, serverPlatformURL, userId, assetName, assetGUID, assetOwner, ownerType):
    governanceURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/access-services/asset-owner/users/' + userId 
    print ("Setting owner on " + assetName + " to " + assetOwner + " ...")
    body = {
        "class" : "OwnerRequestBody",
        "ownerType" : ownerType,
        "ownerId" : assetOwner
    }
    addOwnerURL = governanceURL + "/assets/" + assetGUID + "/owner"
    response=issuePost(addOwnerURL, body)
    if response.status_code != 200:
        processErrorResponse(serverName, serverPlatformName, serverPlatformURL, response)
        
def addOrigin(serverName, serverPlatformName, serverPlatformURL, userId, assetName, assetGUID, contact, originatingDept, originatingOrganization):
    governanceURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/access-services/asset-owner/users/' + userId 
    print ("Setting origin on " + assetName + " ...")
    body = {
        "class" : "OriginRequestBody",
        "otherOriginValues" : {
            "originatingOrganization" : originatingOrganization,
            "originatingDept" : originatingDept,
            "contact" : contact
        }
    }
    addOriginURL = governanceURL + "/assets/" + assetGUID + "/origin"
    response=issuePost(addOriginURL, body)
    if response.status_code != 200:
        processErrorResponse(serverName, serverPlatformName, serverPlatformURL, response)
        
def addZones(serverName, serverPlatformName, serverPlatformURL, userId, assetName, assetGUID, zones):
    print ("Setting governance zones on " + assetName + " ...")
    governanceURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/access-services/asset-owner/users/' + userId 
    
    addZonesURL = governanceURL + "/assets/" + assetGUID + "/governance-zones"
    response=issuePost(addZonesURL, zones)
    if response.status_code != 200:
        processErrorResponse(serverName, serverPlatformName, serverPlatformURL, response)

                      
# Create a semantic assignment between an Asset's attachment - like a Schema Type - and Glossary Term 
def createSemanticAssignment(serverName, serverPlatformName, serverPlatformURL, userId, assetGUID, schemaTypeGUID, glossaryTermGUID):                
    assetOwnerURL = serverPlatformURL + '/servers/' + serverName + '/open-metadata/access-services/asset-owner/users/' + userId
    semanticAssignmentURL =  assetOwnerURL + '/assets/' + assetGUID + '/attachments/' + schemaTypeGUID + '/meanings/' + glossaryTermGUID
    response=issuePost(semanticAssignmentURL, {})
    if response.status_code == 200:
        print("Semantic assignment relationship created") 
    else:
        print ("No semantic assignment Relationship created")
        processErrorResponse(serverName, serverPlatformName, serverPlatformURL, response)