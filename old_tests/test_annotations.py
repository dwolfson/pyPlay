from src.egeria_client.assetLib import print_asset_detail, print_asset_summary, Comment
from src.egeria_client.asset_consumer import AssetConsumer, AssetUniverse, print_comment_list
from src.egeria_client.utils import get_last_guid
import time

my_endpoint = "https://wolfsonnet.me:30081"

c = AssetConsumer('cocoMDS1', my_endpoint, 'peterprofile')
lg=None
comment_guid_list = []


# Find an asset we can play with and set the lg to the last asset GUID we find.
# Print any comments on the asset and then remove them.
try:
    print(c.search_for_assets('.*'))  # returns a list of GUIDS in c.guids
    lg = get_last_guid(c.guids)
    print("Last Guid is " + lg)
    comments_list = c.get_comments(lg)
    if comments_list:
        print(f"There are  {len(comments_list)} comments on this last asset:")
        print_comment_list(comments_list)
        print(f"Now we will remove all the comments we found above")
        # for i in range(len(comments_list)):
        #     status = c.remove_comment(lg, comments_list[i].comment_guid)
        for i in comments_list:
             status = c.remove_comment(lg, i.comment_guid)

        time.sleep(2)
        comments_list = c.get_comments(lg)
        if comments_list is None:
            print("All comments successfully removed")
            comments_list = []
        else:
            print(f"there seem to be {len(comments_list)} comments left?")
            print_comment_list(comments_list)
    else:
        print("There were no comments to remove")

except Exception as e:
    print(e)
