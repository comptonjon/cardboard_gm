
from constants import EBAY_URL_ENDPOINT, EBAY_RESULT_COUNT
import requests
from flask import jsonify
import os

def get_recent_prices(card_info):

    ebay_key = os.environ.get('EBAY_KEY')
    res = requests.get(EBAY_URL_ENDPOINT, params={'keywords'                       : card_info,
                                                  'OPERATION-NAME'                 : "findItemsByKeywords",
                                                  'SECURITY-APPNAME'               : ebay_key,
                                                  'paginationInput.entriesPerPage' : EBAY_RESULT_COUNT,
                                                  'itemFilter(0).name'             : "ListingType",
                                                  'itemFilter(0).value'            : "FixedPrice",
                                                  'RESPONSE-DATA-FORMAT'           : 'JSON',
                                                  'siteid'                         : 0,
                                                  'GLOBAL-ID'                      : 'EBAY-US',
                                                  'SERVICE-VERSION'                : '1.0.0',
                                                  'sortOrder'                      : 'EndTimeSoonest'})
    api_results = res.json()
    print(api_results)

    result_list = []

    if res.status_code == 200 and api_results['findItemsByKeywordsResponse'][0]['searchResult'][0]['@count'] != '0':

        for item in api_results['findItemsByKeywordsResponse'][0]['searchResult'][0]['item']:
            info = { 'title'    : item['title'][0],
                     'price'    : "${:,.2f}".format(float(item['sellingStatus'][0]['currentPrice'][0]['__value__'])),
                     'img_url'  : item['galleryURL'][0],
                     'ebay_url' : item['viewItemURL'][0] 
                     }
            result_list.append(info)

    return jsonify(result_list)
