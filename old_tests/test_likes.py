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
comment_guid_list = []
replies_list = []

# Find an asset we can play with and set the lg to the last asset GUID we find.
# Print any comments on the asset and then remove them.
try:

    guids = c.search_for_assets('.*')

    lg = get_last_guid(guids)
    print("Last Guid is " + lg)
    # status = c.add_like(lg,True, end_user_id='tanyatidie')
    # print(f"Added a like to {lg} with status of {status}")
    # response = c.add_rating(lg,"THREE_STARS", "meh", True, end_user_id='peterprofile')
    # if response:
    #     print(f"Added a like to {lg} with status of {response}")
    # else:
    #     print("there was no response on the add")
    # status = c.add_rating(lg, "TWO_STARS", "meh", True, end_user_id='garygeeke')
    # if status:
    #     print(f"Added a like to {lg} with status of {status}")
    # else:
    #     print("there was no response on the add")
    #
    # response = c.add_rating(lg, "FOUR_STARS", "hmm", True, end_user_id='peterprofile')
    # if response:
    #     print(f"Added a like to {lg} with status of {response}")
    # else:
    #     print("there was no response on the add")
    #
    response = c.remove_rating(lg, 'peterprofile')
    # print(f"tried to remove the added rating on {lg} with a response of {response}")
    response = c.remove_rating(lg, 'garygeeke')
    print(f"tried to remove the added rating on {lg} with a response of {response}")

except (ConnectionError, ConnectTimeout) as e:
    print(f"A connection error occurred {e}")
except Exception as e:
    print(f"An exception occurred: {e}")
