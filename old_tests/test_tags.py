#
# This file tests Asset ratings
#

import urllib3.exceptions
from requests import ConnectTimeout, ConnectionError

from src.egeria_client.assetLib import print_asset_detail, print_asset_summary, Comment
from src.egeria_client.asset_consumer import AssetConsumer, AssetUniverse, print_comment_list
from src.egeria_client.utils import get_last_guid
import time
import sys

my_endpoint = "https://localhost:30081"
c = AssetConsumer('cocoMDS1', my_endpoint, 'peterprofile')

lg=None


# Find an asset we can play with and set the lg to the last asset GUID we find.
# Print any comments on the asset and then remove them.
try:

    guids = c.search_for_assets('.*')

    lg = get_last_guid(guids)
    print("Last Guid is " + lg)

    # response = c.create_public_tag("Peter_first_pub", "Peter's first public tag")
    # print(f"created a public tag with status of {response}")
    #
    # print("Now what happens if I pass a different user ID?")
    # response = c.create_public_tag("Peter_second_pub", "Peter's second public tag", "erinoverview")
    # print(f"created a public tag with status of {response}")
    response = c.find_tags(".*")
    print(response)


except (ConnectionError, ConnectTimeout) as e:
    print(f"A connection error occurred {e}")
except Exception as e:
    print(f"An exception occurred: {e}")
