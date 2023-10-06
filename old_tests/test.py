from src.egeria_client.assetLib import print_asset_detail, print_asset_summary
from src.egeria_client.asset_consumer import AssetConsumer, AssetUniverse
from src.egeria_client.utils import get_last_guid


my_endpoint = "https://wolfsonnet.me:30081"

c = AssetConsumer('cocoMDS1', my_endpoint, 'peterprofile')
lg=None
# print(c.find_assets('.*'))
try:
    print(c.print_asset_guids('.*'))
    lg = get_last_guid(c.guids)
    print("Last Guid is " + lg)
except Exception as e:
    print(e)

try:
#    guid1 = c.add_comment(lg,"question 1","QUESTION",True)
    c.print_comments(lg)

    comments1 = c.get_comments(lg)

    print(comments1)
#    update_comment(lg, comment_guid: str, comment_text: str, comment_type: , True)
except Exception as e:
    print(e)
#    guid2 = c.add_comment_to_asset(lg,"question 2","QUESTION","True")
#    print(guid1, guid2)
#    guid3= c.add_reply_to_asset_comment(lg,"reply 1","ANSWER",True)
#    u = c.asset_consumer_print_asset_universe(lg)
#    guid3 = c.add_reply_to_asset_comment(lg,"5cd575c3-d6a1-4973-8d27-35c7f095aeb7","reply 1", "ANSWER", True)
#    print(guid3)
#   comment_guid = c.add_comment(lg,'This is the first comment', 'OTHER',True)
#   print('comment guid is: '+ comment_guid)
#
#   c.update_comment(lg,comment_guid,'This is updated text','OTHER',True)
#    c.remove_comment(lg, comment_guid)
#    c.print_asset_consumer_comments(lg)
#    comments2 = c.get_comments(lg)
#    print(comments2)
#     response = c.asset_consumer_get_asset_universe(lg)
#     pretty_response = json.dumps(response.json(), indent=4)
#     print(pretty_response)
# #    print (u.get('asset').get('classifications'))
#     print(c.asset_consumer_get_asset_universe(lg)['asset'].get('typeName'))
# #    asset_consumer_print_related_assets(lg)
#     cau = ConsumerAssetUniverse(c, lg)
#     print(cau)



